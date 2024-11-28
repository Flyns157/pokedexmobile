import random
import string

def generate_password(size: int = 15) -> str:
    """
    Generate a random password of a given size.

    Parameters:
    size (int): The length of the password to be generated. Defaults to 15.

    Returns:
    str: A randomly generated password consisting of ASCII letters and digits.
    """
    CHARS = string.ascii_letters + string.digits
    return ''.join(random.choice(CHARS) for _ in range(size))
