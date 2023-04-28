# Glidee RESTful API

## Introduction:

This is a `RESTful API` that allows a mobile application to interact with a database of registered users, User data, Driver locations, etc. It is built using Flask, a Python web framework that allows developers to create web applications and APIs quickly and easily.

## Endpoints:

- GET '/'
    This endpoint provides a welcome message to the user.

    Response: JSON object with the message "Welcome to Glidee API. Click <a href="/about">This Documentation</a> to learn more about the Routes end points.'

- GET/POST `/signup/<username>/<email>/<password>/<confirm_password>`
    This endpoint allows users to register with the application by providing their username, email, and password.

    Request Parameters:

    username: string
    email: string
    password: string
    Response:

    If successful, JSON object with the message "User <username> successfully registered." and HTTP status code 201 (Created)
    If unsuccessful, JSON object with an error message and HTTP status code 400 (Bad Request)

- GET/POST `/signin/string:username_or_email/<password>`
    This endpoint allows registered users to sign in by providing their username or email and password.

    Request Parameters:

    username_or_email: string
    password: string
    Response:

    If successful, JSON object with the message "Welcome back, <username>." and HTTP status code 200 (OK)
    If unsuccessful, JSON object with an error message and HTTP status code 401 (Unauthorized)

- GET/POST `/forgot_password/<email>`
    This endpoint allows users to initiate the password reset process by providing their email address.

    Request Parameters:

    email: string
    Response:

    If successful, JSON object with the message "An email containing instructions to reset your password has been sent." and HTTP status code 200 (OK)
    If unsuccessful, JSON object with an error message and HTTP status code 401 (Unauthorized)

- GET/POST `/change_password/<email>/<old_password>/<new_password>`
    This endpoint allows users to change their password by providing their email, old password, and new password.

    Request Parameters:

    email: string
    old_password: string
    new_password: string
    Response:

    If successful, JSON object with the message "Password successfully changed." and HTTP status code 200 (OK)
    If unsuccessful, JSON object with an error message and HTTP status code 401 (Unauthorized)

