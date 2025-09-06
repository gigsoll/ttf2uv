class CmapSubtable:
    def __init__(self, binary_data: bytes) -> None:
        self.binary_data: bytes = binary_data

    def map_character(self, character: bytes) -> int: ...
