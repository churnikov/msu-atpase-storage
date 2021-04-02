def generate_id(id_: int, size: int = 6):
    raw_id = str(id_)
    return "".join(["0"] * (size - len(raw_id))) + raw_id
