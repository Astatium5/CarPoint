from typing import Generator

def paginate(data_list: list, count: int) -> Generator[list, None, None]:
    for i in range(0, len(data_list), count):
        yield data_list[i:i + count]
