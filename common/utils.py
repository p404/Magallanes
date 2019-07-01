import sys
import logging
import hashlib

def hash(string):
    return hashlib.md5(string.encode()).hexdigest()

def logger(severity, string):
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        handler   = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return getattr(logger, severity)(string)