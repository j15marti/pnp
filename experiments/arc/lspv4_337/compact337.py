#!/usr/bin/env python3
"""LSPV-4 337, no-dependency, exhaustive source-only finite guard census.
Exec: python experiments/arc/lspv4_337/compact337.py > summary337.json
NOT an indexed FLMV TM runtime measurement. P versus NP OPEN.
"""
import itertools, collections, json
Z=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
def legal(F,n):
    if len(F)*3!=4*n or n%3:return False
    count=collections.Counter();seen=set()
    for C in F:
        if len(C)!=3 or any(type(v)!=int or not (0<abs(v)<=n) for v in C):return False
        if len({abs(v) for v in C})!=3 or not(all(v>0 for v in C) or all(v<0 for v in C)):return False
        key=tuple(sorted(C))
        if key in seen:return False
        seen.add(key);count.update(C)
    return all(count[v]==count[-v]==2 for v in range(1,n+1))
def connected(F,n):
    adj=[set() for _ in range(n)]
    for C in F:
        for a in C:
            for b in C:
                if abs(a)!=abs(b):adj[abs(a)-1].add(abs(b)-1)
    seen={0};todo=[0]
    while todo:
        for b in adj[todo.pop()]:
            if b not in seen:seen.add(b);todo.append(b)
    return len(seen)==n
def swap(F,i,p,j,q):
    out=[list(C) for C in F]
    out[i][p],out[j][q]=out[j][q],out[i][p]
    return tuple(map(tuple,out))
def masks(n):
    full=(1<<(1<<n))-1
    x=[sum(1<<a for a in range(1<<n) if (a>>i)&1) for i in range(n)]
    return full,x
def clause(C,x,full):
    a=0
    for v in C:a|=x[abs(v)-1] if v>0 else full^x[abs(v)-1]
    return a
def models(F,x,full):
    a=full
    for C in F:a&=clause(C,x,full)
    return a
def count(F,pins):
    n=max(abs(v) for C in F for v in C)
    return sum(all(any(((a>>(abs(v)-1))&1)==int(v>0) for v in C) for C in F)
               for a in range(1<<n)
               if all(((a>>(i-1))&1)==b for i,b in pins.items()))
def width(r):
    k=(2**r-1)//7;n=3*k;m=4*k
    ceil2=lambda q:(q-1).bit_length()
    w=6+ceil2(n+m+1);wp=6+ceil2(n+m+29)
    N=(4*m+2)*w;Np=(4*m+66)*wp
    assert wp==w+1 and Np-N==(4*m+2)+64*wp
    return (n,w,wp,N,Np,Np-N)
def main():
    K=Z+tuple(tuple((abs(v)+6)*(1 if v>0 else -1) for v in C) for C in Z)
    assert legal(Z,6) and legal(F9,9) and legal(K,12)
    full,x=masks(12)
    assert models(K,x,full).bit_count()==324
    hports=collections.Counter();hpins=collections.Counter();n=0
    for sign in (1,-1):
        for i in range(8):
            if (K[i][0]>0)!=(sign>0):continue
            for j in range(8,16):
                if (K[j][0]>0)!=(sign>0):continue
                for p,q in itertools.product(range(3),repeat=2):
                    Q=swap(K,i,p,j,q)
                    assert legal(Q,12) and connected(Q,12)
                    b=models(Q,x,full);assert b.bit_count()==318;n+=1
                    for C in Q:
                        for vslot in range(3):
                            v=C[vslot];other=[C[t] for t in range(3) if t!=vslot]
                            vm=x[abs(v)-1] if v>0 else full^x[abs(v)-1]
                            hports[(b&vm&clause(other,x,full)).bit_count()]+=1
                    for a,t in itertools.combinations(range(12),2):
                        for va,vb in itertools.product((0,1),repeat=2):
                            am=x[a] if va else full^x[a]
                            bm=x[t] if vb else full^x[t]
                            hpins[(b&am&bm).bit_count()]+=1
    assert n==288 and sum(hports.values())==13824 and sum(hpins.values())==76032
    assert min(hports)==90 and min(hpins)==37
    guard=swap(K,0,0,8,0)
    D=guard[0];v=D[1];B=[D[0],D[2]]
    W=[[0,0],[0,0]]
    for a in range(4096):
        if not all(any(((a>>(abs(l)-1))&1)==int(l>0) for l in C) for C in guard[1:]):continue
        i=int(((a>>(abs(v)-1))&1)==int(v>0))
        j=int(any(((a>>(abs(l)-1))&1)==int(l>0) for l in B))
        W[i][j]+=1
    assert W==[[75,162],[66,90]]
    E=[[W[1][1],W[0][1]+W[1][1]],[W[1][0]+W[1][1],sum(map(sum,W))]]
    assert E==[[90,252],[156,393]]
    guardplus=tuple(tuple((abs(v)+9)*(1 if v>0 else -1) for v in C) for C in guard)
    lifted=swap(F9+guardplus,0,0,12,1)
    assert legal(lifted,21) and connected(lifted,21)
    rows=[]
    for pivot in (0,1):
        pins={1:pivot,2:0,4:0,6:0}
        f9=count(F9,pins);deleted=count(F9[1:],pins)
        lifted_count=0
        for a in range(512):
            if any(((a>>(i-1))&1)!=b for i,b in pins.items()):continue
            if not all(any(((a>>(abs(v)-1))&1)==int(v>0) for v in C) for C in F9[1:]):continue
            for z in range(4096):
                w=a|(z<<9)
                lifted_count+=all(any(((w>>(abs(v)-1))&1)==int(v>0) for v in C) for C in lifted)
        rows.append((f9,deleted,lifted_count))
    assert rows==[(0,2,180),(3,3,468)]
    for bad in (K[:-1],K+(K[0],),((1,1,2),)+K[1:],((1,-2,3),)+K[1:],((1,2,13),)+K[1:]):
        assert not legal(bad,12)
    widths={str(r):width(r) for r in (8,12,16,20,24)}
    print(json.dumps({'status':'COMPUTATIONAL exhaustive source audit; exact width lemma; P vs NP OPEN',
       'source':'two Z6 blocks; all 288 cross-copy same-sign literal swaps',
       'source_models':324,'swaps':n,'models_per_swapped_original':318,
       'all_connected':True,'port_tests':sum(hports.values()),'min_W11':min(hports),
       'two_pin_tests':sum(hpins.values()),'min_two_pin':min(hpins),
       'W':W,'E':E,'F9_pinned_source_delete_lift':rows,'malformed_rejected':5,
       'port_hist':dict(sorted(hports.items())),'two_pin_hist':dict(sorted(hpins.items())),
       'fixed_width_threshold_rows':widths},indent=2,sort_keys=True))
if __name__=='__main__':main()
