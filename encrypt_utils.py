# encrypt_utils.py
import os
from cryptography.fernet import Fernet
from sqlalchemy.types import TypeDecorator, String
from cryptography.fernet import InvalidToken

KEY_FILE = 'fernet.key'
if os.path.exists(KEY_FILE):
    key = open(KEY_FILE, 'rb').read()
else:
    key = Fernet.generate_key()
    open(KEY_FILE, 'wb').write(key)

# ahora key es siempre la misma entre reinicios
fernet = Fernet(key)


# Funciones manuales
def encrypt_data(data):
    return fernet.encrypt(data.encode()).decode() if data else None

def decrypt_data(token):
    return fernet.decrypt(token.encode()).decode() if token else None





class EncryptedType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return encrypt_data(value)

    def process_result_value(self, value, dialect):
        try:
            return decrypt_data(value)
        except InvalidToken:
            return value   # o "[sin descifrar]"
