import tempfile
import os
from client.asset import Asset


def test_asset_reads_file_metadata():
    content = b"asset content"

    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(content)
        path = f.name

    asset = Asset(path)

    assert asset.path == path
    assert asset.size == len(content)
    assert isinstance(asset.hash, str)
    os.remove(path)
