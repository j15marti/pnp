#!/usr/bin/env python3
"""LSPV-1/618: exhaustive small-graph parity-source and redundancy controls.
Independent of the archived /341 checker and its accepted-byte syntax.
"""
import itertools, json, hashlib, pathlib, sys
from collections import Counter


def graphs():
    k4 = [(i,j) for i in range(4) for j in range(i+1,4)]
    k33 = [(i,j) for i in range(3) for j in range(3,6)]
    cube = [(i,i^(1<<b)) for i in range(8) for b in range(3) if i < (i^(1<<b))]
    pete = [(i,(i+1)%5) for i in range(5)]
    pete += [(i,i+5) for i in range(5)]
    pete += [(i+5,((i+2)%5)+5) for i in range(5)]
    return [("K4",4,k4),("K33",6,k33),("cube",8,cube),("Petersen",10,pete)]


def is_connected(vertices,edges,without=None):
    avail=set(range(vertices)) - ({without} if without is not None else set())
    if not avail:return True
    seen={next(iter(avail))}; stack=list(seen)
    while stack:
        v=stack.pop()
        for a,b in edges:
            u=b if a==v else a if b==v else None
            if u is not None and u in avail and u not in seen:
                seen.add(u);stack.append(u)
    return seen==avail


def run():
    out={"status":"pass","method":"exhaustive all edge assignments (at most 2^15 per graph), all 70 four-pattern S", "cases":[]}
    for name,V,edges in graphs():
        E=len(edges);t=0
        assert E*2==3*V and len(set(tuple(sorted(x)) for x in edges))==E
        assert all(sum(v in edge for edge in edges)==3 for v in range(V))
        assert is_connected(V,edges) and all(is_connected(V,edges,without=v) for v in range(V))
        incid=[[i for i,(a,b) in enumerate(edges) if a==v or b==v] for v in range(V)]
        bypat=Counter()
        for bits in range(1<<E):
            if any(sum((bits>>e)&1 for e in incid[v])&1 for v in range(1,V)):
                continue
            pat=sum(((bits>>e)&1)<<j for j,e in enumerate(incid[t]))
            bypat[pat]+=1
        unit=1<<(E-V-1)
        assert all(bypat[p]==(unit if p.bit_count()%2==0 else 0) for p in range(8))
        hist=Counter(); total_models=0; all_false_sat_controls=0
        cases=[]
        for S in itertools.combinations(range(8),4):
            k=sum(s.bit_count()%2==0 for s in S)
            models=sum(v for pat,v in bypat.items() if pat not in S)
            t_essential=sum(bypat[s]>0 for s in S)
            expected=(4-k)*unit
            assert models==expected and t_essential==k
            assert not (models>0 and t_essential==4)
            hist[k]+=1;total_models+=models
            if models>0:all_false_sat_controls+=1
            cases.append({"forbidden":list(S),"even_forbidden":k,"models":models,"terminal_vertex_essential":t_essential})
        assert [hist[i] for i in range(5)]==[1,16,36,16,1]
        out["cases"].append({"graph":name,"V":V,"E":E,"target":t,"local_unit":unit,"per_local_pattern":dict(sorted(bypat.items())),"source_choices":len(cases),"satisfiable_sources":all_false_sat_controls,"k_histogram":{str(i):hist[i] for i in range(5)},"full_case_results":cases,"model_count_sum":total_models})
    return out


if __name__=="__main__":
    d=run()
    p=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else (pathlib.Path(__file__).resolve().parents[2]/'results/raw/arc/2026-11-13_0526_LSPV1_618_ONE_DEFECTIVE_CHARGE_RAW.json')
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p,'w') as f:json.dump(d,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({"status":d["status"],"results":[{k:v for k,v in x.items() if k!='full_case_results' and k!='per_local_pattern'} for x in d["cases"]],"raw_path":str(p),"sha256":hashlib.sha256(open(p,'rb').read()).hexdigest()},indent=2))
