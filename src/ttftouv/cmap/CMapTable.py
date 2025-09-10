from ttftouv.Table import Table
from ttftouv.BinaryReader import BinaryReader
from ttftouv.cmap.SubtableFormat4 import SubtableFormat4
from ttftouv.cmap.SubtableFormat12 import SubtableFormat12
from ttftouv.cmap.CmapSubtable import CmapSubtable


class CMapTable(Table):
    def __init__(self, binary_data: bytes) -> None:
        br = BinaryReader(binary_data)
        br.skip_bytes(2)  # skipping version
        self.n_subtables: int = br.read_uint16()
        self.utf_subtable: CmapSubtable

        subtables: list[CmapSubtable] = []
        for i in range(self.n_subtables):
            platform_id: int = br.read_uint16()
            platform_specific_id: int = br.read_uint16()
            offset: int = br.read_uint32()

            subtables.append(
                CmapSubtable(platform_id, platform_specific_id, offset, binary_data)
            )

        for subtable in subtables:
            platform_id, platform_specific_id, offset = (
                subtable.platform_id,
                subtable.platform_specific_id,
                subtable.offset,
            )
            if (platform_id, platform_specific_id) in [
                (0, 3),
                (3, 1),
            ]:
                """
                0, 3 – Unicode Basic Multilingual Plane (BMP)
                3, 1 – Microsoft Unicode BMP
                """
                br = BinaryReader(subtable.binary_data)
                format: int = br.read_uint16()
                match format:
                    case 4:
                        self.utf_subtable = SubtableFormat4(
                            platform_id,
                            platform_specific_id,
                            offset,
                            subtable.binary_data,
                        )
                    case 12:
                        self.utf_subtable = SubtableFormat12(
                            platform_id,
                            platform_specific_id,
                            offset,
                            subtable.binary_data,
                        )
                    case _:
                        raise NotImplementedError(f"Format {format} is not implemented")
                break  # bc if here is multiple Unicode subtables only one will be used, preferably 0,3
