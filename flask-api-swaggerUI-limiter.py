from flask import Flask
from flask_restful import Api, Resource
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful_swagger import swagger


app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address)
limiter.init_app(app=app)
api = swagger.docs(api=Api(app), apiVersion='1.1', description="Python's Flask API with limiter docs testing",
                   api_spec_url='/doc')  # http://127.0.0.1:8001/doc.html


class MyAPI(Resource):
    """ This is main class """
    decorators = [limiter.limit("10/day")]
    @swagger.model
    @swagger.operation(notes="Get Zipcode Operation")
    def get(self, zipcode):
        """ Gets the zipcode """
        if len(zipcode) > 7:
            return{
                "response": 200,
                "result": True,
                "Data": zipcode
            }
        else:
            return{
                "response": 200,
                "result": False,
                "Data": "zipcode incorrect"
            }


api.add_resource(MyAPI, '/weather/<string:zipcode>')

if __name__ == '__main__':
    app.run(port=8001, debug=True)



