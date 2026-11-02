#!/usr/bin/env python3
"""Independent no-import verifier for REFEREE285."""
import argparse,collections,functools,itertools,json

F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
C={None:0,0:1,1:2}
checks=0
def ck(x):
 global checks;assert x;checks+=1
def truth(p):return all(any(p[abs(x)-1]==(x>0) for x in c) for c in F)
def desc(vals):
 rows=[];sums=[]
 for c in F:
  r=[]
  for x in c:
   q=vals[abs(x)-1];r.append(0 if q is None else C[int(q==(x>0))])
  rows.append(tuple(r));sums.append((2 in r,r.count(0),r.count(1)))
 return tuple(C[x] for x in vals),tuple(rows),tuple(sums)
def models(vals):
 free=[i for i,x in enumerate(vals) if x is None];q=0
 for z in range(1<<len(free)):
  a=list(vals)
  for k,i in enumerate(free):a[i]=(z>>k)&1
  q+=truth(a)
 return q
def obdd():
 tab=tuple(int(truth([(z>>i)&1 for i in range(9)])) for z in range(512));cost={}
 for S in range(512):
  pre=[i for i in range(9) if S>>i&1]
  for v in range(9):
   if S>>v&1:continue
   rest=[i for i in range(9) if not(S>>i&1) and i!=v];pairs=set()
   for pa in range(1<<len(pre)):
    base=sum(((pa>>k)&1)<<i for k,i in enumerate(pre));lo=hi=0
    for rb in range(1<<len(rest)):
     z=base+sum(((rb>>k)&1)<<i for k,i in enumerate(rest));lo|=tab[z]<<rb;hi|=tab[z|1<<v]<<rb
    if lo!=hi:pairs.add((lo,hi))
   cost[S,v]=len(pairs)
 @functools.lru_cache(None)
 def dp(S,w):
  if S==511:return 0
  q=[cost[S,v]+dp(S|1<<v,w) for v in range(9) if not(S>>v&1)]
  return (max if w else min)(q)
 S=nat=0
 for v in range(9):nat+=cost[S,v];S|=1<<v
 return {"best":dp(0,False),"natural":nat,"worst":dp(0,True)}
def trail(gray):
 seq=[z^(z>>1) if gray else z for z in range(512)];flips=occ=summ=0
 D=[desc(tuple((z>>i)&1 for i in range(9))) for z in seq]
 for a,b,x,y in zip(seq,seq[1:],D,D[1:]):
  h=(a^b).bit_count();flips+=h;occ+=4*h;summ+=sum(i!=j for i,j in zip(x[2],y[2]))
 return flips,occ,summ,5*flips,(seq[0]^seq[-1]).bit_count()
def circuit():
 g=[];dep={i:0 for i in range(1,10)};outs=[]
 def add(op,a,b):
  z=10+len(g);g.append((z,op,a,b));dep[z]=1+max(dep[abs(a)],dep[abs(b)]);return z
 for c in F:
  q=add('OR',c[0],c[1]);outs.append(add('OR',q,c[2]))
 while len(outs)>1:outs=[add('AND',outs[i],outs[i+1]) if i+1<len(outs) else outs[i] for i in range(0,len(outs),2)]
 return g,outs[0],dep[outs[0]]
def ceval(g,r,a):
 b={i+1:x for i,x in enumerate(a)}
 for z,op,x,y in g:
  u=b[abs(x)] if x>0 else 1-b[abs(x)];v=b[abs(y)] if y>0 else 1-b[abs(y)];b[z]=int((u or v) if op=='OR' else (u and v))
 return bool(b[r])
def main():
 ap=argparse.ArgumentParser();ap.add_argument("raw");a=ap.parse_args();r=json.load(open(a.raw))
 occ=[[] for _ in range(10)]
 for ci,c in enumerate(F):
  for si,x in enumerate(c):occ[abs(x)].append((ci,si))
 for v in range(1,10):ck(len(occ[v])==4)
 states={vals:desc(vals) for vals in itertools.product((None,0,1),repeat=9)};ck(len(states)==3**9)
 labels={vals:models(vals)>0 for vals in states};tot=ext=lab=slot=summ=dphys=0;sh=collections.Counter();dh=collections.Counter()
 for vals,A in states.items():
  for v in range(1,10):
   for q in (None,0,1):
    if q==vals[v-1]:continue
    w=list(vals);w[v-1]=q;w=tuple(w);B=states[w]
    changed={(ci,si) for ci,(ra,rb) in enumerate(zip(A[1],B[1])) for si,(x,y) in enumerate(zip(ra,rb)) if x!=y}
    ck(changed==set(occ[v]));z=sum(x!=y for x,y in zip(A[2],B[2]));sh[z]+=1;summ+=z;slot+=4;tot+=1
    dd=(C[vals[v-1]]^C[q]).bit_count()+sum((A[1][ci][si]^B[1][ci][si]).bit_count() for ci,si in changed)
    dh[dd]+=1;dphys+=dd
    if vals[v-1] is None and q is not None:ext+=1
    if labels[vals]!=labels[w]:lab+=1
 T=r["F9"]["transitions"]
 ck((tot,ext,lab,slot,summ,dphys)==(T["directed_single_trit_transitions"],T["pin_extension_transitions"],T["label_changing_transitions"],T["occurrence_record_changes"],T["clause_summary_record_changes"],T["core_fixed_layout_bit_xor"]))
 ck({str(k):v for k,v in sh.items()}==T["summary_change_histogram"]);ck({str(k):v for k,v in dh.items()}==T["core_dphys_histogram"])
 ck([models((x, None,None,0,1,None,None,0,None)) for x in (0,1)]==[7,0])
 ck(obdd()==r["F9"]["obdd"]=={"best":52,"natural":66,"worst":80})
 for name,g in (("binary_trail",False),("gray_trail",True)):
  q=trail(g);x=r["F9"][name];ck(q==(x["variable_flips"],x["occurrence_record_changes"],x["clause_summary_record_changes"],x["core_fixed_layout_bit_xor"],x["endpoint_variable_delta"]))
 ck(r["F9"]["models"]==sum(truth([(z>>i)&1 for i in range(9)]) for z in range(512))==70)
 g,root,depth=circuit();ck((len(g),depth)==(35,6))
 ones=0
 for z in range(512):
  a=[(z>>i)&1 for i in range(9)];b=ceval(g,root,a);ck(b==truth(a));ones+=b
 ck((ones,r["F9"]["forward_private"]["truth_table_rows"],r["F9"]["forward_private"]["output_ones"])==(70,512,70))
 ck(r["P_vs_NP"]=="OPEN" and r["malformed_rejections"]==6)
 print(json.dumps({"verified":True,"independent_assertion_groups":checks,"transition_rows":tot,"P_vs_NP":"OPEN"},sort_keys=True))
if __name__=="__main__":main()
