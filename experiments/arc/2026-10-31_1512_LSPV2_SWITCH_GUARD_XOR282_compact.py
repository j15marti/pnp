#!/usr/bin/env python3
"""Compact source-based check for LSPV-2 SWITCH-GUARD-XOR282.
Run: python this_script.py research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt
The complete 528168-event physical producer/verifier is in the archived ZIP.
"""
import ast,collections,itertools,sys,json
Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]
W='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
def ok(f):
 n=max(abs(z) for c in f for z in c);h=collections.Counter((abs(z),z>0) for c in f for z in c)
 return 3*len(f)==4*n and len({tuple(sorted(c)) for c in f})==len(f) and all(len(c)==3 and len({abs(z) for z in c})==3 and len({z>0 for z in c})==1 for c in f) and all(h[v,s]==2 for v in range(1,n+1) for s in (0,1))
def sat(f,a):return all(any(bool(a[abs(z)-1])==(z>0) for z in c) for c in f)
def switch(f,j,k,p,q):
 g=[c[:] for c in f];g[j][p],g[k][q]=g[k][q],g[j][p];return g
def guard(f,j,k,p,q,a):
 def lit(z):return bool(a[abs(z)-1])==(z>0)
 x,y=f[j][p],f[k][q]
 A=any(lit(z) for t,z in enumerate(f[j]) if t!=p)
 B=any(lit(z) for t,z in enumerate(f[k]) if t!=q)
 R=all(any(lit(z) for z in c) for i,c in enumerate(f) if i not in (j,k))
 return R and (lit(x)!=lit(y)) and (A!=B)
def enc(f):
 n=max(abs(z) for c in f for z in c)
 def gam(a):
  b=format(a,'b');return '0'*(len(b)-1)+b
 return gam(n)+gam(len(f))+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(z),'0%db'%n.bit_length()) for z in c) for c in f)
assert ok(Y)
cnt=0
for j,k in itertools.combinations(range(8),2):
 if (Y[j][0]>0)!=(Y[k][0]>0):continue
 for p,q in itertools.product(range(3),repeat=2):
  if Y[j][p]==Y[k][q]:continue
  g=switch(Y,j,k,p,q)
  if not ok(g):continue
  cnt+=1
  for i in range(64):
   a=[i>>v&1 for v in range(6)]
   assert (sat(Y,a)!=sat(g,a))==guard(Y,j,k,p,q,a)
assert cnt==48
text=open(sys.argv[1]).read();u=ast.literal_eval(text[text.index('[['):]);assert ok(u)
v=switch(u,2,44,u[2].index(197),u[44].index(196));assert ok(v)
a=[int(z) for z in W]
assert len(a)==198 and sat(v,a) and not sat(u,a)
assert guard(u,2,44,u[2].index(197),u[44].index(196),a)
d=[i for i,(x,y) in enumerate(zip(enc(u),enc(v))) if x!=y]
assert d==[106,1156]
for f in (u,v):
 g=[[-z for z in c] for c in f];assert ok(g) and len(enc(f))==len(enc(g))
 assert sum(a!=b for a,b in zip(enc(f),enc(g)))==264
 c=switch(f,3,4,f[3].index(-3),f[4].index(-4))
 assert ok(c) and sorted(map(lambda r:tuple(sorted(r)),f))==sorted(map(lambda r:tuple(sorted(r)),c))
 assert sum(a!=b for a,b in zip(enc(f),enc(c)))==6
for f in (Y,u,v):
 n=max(abs(z) for c in f for z in c)
 for assignment in ([0]*n,[1]*n):
  t=[sum((assignment[abs(z)-1]==1)==(z>0) for z in cl) for cl in f]
  assert sum(t)==2*n
print(json.dumps({'status':'PASS','legal_Y6_switches':cnt,'Y6_assignment_checks':cnt*64,'U_V_different_encoded_positions':d,'safe_permutation_edit_bits':6,'safe_complement_edit_bits':264,'V_source_witness':'PASS','U_source_witness':'FAILS, UNSAT separately certified','ARC_and_P_vs_NP':'OPEN'},indent=2))
