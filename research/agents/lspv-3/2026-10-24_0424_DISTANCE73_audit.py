#!/usr/bin/env python3
"""Independent exact DISTANCE73 audit. Python 3 standard library only.
Run from repository root with no arguments, or provide original-source path.
No SAT solver or random sampling is invoked.
"""
import ast
import collections
import hashlib
import itertools
import json
import pathlib
import sys

def sat(cnf, n):
    for a in itertools.product((False, True), repeat=n):
        if all(any(a[abs(z)-1] if z > 0 else not a[abs(z)-1] for z in c) for c in cnf):
            return True
    return False

def exact22(cnf, n):
    assert len(cnf)*3 == 4*n
    p = [0]*(n+1)
    q = [0]*(n+1)
    seen = set()
    for c in cnf:
        assert len(c)==3 and len(set(map(abs,c)))==3
        k=tuple(sorted(c))
        assert k not in seen
        seen.add(k)
        for z in c:
            assert 1<=abs(z)<=n
            (p if z>0 else q)[abs(z)]+=1
    assert all(p[x]==q[x]==2 for x in range(1,n+1))
    return True

def toy():
    sets=list(itertools.combinations(range(4),2))
    cases=[]
    for x,y in itertools.product(range(6), repeat=2):
        f=tuple(((1 if j in sets[x] else -1),(2 if j in sets[y] else -2)) for j in range(4))
        cases.append((x,y,f))
    edges={}
    for i,(x,y,_) in enumerate(cases):
        edges[i]=[
            j for j,(u,v,_) in enumerate(cases)
            if (y==v and len(set(sets[x])&set(sets[u]))==1)
            or (x==u and len(set(sets[y])&set(sets[v]))==1)]
    yes={i for i,(_,_,f) in enumerate(cases) if sat(f,2)}
    no=set(range(36))-yes
    assert yes and no
    dq=collections.deque(yes); dist={i:0 for i in yes}
    while dq:
        i=dq.popleft()
        for j in edges[i]:
            if j not in dist:
                dist[j]=dist[i]+1;dq.append(j)
    assert len(dist)==36
    original={(1,2),(1,-2),(-1,2),(-1,-2)}
    u=next(i for i,(_,_,f) in enumerate(cases) if set(f)==original)
    assert u in no and dist[u]==1
    yes_pairs={(i,j) for i in yes for j in yes}
    dp={v:0 for v in yes_pairs}
    dq=collections.deque(yes_pairs)
    while dq:
        i,j=dq.popleft()
        for k,l in [(v,j) for v in edges[i]]+[(i,v) for v in edges[j]]:
            if (k,l) not in dp:
                dp[k,l]=dp[i,j]+1; dq.append((k,l))
    assert len(dp)==1296
    assert all(dp[i,j]==dist[i]+dist[j] for i in range(36) for j in range(36))
    assert all((dp[u,j]<=1)==(j in yes) for j in range(36))
    return dict(source_model="balanced signed 2CNF hostile control, not 3CNF",
                signings=36, sat=len(yes), unsat=len(no),
                all_product_signings=1296, additive_cases_checked=1296,
                trivial_root_island_cases=36, radius_one_checks=36,
                fixed_unsat_distance=1, max_distance=max(dist.values()))

def real_source(path):
    if not path.exists():
        return {"source_access":"UNAVAILABLE", "path":str(path)}
    raw=path.read_bytes()
    lines=[line for line in raw.decode().splitlines() if not line.startswith("#")]
    f=ast.literal_eval("\n".join(lines))
    assert len(f)==264 and exact22(f,198)
    assert f[3]==[-2,-3,-194] and f[13]==[3,9,10]
    v=[list(c) for c in f];v[3][1]=3;v[13][0]=-3
    assert exact22(v,198)
    witness=bin(int("39a2b53c16ab15bc16ab15ca4b9715c4faa7143d31b0f26598",16))[2:].zfill(198)
    def failures(cs):
        return [i for i,c in enumerate(cs)
                if not any((witness[abs(z)-1]=="1") if z>0
                           else (witness[abs(z)-1]=="0") for z in c)]
    assert failures(f)==[3] and failures(v)==[]
    def shift(cs,o):
        return [[(abs(z)+o)*(1 if z>0 else -1) for z in c] for c in cs]
    assert exact22(f+shift(f,198),396)
    assert exact22(f+shift(v,198),396)
    return dict(source_access="GitHub original file",sha256=hashlib.sha256(raw).hexdigest(),
                original_variables=198,original_clauses=264,original_bits=15870,
                double_bits=33824,source_grammar_checked=True,
                real_mutant_witness_checked=True,original_witness_failures=[3],
                two_copy_grammar_checked=True,
                imported_UNSAT_proof="not rerun: peer DOECKER-CORE-CERT61")

def main():
    here=pathlib.Path(__file__).resolve()
    default=here.parents[1]/"lspv-2"/"2026-10-24_0011_DOECKER61_original_source.txt"
    fallback=pathlib.Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt")
    path=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else (default if default.exists() else fallback)
    out=dict(run="DISTANCE73",status="COMPUTATIONAL",seed=None,
             experiment="exhaustive 2CNF source swap graph; actual 198/264 clause and witness replay",
             toy=toy(),doecker=real_source(path))
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=="__main__":
    main()
