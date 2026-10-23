import itertools, subprocess, json, sys
def tt(n, f): return sum(1<<x for x in range(1<<n) if f([(x>>i)&1 for i in range(n)]))
def sat_fn(n,k):
    # inputs: clause c, variable v: p[c][v] (pos literal in clause), q[c][v] (neg literal). order p then q per clause.
    N=2*n*k
    def f(bits):
        P=[[bits[c*2*n+v] for v in range(n)] for c in range(k)]
        Q=[[bits[c*2*n+n+v] for v in range(n)] for c in range(k)]
        for a in itertools.product([0,1],repeat=n):
            if all(any((a[v] and P[c][v]) or ((not a[v]) and Q[c][v]) for v in range(n)) for c in range(k)): return 1
        return 0
    return N,f
rows=[]
for (n,k) in [(1,1),(1,2),(2,1)]:
    N,f=sat_fn(n,k); t=tt(N,f)
    # exact_synth supports n<=4 inputs
    g=int(subprocess.check_output(['./exact_synth',str(N),str(t)]).split()[0])
    rows.append(dict(vars=n,clauses=k,inputs=N,exact_gates=g,wires=2*g,trivial_lb=N-1,naive_ub=(2**n)*n*k-1))
# n=1,k=3 has 6 inputs: use relevance lower bound (5) and explicit upper bound (5)
N,f=sat_fn(1,3)
rows.append(dict(vars=1,clauses=3,inputs=6,exact_gates='5 (lb=ub)',wires=10,trivial_lb=5,naive_ub=5))
N,f=sat_fn(2,2)
# relevance check n=2,k=2: every input matters
t=tt(N,f); rel=[any(f([(x>>b)&1 for b in range(N)])!=f([((x^(1<<i))>>b)&1 for b in range(N)]) for x in range(1<<N)) for i in range(N)]
rows.append(dict(vars=2,clauses=2,inputs=8,exact_gates='unknown',wires='?',trivial_lb=7,naive_ub=15,all_inputs_relevant=all(rel)))
json.dump(rows,open('results.json','w'),indent=1); [print(r) for r in rows]
