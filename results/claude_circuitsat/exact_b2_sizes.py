"""Exact minimum B2 circuit sizes (gates; wires = 2*gates, fan-in 2) for n-variable functions.
Normal-chain BFS over sets of computed truth tables. Usage: python3 exact_b2_sizes.py n maxgates
Cost of f = cost of ~f (free output negation). Run time per call kept well under 30s for (3,5),(4,3)."""
import sys, json, itertools
n=int(sys.argv[1]); K=int(sys.argv[2])
N=1<<n; M=(1<<N)-1
inputs=[sum(1<<i for i in range(N) if (i>>v)&1) for v in range(n)]
ops=[lambda a,b:a&b, lambda a,b:a&~b&M, lambda a,b:~a&b&M, lambda a,b:a|b, lambda a,b:a^b]
cost={0:0}
for x in inputs: cost[x]=0
def norm(f): return f if not f&1 else (~f)&M
level={frozenset(inputs)}
cnt=[len(level)]
for k in range(1,K+1):
    nxt=set()
    for st in level:
        L=sorted(st)
        for a,b in itertools.combinations(L,2):
            for op in ops:
                g=op(a,b)
                if g in st: continue
                if g not in cost: cost[g]=k
                nxt.add(st|{g})
    level=nxt; cnt.append(len(level))
    print(f"gates={k} states={len(level)} functions_cost<=k:{len(cost)}",flush=True)
# report over all functions (via normalization)
hist={}
for f in range(1<<N):
    c=cost.get(norm(f)); 
    hist[c]=hist.get(c,0)+1
print("n",n,"cost histogram over all 2^2^n functions (None = >K):",dict(sorted(hist.items(),key=lambda t:(t[0] is None,t[0]))))
named={}
pop=lambda f:bin(f).count("1")
def tt(fn): return sum(1<<i for i in range(N) if fn([(i>>v)&1 for v in range(n)]))
named["AND"]=tt(lambda x:all(x)); named["OR"]=tt(lambda x:any(x)); named["XOR"]=tt(lambda x:sum(x)%2)
named["MAJ"]=tt(lambda x:sum(x)*2>n); named["EXACT1"]=tt(lambda x:sum(x)==1); named["MOD3=0"]=tt(lambda x:sum(x)%3==0)
named["THR2"]=tt(lambda x:sum(x)>=2); named["MUX/ITE(x0?x1:x2)"]=tt(lambda x:x[1] if x[0] else x[2]) if n>=3 else 0
res={k:cost.get(norm(v),">%d"%K) for k,v in named.items()}
print(res)
json.dump({"n":n,"K":K,"states":cnt,"hist":{str(k):v for k,v in hist.items()},"named_cost_gates":res},open(f"results/claude_circuitsat/b2_exact_n{n}_K{K}.json","w"),indent=1)
