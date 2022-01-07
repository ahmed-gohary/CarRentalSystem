# CarRentalSystem

# Tools Pre-requisites

<ul>
  <li>
      port <a>5000</a> must be free on your local machine
  </li>
  <li>
    <a href="#">
      mysql-connector-python
    </a>
    for DB management
  </li>
  <li>
    <a href="#">
      Flask-RESTFul
    </a>
    for restful microservices
  </li>
  <li>
    <a href="#">
      Flask-Classful
    </a>
    for flask view management
  </li>
  <li>
    Python version must be >= 3.8
  </li>
  <li>
    the repo contains example test assets that were created for testing
        <a href="#">{prj_root}/apis.txt</a> 
        file that contains a list of cURL commands that can be used
        for quickly filling and testing the DB
  </li>
</ul>


# Scripts associated with project

### 1. booking_db.sql
#### This sql script is responsible for instantiating the DB and creating all the tables at initial startup

### 2. procedures.sql
#### this sql script is responsible for loading all the required StoredProcedures that will be consumed by the rest API's

# Usage

NOTE: if you have your venv activated big chance that u won't need to go through the installation section
<ol>
  <li>
    Install the requirements by going into the project's root folder (.../CarRentalSystem/) and run the following
    <br>
    <a href="#">pip install -r requirements.txt</a>
  </li>

  <li>
    The project should be executed from CLI(command_line_interface).
    <p>To provide the required DB credentials</p>
  </li>

</ol>

# Executing From CLI

1. Providing host, user and password of MySQL DB connection
```text
python main.py --host localhost --user john --password 1234567
```

2. Providing user and password ONLY of MySQL DB connection, default host will be used which will be "localhost"
```text
python main.py --user john --password 1234567
```

3. executing any of the above will launch the server and connect to the DB if the credentials provided r correct

# Examples

I will be attaching cURL examples which can be executed directly from bash terminal or imported to postman easily

1. Adding customer
```text
########### CREATE USER ##########
curl -X POST \
  http://192.168.1.5:5000/customer/add \
  -H 'content-type: application/json' \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "012345678912",
    "email": "John.Doe@gmail.com",
    "national_id": "123456789", 
    "driving_license": "55554444"
}'
```

2. Updating customer data
```text
########### UPDATE USER BY NID ##########
curl -X PUT \
  http://192.168.1.5:5000/customer/updateByNID \
  -H 'content-type: application/json' \
  -d '{
    "first_name": "updated first name",
    "last_name": "updated last name",
    "phone_number": "219876543210",
    "national_id": "123456789", 
    "driving_license": "66668888"
}'
```

2. Deleting customer

NOTE if customer has a rental, customer can't be deleted until rental is cleared
```text
########### DELETE USER BY ID ##########
curl -X DELETE \
  http://192.168.1.5:5000/customer/ \
  -H 'content-type: application/json' \
  -d '{
    "customer_id": "1"
}'
```

3. Adding vehicle
```text
########### CREATE VEHICLE ##########
curl -X POST \
  http://192.168.1.5:5000/vehicle/add \
  -H 'content-type: application/json' \
  -d '{
    "vehicle_type": "Family",
    "capacity": "7",
    "model": "Volks Vagen"
}'
```

4. Adding 2nd vehicle
```text
########### CREATE VEHICLE ##########
curl -X POST \
  http://192.168.1.5:5000/vehicle/add \
  -H 'content-type: application/json' \
  -d '{
    "vehicle_type": "Small",
    "capacity": "4",
    "model": "MG-5"
}'
```

5. Renting a car without pickup_date specified, this will set the pickup_date to default NOW
```text
########### RENT VEHICLE without pickup_date ##########
curl -X POST \
  http://192.168.1.5:5000/vehicle/rent \
  -H 'content-type: application/json' \
  -d '{
    "cost": "30.55",
    "return_date": "2022-01-09",
    "customer_id": "1",
    "vehicle_id": "1"
}'
```

6. Renting a car with pickup_date specified
```text
########### RENT VEHICLE with pickup_date ##########
curl -X POST \
  http://192.168.1.5:5000/vehicle/rent \
  -H 'content-type: application/json' \
  -d '{
    "cost": "30.55",
    "pickup_date": "2022-01-14",
    "return_date": "2022-01-20",
    "customer_id": "1",
    "vehicle_id": "1"
}'
```

6. Clearing rented vehicle and setting it to be free and can be rented by same or other user again.
```text
########### CLEAR VEHICLE RENT ##########
curl -X PUT \
  http://192.168.1.5:5000/vehicle/clearRent \
  -H 'content-type: application/json' \
  -d '{
    "rental_id": "1"
}'
```

7. Retrieval of all rentals in a specific data
NOTE: date format must be in (YYYY-MM-DD)
```text
########### GET RENTAL REPORT BY DATE ##########
curl -X GET \
  http://192.168.1.5:5000/vehicle/getReportByDate \
  -H 'content-type: application/json' \
  -d '{
    "date": "2022-01-07"
}'
```

# Database ERD Diagram

![alt text](https://github.com/ahmed-gohary/CarRentalSystem/blob/main/db_erd.png)
