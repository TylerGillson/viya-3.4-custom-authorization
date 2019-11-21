import datetime
from customize_authorization.config import LOG_ROOT

"""
logger.py
=========

A collection of helper methods for writing messages to a log file in order to record the actions performed
by the script during the maintenance of custom groups.
"""


def get_timestamp_by_second():
    """
    Generate a timestamp string with the following format: YYYY-MM-DD_HH-MM-SS
    """
    timestamp = datetime.datetime.now()
    return timestamp.strftime("%Y-%m-%d_%I-%M-%S")


def get_timestamp_by_minute():
    """
    Generate a timestamp string with the following format: YYYY-MM-DD_HH-MM
    """
    timestamp = datetime.datetime.now()
    return timestamp.strftime("%Y-%m-%d_%I-%M")  # YYYY-MM-DD_HH-MM


def log(message):
    """
    Write a message to a log file, named by the current date + minute combination.

    Parameters
    ----------

    message:
        The message to log.
    """
    timestamp_by_second = get_timestamp_by_second()
    timestamp_by_minute = get_timestamp_by_minute()
    log_path = "\\".join([LOG_ROOT, timestamp_by_minute + ".txt"])
    with open(log_path, "a+") as log_file:
        log_file.write("".join([timestamp_by_second, ": ", message, "\n"]))
