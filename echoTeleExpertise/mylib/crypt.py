from .crypt_consts import cipher_suite
import base64

def     encrypt_val(email):
    '''
    The Encryption to have the activate link
    '''
    cipher_text = cipher_suite.encrypt(bytes(email, encoding='utf-8'))
    return str(bytes.decode(cipher_text))


def     decrypt_val(cipher_text):
    '''
    The decryption to have the user email
    '''
    email = bytes.decode(cipher_suite.decrypt(cipher_text))
    return str(email)