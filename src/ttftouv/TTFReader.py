from ttftouv.cmap.CMapTable import CMapTable, CmapSubtable
from ttftouv.glyf.Glyf import Glyf
from ttftouv.TableDirectory import Table, TableDirectoryFactory
from ttftouv.helpers import bytes_to_uint, bytes_to_chars


class TTFReader:
    def __init__(self, font_data: bytes) -> None:
        self.font_data: bytes = font_data

        num_tables: int = bytes_to_uint(self.font_data[4:6])
        self.font_dirs: list[Table] = self.read_font_dirs(num_tables)
        self.cmap_unicode: CmapSubtable = self.get_cmap().utf_subtable
        self.glyfs: list[Glyf] = []
        print(self.cmap_unicode)

    def read_font_dirs(self, n_tables: int) -> list[Table]:
        STARTFROM = 12  # length of offset tables
        font_dirs: list[Table] = []
        for i in range(STARTFROM, n_tables * 16, 16):
            header = self.font_data[i : i + 16]
            offset: int = bytes_to_uint(header[8:12])
            length: int = bytes_to_uint(header[12:16])

            tag: str = bytes_to_chars(header[0:4])
            table_data = self.font_data[offset : offset + length]

            try:
                font_dirs.append(TableDirectoryFactory.create_table(tag, table_data))
            except NotImplementedError:
                print(f"{tag} is not implemented")

        return font_dirs

    def get_cmap(self) -> CMapTable:
        return [dir for dir in self.font_dirs if isinstance(dir, CMapTable)][0]


if __name__ == "__main__":
    from os import path, environ

    font_dir = path.join(str(environ.get("HOME")), ".fonts")
    font_name = "Roboto-Regular.ttf"
    font_loc = path.join(font_dir, font_name)

    with open(font_loc, "rb") as ttf:
        font = TTFReader(ttf.read())
