#!/usr/bin/env python3
"""Independent source-only U198 critical-port and same-source H SAT/UNSAT verifier.
No producer import. Can be run in j15marti/pnp checkout. Exact search cost varies.
"""
import ast
from pathlib import Path
from itertools import product
ROOT=Path(__file__).resolve().parents[3]
UFILE=ROOT/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt'
D_WITNESS='010100010101000010000001110010101101010101010000100000001100111001011001010101001000000111001011000001000100001110101011000001111100100001000011101010000100001111000100010000111010100011000110001000'
F9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]]
H=[[1,2],[5,3],[6,8]]+F9[2:]
def sat(cs,b):return all(any((b[abs(x)-1]=='1')==(x>0) for x in c) for c in cs)
def red(cs,l):return [[x for x in c if x!=-l] for c in cs if l not in c]
nodes=0
def dpll(cs):
 global nodes
 nodes+=1
 while cs:
  if any(not c for c in cs):return False
  u=next((c[0] for c in cs if len(c)==1),None)
  if u is None:break
  cs=red(cs,u)
 if not cs:return True
 x=cs[0][0]
 return dpll(red(cs,x)) or dpll(red(cs,-x))
def main():
 s=UFILE.read_text();U=ast.literal_eval('\n'.join(z for z in s.splitlines() if not z.startswith('#')))
 assert len(U)==264 and U[1]==[194,196,197] and len(D_WITNESS)==198
 assert sat(U[:1]+U[2:],D_WITNESS) and all(D_WITNESS[x-1]=='0' for x in U[1])
 mods=[]
 for i in range(6):
  lo=1+32*i;hi=lo+31
  part=[c for c in U[2:254] if any(lo<=abs(x)<=hi for x in c)]
  assert len(part)==42 and all(all(lo<=abs(x)<=hi or abs(x)>=193 for x in c) for c in part)
  mods.append(part)
 direct=refuted=calls=0
 for mask in range(64):
  p={193+j:(mask>>j)&1 for j in range(6)}
  if any(all(p[abs(x)]!=int(x>0) for x in c) for c in U[:2]):direct+=1;continue
  found=False
  for part in mods:
   calls+=1
   z=[[x for x in c if abs(x)<193] for c in part
      if not any(abs(x)>=193 and p[abs(x)]==int(x>0) for x in c)]
   if not dpll(z):found=True;break
  assert found
  refuted+=1
 assert (direct,refuted,calls)==(16,48,152)
 S={1:0,2:1,3:0,4:0,5:1};B={i:0 for i in range(1,6)}
 totals=[0,0]
 for m in range(512):
  a=''.join(str((m>>i)&1) for i in range(9))
  if sat(H,a):
   totals[0]+=all(int(a[v-1])==p for v,p in S.items())
   totals[1]+=all(int(a[v-1])==p for v,p in B.items())
 assert totals==[6,0]
 assert sum(sat(H,''.join(str((m>>i)&1) for i in range(9))) for m in range(512))==37
 assert sum(sat(F9,''.join(str((m>>i)&1) for i in range(9))) for m in range(512))==70
 print({'status':'PASS','U198_direct':direct,'U198_modular':refuted,
        'U198_module_calls':calls,'UP_DPLL_nodes':nodes,'H_SAT_cube':6,'H_UNSAT_cube':0,
        'U198_original_clause_refuted':True,'P_vs_NP':'OPEN'})
if __name__=='__main__':main()
