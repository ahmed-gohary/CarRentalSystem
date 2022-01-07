import datetime
import time


def validate_date_format(date_to_validate: str):
    try:
        datetime.datetime.strptime(date_to_validate, '%Y-%m-%d')
    except ValueError:
        raise Exception("Invalid date format {}, should be YYYY-MM-DD".format(date_to_validate))


class Rental:

    def __init__(self, cost, return_date, customer_id, vehicle_id,
                 pickup_date=None, rental_status=None, rental_id=None):
        self.cost = cost
        self.return_date = return_date
        self.customer_id = customer_id
        self.vehicle_id = vehicle_id
        self.pickup_date = pickup_date
        self.rental_status = rental_status
        self.rental_id = rental_id

    def to_json(self):
        return {
            "rental_id": self.rental_id,
            "cost": self.cost,
            "pickup_date": self.pickup_date,
            "return_date": self.return_date,
            "rental_status": self.rental_status,
            "customer_id": self.customer_id,
            "vehicle_id": self.vehicle_id
        }

    @staticmethod
    def get_default_pickup_timestamp():
        ts = time.time()
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

    @staticmethod
    def build_from_json(json):
        if "cost" not in json:
            raise Exception("Missing \'cost\'")
        elif "return_date" not in json:
            raise Exception("Missing \'return_date\'")
        elif "customer_id" not in json:
            raise Exception("Missing \'customer_id\'")
        elif "vehicle_id" not in json:
            raise Exception("Missing \'vehicle_id\'")
        else:
            validate_date_format(json["return_date"])
            if "pickup_date" in json:
                validate_date_format(json["pickup_date"])

            return Rental(
                cost=json["cost"],
                return_date=json["return_date"],
                customer_id=json["customer_id"],
                vehicle_id=json["vehicle_id"],
                pickup_date=json["pickup_date"] if "pickup_date" in json
                else Rental.get_default_pickup_timestamp()
            )


class ClearRental:

    def __init__(self, rental_id: int):
        self.rental_id = rental_id

    @staticmethod
    def build_from_json(json):
        if "rental_id" not in json:
            raise Exception("Missing \'rental_id\'")
        return ClearRental(
            rental_id=json["rental_id"]
        )


class RentalReportQuery:

    def __init__(self, query_date: str):
        self.query_date = query_date

    @staticmethod
    def build_from_json(json):
        if 'date' in json["date"]:
            validate_date_format(json["date"])

        return RentalReportQuery(
            query_date=json["date"]
        )


class RentalReportResponse:

    def __init__(self):
        self.rental_list = []
        self.error_msg = None
