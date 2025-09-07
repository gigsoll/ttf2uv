from ttftouv.helpers import bytes_to_int, bytes_to_uint, read_int_array


class Glyf:
    def __init__(self, glyf_data: bytes) -> None:
        self.n_contours: int = bytes_to_int(glyf_data[0:2])
        self.bountding_box: tuple[int, ...] = tuple(
            read_int_array(glyf_data, 2, 4, signed=True)
        )


class SimpleGlyf(Glyf):
    def __init__(self, glyf_data: bytes) -> None:
        super().__init__(glyf_data)
        SIMPLE_GLYF_DATA_START = 10
        end_points_of_countours: list[int] = read_int_array(
            glyf_data, SIMPLE_GLYF_DATA_START, self.n_contours
        )
        self.n_points: int = end_points_of_countours[-1] + 1

        instructions_start = SIMPLE_GLYF_DATA_START + 2 * self.n_contours
        n_instructions: int = bytes_to_uint(
            glyf_data[instructions_start : instructions_start + 2]
        )
        flags_start = instructions_start + 2 + n_instructions
        flags = self.read_flags(glyf_data[flags_start:])
        print(flags, len(flags), self.n_points)
        print(self.bountding_box)

    def read_flags(self, data: bytes) -> list[str]:
        flags: list[str] = []
        count, cur = 0, 0
        while count < self.n_points:
            repeat = 0
            bin_flag: str = self._byte_int_to_int(data[cur])
            flags.append(bin_flag)
            count += 1
            if bin_flag[3] == "1":
                repeat = data[cur + 1]
                flags.extend([bin_flag] * repeat)
                count += repeat
                print(repeat)
                cur += 1
            cur += 1
        return flags

    @staticmethod
    def _byte_int_to_int(integer: int, endian: str = "little") -> str:
        if not 0 <= integer <= 255:
            raise ValueError("Integer must be 1 byte sized")

        bin_int = bin(integer)[2:]
        if len(bin_int) < 8:
            len_dif: int = 8 - len(bin_int)
            bin_int = "0" * len_dif + bin_int

        if endian == "little":
            bin_int = bin_int[::-1]
        return bin_int
