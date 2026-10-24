from datetime import datetime
import random
import secrets
import string



#tool 1
def get_current_time():
    """Return the current date and time"""
    return datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

#tool 2
def roll_dice():
    """Return a random number between 1 and 6"""
    return random.randint(1,6)

#tool 3
def generate_password(length=14):
    """Generate a secure random password"""
    characters = (string.ascii_letters + string.digits + string.punctuation)
    password=""
    
    for _ in range(length):
        password += secrets.choice(characters)

    return password

#tool 4 read file function
def read_text_file(filename):
    try:
        with open(filename, "r") as file:
            content=file.read()
        return content
    except FileNotFoundError:
        print('Error: File not found')
        return "quit"