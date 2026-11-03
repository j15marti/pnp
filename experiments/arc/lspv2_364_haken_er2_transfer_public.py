#!/usr/bin/env python3
"""Finite PHP and strict Resolution certificate controls; no asymptotic proof."""
import json
from itertools import combinations

def canon(s):
    s=set(s)
    if 0 in s or any(-v in s for v in s): raise ValueError("bad clause")
    return tuple(sorted(s,key=lambda x:(abs(x),x<0)))

def php(n,p=None):
    if p is None:p=n+1
    v=lambda i,j:i*n+j+1
    a=[canon(v(i,j) for j in range(n)) for i in range(p)]
    for j in range(n):
        for i,k in combinations(range(p),2):
            a.append(canon((-v(i,j),-v(k,j))))
    return n*p,a

def count_models(n,clauses):
    return sum(all(any(bool(mask>>(abs(x)-1)&1)==(x>0) for x in c) for c in clauses)
               for mask in range(1<<n))

def proof(n,sources):
    rec=[dict(rule="source",clause=list(c),source=i) for i,c in enumerate(sources)]
    ids={c:i for i,c in enumerate(sources)}
    active=set(sources)
    for p in range(1,n+1):
        pos=sorted(c for c in active if p in c)
        neg=sorted(c for c in active if -p in c)
        made=set()
        for a in pos:
            for b in neg:
                z=set(a)|set(b);z.remove(p);z.remove(-p)
                if any(-x in z for x in z):continue
                c=canon(z);made.add(c)
                if c not in ids:
                    ids[c]=len(rec)
                    rec.append(dict(rule="res",clause=list(c),parent_a=ids[a],parent_b=ids[b],pivot=p))
        active={c for c in active if p not in c and -p not in c}|made
        if () in ids:break
    assert () in ids
    relevant=set()
    def walk(i):
        if i in relevant:return
        relevant.add(i)
        if rec[i]["rule"]=="res":
            walk(rec[i]["parent_a"]);walk(rec[i]["parent_b"])
    walk(ids[()])
    compact=[];mapping={}
    for i in sorted(relevant):
        r=rec[i].copy()
        if r["rule"]=="res":
            r["parent_a"]=mapping[r["parent_a"]]
            r["parent_b"]=mapping[r["parent_b"]]
        mapping[i]=len(compact);compact.append(r)
    return compact

def check(n,sources,rec):
    out=[]
    for row in rec:
        c=canon(row["clause"])
        if row["rule"]=="source":
            assert c==sources[row["source"]]
        else:
            i,j,p=row["parent_a"],row["parent_b"],row["pivot"]
            assert i<len(out) and j<len(out) and i>=0 and j>=0
            a,b=out[i],out[j]
            assert (p in a and -p in b) or (-p in a and p in b)
            w=(set(a)|set(b))-{p,-p}
            assert c==canon(w)
        out.append(c)
    assert out[-1]==()
    return sum(x["rule"]=="res" for x in rec)

def main():
    ans=[]
    for n in (1,2,3):
        v,F=php(n);proofdag=proof(v,F)
        paid=check(v,F,proofdag)
        sv,S=php(n,n)
        d="p cnf %d %d\n"%(v,len(F))+"".join(" ".join(map(str,c))+" 0\n" for c in F)
        ans.append(dict(n=n,clauses=len(F),variables=v,paid_res_nodes=paid,
                        source_ascii_bytes=len(d.encode()),proof_json_bits=8*len(json.dumps(proofdag,separators=(",",":")).encode()),
                        unsat_models=count_models(v,F),sat_control_models=count_models(sv,S)))
    print(json.dumps(ans,sort_keys=True))
if __name__=="__main__":main()
