#!/usr/bin/env python3
"""Compact, standalone LSPV-1 320 directional-cofactor reproducer."""
import json
P9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
N9=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
P6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
N6=[(1,2,4),(1,3,6),(2,3,5),(4,5,6)]
def clauses(p,n,shift=0):return [(1,tuple(v+shift for v in c)) for c in p]+[(-1,tuple(v+shift for v in c)) for c in n]
def valid(n,cs):
 if 3*len(cs)!=4*n:return False
 counts={(i,s):0 for i in range(1,n+1) for s in (-1,1)};seen=set()
 for s,c in cs:
  if s not in (-1,1) or len(c)!=3 or len(set(c))!=3 or any(v<1 or v>n for v in c):return False
  key=(s,tuple(sorted(c)))
  if key in seen:return False
  seen.add(key)
  for v in c:counts[v,s]+=1
 return all(v==2 for v in counts.values())
def sat(cs,a):return all(any(((a>>(v-1))&1)==(s==1) for v in c) for s,c in cs)
def check(n,cs,x):
 assert valid(n,cs)
 pos=[set(c)-{x} for s,c in cs if s==1 and x in c]
 neg=[set(c)-{x} for s,c in cs if s==-1 and x in c]
 assert len(pos)==len(neg)==2
 d={k:0 for k in ('f0','f1','only0','only1','both','T0a','T0b','T0overlap','T1a','T1b','T1overlap')}
 for z in range(1<<(n-1)):
  a0=(z&((1<<(x-1))-1))|((z>>(x-1))<<x);a1=a0|(1<<(x-1))
  s0=sat(cs,a0);s1=sat(cs,a1)
  d['f0']+=s0;d['f1']+=s1;d['both']+=s0 and s1
  u=[s0 and all((a0>>(v-1))&1 for v in c) for c in neg]
  v=[s1 and all(not ((a1>>(w-1))&1) for w in c) for c in pos]
  assert (s0 and not s1)==any(u) and (s1 and not s0)==any(v)
  d['only0']+=s0 and not s1;d['only1']+=s1 and not s0
  for prefix,values in [('T0',u),('T1',v)]:
   d[prefix+'a']+=values[0];d[prefix+'b']+=values[1]
   d[prefix+'overlap']+=all(values)
 assert d['only0']==d['T0a']+d['T0b']-d['T0overlap']
 assert d['only1']==d['T1a']+d['T1b']-d['T1overlap']
 return d
if __name__=='__main__':
 f=clauses(P9,N9);y=clauses(P6,N6);h=f+clauses(P6,N6,9)
 result={'F9':check(9,f,1),'Y6':check(6,y,1),'H15':check(15,h,10)}
 assert (result['F9']['only0'],result['F9']['only1'])==(28,18)
 assert (result['Y6']['only0'],result['Y6']['only1'])==(6,6)
 assert (result['H15']['only0'],result['H15']['only1'])==(420,420)
 p={3:0,5:1,6:0,7:0,8:0}
 branches=[]
 for b in (0,1):
  fixed={**p,1:b};free=[v for v in range(1,10) if v not in fixed]
  count=0
  for z in range(1<<len(free)):
   a=sum(v<<(i-1) for i,v in fixed.items())
   a+=sum(((z>>j)&1)<<(i-1) for j,i in enumerate(free))
   count+=sat(f,a)
  branches.append(count)
 assert branches==[2,0]
 result['F9_same_original_branch_models']=branches
 result['model_counts']={name:sum(sat(cs,a) for a in range(1<<n)) for name,n,cs in [('F9',9,f),('Y6',6,y),('H15',15,h)]}
 assert result['model_counts']=={'F9':70,'Y6':20,'H15':1400}
 print(json.dumps(result,sort_keys=True,indent=2))
