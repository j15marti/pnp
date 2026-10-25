#!/usr/bin/env python3
"""ARC-IMAGE-PROMISE-BRIDGE160 finite guarded-Horn promise counterexample.
NOT the FLMV tableau reduction or a matched random-access Turing-machine trace.
"""
import itertools, json
from pathlib import Path

GUARDS=((10,-10),(11,-11))
CANDIDATES=((1,),(-1,),(2,),(-2,),(-1,-2),(-1,2),(-2,1))

def brute_sat(clauses):
    names=sorted({abs(x) for clause in clauses for x in clause})
    for bits in itertools.product((False,True),repeat=len(names)):
        assign=dict(zip(names,bits))
        if all(any(assign[abs(x)] if x>0 else not assign[-x] for x in c) for c in clauses):
            return True
    return False

def horn_sat(clauses):
    if any(sum(x>0 for x in c)>1 for c in clauses):
        raise ValueError("not Horn")
    true=set()
    while True:
        change=False
        for clause in clauses:
            neg={-x for x in clause if x<0}
            pos=[x for x in clause if x>0]
            if neg.issubset(true):
                if not pos:
                    return False
                if pos[0] not in true:
                    true.add(pos[0]);change=True
        if not change:
            return True

def is_promise(formula):
    return len(formula)>=2 and tuple(formula[:2])==GUARDS and all(
       len(set(abs(x) for x in c))==len(c)
       and sum(x>0 for x in c)<=1
       and all(abs(x) in (1,2) for x in c)
       for c in formula[2:])

def promise_B(formula):
    """Total algorithm: exact on guarded Horn promise; arbitrary outside."""
    return horn_sat(formula[2:]) if is_promise(formula) else True

def encoded_bits(formula):
    mx=max((abs(x) for c in formula for x in c),default=0)
    b=("p cnf %d %d\n"%(mx,len(formula)))+"".join(" ".join(map(str,c))+" 0\n" for c in formula)
    return len(b.encode("utf-8"))*8

def run():
    assertions=0
    cores=0;yes=0;no=0;illegal_first=0;illegal_second=0
    wrong_first=0;wrong_second=0
    emitted_first=0;emitted_second=0
    examples=[]
    for flags in itertools.product((False,True),repeat=len(CANDIDATES)):
        core=tuple(c for c,flag in zip(CANDIDATES,flags) if flag)
        truth=brute_sat(core)
        assert truth==horn_sat(core); assertions+=1
        f0=GUARDS+core
        f1=f0[1:]; f2=f1[1:]
        assert is_promise(f0); assertions+=1
        assert not is_promise(f1) and not is_promise(f2); assertions+=1
        assert brute_sat(f0)==brute_sat(f1)==brute_sat(f2)==truth; assertions+=1
        assert promise_B(f0)==truth; assertions+=1
        b1,b2=promise_B(f1),promise_B(f2)
        illegal_first+=not is_promise(f1);illegal_second+=not is_promise(f2)
        wrong_first+=(b1!=truth);wrong_second+=(b2!=truth)
        emitted_first+=encoded_bits(f1)
        emitted_second+=encoded_bits(f2)
        cores+=1;yes+=truth;no+=not truth
        if not truth and len(examples)<3:
            examples.append({"core":core,"actual_label":"UNSAT",
                             "B_on_parent":promise_B(f0),
                             "B_on_child1":b1,"B_on_child2":b2,
                             "bit_lengths":[encoded_bits(f0),encoded_bits(f1),encoded_bits(f2)]})
    assert cores==128 and yes+no==128;assertions+=1
    assert wrong_first==no and wrong_second==no;assertions+=1
    return {
      "identifier":"ARC-IMAGE-PROMISE-BRIDGE160",
      "status":"COMPUTATIONAL only; structural counterexample has a separate symbolic proof",
      "test":"All subsets of seven Horn clauses on two variables, two real guard-deletion levels",
      "core_count":cores,"SAT":yes,"UNSAT":no,
      "correct_on_promise":cores,
      "off_promise_calls_at_level_1":illegal_first,
      "off_promise_calls_at_level_2":illegal_second,
      "false_SAT_returns_on_UNSAT_level_1":wrong_first,
      "false_SAT_returns_on_UNSAT_level_2":wrong_second,
      "assertions":assertions,
      "serialized_child1_bits_total":emitted_first,
      "serialized_child2_bits_total":emitted_second,
      "examples":examples,
      "limitations":"No FLMV tableau compiler implemented. Not a TM bit-work/peak-space trace. Validates only the two-level typed-promise guard."
    }

if __name__=="__main__":
    res=run()
    p=Path(__file__).with_name("2026-10-25_0127_ARC_IMAGE_PROMISE_BRIDGE160_results.json")
    p.write_text(json.dumps(res,indent=2,default=list)+"\n")
    print(json.dumps({k:v for k,v in res.items() if k!="examples"},indent=2))
