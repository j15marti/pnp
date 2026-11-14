#!/usr/bin/env python3
"""Independent exact verifier using bit-parallel enumeration of ALL 8! UNSAT permutations.
Not a physical Turing-machine simulation; certificate assertions are finite.
"""
import itertools, json, sys
base=(1,2,3,4,5,6,7,7)
perms=list(itertools.permutations(range(8)))
assert len(perms)==40320
allbits=(1<<len(perms))-1
colbits=[0]*24
for k,p in enumerate(perms):
    bit=1<<k
    for pos in range(24):
        row,b=divmod(pos,3)
        if ((p[row]>>b)&1)==((base[row]>>b)&1):colbits[pos]|=bit
counts={}
for k in range(6):
    total=certs=0
    for subset in itertools.combinations(range(24),k):
        intersection=allbits
        for pos in subset:intersection&=colbits[pos]
        total+=1
        if intersection==0:certs+=1
    counts[str(k)]={'subsets':total,'SAT_certificates':certs,'UNSAT_completion_exists':total-certs}
assert all(counts[str(k)]['SAT_certificates']==0 for k in range(5))
assert counts['5']['SAT_certificates']==3
assert all(len(set(tuple(v^(1<<b) if i==row else v for i,v in enumerate(range(8)))))==7 for row in range(8) for b in range(3))
print(json.dumps({'tag':'TMR2-CERT011-INDEPENDENT-40320-PERMUTATIONS','python':sys.version.split()[0],'permutations':len(perms),'counts':counts,'unsat_single_sign_flips':24,'failures':0},indent=2))
