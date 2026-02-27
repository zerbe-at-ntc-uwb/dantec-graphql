"""
Helper functions for encoding ids by.
"""
from base64 import b64encode, b64decode

def encode_cursor(prefix: str, id: str, delimiter: str = ":") -> str:
    """
    Encodes the given user ID into a global cursor id.

    :param id: The ID to encode.

    :return: The encoded cursor id.
    """
    return b64encode(f"{prefix}{delimiter}{id}".encode("ascii")).decode("ascii")


def decode_cursor(cursor: str, delimiter: str = ":", prefix_check=None) -> str:
    """
    Decodes the user ID from the given cursor.

    :param cursor: The cursor to decode.

    :return: The decoded user ID.
    """
    cursor_data = b64decode(cursor.encode("ascii")).decode("ascii")
    cursor_split = cursor_data.split(":")
    if prefix_check:
        assert cursor_split[0] == prefix_check
    return delimiter.join(cursor_split[1:])
