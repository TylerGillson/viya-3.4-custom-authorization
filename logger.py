from config import LOG_PATH


def log(message):
    with open(LOG_PATH, "a") as log_file:
        log_file.write(message)
