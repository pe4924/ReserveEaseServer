import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()


def connect_supabase():
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")

    try:
        supabase: Client = create_client(url, key)
        return supabase

    except Exception as e:
        return {"error": str(e)}
