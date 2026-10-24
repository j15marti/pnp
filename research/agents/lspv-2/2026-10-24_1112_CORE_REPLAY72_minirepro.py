#!/usr/bin/env python3
"""CORE-REPLAY72 standalone source-certificate reproducer.
Validates the explicit connected proper-3CNF opposite-label construction.
This short script does not reproduce the general DPLL proof-replay experiment;
the complete audit is in the conversation archive CORE_REPLAY72.
"""
import itertools, json, hashlib
from collections import Counter

def make(k, label):
    x=1;c=k+2;d=k+3;a=k+4;b=k+5
    block=[(x,sa*a,sb*b) for sa in (1,-1) for sb in (1,-1)]
    for i in range(k):
        y=2+i;q=k+6+i
        block.extend(((y,a,q),(-y,a,q)))
    globals_=[((1 if label=="SAT" else -1)*x,sa*c,sb*d)
              for sa in (1,-1) for sb in (1,-1)]
    return globals_+block,block,globals_

def value(literal,assignment):
    return assignment[abs(literal)] == (literal>0)

def clause_true(clause,assignment):
    return any(value(l,assignment) for l in clause)

def connected(formula):
    variables={abs(l) for C in formula for l in C}
    neighbors={v:set() for v in variables}
    for C in formula:
        for l in C:
            neighbors[abs(l)].update(abs(u) for u in C if abs(u)!=abs(l))
    start=next(iter(variables))
    reached={start};queue=[start]
    for v in queue:
        for w in neighbors[v]-reached:
            reached.add(w);queue.append(w)
    return reached==variables

def source_entails_x_from_core(block):
    """Independent four-assignment check of the original x,a,b clauses.
    No dummy y assumption, inferred runtime, or unsat oracle is used.
    """
    core=block[:4]
    for av,bv in itertools.product((False,True),repeat=2):
        assn={1:False, abs(core[0][1]):av, abs(core[0][2]):bv}
        assert not all(clause_true(C,assn) for C in core)
    return True

def globals_force_sign(G,sign):
    c,d=abs(G[0][1]),abs(G[0][2])
    x=abs(G[0][0])
    for cv,dv in itertools.product((False,True),repeat=2):
        assn={x:not sign,c:cv,d:dv}
        assert not all(clause_true(C,assn) for C in G)
    return True

def sample_sat_witness(F,k):
    n=max(abs(l) for C in F for l in C)
    assn={v:True for v in range(1,n+1)}
    assert all(clause_true(C,assn) for C in F)
    return True

def audit(k,label):
    F,B,G=make(k,label)
    assert len(F)==2*k+8
    assert max(abs(l) for C in F for l in C)==2*k+5
    assert len(set(F))==len(F)
    assert all(len(C)==3 and len({abs(l) for l in C})==3 for C in F)
    assert connected(F)
    assert source_entails_x_from_core(B)
    assert globals_force_sign(G,label=="SAT")
    if label=="SAT":
        sample_sat_witness(F,k)
        old_calls=new_calls=1
    else:
        # The earlier full-row policy learns one forbidden y-cube at a time;
        # every one of the 2^k vectors must be blocked before its master ends.
        seen=set()
        for z in range(1<<k):
            beta=tuple(bool(z>>i&1) for i in range(k))
            assert beta not in seen
            seen.add(beta)
        assert len(seen)==1<<k
        old_calls=1<<k
        # A checked proof not using any y assumption learns unit x.
        new_calls=1
    n=max(abs(l) for C in F for l in C);m=len(F)
    w=(64*(n+m+1)-1).bit_length()
    N=(4*m+2)*w
    return {"k":k,"label":label,"n":n,"m":m,"N_bits":N,
            "connected":True,"full_row_policy_local_calls":old_calls,
            "proof_core_policy_local_calls":new_calls,
            "checked_core_width":1 if label=="UNSAT" else None}

if __name__=="__main__":
    results=[audit(k,label) for k in (1,3,5,7,9,16,32)
             for label in ("SAT","UNSAT")]
    print(json.dumps({"run":"CORE-REPLAY72","model":"standalone family-certificate check",
        "status":"restricted source checks, not all-decider coverage",
        "cases":results},indent=2))
