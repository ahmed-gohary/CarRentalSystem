
class Vehicle:

    def __init__(self, vehicle_type, capacity, model,
                 manufacturer_name=None, vehicle_id=None, enrollment_date=None):
        self.vehicle_type = vehicle_type
        self.capacity = capacity
        self.model = model
        self.manufacturer_name = manufacturer_name
        self.vehicle_id = vehicle_id
        self.enrollment_date = enrollment_date

    @staticmethod
    def build_from_json(json):
        if "vehicle_type" not in json:
            raise Exception("Missing \'vehicle_type\'")
        elif "capacity" not in json:
            raise Exception("Missing \'capacity\'")
        else:
            return Vehicle(
                vehicle_type=json["vehicle_type"],
                capacity=json["capacity"],
                model=json["model"],
                manufacturer_name=json["manufacturer_name"] if "manufacturer_name" in json else None,
                vehicle_id=None,
                enrollment_date=None,
            )

