#!/usr/bin/env python3
"""Deterministic signed universal-reflection three-variable toy producer.
No packages. The general B3 implication and mixed rule-transport are OPEN.
"""
import itertools, hashlib, json
C=((1,2),(-1,-2),(3,1),(-3,-1),(3,2),(-3,-2))
def sat(cs,a):
    return all(any(a[abs(l)-1]==(l>0) for l in c) for c in cs)
def models(cs):
    return [a for a in itertools.product((False,True),repeat=3) if sat(cs,a)]
def parity(m,b,a):
    return (sum(a[i] for i in range(3) if m&(1<<i))%2)==b
def main():
    assert not models(C)
    proof=[
        {"id":6,"rule":"AND3","parents":[0,1],"mask":3,"rhs":1},
        {"id":7,"rule":"AND3","parents":[2,3],"mask":5,"rhs":1},
        {"id":8,"rule":"AND3","parents":[4,5],"mask":6,"rhs":1},
        {"id":9,"rule":"XOR","parents":[6,7],"mask":6,"rhs":0},
        {"id":10,"rule":"XOR","parents":[9,8],"mask":0,"rhs":1}]
    for a,b,mask,rhs in ((0,1,3,1),(2,3,5,1),(4,5,6,1)):
        for v in itertools.product((False,True),repeat=3):
            assert sat((C[a],C[b]),v)==parity(mask,rhs,v)
    assert (3^5^6,1^1^1)==(0,1)
    deletion=[]
    for i in range(6):
        w=models(C[:i]+C[i+1:]);assert len(w)==1
        deletion.append({"deleted_clause":i+1,"witness_bits":[int(x) for x in w[0]]})
    flips=[]
    for i,c in enumerate(C):
        for j in (0,1):
            z=[list(x) for x in C];z[i][j]*=-1
            count=len(models(z));assert count
            flips.append({"clause":i+1,"literal":j+1,"models":count})
    both=[{"signs":[a,b],"label":"SAT" if a==b else "UNSAT",
           "models":sum(x!=a and x!=b for x in (0,1))}
          for a,b in itertools.product((0,1),repeat=2)]
    s="p cnf 3 6\n"+"".join(" ".join(map(str,c))+" 0\n" for c in C)
    out={"clauses":C,"dimacs":s,"sha256":hashlib.sha256(s.encode()).hexdigest(),
         "min_paid_mixed_nodes":5,"proof":proof,"deletion_witnesses":deletion,
         "one_occurrence_sign_flips":flips,"both_labels":both,
         "scope":"exact three-variable toy; RT/SC and B3 open"}
    print(json.dumps(out,indent=2))
if __name__=="__main__":main()
