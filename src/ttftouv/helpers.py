def bytes_to_uint(byte_data: bytes) -> int:
    VALIDSIZES = (2, 4)
    if len(byte_data) not in VALIDSIZES:
        raise ValueError("Wrong size of bytes chunk")
    return int.from_bytes(byte_data, signed=False)


def bytes_to_chars(byte_data: bytes) -> str:
    return "".join([chr(byte) for byte in byte_data])
