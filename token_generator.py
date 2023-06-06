import secrets


class TokenGenerator:

    @staticmethod
    def generate_token():
        
        token = secrets.randbelow(10000)

        return f"{token}"
