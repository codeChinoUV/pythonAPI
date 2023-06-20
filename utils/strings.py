import re


def snake_case_to_camel_case(text_snake_case: str) -> str:
    """
    Convert a snake case string to camel case string
    :param text_snake_case: The string to convert
    :return: The string converted
    """
    components = text_snake_case.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def camel_case_to_snake_case(text_camel_case: str) -> str:
    """
    Convert a camel case string to snake case string
    :param text_camel_case: The string to convert
    :return: The string converted
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text_camel_case).lower()
