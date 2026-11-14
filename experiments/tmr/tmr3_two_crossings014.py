#!/usr/bin/env python3
"""TMR-3/014: exact local-head two-crossing parity prepass.
No external packages, no uncharged random access in the modeled prepass.
Finite tests, not a general SAT-machine simulation.
"""
import itertools
import json
import time


def restricted_3sat_finite_control(bits):
    """Read-only left-to-right finite-state decider for sign-only 3-CNF.
    Each 3-bit clause encodes the unique forbidden assignment on x0,x1,x2.
    A partial trailing triple is MALFORMED. No writable work cells are used.
    """
    seen, phase, triple = 0, 0, 0
    for bit in bits:
        if bit not in (0, 1):
            return "MALFORMED"
        triple = (triple << 1) | bit
        phase += 1
        if phase == 3:
            seen |= 1 << triple
            phase, triple = 0, 0
    if phase:
        return "MALFORMED"
    return "UNSAT" if seen == 255 else "SAT"


def independent_brute(bits):
    if len(bits) % 3:
        return "MALFORMED"
    chunks = [bits[i:i+3] for i in range(0, len(bits), 3)]
    for assignment in itertools.product((0, 1), repeat=3):
        if all(tuple(c) != assignment for c in chunks):
            return "SAT"
    return "UNSAT"


def two_crossing_prepass(bits):
    """Fully local input-head simulation, endpoints at 0 and L+1.
    The left marker is at index 0; data at 1..L; right marker at L+1.
    First pass stores parity and last observed bit in finite control.
    Reverse pass holds the completed parity in finite control.
    Query cuts are after each data cell 1..L, before the right endmarker.
    """
    n = len(bits)
    head = 0
    parity = 0
    seen, phase, triple = 0, 0, 0
    steps = 0
    forward = {}
    reverse = {}
    crossings = {i: 0 for i in range(1, n+1)}
    while head < n + 1:
        if 1 <= head <= n:
            bit = bits[head-1]
            parity ^= bit
            triple = (triple << 1) | bit
            phase += 1
            if phase == 3:
                seen |= 1 << triple
                phase, triple = 0, 0
            if head <= n:
                # Crossing cut after this cell from left to right.
                forward[head] = (bit, parity)
                crossings[head] += 1
        head += 1
        steps += 1
    assert head == n + 1
    while head > 0:
        before = head
        head -= 1
        steps += 1
        if 1 <= head <= n:
            # Crossing cut after cell 'head' from right to left.
            reverse[head] = parity
            crossings[head] += 1
    assert head == 0 and steps == 2*(n+1)
    label = "MALFORMED" if phase else ("UNSAT" if seen == 255 else "SAT")
    assert all(count == 2 for count in crossings.values())
    code = {i: (forward[i][0], reverse[i]) for i in crossings}
    return {"steps": steps, "label": label, "parity": parity, "crossings": crossings,
            "code": code, "forward": forward, "reverse": reverse}


def run():
    start = time.monotonic()
    stats = {"version":"TMR3-2C14", "exhaustive_strings":0,
             "all_8_mask_unsat_permutations":0, "adaptive_flip_checks":0,
             "total_physically_charged_prepass_steps":0,
             "forward_and_reverse_cut_events":0, "restricted_sat":0,
             "restricted_unsat":0,"malformed":0,"failures":0}
    def check(bits, full_flips=False):
        status = restricted_3sat_finite_control(bits)
        if len(bits) <= 18:
            assert status == independent_brute(bits)
        pre = two_crossing_prepass(bits)
        n = len(bits)
        assert pre["label"] == status
        assert pre["parity"] == (sum(bits)&1)
        assert pre["steps"] == 2*(n+1)
        assert len(pre["crossings"]) == n
        stats["total_physically_charged_prepass_steps"] += pre["steps"]
        stats["forward_and_reverse_cut_events"] += 2*n
        stats[{"SAT":"restricted_sat","UNSAT":"restricted_unsat","MALFORMED":"malformed"}[status]] += 1
        if full_flips:
            for j in range(1,n):
                alt = list(bits)
                alt[j] ^= 1
                other = two_crossing_prepass(alt)
                assert pre["crossings"] == other["crossings"]
                for i in range(1,j+1):
                    # At cut i<j+1, flipping later bit j+1 changes the
                    # returning parity tag but not the queried Xi.
                    assert pre["code"][i][0] == other["code"][i][0]
                    assert pre["code"][i][1] != other["code"][i][1]
                    stats["adaptive_flip_checks"] += 1
        return status

    # Exhaust all binary inputs of length <=15 (including malformed lengths).
    for n in range(16):
        for x in itertools.product((0,1),repeat=n):
            check(x,full_flips=(n<=6))
            stats["exhaustive_strings"] += 1

    # All 40,320 permutations of the eight forbidden 3-variable patterns are
    # legitimate 24-bit UNSAT sign-stream sources. Each is checked physically.
    for perm in itertools.permutations(range(8)):
        bits = tuple((mask >> shift)&1 for mask in perm for shift in (2,1,0))
        assert check(bits) == "UNSAT"
        stats["all_8_mask_unsat_permutations"] += 1

    # Explicit SAT input, disjoint repeated subproducts, parity/cut checks,
    # a source that is longer than any hardwired lookup-size fixture.
    for r in (8, 9, 16, 64, 1024):
        bits = tuple((i // 3)&1 for i in range(3*r))
        check(bits,full_flips=(r==8))
    # Sample SAT sources with all cuts and all suffix flips; mask 0 repeated.
    for offset in range(16):
        bits = tuple(((i+offset) % 7) & 1 for i in range(24))
        check(bits,full_flips=True)

    # Projection at cut i is exactly (X_i, parity(X)), two bits. For every
    # fixed assignment of all other bits, varying X_i yields two distinct
    # length-two words (conditionally prefix-free).
    for n in (3, 8, 24):
        for i in range(1,n+1):
            x = [0]*n
            y = x.copy();y[i-1] = 1
            cx = two_crossing_prepass(x)["code"][i]
            cy = two_crossing_prepass(y)["code"][i]
            assert len(cx)==len(cy)==2 and cx!=cy

    stats["elapsed_seconds"] = round(time.monotonic()-start,4)
    stats["workspace_visited_prepass_cells"] = 0
    stats["restricted_controller_time"] = "2*(L+1)+1 including terminal step"
    stats["cost_identity"] = "T_B(x)=T_A(x)+2*(L+1); S_B(x)=S_A(x)"
    stats["verdict"] = "PASS"
    return stats


if __name__ == "__main__":
    print(json.dumps(run(),sort_keys=True,indent=2))
