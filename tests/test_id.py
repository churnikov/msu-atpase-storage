from msu_atpase_storage.id_gen import generate_id


def test_id_1():
    assert generate_id(1) == "000001"


def test_id_10():
    assert generate_id(10) == "000010"


def test_id_101():
    assert generate_id(101) == "000101"


def test_id_999999():
    assert generate_id(999999) == "999999"
