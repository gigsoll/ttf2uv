from ttftouv.CMap import CMap, CmapSubtable
from ttftouv.TableDirectory import TableDirectory
from ttftouv.helpers import bytes_to_uint


class TTFReader:
    def __init__(self, font_data: bytes) -> None:
        self.font_data: bytes = font_data

        num_tables: int = bytes_to_uint(self.font_data[4:6])[0]
        self.font_dirs: list[TableDirectory] = self.read_font_dirs(num_tables)
        self.cmap_unicode: CmapSubtable = self.create_cmap().utf_subtable

    def read_font_dirs(self, n_tables: int) -> list[TableDirectory]:
        STARTFROM = 12  # length of offset tables
        return [
            TableDirectory(self.font_data[i : i + 16], self.font_data)
            for i in range(STARTFROM, n_tables * 16, 16)
        ]

    def create_cmap(self) -> CMap:
        cmap_dir: TableDirectory | None = None
        for dir in self.font_dirs:
            if dir.tag == "cmap":
                cmap_dir = dir
        if cmap_dir is None:
            raise ValueError("Font file is corrupt, cmap is missing")

        cmap = CMap(cmap_dir.table_data)
        return cmap
