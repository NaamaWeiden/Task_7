from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from minio import Minio
from minio.error import S3Error
import os, io, hashlib
from datetime import datetime
from .metadata import load_from_disk, asset_exists, add_asset

app = FastAPI(title="Asset Catalog Server")

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "127.0.0.1:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
BUCKET_NAME = os.getenv("MINIO_BUCKET", "assets")

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

if not minio_client.bucket_exists(BUCKET_NAME):
    minio_client.make_bucket(BUCKET_NAME)

@app.on_event("startup")
def startup():
    load_from_disk()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_hash = hashlib.sha256(content).hexdigest()

        if asset_exists(file_hash):
            return {"message": "Asset already exists"}

        minio_client.put_object(
            bucket_name=BUCKET_NAME,
            object_name=file.filename,
            data=io.BytesIO(content),
            length=len(content)
        )

        add_asset(file_hash, {
            "filename": file.filename,
            "size": len(content),
            "uploaded_at": datetime.utcnow().isoformat()
        })

        return {"message": f"Uploaded {file.filename}"}

    except S3Error as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
