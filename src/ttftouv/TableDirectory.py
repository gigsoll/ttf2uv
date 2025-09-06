from ttftouv.helpers import bytes_to_uint, bytes_to_chars


class TableDirectory:
    def __init__(self, header: bytes, font_data: bytes) -> None:
        if len(header) != 16:
            print(len(header), header)
            raise ValueError("Wrong size of table directory")

        offset: int = bytes_to_uint(header[8:12])[0]
        length: int = bytes_to_uint(header[12:16])[0]

        self.tag: str = bytes_to_chars(header[0:4])
        self.table_data = font_data[offset : offset + length]

    def __repr__(self) -> str:
        return f"TableDirectory(tag = {self.tag}, {self.table_data})"
