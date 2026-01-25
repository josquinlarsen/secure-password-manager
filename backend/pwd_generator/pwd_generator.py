import random


def generate_password(
        length=16, 
        has_symbols=True, 
        has_numbers=True, 
        mixed_case=True
) -> str:
    """
    Generates a randomized password based on flags passed by user
    length = 16 (default)
    has_symbols = include symbols 
    has_numbers = include digits 
    mixed_case = include upper and lower roman english letters
    """

    # should split into upper and lower and require at least 1 char each?
    alphabet = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
    symbols = ""
    numbers = ""
    
    total_symbols, total_numbers = 0, 0

    if has_symbols:
        max_symbols = length // 4
        total_symbols = random.randint(1, max_symbols)
        symbols = "~!@#$%^&*()-_+=,.?:;"
    if has_numbers:
        max_numbers = length // 4
        total_numbers = random.randint(1, max_numbers)
        numbers = "1234567890"
    
    if not mixed_case:
        alphabet = "qwertyuiopasdfghjklzxcvbnm"
    
    total_letters = length - total_symbols - total_numbers

    return create_password(
        length, symbols, numbers, 
        alphabet, total_symbols, total_numbers, 
        total_letters,
    )


def create_alphabet():
    pass


def create_password(
        length: int, 
        symbols: str, 
        numbers: str, 
        alphabet: str,
        total_symbols: int,
        total_numbers: int,
        total_letters: int,
) -> str:
    """
    Creates the final password string
    """

    password = []

    while len(password) != length:
        if total_symbols > 0:
            password.append(random.choice(symbols))
            total_symbols -= 1
        if total_numbers > 0:
            password.append(random.choice(numbers))
            total_numbers -= 1
        if total_letters > 0:
            password.append(random.choice(alphabet))
            total_letters -= 1

    random.shuffle(password)
    return "".join(password)
