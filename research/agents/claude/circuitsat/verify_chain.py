# Verify: AND-chain circuit on n inputs is SAT; each of its 2(n-1) input wires,
# when rewired to constant 0 ("wire cut"), gives UNSAT. Hence every wire is
# individually critical (adversary lower bound on wire reads).
import itertools, json
def sat(n, cut=None):
    # gates g_1..g_{n-1}; g_i = A_i AND B_i; A_1=x_1, B_1=x_2, A_i=g_{i-1}, B_i=x_{i+1}
    wires=[]
    for i in range(1,n):
        wires.append(('x',1) if i==1 else ('g',i-1)); wires.append(('x',i+1))
    for xs in itertools.product([0,1],repeat=n):
        v={}
        for i in range(1,n):
            a=wires[2*(i-1)]; b=wires[2*(i-1)+1]
            def val(w,k):
                if cut==k: return 0
                return xs[w[1]-1] if w[0]=='x' else v[w[1]]
            v[i]=val(a,2*(i-1)) & val(b,2*(i-1)+1)
        if v[n-1]: return True
    return False
res={}
for n in range(2,9):
    ok=sat(n) and all(not sat(n,k) for k in range(2*(n-1)))
    res[n]={'wires':2*(n-1),'all_critical':ok}
    assert ok
json.dump(res,open('verify_chain_results.json','w'),indent=1); print(res)
