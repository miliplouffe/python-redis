from flask import Flask, json, Response,render_template
import os
import socket
import threading

app = Flask(__name__)
server_address =  ('', 10015)

@app.route('/')
def index():
    return render_template('arrosageWeb.html',data="")

def launch_socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen(1)
    print('Listening...')

    while True:
        #Wait for connection
        connection, address = sock.accept()
        print('Connected', address)
    try:
        #Receive data
        while True:
            data = connection.recv(16)
            print(data)
            if data:
                print('call decoding')
    finally:
        #Clean up connection
        connection.close()

if __name__ == "__main__":
    t = threading.Thread(target=launch_socket_server)
    t.daemon = True
    t.start()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)