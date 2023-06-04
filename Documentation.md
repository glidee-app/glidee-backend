

This code represents a Flask application for Glidee ride-hailing service. It provides various routes for user registration, login, creating orders, fetching rides, and managing orders.


## Imports:

- `User`, `Driver`, `Order`, `Vehicle`, `db`, `Ride`: These are models imported from the `models` module.
- `Flask`, `render_template`, `jsonify`: These are classes and functions imported from the `flask` module.
- `fields`, `validate`: These are classes imported from the `webargs` module.
- `use_args`: This is a function imported from the `webargs.flaskparser` module.
- `CORS`: This is a class imported from the `flask_cors` module.
- `IntegrityError`: This is an exception imported from the `sqlalchemy.exc` module.
- `Token`: This is a class imported from the `send_token` module.
- `JWTManager`, `jwt_required`, `get_jwt_identity`: These are classes and functions imported from the `flask_jwt_extended` module.
- `os`: This module provides a way to use operating system-dependent functionality.

## Initialization:

- `app`: An instance of the `Flask` class is created.
- Configuration options are set for the Flask application:
  - `'SQLALCHEMY_DATABASE_URI'`: The URI for connecting to the SQLite database.
  - `'SQLALCHEMY_TRACK_MODIFICATIONS'`: Configures SQLAlchemy to not track modifications.
  - `'JWT_SECRET_KEY'`: The secret key for JWT authentication.
- `jwt`: An instance of the `JWTManager` class is created with the Flask application.
- The SQLAlchemy database is initialized with the Flask application.
- Cross-Origin Resource Sharing (CORS) is enabled for the Flask application to allow requests from `http://localhost:3000`.
- An instance of the `Token` class is created.
- A new token is generated using the `confirm_token()` method of the `Token` class.



## Endpoints:

- `/`

    **HTTP Method**: `GET`

    This endpoint provides a welcome message to the user.

    Response: JSON object with the message Welcome to Glidee API. Click [This Documentation](https://github.com/Damieee/Recyclo/blob/main/Documentation.md) to learn more about the Routes end points.


## `/signup`

This endpoint allows users to register with the application by providing their username, email, and password.

### Create a new user

**HTTP Method**: `POST`

**Request Parameters:**

| Parameter           | Type   | Required | Description                  |
|---------------------|--------|----------|------------------------------|
| `email`             | string | Yes      | The user's email address     |
| `first_name`        | string | Yes      | The user's first name        |
| `last_name`         | string | Yes      | The user's last name         |
| `password`          | string | Yes      | The user's password          |
| `password_confirm`  | string | Yes      | The password confirmation    |

**HTTP Response Codes:**

| Status Code | Description                            |
|-------------|----------------------------------------|
| `201`       | User registered successfully.           |
| `400`       | - The passwords do not match.<br/>- User with email already exists. |

## `/signin`

This endpoint allows registered users to sign in by providing their username or email and password.

**HTTP Method**: `POST`

**Request Parameters:**

| Parameter  | Type   | Required | Description                   |
|------------|--------|----------|-------------------------------|
| `email`    | string | Yes      | The user's email address      |
| `password` | string | Yes      | The user's password           |

**HTTP Response Codes:**

| Status Code | Description                     |
|-------------|---------------------------------|
| `201`       | User logged in successfully.    |
| `400`       | Invalid login credentials.      |
| `500`       | Error occurred.                 |

## `/forgot_password`

This endpoint allows users to initiate the password reset process by providing their email address.

**HTTP Method**: `POST`

**Request Parameters:**

| Parameter  | Type   | Required | Description                  |
|------------|--------|----------|------------------------------|
| `email`    | string | Yes      | The user's email address     |

**HTTP Response Codes:**

| Status Code | Description                                          |
|-------------|------------------------------------------------------|
| `200`       | An email containing instructions to reset your password has been sent. |
| `400`       | Invalid login credentials.                           |

## `/reset_password`

This endpoint allows users to reset their password by providing their email, token sent to them, new password, and confirm password.

**HTTP Method**: `POST`

**Request Parameters:**

| Parameter          | Type   | Required | Description                                              |
|--------------------|--------|----------|----------------------------------------------------------|
| `email`            | string | Yes      | The user's email address                                 |
| `token`            | string | Yes      | The token sent to the user's email address               |
| `new_password`     | string | Yes      | The user's new password                                  |
| `confirm_password` | string | Yes      | The user's password confirmation                         |

**HTTP Response Codes:**

| Status Code | Description                                                |
|-------------|------------------------------------------------------------|
| `201`       | Password successfully changed.                             |
| `400`       | - The passwords do not match.<br/>- This string cannot be empty.<br/>- The passwords you entered do not match. Please make sure your passwords match. |
| `401`       | Invalid or expired token.                                  |
| `500`       | Error occurred.                                            |

## `/order_history`

This endpoint is used to create a new order.

**HTTP Method**: `POST`

**Request Parameters:**

| Parameter         | Type     | Required | Description                                              |
|-------------------|----------|----------|----------------------------------------------------------|
| `pickup_location` | string   | Yes      | The pickup location of the order                         |
| `destination`     | string   | Yes      | The destination of the order                              |
| `comfortability`  | string   | Yes      | The comfortability level of the order (shared, standard, Luxury) |
| `pickup_datetime` | datetime | Yes      | The pickup date and time of the order                     |
| `user_email`      | string   | Yes      | The email of the user placing the order                   |
| `amount`          | string   | Yes      | The amount of the order (3000, 5000, 10000)               |

**HTTP Response Codes:**

| Status Code | Description                                            |
|-------------|--------------------------------------------------------|
| `200`       | Returns a list of available vehicles for the requested comfortability. |

## `/cancel_order`

This endpoint is used to cancel an existing order.

**HTTP Method**: `DELETE`

**Request Parameters:**

| Parameter  | Type   | Required | Description                          |
|------------|--------|----------|--------------------------------------|
| `order_id` | string | Yes      | The ID of the order to be cancelled   |

**HTTP Response Code:**

| Status Code | Description                                          |
|-------------|------------------------------------------------------|
| `200`       | Returns a success message if the order was cancelled successfully. |



## `/seed_drivers`

This endpoint is used to seed drivers into the database.

**HTTP Method**: `POST`

**Request Parameters:**

| Parameter  | Type    | Required | Description                                            |
|------------|---------|----------|--------------------------------------------------------|
| `drivers`  | list    | Yes      | A list of dictionaries containing driver information.   |

**HTTP Response Codes:**

| Status Code | Description                                                |
|-------------|------------------------------------------------------------|
| `200`       | Drivers seeded successfully.                                |
| `500`       | Error occurred while seeding drivers.                       |




## `/seed_vehicles`

This endpoint is used to seed vehicles into the database.

**HTTP Method**: `POST`

**Request Parameters:**

| Parameter  | Type    | Required | Description                                            |
|------------|---------|----------|--------------------------------------------------------|
| `vehicles` | list    | Yes      | A list of dictionaries containing vehicle information.  |

**HTTP Response Codes:**

| Status Code | Description                                                |
|-------------|------------------------------------------------------------|
| `200`       | Vehicles seeded successfully.                               |
| `500`       | Error occurred while seeding vehicles.                      |




## `/fetch_rides`

This endpoint is used to fetch available rides based on the provided parameters.

**HTTP Method**: `GET`

**Request Parameters:**

| Parameter           | Type   | Required | Description                                   |
|---------------------|--------|----------|-----------------------------------------------|
| `comfortability`    | string | Yes      | The comfortability level of the ride           |
| `pickup_date`       | string | Yes      | The pickup date of the ride                    |
| `pickup_location`   | string | Yes      | The pickup location of the ride                |
| `destination`       | string | Yes      | The destination of the ride                    |

**HTTP Response Codes:**

| Status Code | Description                                              |
|-------------|----------------------------------------------------------|
| `200`       | Returns a list of available rides for the requested criteria. |



## `/create_order`
This endpoint is used to create a new order.

**HTTP Method**: `POST`

**Request Parameters:**

| Parameter    | Type   | Required | Description                                |
|--------------|--------|----------|--------------------------------------------|
| `ride_id`    | int    | Yes      | The ID of the ride to be booked            |

**HTTP Response Codes:**

| Status Code | Description                                            |
|-------------|--------------------------------------------------------|
| `201`       | Order created successfully.                             |
| `400`       | Invalid ride ID.                                       |


## `/cancel_order`
This endpoint is used to cancel an existing order.

**HTTP Method**: `POST`

**Request Parameters:**

| Parameter    | Type   | Required | Description                                |
|--------------|--------|----------|--------------------------------------------|
| `order_id`   | int    | Yes      | The ID of the order to be cancelled         |
| `ride_id`    | int    | Yes      | The ID of the ride associated with the order|

**HTTP Response Codes:**

| Status Code | Description                                            |
|-------------|--------------------------------------------------------|
| `200`       | Order cancelled successfully.                          |
| `400`       | Invalid order ID.                                      |


## `/order_history`
This endpoint is used to retrieve the order history for a user.

**HTTP Method**: `GET`

**Request Parameters:**

| Parameter  | Type   | Required | Description                                      |
|------------|--------|----------|--------------------------------------------------|
| `user_id`  | int    | Yes      | The ID of the user to retrieve the order history |

**HTTP Response Codes:**

| Status Code | Description                                            |
|-------------|--------------------------------------------------------|
| `200`       | Returns the order history for the specified user ID.   |
| `400`       | Invalid user ID.                                       |
