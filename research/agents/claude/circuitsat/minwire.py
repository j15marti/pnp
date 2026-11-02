"""Exhaustive exact synthesis: min #2-input gates (full basis B2, DAG, fan-out allowed)
for functions on n inputs, restricted to gate budgets <= K.  Reports, per gate count k,
which functions with exactly ONE satisfying assignment ('unique-SAT') are reachable.
Usage: python3 minwire.py n K   (each call < 30 s for n<=4,K<=3 and n=5,K<=3)"""
import sys, itertools, json
n=int(sys.argv[1]); K=int(sys.argv[2]); N=1<<n; M=(1<<N)-1
inp=[]
for i in range(n):
    t=0
    for x in range(N):
        if (x>>i)&1: t|=1<<x
    inp.append(t)
def gate(op,a,b):  # op 0..15 truth table over (a,b)
    r=0
    if op&1:  r|=(~a&~b)&M
    if op&2:  r|=(a&~b)&M
    if op&4:  r|=(~a&b)&M
    if op&8:  r|=a&b
    return r
best={}  # truth table -> min gates
def rec(nodes,k):
    out=nodes[-1]
    if out not in best or best[out]>k: best[out]=k
    if k==K: return
    L=len(nodes)
    for i in range(L):
        for j in range(i+1,L):
            for op in range(16):
                rec(nodes+[gate(op,nodes[i],nodes[j])],k+1)
# only the final gate matters for 'output'; every prefix node is also an output of a smaller circuit
for t in inp: best[t]=0
rec(list(inp),0)
uniq={t:k for t,k in best.items() if bin(t).count('1')==1}
res={"n":n,"K":K,"unique_sat_functions_total":N,
     "unique_sat_reached":len(uniq),
     "min_gates_histogram":{},"all_dependent_mingate":None}
for k in uniq.values(): res["min_gates_histogram"][k]=res["min_gates_histogram"].get(k,0)+1
print(json.dumps(res))
