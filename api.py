from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Timetable(Resource):
    def get(self):
        return "self.t.get_timetable(), 200"

api.add_resource(Timetable, "/")
