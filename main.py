from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Log Analysis API is running"}
    