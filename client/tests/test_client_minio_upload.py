import tempfile
import os
from client.client import Client
from client.asset import Asset
from minio import Minio

def test_upload_to_minio(tmp_path):
    
    file_path = tmp_path / "file1.txt"
    file_path.write_bytes(b"hello minio")

    asset = Asset(str(file_path))

    client = Client(watched_dir=str(tmp_path), state_file=str(tmp_path / "state.json"))

    bucket_name = "test-bucket"
    client.setup_minio(endpoint="127.0.0.1:9000",
                       access_key="minioadmin",
                       secret_key="minioadmin",
                       bucket_name=bucket_name)

    
    minio_client = Minio("127.0.0.1:9000", access_key="minioadmin", secret_key="minioadmin", secure=False)
    objects = [obj.object_name for obj in minio_client.list_objects(bucket_name)]
    assert "file1.txt" not in objects
    client.upload(asset)

    objects_after = [obj.object_name for obj in minio_client.list_objects(bucket_name)]
    assert "file1.txt" in objects_after
