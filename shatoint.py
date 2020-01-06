import hashlib
import sys

def shatoint(input_string):
    """ Function prototype for further bloom testing or development """
    return int.from_bytes(hashlib.sha256(input_string.encode('utf-8')).digest(), byteorder=sys.byteorder)
