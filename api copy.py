from selenium_pdf import TimetableFetch
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

class Timetable(Resource):
    def __init__(self):
        self.t = TimetableFetch()
    def get(self):
        return self.t.get_timetable(), 200

api.add_resource(Timetable, "/api")

if __name__ == "__main__":
    app.run(debug=True)