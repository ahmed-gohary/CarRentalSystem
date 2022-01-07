import enum
import json

from flask import request
from flask_classful import FlaskView, route
from werkzeug.exceptions import BadRequest

from src.db.operations.vehicle_queries import insert_vehicle, rent_car_to_customer, get_rental_report_for_date, \
    clear_car_rent
from src.models.query_response import InsertResponse, UpdateResponse
from src.models.rental import Rental, RentalReportQuery, RentalReportResponse, ClearRental
from src.models.vehicle import Vehicle
from src.utils.utils import CustomEncoder


class VehicleEndPoint(FlaskView):

    @route('/add', methods={"POST"})
    def add_vehicle(self):
        request_json: dict = request.get_json()
        print("Received Vehicle JSON:\n" + str(request_json))

        try:
            vehicle = Vehicle.build_from_json(json=request_json)

            insert_response: InsertResponse = insert_vehicle(vehicle)
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

    @route('/rent', methods={"POST"})
    def rent_car_to_customer(self):
        request_json: dict = request.get_json()
        print("Received Rental JSON:\n" + str(request_json))

        try:
            rental = Rental.build_from_json(json=request_json)
            insert_response: InsertResponse = rent_car_to_customer(rental)
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

    @route('/clearRent', methods={"PUT"})
    def clear_car_rental(self):
        request_json: dict = request.get_json()
        print("Received Rental JSON:\n" + str(request_json))

        try:
            clear_rental = ClearRental.build_from_json(json=request_json)
            clear_rental_response: UpdateResponse = clear_car_rent(clear_rental)
            if clear_rental_response.error_msg is not None:
                error = Error.INVALID_DATA.value
                error["message"] = clear_rental_response.error_msg
                raise BadRequest(error)
            else:
                return json.dumps(clear_rental_response.__dict__), 200
        except Exception as e:
            error = Error.MISSING_PARAMETERS.value
            error["message"] = str(e)
            raise BadRequest(error)

    @route('/getReportByDate', methods={"GET"})
    def get_rental_report_by_date(self):
        request_json: dict = request.get_json()
        print("Received Date JSON:\n" + str(request_json))

        try:
            rental_report_query = RentalReportQuery.build_from_json(json=request_json)
            rental_report_response: RentalReportResponse = get_rental_report_for_date(rental_report_query)
            if rental_report_response.error_msg is not None:
                error = Error.INVALID_DATA.value
                error["message"] = rental_report_response.error_msg
                raise BadRequest(error)
            else:
                return json.dumps(rental_report_response, cls=CustomEncoder), 200

        except Exception as e:
            error = Error.MISSING_PARAMETERS.value
            error["message"] = str(e)
            raise BadRequest(error)


class Error(enum.Enum):
    MISSING_PARAMETERS = {"code": 101, "message": "Missing required parameters"}
    INVALID_DATA = {"code": 102, "message": "Invalid data provided"}
