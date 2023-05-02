def is_digit_validator(value_str):
    if not value_str:
        # just to use the clear method
        # or else this field wont cleared
        return True
    if not value_str.isdigit():
        return False
    else:
        return True


def is_float_validator(value_str):
    if not value_str:
        # just to use the clear method
        # or else this field wont cleared
        return True
    try:
        float(value_str)
        return True
    except ValueError:
        return False

