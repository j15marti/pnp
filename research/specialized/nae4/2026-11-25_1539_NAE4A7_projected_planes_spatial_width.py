from collections import defaultdict

def measure(p,spatial):
  cs=[(i,p+(i+j)%p,2*p+(i+2*j)%p) for i,j in ([(i,j) for i in range(p) for j in range(4)] if spatial else [(i,j) for j in range(4) for i in range(p)])]
  def cc(ids):
    parent=list(range(3*p));count=3*p
    def find(a):
      while parent[a]!=a:
        parent[a]=parent[parent[a]];a=parent[a]
      return a
    for i in ids:
      a,b,c=cs[i]
      for x in [b,c]:
        u,v=find(a),find(x)
        if u!=v:parent[v]=u;count-=1
    return count
  all_=set(range(4*p));c=cc(all_);q=[{i} for i in range(4*p)];w=0
  while len(q)>1:
    for s in q:w=max(w,3*p-cc(s)-cc(all_-s)+c)
    q=[q[i]|q[i+1] if i+1<len(q) else q[i] for i in range(0,len(q),2)]
  return w
for p in [7,11,31,101,257]:print(p,measure(p,False),measure(p,True))
