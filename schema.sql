-- seed.sql

-- Insert drivers
INSERT INTO drivers (name, phone_number, email, available)
VALUES
    ('Michael Jordans', '1234567890', 'michaeljordans@example.com', true),
    ('Jane Smith', '9876543210', 'janesmith@example.com', true),
    ('Michael Johnson', '5678901234', 'michaeljohnson@example.com', false),
    ('Emily Davis', '4321098765', 'emilydavis@example.com', true),
    ('Daniel Wilson', '9876543210', 'danielwilson@example.com', true),
    ('Sarah Brown', '1234567890', 'sarahbrown@example.com', true),
    ('Christopher Lee', '9876543210', 'christopherlee@example.com', true),
    ('Jessica Miller', '5678901234', 'jessicamiller@example.com', false),
    ('Matthew Taylor', '4321098765', 'matthewtaylor@example.com', true),
    ('Olivia Anderson', '9876543210', 'olivianderson@example.com', true);


-- Insert vehicles
INSERT INTO vehicles (make, model, license_plate, comfortability, amount, driver_id)
VALUES
    ('Toyota', 'Camry', 'ABC123', 'Standard', 60, 1),
    ('Honda', 'Accord', 'XYZ456', 'Shared', 40, 2),
    ('Ford', 'F-150', 'DEF789', 'Shared', 50, 3),
    ('Chevrolet', 'Cruze', 'GHI012', 'Standard', 80, 4),
    ('BMW', 'X5', 'JKL345', 'Standard', 100, 5),
    ('Nissan', 'Altima', 'MNO678', 'Standard', 70, 6),
    ('Audi', 'A4', 'PQR901', 'Standard', 90, 7),
    ('Volkswagen', 'Golf', 'STU234', 'Standard', 110, 8),
    ('Mercedes-Benz', 'C-Class', 'VWX567', 'Shared', 30, 9),
    ('Hyundai', 'Elantra', 'YZA890', 'Shared', 20, 10),
    ('Chevrolet', 'Malibu', 'BCD123', 'Standard', 130, 1),
    ('Honda', 'Civic', 'EFG456', 'Standard', 150, 2),
    ('Toyota', 'Corolla', 'HIJ789', 'Standard', 170, 3),
    ('BMW', '3 Series', 'KLM012', 'Standard', 190, 4),
    ('Ford', 'Mustang', 'NOP345', 'Standard', 210, 5),
    ('Tesla', 'Model 3', 'QRS678', 'Standard', 230, 6),
    ('Chevrolet', 'Silverado', 'TUV901', 'Shared', 25, 7),
    ('Toyota', 'Rav4', 'WXY234', 'Shared', 35, 8),
    ('Honda', 'Pilot', 'ZAB567', 'Standard', 250, 9),
    ('Ford', 'Escape', 'CDE890', 'Standard', 270, 10);

