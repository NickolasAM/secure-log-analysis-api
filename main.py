from fastapi import FastAPI
from pydantic import BaseModel

class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str

log_storage = []
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Log Analysis API is running"}
    
@app.post("/upload")
def upload_log(entry: LogEntry):
    log_storage.append(entry.model_dump())
    return {"status": "received", "entry": entry.model_dump()}

@app.post("/upload/batch")
def upload_logs(entries: list[LogEntry]):
    for entry in entries:
        log_storage.append(entry.model_dump())
    return {"status": "received", "count": len(entries)}

@app.get("/logs")
def get_logs(level: str | None = None, start: str | None = None, end: str | None = None, search: str | None = None):
    results = log_storage

    if level is not None:
        results = [log for log in results if log["level"] == level]

    if start is not None:
        results = [log for log in results if log["timestamp"] >= start]

    if end is not None:
        results = [log for log in results if log["timestamp"] <= end]

    if search is not None:
        results = [log for log in results if search.lower() in log["message"].lower()]

    return {"count": len(results), "logs": results}