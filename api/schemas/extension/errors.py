
# General errors
general_errors = {
    "required": ["Este campo es requerido"],
    "null": ["Este campo no puede estar vacio"],
    "validator_failed": ["Calor invalido"],
}


# String error messages
def get_string_error_messages():
    return {
        "invalid": ["Texto no valido"],
        **general_errors
    }


def get_one_of_error_message(options: list) -> str:
    """
    Get the error message for one of validation
    :param options: The options available
    :return: The validation message
    """
    return f"Opcion invalida, las opciones validas son: {str.join(', ', options)}"


def get_length_error_message(min=None, max=None, equal=None):
    """
    Get the error message for the length validation error
    :param min: The min characters
    :param max: The max characters
    :param equal: The equal characters
    :return: A str with the error message
    """
    if min is not None and max is None:
        return f'Este campo debe de tener al menos {min} caracteres'
    if min is None and max is not None:
        return f'Este campo no debe de tener mas de {max} caracteres',
    if min is not None and max is not None:
        return f'Este campo debe de tener mas de {min} y menos de {max} caracteres'
    if equal is not None:
        return f'Este campo debe de tener exactamente {equal} caracteres'
    return 'Hay problemas con el largo de la cadena'


# Email error messages
def get_invalid_email_error_message():
    return "Correo no valido"


# Boolean error messages
def get_boolean_errors():
    return {
        "invalid": ["Booleano no valido"],
        **general_errors
    }


# Float error messaged
def get_float_errors():
    return {
        "special": ["Valores numericos especiales no estan permitidos"],
        **general_errors
    }


# Integer error messages
def get_int_errors():
    return {
        "invalid": ["Entero no valido"],
        **general_errors
    }


def get_range_error_message(min=None, max=None):
    """
    Get the error message for the int range validation error
    :param min: The min range
    :param max: The max range
    :return: A str with the error message
    """
    if min is not None and max is None:
        return f'El numero debe de ser mayor a {min}'
    if min is None and max is not None:
        return f'El numero debe de ser menos a {max}'
    if min is not None and max is not None:
        return f'El numero debe de ser mayor a {min} y menor a {max}'
    return 'Hay un problema con el rango del numero'


# List error messages
def get_list_errors():
    return {
        "invalid": ["Lista invalida"],
        **general_errors
    }


# Nested error messages
def get_nested_errors():
    return {
        "type": ["Tipo no valido"],
        **general_errors
    }
