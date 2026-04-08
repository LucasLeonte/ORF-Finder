from typing import List, Iterable
from pathlib import Path

from orf_finder.models import ORFRecord
from orf_finder.translator.translator import translate
from orf_finder.utils.seq_utils import reverse_complement


STOP_CODONS = {"TAA", "TAG", "TGA"}


def _scan_frame(seq: str, offset: int, frame_sign: int, seq_id: str, min_len: int) -> Iterable[ORFRecord]:
    n = len(seq)
    i = offset
    while i + 3 <= n:
        codon = seq[i : i + 3]
        if codon == "ATG":
            # found start; scan to next in-frame stop
            j = i + 3
            while j + 3 <= n:
                c2 = seq[j : j + 3]
                if c2 in STOP_CODONS:
                    nt_seq = seq[i : j + 3]
                    aa_seq = translate(nt_seq)
                    # Trim trailing stop '*' if present
                    if aa_seq.endswith("*"):
                        aa_seq = aa_seq[:-1]
                    start_pos = i + 1
                    stop_pos = j + 3
                    frame = frame_sign * (offset + 1) // (offset + 1)  # placeholder, corrected below
                    yield ORFRecord(sequence_id=seq_id, start=start_pos, stop=stop_pos, frame=frame, nt_sequence=nt_seq, aa_sequence=aa_seq)
                    # advance i to the codon after this stop to avoid nested starts inside reported ORF
                    i = j + 3
                    break
                j += 3
            else:
                # no stop found; break out
                i += 3
        else:
            i += 3


def find_orfs(seq: str, seq_id: str = "seq", min_len: int = 100) -> List[ORFRecord]:
    """Find ORFs in all 6 frames for given sequence.

    - `seq` must be uppercase and only contain A,T,C,G,N (N treated as non-start/stop).
    - Returns list of `ORFRecord` with 1-based coordinates relative to original sequence.
    - Frames: +1,+2,+3 for forward; -1,-2,-3 for reverse.
    """
    seq = seq.strip().upper()
    results: List[ORFRecord] = []
    L = len(seq)

    # Forward frames
    for offset in range(3):
        for orf in _scan_frame(seq, offset, +1, seq_id, min_len):
            if len(orf.nt_sequence) >= min_len:
                # compute frame +1..+3
                orf.frame = offset + 1
                results.append(orf)

    # Reverse frames
    rc = reverse_complement(seq)
    for offset in range(3):
        for orf in _scan_frame(rc, offset, -1, seq_id, min_len):
            if len(orf.nt_sequence) >= min_len:
                # map coords back to original sequence
                # rc ORF has rc_start = orf.start -1 (0-based), rc_stop = orf.stop -1 (inclusive)
                rc_start0 = orf.start - 1
                rc_stop_end0 = orf.stop - 1
                # compute original 1-based coordinates
                start_orig = L - (rc_stop_end0 + 1) - (0)  # L - (rc_stop_end0+1) +1? we'll correct below
                # Using formula: start = L - (rc_end_excl) +1 ; rc_end_excl = rc_stop_start +3 = (rc_stop0 -2)+3? Simpler recompute via indices
                rc_i = rc_start0
                rc_k = rc_stop_end0 - 2  # rc_k is start index of stop codon in rc (0-based)
                # recompute using general formula
                e_excl = rc_k + 3
                start = L - e_excl + 1
                stop = L - rc_i
                # update orf fields
                orf.start = start
                orf.stop = stop
                # frame as negative
                orf.frame = -(offset + 1)
                results.append(orf)

    # Sort results by sequence_id and start
    results.sort(key=lambda r: (r.sequence_id, r.start))
    return results
