"""
Useful functions for the users app.
"""
import random
import string

def generate_random_code(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Generate a random code.
    """
    return ''.join(random.choice(chars) for _ in range(size))