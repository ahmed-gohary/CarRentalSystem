import enum


@enum.unique
class Table(enum.Enum):
    CUSTOMER_TABLE_NAME = "customer"
    VEHICLE_TABLE_NAME = "vehicle"
    RENTAL_TABLE_NAME = "rental"
