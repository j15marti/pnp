#!/usr/bin/env python3
"""LSPV-3 SPLIT-EXCESS353: source-labelled adaptive splitting and certified upper DAGs.
No SAT oracle, external package, or mutation of the shared Rmix341 inference rules.
Run: python experiments/arc/lspv3_353_split_excess_compact.py
Outputs JSON to stdout; independent full Node referee in companion local archive.
"""
import json
BASE=[(-3,1,4),(-1,2),(1,3),(-4,-3),(-2,-1,3),(-2,4)]
STEPS=[('v0','v3',4),('v2','d0',3),('v3','v5',4),
       ('v4','d2',3),('v1','d3',2),('d1','d4',1)]
def canonical(xs):return tuple(sorted(set(xs),key=lambda x:(abs(x),x)))
def satisfied(c,a):return any(((a>>(abs(v)-1))&1)==int(v>0) for v in c)
def resolve(a,b,p):
 assert (p in a and -p in b) or (-p in a and p in b)
 r=canonical(v for v in a+b if abs(v)!=p)
 assert not any(-v in r for v in r)
 return r
def source_witness(i):
 for a in range(16):
  if not satisfied(BASE[i],a) and all(j==i or satisfied(c,a) for j,c in enumerate(BASE)):return a
 raise AssertionError('seed is not minimally UNSAT')
def run(t,policy):
 leaf={f'v{i}':{'id':f'v{i}','origin':i,'clause':canonical(c),'depth':0,'path':{}} for i,c in enumerate(BASE)}
 history=[]
 for j in range(1,t+1):
  if policy=='wide':v=min(leaf.values(),key=lambda a:(a['depth'],a['origin'],a['id']))
  else:v=min(leaf.values(),key=lambda a:(-a['depth'],a['origin'],a['id']))
  del leaf[v['id']]
  z=4+j
  for idx,lit,val in [(0,z,0),(1,-z,1)]:
   ident=f'v{6+2*j-2+idx}'
   leaf[ident]={'id':ident,'origin':v['origin'],'clause':canonical(v['clause']+(lit,)),
                'depth':v['depth']+1,'path':dict(v['path'],**{str(z):val})}
  history.append((v['id'],f'v{6+2*j-2}',f'v{6+2*j-1}',z))
 source=sorted(leaf.values(),key=lambda a:(a['origin'],a['id']))
 known={s['id']:s['clause'] for s in source};dag=[]
 for parent,left,right,p in reversed(history):
  out=resolve(known[left],known[right],p)
  dag.append((parent,left,right,p,out));known[parent]=out
 for i,(left,right,p) in enumerate(STEPS):
  out=resolve(known[left],known[right],p)
  dag.append((f'd{i}',left,right,p,out));known[f'd{i}']=out
 assert dag[-1][4]==() and len(dag)==t+6
 for s in source:
  a=source_witness(s['origin'])
  for z,val in s['path'].items():a|=val<<(int(z)-1)
  assert not satisfied(s['clause'],a)
  assert all(u is s or satisfied(u['clause'],a) for u in source)
  for k in range(len(s['clause'])):
   flipped=list(s['clause']);flipped[k]=-flipped[k]
   assert satisfied(flipped,a)
 text=f'p cnf {t+4} {len(source)}\n'+''.join(' '.join(map(str,s['clause']))+' 0\n' for s in source)
 return {'splits':t,'policy':policy,'variables':t+4,'sources':len(source),
         'proof_nodes':len(dag),'DIMACS_bytes':len(text.encode()),
         'max_source_width':max(map(lambda v:len(v['clause']),source)),
         'certified_lower':t+5,'constructive_upper':t+6}
if __name__=='__main__':
 cases=[run(t,policy) for t in (0,1,2,4,8,16,32,64) for policy in ('wide','deep')]
 print(json.dumps({'version':'SPLIT-EXCESS353','calculus':'unchanged Rmix341',
                   'controls':'all source-deletion and occurrence-sign witnesses checked',
                   'scope':'upper proof via RES only; all-mixed lower by essential source arity',
                   'cases':cases},indent=2))
