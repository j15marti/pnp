#!/usr/bin/env python3
"""Generate LSPV-3/512 three-arm Tseitin typed certificate (semantic declaration ONLY).
The returned 57-node proof uses AND3, XOR, LOCAL, RES and original CNF sources;
NOT a claim of acceptance by an unavailable full historical R_mix341 byte checker.
Independent replay is in the downloadable lspv3_512_independent_replay.py.
"""
import hashlib,itertools,json,sys
edges=[]
for j in range(3):
 u,a,b,c,d=[1+5*j+k for k in range(5)]
 edges.extend([(0,u),(a,u),(u,b),(a,c),(a,d),(b,c),(b,d),(c,d)])
inc={v:[] for v in range(16)}
for e,(u,v) in enumerate(edges,1): inc[u].append(e);inc[v].append(e)
charge=[1]+[0]*15;source=[];where={};per={}
for v in range(16):
 per[v]=[]
 for bits in itertools.product((0,1),repeat=3):
  if sum(bits)%2==charge[v]:continue
  idx=len(source);per[v].append(idx);where[(v,bits)]=idx
  source.append([-e if b else e for e,b in zip(inc[v],bits)])
cnf='p cnf 24 64\n'+''.join(' '.join(map(str,c))+' 0\n' for c in source)
nodes=[]
def add(rule,p,**kw):
 x={'id':'N'+str(len(nodes)),'rule':rule,'parents':p};x.update(kw);nodes.append(x);return x['id']
units=[]
for j in range(3):
 root=1+5*j;rows=[]
 for v in range(root+1,root+5):
  p=['S'+str(i) for i in per[v]]
  a=add('AND3',p[:2]);b=add('AND3',p[2:])
  rows.append(add('AND3',[a,b],row={'mask':inc[v],'rhs':charge[v]}))
 x=add('XOR',rows[:2]);y=add('XOR',rows[2:]);row=add('XOR',[x,y])
 bridge=inc[0][j];i=inc[root].index(bridge);chosen=[]
 for bits in itertools.product((0,1),repeat=3):
  if bits[i]==1 and sum(bits)%2!=charge[root]:chosen.append('S'+str(where[(root,bits)]))
 assert len(chosen)==2
 f=add('AND3',chosen);g=add('AND3',[f,row]);units.append((bridge,add('LOCAL',[g],clause=[-bridge])))
center=where[(0,(0,0,0))];ref='S'+str(center);remain=source[center][:]
for bridge,unit in units:
 remain.remove(bridge)
 ref=add('RES',[ref,unit],pivot=bridge,clause=remain[:])
pack={'name':'LSPV3-512-bridge-star','calculus':'Rmix341-DECLARED-SEMANTIC-SUBLANGUAGE; NOT HISTORICAL BYTE CHECKER',
 'source_dimacs':cnf,'source_sha256':hashlib.sha256(cnf.encode()).hexdigest(),
 'graph':{'vertices':16,'edges':edges,'charges':charge},'nodes':nodes,'root':ref,
 'expected':{'paid':57,'and3':42,'xor':9,'local':3,'res':3,'used_sources':55,'all_sources':64}}
assert len(source)==64 and len(nodes)==57 and ref=='N56'
json.dump(pack,open(sys.argv[1] if len(sys.argv)>1 else 'lspv3_512_certificate.json','w'),indent=2)
print(json.dumps({'paid':57,'source_sha256':pack['source_sha256'],'root':ref,'warning':pack['calculus']}))
