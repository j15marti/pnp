#!/usr/bin/env python3
"""Exact source-charged Shannon projection, DAG-hash-consing. Proof experiment only.

A circuit is a typed DAG with constants, signed literals, and associative AND/OR gates.
Forgetting one variable is Shannon restriction and OR. Every output is checked
against independent exhaustive source-function projection for n<=9.
No claim of a universal SAT shrinker or a machine-independent runtime lower bound.
"""
from pathlib import Path
import random,json,itertools,math,collections

class Store:
    def __init__(self):
        self.nodes=[('const', False),('const', True)]
        self.memo={('const',False):0,('const',True):1}
        self.calls=0
    def node(self,key):
        if key in self.memo:return self.memo[key]
        j=len(self.nodes)
        self.nodes.append(key);self.memo[key]=j
        return j
    def lit(self,x,positive):
        self.calls+=1
        return self.node(('lit',x,bool(positive)))
    def gate(self,op,terms):
        self.calls+=1
        flat=[]
        is_and=op=='and'
        identity=1 if is_and else 0
        absorb=0 if is_and else 1
        for v in terms:
            if v==absorb:return absorb
            if v==identity:continue
            key=self.nodes[v]
            if key[0]==op:flat.extend(key[1])
            else:flat.append(v)
        terms=tuple(sorted(set(flat)))
        if not terms:return identity
        if len(terms)==1:return terms[0]
        lits={}
        for v in terms:
            k=self.nodes[v]
            if k[0]=='lit':
                if k[1] in lits and lits[k[1]]!=k[2]:return absorb
                lits[k[1]]=k[2]
        return self.node((op,terms))
    def from_cnf(self,clauses):
        return self.gate('and',[self.gate('or',[self.lit(abs(x)-1,x>0) for x in c]) for c in clauses])
    def restrict(self,r,x,bit):
        memo={}
        def rec(j):
            if j in memo:return memo[j]
            t=self.nodes[j]
            if t[0]=='const':v=j
            elif t[0]=='lit':v=self.node(('const', int(t[2]) == int(bit))) if t[1]==x else j
            else:v=self.gate(t[0],(rec(k) for k in t[1]))
            memo[j]=v
            return v
        return rec(r)
    def exists(self,r,x):
        return self.gate('or',(self.restrict(r,x,0),self.restrict(r,x,1)))
    def evaluate(self,r,assign):
        seen={}
        def rec(j):
            if j in seen:return seen[j]
            t=self.nodes[j]
            if t[0]=='const':v=t[1]
            elif t[0]=='lit':v=(bool(assign[t[1]])==t[2])
            elif t[0]=='and':v=all(rec(z) for z in t[1])
            else:v=any(rec(z) for z in t[1])
            seen[j]=v
            return v
        return rec(r)
    def reachable(self,r):
        seen=set()
        def rec(k):
            if k in seen:return
            seen.add(k)
            t=self.nodes[k]
            if t[0] in ('and','or'):
                for i in t[1]:rec(i)
        rec(r)
        return sorted(seen)
    def nodesizes(self,r):
        ids=self.reachable(r)
        keys=[self.nodes[i] for i in ids]
        gate=sum(k[0] in ('and','or') for k in keys)
        edge=sum(len(k[1]) for k in keys if k[0] in ('and','or'))
        lit=sum(k[0]=='lit' for k in keys)
        # Actual declared fixed-width format: 8-bit header for type and arity,
        # indices use ceil(log2(1+num_variables+num_gates+num_literals)) bits.
        idx=max(1,math.ceil(math.log2(max([3]+[z[1]+2 for z in keys if z[0]=='lit'])+len(keys)+2)))
        # 32-bit self-delim header & 8-bit operation tag + arity length for gates
        bits=32+sum((8+idx) if k[0]=='lit' else 8 if k[0]=='const' else (8+idx+idx*len(k[1])) for k in keys)
        return dict(bits=bits,gates=gate,edges=edge,lits=lit,reachable=len(ids),index_width=idx)

def valid_cnf(clauses,n):
    return all(all(abs(x)<=n and x !=0 for x in c) for c in clauses)

def bitcnf(clauses,n):
    width=max(1,math.ceil(math.log2(n+1)))
    return 32+sum(8+len(c)*(1+width) for c in clauses)

def source_sat(clauses,assignment):
    return all(any(bool(assignment[abs(x)-1]) == (x>0) for x in c) for c in clauses)

def run_case(name,n,clauses,check=True):
    assert valid_cnf(clauses,n)
    st=Store();root=st.from_cnf(clauses)
    source=st.nodesizes(root)
    single=[]
    if check and n<=10:
        for bits in itertools.product([0,1],repeat=n):
            assert st.evaluate(root,bits)==source_sat(clauses,bits)
    for x in range(n):
        before=st.calls
        nxt=st.exists(root,x)
        costs=st.calls-before
        size=st.nodesizes(nxt)
        if check and n<=10:
            for small in itertools.product([0,1],repeat=n-1):
                y=list(small);y.insert(x,0)
                a=source_sat(clauses,y)
                y[x]=1
                b=source_sat(clauses,y)
                assert st.evaluate(nxt,y)==(a or b),(name,x,y)
        single.append(dict(x=x,**size,construct_gate_calls=costs))
    best=min(single,key=lambda a:(a['bits'],a['gates'],a['x']))
    return dict(name=name,n=n,m=len(clauses),source_cnf_bits=bitcnf(clauses,n),source_circuit=source,
                best_pivot=best,all_pivots=single,search_gate_calls=sum(k['construct_gate_calls'] for k in single),
                best_circuit_delta=best['bits']-source['bits'])

def xor_gate(a,b,c):
    return [(-a,-b,-c),(-a,b,c),(a,-b,c),(a,b,-c)]

def parity_chain(k):
    # vars x1..xk, hidden y1..y_(k-2)
    v=k
    clauses=[]
    prev=1
    for i in range(2,k):
        v+=1
        clauses+=xor_gate(prev,i,v)
        prev=v
    clauses.extend([(-prev,-k),(prev,k)]) # parity=1 at endpoint
    return v,clauses

def chain(s):
    clauses=[]
    for i in range(s):
        x=i+1;y=i+2;z=s+i+2
        clauses.extend([(-x,y,z),(-x,y,-z)])
    return 2*s+1,clauses

def random_sat(n,m,seed):
    rng=random.Random(seed)
    clauses=[]
    for _ in range(m):
        vs=rng.sample(range(1,n+1),3)
        clauses.append(tuple(v if rng.randrange(2) else -v for v in vs))
    return n,clauses

def random_strict22(n,seed):
    assert n%3==0
    rng=random.Random(seed)
    for tries in range(600):
        occ=[i*s for i in range(1,n+1) for s in (1,1,-1,-1)]
        rng.shuffle(occ)
        clauses=[tuple(occ[3*j:3*j+3]) for j in range(len(occ)//3)]
        if all(len({abs(x) for x in c})==3 for c in clauses) and len(set(clauses))==len(clauses):
            return n,clauses
    raise ValueError('failed strict22 generator')

def main():
    cases=[]
    # include complete 3-cube and sparse robust constructors
    cube=list(itertools.product([0,1],repeat=3))
    cases.append(('cube3_unsat',3,[tuple(-i-1 if b else i+1 for i,b in enumerate(w)) for w in cube]))
    for k in (4,5,6):cases.append((f'parity{k}',*parity_chain(k)))
    for s in (2,3,4):cases.append((f'chain{s}',*chain(s)))
    for n in (6,9,12):
        for seed in range(3):
            cases.append((f'strict22_n{n}_seed{seed}',*random_strict22(n,seed+20261030)))
    for n,m in ((6,24),(8,34),(9,38)):
        for seed in range(4):cases.append((f'random_n{n}_m{m}_seed{seed}',*random_sat(n,m,seed+51)))
    out=[]
    for i,(name,n,clauses) in enumerate(cases):
        x=run_case(name,n,clauses,check=n<=9)
        out.append(x)
        if i%5==0:print(name,x['source_circuit']['bits'],x['best_pivot']['bits'])
    summary={'status':'COMPUTATIONAL','model':'exact DAG Shannon existential projection; serialized size, not native TM time',
     'n_cases':len(out),'n_shrinks':sum(x['best_circuit_delta']<0 for x in out),
     'n_no_shrink':sum(x['best_circuit_delta']>=0 for x in out),'rows':out}
    with open(str(Path(__file__).resolve().parent / 'arc_mixed_projection_results.json'),'w') as f:json.dump(summary,f,indent=2)
    print('SUMMARY',summary['n_cases'],summary['n_shrinks'],summary['n_no_shrink'])
    for x in out:
        print(x['name'],'cnf',x['source_cnf_bits'],'rootcir',x['source_circuit']['bits'],'best',x['best_pivot']['bits'],'delta',x['best_circuit_delta'],'x',x['best_pivot']['x'],'charge',x['search_gate_calls'])

if __name__=='__main__':main()
