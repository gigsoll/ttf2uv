from ttftouv.helpers import bytes_to_uint, bytes_to_chars


class TableDirectory:
    def __init__(self, byte_data: bytes) -> None:
        if len(byte_data) != 16:
            raise ValueError("Wrong size of table directory")

        self.tag: str = bytes_to_chars(byte_data[0:4])
        self.check_sum: bytes = byte_data[4:8]
        self.offset: int = bytes_to_uint(byte_data[8:12])
        self.length: int = bytes_to_uint(byte_data[12:16])
