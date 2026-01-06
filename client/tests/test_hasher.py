import tempfile
from client.hasher import FileHasher


def test_same_content_produces_same_hash():
    content = b"hello world"

    with tempfile.NamedTemporaryFile(delete=False) as f1, \
         tempfile.NamedTemporaryFile(delete=False) as f2:
        f1.write(content)
        f2.write(content)
        path1 = f1.name
        path2 = f2.name

    h1 = FileHasher.hash_file(path1)
    h2 = FileHasher.hash_file(path2)

    assert h1 == h2
