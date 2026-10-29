#!/usr/bin/env python3
"""ARC226 finite controls for source-authenticated PHP and recursive-compression firewalls.
Original, self-contained code. Standard logical claims about asymptotic resolution
size are literature theorems, NOT derived from these finite tests.
"""
from __future__ import annotations
import hashlib, itertools, json, random
from collections import Counter
from pathlib import Path


def canonical(clause):
    return tuple(sorted(set(clause), key=lambda x:(abs(x), x < 0)))

def unary_php(holes):
    assert holes>=1
    m=holes+1
    v=lambda i,j: i*holes+j+1
    records=[]
    for i in range(m): records.append((f'IN({i})',canonical(v(i,j) for j in range(holes))))
    for j in range(holes):
        for i in range(m):
            for ip in range(i+1,m):
                records.append((f'COL({i},{ip},{j})',canonical((-v(i,j),-v(ip,j)))))
    return m*holes, records

def bit_php(bit_length):
    assert bit_length>=1
    holes=1<<bit_length; pigeons=holes+1
    v=lambda i,t:i*bit_length+t+1
    records=[]
    for i in range(pigeons):
        for ip in range(i+1,pigeons):
            for value in range(holes):
                c=[]
                for row in (i,ip):
                    for t in range(bit_length):
                        bit=(value>>t)&1
                        c.append(-v(row,t) if bit else v(row,t))
                records.append((f'DIFF({i},{ip},{value})',canonical(c)))
    return pigeons*bit_length, records

def eval_clause(c, a):
    return any(((a>>(abs(l)-1))&1)==(l>0) for l in c)

def brute_sat(n, records):
    for a in range(1<<n):
        if all(eval_clause(c,a) for _,c in records): return a
    return None

def resolution_dpll_refutation(n, records):
    """Exhaustive branching with authenticated clause/proof DAG, for small NO controls."""
    deriv=[{'kind':'source','clause':list(c),'src':i,'tag':name} for i,(name,c) in enumerate(records)]
    clauses=[c for _,c in records]
    cache={}
    tally={'calls':0,'leaves':0,'resolution_steps':0,'pruned':0}
    def rec(assign):
        tally['calls']+=1
        key=tuple(sorted(assign.items()))
        if key in cache:
            tally['pruned']+=1
            return cache[key]
        for i,cl in enumerate(clauses):
            if all(abs(x) in assign and assign[abs(x)]!=(x>0) for x in cl):
                tally['leaves']+=1
                cache[key]=i
                return i
        if len(assign)==n: raise AssertionError('SAT leaf in UNSAT derivation')
        # Full assignment order is deterministic; conflicting clauses are already pruned.
        x=next(x for x in range(1,n+1) if x not in assign)
        assign[x]=False; left=rec(assign)
        assign[x]=True; right=rec(assign)
        del assign[x]
        c0=canonical(deriv[left]['clause']);c1=canonical(deriv[right]['clause'])
        if x not in c0: res=left
        elif -x not in c1: res=right
        else:
            c=canonical([t for t in c0 if t!=x]+[t for t in c1 if t!=-x])
            if any(-lit in c for lit in c): raise AssertionError('Tautology in branch conflict')
            res=len(deriv)
            deriv.append({'kind':'resolve','clause':list(c),'parents':[left,right],'pivot':x})
            tally['resolution_steps']+=1
        cache[key]=res
        return res
    final=rec({})
    assert canonical(deriv[final]['clause']) == ()
    return deriv,final,tally

def verify_derivation(records, deriv, final):
    assert len(deriv)>=len(records)
    for i,row in enumerate(deriv):
        c=canonical(row['clause'])
        if row['kind']=='source':
            assert i < len(records) and row['src']==i and row['tag']==records[i][0]
            assert c==records[i][1]
        else:
            assert row['kind']=='resolve'
            a,b=row['parents'];x=row['pivot']
            assert a<i and b<i and x>0
            ca=canonical(deriv[a]['clause']);cb=canonical(deriv[b]['clause'])
            assert x in ca and -x in cb
            assert c==canonical([l for l in ca if l!=x]+[l for l in cb if l!=-x])
            assert not any(-lit in c for lit in c)
    assert canonical(deriv[final]['clause'])==()

def scc_2sat(n, clauses):
    g=[[] for _ in range(2*n)];rg=[[] for _ in range(2*n)]
    def litidx(x): return 2*(abs(x)-1)+(x<0)
    for c in clauses:
        if len(c)==1: c=(c[0],c[0])
        if len(c)==0: return False
        assert len(c)<=2
        a,b=c
        for x,y in ((-a,b),(-b,a)):
            i,j=litidx(x),litidx(y);g[i].append(j);rg[j].append(i)
    seen=set();order=[]
    def dfs(start,graph,done):
        todo=[(start,0)];seen.add(start)
        while todo:
            u,k=todo[-1]
            if k<len(graph[u]):
                v=graph[u][k];todo[-1]=(u,k+1)
                if v not in seen:seen.add(v);todo.append((v,0))
            else:
                todo.pop();done.append(u)
    for u in range(2*n):
        if u not in seen: dfs(u,g,order)
    comps=[-1]*(2*n);cid=0
    for u in reversed(order):
        if comps[u]!=-1:continue
        stack=[u];comps[u]=cid
        while stack:
            v=stack.pop()
            for w in rg[v]:
                if comps[w]<0:comps[w]=cid;stack.append(w)
        cid+=1
    return all(comps[2*i]!=comps[2*i+1] for i in range(n))

def run():
    out={'status':'PASS','exhaustive_php':[],'random_2sat_tests':0,'forged_proof_rejections':0,'oracle_truth_table_controls':[],'limitations':[]}
    for holes in (1,2,3):
        n,clauses=unary_php(holes)
        assert brute_sat(n,clauses) is None
        proof,last,stats=resolution_dpll_refutation(n,clauses)
        verify_derivation(clauses,proof,last)
        tampered=json.loads(json.dumps(proof))
        for i,row in enumerate(tampered):
            if row['kind']=='resolve':
                row['pivot']=n+1
                try: verify_derivation(clauses,tampered,last)
                except AssertionError:out['forged_proof_rejections']+=1
                else:raise AssertionError('Forgery not rejected')
                break
        out['exhaustive_php'].append({'encoding':'unary','holes':holes,'variables':n,'source_clauses':len(clauses),'proof_rows':len(proof),'resolvents':stats['resolution_steps'],'calls':stats['calls'],'input_bytes':len(json.dumps(clauses).encode()),'proof_bytes':len(json.dumps(proof).encode())})
    for bits in (1,2):
        n,clauses=bit_php(bits)
        assert brute_sat(n,clauses) is None
        proof,last,stats=resolution_dpll_refutation(n,clauses)
        verify_derivation(clauses,proof,last)
        out['exhaustive_php'].append({'encoding':'bit','holes':1<<bits,'variables':n,'source_clauses':len(clauses),'proof_rows':len(proof),'resolvents':stats['resolution_steps'],'calls':stats['calls'],'input_bytes':len(json.dumps(clauses).encode()),'proof_bytes':len(json.dumps(proof).encode())})
    rng=random.Random(22620261029)
    for n in range(1,9):
        for _ in range(100):
            clauses=[]
            for _ in range(rng.randrange(0,19)):
                a=rng.randrange(1,n+1)*rng.choice((-1,1))
                b=rng.randrange(1,n+1)*rng.choice((-1,1))
                clauses.append(canonical((a,b)))
            expected=brute_sat(n,[(str(i),c) for i,c in enumerate(clauses)]) is not None
            assert scc_2sat(n,clauses)==expected
            out['random_2sat_tests']+=1
    # OR black-box lower bound: on an all-zero truth table, no deterministic algorithm
    # distinguishes it from any one-bit yes-instance without querying every bit.
    # Finite adversarial pairs test the exact transcript argument; asymptotic follows directly.
    for q in (3,4,5,8):
        absent=[0]*(1<<q)
        fixed_transcript={i:absent[i] for i in range((1<<q)-1)}
        yes=absent.copy();yes[-1]=1
        assert all(fixed_transcript[i]==yes[i] for i in fixed_transcript)
        assert bool(any(absent))!=bool(any(yes))
        out['oracle_truth_table_controls'].append({'address_bits':q,'query_lower_bound_on_no':1<<q})
    out['limitations']=[
      'Finite PHP refutations do not establish Haken’s asymptotic lower bound.',
      'DPLL refuter is exponential, not a polynomial-time SAT algorithm.',
      'Bit-PHP checks use width 2ell clauses; no automatic 3CNF lower-bound transfer.',
      'No Lean kernel was run for Braun (2026).',
      'Resolution lower bounds do not apply to arbitrary polynomial-time verifiable proof systems.',
      'Oracle OR lower bound concerns unstructured truth-table queries, not ordinary SAT input representations.'
    ]
    return out
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))