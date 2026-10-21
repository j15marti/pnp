# L1 Fourier spectral norm of indicator functions on k bits: which natural block transitions meet a poly bound B(n)?
import itertools, math
def l1(f,k):
    xs=list(itertools.product([1,-1],repeat=k)); tot=0
    for S in range(1<<k):
        c=0
        for x in xs:
            chi=1
            for j in range(k):
                if S>>j&1: chi*=x[j]
            c+=f(x)*chi
        tot+=abs(c)/len(xs)
    return tot
fs={'parity':lambda x:int(math.prod(x)==1),
 'AND':lambda x:int(all(v==1 for v in x)),
 'IP':lambda x:int(sum((x[2*i]==-1)&(x[2*i+1]==-1) for i in range(len(x)//2))%2==0),
 'MAJ':lambda x:int(sum(v==1 for v in x)>len(x)/2)}
for n,f in fs.items():
    print(n,[round(l1(f,k),2) for k in (2,4,6,8,10)])
