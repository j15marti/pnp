#!/usr/bin/env python3
"""LSPV-4 UPDATE-LOG-REPLAY215: independent exhaustive controls.

No external dependencies. Tests distinct-index read-back, immutable replay,
writable-source update, and a streaming-state fooling set.
These are finite controls; the asymptotic claims are mathematical lemmas.
"""
from __future__ import annotations
import itertools
import json
import math
import hashlib
import random
from collections import Counter
from pathlib import Path

VERSION = "LSPV4_UPDATE_LOG_REPLAY215_v1"
C = Counter()


def check(p, tag):
    C[tag] += 1
    if not p:
        raise AssertionError(f"{tag} assertion {C[tag]} failed")


def truth(bits, commands):
    cur = list(bits)
    answers = []
    for j, v in commands:
        cur[j] = v
        answers.append(int(all(cur)))
    return answers


def ro_distinct(bits, commands):
    """Read immutable source at j once per distinct-coordinate update."""
    z = len(bits) - sum(bits)
    out = []
    for j, v in commands:
        source_bit = bits[j]   # one charged indexed source query
        z += source_bit - v
        out.append(int(z == 0))
    return out


def rw_current(bits, commands):
    """Physically mutable source, one read+write per update."""
    source = list(bits)
    z = len(bits) - sum(source)
    out = []
    for j, v in commands:
        old = source[j]
        z += old - v
        source[j] = v
        out.append(int(z == 0))
    return out, tuple(source)


def ro_log(bits, commands, t):
    """Reconstruct each current bit from original and retained past log."""
    zeros = 0
    for j, initial in enumerate(bits):
        value = initial
        for k in range(t):
            ij, v = commands[k]
            if ij == j:
                value = v
        zeros += (1 - value)
    return int(zeros == 0)


class SequentialInputReplay:
    """Conservative one sequential input-head replay; no free address jumps.

    Physical tape: original m literal bits, then h fixed-width (address,value)
    commands, no output tape. Reads walk the input head to each requested span.
    This is a bit-vector control, not a complete proper-3CNF parser.
    """
    def __init__(self, bits, commands):
        self.m = len(bits)
        self.w = max(1, (self.m - 1).bit_length())
        self.unit = self.w + 1
        self.tape = "".join(map(str, bits)) + "".join(
            format(j, f"0{self.w}b") + str(v) for j, v in commands
        )
        self.head = 0
        self.moves = 0
        self.probes = 0
        self.max_address = 0

    def span(self, start, width):
        if width == 0:
            return ""
        assert 0 <= start and start + width <= len(self.tape)
        self.moves += abs(self.head - start)
        self.head = start
        self.moves += width - 1
        self.head += width - 1
        self.probes += width
        self.max_address = max(self.max_address, start + width - 1)
        return self.tape[start:start+width]

    def decision(self, t):
        zeros = 0
        for j in range(self.m):
            v = int(self.span(j, 1))
            for k in range(t):
                rec = self.span(self.m + k*self.unit, self.unit)
                if int(rec[:self.w], 2) == j:
                    v = int(rec[-1])
            zeros += 1 - v
        return int(zeros == 0)


def witness_suffix(m, a, b):
    """Common continuation distinguishing two distinct intermediate states."""
    za = {i for i in range(m) if not (a >> i) & 1}
    zb = {i for i in range(m) if not (b >> i) & 1}
    target = za if zb - za else zb
    suffix = tuple((i, 1) for i in sorted(target))
    return suffix


def exhaustive_distinct():
    for m in range(1, 8):
        max_h = min(3, m)
        if m <= 5:
            max_h = min(4, m)
        for raw in itertools.product((0, 1), repeat=m):
            for h in range(0, max_h+1):
                for indices in itertools.permutations(range(m), h):
                    for vals in itertools.product((0, 1), repeat=h):
                        cmds = tuple(zip(indices, vals))
                        a = ro_distinct(raw, cmds)
                        b = truth(raw, cmds)
                        check(a == b, "ro_distinct_prefixes")
                        check(len(cmds) == len(set(i for i, _ in cmds)), "distinct_promise")


def exhaustive_rw():
    for m in range(1, 6):
        alphabet = tuple(itertools.product(range(m), (0, 1)))
        for bits in itertools.product((0, 1), repeat=m):
            for h in range(0, 5):
                for cmds in itertools.product(alphabet, repeat=h):
                    res, updated = rw_current(bits, cmds)
                    check(res == truth(bits, cmds), "rw_arbitrary_prefixes")
                    base = list(bits)
                    for j, v in cmds:
                        base[j] = v
                    check(updated == tuple(base), "rw_final_source")


def exhaustive_log():
    for m in range(1, 8):
        alphabet = tuple(itertools.product(range(m), (0, 1)))
        max_h = 3 if m <= 6 else 2
        for bits in itertools.product((0, 1), repeat=m):
            for h in range(max_h+1):
                for cmds in itertools.product(alphabet, repeat=h):
                    expected = int(all(bits)) if h == 0 else truth(bits, cmds)[-1]
                    check(ro_log(bits, cmds, h) == expected,
                          "ro_log_full_prefix")
    # Actual head movements, not counted as unit-cost RAM probes.
    rng = random.Random(2710215)
    max_ratio = 0
    sample = None
    for _ in range(1200):
        m = rng.randint(2, 20)
        h = rng.randint(0, 2*m)
        b = tuple(rng.randint(0, 1) for _ in range(m))
        cmd = tuple((rng.randrange(m), rng.randint(0, 1)) for _ in range(h))
        machine = SequentialInputReplay(b, cmd)
        got = machine.decision(h)
        check(got == ro_log(b, cmd, h), "sequential_replay_correct")
        X = len(machine.tape)
        # Each of m loops scans at most h records and one source position.
        check(machine.moves <= 2*m*(h+1)*max(1, X),
              "sequential_replay_head_bound")
        check(machine.probes == m*(1+h*machine.unit),
              "sequential_replay_probe_count")
        check(machine.max_address < X, "sequential_head_within_input")
        ratio = machine.moves / max(1, m*(h+1)*X)
        if ratio > max_ratio:
            max_ratio = ratio
            sample = {"m":m,"h":h,"input_bits":X,
                      "moves":machine.moves,"probes":machine.probes,
                      "ratio":ratio}
    return sample


def streaming_fooling():
    for m in range(1, 9):
        for a in range(1 << m):
            for b in range(a+1, 1 << m):
                continuation = witness_suffix(m,a,b)
                aa = tuple((a >> i)&1 for i in range(m))
                bb = tuple((b >> i)&1 for i in range(m))
                final_a = truth(aa, continuation)[-1] if continuation else int(all(aa))
                final_b = truth(bb, continuation)[-1] if continuation else int(all(bb))
                check(final_a != final_b, "fooling_pair_distinguished")
                check(len(continuation)<=m, "fooling_suffix_length")
    return {"m":8,"distinct_midpoint_states":256,
            "required_retained_state_bits":8,
            "updates_to_midpoint":8,"max_updates_in_suffix":8}




def unit3(lit, a, b):
    return [(lit, a, b), (lit, a, -b), (lit, -a, b), (lit, -a, -b)]


def scalar_cnf(bits):
    """Independent reconstruction of the prior proper-3CNF scalar gadget."""
    m = len(bits)
    x = [i + 1 for i in range(m)]
    y = [m + i + 1 for i in range(m + 1)]
    u = [2*m + i + 2 for i in range(m)]
    v = [3*m + i + 2 for i in range(m)]
    t = [4*m + i + 2 for i in range(m)]
    w = [5*m + i + 2 for i in range(m)]
    end = [6*m + i + 2 for i in range(4)]
    clauses = unit3(y[0], end[0], end[1])
    for i, bit in enumerate(bits):
        clauses.extend(unit3(x[i] if bit else -x[i], u[i], v[i]))
        p, q, a, b = y[i], y[i+1], t[i], w[i]
        clauses.extend([(-q,p,a),(-q,p,-a),(-q,x[i],b),(-q,x[i],-b),(q,-p,-x[i])])
    clauses.extend(unit3(y[-1], end[2], end[3]))
    return 6*m + 5, tuple(clauses)


def independent_dpll(clauses):
    def reduce(cnf):
        while True:
            if () in cnf:
                return False
            unit = next((clause[0] for clause in cnf if len(clause) == 1), None)
            if unit is None:
                break
            cnf = tuple(tuple(l for l in c if l != -unit) for c in cnf if unit not in c)
        if not cnf:
            return True
        pivot = cnf[0][0]
        for lit in (pivot, -pivot):
            new = tuple(tuple(l for l in c if l != -lit) for c in cnf if lit not in c)
            if reduce(new):
                return True
        return False
    return reduce(clauses)


def exact_cnf_controls():
    for m in range(1, 7):
        for bits in itertools.product((0,1), repeat=m):
            nv, before = scalar_cnf(bits)
            check(nv == 6*m+5 and len(before) == 9*m+8, "proper_cnf_size")
            check(all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in before),
                  "proper_cnf_distinct_vars")
            check(independent_dpll(before) == bool(all(bits)), "cnf_sat_decision")
            for j in range(m):
                for val in (0, 1):
                    changed = list(bits)
                    changed[j] = val
                    _, after = scalar_cnf(changed)
                    literal_changes = sum(1 for a, b in zip(before, after)
                                          for v1, v2 in zip(a, b) if v1 != v2)
                    check(literal_changes == 4*int(bits[j] != val),
                          "four_sign_controls")
                    check(independent_dpll(after) == bool(all(changed)),
                          "cnf_update_decision")


def main():
    exact_cnf_controls()
    exhaustive_distinct()
    exhaustive_rw()
    sample = exhaustive_log()
    fool = streaming_fooling()
    result = {
      "version":VERSION,"status":"all finite controls passed",
      "assertions":sum(C.values()),"failures":0,
      "by_category":dict(sorted(C.items())),
      "max_sampled_sequential_head_ratio":sample,
      "one_pass_fooling_control":fool,
      "model_note":"log replay needs a physically readable log; stream fooling needs a consumed non-rereadable update history",
    }
    out = Path(__file__).with_name('2026-10-29_0003_LSPV4_UPDATE_LOG_REPLAY215_raw.json')
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()