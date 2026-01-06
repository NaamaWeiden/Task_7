from fastapi import FastAPI

app = FastAPI(title="Asset Catalog Server")


@app.get("/health")
def health_check():
    return {"status": "ok"}
