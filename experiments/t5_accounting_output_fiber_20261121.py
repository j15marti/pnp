"""Finite source-fiber and charged cleanup audit. No TM claim for Python counter."""
from collections import Counter
from hashlib import sha256
from math import comb, log2
from pathlib import Path
import json
import t5_construction_disjoint_cut_20261121 as family
import t5_construction_disj_orbit_width_20261121 as solver

def cleanup(output, scratch):
    # A one-head cleanup suffix with explicit positions and read/write moves.
    tape = list(output + "#" + scratch)
    head = len(tape)-1
    steps = 0
    cm_reserved = 0
    boundary = len(output)
    while head > boundary:
        tape[head] = "_"
        head -= 1
        steps += 1
        cm_reserved += len(tape)
    while head:
        head -= 1
        steps += 1
        cm_reserved += len(tape)
    return "".join(tape), head, steps, cm_reserved

def main():
    groups = []
    for k in (2,3):
        weight = k//2
        members = []
        configurations = []
        for b in range(1 << k):
            if b.bit_count() != weight:
                continue
            a = ((1 << k)-1)^b
            encoded = family.image(k,a,b)[0]
            count, detail = solver.evaluate(encoded)
            expected = 10 << (98+282*k+k-weight)
            assert count == expected
            state, head, steps, cm = cleanup(bin(count)[2:], encoded)
            configurations.append((state,head))
            members.append(dict(a=a,b=b,N=len(encoded),count=str(count),
                                input_sha256=sha256(encoded.encode()).hexdigest(),
                                checkpoint_sha256=sha256(state.encode()).hexdigest(),
                                cleanup_steps=steps,cleanup_CM_reserved=cm))
        assert len(set(configurations)) == 1
        assert len(members) == comb(k,weight)
        groups.append(dict(k=k,members=members,
                           exact_decoder_success=f"1/{len(members)}",
                           source_entropy_bits=log2(len(members)),
                           future_information_bits=0,
                           residual_entropy_bits=log2(len(members))))
    # Same length, opposite labels cannot have the same normalized output state.
    controls = []
    for a,b in ((0,0),(3,1)):
        encoded=family.image(2,a,b)[0]
        count,detail=solver.evaluate(encoded)
        state,head,steps,cm=cleanup(bin(count)[2:],encoded)
        controls.append(dict(a=a,b=b,label=detail["status"],count=str(count),
                             checkpoint_sha256=sha256(state.encode()).hexdigest()))
    assert controls[0]["label"]=="SAT" and controls[1]["label"]=="UNSAT"
    assert controls[0]["checkpoint_sha256"] != controls[1]["checkpoint_sha256"]
    return dict(lemma="T5-OUTPUT-FIBER-LOSS1",groups=groups,controls=controls,
                scope="Explicit cleanup suffix and exact orbit counts; no timing claim for Python.",
                dependencies={Path(m.__file__).name:sha256(Path(m.__file__).read_bytes()).hexdigest()
                              for m in (family,solver,solver.wrapper,solver.c,family.balanced)})
if __name__=="__main__":
    print(json.dumps(main(),indent=2))
