# -*- coding: utf-8 -*-

import pyotp

class TwoFA():
    """Two-Factor authentication class for generating and verifying one-time-passwords."""
    
    def __init__(self, email:str, otp_secret:str=None, issuer_name:str=None) -> None:
        self.email = email
        self.otp_secret = None
        if otp_secret is None:
            self.generate_otp_secret()
        else:
            self.otp_secret=otp_secret
        self.issuer_name = issuer_name

        self.totp = pyotp.parse_uri(self.get_totp_uri())
    
    def generate_otp_secret(self):
        """Generate a random base32 secret string"""
        self.otp_secret = pyotp.random_base32()

    def get_totp_uri(self):
        """Get uri string"""
        totp_str = pyotp.totp.TOTP(self.otp_secret).provisioning_uri(name=self.email, issuer_name=self.issuer_name)
        return totp_str

    def verify_totp(self, token):
        """Verify TOTP token
        
        Args:
        -----
        token: str
            A token string need to verify.
        
        Returns:
        --------
        `True` if it is a valid token. Otherwise return `False`.
        """
        return self.totp.verify(token)