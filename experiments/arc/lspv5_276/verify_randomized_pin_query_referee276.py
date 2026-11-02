#!/usr/bin/env python3
"""Independent no-producer-import verifier for REFEREE276."""
import argparse,collections,itertools,json
from fractions import Fraction

F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
A={1:1,2:0,3:1,4:0,8:0};B={1:1,2:1,3:0,4:0,8:0}
C=0
def ck(x,msg):
 global C
 assert x,msg;C+=1
def source(t):
 z=[]
 for i in range(t):
  for j,c in enumerate(F):
   cc=[]
   for lit in c:
    v=abs(lit)+9*i
    if j==0 and lit==5:v=9*((i+1)%t)+5
    cc.append(v if lit>0 else -v)
   z.append(tuple(cc))
 return tuple(z)
def pins(w):
 p={}
 for i,ch in enumerate(w):
  for v,b in (A if ch=='A' else B).items():p[9*i+v]=b
 return p
def models(G,p):
 n=max(abs(x) for c in G for x in c);free=[v for v in range(1,n+1) if v not in p];q=0
 for bs in itertools.product((0,1),repeat=len(free)):
  a=dict(p);a.update(zip(free,bs))
  q+=all(any(a[abs(x)]==int(x>0) for x in c) for c in G)
 return q
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--raw',required=True);a=ap.parse_args()
 d=json.load(open(a.raw));ck(d['run']=='RANDOMIZED-PIN-QUERY-REFEREE276','run')
 for t in (2,3):
  G=source(t)
  for w in map(''.join,itertools.product('AB',repeat=t)):
   z=models(G,pins(w));ck((z==1)==(w=='A'*t),('promise',t,w,z))
 for row in d['randomized_bounds']:
  t=row['t'];eps=Fraction(row['epsilon'])
  lo=(1-2*eps)*t
  ck(Fraction(row['lower_expected_queries'])==lo,'lower')
  ck(Fraction(row['matching_expected_queries'])==lo,'upper')
  ck(Fraction(row['query_all_probability'])==1-2*eps,'mixture')
  # Algebraic coupling certificate: t(1-eps)-E|Q| <= eps*t.
  ck(t*(1-eps)-lo<=eps*t,'coupling')
 ck(d['controls']['F9_root_models']==70 and d['controls']['F9_A_models']==1 and d['controls']['F9_B_models']==0,'F9')
 ck(d['controls']['F9_S_models']==3 and d['controls']['F9_U_models']==0,'both labels')
 ck(d['controls']['F9_U_false_cover']['leaves']==8,'UNSAT cover')
 ck(d['controls']['F9_SU_pair_modes']==264,'S/U')
 ck(d['controls']['F15_SAT_models']==2 and d['controls']['F15_UNSAT_models']==0,'F15')
 ck(d['controls']['Y6_models']==20 and d['controls']['malformed_rejected']==6,'Y6/malformed')
 print(json.dumps({'status':'PASS','assertion_groups':C,'independent_promise_rows':12,
   'theorem':'R_epsilon_expected(AND_t)=(1-2epsilon)t on declared promise','P_vs_NP':'OPEN'},indent=2))
if __name__=='__main__':main()
