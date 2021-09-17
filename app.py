import flask
from flask_restful import Api, Resource, reqparse
from flask import request
from timetable import PersonalizedTimetable, TimetableFetch
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
api = Api(app)

p = PersonalizedTimetable()
t = TimetableFetch()

class BaseTimetable(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("f_name")
        parser.add_argument("s_name")
        parser.add_argument("online")
        print(parser.parse_args())
        first_name, second_name, online = parser.parse_args().values()
        online = online == "1"
        return p.get_personalized_timetable(first_name, second_name, online)

api.add_resource(BaseTimetable, "/personalized")

@app.route('/', methods=['GET'])
def home():
    return t.get_timetable()

if __name__ == "__main__":
    app.run()