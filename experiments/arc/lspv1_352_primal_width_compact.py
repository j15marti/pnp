#!/usr/bin/env python3
"""LSPV-1 352: exact source-indexed Davis-Putnam Resolution proof upper compiler.
Fixed Rmix341 RES subsystem; no oracle; results are upper, not global minima.
Run: python experiments/arc/lspv1_352_primal_width_compact.py
"""
import itertools,json,hashlib
def norm(c):
 s=set(c)
 if 0 in s or any(-x in s for x in s):raise ValueError("bad clause")
 return tuple(sorted(s,key=lambda x:(abs(x),x)))
def graph(F):
 g={abs(x):set() for C in F for x in C}
 for C in F:
  for a,b in itertools.combinations(sorted(set(map(abs,C))),2):
   g[a].add(b);g[b].add(a)
 return g
def width(order,G):
 G={v:set(z) for v,z in G.items()};w=0
 for x in order:
  nb=G[x];w=max(w,len(nb))
  for a,b in itertools.combinations(nb,2):G[a].add(b);G[b].add(a)
  for a in nb:G[a].remove(x)
  del G[x]
 return w
def solve(F):
 F=list(dict.fromkeys(norm(C) for C in F));G=graph(F);vs=list(G)
 if len(vs)<=8: order=min(itertools.permutations(vs),key=lambda p:(width(p,G),p))
 else:
  H={v:set(z) for v,z in G.items()};order=[]
  while H:
   x=min(H,key=lambda v:(len(H[v]),v));nb=H[x]
   for a,b in itertools.combinations(nb,2):H[a].add(b);H[b].add(a)
   for a in nb:H[a].remove(x)
   del H[x];order.append(x)
 w=width(order,G);rows=[{"kind":"source","c":list(C)} for C in F]
 active={C:i for i,C in enumerate(F)}
 for x in order:
  plus=[(C,i) for C,i in active.items() if x in C]
  minus=[(C,i) for C,i in active.items() if -x in C]
  next={C:i for C,i in active.items() if x not in C and -x not in C}
  for A,i in plus:
   for B,j in minus:
    s=set(A)|set(B);s.discard(x);s.discard(-x)
    if any(-z in s for z in s):continue
    C=norm(s)
    if C not in next:
     k=len(rows);rows.append({"kind":"RES","c":list(C),"pos":i,"neg":j,"pivot":x});next[C]=k
  active=next
 root=active.get(())
 if root is not None:
  seen=set();todo=[root]
  while todo:
   i=todo.pop()
   if i in seen:continue
   seen.add(i)
   if rows[i]["kind"]=="RES":todo.extend([rows[i]["pos"],rows[i]["neg"]])
  paid=sum(rows[i]["kind"]=="RES" for i in seen)
 else:paid=None
 out={"order":list(order),"primal_width":w,"original_clauses":[list(c) for c in F],
      "rows":rows,"root":root,"paid_ancestry":paid,"width_upper":len(order)*3**w}
 if (root is not None) != (models(F)==0 if len(vs)<=12 else root is not None):
  raise AssertionError("label inconsistency")
 return out
def models(F):
 vs=sorted({abs(x) for C in F for x in C})
 if len(vs)>12:return None
 ans=0
 for t in range(1<<len(vs)):
  val=dict(zip(vs,((t>>i)&1 for i in range(len(vs)))))
  if all(any(val[abs(x)]==(x>0) for x in C) for C in F):ans+=1
 return ans
def tseitin(odd):
 E=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)];F=[]
 for v in range(4):
  incident=[i+1 for i,(a,b) in enumerate(E) if a==v or b==v]
  for bits in itertools.product((0,1),repeat=3):
   if sum(bits)%2 != (1 if odd and v==0 else 0):
    F.append([e if not b else -e for e,b in zip(incident,bits)])
 return F
def blockers(n):return [[i+1 if (bits>>i)&1==0 else -(i+1) for i in range(n)] for bits in range(1<<n)]
def horn(n):return [[1]]+[[-i,i+1] for i in range(1,n)]+[[-n]]
cases={"horn5":horn(5),"horn12":horn(12),"oddK4":tseitin(True),"evenK4":tseitin(False),
 "G342":[[-3,1,4],[-1,2],[1,3],[-4,-3],[-2,-1,3],[-2,4]],
 "Peitl7":[[-1,2],[-2,3],[-3,4],[-4,5],[1,-5],[1,2,3,4,5],[-1,-2,-3,-4,-5]],
 "block4":blockers(4),"block5":blockers(5),"units":[[1],[-1]]}
result=[]
for name,F in cases.items():
 r=solve(F)
 # Check source-ancestry soundness, pivot orientation and exact clause:
 for i,x in enumerate(r["rows"]):
  if x["kind"]=="RES":
   A=set(r["rows"][x["pos"]]["c"]);B=set(r["rows"][x["neg"]]["c"]);p=x["pivot"]
   assert x["pos"]<i and x["neg"]<i and p in A and -p in B
   assert norm((A-{p})|(B-{-p}))==norm(x["c"])
 n=len(r["order"]);m=len(r["original_clauses"])
 assert len(r["rows"])-m <= r["width_upper"]
 result.append({"name":name,"n":n,"m":m,"width":r["primal_width"],"delta":m-n,
   "proof_rows":len(r["rows"])-m,"root_ancestry":r["paid_ancestry"],
   "bound":r["width_upper"],"models":models(F),
   "source_sha256":hashlib.sha256(json.dumps(r["original_clauses"],separators=(",",":")).encode()).hexdigest()})
print(json.dumps(result,indent=2))
