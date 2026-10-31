"""Exact small-n tables for the ClaudeCircuitSAT ledger.
For n inputs (n<=3), iterative deepening over circuits of g binary gates (10 non-degenerate
2-input gate types; negation is free via the gate table).  Records:
  C(f): minimum gates for every f on n inputs (all inputs available as nodes).
  U(n): min gates of a circuit whose output depends syntactically on all n inputs
        (every input reaches the output) and computes the constant-0 function (UNSAT).
  S1(n): same connectivity, exactly one satisfying assignment.
Runs in a few seconds."""
import itertools, json, sys
GATES=[t for t in range(16) if t not in (0,15,3,5,10,12)]  # drop consts and projections/negations
def tt_inputs(n):
    N=1<<n; return [sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
def apply(t,x,y,N):
    r=0
    for a in range(N):
        b=((x>>a)&1)*2+((y>>a)&1)
        if (t>>b)&1: r|=1<<a
    return r
def search(n,maxg,rep):
    N=1<<n; full=(1<<N)-1
    ins=tt_inputs(n)
    best={}            # f -> min gates (any circuit)
    conn={}            # (f)-> min gates with all inputs reaching the last gate
    # nodes: (tt, support-mask of inputs reaching it)
    def rec(nodes,g,limit):
        if g>0:
            tt,sup=nodes[-1]
            if tt not in best or best[tt]>g: best[tt]=g
            if sup==(1<<n)-1 and (tt not in conn or conn[tt]>g): conn[tt]=g
        if g==limit: return
        k=len(nodes)
        for i in range(k):
            for j in range(i if rep else i+1,k):
                for t in GATES:
                    v=apply(t,nodes[i][0],nodes[j][0],N)
                    rec(nodes+[(v,nodes[i][1]|nodes[j][1])],g+1,limit)
    rec([(ins[i],1<<i) for i in range(n)],0,maxg)
    return best,conn
out={}
# stage A: repeats allowed (needed for x&~x style gates), shallow depth -> U,S1
# stage B: distinct-node gates, full depth -> gate-count distribution (repeats only create constants/negations)
for n,maxg,rep in [(1,2,True),(2,3,True),(3,3,True),(3,4,False)]:
    best,conn=search(n,maxg,rep)
    N=1<<n
    dist={}
    for f in range(1<<N):
        c=0 if (f in tt_inputs(n) or f in [(1<<N)-1-x for x in tt_inputs(n)] or f in (0,(1<<N)-1)) else best.get(f)
        dist[c]=dist.get(c,0)+1
    U=conn.get(0)
    S1=min((conn[f] for f in conn if bin(f).count('1')==1),default=None)
    out[f'n{n}_depth{maxg}_rep{int(rep)}']={'gate_count_distribution(None=exceeds search depth)':{str(k):v for k,v in dist.items()},'U':U,'S1':S1,'searched_depth':maxg}
    print(n,maxg,rep,list(out.values())[-1])
json.dump(out,open('mincircuit_results.json','w'),indent=1)
