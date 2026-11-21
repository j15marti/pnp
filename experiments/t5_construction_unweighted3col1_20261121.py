"""Exact local enumeration and new unweighted-3COL compiler; no lower bound."""
import itertools as it
import json, hashlib
from collections import Counter
from pathlib import Path

TRIPLES={frozenset((i,(i+1)%5,(i+2)%5)) for i in range(5)}
def C(*a): return len(set(a))==3 and frozenset(a) in TRIPLES
def frame(): return [(i,(i+1)%5,(i+2)%5) for i in range(5)]
def exclude(a,x,p): return [(a,x,p),((a+2)%5,(a+3)%5,p)]
def graph(v,edges):
    edges=sorted(edges)
    assert len(set(edges))==len(edges) and all(0<=u<w<v for u,w in edges)
    cs=frame(); nxt=5+v
    for j in range(v):
        cs+=exclude(0,5+j,nxt)+exclude(1,5+j,nxt+1); nxt+=2
    for u,w in edges:
        l,p,q=nxt,nxt+1,nxt+2; nxt+=3
        cs.append((5+u,5+w,l));cs+=exclude(2,l,p)+exclude(4,l,q)
    assert nxt==5+3*v+3*len(edges)
    return nxt,cs
def encode(n,cs):
    assert all(len(set(t))==3 and all(0<=x<n for x in t) for t in cs)
    b=bin(len(cs)+1)[2:];w=n.bit_length()
    return '1'*n+'0'+'0'*(len(b)-1)+b+''.join(format(x+1,f'0{w}b') for t in cs for x in t)
def split(n,cs):
    # Previously proved full-domain equality path compiler, explicitly reproduced.
    copies=[[] for _ in range(n)];out=[];nxt=0
    for t in cs:
        out.append(tuple(range(nxt,nxt+3)))
        for i,x in enumerate(t):copies[x].append(nxt+i)
        nxt+=3
    for xs in copies:
        if not xs:xs.append(nxt);nxt+=1
    E=0
    for xs in copies:
        for u,v in zip(xs,xs[1:]):
            a=[u]+list(range(nxt,nxt+4));nxt+=4;E+=1
            out += [tuple(a[(i+j)%5] for j in range(3)) for i in range(5)]
            out.append((a[4],v,a[1]))
    return nxt,out,E
def local(a):
    ex=[[sum(C(a[k],x,p) and C(a[(k+2)%5],a[(k+3)%5],p) for p in range(5)) for x in range(5)] for k in range(5)]
    domain=[ex[0][x]*ex[1][x] for x in range(5)]
    edge=[[sum(C(x,y,l)*ex[2][l]*ex[4][l] for l in range(5)) for y in range(5)] for x in range(5)]
    return ex,domain,edge
def main():
    frames=[a for a in it.product(range(5),repeat=5) if all(C(*(a[i] for i in t)) for t in frame())]
    assert len(frames)==10
    interfaces=[]
    for a in frames:
        ex,d,w=local(a)
        assert ex==[[int(x!=a[k]) for x in range(5)] for k in range(5)]
        assert d==[int(x in a[2:]) for x in range(5)]
        for x,y in it.product(a[2:],repeat=2): assert w[x][y]==int(x!=y)
        interfaces.append({'frame':a,'exclude':ex,'domain':d,'edge':w})
    _,d,w=local(tuple(range(5)))
    cases=[]
    for v in range(5):
        possible=list(it.combinations(range(v),2))
        for mask in range(1<<len(possible)):
            edges=[e for j,e in enumerate(possible) if mask>>j&1]
            z3=sum(all(x[u]!=x[t] for u,t in edges) for x in it.product((2,3,4),repeat=v))
            z=0
            for x in it.product(range(5),repeat=v):
                weight=1
                for c in x:weight*=d[c]
                for u,t in edges:weight*=w[x[u]][x[t]]
                z+=weight
            assert z==z3
            n,cs=graph(v,edges);nn,out,E=split(n,cs);e=len(edges)
            assert (n,len(cs))==(5+3*v+3*e,5+4*v+5*e)
            assert (nn,len(out),E)==(55+48*v+63*e,65+58*v+77*e,10+9*v+12*e)
            assert max(Counter(i for t in out for i in t).values())<=5
            s,ss=encode(n,cs),encode(nn,out)
            row=dict(v=v,edges=edges,n=n,m=len(cs),N=len(s),n_split=nn,m_split=len(out),N_split=len(ss),E=E,colorings=z3,count=10*z3,split_count=(10*z3)<<E,status='SAT' if z3 else 'UNSAT')
            if (v==2 and e==1) or (v==4 and e==6):row.update(clauses=cs,encoding=s,split_clauses=out)
            cases.append(row)
    print(json.dumps({'lemma':'T5-UNWEIGHTED-3COL1','code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'frames':interfaces,'cases':cases,'case_count':len(cases),'seed':None,'status':'PASS','scope':'Exact local interface enumeration and 76 small graph projections; split counts use prior equality theorem, not full target enumeration.'},separators=(',',':')))
if __name__=='__main__':main()
