#!/usr/bin/env python3
"""Exact partial VALUE member for balanced rectangular pigeonhole CNFs.

Read-only, seekable DIMACS source; two passes, no stored formula or edge list.
The first pass verifies format, uniqueness of negative clauses and a density
precondition BEFORE allocating O(n) arrays. This also bounds failed attempts.
Accepted formulas are recognized by clique components and row/component incidence,
not by filenames, variable naming conventions, a SAT call, or trusted metadata.
A FAIL result makes no claim about satisfiability.
"""
from __future__ import annotations
import hashlib,itertools,json,os,random,sys,time,tracemalloc
from pathlib import Path
from collections import Counter

class Reject(Exception): pass

def tokens(handle, nbytes, met):
    handle.seek(0); buf=bytearray(); max_token=max(8,len(str(nbytes))+2)
    while True:
        chunk=handle.read(1024)
        if not chunk: break
        met['source_bytes_read']+=len(chunk)
        for b in chunk:
            if b in (9,10,13,32):
                if buf:
                    yield bytes(buf).decode('ascii'); buf.clear()
            else:
                if b>127 or len(buf)>=max_token: raise Reject('invalid/oversized token')
                buf.append(b)
    if buf: yield bytes(buf).decode('ascii')

def header(handle,nbytes,met):
    ts=tokens(handle,nbytes,met)
    try:
        if next(ts)!='p' or next(ts)!='cnf': raise Reject('DIMACS header required; comments unsupported')
        ns,ms=next(ts),next(ts)
        if not ns.isdigit() or not ms.isdigit(): raise Reject('invalid header integers')
        n,m=int(ns),int(ms)
    except StopIteration: raise Reject('truncated header')
    if n<1 or m<1 or n>nbytes or m>nbytes: raise Reject('header bound')
    return n,m,ts

def integers(ts,n):
    for t in ts:
        digits=t[1:] if t.startswith('-') else t
        if not digits.isdigit() or (len(digits)>1 and digits[0]=='0') or t=='-0':
            raise Reject('noncanonical integer')
        x=int(t)
        if abs(x)>n: raise Reject('variable outside declared range')
        yield x

def recognize(path: Path):
    met=Counter(); start=time.monotonic(); result={'kind':'FAIL'}
    try:
        with path.open('rb') as handle:
            nbytes=os.fstat(handle.fileno()).st_size
            n,m,ts=header(handle,nbytes,met)
            count=arity=p=e=0; h=None; sign=None; prev_lit=None; first=None; prev_neg=None
            for x in integers(ts,n):
                if x:
                    sx=x>0
                    if sign is not None and sign!=sx: raise Reject('mixed-sign clause')
                    if prev_lit is not None and x<=prev_lit: raise Reject('unordered/repeated clause literal')
                    if arity==0: first=x
                    sign=sx; prev_lit=x; arity+=1
                    if not sx and arity>2: raise Reject('negative nonbinary clause')
                else:
                    count+=1
                    if count>m or arity<2: raise Reject('clause count/arity')
                    if sign:
                        p+=1
                        if h is None: h=arity
                        if h!=arity: raise Reject('positive rows unequal')
                    else:
                        pair=(first,prev_lit)
                        if arity!=2 or (prev_neg is not None and pair<=prev_neg):
                            raise Reject('negative pair duplicate/order')
                        prev_neg=pair; e+=1
                    arity=0; sign=None; prev_lit=None; first=None
            if arity or count!=m: raise Reject('truncated/count mismatch')
            if h is None or min(p,h)<2 or not (p<=2*h and h<=2*p):
                raise Reject('outside balanced domain')
            if n!=p*h or e!=h*p*(p-1)//2 or m!=p+e:
                raise Reject('density/count gate')
            # Only after the gate: e=Theta(n**(3/2)) on balanced dimensions.
            met['density_gate_passed']=1
            parent=list(range(n+1)); size=[1]*(n+1); degree=[0]*(n+1); row=[0]*(n+1)
            met['array_integer_slots']=4*(n+1)
            def find(v):
                while parent[v]!=v:
                    parent[v]=parent[parent[v]]; v=parent[v]; met['uf_steps']+=1
                return v
            def union(a,b):
                a,b=find(a),find(b)
                if a==b:return
                if size[a]<size[b]:a,b=b,a
                parent[b]=a; size[a]+=size[b]; met['uf_unions']+=1
            nn,mm,ts=header(handle,nbytes,met)
            if (nn,mm)!=(n,m):raise Reject('source changed')
            rp=0; sign=None; first=None
            for x in integers(ts,n):
                if x:
                    if sign is None: sign=x>0; first=x
                    if x>0:
                        if row[x]:raise Reject('variable in multiple rows')
                        row[x]=rp+1
                    elif x!=first:
                        a,b=-first,-x
                        degree[a]+=1;degree[b]+=1;union(a,b)
                else:
                    if sign:rp+=1
                    sign=None;first=None
            # Complete, simple, p-vertex components with degree p-1 are cliques.
            incidence=[]
            for v in range(1,n+1):
                root=find(v)
                if not (1<=row[v]<=p) or degree[v]!=p-1 or size[root]!=p:
                    raise Reject('degree/component/row gate')
                incidence.append((root,row[v]))
            met['incidence_pairs_stored']=n
            incidence.sort()
            if any(incidence[i]==incidence[i-1] for i in range(1,n)):
                raise Reject('row repeats in a hole component')
            result={'kind':'VALUE','answer':p<=h,'pigeons':p,'holes':h,
                    'variables':n,'negative_edges':e,'input_bytes':nbytes}
    except (Reject,UnicodeDecodeError,ValueError) as e:
        result={'kind':'FAIL','reason':str(e)}
    result['metrics']=dict(met);result['seconds']=time.monotonic()-start
    return result

def main():
    # The bounded experimental runner, not recognize(), installs the alarm.
    import orbit_first_wrapper as o
    import argparse,tempfile
    parser=argparse.ArgumentParser()
    parser.add_argument('--suite',choices=('controls','scale'),required=True)
    parser.add_argument('--holes',type=int,default=24)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    rows=[];out={'run_id':'ARC-0005-ORBIT','status':'RUNNING','cases':rows,
                'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'seed':2026100806,'scope':'Exact partial recognizer. READ-ONLY source is required to remain unchanged for both passes.'}
    rng=random.Random(2026100806)
    try:
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'input.cnf'
            if args.suite=='scale':
                cases=[(f'PHP_{p}_{args.holes}',o.php(p,args.holes)) for p in (args.holes,args.holes+1)]
            else:
                cases=[]
                for p,h in ((2,2),(2,3),(3,2),(3,3),(3,4),(4,3),(4,4)):
                    f=o.php(p,h); cases.append((f'PHP_{p}_{h}',f))
                    vs=o.variables(f); target=vs[:];rng.shuffle(target)
                    cases.append((f'renamed_{p}_{h}',o.mapped(f,dict(zip(vs,target)))))
                base=o.php(3,3)
                for j in range(40):
                    altered=list(base)
                    if j%2: altered.pop(rng.randrange(len(altered)))
                    else:altered.append(tuple(v*rng.choice((-1,1)) for v in rng.sample(range(1,10),2)))
                    cases.append((f'altered_{j}',o.canon(altered)))
                # Three 3-cliques replaced by a 9-cycle: same degree and edge count,
                # wrong component sizes. The density gate passes, later check rejects.
                cyc=[(-i,-(i%9+1)) for i in range(1,10)]
                cases.append(('cycle_not_columns',o.canon([(1,2,3),(4,5,6),(7,8,9)]+cyc)))
                # Same clique graph, rows deliberately include two vertices of a clique.
                neg=[c for c in base if c[0]<0]
                cases.append(('bad_row_incidence',o.canon(neg+[(1,4,2),(3,5,6),(7,8,9)])))
            for name,f in cases:
                o.guard();path.write_bytes(o.dimacs(f))
                tracemalloc.start();r=recognize(path)
                r['incremental_python_peak_bytes']=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
                if args.suite=='controls':
                    expected=o.brute(f)
                    if r['kind']=='VALUE': assert r['answer']==expected
                else:expected=int(name.split('_')[1])<=args.holes;assert r['kind']=='VALUE' and r['answer']==expected
                rows.append({'name':name,'expected':expected,'input_bytes':path.stat().st_size,'result':r})
            # These malformed/provenance controls MUST reject, never infer UNSAT.
            if args.suite=='controls':
                texts=['p cnf 2 2\n1 2 0\n-1 -2 0\n-1 -2 0\n',
                       'p cnf 99999999999999999999 1\n1 0\n','p cnf 2 1\n1 -2 0\n',
                       'p cnf 2 1\n1 1 0\n','p cnf 2 1\n1 2','bad header\n']
                for i,text in enumerate(texts):
                    path.write_text(text);r=recognize(path);assert r['kind']=='FAIL'
                    rows.append({'name':f'malformed_{i}','result':r})
        out['status']='PASS';out['cases_checked']=len(rows)
        out['value_returns']=sum(r['result']['kind']=='VALUE' for r in rows)
        out['fail_returns']=len(rows)-out['value_returns']
    except o.BudgetExceeded as e:
        out['status']='BLOCKED_BUDGET';out['error']=str(e)
    except Exception as e:
        out['status']='FAIL';out['error']=repr(e);raise
    finally:
        if tracemalloc.is_tracing():tracemalloc.stop()
        out['elapsed_seconds']=time.monotonic()-o.START
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
    if args.suite=='scale':
        for row in rows:print(json.dumps(row,sort_keys=True))
    return 0 if out['status']=='PASS' else 2
if __name__=='__main__':raise SystemExit(main())
