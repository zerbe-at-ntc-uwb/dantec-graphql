"""
Helper functions for encoding ids by.
"""
from base64 import b64encode, b64decode

def encode_cursor(prefix: str, id: str, delimiter: str = ":") -> str:
    """
    Encodes the given id into a global cursor id.

    :param id: The ID to encode.

    :return: The encoded cursor id.
    """
    return b64encode(f"{prefix}{delimiter}{id}".encode("ascii")).decode("ascii")


def decode_cursor(cursor: str, delimiter: str = ":", prefix_check=None) -> str:
    """
    Decodes the ID from the given global cursor id.

    :param cursor: The cursor to decode.

    :return: The decoded ID.
    """
    cursor_data = b64decode(cursor.encode("ascii")).decode("ascii")
    cursor_split = cursor_data.split(delimiter)
    if prefix_check:
        assert cursor_split[0] == prefix_check
    return delimiter.join(cursor_split[1:])


class StandardCursorFactory:
    """
    Standard protocol for packing the class name and source repo into the
    id to create a cursor.  This assumes that the id is unique for the class
    name (from the source_repo), so including the source repo and class name
    within the cursor will make it globally unique.
    """
    
    def __init__(self, source_repo: str, cls_name: str, delimiter: str = ":"):
        """
            :param source_repo: The name of the repo from which the information was
                                pulled.
            :param cls_name: The name of the object's class to which the cursor points.
            :param delimiter: Specified the delimiter used for
                              packing/unpacking.
        """
        self.source_repo = source_repo
        self.cls_name = cls_name
        self.delim = delimiter

    def pack(self, id) -> str:
        """
        Converts the id to a globally unique cursor.
        """
        return encode_cursor(self.source_repo,
                             encode_cursor(self.cls_name, id, self.delim),
                             self.delim)

    def unpack(self, cursor) -> str:
        """
        Retrieves the from the globally unique cursor.
        """
        return decode_cursor(decode_cursor(cursor, self.delim,
                                           self.source_repo),
                             self.delim,
                             self.cls_name)
