"""Finite suffix-event and branch-fiber audit. No complete SAT machine timing."""
from collections import Counter
from itertools import product
from math import log2, isclose
import hashlib
import json
from pathlib import Path


def entropy(values):
    counts = Counter(values)
    n = len(values)
    return -sum((c/n)*log2(c/n) for c in counts.values())


def cleaned_suffix(answer):
    # Fixed state, head at origin, one binary cache cell and blank remainder.
    tape = {0: answer}
    events = [(0, "READ", 0, tape[0])]
    tape[1] = "#"
    events.append((1, "TERMINATE", 1, "#"))
    return events


rows = []
for p, q in product((1, 2), repeat=2):
    branches = (p % 2, q % 2)
    answer = int(any(branches))
    rows.append(dict(p=p, q=q, branches=branches, answer=answer,
                     suffix=cleaned_suffix(answer)))
u = [tuple(r["branches"]) for r in rows]
d = [r["answer"] for r in rows]
hu, hd = entropy(u), entropy(d)
equivocation = hu - hd
assert isclose(equivocation, 0.75*log2(3))
assert rows[1]["suffix"] == rows[2]["suffix"]
assert rows[1]["branches"][0] != rows[2]["branches"][0]
# Both labels represented. One read is the actual selected event.
assert set(d) == {0, 1}
repetitions = []
for copies in (1, 3, 9):
    memberships = [{0} for _ in range(copies)]
    rho = sum(0 in e for e in memberships)
    bound = copies*(hu-equivocation)/rho
    assert isclose(bound, hd)
    repetitions.append(dict(copies=copies,rho=rho,corrected_bound=bound))
result = dict(status="COMPUTATIONAL",mode="all four parity pairs; no randomness",
              rows=rows, H_U=hu,H_D=hd,H_U_given_D=equivocation,
              repeats=repetitions,
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              scope="Abstract normalized suffix only; compiler and prefix costs proved separately.")
print(json.dumps(result, indent=2, sort_keys=True))
