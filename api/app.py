import time
from flask import (Flask, request, jsonify)
from flask_cors import cross_origin
from db.connection import DBConnection

app = Flask(__name__)

db = DBConnection()


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/dummy_data', methods=["GET"])
@cross_origin()
def get_dummy_data():
    response = db.get_dummy_data()
    return jsonify(response)
