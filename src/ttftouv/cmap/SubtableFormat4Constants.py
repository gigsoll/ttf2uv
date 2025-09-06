class SubtableFormat4Constants:
    def __init__(
        self,
        seg_count: int,
        start_codes_start: int,
        endcodes_start: int,
        deltas_start: int,
        id_range_offset_start: int,
        glyf_index_array_start: int,
        glyf_index_array_len: int,
    ) -> None:
        self.seg_count = seg_count
        self.start_codes_start = start_codes_start
        self.endcodes_start = endcodes_start
        self.deltas_start = deltas_start
        self.id_range_offset_start = id_range_offset_start
        self.glyf_index_array_start = glyf_index_array_start
        self.glyf_index_array_len = glyf_index_array_len
