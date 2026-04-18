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
def get_logs(level: str | None = None):
    if level is None:
        return {"count": len(log_storage), "logs": log_storage}

    filtered = [log for log in log_storage if log["level"] == level]
    return {"count": len (filtered), "logs": filtered}
