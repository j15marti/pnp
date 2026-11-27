# L03-11 audit.py, executed in Python 3; reproduces the native family and guarded hostile.
import itertools as I, random, json, hashlib
def ports(k):
 p=[]; ids={}
 for r in range(k):
  for c in range(k):
   q=[]
   for d,(dr,dc) in enumerate([(-1,0),(0,1),(1,0),(0,-1)]):
    rr,cc=r+dr,c+dc; v=r*k+c
    key=tuple(sorted((v,rr*k+cc))) if 0<=rr<k and 0<=cc<k else (v,v,d)
    q.append(ids.setdefault(key,len(ids)))
   p.append(q)
 pins={p[c][0]:0 for c in range(k)}|{p[(k-1)*k+c][2]:1 for c in range(k)}
 return p,pins,ids
W=list(I.product(range(2),repeat=4))
def build(k,flip=1):
 p,pins,ids=ports(k); mid=k//2; l=mid*k; r=l+k-1
 paths=[[l]+[j*k for j in range(mid-1,-1,-1)]+list(range(1,k))+[j*k+k-1 for j in range(1,mid+1)], [l]+[j*k for j in range(mid+1,k)]+list(range((k-1)*k+1,k*k))+[j*k+k-1 for j in range(k-2,mid-1,-1)],list(range(l,r+1))]
 active=[{} for _ in p]
 for i,path in enumerate(paths):
  for u,v in zip(path,path[1:]):
   e=ids[tuple(sorted((u,v)))];active[u].setdefault(i,[]).append(p[u].index(e));active[v].setdefault(i,[]).append(p[v].index(e))
 tables=[]
 for v,a in enumerate(active):
  used=sum(a.values(),[]); unused=[j for j in range(4) if j not in used]; pin=unused[:1] if used else unused[:2]
  def valid(w):
   if any(w[j]!=pins.get(p[v][j],0) for j in pin):return False
   if v in (l,r):return w[a[2][0]]==w[a[0][0]]*w[a[1][0]]
   if used:return w[used[0]]^w[used[1]] == (flip if v==l+1 else 0)
   return True
  table=[w for w in W if valid(w)];assert len(table)==4;tables.append(table)
 return p,pins,tables,len(ids)
def fingerprint(t):return hashlib.sha256(b"".join(sum(1<<sum(b<<(3-i) for i,b in enumerate(w)) for w in a).to_bytes(2,"little") for a in t)).hexdigest()
def closure(p,pins,t):
 t=[a[:] for a in t]; domains={e:{0,1} for q in p for e in q};domains.update({e:{b} for e,b in pins.items()}); rounds=0
 while True:
  rounds+=1; changed=False
  for q,a in zip(p,t):
   old=len(a);a[:]=[w for w in a if all(w[i] in domains[e] for i,e in enumerate(q))]
   if not a:return None,rounds
   changed|=old!=len(a)
   for i,e in enumerate(q):
    d=domains[e]&{w[i] for w in a};changed|=d!=domains[e];domains[e]=d
  if not changed:return t,rounds
def mul(a,b):
 out=set()
 for x in a:
  for y in b:out^={tuple(sorted(set(x+y)))}
 return out
ONE={()}
def lin_basis(rows):
 b={}
 for row in rows:
  row=set(row)
  while row:
   pivot=max(row,key=lambda x:(len(x),x))
   if pivot not in b:b[pivot]=row;break
   row^=b[pivot]
 return b
def local(q,a,degree):
 mons=[()]+[(i,) for i in range(4)]+(list(I.combinations(range(4),2)) if degree==2 else [])
 b={}; out=[]
 for j,m in enumerate(mons):
  ev=sum((all(w[i] for i in m))<<h for h,w in enumerate(a)); coeff=1<<j
  while ev:
   z=ev.bit_length()-1
   if z not in b:b[z]=(ev,coeff);break
   v,c=b[z];ev^=v;coeff^=c
  if not ev:out.append({tuple(sorted(q[i] for i in m)) for j,m in enumerate(mons) if coeff>>j&1})
 return out
def subst(poly,forms):
 out=set()
 for m in poly:
  z=ONE
  for i in m:z=mul(z,forms[i])
  out^=z
 return out
def hybrid(p,pins,t,n):
 linear=[{(e,)}^ (ONE if b else set()) for e,b in pins.items()];linear += sum((local(q,a,1) for q,a in zip(p,t)),[])
 quad=sum((local(q,a,2) for q,a in zip(p,t)),[])
 raw=lin_basis(linear+quad); assert (() in raw)==(raw.get(())==ONE)
 raw_no=() in raw; rounds=0
 while True:
  rounds+=1;b=lin_basis(linear)
  if () in b:return raw_no,True,rounds,len(b),0
  forms={i:{(i,)} for i in range(n)}
  for m,row in sorted(b.items()):forms[m[0]]=subst(row^{m},forms)
  qb=lin_basis(subst(row,forms) for row in quad)
  if () in qb:return raw_no,True,rounds,len(b),len(qb)
  learned=[row for m,row in qb.items() if len(m)==1]
  if not learned:return raw_no,False,rounds,len(b),len(qb)
  linear+=learned
def reference(k,p,pins,t,cap):
 states={tuple(sorted(pins.items()))}; attempts=0
 for v,(q,a) in enumerate(zip(p,t)):
  future=set(e for qq in p[v+1:] for e in qq);new=set()
  for s in states:
   d=dict(s)
   for w in a:
    attempts+=1
    if attempts>cap:return None,attempts
    if all(e not in d or d[e]==b for e,b in zip(q,w)):
     x=d|dict(zip(q,w));new.add(tuple(sorted((e,b) for e,b in x.items() if e in future)))
  states=new
  if not states:return False,attempts
 return bool(states),attempts
def main():
 rows=[]
 for k in [3,4,8,16,32]:
  p,pins,t,n=build(k);cl,r=closure(p,pins,t);assert cl is not None
  raw,no,hr,lr,qr=hybrid(p,pins,cl,n);assert not raw and no
  ref,steps=reference(k,p,pins,t,100000)
  if ref is not None:assert not ref
  rows.append(dict(k=k,N=16*k*k,hash=fingerprint(t),arc_rounds=r,raw_no=raw,hybrid_no=no,hybrid_rounds=hr,affine_rank=lr,quadratic_rank=qr,reference=ref,reference_attempts=steps))
 p,pins,t,n=build(3,0);cl,r=closure(p,pins,t);assert cl is not None
 assert not hybrid(p,pins,cl,n)[1] and reference(3,p,pins,t,100000)[0]
 rng=random.Random(612); hostile=None; outcomes={'arc_rejected':0,'hybrid_rejected':0,'reference_sat_excluded':0,'reference_unknown':0}
 k=4;p,pins,ids=ports(k);n=len(ids)
 pins.update({p[r*k][3]:0 for r in range(k)});pins.update({p[r*k+k-1][1]:0 for r in range(k)})
 for attempt in range(1,2001):
  t=[rng.sample([w for w in W if all(w[i]==pins[e] for i,e in enumerate(q) if e in pins)],4) for q in p]
  cl,r=closure(p,pins,t)
  if cl is None:outcomes['arc_rejected']+=1;continue
  raw,no,hr,lr,qr=hybrid(p,pins,cl,n)
  if no:outcomes['hybrid_rejected']+=1;continue
  ref,steps=reference(k,p,pins,t,100000)
  if ref is None:outcomes['reference_unknown']+=1;continue
  if ref:outcomes['reference_sat_excluded']+=1;continue
  hostile=dict(attempt=attempt,hash=fingerprint(t),masks=[[sum(b<<(3-i) for i,b in enumerate(w)) for w in a] for a in t],arc_rounds=r,raw_no=raw,hybrid_rounds=hr,affine_rank=lr,quadratic_rank=qr,reference=ref,reference_attempts=steps);break
 print(json.dumps(dict(family=rows,hostile=hostile,search_outcomes=outcomes,seed=612,guard="hostile only: east/west exterior zero",reference_cap=100000),indent=2))
if __name__=='__main__':main()
