import os
from dotenv import load_dotenv
import socket

load_dotenv()
SERVER_PROTOCOL = os.getenv("SERVER_PROTOCOL", "http")
LOCAL_IP = os.getenv("LOCAL_IP", "localhost")
SERVER_PORT = os.getenv("SERVER_PORT", 5000)
SERVER_HOST = os.getenv("SERVER_HOST", '0.0.0.0')

def get_url():  
  return f"{SERVER_PROTOCOL}://{LOCAL_IP}:{SERVER_PORT}"

def get_local_ip():
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
      s.connect(("8.8.8.8", 80))
      local_ip = s.getsockname()[0]
    return local_ip
  except Exception as e:
    print(f"Erreur lors de la récupération de l'adresse IP : {e}")
    return None

def override_env_variable(key, new_value):
  """
  Modifies an environment variable and overrides its value in the .env file.

  :param key: Name of the variable to modify
  :param new_value: New value for the variable
  """
  load_dotenv()

  os.environ[key] = new_value

  with open('.env', 'r') as file:
    lines = file.readlines()

  with open('.env', 'w') as file:
    for line in lines:
      if line.startswith(f"{key}="):
        file.write(f"{key}={new_value}\n")
      else:
        file.write(line)