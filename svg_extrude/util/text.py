# TODO unit test
def count(count: int, singular: str, plural: str) -> str:
    if count == 1:
        return f"1 {singular}"
    else:
        return f"{count} {plural}"
    