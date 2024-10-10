def truncate_to_two_decimals(n):
    return float(str(n)[:str(n).find('.') + 3])
