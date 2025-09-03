from typing import overload


def bytes_to_uint(*byte_data: bytes) -> tuple[int, ...]:
    VALIDSIZES = (2, 4)
    result = []
    for byte_group in byte_data:
        if len(byte_group) not in VALIDSIZES:
            raise ValueError("Wrong size of bytes chunk")
        result.append(int.from_bytes(byte_group, signed=False))
    return tuple(result)


def bytes_to_chars(byte_data: bytes) -> str:
    return "".join([chr(byte) for byte in byte_data])
