#!/usr/bin/env python3
"""LSPV-3 HORN-AFFINE-MIX274: exact proper-3CNF conjunction countercontrol."""
import json, sys, time, hashlib, itertools, os
from pathlib import Path
BASE=Path(__file__).resolve().parent

def ok(c,a): return any((a[abs(l)-1] if l>0 else 1-a[abs(l)-1]) for l in c)
def ev(cnf,a): return all(ok(c,a) for c in cnf)
def dimacs(n,cnf):return 'p cnf %d %d\n'%(n,len(cnf))+''.join(' '.join(map(str,c))+' 0\n' for c in cnf)
def counts(cnf,a):
 out=[]
 for c in cnf:out.append(sum(a[abs(l)-1] if l>0 else 1-a[abs(l)-1] for l in c))
 return [out.count(i) for i in range(4)]

def prop(cnf,state,ledger):
 st=state.copy(); changed=True
 while changed:
  changed=False
  for c in cnf:
   ledger['clause_visits']+=1; unk=[]; sat=False
   for l in c:
    ledger['literal_tests']+=1
    x=st.get(abs(l))
    if x is None:unk.append(l)
    elif (x==1)==(l>0):sat=True;break
   if sat:continue
   if not unk:return st,False
   if len(unk)==1:
    l=unk[0];v=1 if l>0 else 0
    old=st.get(abs(l))
    if old is not None and old!=v:return st,False
    if old is None:st[abs(l)]=v;ledger['units']+=1;changed=True
 return st,True

def dpll(cnf,n,cap=2000):
 ledger={'nodes':0,'leaves':0,'units':0,'clause_visits':0,'literal_tests':0,'complete':True}
 def rec(st):
  if ledger['nodes']>=cap:ledger['complete']=False;return None,None
  ledger['nodes']+=1
  s,consistent=prop(cnf,st,ledger)
  if not consistent:ledger['leaves']+=1;return False,{'conflict':[[i,v] for i,v in sorted(st.items())]}
  ledger['clause_visits']+=len(cnf)
  if all(any(abs(l) in s and ((s[abs(l)]==1)==(l>0)) for l in c) for c in cnf):
   witness=[s.get(i,0) for i in range(1,n+1)]
   assert ev(cnf,witness)
   return True,{'witness':witness}
  idx=next(i for i in range(1,n+1) if i not in s)
  children=[]
  for val in (0,1):
   q=s.copy();q[idx]=val
   ans,proof=rec(q)
   if ans is None:return None,None
   children.append(proof)
   if ans:return True,proof
  return False,{'var':idx,'decisions':[[i,v] for i,v in sorted(s.items())], 'left':children[0], 'right':children[1]}
 answer,pr=rec({})
 return answer,pr,ledger

def verify_proof(cnf,n,proof,st=None):
 if st is None:st={}
 if 'witness' in proof:return ev(cnf,proof['witness'])
 if 'conflict' in proof:
  assumed=dict(proof['conflict'])
  if any(assumed.get(k)!=v for k,v in st.items()):return False
  scratch={'clause_visits':0,'literal_tests':0,'units':0}
  return not prop(cnf,assumed,scratch)[1]
 if 'var' not in proof or proof['var'] in st:return False
 # Parent may include forced units, validated through UP at this state.
 aux={'clause_visits':0,'literal_tests':0,'units':0}
 s,consistent=prop(cnf,st,aux)
 if not consistent:return False
 if s!=dict(proof['decisions']):return False
 v=proof['var']
 l=s.copy();l[v]=0;r=s.copy();r[v]=1
 return verify_proof(cnf,n,proof['left'],l) and verify_proof(cnf,n,proof['right'],r)

def mixer(n,clauses):
 assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in clauses)
 m=len(clauses); H=[];E=[];meta=[]
 # Original variables 1..n, occurrence-falsity y in n+1..n+3m, private padding t in n+3m+1..n+6m.
 for j,c in enumerate(clauses):
  Y=[n+3*j+k+1 for k in range(3)]
  H.append(tuple(-y for y in Y))
  for k,l in enumerate(c):
   x=abs(l);y=Y[k];t=n+3*m+3*j+k+1;b=1 if l>0 else 0
   binaries=((x,y),(-x,-y)) if b else ((-x,y),(x,-y))
   eq=[(a,v,t) for a,v in binaries]+[(a,v,-t) for a,v in binaries]
   # Explicit order [binary0 +t, binary1 +t, binary0 -t, binary1 -t]
   E.extend(eq);meta.append([j+1,k+1,l,y,t,b])
 return n+6*m,H,E,meta

def auth_recover(n,mixed):
 # Strong canonical source recognizer, no metadata trusted; rejects malformed/renamed.
 if len(mixed)%13:return None
 m=len(mixed)//13
 if len(mixed)<1:return None
 n= max((abs(x) for c in mixed for x in c),default=0)-6*m
 if n<1:return None
 H=mixed[:m]; E=mixed[m:]; cand=[]
 for j,h in enumerate(H):
  expect=tuple(-(n+3*j+k+1) for k in range(3))
  if tuple(h)!=expect:return None
  ls=[]
  for k in range(3):
   start=4*(3*j+k); block=E[start:start+4]
   y=n+3*j+k+1;t=n+3*m+3*j+k+1
   if any(len(c)!=3 or len({abs(z) for z in c})!=3 for c in block):return None
   if block[0][2]!=t or block[1][2]!=t or block[2][2]!=-t or block[3][2]!=-t:return None
   if block[0][:2]!=block[2][:2] or block[1][:2]!=block[3][:2]:return None
   if abs(block[0][0])!=abs(block[1][0]) or block[0][1]!=y or block[1][1]!=-y:return None
   x=abs(block[0][0]);
   if x<1 or x>n or block[1][0]!=-block[0][0]:return None
   # b=1 iff x positive in first binary
   l=x if block[0][0]>0 else -x
   ls.append(l)
  if len(set(map(abs,ls)))!=3:return None
  cand.append(tuple(ls))
 # regenerate every signed clause, not just local tests
 newn,h2,e2,meta=mixer(n,cand)
 if newn!=max(abs(x) for c in mixed for x in c) or [tuple(c) for c in mixed]!=h2+e2:return None
 return n,cand

def extremal(cnf,n,limit=40000):
 per=[]; pairs=[]; counts_pairs={'SS':0,'SU':0,'US':0,'UU':0,'all_incompatible':0}
 for j,c in enumerate(cnf):
  S={abs(x):int(x>0) for x in c};U={k:1-v for k,v in S.items()}
  per.append({'clause':j+1,'source':list(c),'S':S,'inverted_S_is_U':U,'U':U,'inverted_U_is_S':S,
              'occurrences':[{'x_ij':f'x_{abs(l)},{j+1}','signed':l,'S':int(l>0),'U':int(l<0),'invert_S':int(l<0),'invert_U':int(l>0)} for l in c]})
 for j,c in enumerate(cnf):
  for k in range(j+1,len(cnf)):
   d=cnf[k];same=any(abs(a)==abs(b) and (a>0)==(b>0) for a in c for b in d)
   opposite=any(abs(a)==abs(b) and (a>0)!=(b>0) for a in c for b in d)
   mask={'SS':not opposite,'SU':not same,'US':not same,'UU':not opposite}
   for name,b in mask.items():counts_pairs[name]+=int(b)
   counts_pairs['all_incompatible']+=int(not any(mask.values()))
   if len(pairs)<limit:pairs.append({'Cj':j+1,'Ck':k+1,'modes':mask})
 return per,pairs,counts_pairs

def graytrail(cnf,n,steps=16):
 arr=[]
 for i in range(min(2**n,steps)):
  g=i^(i>>1);a=[(g>>j)&1 for j in range(n)]
  arr.append({'flip_count':i,'gray_mask':g,'assignment':a,'N0123':counts(cnf,a),'SAT':ev(cnf,a)})
 return arr

def witness_expand(orig, source_witness,m):
 x=list(source_witness); y=[]
 for c in orig:
  y.extend(int(not (x[abs(l)-1] if l>0 else (1-x[abs(l)-1]))) for l in c)
 return x+y+[0]*(3*m)

def main():
 fixtures=json.loads((BASE/'fixtures271.json').read_text())
 chosen=sys.argv[1:] or ['HORN_CHAIN_SAT','HORN_CHAIN_UNSAT','KROM_SAT','KROM_UNSAT','RANDOM3_SEED11','RANDOM3_SEED12','SWAP6_SAT','W1_UNSAT','SWAP6_RENAMED_SAT','W1_RENAMED_UNSAT']
 rows=[]
 for name in chosen:
  src=fixtures[name];orig=[tuple(c) for c in src['original_clauses']]
  if any(len(c)!=3 or len(set(map(abs,c)))!=3 for c in orig):continue
  n=src['n'];m=len(orig);mixed_n,H,E,meta=mixer(n,orig);combined=H+E
  rec=auth_recover(mixed_n,combined)
  assert rec is not None and rec==(n,orig),(name,'bad reconstruction')
  label,proof,L=dpll(orig,n,cap=10000)
  assert label is not None and (label or verify_proof(orig,n,proof)),name
  if label:assert ev(combined,witness_expand(orig,proof['witness'],m))
  else:assert not any(ev(orig,a) for a in itertools.product((0,1),repeat=n)) if n<=8 else True
  # Both individual families are always SAT, explicitly verified.
  wH=[0]*mixed_n
  wE=witness_expand(orig,[0]*n,m)
  assert ev(H,wH) and ev(E,wE)
  # Baseline original-source UP-first DPLL on physical mixed only for small fixtures.
  mixed_label=None; mixed_ledger=None
  if m<=8:
   mixed_label,mixed_proof,mixed_ledger=dpll(combined,mixed_n,cap=1200)
   assert mixed_label==label,name
  # Full original-source controls, with explicit occurrence and clause provenance
  extrema,pairs,pc=extremal(orig,n)
  a0=[0]*n;a1=[1]*n
  row={'name':name,'source_n':n,'source_m':m,'source_sat':label,'H_sat':True,'E_sat':True,
       'mixed_n':mixed_n,'mixed_m':len(combined),'input_bytes':len(dimacs(mixed_n,combined)),'child_bytes':len(dimacs(n,orig)),
       'source_bytes':len(dimacs(n,orig)),'recognition_clause_visits':len(combined),'recognized':True,
       'full_mixed_nodes':mixed_ledger['nodes'] if mixed_ledger else None,
       'full_mixed_tests':mixed_ledger['literal_tests'] if mixed_ledger else None,
       'child_dpll':L,'proof':proof,'source':orig,'mixed':combined,'occurrence_map':meta,
       'extrema':extrema,'pairs':pairs,'pair_counts':pc,
       'endpoints':{'0^n':{'N0123':counts(orig,a0),'SAT':ev(orig,a0)},'1^n':{'N0123':counts(orig,a1),'SAT':ev(orig,a1)}},
       'graytrail':graytrail(orig,n),
       'declared_storage_bits':{'input_materialized':8*len(dimacs(mixed_n,combined)),
                                'child_materialized':8*len(dimacs(n,orig)),
                                'occurrence_metadata_proxy':len(json.dumps(meta).encode())*8,
                                'proof_host_proxy':len(json.dumps(proof).encode())*8}}
  rows.append(row)
  print(name,'SAT' if label else 'UNSAT','m',m,'mixed',len(combined),'full_nodes',row['full_mixed_nodes'],'source_nodes',L['nodes'],'ratio',round(row['input_bytes']/row['child_bytes'],2),flush=True)
 out={'run':'HORN-AFFINE-MIX274','version':'v1','seed':'deterministic','family':'occurrence false-indicator Horn + affine','rows':rows}
 raw=json.dumps(out,separators=(',',':'),sort_keys=True).encode()
 (BASE/'raw274.json').write_bytes(raw)
 mini={'run':out['run'],'case_count':len(rows),'SAT':sum(x['source_sat'] for x in rows),'UNSAT':sum(not x['source_sat'] for x in rows),'cases':[{'name':r['name'],'SAT':r['source_sat'],'m':r['source_m'],'mixed_m':r['mixed_m'],'mixed_bytes':r['input_bytes'],'child_bytes':r['child_bytes'],'baseline_nodes':r['full_mixed_nodes'],'child_nodes':r['child_dpll']['nodes'],'full_mixed_literal_tests':r['full_mixed_tests'],'child_literal_tests':r['child_dpll']['literal_tests'],'S_U_pairs':len(r['pairs'])} for r in rows],'raw_sha256':hashlib.sha256(raw).hexdigest()}
 (BASE/'summary274.json').write_text(json.dumps(mini,indent=2))
 print(json.dumps(mini,indent=2))
if __name__=='__main__':main()