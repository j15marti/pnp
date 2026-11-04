#!/usr/bin/env python3
"""Independent Horn UP + direct valuation and strict signed-RES audit, LSPV-1/383."""
import json

def clauses(k):
    out = [(1,), (-(k+1),)]
    for i in range(1,k+1):
        a, b = k+1+i, 2*k+1+i
        out.extend([(-i,a),(-a,i+1),(-i,b),(-b,i+1)])
    return out

def unsat_via_horn(k, mask):
    c=clauses(k)
    active=[c[i] for i in range(len(c)) if (mask>>i)&1]
    true={r[0] for r in active if len(r)==1 and r[0]>0}
    forbidden={-r[0] for r in active if len(r)==1 and r[0]<0}
    while True:
        new=set(true)
        for r in active:
            if len(r)==2 and r[0]<0 and r[1]>0 and -r[0] in true: new.add(r[1])
        if new==true: break
        true=new
    return bool(true & forbidden)

def brute_satisfiable(k, mask):
    C=clauses(k)
    for assignment in range(1<<(3*k+1)):
        if all(any((((assignment>>(abs(lit)-1))&1)==1) if lit>0 else (((assignment>>(abs(lit)-1))&1)==0) for lit in C[j]) for j in range(len(C)) if mask>>j&1):
            return True
    return False

def resolve(a,b,pivot):
    sa,sb=set(a),set(b)
    if pivot in sa and -pivot in sb: return tuple(sorted((sa-{pivot}) | (sb-{-pivot})))
    if -pivot in sa and pivot in sb: return tuple(sorted((sa-{-pivot}) | (sb-{pivot})))
    raise ValueError('bad RES pivot')

def proof_for(k):
    proof=[]; root=0
    for i in range(1,k+1):
        a=k+1+i; src=2+4*(i-1)
        proof.append((root,src,i,(a,)))
        idx1=len(clauses(k))+len(proof)-1
        proof.append((idx1,src+1,a,(i+1,)))
        root=len(clauses(k))+len(proof)-1
    proof.append((root,1,k+1,()))
    return proof

def replay(c,proof):
    seen=list(c)
    for u,v,p,claimed in proof:
        if not (0<=u<len(seen) and 0<=v<len(seen)): return False
        try:actual=resolve(seen[u],seen[v],p)
        except ValueError: return False
        if actual!=tuple(sorted(claimed)) or any(-x in actual for x in actual):return False
        seen.append(actual)
    return len(proof)>0 and seen[-1]==()

out={'checker':'independent Horn UP; direct valuation k<=2; strict signed RES',
     'random_seed':None,'instances':[],'assertions':0,'corrupt_rejected':0}
for k in range(1,4):
    n=1<<(4*k+2); sat=unsat=mus=0
    for mask in range(n):
        u=unsat_via_horn(k,mask);out['assertions']+=1
        if k<=2:
            assert u != brute_satisfiable(k,mask),(k,mask);out['assertions']+=1
        if u:
            unsat+=1
            if all(not unsat_via_horn(k, mask^(1<<i)) for i in range(4*k+2) if mask>>i&1):
                mus+=1
        else:sat+=1
    assert unsat==7**k and mus==2**k;out['assertions']+=2
    out['instances'].append({'k':k,'sat':sat,'unsat':unsat,'mus':mus})
for k in [4,5,6]:
    for mask in range(0,1<<(4*k+2),max(1,(1<<(4*k+2))//1024)):
        t=bool((mask&3)==3 and all(
            (((mask>>(2+4*(i-1)))&3)==3 or ((mask>>(4+4*(i-1)))&3)==3)
            for i in range(1,k+1)))
        assert unsat_via_horn(k,mask)==t;out['assertions']+=1
for k in range(1,5):
    C=clauses(k); cert=proof_for(k)
    assert len(cert)==2*k+1 and replay(C,cert)
    out['assertions']+=2
    damaged=[cert[:-1],[(99,)+cert[0][1:]]+cert[1:],
             [(cert[0][0],cert[0][1],999,cert[0][3])]+cert[1:],
             [(cert[0][0],cert[0][1],cert[0][2],())]+cert[1:]]
    for p in damaged:
        assert not replay(C,p)
        out['corrupt_rejected']+=1;out['assertions']+=1
    changed=C.copy();changed[0]=(-1,)
    assert not replay(changed,cert)
    out['corrupt_rejected']+=1;out['assertions']+=1
assert out['assertions']==21666
assert out['corrupt_rejected']==20
print(json.dumps(out,indent=2))
