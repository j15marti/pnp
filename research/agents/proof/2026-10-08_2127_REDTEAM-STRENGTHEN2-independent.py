#!/usr/bin/env python3
"""Independent guard-embedding audit, hard 24-second cooperative limit.

Pass the authenticated original portfolio file as argv[1].
"""
import hashlib, importlib.util, itertools, json, random, signal, sys, time
from pathlib import Path
signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('24 second budget')))
signal.alarm(24)
source = Path(sys.argv[1])
body = source.read_bytes()
blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
assert blob == '51f0a58467370a04284aee4c1cccfd97a4a61f91'
spec = importlib.util.spec_from_file_location('authenticated_portfolio', source)
old = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = old
spec.loader.exec_module(old)

def parity(triple):
    return tuple(tuple(-v if bit else v for v, bit in zip(triple, bits))
                 for bits in itertools.product((0, 1), repeat=3) if sum(bits) % 2)

def embed(formula, n):
    h, r, a, b, c, d = range(n + 1, n + 7)
    return (formula + ((h, r),) + parity((h, a, b)) + parity((h, c, d))
            + tuple((h, v, n + 6 + v) for v in range(1, n + 1)))

restriction_checks = assignment_checks = 0
def check(formula, n):
    global restriction_checks, assignment_checks
    result = embed(formula, n)
    assert old.run_portfolio(result)[0] is None
    h, r, a, b, c, d = range(n + 1, n + 7)
    triples = ((h, a, b), (h, c, d))
    pairs = [(u, v, t) for triple in triples for u, v in itertools.combinations(triple, 2)
             for t in triple if t not in (u, v)]
    for width in (1, 2):
        for backdoor in itertools.combinations(range(1, 2 * n + 7), width):
            chosen = set(backdoor)
            assignment = {v: False for v in chosen}
            if chosen == {h, r}:
                assignment[h] = True
            else:
                u, v, t = next(p for p in pairs if not (chosen & set(p[:2])))
                if t in chosen:
                    assignment[t] = True
            assert not old.is_horn(old.restrict(result, assignment))
            restriction_checks += 1
    for bits in itertools.product((False, True), repeat=n):
        assignment = dict(zip(range(1, n + 1), bits))
        value = old.evaluate(formula, assignment)
        assignment.update({h: True, r: True, a: True, b: False, c: True, d: False})
        assignment.update({n + 6 + v: False for v in range(1, n + 1)})
        assert old.evaluate(result, assignment) == value
        assignment_checks += 1

started = time.monotonic()
cases = 0
clauses = parity((1, 2, 3)) + tuple(tuple(-x for x in c) for c in parity((1, 2, 3)))
for mask in range(1, 256):
    formula = tuple(c for j, c in enumerate(clauses) if mask >> j & 1)
    check(formula, 3)
    cases += 1
rng = random.Random(2119)
for n in (4, 5, 6):
    for _ in range(24):
        formula = tuple(tuple(v if rng.getrandbits(1) else -v for v in rng.sample(range(1, n + 1), 3)) for j in range(12))
        if set(old.variables(formula)) == set(range(1, n + 1)):
            check(formula, n)
            cases += 1
for formula in [((1, 2, 3), (1, 2, 4), (1, 3, 4)), ((1, 2, 3), (1, 4, 5))]:
    assert old.run_portfolio(formula)[0] is None
signal.alarm(0)
print(json.dumps({'status': 'COMPUTATIONAL', 'passed': True, 'seed': 2119,
                  'embedding_cases': cases, 'small_controls': 2,
                  'restriction_witness_checks': restriction_checks,
                  'source_assignment_extension_checks': assignment_checks,
                  'seconds': time.monotonic() - started,
                  'portfolio_git_blob': blob,
                  'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'scope': 'Bounded semantics only; symbolic encoding and local-bit interface need separate proof.'}, indent=2))
