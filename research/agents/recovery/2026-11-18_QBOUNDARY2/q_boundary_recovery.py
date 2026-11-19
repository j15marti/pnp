"""Exact finite boundary audit. No random grids. python q_boundary_recovery.py"""
import itertools as I, json
W=({1,3},{2,4},{0,3},{1,4},{0,2})
def rel(a,b,c,mode):
    return ((b in W[a]) != (c in W[a])) if mode=='Q' else ((b in W[a]) and (c in W[a]))
def models(cl,mode):
    vs=sorted(set(v for c in cl for v in c))
    ans=[]; checks=0
    for vals in I.product(range(5),repeat=len(vs)):
        a=dict(zip(vs,vals)); ok=True
        for c in cl:
            checks+=1
            if not rel(*(a[v] for v in c),mode): ok=False; break
        if ok: ans.append(a)
    return ans,checks
def table(ms,S):
    t={}
    for a in ms:
        key=tuple(a[v] for v in S)
        t[key]=t.get(key,0)+1
    return t
clauses=[(h,a,b) for h in range(4) for a,b in I.combinations([v for v in range(4) if v!=h],2)]
raw={'seed':None,'clauses':clauses,'paired':[], 'metric':'Q/P predicate evaluations and boundary-row lookups; not native RAM instructions'}
for mode in ['Q','P']:
    rows=[]; checks=0; lookups=0; peak_entries=0
    for i,c in enumerate(clauses):
        for j,d in enumerate(clauses):
            A,ca=models([c],mode); B,cb=models([d],mode); C,cc=models([c,d],mode)
            checks+=ca+cb+cc
            S=sorted(set(c)&set(d)); ta=table(A,S); tb=table(B,S)
            # Same first boundary variable fixes a COMMON rotation.
            oa={k:v for k,v in ta.items() if k[0]==0}; ob={k:v for k,v in tb.items() if k[0]==0}
            total=0; witness=None
            for rest in I.product(range(5),repeat=len(S)-1):
                key=(0,)+rest; lookups+=2
                total+=5*oa.get(key,0)*ob.get(key,0)
                if witness is None and key in oa and key in ob:
                    aa=next(a for a in A if tuple(a[v] for v in S)==key)
                    bb=next(b for b in B if tuple(b[v] for v in S)==key)
                    witness=aa|bb
            assert total==len(C)
            if witness is not None: assert all(rel(*(witness[v] for v in e),mode) for e in [c,d])
            assert (witness is not None)==bool(C)
            peak_entries=max(peak_entries,len(oa)+len(ob))
            rows.append({'i':i,'j':j,'boundary':S,'count':total,'witness':witness})
    raw['paired'].append({'mode':mode,'pairs':rows,'predicate_checks':checks,'boundary_lookups':lookups,
                          'peak_two_sparse_orbit_tables_entries':peak_entries})
Q={v for v in I.product(range(5),repeat=3) if rel(*v,'Q')}
proj={(i,j):{(v[i],v[j]) for v in Q} for i,j in I.combinations(range(3),2)}
closure=[v for v in I.product(range(5),repeat=3) if all((v[i],v[j]) in p for (i,j),p in proj.items())]
assert len(Q)==60 and len(closure)==100
core=[(0,1,2),(0,1,3),(1,0,2),(1,2,3),(2,0,3)]
relaxed=[a for a in I.product(range(5),repeat=4) if all(a[y]!=a[z] for x,y,z in core)]
exact,_=models(core,'Q'); assert not exact and len(relaxed)==180
deletions=[len(models(core[:i]+core[i+1:],'Q')[0]) for i in range(5)]
assert deletions==[10,40,10,30,25]
raw['projection']={'Q_count':len(Q),'binary_closure_count':len(closure),'first_false_positive':next(v for v in closure if v not in Q),
 'core':core,'core_exact':len(exact),'core_relaxed':len(relaxed),'relaxed_assignments':relaxed,'deletion_counts':deletions}
raw['status']='PASS'
raw['space_note']='Audit retains brute-force model lists and raw output. Peak table entries count only the two sparse quotient tables, not process RAM or total audit memory.'
print(json.dumps(raw,indent=2))
