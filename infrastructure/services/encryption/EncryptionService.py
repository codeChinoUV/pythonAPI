import bcrypt as bcrypt

from entites.shared.encryption.IEncriptionService import IEncryptionService


class EncryptionService(IEncryptionService):

    def encrypt(self, value: str) -> str:
        """
        Encrypt a value
        :param value: The value to encrypt
        :return: The encrypted value
        """
        text = value.encode('utf-8')
        hashed_text = bcrypt.hashpw(text, bcrypt.gensalt())
        return hashed_text.decode('utf-8')

    def check_encrypted_value(self, encrypted_value: str, value_to_check: str) -> bool:
        """
        Validate if a plain value is equal to a encrypted value
        :param encrypted_value: The encrypted value to check
        :param value_to_check: The plain value to check if is equal to the encrypted value
        :return: The decrypted value
        """
        text_bytes = bytes(value_to_check, 'utf-8')

        encrypted_bytes = bytes(encrypted_value, 'utf-8')
        return bcrypt.checkpw(text_bytes, encrypted_bytes)
