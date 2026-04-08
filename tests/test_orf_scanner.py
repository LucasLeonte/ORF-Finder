from orf_finder.scanner.orf_scanner import find_orfs
from orf_finder.utils.seq_utils import reverse_complement


def test_find_forward_orf():
    seq = "AAAATGAAATAGGGG"
    orfs = find_orfs(seq, seq_id="test", min_len=9)
    assert len(orfs) == 1
    orf = orfs[0]
    assert orf.start == 4
    assert orf.stop == 12
    assert orf.frame == 1
    assert orf.aa_sequence == "MK"


def test_find_reverse_orf():
    rc_orf = "ATGAAATAG"  # rc contains a forward ORF
    seq = reverse_complement(rc_orf)
    orfs = find_orfs(seq, seq_id="rev", min_len=9)
    assert len(orfs) == 1
    orf = orfs[0]
    assert orf.frame < 0
    # ensure coordinates map within sequence length and are ordered start <= stop
    assert 1 <= orf.start < orf.stop <= len(seq)
