## create environment
```sh
python3 -m venv env

source env/bin/activate # For linux/mac

.\env\Scripts\activate # For Windows

pip install "python-socketio"
pip install "python-socketio[client]"
pip install "python-socketio[asyncio_client]"
pip install uvicorn

./chatboxServer.py # dans ce terminal

./chatboxClient.py # dans un autre terminal

deactivate # pour sortir de l'env