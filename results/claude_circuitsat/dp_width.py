# Syntactic residual DP ("forward DP" over a variable order) for CNF / circuit-SAT.
# State after assigning variable set S by assignment a = set of residual clauses
# (crossing clauses not satisfied by a, restricted to unassigned vars); assignments
# falsifying a clause inside S are dead.  W(S) = #distinct live states.
# Ordered DP cost over order pi: max_i W(prefix_i).  Optimal order found exactly by
# bottleneck DP over the subset lattice.  Reverse DP over pi = forward DP over
# reversed pi; meet-in-the-middle = min_S max(F[S], F[~S]).  Each run < 30 s.
import sys, json, itertools, random
import numpy as np

def php(h):  # pigeons h+1 into h holes; var p*h+j
    n=(h+1)*h; C=[]
    for p in range(h+1): C.append([(p*h+j,1) for j in range(h)])
    for j in range(h):
        for p,q in itertools.combinations(range(h+1),2): C.append([(p*h+j,0),(q*h+j,0)])
    return n,C
def rand3(n,m,seed):
    R=random.Random(seed); C=[]
    while len(C)<m:
        vs=R.sample(range(n),3); C.append([(v,R.randint(0,1)) for v in vs])
    return n,C
def brute_sat(n,C):
    A=((np.arange(1<<n)[:,None]>>np.arange(n))&1).astype(bool)
    ok=np.ones(1<<n,bool)
    for cl in C: ok&=np.any([A[:,v]==bool(s) for v,s in cl],axis=0)
    return int(ok.sum())

def widths(n,C):
    W=np.zeros(1<<n,np.int64)
    for S in range(1<<n):
        vs=[v for v in range(n) if S>>v&1]; k=len(vs)
        A=((np.arange(1<<k)[:,None]>>np.arange(k))&1).astype(bool)
        col={v:i for i,v in enumerate(vs)}
        live=np.ones(1<<k,bool); sig=[]; ids={}
        for cl in C:
            ins=[(v,s) for v,s in cl if v in col]; out=tuple(sorted((v,s) for v,s in cl if v not in col))
            sat=np.zeros(1<<k,bool)
            for v,s in ins: sat|=(A[:,col[v]]==bool(s))
            if not out: live&=sat
            elif ins:
                rid=ids.setdefault(out,len(ids))
                sig.append((rid,~sat))
        if not live.any(): W[S]=0; continue
        if not ids: W[S]=1; continue
        M=np.zeros((1<<k,len(ids)),bool)
        for rid,uns in sig: M[:,rid]|=uns
        M=M[live]; P=np.packbits(M,axis=1)
        W[S]=len(np.unique(P.view(np.dtype((np.void,P.shape[1]))).ravel()))
    return W

def bottleneck(n,W):
    F=np.full(1<<n,np.iinfo(np.int64).max); F[0]=1
    T=np.full(1<<n,np.iinfo(np.int64).max); T[0]=1   # min total states
    for S in sorted(range(1,1<<n),key=lambda s:bin(s).count('1')):
        best=bt=None
        for v in range(n):
            if S>>v&1:
                b=max(F[S^(1<<v)],W[S]); t=T[S^(1<<v)]+W[S]
                best=b if best is None else min(best,b); bt=t if bt is None else min(bt,t)
        F[S]=best; T[S]=bt
    full=(1<<n)-1
    meet=min(max(F[S],F[full^S]) for S in range(1<<n))
    return int(F[full]),int(T[full]),int(meet)

if __name__=="__main__":
    kind=sys.argv[1]
    if kind=="php": n,C=php(int(sys.argv[2])); name=f"PHP^{int(sys.argv[2])+1}_{sys.argv[2]}"
    else: n,C=rand3(int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])); name=f"rand3cnf n={n} m={len(C)} seed={sys.argv[4]}"
    nsat=brute_sat(n,C); W=widths(n,C); b,t,m=bottleneck(n,W)
    ident=list(range(n)); prefix=[int(W[(1<<i)-1]) for i in range(n+1)]
    print(json.dumps({"instance":name,"n":n,"m":len(C),"models":nsat,
      "opt_forward_max_width":b,"opt_forward_total_states":t,"opt_meet_in_middle_max_width":m,
      "max_crossing_bound_log2":None,"identity_order_profile":prefix}))
