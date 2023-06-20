import random
import string


def generate_barcode(length=13):
    """
    Generate a random barcode
    :param length: The length of the barcode
    :return: The generated barcode
    """
    numbers = string.digits
    barcode = ''.join(random.choice(numbers) for _ in range(length))
    return barcode
