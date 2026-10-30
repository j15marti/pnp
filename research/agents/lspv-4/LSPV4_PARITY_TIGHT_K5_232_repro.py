#!/usr/bin/env python3
"""LSPV-4 parity-tight signed exact22 multi-module SAT construction.
Deterministic, no dependencies. Test chunks are bounded (typically < 10 seconds).
Outputs raw JSON; the finite experiment is not a SAT time lower bound.
"""
import json, math, sys, hashlib
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

class Family:
    def __init__(self,b,q,deficits=None):
        assert b>=1 and q>=2
        self.b,self.q=b,q
        self.deficits=deficits or {}
        self.Y=set(range(b))
        self.n=b;self.C=[];self.modules=[]
        for i in range(b-1):self.connector(i,i+1)
        for i in range(b):
            degree=int(i>0)+int(i<b-1)
            for _ in range(4-degree):self.leaf(i)
        for idx,m in enumerate(self.modules):self.attach(m,self.deficits.get(idx,0))
        loc=defaultdict(list)
        for ci,c in enumerate(self.C):
            for j,(v,s) in enumerate(c):
                if v in self.Y:
                    assert s is None
                    loc[v].append((ci,j))
        for v in self.Y:
            assert len(loc[v])==4
            for j,(ci,li) in enumerate(loc[v]):
                c=list(self.C[ci]);c[li]=(v,j<2);self.C[ci]=tuple(c)
    def new(self):
        z=self.n;self.n+=1;return z
    def new_module(self,kind,ports,scopes,positive,hitting,swap_idx,swap_var,private):
        ids=[]
        for j,scope in enumerate(scopes):
            c=tuple((v,None if v in self.Y else j in positive[v]) for v in scope)
            ids.append(len(self.C));self.C.append(c)
        self.modules.append(dict(kind=kind,ports=tuple(ports),private=set(private),base=set(private),
                            ids=ids,hit=set(hitting),swapi=ids[swap_idx],swapvar=swap_var,cyclic=[]))
    def leaf(self,y):
        a,z,c,d,e=[self.new() for _ in range(5)]
        sc=[(y,a,z),(a,c,d),(a,c,e),(a,d,e),(z,c,d),(z,c,e),(z,d,e)]
        po={a:{0,1},z:{0,4},c:{1,2},d:{1,3},e:{5,6}}
        self.new_module('leaf',[y],sc,po,{a,z},1,c,{a,z,c,d,e})
    def connector(self,yl,yr):
        h1,h2=[self.new() for _ in range(2)];u=[self.new() for _ in range(5)]
        edges=[(i,j) for i in range(5) for j in range(i+1,5)]
        # Each edge receives exactly one positive U literal according to a regular tournament.
        # First two edge clauses carry the boundary variables, four carry h1, four carry h2.
        ports=[yl,yr]+[h1]*4+[h2]*4
        sc=[(port,u[i],u[j]) for port,(i,j) in zip(ports,edges)]
        po={h1:{2,3},h2:{6,7}}
        for z in u:po[z]=set()
        for ei,(i,j) in enumerate(edges):
            if ((j-i)%5) in (1,2):po[u[i]].add(ei)
            else:po[u[j]].add(ei)
        assert all(len(po[z])==2 for z in u)
        # Exchange the positive U literal from first h1 internal clause with cyclic x1.
        ei=2
        v=next(z for z in (u[edges[ei][0]],u[edges[ei][1]]) if ei in po[z])
        self.new_module('connector',[yl,yr],sc,po,{h1,h2},ei,v,set([h1,h2]+u))
    def attach(self,m,deficit=0):
        r=self.q-2-deficit
        assert r>=0
        m['local_q']=r+2
        if r==0:return
        x=[self.new() for _ in range(3*r)];m['cyclic']=x
        m['private'].update(x);m['hit'].update(x[::3]);ids=[]
        for i in range(3*r):
            ids.append(len(self.C));self.C.append(((x[i],True),(x[(i+1)%(3*r)],True),(x[(i+2)%(3*r)],False)))
        for j in range(r):
            ids.append(len(self.C));self.C.append(((x[3*j],False),(x[3*j+1],False),(x[3*j+2],False)))
        m['ids']+=ids
        a=list(self.C[m['swapi']]);z=list(self.C[ids[0]])
        idx=next(k for k,(var,sgn) in enumerate(a) if var==m['swapvar'])
        assert a[idx][1] and z[1]==(x[1],True)
        a[idx],z[1]=z[1],a[idx]
        self.C[m['swapi']]=tuple(a);self.C[ids[0]]=tuple(z)
    def witness(self,boundary_bits=None):
        x={v:True for v in range(self.n)}
        for m in self.modules:
            for j,v in enumerate(m['cyclic']):x[v]=(j%3 != 2)
        if boundary_bits is not None:
            for v in self.Y:x[v]=bool((boundary_bits>>v)&1)
        return x
    def sat(self,x):return all(any(x[v]==s for v,s in c) for c in self.C)
    def dimacs(self):
        return (f'p cnf {self.n} {len(self.C)}\n'+''.join(' '.join(str(v+1 if s else -(v+1)) for v,s in c)+' 0\n' for c in self.C))
    def validate(self):
        b,q=self.b,self.q;k=3*b+1
        n_expected=(9*b+3)*q-3-3*sum(self.deficits.values())
        assert len(self.modules)==k and self.n==n_expected and len(self.C)==4*self.n//3
        hist=defaultdict(lambda:[0,0]);seen=set();adj=[set() for _ in range(self.n)]
        for c in self.C:
            assert len(c)==3 and len(set(v for v,s in c))==3
            code=tuple(sorted(c));assertion=code not in seen
            assert assertion,code
            seen.add(code)
            names=[v for v,s in c]
            for v,s in c:hist[v][not s]+=1
            for i in range(3):
                for j in range(i+1,3):adj[names[i]].add(names[j]);adj[names[j]].add(names[i])
        assert all(hist[v]==[2,2] for v in range(self.n))
        todo=[0];vis={0}
        for x in todo:
            for y in adj[x]:
                if y not in vis:vis.add(y);todo.append(y)
        assert len(vis)==self.n
        owner={v:i for i,m in enumerate(self.modules) for v in m['private']}
        assert set(owner)|self.Y==set(range(self.n)) and len(owner)==self.n-b
        assert all(len(set(owner[v] for v,s in c if v not in self.Y))<=1 for c in self.C)
        assert self.sat(self.witness())
        if b<=6:
            for bits in range(1<<b):assert self.sat(self.witness(bits))
        sum_delta=0;sum_a=0;leaves=0;module_summaries=[]
        for m in self.modules:
            priv=m['private'];start=next(iter(priv));seenp={start};qnext=[start]
            for u in qnext:
                for v in adj[u]&priv:
                    if v not in seenp:seenp.add(v);qnext.append(v)
            assert seenp==priv
            assert len(m['hit'])==m['local_q'] and m['local_q']<=q
            own=[self.C[idx] for idx in m['ids']]
            internal=[c for c in own if not any(v in self.Y for v,s in c)]
            assert all(any(v in m['hit'] for v,s in c) for c in internal)
            cross=[c for c in own if any(v in self.Y for v,s in c)]
            a=sum(sum(v in self.Y for v,s in c) for c in cross)
            delta=sum(sum(v in m['hit'] or v in self.Y for v,s in c)-1 for c in own)
            assert delta%4==(2*a)%4
            if a==1:assert delta>=2;leaves+=1
            assert a==len(m['ports']) and delta >=0
            sum_delta+=delta;sum_a+=a
            module_summaries.append((m['kind'],len(priv),a,delta))
        assert sum_a==4*b and leaves==2*b+2
        assert sum_delta==4*(b+sum(m['local_q'] for m in self.modules))-len(self.C)
        assert self.n==3*(b+sum(m['local_q'] for m in self.modules))-3*sum_delta//4
        assert sum_delta==4*(b+1), (b,q,sum_delta)
        assert self.n==(9*b+3)*q-3-3*sum(self.deficits.values())
        assert sum(d for typ,_,_,d in module_summaries if typ=='connector')==0
        assert all(d==2 for typ,_,_,d in module_summaries if typ=='leaf')
        return {'b':b,'q':q,'k':k,'n':self.n,'m':len(self.C),'source_bytes':len(self.dimacs().encode()),
                'leaves':leaves,'connectors':b-1,'delta':sum_delta,
                'leaf_delta':2,'connector_delta':0,'amplification_deficits':sum(self.deficits.values()),'realized_t_log2_proxy':b+q,
                'realized_s_log2_optional_table':b}


def hitting_possible(rows,cap):
    cols=[]
    for c in rows:
        group=tuple(sorted({v for v,s in c}));
        if group not in cols:cols.append(group)
    cover={v:0 for col in cols for v in col}
    for i,col in enumerate(cols):
        for v in col:cover[v]|=1<<i
    @lru_cache(None)
    def solve(uncovered,remaining):
        if uncovered==0:return True
        if remaining==0:return False
        first=(uncovered & -uncovered).bit_length()-1
        return any(solve(uncovered&~cover[v],remaining-1) for v in cols[first])
    result=solve((1<<len(cols))-1,cap)
    return result,solve.cache_info().misses


def lower_q_old(n,b):return max(0,math.ceil((n-3*b)/(12*b)))
def lower_q_quotient(n,b):return max(0,math.ceil((n-3*b)/(9*b+3)))
def lower_q_parity(n,b):return 0 if 3*b>=n else max(1,math.ceil((n+3)/(9*b+3)))
def full_frontier(n):
    records=[]
    for b in range(1,n//3+1):
        a=lower_q_old(n,b);c=lower_q_quotient(n,b);d=lower_q_parity(n,b)
        assert a<=c<=d
        records.append({'b':b,'old_q':a,'quotient_q':c,'parity_q':d,
                        'old_t':b+a,'quotient_t':b+c,'parity_t':b+d,
                        's_table_log2':b})
    result={}
    for key in ['old','quotient','parity']:
        t=min(row[key+'_t'] for row in records)
        result[key]={'t_min':t,'argmin':[[r['b'],r[key+'_q']] for r in records if r[key+'_t']==t]}
    result['q_changed_by_parity_vs_quotient']=sum(r['parity_q']!=r['quotient_q'] for r in records)
    return result,records

def main():
    cases=[];exact=[];square=[]
    for b in [1,2,3,4,7,12]:
        for q in [2,3,4,5,8,12]:
            f=Family(b,q)
            cases.append(f.validate())
            if b<=3 and q<=5:
                for m in f.modules:
                    C=[f.C[i] for i in m['ids'] if all(v not in f.Y for v,s in f.C[i])]
                    flag,nodes=hitting_possible(C,q-1)
                    assert not flag,(b,q,m['kind'])
                    exact.append({'b':b,'q':q,'kind':m['kind'],'search_nodes':nodes})
    for j in [2,3,4,5,8,10]:
        f=Family(j,j);row=f.validate()
        fnt,_=full_frontier(row['n'])
        assert fnt['parity']['t_min']==2*j and [j,j] in fnt['parity']['argmin'],(j,fnt)
        square.append({'j':j,'n':row['n'],'t_global_integer_min':2*j,'b':j,'q':j,'N_bytes':row['source_bytes']})
    frontiers={}
    for n in [21,36,900,1200,2700]:
        result,records=full_frontier(n)
        frontiers[str(n)]=result
    special=Family(10,13,{0:1,1:1}).validate()
    assert special['n']==1200 and special['q']==13
    f1200,_=full_frontier(1200)
    assert f1200['parity']['t_min']==23 and [10,13] in f1200['parity']['argmin']
    # New parity tightening is strict for some admissible integer n,b:
    assert lower_q_quotient(36,1)==3 and lower_q_parity(36,1)==4
    assert frontiers['2700']['quotient']['t_min']==34 and frontiers['2700']['parity']['t_min']==35
    raw={ 'run_id':'LSPV4_PARITY_TIGHT_K5_232', 'status':'PROVED/EXACT symbolic theorem separately; COMPUTATIONAL finite tests',
          'cases':cases,'exact_private_hitting_tests':exact,'square_global_optima':square,
          'proxy_frontiers':frontiers,'n1200_realized_optimum':special,'source':'standalone Python 3 standard library',
          'scope':'connected strict signed exact22 3CNF, fixed private components, residual syntactic hitting sets',
          'not_a_SAT_lower_bound':True }
    out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('LSPV4_PARITY_TIGHT_K5_232_raw.json')
    out.write_text(json.dumps(raw,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'full_cases':len(cases),'exact_hitting_modules':len(exact),'square_verified':len(square),
          'n2700_quotient':frontiers['2700']['quotient']['t_min'],'n2700_parity':frontiers['2700']['parity']['t_min'], 'n1200_realized_b_q':[special['b'],special['q']],
          'output':str(out)},sort_keys=True))

if __name__=='__main__':main()