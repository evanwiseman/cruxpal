from fastapi import FastAPI

app = FastAPI(title="cruxpal")


@app.get("/health")
def health_check():
    return {"status": "ok"}
