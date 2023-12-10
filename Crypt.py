from cryptography.fernet import Fernet

class Crypt:
    cipher_suite: Fernet
    key: bytes

    def __init__(self):
        with open('key.key', 'rb') as file:
            self.key = file.read()
        self.cipher_suite = Fernet(self.key)
    @staticmethod
    def encrypt(self,str_to_enc):
        try:
            encoded_message = str_to_enc.encode()
            encoded_text = self.cipher_suite.encrypt(encoded_message)
            return encoded_text.decode()
        except Exception as e:
            raise
    def decrypt(self,enc_str):
        try:
            encrypted_message = enc_str.encode()
            decrypted_message = self.cipher_suite.decrypt(encrypted_message)                    
            return decrypted_message.decode()
        except Exception as e:
            raise
