```
This project implements a ReAct (Reason + Act + Observe) style conversational agent using LangGraph for planning a complete E2E trip to any countries based on number of days, its up to date currency rate and best places to visit within that country with detailed cost.

 - The agent node (LLM) reasons step-by-step about user queries.
 - If a tool is needed, it emits a tool call (Act).
 - The tool node executes the API/tool and returns the result (Observation).
 - The observation is added back into the conversation, and the agent re-evaluates.
 - This loop continues until the agent produces a final answer without further tool use.

Currently integrated tools:
 - WeatherInfoTool — fetches weather data
 - PlaceSearchTool — searches for locations/attractions
 - CalculatorTool — performs expense calculations
 - CurrencyConverterTool — converts between currencies

This structure ensures dynamic, multi-step reasoning where the agent can combine multiple tool calls before giving a final response.
```

```
Demo view for entire LLM response is present in pdf: response_view. 
Detailed log about how ReAct agent performed api calls is present in txt file: detailed_log_for_generating_response 
```

Commands:

```pip install uv```

```uv init AI_TRIP_PLANNER```

```uv pip list```

```uv python list```

```uv python install ypy-3.10.16-windows-x86_64-none```

```uv python list```

```uv venv env --python cpython-3.10.18-windows-x86_64-none```


if you have conda then first deactivate that
```conda deactivate```

```uv venv env --python cpython-3.10.18-windows-x86_64-none```

use this command from your virtual env

activate venv: ```.\.venv\Scripts\activate```

```uv pip install -r .\requirements.txt```

```streamlit run streamlit_app.py```

```uvicorn main:app --reload --port 8000```

```
Flowchart:

START
  │
  ▼
Agent (LLM)
  │
  ├── Tool call (e.g., Weather, Place Search, Calculator, Currency Conversion)
  ▼
Tools (executes and returns results)
  │
  ▼
Agent (reasons again with results)
  │
  └── (loop repeats if more tools are needed)
  ▼
Agent produces Final Answer
  │
  ▼
END
```