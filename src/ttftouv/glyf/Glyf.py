from dataclasses import dataclass
from ttftouv.helpers import bytes_to_int, bytes_to_uint, read_int_array
from collections import Counter
from pprint import pprint


@dataclass
class Point:
    id: int
    x: int
    y: int
    on_curve: bool


class Glyf:
    def __init__(self, glyf_data: bytes) -> None:
        self.n_contours: int = bytes_to_int(glyf_data[0:2])
        self.bountding_box: tuple[int, ...] = tuple(
            read_int_array(glyf_data, 2, 4, signed=True)
        )


class SimpleGlyf(Glyf):
    def __init__(self, glyf_data: bytes) -> None:
        super().__init__(glyf_data)

        # properties
        self.n_points: int = 0
        self.flags: list[list[int]] = []
        self.points: list[Point] = []
        self.end_points_ids: list[int] = []
        self.lenth: int = 0

        SIMPLE_GLYF_DATA_START = 10  # bc base Glyf have 5 properties each 2bytes
        self.end_points_ids: list[int] = read_int_array(
            glyf_data, SIMPLE_GLYF_DATA_START, self.n_contours
        )
        self.n_points = self.end_points_ids[-1] + 1

        # skip instructions, for now, just calculating bytes offset
        instructions_start = SIMPLE_GLYF_DATA_START + 2 * self.n_contours
        n_instructions: int = bytes_to_uint(
            glyf_data[instructions_start : instructions_start + 2]
        )
        flags_start = instructions_start + 2 + n_instructions

        self.flags = self.read_flags(glyf_data[flags_start:])

        x_coords_start = flags_start + len(self.flags)
        flag_offset_mapping: dict[int, int] = {0: 2, 1: 1}
        x_coords_end: int = x_coords_start + self._count_flags_offset(
            1, flag_offset_mapping
        )
        x_coords, x_len = self.parce_coordinates(
            glyf_data[x_coords_start:x_coords_end], "x"
        )

        x_coords_end = x_coords_start + x_len

        y_coords_end = x_coords_end + self._count_flags_offset(2, flag_offset_mapping)
        y_coords, _ = self.parce_coordinates(glyf_data[x_coords_end:y_coords_end], "y")

        self.points = self.create_points(x_coords, y_coords)

    def read_flags(self, data: bytes) -> list[list[int]]:
        flags: list[list[int]] = []
        count, cur = 0, 0
        while count < self.n_points:
            repeat = 0
            bin_flag: list[int] = self._byte_int_to_int(data[cur], 8)
            flags.append(bin_flag)
            count += 1
            if bin_flag[3] == 1:
                repeat = data[cur + 1]
                flags.extend([bin_flag] * repeat)
                count += repeat
                cur += 1
            cur += 1
        return flags

    def create_points(self, x_coords: list[int], y_coords: list[int]) -> list[Point]:
        result = []
        for i in range(len(x_coords)):
            if i == 0:
                x = x_coords[i]
                y = y_coords[i]
            else:
                x = x_coords[i - 1] + x_coords[i]
                y = y_coords[i - 1] + y_coords[i]
            point = Point(i, x, y, True if self.flags[i][0] == "1" else False)
            result.append(point)
        return result

    def parce_coordinates(self, data: bytes, axis: str) -> tuple[list[int], int]:
        """
        Takes binary data, read set coordinates using flags
        """
        check_flags: tuple[
            int, int
        ]  # first flag for short/long, second – positive/negative if short an repeat or not if not short
        match axis:
            case "x":
                check_flags = (1, 4)
            case "y":
                check_flags = (2, 5)
            case _:
                raise ValueError("Coordinate should be x or y")

        coordinates: list[int] = []
        cur_byte = 0
        for i, flag in enumerate(self.flags):
            is_short_vector: bool = bool(int(flag[check_flags[0]]))
            is_same_or_positive: bool = bool(int(flag[check_flags[1]]))

            pprint(
                f"{ flag= }  { check_flags= }  { is_short_vector=  }  { is_same_or_positive= }  "
            )

            if is_short_vector:
                coord = data[cur_byte]
                is_positive = is_same_or_positive
                if not is_positive:
                    coord = coord * -1
                cur_byte += 1
            else:
                is_same = is_same_or_positive
                if not is_same:
                    coord = bytes_to_int(data[cur_byte : cur_byte + 2])
                    cur_byte += 2
                else:
                    # TODO check later
                    coord = coordinates[i - 1]
            print(coord)
            if i != 0 and not is_same_or_positive:
                coord = coordinates[i - 1] + coord
            coordinates.append(coord)
        print(coordinates)
        return coordinates, cur_byte

    def _count_flags_offset(self, index: int, mapping: dict[int, int]) -> int:
        flags_count = Counter([flag[index] for flag in self.flags])
        result = 0
        for key, value in mapping.items():
            result += flags_count[key] * value
        return result

    @staticmethod
    def _byte_int_to_int(value: int, length: int) -> list[int]:
        if not 0 <= value <= 255:
            raise ValueError("Integer must be 1 byte sized")

        return [(value >> i) & 1 for i in range(length)]
