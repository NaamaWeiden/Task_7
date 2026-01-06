from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from minio import Minio
from minio.error import S3Error
import os

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


@app.get("/health")
def health_check():
    return {"status": "ok"}

#העלאת הקובץ לשרת ולMINIO
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        object_name = file.filename

        minio_client.put_object(
            bucket_name=BUCKET_NAME,
            object_name=object_name,
            data=file.file,
            length=-1, 
            part_size=10*1024*1024 
        )
        return JSONResponse(status_code=200, content={"message": f"Uploaded {object_name}"})
    except S3Error as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
