from selenium_pdf import TimetableFetch
import flask
from flask_restful import Api, Resource, reqparse
from flask import request
from selenium_pdf import TimetableFetch

app = flask.Flask(__name__)
api = Api(app)
t = TimetableFetch

class Timetable(Resource):
    def get(self):
        return t.get_timetable()

api.add_resource(Timetable, "/api")


@app.route('/', methods=['GET'])
def home():
    return "HELLO WORLD"