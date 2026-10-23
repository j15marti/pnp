"""ClaudeCircuitSAT ladder. Stage A: exact min B2 circuit size, all 3-var functions.
Stage B: fixed-topology CircuitSAT decision functions F_T(op-tables); essential vars + exact size when small.
Each stage < 30s."""
import itertools, json, sys
def stageA():
    n=3; N=1<<n; M=(1<<N)-1
    xs=[sum(((i>>j)&1)<<i for i in range(N)) for j in range(n)]
    ops=range(16)
    def ap(op,a,b):
        r=0
        for i in range(N):
            if (op>>(((a>>i)&1)*2+((b>>i)&1)))&1: r|=1<<i
        return r
    best={}
    for x in xs: best[x]=0
    best[0]=0; best[M]=0
    cache={}
    def dfs(sig,k,K):
        if k==K: return
        L=len(sig)
        for i in range(L):
            for j in range(i+1,L):
                for op in ops:
                    key=(op,sig[i],sig[j])
                    v=cache.get(key)
                    if v is None: v=cache[key]=ap(op,sig[i],sig[j])
                    if v not in best or best[v]>k+1: best[v]=k+1
                    dfs(sig+[v],k+1,K)
    dfs(list(xs),0,4)
    return best
def stageB(maxk=2):
    # topology: n=2 inputs x1,x2; gate g_t = op_t(a_t,b_t) with fixed wiring; ops 4-bit tables as inputs
    res={}
    topo={ 'k1':[(0,1)], 'k2_chain':[(0,1),(2,0)], 'k2_chain2':[(0,1),(2,1)], 'k2_x1x2_then_g1x2':[(0,1),(2,1)] }
    for name,T in topo.items():
        k=len(T); m=4*k
        tt=0; ess=[]
        F=[]
        for w in range(1<<m):
            ops=[(w>>(4*t))&15 for t in range(k)]
            sat=False
            for x1 in (0,1):
                for x2 in (0,1):
                    sig=[x1,x2]
                    for t,(a,b) in enumerate(T):
                        sig.append((ops[t]>>(sig[a]*2+sig[b]))&1)
                    if sig[-1]: sat=True
            F.append(sat)
        for v in range(m):
            if any(F[w]!=F[w^(1<<v)] for w in range(1<<m)): ess.append(v)
        res[name]={'inputs':m,'essential':len(ess),'sat_count':sum(F),'gate_lb':len(ess)-1,'wire_lb':2*(len(ess)-1)}
    return res
if __name__=='__main__':
    b=stageA()
    from collections import Counter
    c=Counter(b.values())
    out={'stageA_all_funcs_found_by_size4':len(b),'by_size':dict(c)}
    out['stageB']=stageB()
    print(json.dumps(out,indent=1))
    json.dump(out,open('results/claude_circuitsat/ladder_results.json','w'),indent=1)
