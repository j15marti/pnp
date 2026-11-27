# Standalone, standard-library independent replay of five-cap J7 certificate.
from itertools import product,combinations
from collections import Counter

def canon(w):
 d={};return tuple(d.setdefault(c,len(d)) for c in w)
W=sorted({canon(w) for w in product(range(3),repeat=6) if all(w.count(c)%2==0 for c in range(3))})
I={w:i for i,w in enumerate(W)};FULL=(1<<31)-1

def colorable(V,E,P=(),w=(),free=()):
 if any(a==b for a,b in E) or any(w[a]!=w[b] for a,b in free):return False,0
 used={v:set() for v in V};steps=0
 for v,c in zip(P,w):
  if v is None:continue
  if c in used[v]:return False,0
  used[v].add(c)
 def rec(todo):
  nonlocal steps
  steps+=1
  if steps>200000:raise RuntimeError('UNKNOWN: cap reached')
  if not todo:return True
  j=min(todo,key=lambda j:(3-len(used[E[j][0]]|used[E[j][1]]),j));a,b=E[j]
  for c in sorted({0,1,2}-used[a]-used[b]):
   used[a].add(c);used[b].add(c)
   if rec(todo-{j}):return True
   used[a].remove(c);used[b].remove(c)
  return False
 return rec(set(range(len(E)))),steps

def pairs(L):
 if not L:yield ();return
 a=L[0]
 for b in L[1:]:
  for p in pairs([i for i in L if i not in (a,b)]):yield ((a,b),)+p

def close(U):
 rounds=[]
 while True:
  R=set()
  for i in U:
   w=W[i]
   for a,b in combinations(range(3),2):
    good=False
    for p in pairs([j for j,c in enumerate(w) if c in (a,b)]):
     ok=True
     for swaps in product((0,1),repeat=len(p)):
      q=list(w)
      for bit,(r,s) in zip(swaps,p):
       if bit:q[r]=a+b-q[r];q[s]=a+b-q[s]
      if I[canon(q)] not in U:ok=False;break
     if ok:good=True;break
    if not good:R.add(i);break
  if not R:return U,rounds
  rounds.append(sum(1<<i for i in R));U=U-R

def flower():
 E=[]
 for i in range(7):
  for j in range(1,4):
   E.extend([(4*i,4*i+j),(4*i+j,4*((i+1)%7)+(5-j if i==6 and j in (2,3) else j))])
 return list(range(28)),sorted(tuple(sorted(e)) for e in E)

def main():
 V,E=flower();C=[3,5,7,18,19,20];S=set(range(4,12));B=set(V)-S
 assert [i for i,(a,b) in enumerate(E) if (a in S)!=(b in S)]==C
 caps=[[(list(range(4)),[(0,3),(1,3),(2,3)],[0,1,2,2,1,0],[]),(list(range(4)),[(0,3),(1,3),(2,3)],[0,1,2,1,0,2],[])], [([],[],[None]*6,p) for p in [[(0,3),(1,4),(2,5)],[(0,5),(1,3),(2,4)],[(0,4),(1,5),(2,3)]]]]
 plain=[];hybrid=[];metrics=[]
 for A,cs in zip((S,B),caps):
  P=[next(v for v in E[i] if v in A) for i in C];F=[e for e in E if set(e)<=A];U=set(range(31));H=set(U);logs=[]
  for v,f,p,free in cs:
   cap=set();cost=0
   for j,w in enumerate(W):
    ok,n=colorable(v,f,p,w,free);cost+=n
    if ok:cap.add(j)
   off=28;G=F+[(a+off,b+off) for a,b in f]+[(P[j],q+off) for j,q in enumerate(p) if q is not None]+[(P[a],P[b]) for a,b in free]
   ok,n=colorable(sorted(A)+[off+q for q in v],G);assert not ok
   U-=cap;H,rounds=close(H-cap)
   logs.append((sum(1<<j for j in cap),cost,n,rounds))
  assert close(U)[0]==H
  plain.append(sum(1<<j for j in U));hybrid.append(sum(1<<j for j in H));metrics.append(logs)
 assert plain==[845969663,1301792654] and hybrid==[845690993,1301513984]
 assert plain[0]&plain[1]==278670 and not hybrid[0]&hybrid[1]
 # Minimal correctness control: every cap's own actual support is fixed by Kempe closure.
 for cs in caps:
  for v,f,p,free in cs:
   M={j for j,w in enumerate(W) if colorable(v,f,p,w,free)[0]};assert M and close(M)[0]==M
 # Dropping guard-invariance would be unsound: a nonempty singleton pinned word is pruned.
 assert not close({0})[0]
 print('plain',plain,'hybrid',hybrid,'per-cap (mask,cap support nodes,child color nodes,closure rounds)',metrics)
if __name__=='__main__':main()
