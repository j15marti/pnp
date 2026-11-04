#!/usr/bin/env python3
"""LSPV2/374 public compact reproducer, no dependencies or SAT oracle.
The full independently verified proof DAG producer/checker and raw certificates
are included in LSPV2_PARITY_PORT_COMPRESSION374_2026-11-03.zip.
This public script authenticates both boundary relations and the charge-count.
"""
import json
from itertools import product

def blocking(k, a):
    return tuple(-(j+1) if (a >> j)&1 else j+1 for j in range(k))

def parity_port(k, rhs):
    out=[]
    for a in range(1<<k):
        if (a.bit_count()&1)!=rhs:
            out.append(blocking(k,a))
    return out

def xor_gate(a,b,y):
    return [[a if u==0 else -a, b if v==0 else -b,
             y if w==0 else -y]
            for u,v in product((0,1),repeat=2)
            for w in (1-(u^v),)]

def compact(k, rhs_b=1):
    assert k>=2
    n=k; rails=[]; src=[]
    for rhs in (0,rhs_b):
        previous=1
        for j in range(2,k+1):
            n+=1
            src.extend(xor_gate(previous,j,n))
            previous=n
        src.extend([[previous if rhs else -previous]]*2)
        rails.append(previous)
    return {'variables':n,'clauses':src,'outputs':rails}

def truth_clause(cl, assign):
    return any((bool(assign.get(abs(t),0)) if t>0
                else not bool(assign.get(abs(t),0))) for t in cl)

def projected(k,rhs):
    side=compact(k,rhs_b=rhs)
    # This separately checks the 0/0 SAT neighbor.
    for a in range(1<<k):
        x={i+1:(a>>i)&1 for i in range(k)}
        vals=dict(x)
        for s in range(2):
            previous=x[1]
            for j in range(2,k+1):
                y=k+s*(k-1)+(j-1)
                previous=previous^x[j]
                vals[y]=previous
        actual=all(truth_clause(cl,vals) for cl in side['clauses'])
        expected=(a.bit_count()&1)==0 if rhs==0 else False
        assert actual==expected
    return side

def authentic_full_blocking(k, source):
    """Explicit scan and a materialized 2**k bitmap, O(N_input) memory."""
    if len(source)!=(1<<k):return False
    marked=bytearray(1<<k)
    for cl in source:
        if len(cl)!=k or {abs(t) for t in cl}!=set(range(1,k+1)):
            return False
        a=sum(1<<(abs(t)-1) for t in cl if t<0)
        if marked[a]:return False
        marked[a]=1
    return all(marked)

def main():
    records=[]
    for k in range(1,9):
        ports=[parity_port(k,0),parity_port(k,1)]
        full=ports[0]+ports[1]
        assert authentic_full_blocking(k,full[::-1])
        assert all(sum(not truth_clause(c,{j+1:(a>>j)&1
                   for j in range(k)}) for c in full)==1
                   for a in range(1<<k))
        entry={'k':k,'full_sources':len(full),'full_exact_paid':(1<<k)-1}
        if k>=2:
            comp=compact(k,1)
            sat=compact(k,0)
            assert len(comp['clauses'])==8*k-4
            assert comp['variables']==3*k-2
            assert all(truth_clause(cl,{}) for cl in sat['clauses'])
            for a in range(1<<k):
                x={i+1:(a>>i)&1 for i in range(k)}
                value=dict(x)
                for side in range(2):
                    prev=x[1]
                    for j in range(2,k+1):
                        y=k+side*(k-1)+j-1
                        prev^=x[j]
                        value[y]=prev
                gates=comp['clauses'][:-4]
                assert all(truth_clause(cl,value) for cl in gates)
                left=all(truth_clause(cl,value) for cl in comp['clauses'][-4:-2])
                right=all(truth_clause(cl,value) for cl in comp['clauses'][-2:])
                assert left == ((a.bit_count()&1)==0)
                assert right == ((a.bit_count()&1)==1)
                assert not(left and right)
            entry.update(compact_sources=len(comp['clauses']),
                         compact_paid_upper=8*k-5)
        records.append(entry)
    print(json.dumps({'status':'PASS','records':records,
                      'source_lower_bound':'previous theorem LSPV2/344',
                      'mixed_upper_certificate':'full archive checker, not this program',
                      'B3':'OPEN'},indent=2))

if __name__=='__main__':main()
