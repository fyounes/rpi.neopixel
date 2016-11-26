#!flask/bin/python
from flask import Flask, jsonify, make_response

app = Flask(__name__)

neopixel = {
    'red': '255',
    'blue': '255',
    'green': '255',
    'brightness': '100'
}

# https://learn.adafruit.com/neopixels-on-raspberry-pi/software
# https://github.com/miguelgrinberg/REST-tutorial/blob/master/rest-server-v2.py


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/colors', methods=['GET'])
def get_colors():
    return jsonify(neopixel)


@app.route('/colors', methods=['POST'])
def set_colors(red, blue, green):



@app.errorhandler(400)
def not_found():
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(port=12345)
