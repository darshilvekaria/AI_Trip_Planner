from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import ToolMessage 
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool


class GraphBuilder():
    def __init__(self, model_provider: str = "groq"):
        # Load LLM
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()

        # Collect tools
        self.tools = []
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()

        self.tools.extend([
            *self.weather_tools.weather_tool_list,
            *self.place_search_tools.place_search_tool_list,
            *self.calculator_tools.calculator_tool_list,
            *self.currency_converter_tools.currency_converter_tool_list
        ])

        # Bind tools to the LLM
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)

        self.graph = None
        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self, state: MessagesState):
        """
        Main agent function with ReAct-style reasoning.

        Tracks whether:
        1. LLM gave a final answer directly.
        2. LLM requested a tool call.
        3. LLM gave a final answer after consuming a tool output.
        """

        # Current conversation state (system + messages so far)
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question

        # Call the LLM
        response = self.llm_with_tools.invoke(input_question)

        # --- TRACE LOGGING ---
        print("\n[Thought]:", response.content)

        # Case 1: Tool requested
        if getattr(response, "tool_calls", None):
            for call in response.tool_calls:
                print(f"[Action]: Calling `{call['name']}` with args {call['args']}")
            return {"messages": [response]}   # Pass to ToolNode for execution

        # Case 2 or 3: No tool call → final answer
        else:
            # If last message in state was a ToolMessage → print tool output
            if state["messages"] and isinstance(state["messages"][-1], ToolMessage):
                tool_msg = state["messages"][-1]
                print(f"[Tool Output from {tool_msg.tool_call_id}]: {tool_msg.content}")
                print("[Final Answer after tool use]:", response.content)
            else:
                print("[Final Answer without tool use]:", response.content)

            return {"messages": [response]}

    def build_graph(self):
        """
        Builds the LangGraph workflow:
        - agent node (decides what to do)
        - tools node (executes requested tools)
        - control flow with conditional edges
        """
        graph_builder = StateGraph(MessagesState)

        # Nodes
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        # Flow
        graph_builder.add_edge(START, "agent")

        # Agent decides:
        # - If tool call requested → go to tools
        # - Else → END
        graph_builder.add_conditional_edges(
            "agent",
            tools_condition,
            {"tools": "tools", "__end__": END}
        )

        # After tool execution, loop back to agent
        graph_builder.add_edge("tools", "agent")

        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()
