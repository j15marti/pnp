#!/usr/bin/env python3
"""LSPV-1/418: compact original-source public-port certificate constructor."""
def norm(a): return tuple(sorted(set(a),key=lambda x:(abs(x),x<0)))
def lit(i,b): return i if b else -i
def compile_port(k,F,gates,target):
    ledger=list(map(norm,F)); steps=[]
    for j,(u,v,table) in enumerate(gates):
        z=k+j+1
        for a in (0,1):
            for b in (0,1):
                val=(table>>(2*a+b))&1
                ledger.append(norm([-lit(u,a),-lit(v,b),lit(z,val)]))
    m=len(ledger)
    def resolve(i,j,p):
        a,b=ledger[i],ledger[j]
        assert p in a and -p in b
        ledger.append(norm((set(a)-{p})|(set(b)-{-p})))
        steps.append((i,j,p))
        return len(ledger)-1
    leaves={}
    for mask in range(1<<k):
        env={i:(mask>>(i-1))&1 for i in range(1,k+1)}
        for j,(u,v,table) in enumerate(gates):
            env[k+j+1]=(table>>(2*env[u]+env[v]))&1
        bad=next((idx for idx,C in enumerate(F) if all(env[abs(x)]!=int(x>0) for x in C)),None)
        if bad is not None: leaves[mask]=bad;continue
        goal=next((x for x in target if env[abs(x)]==int(x>0)),None)
        if goal is None: raise ValueError('not entailed')
        known={}
        for j,(u,v,table) in enumerate(gates):
            z=k+j+1
            if z>abs(goal):break
            idx=len(F)+4*j+2*env[u]+env[v]
            for w in dict.fromkeys((u,v)):
                if w>k: idx=resolve(known[w],idx,lit(w,env[w]))
            known[z]=idx
        leaves[mask]=known[abs(goal)]
    for x in range(k,0,-1):
        nxt={}
        for mask in sorted({a&~(1<<(x-1)) for a in leaves}):
            left,right=leaves[mask],leaves[mask|(1<<(x-1))]
            if x not in ledger[left]:nxt[mask]=left
            elif -x not in ledger[right]:nxt[mask]=right
            else:nxt[mask]=resolve(left,right,x)
        leaves=nxt
    assert set(ledger[leaves[0]])<=set(target)
    assert len(steps)<=(2*len(gates)+1)*(1<<k)-1
    return len(steps),list(ledger[leaves[0]])
if __name__=='__main__':
    for case in [(1,[[1]],[(1,1,12)],[2]),(2,[[1,2],[-1]],[(2,2,12)],[3]),(1,[[1],[-1]],[(1,1,12)],[2])]:
        print(case,compile_port(*case))
