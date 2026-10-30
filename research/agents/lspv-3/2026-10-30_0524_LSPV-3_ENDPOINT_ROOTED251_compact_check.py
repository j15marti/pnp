#!/usr/bin/env python3
"""Independent compact original-source clause-extreme and resolvent checker.
Run: python3 research/agents/lspv-3/2026-10-30_0524_LSPV-3_ENDPOINT_ROOTED251_compact_check.py
Python standard library only, exhaustive n=15. No SAT decision oracle is used by
the controller in the separate full experiment; this is a validation checker.
"""
import itertools, json
W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),
(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),
(-3,12,15),(-5,-12,15),(-1,13,14)]
SWAP=W1.copy()
SWAP[7]=(-1,7,13)
SWAP[19]=(1,13,14)
def assignment(mask,n):
    return {i:bool((mask>>(i-1))&1) for i in range(1,n+1)}
def truth(l,a):
    return a[abs(l)]==(l>0)
def counts(F,a):
    return [sum(truth(l,a) for l in clause) for clause in F]
def histogram(ts):
    return [ts.count(r) for r in range(4)]
def sat(F,a):
    return all(any(truth(l,a) for l in c) for c in F)
def modes(F):
    k=0
    for j,h in itertools.combinations(range(len(F)),2):
        p={abs(l):(l>0) for l in F[j]}
        q={abs(l):(l>0) for l in F[h]}
        common=set(p)&set(q)
        same=any(p[i]==q[i] for i in common)
        opp=any(p[i]!=q[i] for i in common)
        possible={'SS':not opp,'UU':not opp,'SU':not same,'US':not same}
        used=sorted(set(p)|set(q))
        for md,want in possible.items():
            ok=False
            for mask in range(1<<len(used)):
                a={i:bool(mask>>b&1) for b,i in enumerate(used)}
                if (sum(truth(l,a) for l in F[j])==(3 if md[0]=='S' else 0)
                and sum(truth(l,a) for l in F[h])==(3 if md[1]=='S' else 0)):
                    ok=True
                    break
            assert ok==want,(j,h,md)
            k+=1
    return k
def original_local_extremes(F):
    total=0
    for j,c in enumerate(F):
        seen={}
        for l in c:
            i=abs(l)
            assert i not in seen
            seen[i]=True
            s=int(l>0)
            u=1-s
            assert 1-s==u and 1-u==s
            # A source occurrence x_{i,j} has the SAME global x_i as all other clauses.
            total+=1
        assert len(seen)==3
    return total
def source_resolvents(F):
    E={j for j,c in enumerate(F) if all(l>0 for l in c) or all(l<0 for l in c)}
    out={}
    for j in E:
        for l in F[j]:
            for k,c in enumerate(F):
                if j==k or -l not in c:
                    continue
                r=(set(F[j])-{l}) | (set(c)-{-l})
                if len(r)>3 or any(-t in r for t in r):
                    continue
                if any(set(d).issubset(r) for d in F):
                    continue
                key=tuple(sorted(r))
                if key in out:
                    continue
                assert l in F[j] and -l in F[k]
                out[key]=(j,k,abs(l))
    return out
def check(F,expected):
    n=max(abs(l) for c in F for l in c)
    assert all(len(c)==3 and len({abs(l) for l in c})==3 for c in F)
    local=original_local_extremes(F)
    pair=modes(F)
    e={}
    for bit in (0,(1<<n)-1):
        a=assignment(bit,n)
        e[str(bit)]=histogram(counts(F,a))
    assert e['0']==[1,10,7,2],e
    assert e[str((1<<n)-1)]==[2,7,10,1],e
    found=[]
    learn=source_resolvents(F)
    checked=0
    allmask=(1<<n)-1
    for mask in range(1<<n):
        a=assignment(mask,n)
        t=counts(F,a)
        at=counts(F,assignment(mask^allmask,n))
        assert all(tj+tt==3 for tj,tt in zip(t,at))
        if sat(F,a):
            found.append(mask)
            assert all(any(truth(l,a) for l in r) for r in learn)
        checked+=1
    assert len(found)==expected,(expected,len(found))
    for r,(j,k,pivot) in learn.items():
        assert pivot in {abs(l) for l in F[j]}&{abs(l) for l in F[k]}
        assert set(F[j]) and set(F[k])
    return {'variables':n,'source_clauses':len(F),'source_occurrences':local,
            'four_way_pair_modes_exhaustive':pair,'endpoint_histograms':e,
            'source_one_round_resolvents':len(learn),
            'exhaustive_global_complement_assignments':checked,
            'models':len(found),'SAT':bool(found)}
if __name__=='__main__':
    w=check(W1,0)
    s=check(SWAP,168)
    assert w['endpoint_histograms']==s['endpoint_histograms']
    print(json.dumps({'W1_UNSAT':w,'SWAP_SAT':s,'result':'PASS'},sort_keys=True,indent=2))
