#!/usr/bin/env python3
"""Finite firewall: verifying a routed adaptive-RAM trace is not generating it."""

from __future__ import annotations

import hashlib
import itertools
import json
import time


def step(m, t, state, guessed_read):
    a, q = state
    read_addr = a
    b = guessed_read
    write_addr = (a + 1 + b + (q & 1)) % m
    write_value = b ^ (t & 1) ^ (q & 1)
    next_q = q ^ b
    next_a = (write_addr + next_q + 1) % m
    events = [
        {"time": 2 * t, "kind": "R", "addr": read_addr, "value": b},
        {"time": 2 * t + 1, "kind": "W", "addr": write_addr, "value": write_value},
    ]
    return (next_a, next_q), events


def build_claim(m, source_bits, guesses):
    state = (0, 0)
    states = [state]
    events = []
    for t, b in enumerate(guesses):
        state, new_events = step(m, t, state, b)
        events.extend(new_events)
        states.append(state)
    route = sorted(range(len(events)), key=lambda i: (events[i]["addr"], events[i]["time"]))
    return {"m": m, "source": tuple(source_bits), "guesses": tuple(guesses),
            "states": tuple(states), "events": tuple(events), "route": tuple(route),
            "output": state}


def verify_claim(claim):
    m = claim.get("m")
    source = claim.get("source")
    guesses = claim.get("guesses")
    states = claim.get("states")
    events = claim.get("events")
    route = claim.get("route")
    output = claim.get("output")
    if not isinstance(m, int) or m <= 0 or len(source) != m:
        return False
    if any(bit not in (0, 1) for bit in source) or any(bit not in (0, 1) for bit in guesses):
        return False
    if len(states) != len(guesses) + 1 or states[0] != (0, 0):
        return False
    if len(events) != 2 * len(guesses) or output != states[-1]:
        return False
    for t, b in enumerate(guesses):
        expected_state, expected_events = step(m, t, states[t], b)
        if states[t + 1] != expected_state:
            return False
        if list(events[2 * t:2 * t + 2]) != expected_events:
            return False
    if sorted(route) != list(range(len(events))):
        return False
    routed = [events[i] for i in route]
    if any((routed[i]["addr"], routed[i]["time"]) >
           (routed[i + 1]["addr"], routed[i + 1]["time"])
           for i in range(len(routed) - 1)):
        return False
    last = dict(enumerate(source))
    for event in routed:
        if not (0 <= event["addr"] < m) or event["value"] not in (0, 1):
            return False
        if event["kind"] == "W":
            last[event["addr"]] = event["value"]
        elif event["kind"] == "R":
            if event["value"] != last[event["addr"]]:
                return False
        else:
            return False
    return True


def actual_run(m, source, depth):
    memory = list(source)
    state = (0, 0)
    reads = []
    for t in range(depth):
        b = memory[state[0]]
        reads.append(b)
        state, events = step(m, t, state, b)
        write = events[1]
        memory[write["addr"]] = write["value"]
    return tuple(reads), state


def main():
    started = time.time()
    candidates = accepted = cases = corruptions = assertions = 0
    digest = hashlib.sha256()
    per_m = {}
    for m in (2, 4, 8):
        local_candidates = local_cases = 0
        for source in itertools.product((0, 1), repeat=m):
            for depth in range(1, 9):
                cases += 1
                local_cases += 1
                actual_reads, actual_output = actual_run(m, source, depth)
                good_claim = build_claim(m, source, actual_reads)
                assert verify_claim(good_claim)
                assert good_claim["output"] == actual_output
                assertions += 2
                accept_count = 0
                for guesses in itertools.product((0, 1), repeat=depth):
                    claim = build_claim(m, source, guesses)
                    ok = verify_claim(claim)
                    candidates += 1
                    local_candidates += 1
                    accept_count += int(ok)
                    assert ok == (tuple(guesses) == actual_reads)
                    assertions += 1
                assert accept_count == 1
                accepted += accept_count
                assertions += 1
                if len(good_claim["route"]) >= 2:
                    bad = dict(good_claim)
                    route = list(bad["route"])
                    route[0], route[1] = route[1], route[0]
                    bad["route"] = tuple(route)
                    assert not verify_claim(bad)
                    corruptions += 1
                    assertions += 1
                bad_output = dict(good_claim)
                bad_output["output"] = (good_claim["output"][0], good_claim["output"][1] ^ 1)
                assert not verify_claim(bad_output)
                corruptions += 1
                assertions += 1
                digest.update(bytes(source + actual_reads + actual_output))
        per_m[str(m)] = {"cases": local_cases, "candidates": local_candidates}

    malformed = build_claim(2, (0, 1), (0,))
    malformed = dict(malformed)
    malformed["source"] = (0, 2)
    assert not verify_claim(malformed)
    assertions += 1
    summary = {
        "status": "COMPUTATIONAL",
        "model": "deterministic adaptive bit-RAM trace relation",
        "depths": [1, 8],
        "memory_cells": [2, 4, 8],
        "cases": cases,
        "candidate_transcripts": candidates,
        "accepted_transcripts": accepted,
        "corruption_rejections": corruptions + 1,
        "assertions": assertions,
        "unique_accepting_trace_per_case": accepted == cases,
        "digest": digest.hexdigest(),
        "elapsed_seconds": round(time.time() - started, 6),
        "per_memory_size": per_m,
        "limitation": "enumeration demonstrates the acquisition/verification gap; it is not a search lower bound",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
