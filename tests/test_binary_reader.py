from src.ttftouv.BinaryReader import BinaryReader

test_data = (
    b"\xff\xff\xfe\xff"  # negative numbers, 2 bytes
    b"\xff\xf7\x00\xe8"  # not -1 and just number
    b"\xff\x10"  # just unint 8 numbers
    b"Hello world!"
    b"\x00\x01\x00\x0a\xff\xf6"  # array for int16
    b"\xff\xff\x00\x00\x00\x17"  # array for uint16
    b"\xff\x10\x01"  # array for uint8
)

br = BinaryReader(test_data)


def test_read_int16():
    assert br.read_int16() == -1
    assert br.read_int16() == -257


def test_read_uint16():
    assert br.read_uint16() == 65527
    assert br.read_uint16() == 232


def test_read_uint8():
    assert br.read_uint8() == 255
    assert br.read_uint8() == 16


def test_text_reading():
    assert br.read_text(12) == "Hello world!"


def test_read_array():
    assert br.read_int_array(3, "int16") == [1, 10, -10]
    assert br.read_int_array(3, "uint16") == [65535, 0, 23]
    assert br.read_int_array(3, "uint8") == [255, 16, 1]
