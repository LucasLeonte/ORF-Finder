from pathlib import Path
import json
from typing import Iterable

from orf_finder.models import ORFRecord


def write_orfs_to_json(orfs: Iterable[ORFRecord], out_path: Path) -> None:
    """Write an iterable of `ORFRecord` to a JSON file as an array.

    The output file will be created (parent directories created if necessary).
    """
    out_p = Path(out_path)
    entries = []
    for o in orfs:
        entries.append(
            {
                "sequence_id": o.sequence_id,
                "start": o.start,
                "stop": o.stop,
                "frame": o.frame,
                "nt_sequence": o.nt_sequence,
                "aa_sequence": o.aa_sequence,
            }
        )
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(json.dumps(entries, indent=2), encoding="utf-8")
