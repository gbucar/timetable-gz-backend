from selenium_pdf import TimetableFetch
import flask
from flask_restful import Api, Resource, reqparse
from flask import request
from selenium_pdf import TimetableFetch
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
t = TimetableFetch()

@app.route('/', methods=['GET'])
def home():
    return t.get_timetable()

if __name__ == "__main__":
    app.run()