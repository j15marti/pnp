#!/usr/bin/env python3
"""LSPV-4 336 source-only exact finite checks; NO FLMV native time claim."""
import json
from itertools import combinations
from collections import Counter
Z6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6)]
F9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]
def valid(f,n):
 if n%3 or len(f)*3!=4*n:return False
 p=[0]*n;q=[0]*n;seen=set()
 for c in f:
  if len(c)!=3 or any(type(x)!=int or x==0 or abs(x)>n for x in c) or len({abs(x) for x in c})!=3:return False
  if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
  if tuple(sorted(c)) in seen:return False
  seen.add(tuple(sorted(c)))
  for x in c:(p if x>0 else q)[abs(x)-1]+=1
 return all(v==2 for v in p+q)
def clause(c,a):return any(bool(a>>(abs(x)-1)&1)==(x>0) for x in c)
def sat(f,a):return all(clause(c,a) for c in f)
def guard_table(g,d,p):
 n=max(abs(x) for c in g for x in c);D=g[d];v=D[p];tail=[D[j] for j in range(3) if j!=p];H=g[:d]+g[d+1:];W=[[0,0],[0,0]]
 for a in range(1<<n):
  if not sat(H,a):continue
  i=int(bool(a>>(abs(v)-1)&1)==(v>0))
  j=int(any(bool(a>>(abs(x)-1)&1)==(x>0) for x in tail))
  W[i][j]+=1
 return W
def six_audit():
 n=6;triples=list(combinations(range(n),3))
 shapes=[p for p in combinations(triples,4) if all(sum(i in c for c in p)==2 for i in range(n))]
 assert len(shapes)==75
 B=[sum(1<<a for a in range(64) if a>>i&1) for i in range(n)]
 allbits=(1<<64)-1
 cp={c:B[c[0]]|B[c[1]]|B[c[2]] for c in triples}
 cn={c:allbits^(B[c[0]]&B[c[1]]&B[c[2]]) for c in triples}
 hist=Counter();whist=Counter();ports=0
 for P in shapes:
  for M in shapes:
   pos=[cp[c] for c in P];neg=[cn[c] for c in M];F=allbits
   for mask in pos+neg:F &=mask
   hist[F.bit_count()]+=1
   for s,groups in ((1,P),(-1,M)):
    for j,triple in enumerate(groups):
     H=allbits
     for k,mask in enumerate(pos):
      if s!=1 or k!=j:H &=mask
     for k,mask in enumerate(neg):
      if s!=-1 or k!=j:H &=mask
     for v in triple:
      tail=[i for i in triple if i!=v]
      vm=B[v] if s==1 else allbits^B[v]
      bm=(B[tail[0]]|B[tail[1]]) if s==1 else (allbits^B[tail[0]])|(allbits^B[tail[1]])
      whist[(H&vm&bm).bit_count()]+=1;ports+=1
 assert ports==135000 and min(whist)==4 and hist[18]==450
 return {'shapes':len(shapes),'pairs':len(shapes)**2,'ports':ports,'model_histogram':dict(sorted(hist.items())),'W11_histogram_both_signs':dict(sorted(whist.items())),'min_W11':min(whist)}
def lifted():
 G=[list(c) for c in F9];K=[[int((1 if x>0 else -1)*(abs(x)+9)) for x in c] for c in Z6]
 Q=G+K;Q[0][0],Q[12][0]=Q[12][0],Q[0][0]
 assert valid(Q,15)
 rows=[]
 for v in (0,1):
  source=deleted=lifted=0;bad_clause=[]
  fixed={1:v,2:0,4:0,6:0}
  for j,c in enumerate(F9):
   if all(abs(x) in fixed and bool(fixed[abs(x)])!=(x>0) for x in c):bad_clause.append(j+1)
  for a in range(512):
   if any((a>>(i-1)&1)!=u for i,u in fixed.items()):continue
   source+=sat(F9,a);deleted+=sat(F9[1:],a)
   for b in range(64):lifted+=sat(Q,a|(b<<9))
  rows.append({'x1':v,'source':source,'deleted_C1':deleted,'lifted':lifted,'empty_pinned_original_clauses':bad_clause})
 assert [(r['source'],r['deleted_C1'],r['lifted']) for r in rows]==[(0,2,12),(3,3,27)]
 assert all(not r['empty_pinned_original_clauses'] for r in rows)
 return rows
def obdd():
 n=9;t=[int(sat(F9,a)) for a in range(1<<n)];edge={}
 for S in range(1<<n):
  used=[i for i in range(n) if S>>i&1];free=[i for i in range(n) if not S>>i&1];cof=set()
  for a in range(1<<len(used)):
   k=sum(((a>>j)&1)<<i for j,i in enumerate(used));f=0
   for b in range(1<<len(free)):
    x=k|sum(((b>>j)&1)<<i for j,i in enumerate(free));f|=t[x]<<b
   cof.add(f)
  for j,i in enumerate(free):
   edge[(S,i)]=sum(any(((f>>b)&1)!=((f>>(b|(1<<j)))&1) for b in range(1<<len(free)) if not (b>>j&1)) for f in cof)
 def optimal(minim):
  d={0:(0,[])}
  for S in range(512):
   if S not in d:continue
   cost,order=d[S]
   for i in range(n):
    if S>>i&1:continue
    q=S|(1<<i);value=cost+edge[S,i]
    if q not in d or ((value<d[q][0]) if minim else (value>d[q][0])):d[q]=(value,order+[i+1])
  return d[511]
 mi=optimal(True);ma=optimal(False);natural=sum(edge[((1<<i)-1,i)] for i in range(n))
 assert (mi[0],natural,ma[0])==(52,66,80)
 return {'minimum':mi,'natural':natural,'maximum':ma,'transition_edges':len(edge)}
def main():
 assert valid(Z6,6) and valid(F9,9)
 W=guard_table(Z6,0,0);assert W==[[4,9],[3,6]]
 E=[[W[1][1],W[0][1]+W[1][1]],[W[1][0]+W[1][1],sum(map(sum,W))]]
 assert E==[[6,15],[9,22]]
 malformed=[Z6+[Z6[0]],Z6[:-1],[(1,-2,3)]+Z6[1:],[(1,1,3)]+Z6[1:],[(0,2,3)]+Z6[1:],[(1,2,7)]+Z6[1:]]
 assert all(not valid(f,6) for f in malformed)
 out={'status':'PROVED/EXACT abstract identity; COMPUTATIONAL finite checks; P vs NP OPEN','W':W,'E':E,'six_guard_census':six_audit(),'F9_models':sum(sat(F9,a) for a in range(512)),'F9_W11_range':[min(guard_table(F9,i,j)[1][1] for i in range(12) for j in range(3)),max(guard_table(F9,i,j)[1][1] for i in range(12) for j in range(3))],'F9_pins_x2_x4_x6_0':lifted(),'F9_OBDD':obdd(),'malformed_rejected':len(malformed),'flmv_native_traces':'NOT EXECUTED'}
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
