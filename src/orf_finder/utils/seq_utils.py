from typing import Iterable


def reverse_complement(seq: str) -> str:
    """Return the reverse complement of a DNA sequence.

    - Accepts A, T, C, G and N (case-insensitive).
    - Returns uppercase reverse-complement.

    Raises:
        ValueError: if sequence contains invalid characters.
    """
    if seq is None:
        raise ValueError("Sequence must be a string, got None")

    s = seq.strip().upper()
    if s == "":
        return ""

    valid = set("ATCGN")
    if any(ch not in valid for ch in s):
        raise ValueError("Sequence contains invalid characters (allowed: A,T,C,G,N)")

    trans_table = str.maketrans("ATCGN", "TAGCN")
    return s.translate(trans_table)[::-1]


def chunk_iterable(iterable: Iterable, size: int):
    """Yield successive `size`-sized chunks from `iterable`."""
    it = iter(iterable)
    while True:
        chunk = []
        try:
            for _ in range(size):
                chunk.append(next(it))
        except StopIteration:
            if chunk:
                yield chunk
            break
        yield chunk
