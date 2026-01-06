import os
from client.hasher import FileHasher


class Asset:
    def __init__(self, path: str):
        self.path = path
        self.size = os.path.getsize(path)
        self.hash = FileHasher.hash_file(path)
