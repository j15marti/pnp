import itertools, math
def tab(n):
    N=n+1; f=[0]*(1<<N)
    for m in range(1<<N):
        b=m&1; z=[(m>>(i+1))&1 for i in range(n)]; u=[1-t for t in z]
        x=sum(u[i]&u[j] for i in range(n) for j in range(i+1,n))&1
        f[m]=b|(x^int(all(u)))
    return f
def anf_deg(f,N):
    f=f[:]
    for i in range(N):
        for m in range(1<<N):
            if m>>i&1: f[m]^=f[m^(1<<i)]
    return max(bin(m).count('1') for m in range(1<<N) if f[m])
for n in range(3,12):
    f=tab(n); a=sum(f)
    form=2**n+sum(math.comb(n,k) for k in range(n+1) if k%4 in(2,3))+(1 if n%4 in(0,1) else -1)
    print(n,a,form,a==form,anf_deg(f,n+1))
