#!/usr/bin/env python3
"""GATE306 compact, original-clause checked, standard-library only.
Only a restricted source theorem and finite tests, not a polynomial P=NP solver.
Full independent no-import verifier and full raw data are in the GATE306 archive.
"""
import itertools, collections, json, math
P6=['123','145','246','356']; Q6=['124','136','235','456']
P9=['156','238','135','469','247','789']; Q9=['468','167','234','358','129','579']
def cnf(P,Q):
 return [tuple(map(int,c)) for c in P]+[tuple(-int(x) for x in c) for c in Q]
def sat(F,a):
 return all(any(((a>>(abs(l)-1))&1)==int(l>0) for l in C) for C in F)
def validate(F,n):
 if not F or 3*len(F)!=4*n:return False
 if any(len(C)!=3 or len({abs(x) for x in C})!=3 or len({x>0 for x in C})!=1 or any(abs(x)>n or x==0 for x in C) for C in F):return False
 if len({tuple(sorted(C)) for C in F})!=len(F):return False
 cnt=collections.Counter((abs(x),x>0) for C in F for x in C)
 return all(cnt[x,True]==cnt[x,False]==2 for x in range(1,n+1))
def pins(F,n,p):
 free=[i for i in range(1,n+1) if i not in p]
 vals=[]
 for bits in itertools.product((0,1),repeat=len(free)):
  a=sum(v<<(i-1) for i,v in p.items())+sum(v<<(i-1) for i,v in zip(free,bits))
  if sat(F,a):vals.append(a)
 return vals
def main():
 F=cnf(P9,Q9);Y=cnf(P6,Q6)
 assert validate(F,9) and validate(Y,6)
 m=[a for a in range(512) if sat(F,a)]
 s={1:1,2:0,5:1,6:1};u={8:0,3:0,7:0,6:0,1:1,5:1}
 ps=pins(F,9,s);pu=pins(F,9,u)
 assert len(m)==70 and ps==[317] and not pu
 assert not any(all(abs(l) in s and s[abs(l)]!=int(l>0) for l in C) for C in F)
 assert not any(all(abs(l) in u and u[abs(l)]!=int(l>0) for l in C) for C in F)
 triples=list(itertools.combinations(range(1,7),3))
 families=[a for a in itertools.combinations(triples,4) if all(sum(i in C for C in a)==2 for i in range(1,7))]
 assert len(families)==75
 hist=collections.Counter()
 for p in families:
  for q in families:
   G=list(p)+[tuple(-x for x in C) for C in q]
   assert validate(G,6)
   n=sum(sat(G,a) for a in range(64))
   assert any(sat(G,a) for a in range(64) if a.bit_count()==3)
   hist[n]+=1
 assert len([a for a in range(64) if sat(Y,a)])==20
 assert hist=={18:450,19:240,20:1080,21:1440,22:1650,24:720,26:45}
 print(json.dumps({'run':'GATE306','n6_valid_sources':5625,'n6_assignment_checks':360000,'n6_model_histogram':hist,'F9_models':70,'F9_weights':dict(collections.Counter(a.bit_count() for a in m)),'F9_pinned_SAT':ps,'F9_pinned_UNSAT':pu,'central_Witness_theorem':'exact on valid originals, not pinned residuals','P_vs_NP':'OPEN'},indent=2))
if __name__=='__main__':main()
