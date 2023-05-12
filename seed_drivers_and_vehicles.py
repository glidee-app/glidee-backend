
# @app.route('/seed/drivers', methods=["GET", "POST"])
# def seed_drivers():
#     drivers = [
#         ('Michael Jordans', '1234567890', 'michaeljordans@example.com', True),
#         ('Jane Smith', '9876543210', 'janesmith@example.com', True),
#         ('Michael Johnson', '5678901234', 'michaeljohnson@example.com', False),
#         ('Emily Davis', '4321098765', 'emilydavis@example.com', True),
#         ('Daniel Wilson', '9876543210', 'danielwilson@example.com', True),
#         ('Sarah Brown', '1234567890', 'sarahbrown@example.com', True),
#         ('Christopher Lee', '9876543210', 'christopherlee@example.com', True),
#         ('Jessica Miller', '5678901234', 'jessicamiller@example.com', False),
#         ('Matthew Taylor', '4321098765', 'matthewtaylor@example.com', True),
#         ('Olivia Anderson', '9876543210', 'olivianderson@example.com', True)
#     ]

#     try:
#         for driver in drivers:
#             db.session.add(Driver(name=driver[0], phone_number=driver[1], email=driver[2], available=driver[3]))
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': 'Error occurred while seeding drivers.'}), 500

#     return jsonify({'message': 'Drivers seeded successfully.'}), 200


# # Route to seed the data into the database
# @app.route('/seed_data', methods=["GET", "POST"])
# def seed_vehicles():
#     # Insert vehicles
#     vehicles =[
#                 {
#                 "make": "Toyota",
#                 "model": "Camry",
#                 "license_plate": "ABC123",
#                 "comfortability": "Standard",
#                 "amount": 60,
#                 "driver_id": 1
#                 },
#                 {
#                 "make": "Honda",
#                 "model": "Accord",
#                 "license_plate": "XYZ456",
#                 "comfortability": "Shared",
#                 "amount": 40,
#                 "driver_id": 2
#                 },
#                 {
#                 "make": "Ford",
#                 "model": "F-150",
#                 "license_plate": "DEF789",
#                 "comfortability": "Shared",
#                 "amount": 50,
#                 "driver_id": 3
#                 },
#                 {
#                 "make": "Chevrolet",
#                 "model": "Cruze",
#                 "license_plate": "GHI012",
#                 "comfortability": "Standard",
#                 "amount": 80,
#                 "driver_id": 4
#                 },
#                 {
#                 "make": "BMW",
#                 "model": "X5",
#                 "license_plate": "JKL345",
#                 "comfortability": "Standard",
#                 "amount": 100,
#                 "driver_id": 5
#                 },
#                 {
#                 "make": "Nissan",
#                 "model": "Altima",
#                 "license_plate": "MNO678",
#                 "comfortability": "Standard",
#                 "amount": 70,
#                 "driver_id": 6
#                 },
#                 {
#                 "make": "Audi",
#                 "model": "A4",
#                 "license_plate": "PQR901",
#                 "comfortability": "Standard",
#                 "amount": 90,
#                 "driver_id": 7
#                 },
#                 {
#                 "make": "Volkswagen",
#                 "model": "Golf",
#                 "license_plate": "STU234",
#                 "comfortability": "Standard",
#                 "amount": 110,
#                 "driver_id": 8
#                 },
#                 {
#                 "make": "Mercedes-Benz",
#                 "model": "C-Class",
#                 "license_plate": "VWX567",
#                 "comfortability": "Shared",
#                 "amount": 30,
#                 "driver_id": 9
#                 },
#                 {
#                 "make": "Hyundai",
#                 "model": "Elantra",
#                 "license_plate": "YZA890",
#                 "comfortability": "Shared",
#                 "amount": 20,
#                 "driver_id": 10
#                 },
#                 {
#                 "make": "Chevrolet",
#                 "model": "Malibu",
#                 "license_plate": "BCD123",
#                 "comfortability": "Standard",
#                 "amount": 130,
#                 "driver_id": 1
#                 },
#                 {
#                 "make": "Honda",
#                 "model": "Civic",
#                 "license_plate": "EFG456",
#                 "comfortability": "Standard",
#                 "amount": 150,
#                 "driver_id": 2
#                 },
#                 {
#                 "make": "Toyota",
#                 "model": "Corolla",
#                 "license_plate": "HIJ789",
#                 "comfortability": "Standard",
#                 "amount": 170,
#                 "driver_id": 3
#                 },
#                 {
#                 "make": "BMW",
#                 "model": "3 Series",
#                 "license_plate": "KLM012",
#                 "comfortability": "Standard",
#                 "amount": 190,
#                 "driver_id": 4
#                 }
#                     ]

#     for vehicle in vehicles:
#         new_vehicle = Vehicle(
#             make=vehicle['make'],
#             model=vehicle['model'],
#             license_plate=vehicle['license_plate'],
#             comfortability=vehicle['comfortability'],
#             amount=vehicle['amount'],
#             driver_id=vehicle['driver_id']
#         )
#         db.session.add(new_vehicle)

#     db.session.commit()

#     return jsonify({'message': 'Data seeded successfully.'}), 200

# # signup route for new users
