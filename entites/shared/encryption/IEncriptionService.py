from abc import ABC, abstractmethod


class IEncryptionService(ABC):

    @abstractmethod
    def encrypt(self, value: str) -> str:
        """
        Encrypt a value
        :param value: The value to encrypt
        :return: The encrypted value
        """
        pass

    @abstractmethod
    def check_encrypted_value(self, encrypted_value: str, value_to_check: str) -> bool:
        """
        Validate if a plain value is equal to a encrypted value
        :param encrypted_value: The encrypted value to check
        :param value_to_check: The plain value to check if is equal to the encrypted value
        :return: The decrypted value
        """
        pass
