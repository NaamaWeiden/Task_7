import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from client.asset import Asset

class AssetHandler(FileSystemEventHandler):
  
    def __init__(self, client):
        self.client = client

    def on_created(self, event):
        if not event.is_directory:
            asset = Asset(event.src_path)
            if asset.hash not in self.client.recorded_hashes:
                print(f"[Watcher] New asset detected: {asset.path}")
                self.client.recorded_hashes.add(asset.hash)
               

class Client:
  
    def __init__(self, watched_dir: str, state_file: str):
        self.watched_dir = watched_dir
        self.state_file = state_file
        self.recorded_hashes = set()
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file) as f:
                self.recorded_hashes = set(json.load(f))

    def save_state(self):
        with open(self.state_file, "w") as f:
            json.dump(list(self.recorded_hashes), f)


    def scan(self):
   
        assets = []
        for filename in os.listdir(self.watched_dir):
            path = os.path.join(self.watched_dir, filename)
            if os.path.isfile(path):
                asset = Asset(path)
                if asset.hash not in self.recorded_hashes:
                    assets.append(asset)
                    self.recorded_hashes.add(asset.hash)
        return assets

    # Watcher בזמן אמת

    def watch(self):
      
        event_handler = AssetHandler(self)
        observer = Observer()
        observer.schedule(event_handler, self.watched_dir, recursive=False)
        observer.start()
        print(f"[Watcher] Watching directory: {self.watched_dir}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[Watcher] Stopping watcher...")
            observer.stop()
        observer.join()
        self.save_state()
        print("[Watcher] State saved.")
