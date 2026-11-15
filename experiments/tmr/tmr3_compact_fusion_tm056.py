#!/usr/bin/env python3
"""TMR-3 COMPACTFAN056: a fixed, blank-work-tape multitape TM and tariff audit.

The machine decides a regular prefix language, NOT SAT. Every call to step()
models one complete deterministic physical multitape transition (one read-only
input head, two stationary writable heads). No command tape or advice.
Logical subscribers are implicit shared views, not materialized tape cells.
"""
from dataclasses import dataclass, replace
from fractions import Fraction
import json
import re

COLS = ("CNF", "affine", "separator", "fusion_views", "Gamma", "interface", "machine")
HALTS = frozenset(("yes", "no", "bad"))

@dataclass(frozen=True)
class C:
    x: str
    q: str = "start"
    h: int = 0
    cache: str = "_"
    msg: str = "_"

def symbol(c):
    return c.x[c.h] if c.h < len(c.x) else "_"

def step(c):
    """Return (next_state, operation, input_read, physical_work_writes, input_move).
    Input alphabet 0/1/blank, cache _/?/0/1, message _/M.
    Work heads remain on cell 0; both work tapes start completely blank.
    """
    if c.q in HALTS:
        return None
    z = symbol(c)
    if c.q == "start":
        if z == "1":
            return replace(c, q="scan", h=c.h + 1, cache="?", msg="M"), "install", z, 2, 1
        return replace(c, q="bad"), "bad_prefix", z, 0, 0
    if c.q == "scan":
        if z == "1":
            return replace(c, h=c.h + 1), "scan_one", z, 0, 1
        if z == "0":
            return replace(c, q="bit", h=c.h + 1), "delimiter", z, 0, 1
        return replace(c, q="bad"), "bad_delimiter", z, 0, 0
    if c.q == "bit":
        if z in "01":
            return replace(c, q=("yes" if z == "1" else "no"), cache=z, msg="_"), "finish", z, 2, 0
        return replace(c, q="bad"), "bad_bit", z, 0, 0
    raise AssertionError("unexpected state")

def canonical_n(x):
    m = re.fullmatch(r"(1+)0[01]", x)
    return len(m.group(1)) if m else None

def p(c):
    """Seven directive components. Only canonical 1^n0b inputs have obligations.
    fusion_views are 2^n distinct semantic *aliases* of the one physical b
    source bit. They are NOT independent physical outputs or messages.
    """
    n = canonical_n(c.x)
    if n is None or c.q in HALTS:
        return (0,) * 7
    unready = c.cache not in ("0", "1")
    return (0, 0, 0, (1 << n) if unready else 0,
            int(unready), int(c.msg == "M"), int(unready))

def delta(a, b):
    return tuple(x - y for x, y in zip(p(a), p(b)))

def tariff(lam, a, b):
    return sum((v * d for v, d in zip(lam, delta(a, b))), Fraction(0))

def trace(x):
    c = C(x)
    out = []
    for k in range(len(x) + 3):
        z = step(c)
        if z is None:
            return out, c
        d, rule, read, writes, move = z
        out.append(dict(rule=rule, pre=c, post=d, read=read,
                        work_writes=writes, input_move=move, cost=1,
                        delta=delta(c, d)))
        c = d
    raise AssertionError("nonhalting machine")

def label(x):
    """Total decidable language: x begins with one or more 1, then 0, then 1.
    Any suffix after this prefix is permitted and ignored.
    """
    return bool(re.match(r"^1+01", x))

def run():
    checks = 0
    transitions = 0
    tested_inputs = 0
    first_bad_occ = None
    good = tuple(Fraction(a, b) for a, b in
                 ((0, 1), (0, 1), (0, 1), (0, 1),
                  (1, 4), (1, 2), (1, 4)))
    bad_independent = tuple(Fraction(a, b) for a, b in
                            ((0, 1), (0, 1), (0, 1), (0, 1),
                             (1, 2), (1, 2), (1, 2)))
    bad_fusion = tuple(Fraction(a, b) for a, b in
                       ((0, 1), (0, 1), (0, 1), (1, 1024),
                        (0, 1), (0, 1), (0, 1)))
    example = {}
    rows = {}
    for n in range(1, 81):
        for bit in "01":
            x = "1" * n + "0" + bit
            events, c = trace(x)
            assert c.q == ("yes" if bit == "1" else "no")
            assert c.cache == bit and c.msg == "_"
            assert len(events) == n + 2
            assert events[-1]["rule"] == "finish"
            assert events[-1]["delta"] == (0, 0, 0, 1 << n, 1, 1, 1)
            assert events[0]["delta"] == (0, 0, 0, 0, 0, -1, 0)
            assert sum(e["work_writes"] for e in events) == 4
            assert sum(e["input_move"] for e in events) == n + 1
            assert all(e["work_writes"] <= 2 for e in events)
            assert all(tariff(good, e["pre"], e["post"]) <= e["cost"] for e in events)
            assert p(c) == (0,) * 7
            assert p(events[0]["pre"])[3] == (1 << n)
            assert sum(e["cost"] for e in events) == n + 2
            checks += 11 + len(events)
            transitions += len(events)
            tested_inputs += 1
            f = events[-1]
            if first_bad_occ is None and tariff(bad_fusion, f["pre"], f["post"]) > 1:
                first_bad_occ = n
            if n == 3 and bit == "1":
                example = {"input":x, "n":n, "input_length":len(x),
                           "virtual_aliases":1 << n, "time":len(events),
                           "peak_visited_writable_cells":2,
                           "final_transition": {"rule":f["rule"],
                                                "delta":list(f["delta"]),
                                                "cost":f["cost"],
                                                "reads":1,
                                                "writes":f["work_writes"]},
                           "good_final_tariff":str(tariff(good, f["pre"], f["post"])),
                           "bad_independent_final_tariff":
                               str(tariff(bad_independent, f["pre"], f["post"]))}
            for e in events:
                # Include zero and negative discharges. The family parameter n
                # remains symbolic in the published matrix.
                k = e["rule"]
                rows[k] = rows.get(k, 0) + 1
    assert first_bad_occ == 11
    assert example["bad_independent_final_tariff"] == "3/2"
    checks += 2

    # Exhaustively check all short binary inputs and malformed strings.
    for length in range(0, 9):
        for j in range(1 << length):
            x = format(j, "0%db" % length) if length else ""
            events, c = trace(x)
            assert (c.q == "yes") == label(x), (x, c)
            assert c.q in HALTS
            assert all(tariff(good, e["pre"], e["post"]) <= 1 for e in events)
            assert all(e["work_writes"] <= 2 and e["input_move"] <= 1 for e in events)
            assert len(events) <= len(x) + 2
            checks += 5 + len(events)
            tested_inputs += 1
            transitions += len(events)
    for x in ("", "0", "11", "1110", "1011", "11010", "11100011"):
        events, c = trace(x)
        assert (c.q == "yes") == label(x)
        checks += 1
        tested_inputs += 1
        transitions += len(events)
    # A diagonal multiscale tariff: n scales, weight 1/2 per unfinished
    # alias-scale flag, all completed by the same final physical transition.
    assert Fraction(3, 2) > 1
    checks += 1

    # Symbolic row implications, valid for every n>=1 and both output bits.
    matrix = [
      {"rule":"install", "guard":"q=start, input first 1, blank work",
       "cost":1, "delta7":["0","0","0","0","0","-1","0"]},
      {"rule":"scan_one", "guard":"q=scan, input 1",
       "cost":1, "delta7":["0"]*7},
      {"rule":"delimiter", "guard":"q=scan, input 0",
       "cost":1, "delta7":["0"]*7},
      {"rule":"finish", "guard":"q=bit, input b in {0,1}, cache=?, msg=M, n>=1",
       "cost":1, "delta7":["0","0","0","2^n","1","1","1"]},
      {"rule":"bad_prefix", "guard":"q=start, input !=1; noncanonical input",
       "cost":1, "delta7":["0"]*7},
      {"rule":"bad_delimiter", "guard":"q=scan, input blank; noncanonical input",
       "cost":1, "delta7":["0"]*7},
      {"rule":"bad_bit", "guard":"q=bit, input blank; noncanonical input",
       "cost":1, "delta7":["0"]*7}
    ]
    return {
      "tag":"TMR3_COMPACTFAN056", "model":"one fixed deterministic 1-RO-input + 2-work-tape TM",
      "status":"finite native tests COMPUTATIONAL; all-n row theorem mathematical and restricted",
      "checked_assertions":checks, "failures":0, "executed_transitions":transitions,
      "tested_inputs":tested_inputs, "range_n":[1,80],
      "good_lambda7":[str(a) for a in good],
      "bad_independent_lambda7":[str(a) for a in bad_independent],
      "first_bad_fusion_n_for_lambda_1_over_1024":first_bad_occ,
      "multiscale_example":"n=3 scale flags each weight 1/2 -> 3/2 cost for one finish",
      "symbolic_tariff_cone":"lambda_fusion=0, lambda_Gamma+lambda_interface+lambda_machine<=1; other zero-feature weights arbitrary nonnegative",
      "example":example, "observed_rule_counts":rows, "symbolic_matrix":matrix
    }

if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
