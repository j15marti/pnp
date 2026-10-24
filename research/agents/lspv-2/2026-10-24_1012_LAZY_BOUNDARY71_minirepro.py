#!/usr/bin/env python3
"""LAZY-BOUNDARY71 minimal reproducer. Run at root of j15marti/pnp.
Standard library only. Generates source-checked positive cache and negative
interface no-goods. Full independent proof checker is in downloadable package.
A query budget ending without a model is UNKNOWN, never UNSAT.
"""
import ast,collections,hashlib,json
from pathlib import Path

SOURCE=Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt")
SHA="4ed9031a7a1b1fa9fcb752f9feece1ea7201df6b610059b90793517ecd874001"
Y=tuple(range(193,199))
class Budget(Exception): pass

class DPLL:
 def __init__(self,F,cap=200000):
  self.cap=cap;self.nodes=0;self.scans=0;self.props=0
  self.masks=[(sum(1<<(l-1) for l in c if l>0),
               sum(1<<(-l-1) for l in c if l<0)) for c in F]
 def go(self,T=0,Q=0):
  if self.nodes>=self.cap:raise Budget()
  self.nodes+=1
  while True:
   change=False;todo=[]
   for i,(p,n) in enumerate(self.masks):
    self.scans+=1
    if p&T or n&Q:continue
    left=(p|n)&~(T|Q)
    if not left:return None
    if left&(left-1)==0:
     if left&p:T|=left
     else:Q|=left
     self.props+=1;change=True
    else:todo.append((left,p,n))
   if not change:break
  if not todo:return T
  score=collections.Counter()
  for left,p,n in todo:
   wt=1<<(5-min(5,left.bit_count()))
   while left:
    bit=left&-left;left-=bit;score[bit]+=wt
  bit=max(score,key=lambda v:(score[v],-v))
  pos=sum(bool(p&bit) for left,p,n in todo)
  neg=sum(bool(n&bit) for left,p,n in todo)
  first=pos>=neg
  ans=self.go(T|bit if first else T,Q if first else Q|bit)
  if ans is not None:return ans
  return self.go(T if first else T|bit,Q|bit if first else Q)

def sat_check(F,T):
 return all(any(bool((T>>(abs(l)-1))&1)==(l>0) for l in c) for c in F)

def source():
 body="\n".join(l for l in SOURCE.read_text().splitlines() if not l.startswith("#"))
 F=[tuple(c) for c in ast.literal_eval(body)]
 assert len(F)==264
 assert hashlib.sha256(json.dumps(F,separators=(",",":")).encode()).hexdigest()==SHA
 counts=collections.Counter(l for c in F for l in c)
 assert all(counts[x]==counts[-x]==2 for x in range(1,199))
 return F

def blocks(F):
 out=[]
 for g in range(6):
  lo=32*g+1;private=set(range(lo,lo+32));allowed=private|set(Y)
  B=[c for c in F if set(map(abs,c))&private and set(map(abs,c))<=allowed]
  assert len(B)==42
  supp=tuple(x for x in Y if any(abs(l)==x for c in B for l in c))
  out.append((B,supp))
 return out

def lazy(F,cache=True,short_first=False):
 BS=blocks(F);base=F[:2];learned=[];mem={};stats=collections.Counter()
 while True:
  a=None
  for bits in range(64):
   stats["candidate_rows"]+=1
   aa={y:bool((bits>>(y-193))&1) for y in Y}
   if all(any(aa[abs(l)]==(l>0) for l in c) for c in base+learned):
    a=aa;break
  if a is None:return "UNSAT_SUBFORMULA",stats,learned
  order=list(range(6))
  if short_first:order.sort(key=lambda j:(len(BS[j][1]),j))
  failed=False
  for j in order:
   B,support=BS[j]
   key=(j,tuple(a[y] for y in support))
   stats["cache_lookups"]+=1
   if cache and key in mem:
    stats["cache_hits"]+=1
    continue
   T=sum(1<<(y-1) for y in support if a[y])
   Q=sum(1<<(y-1) for y in support if not a[y])
   S=DPLL(B);witness=S.go(T,Q)
   stats["calls"]+=1;stats["nodes"]+=S.nodes;stats["clause_scans"]+=S.scans
   if witness is None:
    learned.append(tuple(-y if a[y] else y for y in support))
    failed=True;break
   if cache:mem[key]=witness
  if not failed:return "ABSTRACT_SAT_REQUIRES_SOURCE_REPLAY",stats,learned

def main():
 U=source();V=[list(c) for c in U];V[3][1]=3;V[13][0]=-3
 V=[tuple(c) for c in V]
 assert sat_check(V,DPLL(V).go())
 P=DPLL(V,cap=128);sat=P.go();assert sat is not None and P.nodes==104
 Uprobe=DPLL(U,cap=128)
 try:Uprobe.go();assert False,"UNSAT U should exhaust 128-node cap"
 except Budget:pass
 assert Uprobe.nodes==128
 res={}
 for tag,F in [("UNSAT",U),("SAT",V)]:
  policies={}
  for nm,cache,short in [("cached",True,False),("uncached",False,False),
                         ("support_order",True,True)]:
   label,stats,clauses=lazy(F,cache,short)
   policies[nm]={"outcome":label,**dict(stats),"lemmas":clauses}
  res[tag]=policies
 assert res["UNSAT"]["cached"]["calls"]==16
 assert res["UNSAT"]["cached"]["nodes"]==688
 assert len(res["UNSAT"]["cached"]["lemmas"])==6
 assert res["UNSAT"]["uncached"]["calls"]==21
 assert res["UNSAT"]["support_order"]["calls"]==15
 assert res["SAT"]["cached"]["calls"]==6
 print(json.dumps({"run":"LAZY-BOUNDARY71","source_digest":SHA,
                   "probe_SAT_nodes":P.nodes,"probe_UNSAT_nodes":Uprobe.nodes,
                   "controls":res,"P_versus_NP":"OPEN"},indent=2))
if __name__=="__main__":main()
