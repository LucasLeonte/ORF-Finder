# ORF-Finder

Minimal ORF Finder project (educational). Implements utilities to find Open Reading Frames in DNA sequences.

## Quick start

### 1. (Optional) create a virtualenv and install deps:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Run tests:

```powershell
python -m pytest -q
```

Project layout

- `src/orf_finder/` - core modules
- `tests/` - unit tests
- `data/escherichia_coli/` - example fasta files

## CLI Usage

Run the CLI to parse a FASTA and write ORFs to JSON:

```powershell
python -m src.cli data/escherichia_coli/sequence_1.fasta --min-len 100 -o results.json
```

JSON output schema

Each ORF is written as an object in a JSON array with these fields:

- `sequence_id`: FASTA header (string)
- `start`: 1-based inclusive start coordinate (int)
- `stop`: 1-based inclusive stop coordinate (int)
- `frame`: reading frame (+1..+3 for forward, -1..-3 for reverse)
- `nt_sequence`: nucleotide sequence of the ORF (string)
- `aa_sequence`: translated amino-acid sequence (string)

## Source

Escherichia coli CFT073, complete genome: https://www.ncbi.nlm.nih.gov/nuccore/AE014075.1?report=fasta
