#!/usr/bin/env python3
"""Bounded regression: disjunctive cover followed by the existing double wrapper.
Run with the path to experiments/DOUBLE_WRAPPER_2026-10-07/double_wrapper.py.
Finite correctness and cost proxies only; no asymptotic or space theorem.
"""
import hashlib
import importlib.util
import itertools
import json
import signal
import sys
import time
from collections import Counter
from pathlib import Path

def timeout(*args):
    raise TimeoutError('25-second batch budget exceeded; split the case list')

signal.signal(signal.SIGALRM, timeout)
signal.alarm(25)
start = time.perf_counter()
source = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('double_wrapper', source)
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)
cases = [(family, seed, f) for family, seed, f in w.cases()
         if family in ('exhaustive_3var', 'random_8var', 'PHP_4_3', 'PHP_3_3',
                       'XOR_SAT', 'XOR_UNSAT', 'disjoint',
                       'planted_separator_bridges_0')]
# Reference answers are acquired before the production code is guarded.
expected = [w.reference(w.normalize(f)) for _, _, f in cases]
reference_calls = [0]
def forbidden_reference(*args):
    reference_calls[0] += 1
    raise AssertionError('Production path called the reference SAT solver')
w.reference = forbidden_reference
rows = []
checks = 0
for (family, seed, raw), want in zip(cases, expected):
    f = w.normalize(raw)
    boundary = sorted({abs(x) for clause in f for x in clause})[:2]
    for strategy in ('flat', 'separator_fast'):
        metrics = Counter()
        answers = []
        for bits in itertools.product((False, True), repeat=len(boundary)):
            child = w.restrict(f, dict(zip(boundary, bits)), metrics)
            answer, cm = w.outer(child, strategy)
            answers.append(answer)
            metrics['branches_evaluated'] += 1
            metrics['literal_visits'] += cm['literal_visits']
            metrics['dag_nodes'] += cm['dag_nodes']
        assert any(answers) == want, (family, seed, strategy)
        checks += 1
        rows.append(dict(family=family, seed=seed, strategy=strategy,
                         answer=want, metrics=dict(metrics)))
# Failure of accepting the first UNSAT residual as the parent result.
assert any((False, True)) is True
out = dict(status='COMPUTATIONAL', formula_cases=len(cases),
           combined_solver_checks=checks, errors=0,
           guarded_reference_calls=reference_calls[0],
           source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
           runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           seconds=time.perf_counter()-start,
           scope='Fixed two-variable Shannon cover plus exact recursive double wrapper; all branches evaluated.',
           limitations=['Literal visits omit sorting, hashing and other work.',
                        'No peak-space or asymptotic resource bound.',
                        'Decision-only normalization does not preserve original lineage.',
                        'No novel merge rule or general-input speedup established.'], rows=rows)
dest = Path(sys.argv[2]) if len(sys.argv)>2 else Path(__file__).with_suffix('.json')
dest.write_text(json.dumps(out, indent=2)+'\n')
signal.alarm(0)
print(json.dumps({k:v for k,v in out.items() if k!='rows'}, indent=2))
