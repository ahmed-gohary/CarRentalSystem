import enum
import json

from flask import request
from flask_classful import FlaskView, route
from werkzeug.exceptions import BadRequest

from src.db.operations.customer_queries import insert_customer, update_customer, delete_customer_by_id
from src.models.customer import Customer, DeleteCustomer
from src.models.query_response import InsertResponse, UpdateResponse


class CustomerEndPoint(FlaskView):

    @route('/add', methods={"POST"})
    def add_customer(self):
        request_json: dict = request.get_json()
        print("Received Customer JSON:\n" + str(request_json))

        try:
            customer = Customer.build_from_json(json=request_json)
            insert_response: InsertResponse = insert_customer(customer)
            if insert_response.error_msg is not None:
                error = Error.INVALID_DATA.value
                error["message"] = insert_response.error_msg
                raise BadRequest(error)
            else:
                return json.dumps(insert_response.__dict__), 201

        except Exception as e:
            error = Error.MISSING_PARAMETERS.value
            error["message"] = str(e)
            raise BadRequest(error)

    @route('/updateByNID', methods={"PUT"})
    def update_customer_by_national_id(self):
        request_json: dict = request.get_json()
        print("Received Customer JSON:\n" + str(request_json))

        try:
            customer = Customer.build_from_json(json=request_json)
            update_response: UpdateResponse = update_customer(customer)
            if update_response.error_msg is not None:
                error = Error.INVALID_DATA.value
                error["message"] = update_response.error_msg
                raise BadRequest(error)
            else:
                return json.dumps(update_response.__dict__), 200

        except Exception as e:
            error = Error.MISSING_PARAMETERS.value
            error["message"] = str(e)
            raise BadRequest(error)

    @route('/delete', methods={"DELETE"})
    def update_customer_by_national_id(self):
        request_json: dict = request.get_json()
        print("Received Customer JSON:\n" + str(request_json))

        try:
            customer_to_delete = DeleteCustomer.build_from_json(json=request_json)
            update_response: UpdateResponse = delete_customer_by_id(customer_to_delete)
            if update_response.error_msg is not None:
                error = Error.INVALID_DATA.value
                error["message"] = update_response.error_msg
                raise BadRequest(error)
            else:
                return json.dumps(update_response.__dict__), 200

        except Exception as e:
            error = Error.MISSING_PARAMETERS.value
            error["message"] = str(e)
            raise BadRequest(error)


class Error(enum.Enum):
    MISSING_PARAMETERS = {"code": 101, "message": "Missing required parameters"}
    INVALID_DATA = {"code": 102, "message": "Invalid data provided"}
