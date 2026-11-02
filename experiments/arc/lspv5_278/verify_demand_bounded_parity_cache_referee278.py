#!/usr/bin/env python3
"""No-producer-import verifier for REFEREE278."""
import argparse,itertools,json,random
from fractions import Fraction
C=0
def ck(x,m):
 global C
 assert x,m;C+=1
def bit(r,z):return ((1072*r+4*(r-z.bit_count()))>>2)&1
def cached(r,z):return (r&1)^(z.bit_count()&1)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--raw',required=True);ap.add_argument('--out');a=ap.parse_args()
 d=json.load(open(a.raw));ck(d['run']=='DEMAND-BOUNDED-PARITY-CACHE-REFEREE278','run')
 variants=flips=0
 for r in range(1,11):
  for z in range(1<<r):
   ck(bit(r,z)==cached(r,z),('cache',r,z))
   for i in range(r):ck(bit(r,z)!=bit(r,z^(1<<i)),('flip',r,z,i));flips+=1
   variants+=1
 for row in d['randomized_bounds']:
  r=row['r'];e=Fraction(row['epsilon']);v=(1-2*e)*r
  ck(Fraction(row['lower_expected_width_queries'])==v,'lower');ck(Fraction(row['matching_expected_width_queries'])==v,'upper')
  ck(Fraction(row['query_all_probability'])==1-2*e,'mix')
 rng=random.Random(9278);reconstruct=0
 for r in range(1,200):
  for _ in range(4):
   z=[rng.randrange(2) for _ in range(r)];p=[];x=0
   for b in z:x^=b;p.append(x)
   zz=[p[0]]+[p[i]^p[i-1] for i in range(1,r)]
   ck(zz==z,'all-prefix injective');reconstruct+=r
 for row in d['amortized_work']:
  ck(row['stateless_source_probes']==row['r']*row['repeated_queries'],'stateless')
  ck(row['cached_source_probes']==row['r'] and row['retained_semantic_bits']==1,'cache')
 c=d['controls'];ck((c['F9_models'],c['Y6_models'],c['F15_models'])==(70,20,1032),'roots')
 ck((c['F9_SAT_models'],c['F9_UNSAT_models'],c['F9_UNSAT_cover_leaves'])==(3,0,8),'F9 labels')
 ck((c['F15_SAT_models'],c['F15_UNSAT_models'])==(2,0),'F15 labels')
 ck(c['F9_SU_modes']==264 and c['malformed_rejected']==6,'S/U malformed')
 out={'status':'PASS','assertion_groups':C,'independent_variants':variants,'independent_flips':flips,
      'reconstructed_prefix_bits':reconstruct,'theorem':'one paid parity bit suffices for repeated fixed-pivot address queries; all-prefix table is r-bit injective','scope':'restricted source-layout query theorem','P_vs_NP':'OPEN'}
 if a.out:open(a.out,'w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
