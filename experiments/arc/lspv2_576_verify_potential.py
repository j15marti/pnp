#!/usr/bin/env python3
"""Independent exhaustive verifier of finite 2187-clause tree Resolution potential.
This is NOT an authoritative R_mix341 checker.
Usage: python3 experiments/arc/lspv2_576_verify_potential.py [repo_root] [result_dir]
"""
import hashlib, json, pathlib, subprocess, sys
root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '.')
out=pathlib.Path(sys.argv[2] if len(sys.argv)>2 else '/tmp/lspv2_576')
source=(root/'results/raw/arc/574_k01_SIGNED_SOURCE.cnf').read_bytes()
lines=source.decode('utf8').strip().splitlines()
assert lines[0]=='p cnf 7 17'
clauses=[tuple(map(int,line.split()[:-1])) for line in lines[1:]]
assert len(clauses)==17 and all(line.endswith(' 0') for line in lines[1:])
pot=json.loads((out/'576_potential_2187.json').read_text())
assert len(pot)==3**7 and all(type(z) is int and 0<=z<=28 for z in pot)
def decode(i):
    a=[]
    for v in range(1,8):
        r=i%3;i//=3
        if r:a.append(v if r==1 else -v)
    return tuple(a)
def encode(a):
    x={abs(v):(1 if v>0 else 2) for v in a}
    return sum(x.get(v,0)*3**(v-1) for v in range(1,8))
universe=[decode(i) for i in range(3**7)]
assert len(set(universe))==3**7
assert pot[0]==28 and all(pot[encode(c)]==0 for c in clauses)
ineq=0;false_29=0
for i,a in enumerate(universe):
    if pot[i]>=28:continue
    for j,b in enumerate(universe):
        if pot[j]>=28:continue
        for p in a:
            if -p not in b:continue
            r=set(a).difference([p])|set(b).difference([-p])
            if any(-x in r for x in r):continue
            k=encode(r);ineq+=1
            assert pot[k]<=pot[i]+pot[j]+1,(i,j,p,k)
            if k==0 and 29>pot[i]+pot[j]+1:false_29+=1
assert ineq==711298 and false_29>0
checker=root/'experiments/arc/lspv2_386_independent_verify.js'
cb=checker.read_bytes()
h=hashlib.sha1(b'blob '+str(len(cb)).encode()+b'\0'+cb).hexdigest()
assert h=='338305c0ce101704205e57543756b8127074a986'
cert=out/'576_accepted_tree_min_W29.json'
pkt=json.loads(cert.read_bytes())
assert [r['c'] for r in pkt['records'] if r['kind']=='SOURCE']==[list(c) for c in clauses]
derived=pkt['records'][17:]
assert len(derived)==28 and all(r['kind']=='RES' for r in derived)
uses=[0]*len(pkt['records'])
for n,r in enumerate(pkt['records']):
    if r['kind']!='RES':continue
    assert all(p<n for p in r['parents'])
    for p in r['parents']:uses[p]+=1
assert all(uses[j]==1 for j in range(17,44)) # derived intermediates not shared
assert sum(uses[:17])==29 and pkt['records'][-1]['c']==[]
assert pkt['summary']['paid_total']==29
run=subprocess.run(['node',str(checker),str(cert)],capture_output=True,text=True,timeout=30)
assert run.returncode==0,run.stderr
v=json.loads(run.stdout)
assert v['assertions']==3542
print(json.dumps({
'PASS':True,'signed_source_SHA256':hashlib.sha256(source).hexdigest(),
'potential_SHA256':hashlib.sha256((out/'576_potential_2187.json').read_bytes()).hexdigest(),
'inequalities':ineq,'invalid_29_goal_violations':false_29,
'tree_min_RES':28,'source_leaf_uses':29,'original_checker_assertions':v['assertions']}))
