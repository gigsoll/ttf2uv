class CmapSubtable:
    def __init__(
        self,
        platform_id: int,
        platform_specific_id: int,
        offset: int,
        binary_data: bytes,
    ) -> None:
        self.platform_id = platform_id
        self.platform_specific_id = platform_specific_id
        self.offset = offset
        self.binary_data: bytes = binary_data[offset:]

    def map_character(self, character_code: int) -> int: ...
