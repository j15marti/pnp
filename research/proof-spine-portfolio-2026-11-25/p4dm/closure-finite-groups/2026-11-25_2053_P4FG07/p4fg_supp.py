from p4fg_block import *
def ring(k):
 T=[tuple(x+2*j for x in t) for j in range(k) for t in CUBE]
 for j in range(0,k,2):T=swap(T,6*j+2,6*(j+1)+2,0)
 for j in range(1,k,2):T=swap(T,6*j,6*((j+1)%k),1)
 return T,2*k
def tail(base,k):
 T=list(base)+[tuple(x+6+2*j for x in t) for j in range(k) for t in CUBE]
 for j in range(k):T=swap(T,0 if j==0 else 18+6*(j-1)+1,18+6*j,0)
 return T,6+2*k
if __name__=='__main__':
 out={'rings':[],'tails':[],'exceptions':{}}
 for k in [4,6,8,16,32]:
  T,n=ring(k);a,w,s=solve2(T,n);assert a=='YES' and verify(T,n,w) and nx.is_connected(graph(T,n));out['rings'].append({'k':k,'status':a,'stats':s})
 for k in [1,4,16,32]:
  for label,base in [('U',U),('V',V)]:
   T,n=tail(base,k);a,w,s=solve2(T,n);assert nx.is_connected(graph(T,n));assert a=='UNKNOWN' or (a=='YES')==(label=='V');out['tails'].append({'k':k,'name':label,'status':a,'stats':s})
 r=random.Random(20261125);C=Counter();calls=0
 for _ in range(500):
  nr=r.randrange(1,9);k=r.randrange(1,10);R=[]
  for j in range(nr):
   d=tuple(sorted((i,r.choice([-1,1])) for i in r.sample(range(k),r.randrange(1,min(k,3)+1))));R.append((d,1-sum(c<0 for i,c in d)))
  a,x,s=block_solver(R,k,cap=3);truth=any(all(sum(c*y[i] for i,c in d)==b for d,b in R) for y in it.product([0,1],repeat=k));assert a=='UNKNOWN' or (a=='YES')==truth;C[a]+=1;calls+=s.get('matching_calls',0)
 out['exceptions']={'counts':C,'matching_calls':calls};print(json.dumps(out,indent=2))
