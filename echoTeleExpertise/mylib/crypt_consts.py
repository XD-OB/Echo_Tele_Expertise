from cryptography.fernet import Fernet

KEY = Fernet.generate_key()
cipher_suite = Fernet(KEY)