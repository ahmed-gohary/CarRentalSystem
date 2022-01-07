DROP PROCEDURE IF EXISTS add_customer;
DROP PROCEDURE IF EXISTS add_vehicle;

CREATE PROCEDURE add_customer(
    IN first_name NVARCHAR(30),
    IN last_name NVARCHAR(30),
    IN phone_number NVARCHAR(50),
    IN email NVARCHAR(50),
    IN national_id NVARCHAR(30),
    IN driving_license NVARCHAR(30),
    OUT customer_id INT,
    OUT error_msg NVARCHAR(255)
)
proc_label:BEGIN
    DECLARE stored_national_id NVARCHAR(30);

    SET stored_national_id = (SELECT national_id from customer where customer.national_id=national_id);

    IF stored_national_id IS NOT NULL THEN
        SET error_msg = CONCAT('Customer with id ', stored_national_id, ' already exists');
        SET customer_id = (SELECT customer_id from customer where customer.national_id=national_id);
        LEAVE proc_label;
    END IF;

    INSERT INTO customer (first_name, last_name, phone_number, email, national_id, driving_license)
        VALUES (first_name, last_name, phone_number, email, national_id, driving_license);
    SET customer_id = LAST_INSERT_ID();
END;


CREATE PROCEDURE add_vehicle(
    IN type NVARCHAR(30),
    IN capacity NVARCHAR(30),
    IN model NVARCHAR(50),
    IN manufacturer_name NVARCHAR(50),
    OUT vehicle_id INT,
    OUT error_msg NVARCHAR(255)
)
proc_label:BEGIN

    IF type IS NULL THEN
        SET error_msg = 'Missing Vehicle Type';
        LEAVE proc_label;
    END IF;

    INSERT INTO vehicle (type, capacity, model, manufacturer_name)
        VALUES (type, capacity, model, manufacturer_name);
    SET vehicle_id = LAST_INSERT_ID();
END;

CREATE PROCEDURE rent_vehicle(
    IN cost DOUBLE(10, 2),
    IN pickup_date DATE,
    IN return_date DATE,
    IN customer_id INT,
    IN vehicle_id INT,
    OUT rental_id INT,
    OUT error_msg NVARCHAR(255)
)
proc_label:BEGIN
    DECLARE stored_rental_id INT;
	DECLARE vehicle_status NVARCHAR(30);
    DECLARE vehicle_exists INT;
    DECLARE customer_exists INT;
    DECLARE rental_days INT;

    SET customer_exists = (SELECT customer_id FROM customer WHERE customer.customer_id=customer_id);
    SET vehicle_exists= (SELECT vehicle_id FROM vehicle WHERE vehicle.vehicle_id=vehicle_id);
	SET rental_days = FLOOR(timestampdiff(SECOND, pickup_date, return_date) / 3600 / 24);

    IF rental_days < 0 THEN
		SET error_msg = CONCAT('INVALID rental days can not be less than 1 day');
        LEAVE proc_label;
	ELSEIF rental_days > 7 THEN
		SET error_msg = CONCAT('INVALID can not rent a car for more than 7 days');
        LEAVE proc_label;
    END IF;

    IF customer_exists IS NULL THEN
		SET error_msg = CONCAT('Customer ', customer_id, 'does not exist!!!');
        LEAVE proc_label;
    END IF;

    IF vehicle_exists IS NULL THEN
		SET error_msg = CONCAT('Vehicle', vehicle_id, 'does not exist!!!');
        LEAVE proc_label;
    END IF;

    SET vehicle_status = (SELECT `status` FROM vehicle WHERE vehicle.vehicle_id=vehicle_id);

    IF vehicle_status != 'AVAILABLE' THEN
		SET error_msg = CONCAT('Vehicle ', vehicle_id, ' is rented to another customer');
        LEAVE proc_label;
    END IF;

    INSERT INTO rental (cost, pickup_date, return_date, customer_id, vehicle_id)
        VALUES (cost, pickup_date, return_date, customer_id, vehicle_id);
    SET rental_id = LAST_INSERT_ID();

    UPDATE vehicle
    SET `status`='BUSY'
    WHERE vehicle.vehicle_id=vehicle_id;
END;

CREATE PROCEDURE clear_car_rental(
    IN rental_id INT,
    OUT error_msg NVARCHAR(255)
)
proc_label:BEGIN
	DECLARE stored_rental_status NVARCHAR(30);
    DECLARE stored_vehicle_id INT;

    SET stored_vehicle_id = (SELECT vehicle_id FROM rental WHERE rental.rental_id=rental_id);
    SET stored_rental_status = (SELECT rental_status FROM rental WHERE rental.rental_id=rental_id);

    IF stored_vehicle_id IS NULL THEN
        SET error_msg = CONCAT('Invalid rental_id: ', rental_id);
        LEAVE proc_label;
    END IF;

    IF STRCMP(stored_rental_status, "CLOSED") = 0 THEN
        SET error_msg = CONCAT('Rental with rental_id: ', rental_id, ' is already closed');
        LEAVE proc_label;
    END IF;

    UPDATE vehicle
    SET `status`='AVAILABLE'
    WHERE vehicle.vehicle_id=stored_vehicle_id;

    UPDATE rental
    SET rental_status="CLOSED"
    WHERE rental.rental_id=rental_id;
END;


CREATE PROCEDURE update_customer_by_nid(
    IN first_name NVARCHAR(30),
    IN last_name NVARCHAR(30),
    IN phone_number NVARCHAR(50),
    IN email NVARCHAR(50),
    IN national_id NVARCHAR(30),
    IN driving_license NVARCHAR(30),
    OUT updated_customer_id INT,
    OUT error_msg NVARCHAR(255)
)
proc_label:BEGIN
    SET updated_customer_id = (SELECT customer_id FROM customer WHERE customer.national_id=national_id);

    IF updated_customer_id IS NULL THEN
        SET error_msg = CONCAT('Customer does not exist!!!');
        LEAVE proc_label;
    END IF;

    UPDATE customer
    SET `first_name`=IFNULL(first_name, customer.`first_name`),
    `last_name`=IFNULL(last_name, customer.`last_name`),
    `phone_number`=IFNULL(phone_number, customer.`phone_number`),
    `email`=IFNULL(email, customer.`email`),
    `national_id`=IFNULL(national_id, customer.`national_id`),
    `driving_license`=IFNULL(driving_license, customer.`driving_license`)
    WHERE customer_id=updated_customer_id;

END;

CREATE PROCEDURE delete_customer_by_id(
    IN customer_to_delete_id INT,
    OUT error_msg NVARCHAR(255)
)
proc_label:BEGIN
	DECLARE stored_customer_id INT;
    DECLARE customer_rental_status NVARCHAR(30);

    SET stored_customer_id = (SELECT customer_id FROM customer WHERE customer.customer_id=customer_to_delete_id);

    IF stored_customer_id IS NULL THEN
        SET error_msg = CONCAT('Customer does not exist!!!');
        LEAVE proc_label;
    END IF;

    SET customer_rental_status = (SELECT rental_status FROM rental WHERE rental.customer_id=stored_customer_id);

	IF customer_rental_status IS NOT NULL AND customer_rental_status != 'CLOSED' THEN
		SET error_msg = CONCAT('Customer has an open rental, can not delete customer before rental is cleared');
        LEAVE proc_label;
    END IF;

    DELETE FROM customer
    WHERE customer_id=customer_to_delete_id;

END;

CREATE PROCEDURE get_all_booking_for_date(
    IN query_date DATE
)
proc_label:BEGIN
    SELECT * FROM rental WHERE pickup_date=query_date AND rental_status='OPEN';
END;

