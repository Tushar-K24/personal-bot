from __future__ import annotations

from .utils import rand_gen


def main_func(num: int) -> dict[str, int]:
    d = rand_gen(num)
    return d
