from ttftouv.Table import Table
from ttftouv.helpers import bytes_to_uint
from ttftouv.cmap.SubtableFormat4 import SubtableFormat4
from ttftouv.cmap.SubtableFormat12 import SubtableFormat12
from ttftouv.cmap.CmapSubtable import CmapSubtable


class CMapTable(Table):
    def __init__(self, binary_data: bytes) -> None:
        self.n_subtables: int = bytes_to_uint(binary_data[2:4])
        self.utf_subtable: CmapSubtable
        subtables_start = 4
        subtables_end = (
            subtables_start + self.n_subtables * 8
        )  # bc each subtable deffinition contains 8 bytes of data
        for i in range(subtables_start, subtables_end, 8):
            platform = bytes_to_uint(binary_data[i : i + 2])
            platform_version = bytes_to_uint(binary_data[i + 2 : i + 4])
            offset = bytes_to_uint(binary_data[i + 4 : i + 8])

            if (platform, platform_version) in [(0, 3), (3, 1)]:
                """
                0, 3 – Unicode Basic Multilingual Plane (BMP)
                3, 1 – Microsoft Unicode BMP
                """
                format: int = int(binary_data[offset : offset + 2].hex(), 16)
                match format:
                    case 4:
                        self.utf_subtable = SubtableFormat4(binary_data[offset:])
                    case 12:
                        self.utf_subtable = SubtableFormat12(binary_data[offset:])
                    case _:
                        raise NotImplementedError(f"Format {format} is not implemented")
                break  # bc if here is multiple Unicode subtables only one will be used, preferably 0,3
