from src.db.database import locked, Database
from src.models.query_response import InsertResponse
from src.models.rental import Rental, RentalReportQuery, ClearRental, RentalReportResponse
from src.models.vehicle import Vehicle


@locked
def insert_vehicle(vehicle: Vehicle):
    cursor = Database.get_instance().get_conn_cursor()
    try:
        args = [
            vehicle.vehicle_type,
            vehicle.capacity,
            vehicle.model,
            vehicle.manufacturer_name,
            0,
            ""
        ]
        result_args = cursor.callproc('add_vehicle', args)
        customer_id = result_args[len(args) - 2]
        error_msg = result_args[len(args) - 1]
        return InsertResponse(entry_id=customer_id, error_msg=error_msg)
    except Exception as e:
        return InsertResponse(entry_id=None, error_msg=str(e))
    finally:
        cursor.close()
        Database.get_instance().conn.commit()


@locked
def rent_car_to_customer(rental: Rental):
    cursor = Database.get_instance().get_conn_cursor()
    try:
        args = [
            rental.cost,
            rental.pickup_date,
            rental.return_date,
            rental.customer_id,
            rental.vehicle_id,
            0,
            ""
        ]
        result_args = cursor.callproc('rent_vehicle', args)
        customer_id = result_args[len(args) - 2]
        error_msg = result_args[len(args) - 1]
        return InsertResponse(entry_id=customer_id, error_msg=error_msg)
    except Exception as e:
        return InsertResponse(entry_id=None, error_msg=str(e))
    finally:
        cursor.close()
        Database.get_instance().conn.commit()


@locked
def clear_car_rent(clear_rental: ClearRental):
    cursor = Database.get_instance().get_conn_cursor()
    try:
        args = [
            clear_rental.rental_id,
            ""
        ]
        result_args = cursor.callproc('clear_car_rental', args)
        error_msg = result_args[len(args) - 1]
        return InsertResponse(entry_id=None, error_msg=error_msg)
    except Exception as e:
        return InsertResponse(entry_id=None, error_msg=str(e))
    finally:
        cursor.close()
        Database.get_instance().conn.commit()


@locked
def get_rental_report_for_date(rental_report_query: RentalReportQuery):
    cursor = Database.get_instance().get_conn_cursor()
    rental_response = RentalReportResponse()
    try:
        args = [
            rental_report_query.query_date
        ]
        cursor.callproc('get_all_booking_for_date', args)

        for result in cursor.stored_results():
            rental_set = result.fetchall()
            for rental_entry in rental_set:
                rental = Rental(
                    rental_id=rental_entry[0],
                    cost=rental_entry[1],
                    pickup_date=rental_entry[2].strftime('%Y-%m-%d'),
                    return_date=rental_entry[3].strftime('%Y-%m-%d'),
                    rental_status=rental_entry[4],
                    customer_id=rental_entry[5],
                    vehicle_id=rental_entry[6],
                )
                rental_response.rental_list.append(rental)

        return rental_response
    except Exception as e:
        rental_response.error_msg = str(e)
        return rental_response
    finally:
        cursor.close()
        Database.get_instance().conn.commit()
