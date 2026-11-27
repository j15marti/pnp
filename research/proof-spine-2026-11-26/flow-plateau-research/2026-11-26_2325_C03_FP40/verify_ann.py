"""Replay FP40 original-edge moment certificates. Standard library only.
python verify_ann.py ann_certificates.json.gz.b64
The finite exhaustive matching reference is not a production-time claim.
"""
import itertools as it, json, sys, gzip, base64
from collections import Counter

def plus(a,b):
    a1,a2=a; b1,b2=b
    return ((a1&~(b1|b2))|(b1&~(a1|a2))|(a2&b2),(a2&~(b1|b2))|(b2&~(a1|a2))|(a1&b1))
def packed(terms):
    a=(0,0)
    for j,c in terms:
        c%=3
        if c:a=plus(a,(1<<j,0) if c==1 else (0,1<<j))
    return a
def add(B,a,D,stats):
    while a[0]|a[1]:
        j=((a[0]|a[1])&-(a[0]|a[1])).bit_length()-1
        stats["pivot_checks"]+=1
        if j==D:return False
        if a[1]>>j&1:a=a[::-1]
        if j not in B:B[j]=a;return True
        a=plus(a,B[j][::-1])
    return True
def check(rec):
    stats=Counter()
    E=rec["edges"];m=len(E);n=1+max(max(e) for e in E)
    inc=[[i for i,e in enumerate(E) if v in e] for v in range(n)]
    assert all(len(x)==3 for x in inc) and len({tuple(sorted(e)) for e in E})==m and all(a!=b for a,b in E)
    ix={p:i for i,p in enumerate(it.combinations_with_replacement(range(m),2))};D=len(ix)
    def idx(a,b):return ix[tuple(sorted((a,b)))]
    def equation(terms,rhs=0):return packed(list(terms)+[(D,-rhs)])
    B={}
    for v in range(n):
        for j in range(m):assert add(B,equation([(idx(e,j),1) for e in inc[v]]),D,stats)
    for j in range(m):assert add(B,equation([(idx(0,j),1)]),D,stats)
    Ms=[]
    def enum(U,chosen):
        stats["reference_states"]+=1
        if stats["reference_states"]>2_000_000:raise RuntimeError("verification cap")
        if not U:Ms.append(frozenset(chosen));return
        u=min(U)
        for e in inc[u]:
            a,b=E[e];v=b if a==u else a
            if v in U:enum(U-{u,v},chosen+[e])
    enum(set(range(n)),[])
    assert len(Ms)==rec["reference"]["matchings"]
    for M in Ms:
        U=set(range(n));odd=False
        while U:
            s=min(U);todo=[s];seen={s}
            while todo:
                u=todo.pop()
                for e in inc[u]:
                    if e in M:continue
                    a,b=E[e];v=b if a==u else a
                    if v not in seen:seen.add(v);todo.append(v)
            U-=seen;odd|=len(seen)%2==1
        stats["even_complements"]+=int(not odd)
    assert stats["even_complements"]==rec["reference"]["even"]
    bad=False
    for tag,_ in rec["hybrid_ann"]["events"]:
        assert not bad;stats["events"]+=1
        if tag[0]=="vertex":
            a,b=inc[tag[1]][:2];eq=equation([(idx(a,a),1),(idx(b,b),1),(idx(a,b),1)],1)
        elif tag[0] in ("annihilator","bad_square"):
            a,b,sign=tag[1:4];square=[(idx(a,a),1),(idx(b,b),1),(idx(a,b),-2*sign)]
            val=0 if tag[0]=="annihilator" else 2
            for c in range(3):
                if c!=val:assert not add(B.copy(),equation(square,c),D,stats)
            stats["square_checks"]+=1
            if tag[0]=="bad_square":eq=equation([],1)
            else:
                h=tag[4];eq=equation([(idx(a,h),1),(idx(b,h),-sign)])
        else:
            assert tag[0] in ("chart","empty")
            C=tag[1];k=len(C);pairs=list(it.combinations_with_replacement(range(k),2));supp=[set(x) for x in tag[2]]
            for c in range(3):
                actual={sum(1<<i for i,e in enumerate(C) if e in M) for M in Ms if (0 in M)==(c==0)}
                assert actual==supp[c];stats["support_checks"]+=1
            for w in it.product(range(3),repeat=k):
                if not all(sum(1<<i for i,c0 in enumerate(w) if c0==c) in supp[c] for c in range(3)):continue
                vals=[w[a]*w[b]%3 for a,b in pairs];stats["word_checks"]+=1
                Z=B.copy()
                if not all(add(Z,equation([(idx(C[a],C[b]),1)],v),D,stats) for (a,b),v in zip(pairs,vals)):continue
                assert tag[0]!="empty"
                h=tag[3];assert (sum(c*v for c,v in zip(h,vals))+h[-1])%3==0
            if tag[0]=="empty":eq=equation([],1)
            else:
                h=tag[3];eq=equation([(idx(C[a],C[b]),c) for (a,b),c in zip(pairs,h)],-h[-1])
        bad=not add(B,eq,D,stats)
    assert bad==(rec["hybrid_ann"]["status"]=="NO")
    return {"name":rec["name"],"verified_NO":bad,"stats":dict(stats)}
if __name__=="__main__":
    with open(sys.argv[1] if len(sys.argv)>1 else "ann_certificates.json.gz.b64","rb") as f:
        records=json.loads(gzip.decompress(base64.b64decode(f.read())))
    for rec in records:print(json.dumps(check(rec),sort_keys=True))
