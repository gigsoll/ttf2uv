from typing import overload


def bytes_to_uint(byte_data: bytes) -> int:
    _validate_bytes(byte_data, (1, 2, 4))
    return int.from_bytes(byte_data, signed=False)


def bytes_to_int(byte_data: bytes):
    _validate_bytes(byte_data, (2, 4))
    return int.from_bytes(byte_data, signed=True)


def _validate_bytes(byte_data: bytes, valid_sizes: tuple[int, ...]):
    if len(byte_data) not in valid_sizes:
        raise ValueError(f"Wrong size of bytes chunk, {byte_data}")


def bytes_to_chars(byte_data: bytes) -> str:
    return "".join([chr(byte) for byte in byte_data])


def read_int_array(
    data: bytes, offset_start_bytes: int, n_items: int, type: int = 16, signed=False
) -> list[int]:
    if type not in (8, 16, 32):
        raise ValueError("INT can be 8, 16 or 32 bits")

    step = type // 8

    if len(data[offset_start_bytes:]) < step * n_items:
        raise ValueError("Array is too short")

    return [
        int.from_bytes(data[i : i + step], signed=signed)
        for i in range(offset_start_bytes, offset_start_bytes + (n_items * step), step)
    ]
