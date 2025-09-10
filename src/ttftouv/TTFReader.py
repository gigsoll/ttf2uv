from ttftouv.BinaryReader import BinaryReader
from ttftouv.cmap.CMapTable import CMapTable, CmapSubtable

from ttftouv.glyf.GlyfTable import GlyfTable

from ttftouv.glyf.Glyf import Glyf, SimpleGlyf
from ttftouv.TableDirectory import Table, TableDirectoryFactory


class TTFReader:
    def __init__(self, font_data: bytes) -> None:
        self.font_data: bytes = font_data
        br = BinaryReader(font_data)
        br.skip_bytes(4)

        num_tables: int = br.read_uint16()
        br.skip_bytes(6)  # skipped searchRange, entrySelector and rangeShift
        self.font_dirs: list[Table] = self.read_font_dirs(num_tables, br)
        self.cmap_unicode: CmapSubtable = self.get_cmap().utf_subtable
        self.glyfs: list[Glyf] = []
        print(self.cmap_unicode)

    def read_font_dirs(self, n_tables: int, reader: BinaryReader) -> list[Table]:
        font_dirs: list[Table] = []
        for i in range(n_tables):
            tag = reader.read_text(4)
            reader.skip_bytes(4)
            offset: int = reader.read_uint32()
            length: int = reader.read_uint32()

            table_data = self.font_data[offset : offset + length]

            try:
                font_dirs.append(TableDirectoryFactory.create_table(tag, table_data))
            except NotImplementedError:
                print(f"{tag} is not implemented")

        return font_dirs

    def read_simple_glif(self) -> SimpleGlyf:
        return SimpleGlyf(
            1,
            [dir for dir in self.font_dirs if isinstance(dir, GlyfTable)][0].table_data[
                :800
            ],
        )

    def get_cmap(self) -> CMapTable:
        return [dir for dir in self.font_dirs if isinstance(dir, CMapTable)][0]


if __name__ == "__main__":
    from os import path, environ

    font_dir = path.join(str(environ.get("HOME")), ".fonts")
    font_name = "JetBrainsMonoNLNerdFont-Regular.ttf"
    font_loc = path.join(font_dir, font_name)

    with open(font_loc, "rb") as ttf:
        font = TTFReader(ttf.read())

    font.read_simple_glif()
