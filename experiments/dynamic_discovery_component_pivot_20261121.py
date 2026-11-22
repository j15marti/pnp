"""One-pivot component backdoor audit. Run at repository root with Python 3."""
from itertools import combinations, product
from hashlib import sha256
import json
import dynamic_accounting_paid_backdoor_20261121 as accounting
import dynamic_construction_connected_hubs_20261121 as hubs


def parity_rows(names, rhs):
    return [tuple(-v if bit else v for v, bit in zip(names, bits))
            for bits in product((0, 1), repeat=3) if sum(bits) % 2 != rhs]


def family(signs):
    gate = 4 * len(signs) + 1
    rows = []
    for i, sign in enumerate(signs):
        x, y, z, t = range(4*i+1, 4*i+5)
        rows.extend(parity_rows((x,y,z), 0))
        rows.extend(parity_rows((x,y,t), 0))
        rows.extend(parity_rows((z,t,gate), sign))
        rows.append((x,y,z))
    return tuple(rows)


def admit(rows, budget):
    names = sorted({abs(lit) for row in rows for lit in row})
    for pivot in [None] + names:
        branches = (rows,) if pivot is None else tuple(
            hubs.restrict(rows, lit) for lit in (-pivot, pivot))
        plan = []
        for branch in branches:
            components = []
            for component in hubs.components(branch):
                key, _ = accounting.find_hit(component, budget)
                if key is None:
                    break
                components.append((component, key))
            else:
                plan.append(components)
                continue
            break
        if len(plan) == len(branches):
            return pivot, plan
    return None


def solve_plan(plan):
    for components in plan:
        for rows, key in components:
            if not any(hubs.binary_sat(accounting.restrict(rows, dict(zip(key, bits))))
                       for bits in product((0,1), repeat=len(key))):
                break
        else:
            return True
    return False


def main():
    counts = []
    for k in range(2, 7):
        labels = []
        for signs in product((0,1), repeat=k):
            rows = family(signs)
            assert len(hubs.components(rows)) == 1
            assert admit(rows, 0) is None
            pivot, plan = admit(rows, 1)
            answer = solve_plan(plan)
            assert answer == (len(set(signs)) == 1)
            if k <= 3:
                assert answer == accounting.truth(rows)
                assert accounting.find_hit(rows, k)[0] is None
                assert accounting.find_hit(rows, k+1)[0] is not None
            labels.append(answer)
        counts.append(dict(k=k, SAT=sum(labels), UNSAT=len(labels)-sum(labels)))
    mod = hubs.construction.codec.load_generator()
    compiled = []
    for signs in [(0,0),(0,1)]:
        rows = family(signs)
        bits, _, _ = hubs.construction.build(mod, rows)
        assert hubs.discovery.extract(mod, bits) == list(rows)
        n, target, _, _, _ = hubs.construction.codec.parse(bits)
        label, version = hubs.construction.z3_result(target, n)
        assert (label == "sat") == solve_plan(admit(rows,1)[1])
        compiled.append(dict(signs=signs, n=n,m=len(target),N=len(bits),
                             sha256_ascii=sha256(bits.encode()).hexdigest(),
                             z3=version,label=label))
    return dict(source=counts,compiled=compiled)


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
