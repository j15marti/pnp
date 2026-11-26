from pathlib import Path
exec(Path(__file__).with_name('audit.py').read_text().split('P,x,t=base();')[0])
A=[[(3*i,3*i+1,3*i+2) for i in range(3)]]+[[tuple(3*i+(a*i+b)%3 for i in range(3)) for b in range(3)] for a in range(3)]
assert not any(sat(A,z) for z in it.product((0,1),repeat=9))
POLY=[-8,-7,1] # (x-8)(x+1), base K9
r=random.Random(21);rows=[]
for trial in range(100):
 Q=[]
 for part in A:
  out=[]
  for c in part:
   s=r.choice([a for a in it.product((0,1),repeat=3) if len(set(a))==2]);out.extend(tuple(2*v+(j^a) for v,a in zip(c,s)) for j in (0,1))
  Q.append(out)
 auth(18,Q);assert sat(Q,[i%2 for i in range(18)])
 w,d=terminal(18,Q)
 if d['groups']==9:
  assert w is None and d['reason']=='quotient_no_unknown'
  rows.append({'trial':trial,**d,'source_SAT':True,'partitions':Q});break
assert rows
print(json.dumps(rows,indent=2))
