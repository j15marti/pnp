#!/usr/bin/env python3
"""Finite audit of explicit SAT-sample lookup circuits, LSPV-1/407."""
import itertools, json, random
from pathlib import Path
SEED=202611041935
def compile_lookup(n, labeled):
    if type(n) is not int or n<1: raise ValueError("width")
    if len(labeled)!=len(set(labeled)): raise ValueError("duplicates")
    for x,y in labeled.items():
        if len(x)!=n or len(y)!=n or set(x+y)-{"0","1"}: raise ValueError("sample")
    gates=[]
    def add(op,a,b=None):
        gates.append((op,a,b))
        return n+1+len(gates)
    negatives=[add("NOT",j) for j in range(n)] if labeled else []
    selectors={}
    for x in sorted(labeled):
        literals=[j if bit=="1" else negatives[j] for j,bit in enumerate(x)]
        v=literals[0]
        for a in literals[1:]: v=add("AND",v,a)
        selectors[x]=v
    outputs=[]
    for j in range(n):
        selected=[selectors[x] for x in sorted(labeled) if labeled[x][j]=="1"]
        if not selected: outputs.append(n)
        else:
            v=selected[0]
            for a in selected[1:]: v=add("OR",v,a)
            outputs.append(v)
    return gates,outputs
def run(n,gates,outputs,bits):
    wires=[int(b) for b in bits]+[0,1]
    for op,a,b in gates:
        if a>=len(wires) or (b is not None and b>=len(wires)): raise ValueError("forward reference")
        if op=="NOT" and b is None: wires.append(1-wires[a])
        elif op=="AND" and b is not None: wires.append(wires[a]&wires[b])
        elif op=="OR" and b is not None: wires.append(wires[a]|wires[b])
        else: raise ValueError("gate")
    if any(o>=len(wires) for o in outputs): raise ValueError("output")
    return "".join(str(wires[o]) for o in outputs)
def check(n,labeled):
    gates,outputs=compile_lookup(n,labeled)
    m=len(labeled)
    count=2
    assert len(gates)<=(2*n-1)*m
    exact=n+m*(n-1)+sum(max(0,sum(y[j]=="1" for y in labeled.values())-1) for j in range(n)) if m else 0
    assert len(gates)==exact
    for x,y in labeled.items():
        assert run(n,gates,outputs,x)==y
        count+=1
    if n<=4:
        for mask in range(2**n):
            x=format(mask,f"0{n}b")
            if x in labeled:
                assert run(n,gates,outputs,x)==labeled[x]
                count+=1
    return count,len(gates)
def main():
    tests=checks=peak=0
    universe=[format(i,"02b") for i in range(4)]
    for choices in itertools.product(range(5),repeat=4):
        labeled={universe[i]:universe[c-1] for i,c in enumerate(choices) if c}
        a,g=check(2,labeled)
        checks+=a;tests+=1;peak=max(peak,g)
    rng=random.Random(SEED)
    for n in range(1,9):
        for _ in range(64):
            keys=rng.sample(range(2**n),rng.randrange(min(2**n,12)+1))
            labeled={format(k,f"0{n}b"):format(rng.randrange(2**n),f"0{n}b") for k in keys}
            a,g=check(n,labeled)
            checks+=a;tests+=1;peak=max(peak,g)
    malformed=0
    for n,bad in [(0,{}),(2,{"0":"00"}),(2,{"00":"0"}),(2,{"00":"0z"}),(2,{"xx":"00"}),(-1,{})]:
        try: compile_lookup(n,bad)
        except ValueError: malformed+=1
    assert malformed==6
    checks+=6
    try: run(2,[("AND",2,99)],[4],"00")
    except ValueError: checks+=1
    else: raise AssertionError("forged forward gate")
    def models(clauses,n):
        return sum(all(any(((mask>>(n-abs(lit)))&1)==(lit>0) for lit in clause) for clause in clauses) for mask in range(2**n))
    assert (models([[1]],1),models([[1],[-1]],1),models([[1,-1]],1))==(1,0,2)
    checks+=3
    raw={"result":"LSPV-1/407 finite lookup controls","seed":SEED,"n2_exhaustive_partial_functions":625,"random_cases":512,
         "tests":tests,"assertions":checks,"max_gate_count":peak,"malformed_rejections":malformed,
         "label_controls":{"SAT_unit_models":1,"UNSAT_contradictory_units_models":0,"SAT_tautology_models":2},
         "bound":"G<=m(2n-1), antichecker requires m>size_bound/(2n-1)",
         "status":"Restricted elementary theorem; AC_k, B3, P-vs-NP OPEN"}
    Path("lspv1_407_antichecker_lookup_raw.json").write_text(json.dumps(raw,indent=2)+"\n")
    print(json.dumps(raw,indent=2))
if __name__=="__main__": main()
