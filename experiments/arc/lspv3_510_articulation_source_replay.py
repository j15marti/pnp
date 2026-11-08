#!/usr/bin/env python3
"""LSPV3/510 independent component criterion versus GF(2) original-clause deletion replay."""
import json

def graphs():
  k4=[(i,j) for i in range(4) for j in range(i+1,4)]
  k33=[(i,j) for i in range(3) for j in range(3,6)]
  cube=[(i,i^(1<<b)) for i in range(8) for b in range(3) if i<(i^(1<<b))]
  prism=[(i,(i+1)%6) for i in range(6)]+[(i+6,(i+1)%6+6) for i in range(6)]+[(i,i+6) for i in range(6)]
  def sub(k):
    return ([(k+i,k+j) for i in range(4) for j in range(i+1,4) if (i,j)!=(0,1)]+[(k,k+4),(k+1,k+4)],k+4)
  a,u=sub(0);b,v=sub(5)
  bridge=a+b+[(u,v)]
  star=[]
  for t in range(3):
    e,p=sub(1+5*t);star+=e+[(0,p)]
  return [('K4',4,k4),('K33',6,k33),('cube',8,cube),('prism6',12,prism),('bridge',10,bridge),('three_branch',16,star)]

def comps(n,edges,v):
  adj=[[] for _ in range(n)]
  for a,b in edges:
    if v not in (a,b):adj[a].append(b);adj[b].append(a)
  remaining=set(range(n))-{v};out=[]
  while remaining:
    stack=[remaining.pop()];C=set(stack)
    while stack:
      for y in adj[stack.pop()]:
        if y in remaining:remaining.remove(y);C.add(y);stack.append(y)
    out.append(C)
  return out

def solve(E,eqs):
  base={}
  for mask,rhs in eqs:
    while mask:
      k=(mask&-mask).bit_length()-1
      if k not in base:base[k]=(mask,rhs);break
      m,b=base[k];mask^=m;rhs^=b
    else:
      if rhs:return None
  a=[0]*E
  for k in sorted(base,reverse=True):
    m,b=base[k]
    a[k]=b^(sum(a[j] for j in range(k+1,E) if m>>j&1)%2)
  return a

def run():
  result=[];deletions=0;witnesses=0
  for name,n,edges in graphs():
    edges=[tuple(sorted(x)) for x in edges]
    inc=[[i for i,e in enumerate(edges) if v in e] for v in range(n)]
    assert len(edges)*2==n*3 and all(len(x)==3 for x in inc)
    assert len(comps(n,edges,-1))==1
    for charge_at in (0,1):
      charges=[int(v==charge_at) for v in range(n)]
      cs=[comps(n,edges,v) for v in range(n)];counts=[0]*n
      source=[]
      for v in range(n):
        for pat in range(8):
          bs=[pat>>j&1 for j in range(3)]
          if bs[0]^bs[1]^bs[2]==charges[v]:continue
          source.append((v,pat,[(-1 if bs[j] else 1)*(inc[v][j]+1) for j in range(3)]))
      assert len(source)==4*n
      for index,(v,pat,cl) in enumerate(source):
        pins={edge:pat>>j&1 for j,edge in enumerate(inc[v])}
        predicted=all((sum(charges[z] for z in C)&1)==(sum(pins[e] for e,(a,b) in enumerate(edges) if (a==v and b in C) or (b==v and a in C))&1) for C in cs[v])
        eqs=[(1<<e,b) for e,b in pins.items()]+[(sum(1<<e for e in inc[z]),charges[z]) for z in range(n) if z!=v]
        a=solve(len(edges),eqs)
        assert (a is not None)==predicted
        if a is not None:
          assert not any(a[abs(l)-1]==int(l>0) for l in cl)
          assert all(j==index or any(a[abs(l)-1]==int(l>0) for l in row) for j,(_,__,row) in enumerate(source))
          counts[v]+=1;witnesses+=1
        deletions+=1
      assert all(counts[v]==1<<(3-len(cs[v])) for v in range(n))
      result.append(dict(name=name,charge_vertex=charge_at,clauses=4*n,essential=sum(counts),components=[len(x) for x in cs]))
  print(json.dumps(dict(version='LSPV3/510',cases=result,clauses_checked=deletions,valid_deletion_witnesses=witnesses,model='source deletion GF2 independent of component test',historical_full_mixed='OPEN'),indent=2))
if __name__=='__main__':run()
