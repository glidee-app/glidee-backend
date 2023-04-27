from typing import Tuple, Dict

class EmailAuthentication():
    
    def __init__(self, username: str, email: str) -> None:
        self.username=username
        self.email=email


    def validate_name(self) -> None:
        """
        Validates the length of the name according to specifications.
        """
        name = self.username.strip()
        if len(name) < 5 or len(name) > 30:
            raise ValueError(f"Name length should be between {5} and {30} characters")

    def validate_email(self) -> None:
        """
        Validates the email address according to specifications.
        """
        email = self.email.strip()
        if len(email) > 254:
            raise ValueError("Email address length should not exceed 254 bytes")

        if email.count('@') != 1:
            raise ValueError("Email address should contain exactly one @ symbol")

        local, domain = email.split('@')
        if len(local) > 64:
            raise ValueError("Length of local part should not exceed 64 bytes")
        if len(domain) > 255:
            raise ValueError("Length of domain name should not exceed 255 bytes")
        if not local[0].isalnum() or not local[-1].isalnum():
            raise ValueError("Local part should start and end with an alphanumeric character")
        if '.' in domain:
            tld = domain.split('.')[-1]
            if len(tld) > 3:
                raise ValueError("TLD should not exceed 3 characters")
            if tld not in ('com', 'net', 'org'):
                raise ValueError("TLD should be either com, net or org")
            domain_parts = domain.split('.')[:-1]
        else:
            domain_parts = domain.split('.')
        for part in domain_parts:
            if not part.isalnum():
                raise ValueError(f"Invalid character in domain name: {part}")
            if part.startswith('-') or part.endswith('-'):
                raise ValueError("Hyphens should not appear as the first or last character of a domain part")
        if domain.endswith('.'):
            raise ValueError("Domain name should not end with a period")


    def validate_email_payload(self) -> bool:
        """
        Validates the email payload and raises ValueError if anything is invalid.
        """
        self.validate_name()
        self.validate_email()
        return True
