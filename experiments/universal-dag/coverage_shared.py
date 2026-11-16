#!/usr/bin/env python3
"""Build and structurally verify a shared AND/OR/NOT SAT circuit for n=3..6."""
import json
import sys
from itertools import combinations
from pathlib import Path

n=int(sys.argv[1]);prefix=Path(sys.argv[2]);assert 3<=n<=6
clauses=[(vs,s) for vs in combinations(range(n),3) for s in range(8)]
C=len(clauses);gates=[];unique={};depth=[0]*C
def gate(op,a,b):
    if op!='N' and a>b:a,b=b,a
    key=(op,a,b)
    if key in unique:return unique[key]
    id=C+len(gates);unique[key]=id;gates.append(key);depth.append(1+max(depth[a],depth[b]));return id
def reduce(op,ids):
    while len(ids)>1:
        ids=[gate(op,ids[i],ids[i+1]) if i+1<len(ids) else ids[i] for i in range(0,len(ids),2)]
    return ids[0]
targets=[];covers=[]
for a in range(1<<n):
    incident=[q for q,(vs,s) in enumerate(clauses)
              if all(((a>>v)&1)==((s>>j)&1) for j,v in enumerate(vs))]
    targets.append(set(incident));covers.append(reduce('O',incident))
unsat=reduce('A',covers);output=gate('N',unsat,unsat)

# Independently reconstruct every OR support and the final AND coverage set.
def or_support(id):
    if id<C:return {id}
    op,a,b=gates[id-C];assert op=='O'
    return or_support(a)|or_support(b)
for a,id in enumerate(covers):
    assert or_support(id)==targets[a]
def and_leaves(id):
    if id in covers:return {id}
    op,a,b=gates[id-C];assert op=='A'
    return and_leaves(a)|and_leaves(b)
assert and_leaves(unsat)==set(covers)
assert gates[output-C]==('N',unsat,unsat)
seen=set()
def visit(id):
    if id<C or id in seen:return
    seen.add(id);_,a,b=gates[id-C];visit(a);visit(b)
visit(output)
assert len(seen)==len(gates)
with Path(str(prefix)+'.circuit').open('w') as f:
    f.write(f'{C} {len(gates)} {output}\n')
    for i,(op,a,b) in enumerate(gates,C):f.write(f'{i} {op} {a} {b}\n')
result=dict(n=n,inputs=C,gates=len(gates),depth=depth[output],
            AND=sum(g[0]=='A' for g in gates),OR=sum(g[0]=='O' for g in gates),NOT=1,
            verification='PASS: all vertex OR supports and final AND/NOT structure',
            valid_for_all_clause_counts=True,minimum_proved=False)
Path(str(prefix)+'_circuit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
