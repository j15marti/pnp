#!/usr/bin/env python3
import itertools, json

K=3
d=m=2
X=list(itertools.product(range(m), repeat=K))
Y=list(itertools.product(range(d), repeat=K*m))
OUT=list(itertools.combinations(range(K),2))

SX={(0,0,1),(0,1,0),(1,0,0),(1,1,1)}
SY={
    (0,0,0,1,1,1),
    (0,0,1,0,1,1),
    (0,0,1,1,0,1),
    (1,0,0,0,1,1),
    (1,0,1,1,0,0),
    (1,1,0,0,0,1),
}

def valid(x,y,o):
    p,q=o
    return y[p*m+x[p]] == y[q*m+x[q]]

assert all(any(valid(x,y,o) for o in OUT) for x in X for y in Y)

checks=max_lhs=equality_cases=0
summary={}
for o in OUT:
    per_size={}
    for mask in range(1,1<<len(X)):
        L=[X[i] for i in range(len(X)) if (mask>>i)&1]
        R=[y for y in Y if all(valid(x,y,o) for x in L)]
        if not R:
            continue
        a=sum(x in SX for x in L)
        b=sum(y in SY for y in R)
        lhs=2*a+3*b
        checks+=1
        max_lhs=max(max_lhs,lhs)
        equality_cases += lhs==8
        assert lhs<=8
        p,q=o
        P={(x[p],x[q]) for x in L}
        key=len(P)
        per_size.setdefault(key,{'max_SY':0,'max_SX':0,'max_lhs':0})
        per_size[key]['max_SY']=max(per_size[key]['max_SY'],b)
        per_size[key]['max_SX']=max(per_size[key]['max_SX'],a)
        per_size[key]['max_lhs']=max(per_size[key]['max_lhs'],lhs)
    summary[str(o)]=per_size

x=(0,0,0)
y=(0,0, 0,1, 1,0)
V=[(s,p) for p in range(K) for s in range(m)]
EA={tuple(sorted(((x[p],p),(x[q],q)))) for p,q in OUT}
def color(v):
    s,p=v
    return y[p*m+s]
EB={tuple(sorted((u,v))) for i,u in enumerate(V) for v in V[i+1:] if color(u)!=color(v)}
AminusB=EA-EB
BminusA=EB-EA
assert AminusB and BminusA
for e in AminusB:
    (_,p),(_,q)=e
    assert valid(x,y,tuple(sorted((p,q))))

result={
    'status':'PASS',
    'relation':{'X':len(X),'Y':len(Y),'outputs':len(OUT),'pairs':len(X)*len(Y)},
    'rectangle_dual_certificate':{
        'SX':sorted(SX),
        'SY':sorted(SY),
        'rectangles_maximal_R_checked':checks,
        'max_lhs_2SX_plus_3SY':max_lhs,
        'equality_cases':equality_cases,
        'projection_summary':summary,
        'consequence':'Summing the rectangle inequality over exact-slice coordinates forces t>=U, hence t=U and no KW output.'
    },
    'graph_hostile_pair':{
        'x':x,'y':y,
        'alice_edges':len(EA),'bob_edges':len(EB),
        'A_minus_B':sorted(map(str,AminusB)),
        'B_minus_A_count':len(BminusA)
    }
}
print(json.dumps(result,indent=2,sort_keys=True))
