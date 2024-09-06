from datetime import datetime
import pytz


def generate_current_datetime():
    return datetime.now(pytz.timezone("Africa/Lagos"))


def generate_current_datetime_timezone():
    return datetime.now(pytz.timezone("Africa/Lagos"))


def perecntage_increase_decrease(original: int, new: int):

    if original == 0:
        if new == 0:
            return 0  # Both original and new are zero, so there is no change
        else:
            return 0

    return (float(new - original) / original) * 100
