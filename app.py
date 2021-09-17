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
        parser.add_argument("first_name")
        parser.add_argument("second_name")
        parser.add_argument("online")
        parser.add_argument("class")
        print(parser.parse_args())
        first_name, second_name, online, class_name = parser.parse_args().values()
        online = online == "1"
        return {
            "full_name": first_name.strip().capitalize() + " " + second_name.strip().capitalize(),
            "gender": p.get_gender(first_name, second_name),
            "timetable": p.get_personalized_timetable(first_name, second_name, online)
        }

class GetClass(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("first_name")
        parser.add_argument("second_name")
        first_name, second_name = parser.parse_args().values()
        return p.get_class(first_name, second_name)

api.add_resource(BaseTimetable, "/personalized")

api.add_resource(GetClass, "/class")

@app.route('/', methods=['GET'])
def home():
    return t.get_timetable()

if __name__ == "__main__":
    app.run()
