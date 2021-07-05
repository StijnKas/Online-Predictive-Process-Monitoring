def int_or_none(s):
    "Converter which either returns an integer or None"

    try:
        return int(s)
    except ValueError:
        return None

def float_or_none(s):
    "Converter which either returns a float or None"

    try:
        return float(s)
    except ValueError:
        return None