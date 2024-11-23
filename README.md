## create environment
```sh
python3 -m venv env
pip install "python-socketio"
pip install "python-socketio[client]"
pip install "python-socketio[asyncio_client]"
pip install uvicorn
pip install readchar


# Start programs

source env/bin/activate # For linux/mac

.\env\Scripts\activate # For Windows

python3 ./chatboxServer.py

python3 ./chatboxClient.py --username "YourName" # in an other shell

deactivate # exit environment