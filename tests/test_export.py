import json
from pathlib import Path

from orf_finder.parser import parse_fasta
from orf_finder.scanner.orf_scanner import find_orfs
from orf_finder.io import write_orfs_to_json


def test_write_orfs_to_json(tmp_path: Path):
    fasta = tmp_path / "in.fasta"
    fasta.write_text(
        ">test\nAAAATGAAATAGGGG\n",
        encoding="utf-8",
    )

    out = tmp_path / "out.json"
    orfs = []
    for hid, seq in parse_fasta(fasta):
        orfs.extend(find_orfs(seq, seq_id=hid, min_len=9))

    write_orfs_to_json(orfs, out)

    data = json.loads(out.read_text(encoding="utf-8"))
    assert len(data) == 1
    rec = data[0]
    assert rec["sequence_id"] == "test"
    assert rec["start"] == 4
    assert rec["stop"] == 12
    assert rec["aa_sequence"] == "MK"
