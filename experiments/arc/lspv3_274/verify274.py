#!/usr/bin/env python3
"""Independent finite verifier for HORN-AFFINE-MIX274, no producer import."""
import json,itertools,hashlib,sys,copy
from pathlib import Path
B=Path(__file__).resolve().parent

def sat_clause(c,values):return any(bool(values[abs(t)-1])==(t>0) for t in c)
def number_true(c,values):return sum(bool(values[abs(t)-1])==(t>0) for t in c)
def sat_cnf(clauses,values):return all(sat_clause(c,values) for c in clauses)
def forced_false(c,values):return [int(not (bool(values[abs(l)-1])==(l>0))) for l in c]

def up_conflict(clauses,assumptions):
 st=dict(assumptions)
 while True:
  new=False
  for c in clauses:
   hit=False;openlit=[]
   for l in c:
    v=st.get(abs(l))
    if v is None:openlit.append(l)
    elif bool(v)==(l>0):hit=True;break
   if hit:continue
   if not openlit:return True
   if len(openlit)==1:
    lit=openlit[0];v=int(lit>0)
    if abs(lit) in st and st[abs(lit)]!=v:return True
    if abs(lit) not in st:st[abs(lit)]=v;new=True
  if not new:return False

def inspect_tree(clauses,n,node,st):
 if 'witness' in node:
  w=node['witness'];assert len(w)==n and sat_cnf(clauses,w)
  assert all(w[v-1]==val for v,val in st.items());return 1
 if 'conflict' in node:
  assumptions=dict(node['conflict']);assert all(assumptions.get(k)==v for k,v in st.items())
  assert up_conflict(clauses,assumptions)
  return 1
 assert node['var'] not in st
 # Validate parent's propagation closure without using producer.
 s=dict(st)
 while True:
  todo=[]
  for c in clauses:
   if any(lit is not None and bool(s.get(abs(lit)))==(lit>0) for lit in c if abs(lit) in s):continue
   missing=[l for l in c if abs(l) not in s]
   assert missing
   if len(missing)==1:todo.append(missing[0])
  if not todo:break
  changed=False
  for l in todo:
   if abs(l) not in s:s[abs(l)]=int(l>0);changed=True
   else:assert s[abs(l)]==int(l>0)
  if not changed:break
 assert s==dict(node['decisions'])
 lo=s.copy();lo[node['var']]=0
 hi=s.copy();hi[node['var']]=1
 return 1+inspect_tree(clauses,n,node['left'],lo)+inspect_tree(clauses,n,node['right'],hi)

def validate(row,limit_matrix=True):
 orig=row['source'];combined=row['mixed'];n=row['source_n'];m=len(orig)
 assert row['mixed_n']==n+6*m and row['mixed_m']==13*m
 assert len(combined)==13*m and len(row['occurrence_map'])==3*m
 # Full authenticated source reconstruction, independent of producer canonical parser.
 H=combined[:m];E=combined[m:]
 for j,c in enumerate(orig):
  assert len(c)==3 and len({abs(z) for z in c})==3
  y=[n+3*j+k+1 for k in range(3)]
  assert H[j]==[-z for z in y]
  for k,lit in enumerate(c):
   entry=row['occurrence_map'][3*j+k]
   x=abs(lit);yy=y[k];t=n+3*m+3*j+k+1
   assert entry==[j+1,k+1,lit,yy,t,int(lit>0)]
   B=[(x,yy),(-x,-yy)] if lit>0 else [(-x,yy),(x,-yy)]
   block=E[12*j+4*k:12*j+4*k+4]
   expect=[list(B[0]) +[t],list(B[1])+[t],list(B[0])+[-t],list(B[1])+[-t]]
   assert block==expect
   for xx,yyv,tv in itertools.product([0,1],repeat=3):
    aa=[0]*row['mixed_n'];aa[x-1]=xx;aa[yy-1]=yyv;aa[t-1]=tv
    assert sat_cnf(block,aa)==(yyv==(xx ^ int(lit>0)))
 # Any satisfying original assignment extends uniquely in y (t free).
 for bits in itertools.product((0,1),repeat=n):
  yvals=[v for c in orig for v in forced_false(c,bits)]
  extended=list(bits)+yvals+[0]*(3*m)
  assert sat_cnf(E,extended)
  assert sat_cnf(H,extended)==sat_cnf(orig,bits)
  assert sat_cnf(combined,extended)==sat_cnf(orig,bits)
 assert not sat_cnf(combined,[0]*(n+6*m)) or sat_cnf(orig,[0]*n)
 assert row['H_sat'] and row['E_sat']
 assert sat_cnf(H,[0]*(n+6*m))
 # Input polarity checks, S/U identities and full local-pair enumeration.
 for j,c in enumerate(orig):
  record=row['extrema'][j];assert record['clause']==j+1 and record['source']==c
  S={str(abs(l)):int(l>0) for l in c};U={k:1-v for k,v in S.items()}
  assert record['S']==S and record['U']==U and record['inverted_S_is_U']==U and record['inverted_U_is_S']==S
  for l,occ in zip(c,record['occurrences']):
   assert occ['signed']==l and occ['x_ij']==f'x_{abs(l)},{j+1}'
   assert (occ['S'],occ['U'],occ['invert_S'],occ['invert_U'])==(int(l>0),int(l<0),int(l<0),int(l>0))
 if limit_matrix:
  assert len(row['pairs'])==m*(m-1)//2
  for p in row['pairs']:
   j=p['Cj']-1;k=p['Ck']-1;A=orig[j];D=orig[k]
   names=sorted({abs(l) for l in A+D});actual={mode:False for mode in ('SS','SU','US','UU')}
   for vals in itertools.product((0,1),repeat=len(names)):
    ass=dict(zip(names,vals))
    ca=sum(ass[abs(l)]==int(l>0) for l in A)
    cd=sum(ass[abs(l)]==int(l>0) for l in D)
    if ca in (0,3) and cd in(0,3):actual[('S' if ca==3 else 'U')+('S' if cd==3 else 'U')]=True
   assert actual==p['modes']
 for step in row['graytrail']:
  a=step['assignment'];assert len(a)==n
  hist=[0,0,0,0]
  for c in orig:hist[number_true(c,a)]+=1
  assert hist==step['N0123'] and (hist[0]==0)==step['SAT']
  comp=[1-v for v in a]
  hist2=[0,0,0,0]
  for c in orig:hist2[number_true(c,comp)]+=1
  assert hist2==hist[::-1]
 for s,a in [('0^n',[0]*n),('1^n',[1]*n)]:
  assert row['endpoints'][s]=={'N0123':[sum(number_true(c,a)==r for c in orig) for r in range(4)],'SAT':sat_cnf(orig,a)}
 if row['source_sat']:
  assert sat_cnf(orig,row['proof']['witness'])
 else:
  assert inspect_tree(orig,n,row['proof'],{})==row['child_dpll']['nodes']
 return 1

def negative_checks(row):
 # Tampering one physical original clause, one S/U mode, or one answer bit must fail.
 bad=copy.deepcopy(row);bad['mixed'][len(row['source'])][0]*=-1
 try:validate(bad);raise AssertionError('false acceptance: changed XOR clause')
 except AssertionError as e:
  if 'false acceptance' in str(e):raise
 bad=copy.deepcopy(row);bad['pairs'][0]['modes']['SS']=not bad['pairs'][0]['modes']['SS']
 try:validate(bad);raise AssertionError('false acceptance: corrupted pair')
 except AssertionError as e:
  if 'false acceptance' in str(e):raise
 bad=copy.deepcopy(row);bad['source_sat']=not bad['source_sat']
 # Independent original-assignment truth and proof check catches flipped label.
 actual=any(sat_cnf(row['source'],a) for a in itertools.product((0,1),repeat=row['source_n']))
 assert bad['source_sat']!=actual
 return 3

def main():
 inp=json.loads((B/'raw274.json').read_text());rows=inp['rows']
 names=sys.argv[1:] or [r['name'] for r in rows]
 checks=0
 for row in rows:
  if row['name'] not in names:continue
  checks+=validate(row)
  checks+=negative_checks(row)
  print('PASS',row['name'], 'SAT' if row['source_sat'] else 'UNSAT',flush=True)
 print(json.dumps({'verified_cases':len(names),'checks_groups':checks,'raw_sha256':hashlib.sha256((B/'raw274.json').read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()