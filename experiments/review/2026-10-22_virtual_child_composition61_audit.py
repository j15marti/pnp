#!/usr/bin/env python3
"""Finite audit for VIRTUAL-CHILD-COMPOSITION61.

Checks that arbitrary read-only-input procedures can be simulated on locally
indexable virtual children without materializing child buffers.  Also records
the batch-storage and per-child-rescan controls.  No unrestricted ARC
constructor or complexity-class separation is claimed.
"""

import json
import math
import random


class VirtualChild:
    def __init__(self, parent, descriptor, length):
        self.parent = parent
        self.a, self.b, self.mask = descriptor
        self.length = length
        self.reads = 0

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        if not 0 <= index < self.length:
            raise IndexError(index)
        self.reads += 1
        pos = (self.a * index + self.b) % len(self.parent)
        return self.parent[pos] ^ ((self.mask >> (index % 8)) & 1)


def materialize(parent, descriptor, length):
    a, b, mask = descriptor
    return [
        parent[(a * i + b) % len(parent)] ^ ((mask >> (i % 8)) & 1)
        for i in range(length)
    ]


def read_only_procedure(bits):
    """A deterministic, adaptive, rereading input procedure."""
    n = len(bits)
    state = 0x9E3779B9
    score = 0
    requests = 0
    steps = 3 * n + 17
    for step in range(steps):
        index = (state + step * step + score * 13) % n
        bit = bits[index]
        requests += 1
        score = (score + bit + (state & 1)) % (n + 1)
        state = ((state << 5) ^ (state >> 2) ^ (index * 257) ^ bit) & 0xffffffff
    # Deliberate rereads at addresses selected by the prior transcript.
    for offset in range(min(11, n)):
        index = (state + 19 * offset + score) % n
        score ^= bits[index] << (offset % 7)
        requests += 1
    return (score ^ state) & 1, requests


def main():
    rng = random.Random(610948)
    assertions = 0
    trials = 180
    child_checks = 0
    virtual_reads = 0

    for _ in range(trials):
        parent_length = 1 << rng.randint(7, 11)
        parent = [rng.getrandbits(1) for _ in range(parent_length)]
        child_length = rng.randint(8, max(8, int(math.sqrt(parent_length) * 3)))
        child_count = rng.randint(1, 80)
        for _child in range(child_count):
            # Odd a makes the affine address stride nondegenerate modulo 2^k.
            descriptor = (rng.randrange(1, parent_length, 2),
                          rng.randrange(parent_length), rng.randrange(256))
            explicit = materialize(parent, descriptor, child_length)
            virtual = VirtualChild(parent, descriptor, child_length)
            explicit_answer, explicit_requests = read_only_procedure(explicit)
            virtual_answer, virtual_requests = read_only_procedure(virtual)
            assert virtual_answer == explicit_answer
            assert virtual_requests == explicit_requests == virtual.reads
            for index in range(child_length):
                assert virtual[index] == explicit[index]
                assertions += 1
            assertions += 2
            child_checks += 1
            virtual_reads += virtual_requests

    # Symbolic ARC recurrence and materialization controls.
    alpha = 0.6       # number of children Q=N^alpha
    lambd = 0.5       # child length L=N^lambda
    generator_time = 1.1
    generator_space = 0.5
    recurrence_rows = []
    for t, s in ((1.0, 1.0), (1.1, 0.8), (1.2, 0.6),
                 (1.203, 0.505), (1.6, 0.4), (2.0, 0.2), (4.0, 0.1)):
        time_prime = max(generator_time, alpha + lambd * t)
        space_prime = max(generator_space, lambd * s)
        assert math.isclose(time_prime, max(1.1, 0.6 + t / 2))
        assert math.isclose(space_prime, max(0.5, s / 2))
        recurrence_rows.append({
            "input_time_exponent_t": t,
            "input_space_exponent_s": s,
            "successor_time_exponent": time_prime,
            "successor_space_exponent": space_prime,
        })
        assertions += 2

    # Physical controls at the target parameters.
    batch_exponent = 0.5
    batch_children_storage = batch_exponent + lambd
    all_output_time = alpha + lambd
    per_child_rescan_time = 1.0 + alpha
    one_child_buffer = lambd
    assert math.isclose(batch_children_storage, 1.0)
    assert math.isclose(all_output_time, 1.1)
    assert math.isclose(per_child_rescan_time, 1.6)
    assert math.isclose(one_child_buffer, 0.5)
    assertions += 4

    result = {
        "status": "FINITE_AUDIT_ONLY_NO_CLASS_SEPARATION",
        "composition_lemma": {
            "hypothesis": "child bit g(x,d,i) computable in polylog(N) time and O(log N) space from read-only parent x",
            "simulation_time": "G + Q*T_A(L)*polylog(N)",
            "simulation_space": "max(H,S_A(L))+O(log N)",
            "target_recurrence": "t'=max(1.1,0.6+t/2), s'=max(0.5,s/2)",
        },
        "finite_virtual_simulation": {
            "trials": trials,
            "children_checked": child_checks,
            "adaptive_virtual_input_reads": virtual_reads,
            "all_answers_equal_materialized_execution": True,
        },
        "recurrence_rows": recurrence_rows,
        "materialization_controls": {
            "B_children_simultaneously": "N^1.0 bits",
            "all_children_write_time": "N^1.1",
            "one_parent_rescan_per_child": "N^1.6 time",
            "one_child_buffer": "N^0.5 bits",
        },
        "open_interfaces": [
            "construct descriptors for every real ARC child on every input",
            "prove local bit indexability and hereditary preservation",
            "charge descriptor generation, validation, failed branches and ancestor state",
            "match the composed simulation to the exact FLMV machine conventions",
            "do not infer MKTP HIGH from a locally indexable target",
        ],
        "assertions": assertions,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
