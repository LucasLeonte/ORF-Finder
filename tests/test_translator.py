from orf_finder.translator.translator import translate


def test_translate_simple():
    assert translate("ATG") == "M"
    assert translate("TAA") == "*"
    assert translate("ATGTAA") == "M*"


def test_translate_unknown_codon():
    assert translate("NNN") == "X"
