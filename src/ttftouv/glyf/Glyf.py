from dataclasses import dataclass
from collections import Counter
from pprint import pprint

from ttftouv.BinaryReader import BinaryReader


@dataclass
class Point:
    id: int
    x: int
    y: int
    on_curve: bool


class Glyf:
    def __init__(self, id: int, glyf_data: bytes) -> None:
        br: BinaryReader = BinaryReader(glyf_data)
        self.id = id
        self.n_contours: int = br.read_int16()
        self.bountding_box: tuple[int, ...] = tuple(br.read_int_array(4, "int16"))


class SimpleGlyf(Glyf):
    def __init__(self, id: int, glyf_data: bytes) -> None:
        super().__init__(id, glyf_data)
        br: BinaryReader = BinaryReader(glyf_data)

        # properties
        self.n_points: int = 0
        self.flags: list[list[int]] = []
        self.points: list[Point] = []
        self.end_points_ids: list[int] = []
        self.lenth: int = 0

        SIMPLE_GLYF_DATA_START = 10  # bc base Glyf have 5 properties each 2bytes
        self.end_points_ids: list[int] = br.read_int_array(self.n_contours, "uint16")
        self.n_points = self.end_points_ids[-1] + 1

        # skip instructions, for now, just calculating bytes offset
        n_instructions = br.read_uint16()
        br.skip_bytes(n_instructions)

        self.flags = self.read_flags(br)
        print(self.flags)

        x_coords: list[int] = self.parce_coordinates(br, "x")

        y_coords = self.parce_coordinates(br, "y")

        self.points = self.create_points(x_coords, y_coords)

    def read_flags(self, reader: BinaryReader) -> list[list[int]]:
        flags: list[list[int]] = []
        count = 0
        while count < self.n_points:
            repeat = 0
            bin_flag: list[int] = self._byte_int_to_int(reader.read_uint8(), 8)
            flags.append(bin_flag)
            count += 1
            if bin_flag[3] == 1:
                repeat = reader.read_uint8()
                flags.extend([bin_flag] * repeat)
                count += repeat
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

    def parce_coordinates(self, reader: BinaryReader, axis: str) -> list[int]:
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
        for i, flag in enumerate(self.flags):
            is_short_vector: bool = bool(int(flag[check_flags[0]]))
            is_same_or_positive: bool = bool(int(flag[check_flags[1]]))

            pprint(
                f"{ flag= }  { check_flags= }  { is_short_vector=  }  { is_same_or_positive= }  "
            )

            if is_short_vector:
                coord = reader.read_uint8()
                is_positive = is_same_or_positive
                if not is_positive:
                    coord = coord * -1
            else:
                is_same = is_same_or_positive
                if not is_same:
                    coord = reader.read_int16()
                else:
                    # TODO check later
                    coord = coordinates[i - 1]
            print(coord)
            if i != 0 and not is_same_or_positive:
                coord = coordinates[i - 1] + coord
            coordinates.append(coord)
        print(coordinates)
        return coordinates

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
