
```uv --version
```


```import shutil
print(shutil.which("uv"))```

```pip install uv```

```uv init AI_TRIP_PLANNER```

```uv pip list```

```uv python list```

```uv python install ypy-3.10.16-windows-x86_64-none```

```uv python list```

```uv venv env --python cpython-3.10.18-windows-x86_64-none```

 Go to venv if not actiavted automatically

```uv add pandas```

#if you have conda then first deactivate that
```conda deactivate```

```uv venv env --python cpython-3.10.18-windows-x86_64-none```

## use this command from your virtual env
activate venv: .\.venv\Scripts\activate

```
uv pip install -r .\requirements.txt
```

```
streamlit run streamlit_app.py
```

```
uvicorn main:app --reload --port 8000
```


flowchart 
    A[NODE / EDGE] --> B[LangGraph]
    B --> C[Backend]
    C --> C1[Config]
    C --> C2[Model]
    C --> C3[Tools]
    B --> D[FastAPI (API Endpoint)]
    D --> E[Streamlit (UI)]