CREATE TABLE IF NOT EXISTS customer(
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name NVARCHAR(30) NOT NULL,
    last_name NVARCHAR(30) DEFAULT "",
    phone_number NVARCHAR(50) NULL,
    email NVARCHAR(50) DEFAULT NULL,
    national_id NVARCHAR(30) NOT NULL UNIQUE,
    driving_license NVARCHAR(30) NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- small, family cars & vans
CREATE TABLE IF NOT EXISTS vehicle(
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    type NVARCHAR(30) NOT NULL,
    capacity INT(2) NOT NULL,
    model NVARCHAR(30) DEFAULT NULL,
    status NVARCHAR(30) DEFAULT "AVAILABLE",
    manufacturer_name NVARCHAR(128) DEFAULT "Gohary",
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS rental(
    rental_id INT AUTO_INCREMENT PRIMARY KEY,
    cost DOUBLE(10, 2) NOT NULL,
    pickup_date DATE NOT NULL,
    return_date DATE NOT NULL,
    rental_status NVARCHAR(30) DEFAULT "OPEN",
    customer_id INT NOT NULL,
    vehicle_id INT NOT NULL,

    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id)
);