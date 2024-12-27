from typing import Generator

MAX_LEN = 4096


def split_message(source: str, max_len=MAX_LEN) -> Generator[str]:
    ...