#!/usr/bin/env python3
"""LSPV-2 337 standalone original-source joint-frontier proof reproducer.
Python 3 standard library. This is a restricted representation result, NOT P vs NP.
"""
import json
F9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]]
PERMS={3:[2,6,4,9,5,3,7,1,8],4:[7,1,11,5,10,8,6,12,9,4,2,3],5:[8,4,2,6,9,1,11,5,3,13,7,10,14,12,15],6:[8,10,11,9,1,16,12,14,2,7,13,6,4,3,17,18,5,15]}
def canonical(F,n):
    if type(n)!=int or 3*len(F)!=4*n:return False
    cp=[0]*(n+1);cn=[0]*(n+1);seen=set()
    for c in F:
        if len(c)!=3 or len(set(map(abs,c)))!=3 or any(type(x)!=int or x==0 or abs(x)>n or (x>0)!=(c[0]>0) for x in c):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key)
        for x in c:(cp if x>0 else cn)[abs(x)]+=1
    return all(cp[i]==cn[i]==2 for i in range(1,n+1))
def dual(k,perm):
    E=[]
    for r in range(2):
        for i in range(k):E.append((r*k+i,r*k+(i+1)%k))
    E.extend((i,k+i) for i in range(k))
    pos=[[] for _ in range(2*k)];neg=[[] for _ in range(2*k)]
    for j,(a,b) in enumerate(E):
        for v in (a,b):pos[v].append(perm[j]);neg[v].append(-(j+1))
    return pos+neg
def minwidth(F,n):
    mask=[sum(1<<(abs(x)-1) for x in c) for c in F]
    size=1<<n;w=bytearray(size);dp=bytearray(size)
    for s in range(1,size-1):w[s]=sum(bool(s&c) and (s&c)!=c for c in mask)
    for s in range(1,size):
        m=s;best=255
        while m:
            bit=m&-m;m-=bit
            best=min(best,max(w[s],dp[s^bit]))
        dp[s]=best
    return dp[-1]
def greedy(F,n):
    remaining=set(range(1,n+1));seen=set();order=[];probes=0
    while remaining:
        candidates=[]
        for v in sorted(remaining):
            a=seen|{v};width=0
            for c in F:
                t=sum(abs(x) in a for x in c);probes+=3
                if 0<t<3:width+=1
            candidates.append((width,v))
        _,v=min(candidates);order.append(v);remaining.remove(v);seen.add(v)
    return order,probes
def source_dp(F,n,order,pins=None):
    pins=pins or {};occ={v:[] for v in order}
    for j,c in enumerate(F):
        for x in c:occ[abs(x)].append((j,int(x>0)))
    assert all(len(occ[v])==4 for v in order)
    index={v:i for i,v in enumerate(order)}
    end=[max(index[abs(x)] for x in c) for c in F]
    masks=[sum(1<<(abs(x)-1) for x in c) for c in F]
    states={0:1};seen=0;peak=1;attempted=0;reads=0
    for i,v in enumerate(order):
        seen|=1<<(v-1)
        crossing=sum(1<<j for j,c in enumerate(masks) if (seen&c) and (seen&c)!=c)
        complete=sum(1<<j for j in range(len(F)) if end[j]==i)
        nxt={}
        for key,ways in states.items():
            for bit in ([pins[v]] if v in pins else [0,1]):
                attempted+=1;current=key
                for j,sign in occ[v]:
                    reads+=1
                    if bit==sign:current|=1<<j
                if (current&complete)!=complete:continue
                future=current&crossing
                nxt[future]=nxt.get(future,0)+ways
        states=nxt;peak=max(peak,len(states))
    return {'models':states.get(0,0),'peak':peak,'transitions':attempted,'incidence_reads':reads}
def main():
    out={}
    for name,n,F in [('F9',9,F9)]+[(f'DUAL{k}',3*k,dual(k,PERMS[k])) for k in sorted(PERMS)]:
        assert canonical(F,n),(name,'bad source')
        wplus=minwidth([c for c in F if c[0]>0],n)
        wminus=minwidth([c for c in F if c[0]<0],n)
        wjoint=minwidth(F,n)
        order,probes=greedy(F,n)
        dp=source_dp(F,n,order)
        out[name]={'n':n,'signed_widths':[wplus,wminus], 'exact_joint_width':wjoint,
                   'paid_greedy_order':order,'paid_greedy_probes':probes,**dp}
    assert out['F9']['signed_widths']==[3,3] and out['F9']['exact_joint_width']==8
    assert [out[f'DUAL{k}']['exact_joint_width'] for k in sorted(PERMS)]==[8,10,11,12]
    print(json.dumps({'status':'PROVED/EXACT restricted; P vs NP OPEN','cases':out},indent=2))
if __name__=='__main__':main()
