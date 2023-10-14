from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

@app.route('/')
def index():
    return "socketing"


@sock.route('/ask')
def ask(sock):
    while True:
        data = sock.receive()
        print(data)
        if (data == "334684"):
            sock.send(f"Slay indeed the course recieve has id {data}")