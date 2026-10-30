"""Standalone finite affine-interface258 falsifier. Python 3 standard library."""
import itertools

def xor_clauses(scope, rhs):
    result=[]
    for bits in itertools.product((0,1), repeat=len(scope)):
        if sum(bits)%2 == rhs: continue
        result.append(tuple(-v if bit else v for v,bit in zip(scope,bits)))
    return result

def holds(F,a):
    return all(any(a[abs(l)]==int(l>0) for l in clause) for clause in F)

def build(last_sign):
    F=[]; E=[]
    for i in range(1,7):
        p=i+8
        for vs in ((i,8,p),(i+1,8,p)):
            E.append(vs)
            F += xor_clauses(vs,0)
    F += [(1,), (7 if last_sign else -7,)]
    return F,E

def rank(rows):
    pivots={}
    for a in rows:
        while a:
            p=(a&-a).bit_length()-1
            if p not in pivots:
                pivots[p]=a; break
            a ^= pivots[p]
    return len(pivots)

def run():
    yes,E=build(True)
    no,_=build(False)
    assert len(yes)==len(no)==50
    projected=[(1<<(i-1))^(1<<i) for i in range(1,7)]
    assert rank(projected)==6
    compatible=[]
    for bbits in range(256):
        beta={i:((bbits>>(i-1))&1) for i in range(1,9)}
        predicted=all(beta[i]==beta[i+1] for i in range(1,7))
        actual=False
        for pbits in range(64):
            a=beta|{i+9:(pbits>>i)&1 for i in range(6)}
            if all(sum(a[x] for x in vs)%2==0 for vs in E):
                actual=True;break
        assert predicted==actual
        if actual:compatible.append(beta)
    assert len(compatible)==4
    assert sum(beta[1]==1 and beta[7]==1 for beta in compatible)==2
    assert sum(beta[1]==1 and beta[7]==0 for beta in compatible)==0
    for F,models in ((yes,2),(no,0)):
        count=0
        for bits in range(1<<14):
            a={v:((bits>>(v-1))&1) for v in range(1,15)}
            if holds(F,a): count+=1
        assert count==models
    for vs in E:
        clauses=xor_clauses(vs,0)
        for bits in itertools.product((0,1),repeat=3):
            a=dict(zip(vs,bits))
            assert holds(clauses,a)==(sum(bits)%2==0)
    print('PASS: 14 variables, 50 clauses, 12 source XOR blocks, rank 6, 4/256 boundary valuations, source SAT=2, source UNSAT=0')

if __name__=='__main__':run()
