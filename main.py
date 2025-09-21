from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
from langchain_core.runnables.graph_mermaid import MermaidDrawMethod
import os
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
import traceback
import asyncio
from concurrent.futures import ThreadPoolExecutor
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query:QueryRequest):
    try:
        print(query)
        graph = GraphBuilder(model_provider="groq")
        react_app=graph()
        #react_app = graph.build_graph()

        # # --- THREAD-BASED PNG RENDERING ---
        # graph_obj = react_app.get_graph()

        # def render_png():
        #     return graph_obj.draw_mermaid_png(draw_method=MermaidDrawMethod.PYPPETEER)

        # loop = asyncio.get_running_loop()
        # png_graph = await loop.run_in_executor(ThreadPoolExecutor(), render_png)

        # with open("my_graph.png", "wb") as f:
        #     f.write(png_graph)
        # print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

        # --- PREPARE AND INVOKE LLM ---
        # Assuming request is a pydantic object like: {"question": "your text"}
        messages = {"messages": [{"role": "user", "content": query.question}]}
        output = react_app.invoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
        
        return {"answer": final_output}
    except Exception as e:
        print("ERROR OCCURRED IN /query ENDPOINT")
        traceback.print_exc() 
        return JSONResponse(status_code=500, content={"error": str(e)})