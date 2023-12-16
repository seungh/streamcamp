import re

def is_valid(email:str) -> bool:
    """ check email format """
    pattern = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
    if pattern.match(email):
        return True
    return False

