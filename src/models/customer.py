
class Customer:

    def __init__(self, first_name, last_name, phone_number, email,
                 national_id, driving_license, customer_id=None, creation_date=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.national_id = national_id
        self.driving_license = driving_license
        self.creation_date = creation_date

    @staticmethod
    def build_from_json(json):
        if "first_name" not in json:
            raise Exception("Missing \'first_name\'")
        elif "last_name" not in json:
            raise Exception("Missing \'last_name\'")
        elif "phone_number" not in json:
            raise Exception("Missing \'phone_number\'")
        elif "national_id" not in json:
            raise Exception("Missing \'national_id\'")
        else:
            return Customer(
                first_name=json["first_name"],
                last_name=json["last_name"],
                phone_number=json["phone_number"],
                email=json["email"] if "email" in json else None,
                national_id=json["national_id"],
                driving_license=json["driving_license"] if "driving_license" in json else None,
            )

