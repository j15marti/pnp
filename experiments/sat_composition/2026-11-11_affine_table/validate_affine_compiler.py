"""Independent exhaustive correctness checks of the affine-table prototype."""

from pathlib import Path
import hashlib
import json
import sys
import time

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
SOURCE_CANDIDATES = [
    SCRIPT_DIRECTORY / "affine_table.py",
    SCRIPT_DIRECTORY.parent / "sat_composition_build" / "affine_table.py",
    SCRIPT_DIRECTORY.parent / "affine_table.py",
]
SOURCE_PATH = next((path for path in SOURCE_CANDIDATES if path.is_file()), None)
if SOURCE_PATH is None:
    raise FileNotFoundError("Place affine_table.py beside this verifier or in ../sat_composition_build")
sys.path.insert(0, str(SOURCE_PATH.parent))

from affine_table import Interface, Work, normalize, project, join
from validate_affine_dimension import rho


def main():
    started = time.perf_counter()
    source_path = SOURCE_PATH.resolve()
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    n = 3
    forms = (1, 2, 4)
    interfaces = []
    for mask in range(256):
        table = tuple(bool((mask >> x) & 1) for x in range(8))
        relation = Interface(n, (), forms, table)
        normalized = normalize(relation, Work(cap=6))
        support = {x for x in range(8) if table[x]}
        assert normalized.width == rho(support, n)
        assert all(normalized.accepts(x) == table[x] for x in range(8))
        for private in [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]:
            result = project(normalized, private, Work(cap=6))
            private_mask = sum(1 << v for v in private)
            for x in range(8):
                wanted = any(
                    table[z]
                    for z in range(8)
                    if (z & ~private_mask) == (x & ~private_mask)
                )
                assert result.accepts(x) == wanted
        interfaces.append(normalized)

    for i, first in enumerate(interfaces):
        for j, second in enumerate(interfaces):
            result = join(first, second, Work(cap=6))
            for x in range(8):
                wanted = bool((i >> x) & 1) and bool((j >> x) & 1)
                assert result.accepts(x) == wanted

    source_hash_after = hashlib.sha256(source_path.read_bytes()).hexdigest()
    assert source_hash == source_hash_after, "Source changed during validation"
    report = {
        "status": "all assertions passed",
        "scope": "PROVED restricted operators; all-input polynomial bound OPEN",
        "source_path": str(source_path),
        "source_sha256": source_hash,
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "runtime_seconds": time.perf_counter() - started,
        "normalizations": 256,
        "projections": 2048,
        "joins": 65536,
        "assignment_checks_per_output": 8,
        "normalized_width_checked_against": "dim affine hull minus dim translation stabilizer",
        "limitations": "Exhaustive finite validation supplements the proofs and establishes no asymptotic bound."
    }
    report_path = Path(__file__).with_name("affine_compiler_validation.json")
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
