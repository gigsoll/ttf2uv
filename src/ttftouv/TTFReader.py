from ttftouv.CMap import CMap
from ttftouv.TableDirectory import TableDirectory
from ttftouv.helpers import bytes_to_uint


class TTFReader:
    def __init__(self, font_data: bytes) -> None:
        self.font_data: bytes = font_data
        self.num_tables: int = bytes_to_uint(self.font_data[4:6])[0]
        self.font_dirs: list[TableDirectory] = self.read_font_dirs()

    def read_font_dirs(self) -> list[TableDirectory]:
        STARTFROM = 12  # length of offset tables
        return [
            TableDirectory(self.font_data[i : i + 16])
            for i in range(STARTFROM, self.num_tables * 16, 16)
        ]

    def create_cmap(self):
        cmap_dir: TableDirectory | None = None
        for dir in self.font_dirs:
            if dir.tag == "cmap":
                cmap_dir = dir
        if cmap_dir is None:
            raise ValueError("Font file is corrupt, cmap is missing")

        start = cmap_dir.offset
        end = start + cmap_dir.length

        cmap = CMap(self.font_data[start:end])
        print(cmap.n_subtables)
