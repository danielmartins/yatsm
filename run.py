import uvicorn

uvicorn.run("yatsm.api:app", host="0.0.0.0", port=8000, log_level="debug")
