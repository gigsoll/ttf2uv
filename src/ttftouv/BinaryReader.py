from typing import Literal


class BinaryReader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.cur_byte = 0

    def read_int16(self) -> int:
        self.skip_bytes(2)
        return int.from_bytes(self.data[self.cur_byte - 2 : self.cur_byte], signed=True)

    def read_uint16(self) -> int:
        self.skip_bytes(2)
        return int.from_bytes(
            self.data[self.cur_byte - 2 : self.cur_byte], signed=False
        )

    def read_int8(self) -> int:
        self.skip_bytes(1)
        return self.data[self.cur_byte - 1]

    def read_text(self, len: int) -> str:
        self.skip_bytes(len)
        return "".join(
            [chr(byte) for byte in self.data[self.cur_byte - len : self.cur_byte]]
        )

    def read_int_array(
        self, n_items: int, type: Literal["uint16", "int16", "int8"]
    ) -> list[int]:
        type_size = 0
        match type:
            case "int16" | "uint16":
                type_size = 2
            case "int8":
                type_size = 1
        array_size = n_items * type_size
        self.skip_bytes(array_size)
        signed = True
        if type[0] == "u":
            signed = False
        return [
            int.from_bytes(self.data[i : i + type_size], signed=signed)
            for i in range(
                self.cur_byte - array_size,
                self.cur_byte + (n_items * type_size),
                type_size,
            )
        ]

    def skip_bytes(self, n_bytes: int) -> None:
        if len(self.data) < self.cur_byte + n_bytes:
            raise IndexError("out of bounce")
        self.cur_byte += n_bytes
