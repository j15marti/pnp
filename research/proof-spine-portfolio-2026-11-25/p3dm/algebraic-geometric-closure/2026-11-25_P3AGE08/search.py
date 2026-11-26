from audit import *
r=random.Random(2125);pool=list(I.product(range(3),repeat=3));stats={'sampled':0,'planar':0,'stagnant':0,'sat':0,'unsat':0,'all_unknown':0,'wrong':0};open_cases=[]
for _ in range(1200):
    T=sorted(r.sample(pool,r.randrange(8,15)));stats['sampled']+=1
    if not nx.check_planarity(graph(T,3))[0]:continue
    stats['planar']+=1;S=close(T,3)
    if S is None or len(S)!=len(T):continue
    stats['stagnant']+=1;ref=solve_ref(T,3);stats['sat' if ref is not None else 'unsat']+=1
    jobs=[run(T,3,c,d,1) for c,d in I.combinations(range(3),2)]
    assert all(q['status']=='UNKNOWN' or (q['status']=='YES')==(ref is not None) for q in jobs)
    if all(q['status']=='UNKNOWN' for q in jobs):
        stats['all_unknown']+=1;open_cases.append({'T':T,'ref':ref,'jobs':jobs,'k2':[run(T,3,c,d,2) for c,d in I.combinations(range(3),2)]})
print(json.dumps({'stats':stats,'cases':open_cases},indent=2))
