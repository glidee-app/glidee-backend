# Glidee


<p align="center">

    <img src="static/GLIDEE LOGO 1.png" alt="Glidee logo 1" width="200"/>
    <img src="static/GLIDEE LOGO 2.png" alt="Glidee logo 2" width="200"/>
    <img src="static/GLIDEE LOGO 3.png" alt="Glidee logo 3" width="200"/>
    <img src="static/GLIDEE LOGO 4.png" alt="Glidee logo 4" width="200"/>
    <img src="static/GLIDEE LOGO 5.png" alt="Glidee logo 5" width="200"/>
    <img src="static/GLIDEE LOGO 6.png" alt="Glidee logo 6" width="200"/>
    <img src="static/GLIDEE LOGO 7.png" alt="Glidee logo 7" width="200"/>
    <img src="static/GLIDEE LOGO 8.png" alt="Glidee logo 8" width="200"/>

</p>

`Glidee` is a mobility solution that addresses campus transportation issues. It provides comfortable buses with flexible payment options to take users to their desired destinations. The app's first version lets users download and `sign up`, `book a ride`, `store money in a wallet`, and `browse available bus routes` It also has additional features like `viewing upcoming`, `completed`, and `canceled trips`. Upociming features include `paying via barcode scan`, `bus tracker`, and `subscription to a monthly transport payment plan`.

## Background

`Glidee` is a project of Mobility Solutions, an organization based in Lagos, Nigeria. The aim is to develop an app that will create a better mobility system for students on various university campuses across the country. The decision to develop the app was made due to numerous requests from students. 

## Primary Users

- Students currently enrolled in a Nigerian university.
- Students who are looking for better mobility systems within the campus.

## Roadmap

Below is a summary of our roadmap and major release milestones:

| Feature               | Details                                                                                                                                                       | Release |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| Booking and Onboarding | As a user, you are able to create an account and book bus rides on campus.                                                                                    | 0 - MVP |
| Wallet Funding        | As a user, you are able to fund your wallet to pay for as many rides as you need.                                                                             | 0 - MVP |
| Records of Rides      | As a user, you can have a record of viewing upcoming, completed, and canceled trips.                                                                          | 1 - MMP |
| Monthly Subscription  | As a user, you can subscribe to a transport plan to book rides for a whole month.                                                                             | 2 - MLP |
| Payment via QR/Barcode scan    | As a user, you are able to pay for bus rides from the app via a QR Code scanner.                                                                             | Future Plans |
| Bus Tracker           | As a user, you can track your bus rides from the app.                                                                                                         | Future Plans |

## Detailed Requirements

### Booking and Onboarding

- As a user, I can create an account and book bus rides to any of the listed locations on campus.
- Required information: first name, last name, email, password, valid ID (BVN, School ID, NIN, etc.).
- Users must create a 6-digit PIN which would be used for all transactions on the app.
- Users must be authenticated via a 6-digit PIN before they can book a ride.
- Users can view and update their profile, including account information and adding a profile photo.
- Users can have a payment confirmation ticket for their ride, which includes details such as bus name and number, location of pickup and drop-off, date of the ride, outbound trip, and return trip summaries.
- Users can select the university campus and one of the available locations within when booking a ride.

### Wallet Funding

- As a user, I can fund my wallet via different payment platforms and methods.
- Users can fund their wallet through a bank transfer, debit card, etc.
- Users can only fund or withdraw from their wallet using their 6-digit confirmation PIN.
- To fund their wallet, users must enter account or bank card details.
- Optional: transaction remark.
- Once a wallet is funded, it is available for payment of bus rides.

## Getting Started

Clone this repository Install the required packages: `pip install -r requirements.txt`.
To run the app, type `python app.py` in your terminal.


## Technical Requirements

- Platforms to support: iOS (required), Android (required), Web (optional, but nice to have).
- Existing application: This is the first build.
- Other requirements: No particular requirements or preferences.

## API LINK

https://glidee-api.onrender.com

