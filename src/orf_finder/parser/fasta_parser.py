from pathlib import Path
from typing import Iterator, Tuple


def parse_fasta(path: Path) -> Iterator[Tuple[str, str]]:
    """Simple FASTA parser yielding tuples (header, sequence).

    - `path` may be a Path or string to a FASTA file.
    - Sequences are returned as uppercase, without whitespace.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"FASTA file not found: {p}")

    header = None
    seq_lines = []
    with p.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n\r")
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(seq_lines).replace(" ", "").upper()
                header = line[1:].strip()
                seq_lines = []
            else:
                seq_lines.append(line.strip())

    if header is not None:
        yield header, "".join(seq_lines).replace(" ", "").upper()
