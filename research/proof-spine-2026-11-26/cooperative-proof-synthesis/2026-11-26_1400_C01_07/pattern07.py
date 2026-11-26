"""Direct three-track certificate, acquired from cyclic word, all literal guards."""
from pair_absorb07 import *
def direct(A,D):
 n=len(A);st={'recognition_trials':0,'local_modes':0,'transitions':0}
 if n%20 or any(len(sc)!=1 for sc,_ in A):return 'OPEN',st
 h=n//20
 for rev in (0,1):
  X=A if not rev else [(sc,{w:{(v,u):s for (u,v),s in M.items()} for w,M in T.items()}) for sc,T in A[::-1]]
  for root in range(n):
   st['recognition_trials']+=1;Y=X[root:]+X[:root];w=[sc[0] for sc,_ in Y];a=[];xx=[];valid=True
   for j in range(h):
    x,x1,u,v,x2,x3=w[6*j:6*j+6]
    if len({x,u,v})!=3 or x!=x1 or x!=x2 or x!=x3:valid=False;break
    a.extend([u,v]);xx.append(x)
   if not valid:continue
   b=w[6*h:8*h]
   if len(set(a+b+xx))!=5*h:continue
   if w[8*h:14*h]!=[c for c in a[::-1] for _ in range(3)] or w[14*h:]!=[c for c in b[::-1] for _ in range(3)]:continue
   break
  else:continue
  break
 else:return 'OPEN',st
 # Group A labels in disjoint pairs. Keep all values on retained variables, including fixed phases.
 groups=[tuple(a[2*j:2*j+2]) for j in range(h)]+[(c,) for c in b]
 dom={j:list(I.product(*(sorted(D[c]) for c in g))) for j,g in enumerate(groups)}
 track1={};track2={};track3={}
 for j,g in enumerate(groups):
  if j<h:
   segment=Y[6*j:6*j+6];M={};N={}
   # Exact six-atom response conditioned on the two retained phases.
   for val in dom[j]:
    z=dict(zip(g,val));out={}
    for q in sorted(D[xx[j]]):
     z[xx[j]]=q;Q=ID;st['local_modes']+=1
     for sc,T in segment:Q=cat(Q,T[(z[sc[0]],)])
     for e,ww in Q.items():out.setdefault(e,ww)
    M[val]=out;Q=ID
    for sc,T in Y[8*h+6*(h-1-j):8*h+6*(h-j)]:Q=cat(Q,T[(z[sc[0]],)])
    N[val]={(v,u):ww for (u,v),ww in Q.items()}
   track1[j]=M;track2[j]=N
  else:
   q=j-h;M={val:Y[6*h+q][1][val] for val in dom[j]};N={}
   for val in dom[j]:
    Q=ID
    for sc,T in Y[14*h+3*(2*h-1-q):14*h+3*(2*h-q)]:Q=cat(Q,T[val])
    N[val]={(v,u):ww for (u,v),ww in Q.items()}
   track1[j]=M;track3[j]=N
 # Common phase order. Tracks 2,3 reversed; join physical cyclic endpoints.
 S={(p,p):() for p in I.product((0,1),repeat=3)}
 for j in range(3*h):
  E={}
  for val in dom[j]:
   matrices=[Z[j][val] if j in Z else ID for Z in (track1,track2,track3)]
   for (p,q),ww in S.items():
    opts=[[(v,t) for (u,v),t in M.items() if u==x] for x,M in zip(q,matrices)]
    for opt in I.product(*opts):
     st['transitions']+=1;v=tuple(x for x,_ in opt);E.setdefault((p,v),ww+tuple(a for _,q in opt for a in q))
  S=E
 for (p,q),ww in S.items():
  # Track order physical: 1 forward, 2 reverse, 3 reverse.
  if q[0]==q[1] and p[1]==q[2] and p[2]==p[0]:return dict(ww),st
 return None,st
if __name__=='__main__':
 import random
 from discover_shape06 import discover
 result=[];rng=random.Random(26112607)
 for k,g in [(10,[162,108]),(20,[322,188]),(40,[642,348]),(80,[1282,668])]:
  T,U,*_=fixture(k,'pair_leaf_dense');perm=list(range(len(T)));rng.shuffle(perm);T=[T[i] for i in perm];guard=[perm.index(j) for j in g];mp={}
  for c in range(3):
   v=sorted(x for d,x in U if d==c);w=v[:];rng.shuffle(w);mp.update({(c,v):y for v,y in zip(v,w)})
  T=[tuple(mp[c,v] for c,v in enumerate(t)) for t in T];L,cc=closure(T,U,set(range(len(T)))-set(guard));assert L is not None
  X,s=discover(T,U,set(range(len(T))));assert X;J,P,pr=X;R=tables(T,J,P,pr,L);A,D,ch=initial(R,P);w,st=direct(A,D);assert w!='OPEN' and w is not None
  row={'k':k,'triples':len(T),'guard':guard,'permutation':perm,'owner_renaming':[[c,v,x] for (c,v),x in sorted(mp.items())],'chart':{'J':J,'P':P,'private':[sorted(x) for x in pr]},'closure_calls':cc,'discovery':s,'stats':st,'witness':lift(T,U,R,w,L)}
  result.append(row);print(k,s,st,flush=True);json.dump(result,open('pattern_results07.json','w'),indent=2)
