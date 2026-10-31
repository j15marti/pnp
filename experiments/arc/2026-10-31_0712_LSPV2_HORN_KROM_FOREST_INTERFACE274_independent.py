#!/usr/bin/env python3
"""Independent verifier for HORN-KROM-FOREST-INTERFACE274 JSON.
No producer imports. Exhaustive source truth tables; replay source-indexed resolution
DAGs; verify signed original S/U targets, coherent flip frames, endpoint complement,
and adversarial certificate corruption rejection.
"""
import sys,json,itertools,copy,hashlib

def truth(l,word):return word[abs(l)-1] == (l>0)
def clause_value(C,word):return sum(truth(l,word) for l in C)
def evaluate(F,word):return all(clause_value(C,word)>0 for C in F)
def norm(C):
 C=set(C)
 if any(-l in C for l in C):return None
 return tuple(sorted(C,key=lambda z:(abs(z),z<0)))
def resolution(A,B,p):
 if not ((p in A and -p in B) or (-p in A and p in B)):
  raise ValueError('wrong resolution pivot')
 return norm([l for l in A if abs(l)!=abs(p)]+[l for l in B if abs(l)!=abs(p)])
def check_proof(T,proof,root):
 claims={i+1:tuple(C) for i,C in enumerate(T)}
 for st in proof:
  ix=st['id']; u,v=st['parents'];p=st['pivot']
  assert u<ix and v<ix and ix==len(claims)+1
  assert u in claims and v in claims
  got=resolution(claims[u],claims[v],p)
  assert got is not None and got==tuple(st['clause'])
  claims[ix]=got
 if root is not None:assert root in claims and claims[root]==()
 return len(proof)
def check_audit(F,n,audit):
 checks=0
 records=audit['signed_occurrences']
 assert len(records)==sum(map(len,F))
 for r in records:
  l=F[r['clause']-1][r['position']-1]
  assert l==r['literal'] and r['source_variable']==abs(l)
  s=int(l>0); assert r['S_value']==r['U_inverse_S']==s
  assert r['U_value']==r['S_inverse_U']==1-s
  checks+=4
 def check_mode(A,B,tag,word):
  for C,mode in ((A,tag[0]),(B,tag[1])):
   if clause_value(C,word)!=(len(C) if mode=='S' else 0):return False
  return True
 for p in audit['pair_extreme_compatibility']:
  j,k=p['source_pair'];assert 1<=j<k<=len(F)
  A=F[j-1];B=F[k-1]
  for tag in ('SS','SU','US','UU'):
   ans=False
   for word in itertools.product((False,True),repeat=n):
    if check_mode(A,B,tag,word):ans=True;break
   assert p[tag]==ans
   checks+=1
 frames=audit['coherent_flip_frames'];assert len(frames)==n+1
 for i,fr in enumerate(frames):
  assert fr['assignment']==[int(j<i) for j in range(n)]
  assert fr['flip']==(None if i==0 else i)
  ct=[clause_value(C,list(map(bool,fr['assignment']))) for C in F]
  assert fr['true_counts']==ct
  assert fr['categories']=={str(k):ct.count(k) for k in range(4)}
  checks+=len(F)+4
 for A,B in zip(frames,frames[1:]):
  flip=B['flip']
  for j,C in enumerate(F):
   d=sum(1-2*int(truth(l,list(map(bool,A['assignment'])))) for l in C if abs(l)==flip)
   assert A['true_counts'][j]+d==B['true_counts'][j];checks+=1
 for c0,c1,C in zip(frames[0]['true_counts'],frames[-1]['true_counts'],F):
  assert c0+c1==len(C);checks+=1
 return checks

def check_record(row):
 F=row['F'];n=row['n'];count=check_audit(F,n,row['audit'])
 models=[a for a in itertools.product((False,True),repeat=n) if evaluate(F,a)]
 assert bool(models)==(row['label']=='SAT');count+=2**n
 if row['source_witness'] is not None:
  assert evaluate(F,row['source_witness'])
 else:assert not models
 if row['policy'].startswith('REJECT'):
  assert any(len(c)!=3 for c in F)
  return count,0
 T=row['T'];groups=row['groups']; assert len(T)==7*len(F)
 assert row['T_n']==n+3*len(F)
 assert len(groups)==len(F)
 for j,(g,C) in enumerate(zip(groups,F)):
  assert g['source']==j+1 and g['lits']==C and g['T_ids']==list(range(7*j+1,7*j+8))
  ys=[n+3*j+k+1 for k in range(3)]
  assert g['y']==ys and T[7*j]==[-y for y in ys]
  for k,(l,y) in enumerate(zip(C,ys)):
   assert T[7*j+2*k+1]==[l,y]
   assert T[7*j+2*k+2]==[-l,-y]
   for x in (False,True):
    for z in (False,True):
     word=[False]*(n+3*len(F));word[abs(l)-1]=x;word[y-1]=z
     left=evaluate(T[7*j+2*k+1:7*j+2*k+3],word)
     assert left==(z != truth(l,word));count+=1
  count+=3
 for x in itertools.product((False,True),repeat=n):
  y=[not truth(l,x) for C in F for l in C]
  full=x+tuple(y)
  assert evaluate(T,full)==evaluate(F,x)
  assert evaluate([T[j] for j in range(7*len(F)) if j%7!=0],full)
  count+=2
 if row['transformed_witness'] is not None:
  assert evaluate(T,row['transformed_witness'])
  assert evaluate(F,row['transformed_witness'][:n])
 else:assert not models
 proof=row['source_resolution_certificate'];root=row['source_refutation_root']
 count+=check_proof(T,proof,root)
 if not models:assert root is not None
 # Certificates must contain recovered original source clauses (in proof DAG, three resolutions each).
 recovered={st['orig_clause']:st['clause'] for st in proof if st.get('kind')=='recover' and st.get('orig_clause') and len(st['clause'])==3 and all(abs(l)<=n for l in st['clause'])}
 assert all(norm(F[j-1])==tuple(recovered[j]) for j in range(1,len(F)+1))
 child=row['child_original_F_dedup']; assert set(map(tuple,child))==set(map(tuple,F))
 assert row['child_bits']==8*len('p cnf %d %d\n'%(n,len(child))+''.join(' '.join(map(str,c))+' 0\n' for c in child))
 assert row['power_short']==(row['child_bits']**2<=row['parent_bits'])
 if row['derived_source_resolvent']:
  d=row['derived_source_resolvent'];a,b=d['parents_original'];
  assert tuple(d['entailed_clause'])==resolution(F[a-1],F[b-1],d['pivot'])
  for x in itertools.product((False,True),repeat=n):
   if evaluate(F,x):assert clause_value(d['entailed_clause'],x)>0
  count+=2**n
 return count,len(proof)

def test_corruptions(row):
 if 'T' not in row:return 0
 T=row['T'];proof=row['source_resolution_certificate'];root=row['source_refutation_root']
 if root is None:return 0
 tamper=0
 for kind in ('pivot','parent','conclusion','root'):
  P=copy.deepcopy(proof);r=root
  if kind=='pivot':P[0]['pivot']=999999
  elif kind=='parent':P[0]['parents'][0]=999999
  elif kind=='conclusion':P[0]['clause']=[999999]
  elif kind=='root':r=P[0]['id']
  try:check_proof(T,P,r)
  except (AssertionError,ValueError,KeyError):tamper+=1
  else:raise AssertionError('mutant accepted: '+kind)
 return tamper

def main(p):
 with open(p) as f:raw=json.load(f)
 summary={'cases':0,'source_checks':0,'proof_nodes':0,'corrupted_certificates_rejected':0,'SAT':0,'UNSAT':0}
 for row in raw['cases']:
  n,pn=check_record(row)
  summary['cases']+=1;summary['source_checks']+=n;summary['proof_nodes']+=pn
  summary[row['label']]+=1
  summary['corrupted_certificates_rejected']+=test_corruptions(row)
 assert summary['cases']==raw['totals']['formulas']
 assert summary['SAT']==raw['totals']['SAT'] and summary['UNSAT']==raw['totals']['UNSAT']
 assert summary['proof_nodes']==raw['totals']['proof_nodes']
 print(json.dumps(summary,indent=2));return summary
if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/lspv2_horn_krom_274_raw.json')