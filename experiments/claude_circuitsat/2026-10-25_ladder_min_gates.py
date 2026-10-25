"""Exact minimum number of fan-in-2 gates (full binary basis, free negation) for
every Boolean function on n<=3 inputs, plus selected n=4 targets, by iterative
deepening over circuits.  Wires = 2*gates (each gate has 2 in-wires), reported
separately from the n input wires needed to make an input relevant.
Each invocation targets <30 s; n=4 targets are separate stages (argv)."""
import sys, json, itertools, time
def tt_inputs(n):
    N=1<<n; full=(1<<N)-1
    xs=[]
    for i in range(n):
        v=0
        for a in range(N):
            if (a>>i)&1: v|=1<<a
        xs.append(v)
    return xs,full
def norm(t,full): return t if not (t&1) else t^full   # up to complement
def ops(a,b,full):
    na,nb=a^full,b^full
    return {a&b,a&nb,na&b,a^b,a|b}
def min_cost(n,targets,maxg):
    xs,full=tt_inputs(n)
    tset={norm(t,full) for t in targets}
    best={}
    base=[norm(x,full) for x in xs]
    for x in base: 
        if x in tset: best[x]=0
    def dfs(nodes,left,depth_goal):
        if left==0: return
    for g in range(1,maxg+1):
        remaining=set(tset)-set(best)
        if not remaining: break
        found=set()
        def rec(nodes,used):
            if used==g:
                return
            m=len(nodes)
            for i in range(m):
                for j in range(i+1,m):
                    for r in ops(nodes[i],nodes[j],full):
                        r=norm(r,full)
                        if r in nodes: continue
                        if r in remaining and used+1<=g: found.add(r)
                        if used+1<g:
                            rec(nodes+[r],used+1)
        rec(list(base),0)
        for f in found: best[f]=g
    return best,full
if __name__=="__main__":
    t0=time.time(); stage=sys.argv[1]; out={}
    if stage in("1","2","3"):
        n=int(stage); N=1<<n; full=(1<<N)-1
        allf=range(1<<N)
        best,_=min_cost(n,allf,{1:1,2:3,3:4}[n]+1)
        hist={}
        for f in allf:
            c=best.get(norm(f,full),None); hist[c]=hist.get(c,0)+1
        out={"n":n,"cost_histogram_all_functions":{str(k):v for k,v in sorted(hist.items(),key=lambda x:(x[0] is None,x[0]))}}
    else:
        n=4; N=16; full=(1<<N)-1; xs,_=tt_inputs(4)
        T={"AND4":xs[0]&xs[1]&xs[2]&xs[3],"XOR4":xs[0]^xs[1]^xs[2]^xs[3],
           "OR4":xs[0]|xs[1]|xs[2]|xs[3],"AND2_XOR2":(xs[0]&xs[1])^(xs[2]&xs[3])}
        best,_=min_cost(4,T.values(),int(sys.argv[2]))
        out={"n":4,"min_gates_up_to_bound":{k:best.get(norm(v,full)) for k,v in T.items()},"search_bound":int(sys.argv[2])}
    out["seconds"]=round(time.time()-t0,2)
    print(json.dumps(out))
