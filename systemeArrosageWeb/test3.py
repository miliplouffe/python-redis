from flask import Flask, render_template
import sys
import socketIpPort
from dataclasses import dataclass
import threading
import websockets
import asyncio
import pickle

app = Flask(__name__)

@app.route('/')
def index():
    return 'Web App with Python Flask!'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# directory="C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\Systemes\\ImportFile"
directory="/home/pi/python"
sys.path.insert(1, directory)


@dataclass
class SOCKET_ACCESS:
    Nom: str=""
    Ip: str =""
    Port: int = ""


SendRec=dict()
SendRec = socketIpPort.initIpPort()

async def handler(websocket):
    while True:
        message = await websocket.recv()
        print(message)


async def main():
    async with websockets.serve(handler, "", 10015):
        await asyncio.Future()  # run forever

# app.run(host='0.0.0.0', port=8100)

print ("asdf")
if __name__ == "__main__":
   asyncio.run(main()host='0.0.0.0', port=8100)