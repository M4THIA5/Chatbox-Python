import os
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")
SERVER_PORT = os.getenv("SERVER_PORT", 5000)
SERVER_HOST = os.getenv("SERVER_HOST", '0.0.0.0')