def is_digit(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
