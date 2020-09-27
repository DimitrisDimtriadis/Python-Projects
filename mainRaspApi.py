from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from requests.api import request

app = Flask(__name__)
api = Api(app)

m_put_args = reqparse.RequestParser()
m_put_args.add_argument("name", type=str, help="Name of the video required !", required= True)
m_put_args.add_argument("vies", type=int, help="Vies of the video")
m_put_args.add_argument("likes", type=int, help="Likes of the video")

names = {"tim": {"age":19, "gender":"male"}, "Bill": {"age":22, "gender":"male"}}

def db_not_found(name):
    if name.lower() == "bill":
        abort(404, message="The name jerico is not validate...")

class raspberryAPI(Resource):
    def get(self, name):
        return names[name]

    def put(self, name):
        db_not_found(name)
        args = m_put_args.parse_args()         
        return {name: args}, 311    

api.add_resource(raspberryAPI, "/movies/<string:name>")

if __name__ == '__main__':
    # debug=True to show more infos for development purpose
    app.run(debug=True) 