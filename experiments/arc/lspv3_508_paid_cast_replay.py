#!/usr/bin/env python3
"""LSPV-3/508 concise independent executable. Separate R_CAST507(w), not native R_mix341."""
import itertools, json
G={
 'K4':(4,[(i,j) for i in range(4) for j in range(i+1,4)]),
 'K33':(6,[(i,j) for i in range(3) for j in range(3,6)]),
 'cube':(8,[(i,j) for i in range(8) for j in range(i+1,8) if (i^j).bit_count()==1])}
def norm(xs):return tuple(sorted(set(xs),key=lambda x:(abs(x),x<0)))
def evaluate(c,a):return any(a[abs(x)-1]==(x>0) for x in c)
def construct(graph,k,w):
 h,edges=G[graph];n=len(edges);assert 2*n==3*h and 0<=k<=4*h and w>=1
 original=[];groups=[]
 for v in range(h):
  idx=[i+1 for i,e in enumerate(edges) if v in e]; assert len(idx)==3
  group=[]
  for bits in itertools.product((0,1),repeat=3):
   if sum(bits)%2!=(v==0):
    group.append(len(original));original.append(norm((-x if b else x for x,b in zip(idx,bits))))
  groups.append(group)
 sources=[]; mapping={};gadgets=[]
 for j,C in enumerate(original):
  if j>=k:
   mapping[j]=len(sources);sources.append(C);continue
  u=n+2*j+1;v=u+1;a,b,c=C
  A=norm((a,b,u));B=norm((-u,c,v));D=norm((-u,c,-v))
  ids=(len(sources),len(sources)+1,len(sources)+2)
  sources.extend([A,B,D]);gadgets.append((j,C,ids,u,v))
 nodes=[dict(kind='SOURCE',clause=list(C),cost=0) for C in sources]
 def add(kind,parents,**attrs):
  i=len(nodes);nodes.append(dict(kind=kind,parents=parents,cost=w if kind=='CAST' else 1,**attrs));return i
 for j,C,(iA,iB,iD),u,v in gadgets:
  r=add('RES',[iB,iD],pivot=v,clause=list(norm((-u,C[2]))))
  r=add('RES',[iA,r],pivot=u,clause=list(C))
  mapping[j]=add('CAST',[r],clause=list(C))
 parity=[]
 for g in groups:
  a,b,c,d=[mapping[j] for j in g]
  left=add('AND3',[a,b]);right=add('AND3',[c,d]);parity.append(add('AND3',[left,right]))
 while len(parity)>1:
  parity=[add('XOR',parity[t:t+2]) if t+1<len(parity) else parity[t] for t in range(0,len(parity),2)]
 return sources,n,nodes,parity[0]
def check(sources,n,nodes,root,w):
 slots=[];depth=[]
 for i,v in enumerate(nodes):
  typ=v['kind'];parents=v.get('parents',[])
  if typ=='SOURCE':
   assert i<len(sources) and v['cost']==0 and norm(v['clause'])==sources[i]
   slots.append(('f',frozenset(map(abs,sources[i])),lambda a,C=sources[i]:evaluate(C,a),None));depth.append(0);continue
  assert all(isinstance(j,int) and 0<=j<i for j in parents)
  depth.append(max(depth[j] for j in parents)+v['cost'])
  if typ=='RES':
   assert v['cost']==1 and len(parents)==2 and all(nodes[j]['kind'] in ('SOURCE','RES') for j in parents)
   A,B=[norm(nodes[j]['clause']) for j in parents];p=v['pivot']
   assert (p in A and -p in B) or (-p in A and p in B)
   C=norm(x for row in (A,B) for x in row if abs(x)!=p)
   assert all(-x not in C for x in C) and norm(v['clause'])==C
   slots.append(('r',None,None,None))
  elif typ=='CAST':
   assert len(parents)==1 and v['cost']==w and nodes[parents[0]]['kind']=='RES'
   C=norm(v['clause']);assert C==norm(nodes[parents[0]]['clause']) and len(set(map(abs,C)))<=3 and max(map(abs,C))<=n
   slots.append(('f',frozenset(map(abs,C)),lambda a,C=C:evaluate(C,a),None))
  elif typ=='AND3':
   assert v['cost']==1 and len(parents)==2 and all(slots[j][0]=='f' for j in parents)
   p,q=[slots[j] for j in parents];support=p[1]|q[1];assert len(support)<=3 and max(support)<=n
   def val(a,fp=p[2],fq=q[2]):return fp(a) and fq(a)
   row=None
   if len(support)==3:
    for rhs in (0,1):
     truth=True
     for bits in itertools.product((0,1),repeat=3):
      a=[False]*n
      for x,b in zip(sorted(support),bits):a[x-1]=bool(b)
      if val(a)!=(sum(bits)%2==rhs):truth=False;break
     if truth:row=(sum(1<<(x-1) for x in support),rhs)
   slots.append(('f',support,val,row))
  elif typ=='XOR':
   assert v['cost']==1 and len(parents)==2 and all(slots[j][3] is not None for j in parents)
   a,b=[slots[j][3] for j in parents];slots.append(('x',None,None,(a[0]^b[0],a[1]^b[1])))
  else:raise AssertionError(typ)
 assert slots[root][3]==(0,1)
 seen=set();stack=[root]
 while stack:
  i=stack.pop()
  if i in seen:continue
  seen.add(i);stack.extend(nodes[i].get('parents',[]))
 assert len(seen)==len(nodes)
 return sum(x['cost'] for x in nodes),depth[root],len(json.dumps(nodes,separators=(',',':')).encode())
def main():
 out=[];neg=0
 for graph,(h,_) in G.items():
  for k in sorted({0,1,2,h,4*h}):
   for w in (1,2,4):
    s,n,p,root=construct(graph,k,w);W,D,B=check(s,n,p,root,w)
    assert W==4*h+2*k-1+k*w and D<=(4+w+(h-1).bit_length() if k else 2+(h-1).bit_length())
    bad=json.loads(json.dumps(p));next(x for x in bad if x['kind']=='AND3')['parents']=[999999,0]
    try:check(s,n,bad,root,w);raise RuntimeError('BAD ACCEPTED')
    except AssertionError:neg+=1
    out.append(dict(graph=graph,h=h,k=k,w=w,work=W,span=D,bytes=B))
 print(json.dumps(dict(cases=out,corrupt_rejected=neg),indent=2))
if __name__=='__main__':main()
