#!/usr/bin/env python3
"""ARC188: read-only indexed trace checks with logarithmic verifier state.
Finite controls only. Not FLMV time/space measurements or an ordinary SAT solver.
"""
from dataclasses import dataclass, replace
from collections import Counter
import json
import math
import pathlib

RUN_ID = "ARC-INDEXED-TRACE-TRADEOFF188"
CLAUSE_LABELS = ("EMPTY", "x", "not_x", "y", "not_y")


def formula_sat(word):
    if len(word) != 5 or any(x not in (0, 1) for x in word):
        return False
    if word[0]:
        return False
    return any(
        (not word[1] or x) and (not word[2] or not x)
        and (not word[3] or y) and (not word[4] or not y)
        for x in (0, 1) for y in (0, 1)
    )


def residual(word, var, bit):
    """Source-preserving residual for an actual fixed original variable."""
    v = list(word)
    pos, neg = (1, 2) if var == "x" else (3, 4)
    v[0] |= v[pos] if bit == 0 else v[neg]
    v[pos], v[neg] = 0, 0
    return tuple(v)


@dataclass(frozen=True)
class Event:
    before: tuple
    action: str
    addr: int
    read: int
    write: int
    after: tuple


def transition(before, read):
    phase, i, accum = before
    if phase == "COPY" and 0 <= i < 5 and read in (0, 1):
        after = ("COPY", i + 1, accum) if i < 4 else ("READ", 4, accum)
        return "input_write", i, read, after
    if phase == "READ" and 0 <= i < 5 and read in (0, 1):
        new_accum = accum | (read << i)
        after = ("READ", i - 1, new_accum) if i > 0 else ("OUTPUT", 0, new_accum)
        return "work_read", i, -1, after
    if phase == "OUTPUT" and i == 0 and read == -1:
        src = tuple((accum >> j) & 1 for j in range(5))
        return "output", -1, int(formula_sat(src)), ("HALT", 0, accum)
    raise ValueError("invalid local transition")


def true_trace(source):
    assert len(source) == 5
    state = ("COPY", 0, 0)
    work = {}
    records = []
    while state[0] != "HALT":
        phase, i, acc = state
        read = source[i] if phase == "COPY" else work.get(i, 0) if phase == "READ" else -1
        action, addr, write, next_state = transition(state, read)
        if action == "input_write":
            work[addr] = write
        records.append(Event(state, action, addr, read, write, next_state))
        state = next_state
    assert len(records) == 11
    return records


def verifier(source, trace):
    """Indexed immutable proof; each work read makes a fresh prior-write scan."""
    counts = Counter()
    if (
        len(source) != 5 or len(trace) != 11
        or not all(isinstance(v, int) and v in (0, 1) for v in source)
    ):
        return False, counts
    state = ("COPY", 0, 0)
    for t, row in enumerate(trace):
        counts["records_scanned"] += 1
        if row.before != state:
            return False, counts
        try:
            action, addr, write, next_state = transition(state, row.read)
        except (ValueError, TypeError):
            return False, counts
        if (row.action, row.addr, row.write, row.after) != (
            action, addr, write, next_state
        ):
            return False, counts
        if action == "input_write":
            counts["indexed_source_reads"] += 1
            if source[addr] != row.read:
                return False, counts
        elif action == "work_read":
            latest = 0
            for old in trace[:t]:
                counts["indexed_proof_reads"] += 1
                if old.action == "input_write" and old.addr == addr:
                    latest = old.write
            if row.read != latest:
                return False, counts
        state = next_state
    return state[0] == "HALT", counts


def unsat_certificate(source, trace):
    """Accept only a source-authenticated rejecting (UNSAT) trace."""
    accepted, counts = verifier(source, trace)
    return accepted and trace[-1].write == 0, counts


def perturbations(tr):
    z = list(tr)
    bad = [
        z[:-1],
        z + [z[-1]],
        [replace(z[0], read=1 - z[0].read)] + z[1:],
        z[:1] + [replace(z[1], write=1 - z[1].write)] + z[2:],
        z[:5] + [replace(z[5], read=1 - z[5].read)] + z[6:],
        z[:6] + [replace(z[6], addr=(z[6].addr + 1) % 5)] + z[7:],
        z[:10] + [replace(z[10], write=1 - z[10].write)],
        z[:7] + [replace(z[7], before=("READ", 0, 0))] + z[8:],
    ]
    return bad


def run():
    checks = 0
    sats = 0
    unsats = 0
    proof_scans = []
    roots = []
    two_level = 0
    forged = 0
    accepted_unsat = 0
    rejected_sat = 0
    for bits in range(32):
        src = tuple((bits >> i) & 1 for i in range(5))
        sat = formula_sat(src)
        sats += int(sat)
        unsats += int(not sat)
        tr = true_trace(src)
        valid, usage = verifier(src, tr)
        assert valid and tr[-1].write == int(sat)
        accepted, _ = unsat_certificate(src, tr)
        assert accepted == (not sat)
        accepted_unsat += int(accepted)
        rejected_sat += int(not accepted)
        checks += 2
        proof_scans.append(usage["indexed_proof_reads"])
        for fake in perturbations(tr):
            assert not verifier(src, fake)[0]
            checks += 1
            forged += 1
        label = []
        for bx in (0, 1):
            one = residual(src, "x", bx)
            for by in (0, 1):
                child = residual(one, "y", by)
                child_trace = true_trace(child)
                ok, _ = verifier(child, child_trace)
                cert_ok, _ = unsat_certificate(child, child_trace)
                assert ok and formula_sat(child) == (not child[0])
                assert cert_ok == (not formula_sat(child))
                checks += 2
                two_level += 1
                label.append(formula_sat(child))
        assert sat == any(label)
        assert (not sat) == all(not x for x in label)
        checks += 2
        roots.append({
            "source": "".join(map(str, src)), "sat": sat,
            "child_sat": [bool(v) for v in label],
        })
    max_r = 11
    address_bits = math.ceil(math.log2(5 + max_r + 2))
    modeled_index_bit_ops = (max_r ** 2 + 5) * (address_bits ** 2)
    assert len(proof_scans) == 32 and min(proof_scans) == max(proof_scans)
    checks += 1
    result = {
        "run_id": RUN_ID,
        "status": "COMPUTATIONAL",
        "source_language": "five-bit optional clauses [EMPTY,x,not x,y,not y]",
        "sources": 32, "sat": sats, "unsat": unsats,
        "two_level_actual_descendants": two_level,
        "source_unsat_certificates_accepted": accepted_unsat,
        "source_sat_certificates_rejected": rejected_sat,
        "rejected_corrupted_traces": forged,
        "assertion_groups": checks, "failures": 0,
        "trace_records": max_r, "source_input_bits": 5,
        "all_witnesses_have_indexed_proof_scans": proof_scans[0],
        "modeled_address_bits": address_bits,
        "conservative_index_bit_operations_budget": modeled_index_bit_ops,
        "warning": "abstract record/index counts; not measured FLMV-machine steps",
        "roots": roots,
    }
    out = pathlib.Path(__file__).with_name(
        "2026-10-26_1627_ARC188_indexed_trace_raw.json"
    )
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf8")
    print(json.dumps({k: v for k, v in result.items() if k != "roots"}, indent=2))
    return result


if __name__ == "__main__":
    run()
