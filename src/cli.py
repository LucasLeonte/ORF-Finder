#!/usr/bin/env python3
"""Simple CLI to find ORFs in a FASTA and export JSON results."""
import argparse
from pathlib import Path
from typing import List

from orf_finder.parser import parse_fasta
from orf_finder.scanner.orf_scanner import find_orfs
from orf_finder.io import write_orfs_to_json


def main(argv: List[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Parse FASTA and export ORFs to JSON")
    p.add_argument("fasta", type=Path, help="Input FASTA file")
    p.add_argument("-o", "--out", type=Path, default=Path("orfs.json"), help="Output JSON path")
    p.add_argument("--min-len", type=int, default=100, help="Minimum ORF length in nt")
    args = p.parse_args(argv)

    all_orfs = []
    for header, seq in parse_fasta(args.fasta):
        all_orfs.extend(find_orfs(seq, seq_id=header, min_len=args.min_len))

    write_orfs_to_json(all_orfs, args.out)


if __name__ == "__main__":
    main()
