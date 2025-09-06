from ttftouv.cmap.SubtableFormat4Constants import SubtableFormat4Constants
from ttftouv.cmap.CmapSubtable import CmapSubtable

from ttftouv.helpers import bytes_to_uint


class SubtableFormat4(CmapSubtable):
    def __init__(self, binary_data: bytes):
        super(SubtableFormat4, self).__init__(binary_data)

        length: int = bytes_to_uint(self.binary_data[2:4])[0]  # UINT16, 2nd field
        self.binary_data = self.binary_data[:length]
        constants: SubtableFormat4Constants = self._prepare_constants()

        # searchRange, entrySelector, and rangeShift are scipped, each UINT16
        seg_count = constants.seg_count
        self.end_codes: list[int] = self._read_array(
            constants.endcodes_start, seg_count
        )
        self.start_codes: list[int] = self._read_array(
            constants.start_codes_start, seg_count
        )
        self.id_delta: list[int] = self._read_array(constants.deltas_start, seg_count)
        self.id_range_offset: list[int] = self._read_array(
            constants.id_range_offset_start, seg_count
        )
        self.glyf_index_array: list[int] = self._read_array(
            constants.glyf_index_array_start, constants.glyf_index_array_len
        )

    def map_character(self, character: bytes) -> int:
        char_int = bytes_to_uint(character)[0]

        end_index: int = 0
        for i, end_code in enumerate(self.end_codes):
            if end_code >= char_int:
                end_index = i
                break

        print(self.id_delta[end_index])

        if self.start_codes[end_index] > char_int:  # not <= char_int
            return 0  # missing character

        if self.id_range_offset[end_index] != 0:
            glyf_index_adress = (
                self.id_range_offset[end_index]
                + 2 * (char_int - self.start_codes[end_index])
                + self._prepare_constants().id_range_offset_start
                + end_index * 2
            )
            glyph_index = (
                self.binary_data[glyf_index_adress] << 8
                | self.binary_data[glyf_index_adress + 1]
            )

            if glyph_index != 0:
                glyph_index = (glyph_index + self.id_delta[end_index]) % 65536

            return glyph_index

        return (self.id_delta[end_index] + char_int) % 65536

    def _read_array(
        self, start_from: int, length: int, intem_size: int | None = None
    ) -> list[int]:
        if intem_size is None:
            intem_size = 2
        return [
            bytes_to_uint(self.binary_data[i : i + 2])[0]
            for i in range(start_from, start_from + length * 2, 2)
        ]  # each element of the array is UINT16

    def _prepare_constants(self) -> SubtableFormat4Constants:
        endcodes_start: int = 14

        seg_count: int = int(
            bytes_to_uint(self.binary_data[6:8])[0] / 2
        )  # bc stores SegCountX2, UINT16, language skipped
        length: int = bytes_to_uint(self.binary_data[2:4])[0]  # UINT16, 2nd field

        array_length: int = seg_count * 2
        start_codes_start: int = (
            endcodes_start + array_length + 2
        )  # bc reservedPad is always 0
        deltas_start: int = start_codes_start + array_length
        id_range_offset_start: int = deltas_start + array_length
        glyf_index_array_start: int = id_range_offset_start + array_length
        glyf_index_array_len: int = int((length - glyf_index_array_start) / 2)

        return SubtableFormat4Constants(
            seg_count,
            start_codes_start,
            endcodes_start,
            deltas_start,
            id_range_offset_start,
            glyf_index_array_start,
            glyf_index_array_len,
        )
