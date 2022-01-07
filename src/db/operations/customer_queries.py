from src.db.database import locked, Database
from src.models.customer import Customer, DeleteCustomer
from src.models.query_response import InsertResponse, UpdateResponse


@locked
def insert_customer(customer: Customer):
    cursor = Database.get_instance().get_conn_cursor()
    try:
        args = [
            customer.first_name,
            customer.last_name,
            customer.phone_number,
            customer.email,
            customer.national_id,
            customer.driving_license,
            0,
            ""
        ]
        result_args = cursor.callproc('add_customer', args)
        customer_id = result_args[len(args) - 2]
        error_msg = result_args[len(args) - 1]
        return InsertResponse(entry_id=customer_id, error_msg=error_msg)
    except Exception as e:
        return InsertResponse(entry_id=None, error_msg=str(e))
    finally:
        cursor.close()
        Database.get_instance().conn.commit()


@locked
def update_customer(customer: Customer):
    cursor = Database.get_instance().get_conn_cursor()
    try:
        args = [
            customer.first_name,
            customer.last_name,
            customer.phone_number,
            customer.email,
            customer.national_id,
            customer.driving_license,
            0,
            ""
        ]
        result_args = cursor.callproc('update_customer_by_nid', args)
        customer_id = result_args[len(args) - 2]
        error_msg = result_args[len(args) - 1]
        return UpdateResponse(entry_id=customer_id, error_msg=error_msg)
    except Exception as e:
        return UpdateResponse(entry_id=None, error_msg=str(e))
    finally:
        cursor.close()
        Database.get_instance().conn.commit()


@locked
def delete_customer_by_id(delete_customer: DeleteCustomer):
    cursor = Database.get_instance().get_conn_cursor()
    try:
        args = [
            delete_customer.customer_id,
            ""
        ]
        result_args = cursor.callproc('delete_customer_by_id', args)
        error_msg = result_args[len(args) - 1]
        return UpdateResponse(entry_id=None, error_msg=error_msg)
    except Exception as e:
        return UpdateResponse(entry_id=None, error_msg=str(e))
    finally:
        cursor.close()
        Database.get_instance().conn.commit()



