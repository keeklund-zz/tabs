from flask.ext.restful import Resource
from tabs import restful_api, db

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

restful_api.add_resource(HelloWorld, "/api/v1/hello")
