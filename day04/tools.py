"""Plain Python tools: callable functions for time, dice, and passwords (Days 04–07)."""

from datetime import datetime
import random
import secrets
import string


def get_current_time():
    """Return current local date/time as a formatted string."""
    return datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")


def roll_dice():
    """Return random integer 1–6 (one die roll)."""
    return random.randint(1, 6)


def generate_password(length=14):
    """Return a random password built from letters, digits, and punctuation."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ""

    for _ in range(length):
        password += secrets.choice(characters)

    return password
