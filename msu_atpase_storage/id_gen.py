def generate_id(id_: int, size: int = 6) -> str:
    """
    Generate int id for file with n zeros comming first

    >>> print(generate_id(1))
    000001

    :param id_: integer number of file.
    :param size: size of resulting string
    :return: int id for file with n zeros comming first
    """
    raw_id = str(id_)
    return "".join(["0"] * (size - len(raw_id))) + raw_id
