from dataclasses import dataclass


@dataclass
class ORFRecord:
    sequence_id: str
    start: int  # 1-based inclusive
    stop: int   # 1-based inclusive
    frame: int  # +1..+3 or -1..-3
    nt_sequence: str
    aa_sequence: str
