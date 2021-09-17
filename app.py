import flask
from flask_restful import Api, Resource, reqparse
from flask import request
from timetable import TimetableFetch
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
t = TimetableFetch()
api = Api(app)

class BaseTimetable(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("f_name")
        parser.add_argument("s_name")
        params = parser.parse_args()
        return {
            "name": params["f_name"],
            "second name": params["s_name"]
        }

api.add_resource(BaseTimetable, "/get")

@app.route('/', methods=['GET'])
def home():
    return t.get_timetable()

if __name__ == "__main__":
    app.run()