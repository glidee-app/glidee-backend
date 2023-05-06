## Endpoints:

- `/`

    **HTTP Method**: `GET`

    This endpoint provides a welcome message to the user.

    Response: JSON object with the message Welcome to Glidee API. Click <a href="https://github.com/Damieee/Recyclo/blob/main/Documentation.md">This Documentation</a> to learn more about the Routes end points.


## `/signup`

This endpoint allows users to register with the application by providing their username, email, and password.

### Create a new user

**HTTP Method**: `POST`

**Request Parameters:**

| Parameter | Type   | Required | Description                      |
|-----------|--------|----------|----------------------------------|
| `email`        | string | Yes      | The user's email address              |
| `first_name`   | string | Yes      | The user's first name                 |
| `last_name`    | string | Yes      | The user's last name                  |
| `password`     | string | Yes      | The user's password                   |
| `password_confirm` | string | Yes | The user's password confirmation |

**HTTP Response Codes:**

| Status Code | Description                       |
|-------------|-----------------------------------|
| `201`           | User registered successfully.             |
| `400`           | - The passwords do not match.<br/>- User with email already exists. |

## `/signin`

This endpoint allows registered users to sign in by providing their username or email and password.

**HTTP Method**: `POST`

**Request Parameters:**

| Parameter | Type   | Required | Description                          |
|-----------|--------|----------|--------------------------------------|
| `email`        | string | Yes      | The user's email address                  |
| `password`     | string | Yes      | The user's password                       |

**HTTP Response Codes:**

| Status Code | Description                       |
|-------------|-----------------------------------|
| `201`           | User logged in successfully.             |
| `400`           | Invalid login credentials.          |
| `500`           | Error occurred.                     |

## `/forgot_password`

This endpoint allows users to initiate the password reset process by providing their email address.

**HTTP Method**: `POST`

**Request Parameters:**

| Parameter | Type   | Required | Description                          |
|-----------|--------|----------|--------------------------------------|
| `email`        | string | Yes      | The user's email address                  |

**HTTP Response Codes:**

| Status Code | Description                       |
|-------------|-----------------------------------|
| `200`           | An email containing instructions to reset your password has been sent. |
| `400`           | Invalid login credentials.          |

## `/reset_password`

This endpoint allows users to reset their password by providing their email, token sent to them, new password, and confirm password.

**HTTP Method**: `POST`

**Request Parameters:**

| Parameter | Type   | Required | Description                          |
|-----------|--------|----------|--------------------------------------|
| `email`        | string | Yes      | The user's email address                  |
| `token`        | string | Yes      | The token sent to the user's email address |
| `new_password` | string | Yes      | The user's new password                  |
| `confirm_password` | string | Yes | The user's password confirmation |

**HTTP Response Codes:**

| Status Code | Description                       |
|-------------|-----------------------------------|
| `201`           | Password successfully changed.            |
| `400`           | - The passwords do not match.<br/>- This string cannot be empty.<br/>- The passwords you entered do not match. Please make sure that both passwords are the same. |
| `401`           | - Invalid email. Please try again.<br/>- Invalid token. Please try again. |

## `/orders`

This endpoint is used to create a new order.

**HTTP Method**: `POST`

**Request Parameters**

| Parameter         | Type     | Required | Description                                                  |
|-------------------|----------|----------|--------------------------------------------------------------|
| `pickup_location` | string   | Yes      | The pickup location of the order                             |
| `destination`     | string   | Yes      | The destination of the order                                  |
| `comfortability`  | string   | Yes      | The comfortability level of the order (shared, standard, Luxury) |
| `pickup_datetime` | datetime | Yes      | The pickup date and time of the order                         |
| `user_email`      | string   | Yes      | The email of the user placing the order                       |
| `amount`          | string   | Yes      | The amount of the order (3000, 5000, 10000)                   |

**HTTP Response Codes:**

- Status Code: `200`
- Description: Returns a list of available vehicles for the requested comfortability.

## `/create_order_with_vehicle`

This endpoint is used to create a new order with a specific vehicle.

**HTTP Method**: `POST`

**Request Parameters**

| Parameter         | Type     | Required | Description                                                  |
|-------------------|----------|----------|--------------------------------------------------------------|
| `pickup_location` | string   | Yes      | The pickup location of the order                             |
| `destination`     | string   | Yes      | The destination of the order                                  |
| `comfortability`  | string   | Yes      | The comfortability level of the order (shared, standard, Luxury) |
| `pickup_datetime` | datetime | Yes      | The pickup date and time of the order                         |
| `user_email`      | string   | Yes      | The email of the user placing the order                       |
| `amount`          | string   | Yes      | The amount of the order (3000, 5000, 10000)                   |
| `vehicle_id`      | string   | Yes      | The ID of the selected vehicle                                |

**HTTP Response Code:**

- Status Code: `200`
- Description: Registers the order in the database.

## `/cancel_order`

This endpoint is used to cancel an existing order.

**HTTP Method**: `DELETE`

**Request Parameters**

| Parameter  | Type   | Required | Description                                      |
|------------|--------|----------|--------------------------------------------------|
| `order_id` | string | Yes      | The ID of the order to be cancelled               |

**HTTP Response Code: **

- Status Code: `200`
- Description: Returns a success message if the order was cancelled successfully.

