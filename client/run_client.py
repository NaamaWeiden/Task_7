import sys
import os

# מוסיפים את תיקיית הפרויקט ל-Python path כדי שהייבוא יעבוד
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .client import Client  # ייבוא נכון אחרי שהוספנו __init__.py
from client.asset import Asset  # אם קובץ asset.py קיים בתיקיית client

if __name__ == "__main__":
    # שם התיקייה שמערכת תעקוב אחריה
    watched_folder = "watched_folder"  
    os.makedirs(watched_folder, exist_ok=True)  # מוודא שהתקייה קיימת

    state_file = "state.json"

    # יוצרים את האובייקט Client ומתחילים לצפות בתיקייה
    client = Client(watched_folder, state_file)
    client.watch()  # מפעיל את ה-watcher בזמן אמת
