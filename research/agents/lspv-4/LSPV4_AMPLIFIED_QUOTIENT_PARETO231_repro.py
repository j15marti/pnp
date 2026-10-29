#!/usr/bin/env python3
"""Exact finite controls for LSPV-4 AMPLIFIED-QUOTIENT-PARETO231.
No external dependencies; Python 3.10+; all tests bounded by small parameters.
Never interprets enumeration proxies as SAT lower bounds.
"""
import json, math, hashlib
from collections import defaultdict, deque
from functools import lru_cache
from pathlib import Path

class Builder:
    def __init__(self, b, q):
        assert b >= 1 and q >= 2
        self.b, self.q = b, q
        self.r = q - 2
        self.num_vars = b
        self.Y = set(range(b))
        self.clauses = []  # tuples (variable index, positive bool)
        self.modules = []
        self.make()
    def new(self):
        x = self.num_vars
        self.num_vars += 1
        return x
    def add_module(self, kind, boundary):
        if kind == 'leaf':
            a, bb, c, d, e = [self.new() for _ in range(5)]
            scopes = [ (boundary[0], a, bb), (a, c, d), (a, c, e),
                       (a, d, e), (bb, c, d), (bb, c, e), (bb, d, e) ]
            pos_indices = {a:{0,1}, bb:{0,4}, c:{1,2}, d:{1,3}, e:{5,6}}
            hit = {a,bb}
            swapi = 1
            private = {a,bb,c,d,e}
        else:
            a, bb, c, d = [self.new() for _ in range(4)]
            scopes = [(boundary[0],a,bb), (boundary[1],c,d),
                      (a,bb,c), (a,bb,d), (a,c,d), (bb,c,d)]
            pos_indices = {a:{0,2},bb:{0,2},c:{1,4},d:{3,5}}
            hit = {a,c}
            swapi = 4
            private = {a,bb,c,d}
        ids=[]
        for ci, scope in enumerate(scopes):
            lits=[]
            for x in scope:
                lits.append((x, None if x in self.Y else ci in pos_indices[x]))
            ids.append(len(self.clauses))
            self.clauses.append(tuple(lits))
        rec = {'kind':kind,'boundary':tuple(boundary),'private':set(private),
               'base_vars':set(private),'ids':ids,'hit':set(hit),
               'swap_clause':ids[swapi], 'swap_var':c, 'x':[]}
        self.modules.append(rec)
        return rec
    def attach_cycle(self, rec):
        r=self.r
        if not r: return
        x=[self.new() for _ in range(3*r)]
        rec['x']=x
        rec['private'].update(x)
        rec['hit'].update(x[::3])
        newids=[]
        for i in range(3*r):
            ci=[(x[i],True),(x[(i+1)%(3*r)],True),(x[(i+2)%(3*r)],False)]
            newids.append(len(self.clauses));self.clauses.append(tuple(ci))
        for i in range(r):
            ci=[(x[3*i],False),(x[3*i+1],False),(x[3*i+2],False)]
            newids.append(len(self.clauses));self.clauses.append(tuple(ci))
        rec['ids'].extend(newids)
        baseidx=rec['swap_clause'];cycleidx=newids[0]
        base=list(self.clauses[baseidx]); cyc=list(self.clauses[cycleidx])
        ib=next(i for i,(v,s) in enumerate(base) if v==rec['swap_var'])
        assert base[ib][1] is True and cyc[1]==(x[1],True)
        base[ib],cyc[1]=cyc[1],base[ib]
        self.clauses[baseidx]=tuple(base)
        self.clauses[cycleidx]=tuple(cyc)
    def make(self):
        for i in range(self.b-1):
            self.add_module('connector',(i,i+1))
        for i in range(self.b):
            degree=(i>0)+(i<self.b-1)
            for _ in range(4-degree):
                self.add_module('leaf',(i,))
        assert len(self.modules)==3*self.b+1
        for mod in self.modules:self.attach_cycle(mod)
        yloc=defaultdict(list)
        for ci, clause in enumerate(self.clauses):
            for li,(v,s) in enumerate(clause):
                if v in self.Y:
                    assert s is None
                    yloc[v].append((ci,li))
        for v in self.Y:
            assert len(yloc[v]) == 4
            for j,(ci,li) in enumerate(yloc[v]):
                c=list(self.clauses[ci]);c[li]=(v,j<2);self.clauses[ci]=tuple(c)
    def witness(self):
        A={v:True for v in range(self.num_vars)}
        for mod in self.modules:
            for i,x in enumerate(mod['x']): A[x]=(i%3 in (0,1))
        return A
    def sat(self,A):
        return all(any(A[v]==p for v,p in c) for c in self.clauses)
    def validate(self):
        n=self.num_vars;b=self.b;q=self.q
        assert n==(9*q-3)*b+3*q
        assert len(self.clauses)==4*n//3
        assert len(self.modules)==3*b+1
        assert self.sat(self.witness())
        # Every boundary value extends to a model, not just the all-true boundary.
        if b <= 7:
            W=self.witness()
            for bits in range(1<<b):
                for v in self.Y: W[v]=bool((bits>>v)&1)
                assert self.sat(W),('boundary failed',b,q,bits)
        counts=defaultdict(lambda:[0,0]); seen=set()
        adj=[set() for _ in range(n)]
        for c in self.clauses:
            assert len(c)==3 and len({v for v,s in c})==3
            key=tuple(sorted((v,s) for v,s in c))
            assert key not in seen,key
            seen.add(key)
            a,bb,d=[v for v,s in c]
            for v,p in c:
                counts[v][0 if p else 1]+=1
            for u,v in [(a,bb),(a,d),(bb,d)]:adj[u].add(v);adj[v].add(u)
        assert all(counts[v]==[2,2] for v in range(n))
        visit={0};queue=[0]
        for u in queue:
            for v in adj[u]:
                if v not in visit:visit.add(v);queue.append(v)
        assert len(visit)==n
        allpriv=set()
        # Private components are exactly the promised modules after deleting Y.
        for mod in self.modules:
            P=mod['private'];assert P.isdisjoint(allpriv)
            allpriv|=P
            start=next(iter(P));V={start};Q=[start]
            for u in Q:
                for v in adj[u] & P:
                    if v not in V:V.add(v);Q.append(v)
            assert V==P
            for cidx in mod['ids']:
                c=self.clauses[cidx]
                assert all(v in P or v in self.Y for v,p in c)
                if not any(v in self.Y for v,p in c):
                    assert any(v in mod['hit'] for v,p in c)
            assert len(mod['hit'])==q
        assert allpriv|self.Y==set(range(n))
        # No clause has private variables in two different modules.
        owner={v:i for i,m in enumerate(self.modules) for v in m['private']}
        assert all(len({owner[v] for v,p in c if v not in self.Y})<=1 for c in self.clauses)
        assert 3*b+3*len(self.modules)*q - n == 6*b
        assert math.ceil((n-3*b)/(9*b+3))==q
        return {'b':b,'q':q,'k':len(self.modules),'n':n,'m':len(self.clauses),
                't_log2':b+q,'s_table_log2':b,'integer_q_lower':q,
                'size_DIMACS_bytes':len(self.dimacs().encode('ascii')),
                'leaf_count':sum(m['kind']=='leaf' for m in self.modules),
                'connector_count':sum(m['kind']=='connector' for m in self.modules)}
    def dimacs(self):
        lines=[f'p cnf {self.num_vars} {len(self.clauses)}']
        for c in self.clauses:
            lines.append(' '.join(str(v+1 if p else -(v+1)) for v,p in c)+' 0')
        return '\n'.join(lines)+'\n'

def hitting_possible(clauses,cap):
    # Exact deterministic bounded hitting search for the finite controls.
    rows=[]
    for c in clauses:
        z=tuple(sorted({v for v,p in c}))
        if z not in rows:rows.append(z)
    d={v:0 for clause in rows for v in clause}
    for i,clause in enumerate(rows):
        for v in clause:d[v]|=1<<i
    full=(1<<len(rows))-1
    @lru_cache(None)
    def search(uncovered,remaining):
        if not uncovered:return True
        if remaining==0:return False
        first=(uncovered & -uncovered).bit_length()-1
        return any(search(uncovered & ~d[v],remaining-1) for v in rows[first])
    ans=search(full,cap)
    return ans,search.cache_info().misses

def finite_suite():
    observed=[];exhaustive=[];assertions=0
    for b in [1,2,3,4,7,10,20,36]:
        for q in [2,3,4,5,6,8,12]:
            F=Builder(b,q); observed.append(F.validate());assertions+=8+F.num_vars
            if b<=3 and q<=5:
                for mod in F.modules:
                    private_clauses=[F.clauses[i] for i in mod['ids'] if not any(v in F.Y for v,p in F.clauses[i])]
                    possible,nodes=hitting_possible(private_clauses,q-1)
                    assert not possible,(b,q,mod['kind'])
                    exhaustive.append({'b':b,'q':q,'kind':mod['kind'],'nodes':nodes})
    square=[]
    for j in [2,3,4,5,8,10,12,20]:
        F=Builder(j,j); R=F.validate()
        assert R['n']==9*j*j
        n=R['n']
        for bb in range(1, n//3+1):
            qq=max(0,(n-3*bb+9*bb+2)//(9*bb+3)) # only used to double-check below
            qq=max(0,math.ceil((n-3*bb)/(9*bb+3)))
            assert bb+qq >= 2*j
        square.append({'j':j,'n':n,'b':j,'q':j,'k':3*j+1,'min_integer_t':2*j,
                       'relaxed_continuous_min':2*(math.sqrt(n+1)-1)/3,
                       'N_DIMACS_bytes':R['size_DIMACS_bytes']})
    F=Builder(36,4)
    assert F.num_vars==1200
    special=F.validate()
    out={'run':'LSPV4_AMPLIFIED_QUOTIENT_PARETO231','theorem':'n=(9q-3)b+3q, k=3b+1, each module minimum q, q>=2',
         'cases':observed,'small_exact_hitting_checks':exhaustive,
         'square_frontier':square,'n1200_realized':special,
         'assertion_proxies':assertions,
         'status':'COMPUTATIONAL controls; symbolic proof in report; no SAT lower bound',
         'method':'deterministic exhaustive local depth-limited hitting; no random seed'}
    return out

if __name__=='__main__':
    import sys
    data=finite_suite()
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('LSPV4_AMPLIFIED_QUOTIENT_PARETO231_raw.json')
    dest.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'cases':len(data['cases']),'hitting_tests':len(data['small_exact_hitting_checks']),
                      'square_tests':len(data['square_frontier']),'assertions_proxy':data['assertion_proxies'],
                      'n1200':data['n1200_realized'], 'raw_path':str(dest)},sort_keys=True))