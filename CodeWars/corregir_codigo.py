def get_status(is_busy):
    msg = "busy" if is_busy else "available"
    return {"status": msg}

