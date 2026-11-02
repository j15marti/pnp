#!/usr/bin/env python3
"""Independent verifier for REFEREE277; deliberately imports no producer."""
import argparse,itertools,json,math,random

C=0
def ck(x,msg):
 global C
 assert x,msg;C+=1
def lg(x):return max(1,(x-1).bit_length())
def make(w):
 m=len(w);L=lg(m+1);S=L*L;b=L;p=[0]
 for x in w:p.append(p[-1]+x)
 G={s:p[s] for s in range(0,m+1,S)};R={}
 for s in range(0,m+1,S):
  for u in range(s,min(s+S,m)+1,b):R[u]=p[u]-p[s]
 return L,S,b,G,R
def ask(w,d,j):
 L,S,b,G,R=d;m=len(w);s=(j//S)*S
 if s not in G:s=((j-1)//S)*S
 u=s+((j-s)//b)*b
 if u not in R:u=s+((j-s-1)//b)*b
 return G[s]+R[u]+sum(w[u:j]),j-u
def row(m):
 L=lg(m+1);S=L*L;b=L;ng=len(range(0,m+1,S))
 nr=sum(len(range(s,min(s+S,m)+1,b)) for s in range(0,m+1,S))
 bits=ng*L+nr*lg(S+1)
 return bits,b-1
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--raw',required=True);ap.add_argument('--out');a=ap.parse_args()
 d=json.load(open(a.raw));ck(d['run']=='HIERARCHICAL-RANK-REFEREE277','run')
 vectors=queries=0
 for m in range(13):
  for w in itertools.product((0,1),repeat=m):
   q=make(w);pref=0
   for j in range(m+1):
    got,probes=ask(w,q,j);ck(got==pref,('rank',m,w,j,got,pref));ck(probes<=q[0]-1,'probes')
    queries+=1
    if j<m:pref+=w[j]
   vectors+=1
 rng=random.Random(991)
 for m in (31,64,127,256,1024):
  for w in ([0]*m,[1]*m,[i&1 for i in range(m)],[rng.randrange(2) for _ in range(m)]):
   q=make(w)
   for j in list(range(min(m+1,70)))+[m//2,m-1,m]:
    got,probes=ask(w,q,j);ck(got==sum(w[:j]),'random');ck(probes<=q[0]-1,'random probes')
 for x in d['asymptotic_rows']:
  bits,probes=row(x['m']);ck(bits==x['two_directory_bits'],'bits');ck(probes==x['two_worst_source_probes'],'bound')
 c=d['controls'];ck((c['F9_root_models'],c['F9_A_models'],c['F9_B_models'])==(70,1,0),'F9')
 ck((c['F9_S_models'],c['F9_U_models'],c['F9_U_false_cover_leaves'])==(3,0,8),'labels')
 ck((c['Y6_models'],c['F15_SAT_models'],c['F15_UNSAT_models'])==(20,2,0),'Y6/F15')
 ck(c['F9_SU_pair_modes']==264 and c['malformed_rejected']==6,'S/U/malformed')
 out={'status':'PASS','assertions':C,'independent_vectors':vectors,'independent_queries':queries,
      'theorem':'two-level exact rank: O(m loglogm/logm) directory bits and O(logm) source probes in declared random-access model',
      'scope':'restricted upper bound; no sequential-tape or FLMV transfer','P_vs_NP':'OPEN'}
 if a.out:open(a.out,'w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
