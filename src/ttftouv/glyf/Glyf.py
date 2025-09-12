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
        self.flags: list[int] = []
        self.points: list[Point] = []
        self.end_points_ids: list[int] = []
        self.lenth: int = 0

        SIMPLE_GLYF_DATA_START = 10  # bc base Glyf have 5 properties each 2bytes
        br.skip_bytes(SIMPLE_GLYF_DATA_START)
        self.end_points_ids: list[int] = br.read_int_array(self.n_contours, "uint16")
        self.n_points = self.end_points_ids[-1] + 1

        # skip instructions, for now, just calculating bytes offset
        n_instructions = br.read_uint16()
        br.skip_bytes(n_instructions)

        self.flags = self.read_flags(br)

        x_coords: list[int] = self.parce_coordinates(br, "x")
        y_coords = self.parce_coordinates(br, "y")

        self.points = self.create_points(x_coords, y_coords)

    def read_flags(self, reader: BinaryReader) -> list[int]:
        flags: list[int] = []
        count = 0
        while count < self.n_points:
            repeat = 0
            flag: int = reader.read_uint8()
            flags.append(flag)
            count += 1
            if self.get_flag(flag, 3):
                repeat = reader.read_uint8()
                flags.extend([flag] * repeat)
                count += repeat
        return flags

    def create_points(self, x_coords: list[int], y_coords: list[int]) -> list[Point]:
        result = []
        for i in range(len(x_coords)):
            x = x_coords[i]
            y = y_coords[i]
            point = Point(i, x, y, self.get_flag(self.flags[i], 0))
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
        prev = self.bountding_box[0] if axis == "x" else self.bountding_box[1]
        for i, flag in enumerate(self.flags):
            is_short_vector: bool = self.get_flag(flag, check_flags[0])
            is_same_or_positive: bool = self.get_flag(flag, check_flags[1])

            match (is_short_vector, is_same_or_positive):
                case (True, True):
                    coord = reader.read_uint8()
                case (True, False):
                    coord = -reader.read_uint8()
                case (False, True):
                    coord = prev
                case (False, False):
                    coord = reader.read_int16()

            if i != 0 and not is_same_or_positive:
                coord = coordinates[i - 1] + coord
            coordinates.append(coord)
            prev = coord

        print(coordinates, min(coordinates), max(coordinates))
        return coordinates

    @staticmethod
    def get_flag(flags: int, flag_id: int) -> bool:
        return flags & 2**flag_id != 0
