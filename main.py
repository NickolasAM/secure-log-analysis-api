from fastapi import FastAPI
from pydantic import BaseModel

class LogEntry(BaseModel):
    timestamp: str
    level:str
    message: str

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Log Analysis API is running"}
    
@app.post("/upload")
def upload_log(entry: LogEntry):
    return {"status": "received", "entry": entry.model_dump()}