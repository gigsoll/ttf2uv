from ttftouv.BinaryReader import BinaryReader
from ttftouv.cmap.CmapSubtable import CmapSubtable


class SubtableFormat4(CmapSubtable):
    def __init__(
        self,
        platform_id: int,
        platform_specific_id: int,
        offset: int,
        binary_data: bytes,
    ) -> None:
        super().__init__(platform_id, platform_specific_id, offset, binary_data)

        br = BinaryReader(binary_data)
        br.skip_bytes(2)
        self.length = br.read_uint16()
        br.skip_bytes(2)  # skip language
        self.n_segments = br.read_uint16() // 2
        br.skip_bytes(6)  # skip searchRange, entrySelector, and rangeShift
        self.end_codes = br.read_int_array(self.n_segments, "uint16")
        br.skip_bytes(2)  # skip reservedPad bc it is always 0
        self.start_codes: list[int] = br.read_int_array(self.n_segments, "uint16")
        self.id_deltas: list[int] = br.read_int_array(self.n_segments, "uint16")
        self._id_range_offsets_start = br.cur_byte
        self.id_range_offsets: list[int] = br.read_int_array(self.n_segments, "uint16")

    def map_character(self, character_code: int) -> int:
        end_code_id = 0
        for i, end_code in enumerate(self.end_codes):
            if end_code >= character_code:
                end_code_id = i
                break

        start_code, id_delta, id_range_offset = (
            self.start_codes[end_code_id],
            self.id_deltas[end_code_id],
            self.id_range_offsets[end_code_id],
        )

        if start_code > character_code:
            return 0

        glyf_index: int = 0
        if id_range_offset == 0:
            glyf_index = (id_delta + character_code) & 0xFFFF

        if id_range_offset != 0:
            br = BinaryReader(self.binary_data)
            id_range_offset_loc = self._id_range_offsets_start + end_code_id * 2
            glyf_index_adress = (
                id_range_offset
                + 2 * (character_code - start_code)
                + id_range_offset_loc
            )
            br.skip_bytes(glyf_index_adress)
            glyf_index = br.read_uint16()

            if glyf_index != 0:
                glyf_index = (glyf_index + id_delta) & 0xFFFF

        return glyf_index
