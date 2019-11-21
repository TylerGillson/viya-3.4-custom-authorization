import datetime
from config import LOG_ROOT


def get_timestamp_by_second():
    timestamp = datetime.datetime.now()
    return timestamp.strftime("%Y-%m-%d_%I-%M-%S")  # YYYY-MM-DD_HH-MM-SS


def get_timestamp_by_minute():
    timestamp = datetime.datetime.now()
    return timestamp.strftime("%Y-%m-%d_%I-%M")  # YYYY-MM-DD_HH-MM


def log(message):
    timestamp_by_second = get_timestamp_by_second()
    timestamp_by_minute = get_timestamp_by_minute()
    log_path = "\\".join([LOG_ROOT, timestamp_by_minute + ".txt"])
    with open(log_path, "a+") as log_file:
        log_file.write("".join([timestamp_by_second, ": ", message, "\n"]))
