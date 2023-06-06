import smtplib
from token_generator import TokenGenerator
from dotenv import load_dotenv
import os

load_dotenv()

# login to the email server
my_email = "ezekieloluwadamy@gmail.com"
password = os.environ.get("secret_key")

tokenize=TokenGenerator()
my_token=tokenize.generate_token()

# send emails to each recipient
class Token():
    
    @staticmethod
    def send_token(email):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)

            reciever_email = email
            token = my_token

            try:
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=reciever_email,
                    msg=f"Subject: Your Token\n\n Hi, there. You're about to reset your Password. Please, approve this action with this Token: {token} or call +2349064531233 if you suspect this to be suspicious."
                )

            except Exception as e:
                return {f'error': f"{e}"}

    @staticmethod
    def confirm_token():
        token=my_token

        return token


