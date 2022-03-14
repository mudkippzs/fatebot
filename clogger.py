import logging
import datetime

watch_log = logging.getLogger('oraclelogs')
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_@_%H-%M-%S')
watch_log.setLevel(logging.INFO)
watch_handler = logging.FileHandler(f"logs/fatebot_{timestamp}.log")
watch_handler.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
watch_log.addHandler(watch_handler)


def clogger(message):
    ts = datetime.datetime.now().strftime('%Y-%m-%d @ %H:%M:%S')
    watch_log.info(f"[{ts}] :: {message}")
