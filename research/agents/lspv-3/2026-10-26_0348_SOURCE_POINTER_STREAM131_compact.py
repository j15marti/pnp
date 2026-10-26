#!/usr/bin/env python3
"""Independent compact audit for ADAPTIVE-SOURCE-POINTER-STREAM131.
Pure Python; source offsets authenticated against serialized DIMACS.
The theoretical streaming-bit-TM space claim is proved, not measured here.
"""
import collections,itertools,json
W='''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''
W1=[tuple(map(int,s.split())) for s in W.split(';')]
G=[(1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3)]
checks=0
def ck(v):
 global checks
 checks+=1
 assert v

def encode(C,n):
 s=f'p cnf {n} {len(C)}\n';loc=[]
 for c in C:
  loc.append(len(s));s+=' '.join(map(str,c))+' 0\n'
 return s,loc

def parsed(s):
 lines=s.splitlines(True);h=lines[0].split();n=int(h[2]);m=int(h[3])
 ck(h[:2]==['p','cnf'] and m==len(lines)-1)
 for row in lines[1:]:
  a=list(map(int,row.split()))
  ck(len(a)==4 and a[-1]==0 and len(set(map(abs,a[:-1])))==3 and all(0<abs(x)<=n for x in a[:-1]))
 return n

def source_clause(s,off):
 if off<=0 or off>=len(s) or s[off-1]!='\n':return None
 end=s.find('\n',off)
 if end<0:return None
 row=s[off:end].split()
 if len(row)!=4 or row[-1]!='0':return None
 try:return tuple(map(int,row[:3]))
 except ValueError:return None

def residue(c,a):
 if any(abs(x) in a and (x>0)==a[abs(x)] for x in c):return None
 return tuple(x for x in c if abs(x) not in a)

def edgelist(c):
 if len(c)==1:return [(-c[0],c[0])]
 if len(c)==2:return [(-c[0],c[1]),(-c[1],c[0])]
 return []

def leaf_certificate(s,C,loc,n,a):
 g=collections.defaultdict(list)
 for c,p in zip(C,loc):
  r=residue(c,a)
  if r==():return ('empty',p)
  if r is not None:
   for u,v in edgelist(r):g[u].append((v,p))
 def path(u,v):
  queue=collections.deque([u]);pre={u:None}
  while queue:
   t=queue.popleft()
   for z,p in g[t]:
    if z not in pre:pre[z]=(t,p);queue.append(z)
  if v not in pre:return None
  out=[];z=v
  while pre[z] is not None:
   t,p=pre[z];out.append((p,t,z));z=t
  return list(reversed(out))
 for x in range(1,n+1):
  if x in a:continue
  p=path(x,-x);q=path(-x,x)
  if p is not None and q is not None:return ('paths',x,p,q)
 return None

def source_verify(s,a,w,n):
 if w is None:return False
 if w[0]=='empty':
  c=source_clause(s,w[1]);return c is not None and residue(c,a)==()
 if w[0]!='paths':return False
 _,x,p,q=w
 if x in a or not 1<=x<=n:return False
 for segment,start,finish in ((p,x,-x),(q,-x,x)):
  if len(segment)>2*n-1:return False
  current=start
  for off,u,v in segment:
   c=source_clause(s,off)
   if c is None or u!=current or abs(u) in a or abs(v) in a:return False
   r=residue(c,a)
   if r is None or (u,v) not in edgelist(r):return False
   current=v
  if current!=finish:return False
 return True

def build(s,C,loc,n,branches,a=None):
 if a is None:a={}
 w=leaf_certificate(s,C,loc,n,a)
 if w is not None:return ('leaf',w)
 if not branches:return None
 v=branches[0]
 return ('branch',v,build(s,C,loc,n,branches[1:],{**a,v:False}),
                    build(s,C,loc,n,branches[1:],{**a,v:True}))

def validate(s,n,t,a=None):
 if a is None:a={}
 if t is None:return False
 if t[0]=='leaf':return source_verify(s,a,t[1],n)
 if t[0]!='branch' or len(t)!=4:return False
 _,v,left,right=t
 if v in a or not 1<=v<=n:return False
 return validate(s,n,left,{**a,v:False}) and validate(s,n,right,{**a,v:True})

def stats(t):
 if t is None:return (0,0,0,0)
 if t[0]=='leaf':
  w=t[1];return (1,1,0 if w[0]=='empty' else len(w[2])+len(w[3]),0)
 a=stats(t[2]);b=stats(t[3])
 return (a[0]+b[0],1+a[1]+b[1],a[2]+b[2],1+max(a[3],b[3]))

out={'run':'ADAPTIVE-SOURCE-POINTER-STREAM131-COMPACT','cases':[]}
for q in (1,2,4):
 C=[tuple((1 if x>0 else -1)*(abs(x)+15*i) for x in c) for i in range(q) for c in W1]
 s,loc=encode(C,15*q);n=parsed(s)
 t=build(s,C,loc,n,(2,4,7,14,15));ck(validate(s,n,t))
 A=stats(t);ck(A==(28,55,536,5))
 out['cases'].append({'W1_copies':q,'N':len(s),'leaves_nodes_edges_depth':A})
 ck(not validate(s,n,('branch',2,t,None)))
C=W1+[tuple((1 if x>0 else -1)*(abs(x)+15) for x in c) for c in G]
s,loc=encode(C,18);n=parsed(s);t=build(s,C,loc,n,(2,4,7,14,15))
ck(validate(s,n,t) and stats(t)==(28,55,536,5))
out['cases'].append({'W1_plus_G':'UNSAT','N':len(s),'leaves_nodes_edges_depth':stats(t)})
# Four untouched G ternaries do not invalidate an original-source subset proof.
def pin(x,a,b):return [(x,a,b),(x,a,-b),(x,-a,b),(x,-a,-b)]
C=pin(1,2,3)+pin(-1,4,5)+[tuple((1 if x>0 else -1)*(abs(x)+5) for x in c) for c in G]
s,loc=encode(C,8);n=parsed(s);t=build(s,C,loc,n,(1,))
ck(validate(s,n,t) and stats(t)==(2,3,8,1))
out['cases'].append({'PINs_plus_G':'UNSAT','N':len(s),'leaves_nodes_edges_depth':stats(t)})
# SAT source and broken original-name alias both reject UNSAT certificates.
s,loc=encode(G,3);n=parsed(s);t=build(s,G,loc,n,(1,))
ck(not validate(s,n,t))
C=pin(1,2,3)+pin(-6,4,5);s,loc=encode(C,6);n=parsed(s)
ck(not validate(s,n,build(s,C,loc,n,(1,6))))
# Genuine path and its tampered source offset on the SAME assignment.
s,loc=encode(W1,15);n=parsed(s);t=build(s,W1,loc,n,(2,4,7,14,15))
def first_path(t,a=None):
 if a is None:a={}
 if t[0]=='leaf' and t[1][0]=='paths':return t[1],a
 if t[0]=='branch':return first_path(t[2],{**a,t[1]:False}) or first_path(t[3],{**a,t[1]:True})
 return None
w,a=first_path(t);ck(source_verify(s,a,w,n))
p=list(w[2]);p[0]=(p[0][0]+1,p[0][1],p[0][2])
ck(not source_verify(s,a,('paths',w[1],p,w[3]),n))
# Actual fully serialized/reparsed ordinary CNF descendants at two levels.
for a in ({2:False,4:False},{2:False,4:False,7:False,14:False,15:False}):
 C=[r for c in W1 if (r:=residue(c,a)) is not None]
 child,_=encode(C,15)
 h=child.splitlines()[0].split();ck(int(h[3])==len(C))
 out['cases'].append({'descendant_byte_size':len(child),'clauses':len(C)})
out['assertion_groups']=checks
print(json.dumps(out,indent=2,sort_keys=True))
