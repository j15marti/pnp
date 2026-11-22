"""Monotone-tail cycle construction and projected semantic audit. No tape simulator."""
from itertools import product, combinations
from collections import Counter
import json
from dynamic_discovery_syndrome_trellis_20261122 import solve, oracle

def generate(q, p):
    if q < 1 or not 0 <= p < 6*q:
        raise ValueError("q>=1 and 0<=p<6q required")
    top = "C"*(6*q) + "A"*(2*q)
    bottom = "C"*p + "A" + "C"*(6*q-p-1) + "A"*(2*q)
    rows = [(2*j, 2*q+2*j, 4*q+2*j) for j in range(q)]
    return top, bottom, rows

def source(top, bottom, rows):
    t = len(top)
    factors = [tuple(3*i+j for j in range(3)) for i in range(2*t)]
    checks = []
    for offset, word in ((0,top),(t,bottom)):
        for i, link in enumerate(word):
            a,b,z = factors[offset+i]
            nxt = factors[offset+(i+1)%t][0 if link=="A" else 2]
            checks.append((a,b,nxt))
    for i in range(t):
        helpers=(6*t+2*i,6*t+2*i+1)
        checks.extend([(factors[i][2],*helpers),(factors[t+i][2],*helpers)])
    checks += [tuple(factors[i][2] for i in row) for row in rows]
    clauses=[]
    for scopes, valid in ((factors,lambda b:sum(b)==1),(checks,lambda b:sum(b)%2==0)):
        for scope in scopes:
            for bits in product((0,1),repeat=3):
                if not valid(bits):
                    clauses.append(tuple((-1 if bit else 1)*(v+1) for v,bit in zip(scope,bits)))
    return factors,checks,clauses

def fast(top,bottom,rows):
    if len(top)!=len(bottom) or not top:
        return "UNKNOWN"
    t=len(top)
    L=next((i for i,pair in enumerate(zip(top,bottom)) if pair==("A","A")),t)
    if L<2 or L%2 or L==t or any(a!="A" or b!="A" for a,b in zip(top[L:],bottom[L:])):
        return "UNKNOWN"
    for s in (0,1):
        z=[s^(i%2) if i<L else s for i in range(t)]
        if all(all(x>=y if link=="A" else x!=y for link in pair)
               for pair,x,y in zip(zip(top,bottom),z,z[1:]+z[:1])) and all(
                   sum(z[i] for i in row)%2==0 for row in rows):
            return True
    return False

def extend(top,bottom,z):
    t=len(top)
    values=[0]*(8*t)
    for offset,word in ((0,top),(t,bottom)):
        for i in range(t):
            a=1-z[(i-1)%t] if word[(i-1)%t]=="A" else 0
            values[3*(offset+i):3*(offset+i)+3]=[a,1-a-z[i],z[i]]
    for i in range(t):
        values[6*t+2*i+1]=z[i]
    assert all(v in (0,1) for v in values)
    return values

def counts(q):
    d,c=64*q,212*q
    g=max(3,2*((c+1)//2)+1)
    n0=d+(10*c+1)*g+2
    m0=(20*c+4)*g
    n,m=n0+m0+3,2*m0+4
    w=n.bit_length()
    N=3*n+2+2*((m+1).bit_length()-1)+3*m*(w+1)+w
    return dict(d=d,c=c,n=n,m=m,N=N)

def main():
    tally=Counter()
    for L in (2,4):
        for tail in (1,2):
            t=L+tail
            for pattern in product(("CC","AC","CA"),repeat=L):
                top="".join(x[0] for x in pattern)+"A"*tail
                bottom="".join(x[1] for x in pattern)+"A"*tail
                for rows in [()] + [(r,) for r in combinations(range(t),3)]:
                    ans=fast(top,bottom,rows)
                    assert ans==oracle(top,bottom,rows)==solve(top,bottom,rows)[0]
                    tally["cases"]+=1
                    tally["SAT" if ans else "UNSAT"]+=1
    controls=[]
    for q in (1,2,4,8):
        for p in range(6*q):
            top,bottom,rows=generate(q,p)
            label,lam,peak=solve(top,bottom,rows)
            assert label==fast(top,bottom,rows)==bool(p%2)
            assert lam==q
            assert sum(a==b=="A" for a,b in zip(top,bottom))==2*q
            if q<=2:
                assert oracle(top,bottom,rows)==label
            factors,checks,clauses=source(top,bottom,rows)
            assert len(clauses)==212*q
            assert all(len({abs(lit) for lit in row})==3 for row in clauses)
            assert max(abs(v) for row in clauses for v in row)==64*q
            if label:
                z=[i%2 if i<6*q else 0 for i in range(8*q)]
                v=extend(top,bottom,z)
                assert all(any((v[abs(lit)-1]==1)==(lit>0) for lit in row) for row in clauses)
            controls.append(dict(q=q,p=p,SAT=label,AA=2*q,lambda_max=lam,peak=peak,
                                 direct_oracle=q<=2,**counts(q)))
    assert fast("CCC","CCC",[])=="UNKNOWN"
    assert fast("CCACA","CCACA",[])=="UNKNOWN"
    print(json.dumps(dict(exhaustive=dict(tally),controls=controls,seed=None,
                         scope="projected cycle oracle; explicit source CNF and SAT extension; no compiled tape execution"),indent=2))

if __name__=="__main__":
    main()
