from ttftouv.TableDirectory import TableDirectory
from ttftouv.helpers import bytes_to_uint


class TTFReader:
    def __init__(self, font_data: bytes) -> None:
        self.font_data: bytes = font_data
        self.num_tables = bytes_to_uint(self.font_data[4:6])
        for table_dir in self.read_font_dirs():
            print(table_dir.tag)

    def read_font_dirs(self) -> list[TableDirectory]:
        STARTFROM = 12  # length of offset tables
        return [
            TableDirectory(self.font_data[i : i + 16])
            for i in range(STARTFROM, self.num_tables * 16, 16)
        ]
