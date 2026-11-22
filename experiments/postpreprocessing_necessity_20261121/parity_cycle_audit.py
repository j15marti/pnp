import itertools,json,time
start=time.monotonic()
counts={'r_values':list(range(3,8)),'formulas':0,'assignments':0,'unsat_formulas':0,'clause_criticality_checks':0,'single_flip_checks':0,'adjacent_near_witness_pairs':0}
def formula(b):
    r=len(b); p=r+1; out=[]
    for i,bi in enumerate(b):
        x=i+1; y=(i+1)%r+1
        bases=[(x,y),(-x,-y)] if bi else [(-x,y),(x,-y)]
        for c in bases:
            out.extend([c+(p,),c+(-p,)])
    return out

def gamma(x):
    s=bin(x)[2:];return '0'*(len(s)-1)+s

def encode(b):
    r=len(b);w=(r+1).bit_length()
    return gamma(r+2)+gamma(4*r+1)+''.join(('1' if x<0 else '0')+format(abs(x),f'0{w}b') for c in formula(b) for x in c)
for r in range(3,8):
    for b in itertools.product(range(2),repeat=r):
        F=formula(b);models=0;seen=set();near={};counts['formulas']+=1
        for a in itertools.product(range(2),repeat=r+1):
            counts['assignments']+=1
            bad=[j for j,c in enumerate(F) if not any(bool(a[abs(x)-1]) == (x>0) for x in c)]
            if not bad:models+=1
            if len(bad)==1:seen.add(bad[0]);near[a]=bad[0]
        parity=sum(b)%2
        assert models==(0 if parity else 4)
        if parity:
            counts['unsat_formulas']+=1
            assert seen==set(range(4*r));counts['clause_criticality_checks']+=4*r
            for a,j in near.items():
                aa=a[:-1]+(1-a[-1],)
                assert aa in near and near[aa]//4==j//4 and near[aa]!=j
                counts['adjacent_near_witness_pairs']+=1
        e=encode(b);w=(r+1).bit_length()
        expected=2*((r+2).bit_length()-1)+2*((4*r+1).bit_length()-1)+2+12*r*(w+1)
        assert len(e)==expected
        supports=[]
        for i in range(r):
            bb=list(b);bb[i]^=1;ee=encode(bb)
            support={j for j,(u,v) in enumerate(zip(e,ee)) if u!=v}
            assert len(support)==4
            assert all(support.isdisjoint(s) for s in supports)
            supports.append(support);counts['single_flip_checks']+=1
print(json.dumps({'status':'PASS','counts':counts,'elapsed_seconds':time.monotonic()-start,'scope':'Exhaustive finite formula semantics, one-clause witness coverage, p-adjacency, and encoded flip support for r=3..7 only. No runtime lower-bound or asymptotic verification.'},indent=2))
