#!/usr/bin/env python3
"""Exact tree-like Resolution optimum on the signed 17-clause guarded K4.
Reference enumerator and native-/386 OS replayer, not an R_mix341 checker.
Usage: python3 experiments/arc/lspv2_576_tree_min.py [repo_root] [output_dir]
"""
import collections, copy, hashlib, itertools, json, pathlib, subprocess, sys, tempfile
root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '.')
out=pathlib.Path(sys.argv[2] if len(sys.argv)>2 else '/tmp/lspv2_576')
out.mkdir(parents=True,exist_ok=True)
P=root/'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json'
F=root/'results/raw/arc/574_k01_SIGNED_SOURCE.cnf'
V=root/'experiments/arc/lspv2_386_independent_verify.js'
hash256=lambda b:hashlib.sha256(b).hexdigest()
blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
assert blob(V.read_bytes())=='338305c0ce101704205e57543756b8127074a986'
seed=json.loads(P.read_bytes())
src=seed['records'][:17]
assert all(s['kind']=='SOURCE' for s in src)
original=F.read_bytes().decode().strip().splitlines()
assert original[0]=='p cnf 7 17'
assert [list(map(int,s.split()[:-1])) for s in original[1:]]==[r['c'] for r in src]
C=lambda a:tuple(sorted(set(a),key=lambda x:(abs(x),x)))
best={C(r['c']):0 for r in src}; bags=[[] for i in range(29)]
bags[0]=list(best); parent={};cand=0;taut=0
for t in range(1,29):
    for u in range(t):
        v=t-1-u
        for a in bags[u]:
            for b in bags[v]:
                for p in a:
                    if -p not in b:continue
                    cand+=1
                    r=C([x for x in a if x!=p]+[x for x in b if x!=-p])
                    if any(-x in r for x in r):taut+=1;continue
                    if r not in best:
                        best[r]=t;parent[r]=(a,b,p);bags[t].append(r)
assert best[()]==28
U=[tuple(v if (i//(3**(v-1)))%3==1 else -v for v in range(1,8) if (i//(3**(v-1)))%3) for i in range(3**7)]
index={c:i for i,c in enumerate(U)}
assert len(index)==2187
h=lambda c:min(28,best.get(c,28))
pot=[h(c) for c in U]
ineq=0
for a in U:
    if h(a)>=28:continue
    for b in U:
        if h(b)>=28:continue
        for p in a:
            if -p not in b:continue
            r=C([x for x in a if x!=p]+[x for x in b if x!=-p])
            if any(-x in r for x in r):continue
            ineq+=1
            assert h(r)<=h(a)+h(b)+1
assert ineq==711298 and pot[0]==28
records=copy.deepcopy(src);indices={C(r['c']):i for i,r in enumerate(records)}
def emit(c):
    if c in indices:return indices[c]
    a,b,p=parent[c];i=emit(a);j=emit(b)
    k=len(records);records.append({'kind':'RES','c':list(c),'parents':[i,j],'pivot':p});indices[c]=k
    return k
assert emit(())==len(records)-1
R=len(records)-17;assert R==28
cert={'spec':seed['spec'],'gate_defs':seed['gate_defs'],'records':records,'summary':{'source':17,'def_views':0,'resolution':R,'paid_gates':1,'paid_total':29,'live_records':len(records)}}
b=(json.dumps(cert,separators=(',',':'))+'\n').encode()
(out/'576_accepted_tree_min_W29.json').write_bytes(b)
pb=(json.dumps(pot,separators=(',',':'))+'\n').encode()
(out/'576_potential_2187.json').write_bytes(pb)
checks=[]
with tempfile.TemporaryDirectory() as d:
    cases=[('accepted',cert,True)]
    for name,modify in [
        ('underpay',lambda x:x['summary'].__setitem__('paid_total',28)),
        ('source_forgery',lambda x:x['records'][0]['c'].__setitem__(0,-1)),
        ('forward_port',lambda x:x['records'][-1]['parents'].__setitem__(0,len(x['records']))),
        ('unknown_AND3',lambda x:x['records'][-1].__setitem__('kind','AND3'))]:
        x=copy.deepcopy(cert);modify(x);cases.append((name,x,False))
    for name,x,want in cases:
        data=(json.dumps(x,separators=(',',':'))+'\n').encode()
        f=pathlib.Path(d)/(name+'.json');f.write_bytes(data)
        r=subprocess.run(['node',str(V),str(f)],capture_output=True,text=True,timeout=30)
        assert (r.returncode==0)==want,(name,r.stderr)
        checks.append({'name':name,'accepted':want,'sha256':hash256(data),'bytes':len(data),'original_assertions':json.loads(r.stdout)['assertions'] if want else None})
result={'status':'PROVED/EXACT finite tree-like RES cost + COMPUTATIONAL original-checker replay; NOT DAG/mixed/full Rmix341',
        'source_sha256':hash256(F.read_bytes()),'original_checker_blob':blob(V.read_bytes()),
        'clauses_universe':2187,'cost_histogram':[len(x) for x in bags],
        'goal_tree_min_res':28,'paid_W_with_owner':29,'candidate_resolvents':cand,'tautology_skips':taut,
        'potential_inequalities':ineq,'potential_sha256':hash256(pb),'certificate_sha256':hash256(b),'cases':checks}
(out/'576_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
