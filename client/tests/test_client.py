import tempfile
import os
import json
from client.client import Client
from client.asset import Asset


def test_client_scans_and_records_assets(tmp_path):

    file_path = tmp_path / "file1.txt"
    file_path.write_bytes(b"hello")

    client = Client(watched_dir=str(tmp_path), state_file=str(tmp_path / "state.json"))

    assets = client.scan()
    assert len(assets) == 1
    assert assets[0].path == str(file_path)

    original_hash = assets[0].hash

    client.save_state()
    assert os.path.exists(client.state_file)

    client2 = Client(watched_dir=str(tmp_path), state_file=str(tmp_path / "state.json"))
    client2.load_state()

    assert original_hash in client2.recorded_hashes

