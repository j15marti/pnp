#!/usr/bin/env python3
"""Independent exact checks for UNIT-TAIL-REPLAY1; no asymptotic runtime claim."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import signal
import time


def main():
    def timeout(*_):
        raise TimeoutError('25-second independent review limit')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(25)
    started = time.perf_counter()
    candidate = Path(__file__).resolve().with_name('unit_tail_replay.py')
    spec = importlib.util.spec_from_file_location('reviewed_unit_tail', candidate)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    clauses = [()] + [(i,) for i in (1, -1, 2, -2, 3, -3)]
    for a, b in ((1, 2), (1, 3), (2, 3)):
        clauses.extend(itertools.product((a, -a), (b, -b)))
    checks = 0
    collision_rejections = 0
    for count in range(4):
        for formula in itertools.combinations(clauses, count):
            # Separate truth-table implementation, independent of both solvers.
            expected = any(all(any(((assignment >> (abs(lit)-1)) & 1) == (lit > 0)
                                   for lit in clause) for clause in formula)
                           for assignment in range(8))
            for budget in (0, 256):
                solver = module.UnitTailReplaySolver(formula, 3, frontier_cap=0,
                                                     cache_budget_bits=budget,
                                                     digest_bytes=0)
                answer, metrics = solver.solve()
                assert answer == expected, (formula, budget, answer, expected)
                assert solver.cache_bits <= budget
                collision_rejections += metrics['cache_hash_collisions_rejected']
                checks += 1
    result = {
        'status': 'PASS', 'answer_checks': checks,
        'formulas': checks // 2, 'clause_universe_size': len(clauses),
        'max_clauses': 3, 'variables': 3, 'frontier_cap': 0,
        'cache_budgets': [0, 256], 'digest_bytes': 0,
        'cache_collision_rejections': collision_rejections,
        'elapsed_seconds': time.perf_counter() - started,
        'candidate_sha256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
        'base_sha256': hashlib.sha256(Path(module._base.__file__).read_bytes()).hexdigest(),
        'review_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'limitations': [
            'Finite semantic checks, not a favorable general-input time-space theorem.',
            'Unit-chain active descriptor payload is O(scope bits + n); ancestor branches, cache, source access and temporary working data are separate.',
            'O(u(scope bits + n)) is an upper bound for the original u-frame descriptor accounting, not a universal lower bound.',
            'Omission of pre-unit cache insertions can change subsequent reuse and total work.',
            'Logical payload counters are neither Python heap measurement nor a complete machine-space bound.'
        ]
    }
    destination = Path(__file__).with_name('unit_tail_review_results.json')
    destination.write_text(json.dumps(result, indent=2) + '\n')
    signal.alarm(0)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
