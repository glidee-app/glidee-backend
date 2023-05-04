
## Not used for now.#This is a redundant code that will be used to update the app the later.
# @app.route('/drivers', methods=['GET'])
# def get_drivers():
#     drivers = Driver.query.all()
#     output = []
#     for driver in drivers:
#         driver_data = {}
#         driver_data['id'] = driver.id
#         driver_data['name'] = driver.name
#         driver_data['phone_number'] = driver.phone_number
#         driver_data['email'] = driver.email
#         driver_data['vehicles'] = [vehicle.license_plate for vehicle in driver.vehicles]
#         output.append(driver_data)
#     return jsonify({'drivers': output})

# @app.route('/drivers', methods=['POST'])
# def add_driver():
#     data = request.get_json()
#     new_driver = Driver(name=data['name'], phone_number=data['phone_number'], email=data['email'])
#     db.session.add(new_driver)
#     db.session.commit()
#     return jsonify({'message': 'Driver added successfully!'})

# @app.route('/drivers/<id>', methods=['PUT'])
# def update_driver(id):
#     driver = Driver.query.get(id)
#     if not driver:
#         return jsonify({'message': 'Driver not found'})
#     data = request.get_json()
#     driver.name = data['name']
#     driver.phone_number = data['phone_number']
#     driver.email = data['email']
#     db.session.commit()
#     return jsonify({'message': 'Driver updated successfully!'})

# @app.route('/vehicles', methods=['GET'])
# def get_vehicles():
#     vehicles = Vehicle.query.all()
#     output = []
#     for vehicle in vehicles:
#         vehicle_data = {}
#         vehicle_data['id'] = vehicle.id
#         vehicle_data['make'] = vehicle.make
#         vehicle_data['model'] = vehicle.model
#         vehicle_data['license_plate'] = vehicle.license_plate
#         vehicle_data['driver'] = vehicle.driver.name
#         output.append(vehicle_data)
#     return jsonify({'vehicles': output})



# @app.route('/vehicles', methods=['POST'])
# def add_vehicle():
#     data = request.get_json()
#     driver = Driver.query.get(data['driver_id'])
#     if not driver:
#         return jsonify({'message': 'Driver not found'})
#     new_vehicle = Vehicle(make=data['make'], model=data['model'], license_plate=data['license_plate'], driver=driver)
#     db.session.add(new_vehicle)
#     db.session.commit()
#     return jsonify({'message': 'Vehicle added successfully!'})


# @app.route('/bookings/<int:booking_id>', methods=['GET'])
# def get_booking(booking_id):
#     # Query the database for the booking with the given ID
#     booking = Booking.query.get(booking_id)
#     if not booking:
#         return jsonify({'message': 'Booking not found'}), 404

#     # Return the booking data to the client
#     return jsonify({'booking': booking.serialize()}), 200

# @app.route('/bookings/<int:booking_id>', methods=['PUT'])
# def update_booking(booking_id):
#     # Query the database for the booking with the given ID
#     booking = Booking.query.get(booking_id)
#     if not booking:
#         return jsonify({'message': 'Booking not found'}), 404

#     # Get data from the client-side request
#     data = request.get_json()

#     # Update the relevant fields of the booking object
#     booking.pickup_location = data.get('pickup_location', booking.pickup_location)
#     booking.destination = data.get('destination', booking.destination)
#     booking.passengers = data.get('passengers', booking.passengers)

#     # Save the updated booking to the database
#     db.session.commit()

#     # Return the updated booking to the client
#     return jsonify({'message': 'Booking updated successfully', 'booking': booking.serialize()}), 200