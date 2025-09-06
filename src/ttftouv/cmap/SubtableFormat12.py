from ttftouv.cmap.CmapSubtable import CmapSubtable


class SubtableFormat12(CmapSubtable):
    def __init__(self, table_data: bytes) -> None:
        super().__init__(table_data)
