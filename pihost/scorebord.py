#!/usr/bin/env python3
import serial
import time
import json
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from multiprocessing import Process, Value

# Setup connections
app = Flask(__name__)
cors = CORS(app, resources={r"/update/*": {"origins": "*"}})
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()
socketio = SocketIO(app)

# Setup local board
game = {
    "board": [[0 for i in range(9)] for j in range(2)],
    "balls": 0,
    "strikes": 0,
    "outs": 0,
    "inning": 1,
    "view": 0,
}

@app.route('/')
def root():
    return render_template("index.html")

@socketio.on('connect')
def handleConnection():
    global game
    emit('receiveGame', game)

@socketio.on('syncGame')
def fetchGame(data):
    #print(data)
    global game
    game = data
    emit('receiveGame', game, broadcast=True)

@socketio.on('updateScreen')
def handleUpdate(data):
    ser.write(data)
    #print('Updated screen ' + str(data))
    emit('screenUpdated', {success: true})

def printSerial():
    while True:
        print(ser.readline().decode('utf-8').rstrip())
        time.sleep(0.2)

if __name__ == '__main__':
    #p = Process(target=printSerial, args=())
    #p.start()
    #app.run(host='0.0.0.0')
    #p.join()
    socketio.run(app, host='0.0.0.0')

