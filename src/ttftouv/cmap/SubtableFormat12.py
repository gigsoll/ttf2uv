from ttftouv.cmap.CmapSubtable import CmapSubtable


class SubtableFormat12(CmapSubtable):
    def __init__(
        self,
        platform_id: int,
        platform_specific_id: int,
        offset: int,
        binary_data: bytes,
    ) -> None:
        super().__init__(platform_id, platform_specific_id, offset, binary_data)
