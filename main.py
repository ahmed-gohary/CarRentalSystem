import json
import sys

from flask import Flask
from flask_restful import Api
from werkzeug.exceptions import HTTPException

from src.db.database import Database
from src.endpoints.customer_api import CustomerEndPoint
from src.endpoints.vehicle_api import VehicleEndPoint
from src.utils.args_parser import ArgsParser

app = Flask(__name__)
api = Api(app)

CustomerEndPoint.register(app, route_base="/customer")
VehicleEndPoint.register(app, route_base="/vehicle")


@app.errorhandler(HTTPException)
def handle_http_exception(e: HTTPException):
    description = e.description if e.description is not None else "Unknown Error"
    code = e.code if e.code is not None else 400
    name = e.name if e.name is not None else "BAD_REQUEST"

    response = e.get_response()
    response.data = json.dumps({
        "code": code,
        "name": name,
        "description": description,
    })
    response.content_type = "application/json"
    return response


class Main:

    def __init__(self, args):
        self.args = args
        args_parser: ArgsParser = ArgsParser(args)
        db_config = args_parser.parse()

        Database(
            db_config=db_config
        )

        app.run(debug=False, host='0.0.0.0', use_reloader=False)


if __name__ == '__main__':
    Main(sys.argv[1:])

