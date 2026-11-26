from p4audit import *
def chain(k, bad):
 T=[tuple(v+6*b for v in t) for b in range(k) for t in (U if bad and b==k//2 else V)]
 for b in range(k-1):
  i,j=18*b,18*(b+1);c=b%2;p,q=list(T[i]),list(T[j]);p[c],q[c]=q[c],p[c];T[i],T[j]=tuple(p),tuple(q)
 return T
if __name__=='__main__':
 for k in [2,4,8]:
  for bad in [False,True]:
   T=chain(k,bad);assert len(T)==len(set(T)) and nx.is_connected(graph(T)) and nx.check_planarity(graph(T))[0];assert all(sum(t[c]==a for t in T)==3 for c in range(4) for a in range(6*k));p,calls,err=closure(T);out=quotient(T,p) if not err else (False,0,0,0,None);assert out[0]!=bad;print(k,bad,len(p),calls,out)
 for T in [U,V,neighbor()]:
  n=len(T)//3;cs=[set(j for j,t in enumerate(T) if t[c]==a) for c in range(4) for a in range(n)]
  sols=[s for s in it.combinations(range(len(T)),n) if all(len(set(s)&c)==1 for c in cs)]
  print('sols',len(sols),sols,'support',len(set(it.chain.from_iterable(sols))))
