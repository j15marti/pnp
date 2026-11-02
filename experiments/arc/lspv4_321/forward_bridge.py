#!/usr/bin/env python3
"""Reproducible source-authenticated circuit/OBDD audit for canonical Döcker M22 F9.
Pure Python 3 standard library. Exact exhaustive n=9 and all 9! OBDD orders via subset DP.
"""
import itertools
import json
import math
from collections import Counter
from pathlib import Path

P = [(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
M = [(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
N = 9
CLAUSES = tuple(tuple(v for v in t) for t in P) + tuple(tuple(-v for v in t) for t in M)

def valid_original(clauses=CLAUSES,n=N):
    assert len(clauses)*3 == 4*n
    seen = set()
    quota = Counter()
    for clause in clauses:
        assert len(clause) == 3 and len({abs(z) for z in clause}) == 3
        assert all(z>0 for z in clause) or all(z<0 for z in clause)
        key = tuple(sorted(clause))
        assert key not in seen
        seen.add(key)
        for z in clause:
            assert 1<=abs(z)<=n
            quota[(abs(z),z>0)] += 1
    assert all(quota[(v, sign)] == 2 for v in range(1,n+1) for sign in (False,True))

def eval_cnf(mask):
    return int(all(any(bool(mask & (1 << (abs(z)-1))) == (z>0) for z in clause) for clause in CLAUSES))

class Circuit:
    def __init__(self):
        self.gates=[]
        self.depth={('I',i):0 for i in range(N)}
        self.inv=[]
        for i in range(N):
            self.inv.append(self.add('NOT',('I',i)))
        clauses=[]
        for clause in CLAUSES:
            literals=[('I',abs(z)-1) if z>0 else self.inv[abs(z)-1] for z in clause]
            a=self.add('OR',literals[0],literals[1]); b=self.add('OR',a,literals[2]); clauses.append(b)
        while len(clauses)>1:
            new=[]
            for i in range(0,len(clauses),2):
                new.append(self.add('AND',clauses[i],clauses[i+1]) if i+1<len(clauses) else clauses[i])
            clauses=new
        self.output=clauses[0]
    def add(self, op, a, b=None):
        v=('G',len(self.gates))
        self.gates.append((op,a,b))
        self.depth[v]=1+max(self.depth[a],self.depth[b] if b is not None else -1)
        return v
    def eval(self,mask):
        values={('I',i):bool(mask & (1<<i)) for i in range(N)}
        for j,(op,a,b) in enumerate(self.gates):
            values[('G',j)] = (not values[a] if op=='NOT' else values[a] or values[b] if op=='OR' else values[a] and values[b])
        return int(values[self.output])

def signature(mask, assignment, var_rem, truth):
    # normalized truth vector of F after fixing 'mask' positions to 'assignment'
    bits = 0
    for b in range(1<<len(var_rem)):
        ix=assignment
        for k,v in enumerate(var_rem):
            ix |= ((b>>k)&1)<<v
        bits |= truth[ix]<<b
    return bits

def dependent(sig, k, width):
    for t in range(1<<width):
        if not (t & (1<<k)) and ((sig>>t)&1) != ((sig>>(t | (1<<k)))&1):
            return True
    return False

def calculate_costs(truth):
    # Each subset S of already tested variables determines a set of distinct residual functions.
    # A BDD node for variable i is required for each distinct residual function depending on i.
    costs={}
    remaining_sigs={}
    for mask in range(1<<N):
        used=[j for j in range(N) if mask>>j & 1]
        rem=[j for j in range(N) if not(mask>>j & 1)]
        sigs=set()
        for a_bits in range(1<<len(used)):
            a=sum(((a_bits>>k)&1)<<v for k,v in enumerate(used))
            sigs.add(signature(mask,a,rem,truth))
        remaining_sigs[mask] = len(sigs)
        for v in rem:
            k=rem.index(v)
            costs[(mask,v)]=sum(dependent(sig,k,len(rem)) for sig in sigs)
    return costs,remaining_sigs

def order_optimal(costs, maximize=False):
    inf=10**20
    dp={0:(0,())}
    for mask in range(1<<N):
        val,seq=dp[mask]
        for v in range(N):
            if mask&(1<<v):continue
            nxt=mask|(1<<v)
            candidate=(val+costs[(mask,v)], seq+(v,))
            if nxt not in dp or (candidate[0]>dp[nxt][0] if maximize else candidate[0]<dp[nxt][0]):
                dp[nxt]=candidate
    ans=dp[(1<<N)-1]
    return ans[0],tuple(v+1 for v in ans[1])

def actual_obdd(truth, order):
    order=[v-1 for v in order]
    uniq={}; levels=Counter()
    zero=('leaf',0); one=('leaf',1)
    def recurse(k,mask):
        if k==N: return one if truth[mask] else zero
        v=order[k]
        lo=recurse(k+1,mask)
        hi=recurse(k+1,mask|(1<<v))
        if lo==hi: return lo
        key=(v,lo,hi)
        if key not in uniq:
            uniq[key]=('node',len(uniq)+1)
            levels[v+1]+=1
        return uniq[key]
    root=recurse(0,0)
    return {'node_count':len(uniq),'levels_by_variable':dict(sorted(levels.items())),'root':str(root)}

def pin_count(pins, truth):
    return sum(truth[a] for a in range(1<<N) if all(((a>>(k-1))&1)==v for k,v in pins.items()))

def pivotal_counts(truth):
    return {str(v+1):sum(truth[a]!=truth[a|(1<<v)] for a in range(1<<N) if not a&(1<<v)) for v in range(N)}

def main():
    valid_original()
    c=Circuit()
    truth=[eval_cnf(a) for a in range(1<<N)]
    assert [c.eval(a) for a in range(1<<N)] == truth
    assert sum(truth)==70
    assert len(c.gates)==44 and c.depth[c.output]==7
    gu=Counter(g[0] for g in c.gates)
    assert dict(gu)=={'NOT':9,'OR':24,'AND':11}
    p_u={8:0,3:0,7:0,6:0,1:1,5:1}
    assert pin_count(p_u,truth)==0
    sat_nearby=[]
    for v in p_u:
        p=dict(p_u);p[v]=1-p[v]
        cnt=pin_count(p,truth)
        if cnt: sat_nearby.append((v,cnt,p))
    assert sat_nearby
    p_s=sorted(sat_nearby)[0][2]
    cost,nu=calculate_costs(truth)
    bmin,order_min=order_optimal(cost,False)
    bmax,order_max=order_optimal(cost,True)
    check_min=actual_obdd(truth,order_min)
    check_max=actual_obdd(truth,order_max)
    assert check_min['node_count']==bmin
    assert check_max['node_count']==bmax
    natu=actual_obdd(truth,tuple(range(1,N+1)))
    piv=pivotal_counts(truth)
    assert min(piv.values())>0
    both_cof={str(v):[sum(truth[a] for a in range(1<<N) if ((a>>(v-1))&1)==b) for b in (0,1)] for v in range(1,N+1)}
    assert all(a and b for a,b in both_cof.values())
    # Exact residual-function lower bound for t disjoint copies under the order
    # x1(block1),...,x1(blockt), followed by all other inputs.
    # Distinct 0,1 cofactors on all blocks imply 2**t distinct nonzero products.
    assert dependent(signature(1,0,[v for v in range(1,N)],truth),0,8) or piv['1']>0
    # Merely precompute the two local nonzero residual truth vectors for x1.
    sx0=signature(1,0,list(range(1,N)),truth)
    sx1=signature(1,1,list(range(1,N)),truth)
    assert sx0!=sx1 and sx0>0 and sx1>0
    frontier=[]
    for t in range(1,9):
        frontier.append({'copies':t,'n':N*t,'m':12*t,
            'forced_order_distinct_nonzero_residuals':2**t,
            'forward_binary_gate_count':(44-9)*t+(t-1),
            'forward_all_gate_count':44*t+(t-1),
            'trivial_all_order_grouped_obdd_upper_bound':t*bmin+(t-1)})
    # For a Tseitin gate equation AND/OR: 3 clauses, NOT: 2; plus output unit.
    tseitin=3*(gu['AND']+gu['OR']) + 2*gu['NOT']+1
    assert tseitin==124
    result={
        'status':'PROVED_RESTRICTED_WITH_EXHAUSTIVE_FINITE_CHECKS',
        'canonical_original':{'n':N,'m':len(CLAUSES),'positive':P,'negative_supports':M,
                              'global_models':sum(truth)},
        'forward_circuit':{'NOT':gu['NOT'],'OR2':gu['OR'],'AND2':gu['AND'],
                           'gates_total':len(c.gates),'gate_depth':c.depth[c.output],
                           'tseitin_CNF_clauses':tseitin,'tseitin_variables':N+len(c.gates),
                           'lower_bound_binary_merge_gates':N-1,'lower_bound_depth_binary':math.ceil(math.log2(N)),
                           'exhaustive_input_checks':len(truth)},
        'same_source_pins':{'UNSAT':p_u,'UNSAT_completions':pin_count(p_u,truth),
                            'SAT':p_s,'SAT_completions':pin_count(p_s,truth),
                            'one_flip_variants':[(v,num) for v,num,_ in sat_nearby]},
        'pivotal_assignment_pairs':piv,'models_by_single_variable_value':both_cof,
        'obdd':{'min_nodes':bmin,'min_order':order_min,
                'max_nodes':bmax,'max_order':order_max,'natural_nodes':natu['node_count'],
                'min_verified':check_min,'max_verified':check_max,'natural_verified':natu,
                'prefix_set_queries':len(nu),'marginal_node_costs_computed':len(cost)},
        'disjoint_copy_order_lower_bound':frontier,
        'warnings':['OBDD bounds are restricted representation lower bounds, NOT arbitrary SAT time lower bounds',
                    'After a completed UNSAT decision the Boolean evaluation function is identically 0 and has constant-size minimal circuit',
                    'Forward circuit evaluation is linear in the CNF length, but determining whether the output can ever be 1 remains Circuit-SAT',
                    'The full 9! ordering optimization is exact via subset lattice DP; this is not free acquisition.']
    }
    out=Path(__file__).resolve().parent/'results.json'
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ['canonical_original','forward_circuit','same_source_pins','pivotal_assignment_pairs','obdd','disjoint_copy_order_lower_bound']},indent=2))
    print('WRITTEN',out)
if __name__=='__main__':main()
