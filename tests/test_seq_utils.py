import pytest

from orf_finder.utils.seq_utils import reverse_complement


def test_reverse_complement_simple():
    assert reverse_complement("ATGCCGTA") == "TACGGCAT"


def test_reverse_complement_empty():
    assert reverse_complement("") == ""


def test_reverse_complement_invalid():
    with pytest.raises(ValueError):
        reverse_complement("ATGBZX")
