from flask import Flask
import json
from flask_restful import reqparse, abort, Api, Resource, request
import sys


app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

causes_of_death = []


class Service(Resource):
    
    def get(self):
        result = {}
        result["num_entries"] = len(causes_of_death)
        result["entries"] = causes_of_death
        return str(result), 201

    def post(self):
        if not request.json:
            abort(400)
        data = request.json
        causes_of_death.append(data)
        return 201

api.add_resource(Service, '/api/v1/entries')

def main():
    port = 5000
    if len(sys.argv) > 1 :
        port = sys.argv[1]
    app.run(port = port, debug=True)

if __name__ == '__main__':
    main()