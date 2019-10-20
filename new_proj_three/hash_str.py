from typing import AnyStr
import hashlib
import os


def get_csci_salt() -> bytes:
    """Returns the appropriate salt for CSCI E-29"""

    # Get the salt in a hex byte string from an environmental variable.
    salt_bytes_hex_str = os.environ["CSCI_SALT"]
    return bytes.fromhex(salt_bytes_hex_str)


def hash_str(some_val: AnyStr, salt: AnyStr = ""):
    """Converts strings to hash digest

    See: https://en.wikipedia.org/wiki/Salt_(cryptography)

    :param some_val: thing to hash

    :param salt: Add randomness to the hashing

    :rtype: bytearray

    """

    # Encode the some_val and the salt value strings to bytes
    some_val_bytes = str.encode(some_val)

    # Check if the salt is of type str or is already a byte string
    if type(salt) is str:
        salt_val_bytes = str.encode(salt)
    else:
        salt_val_bytes = salt

    return hashlib.sha256(salt_val_bytes + some_val_bytes).digest()


def get_user_id(username: str) -> str:
    """ Returns the first 8 characters of the salted username.

    :param username: User name as a string
    :return: First 8 hexadecimal characters of the salted username.
    """
    salt = get_csci_salt()
    return hash_str(username.lower(), salt=salt).hex()[:8]
