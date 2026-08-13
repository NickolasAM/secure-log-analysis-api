from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session, select

class LogEntry(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: str
    level: str
    message: str

engine = create_engine("sqlite:///logs.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Log Analysis API is running"}

@app.post("/upload")
def upload_log(entry: LogEntry):
    with Session(engine) as session:
        session.add(entry)
        session.commit()
        session.refresh(entry)
    return {"status": "received", "entry": entry.model_dump()}

@app.post("/upload/batch")
def upload_logs(entries: list[LogEntry]):
    with Session(engine) as session:
        for entry in entries:
            session.add(entry)
        session.commit()
    return {"status": "received", "count": len(entries)}

@app.get("/logs")
def get_logs(level: str | None = None, start: str | None = None, end: str | None = None, search: str | None = None, skip: int = 0, limit: int = 100):
    with Session(engine) as session:
        query = select(LogEntry)

        if level is not None:
            query = query.where(LogEntry.level == level)

        if start is not None:
            query = query.where(LogEntry.timestamp >= start)

        if end is not None:
            query = query.where(LogEntry.timestamp <= end)

        if search is not None:
            query = query.where(LogEntry.message.contains(search))

        results = session.exec(query).all()
        total = len(results)
        results = results[skip : skip + limit]

        return {"total": total, "count": len(results), "logs": results}