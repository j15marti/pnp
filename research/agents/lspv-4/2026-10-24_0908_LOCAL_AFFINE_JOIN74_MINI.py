#!/usr/bin/env python3
"""LOCAL-AFFINE-JOIN74: standalone exact SAT/UNSAT regression, stdlib only."""
import itertools, json
def xor4(x,y,p,b):
    out=[]
    for a,c in itertools.product((0,1),repeat=2):
        d=1-b^a^c
        out.append((x if a==0 else -x,
                    y if c==0 else -y,
                    p if d==0 else -p))
    return out
def formula(q,b,linked=False):
    p=list(range(1,q+2))
    xs=list(range(q+2,2*q+2))
    ys=list(range(2*q+2,3*q+2))
    u,v=3*q+2,3*q+3
    f=[(p[0],u),(p[0],-u),(-p[-1],v),(-p[-1],-v)]
    for i in range(q):
        f.extend([(xs[i],ys[i]),(-xs[i],p[i+1])])
        f.extend(xor4(xs[i],ys[i],p[i],b[i]))
    if linked:
        for i in range(q-1):
            f.extend([(-xs[i],xs[i+1]),(xs[i],-xs[i+1])])
    return 3*q+3,tuple(f)
def sat(cnf, n):
    def propagate(clauses,assign):
        while True:
            left=[]
            for c in clauses:
                if any(abs(z) in assign and assign[abs(z)]==(z>0) for z in c):
                    continue
                c=tuple(z for z in c if abs(z) not in assign)
                if not c:return None
                left.append(c)
            unit=next((c[0] for c in left if len(c)==1),None)
            if unit is None:return left,assign
            assign[abs(unit)]=(unit>0)
    def search(cs,a):
        p=propagate(cs,a)
        if p is None:return False
        cs,a=p
        if not cs:return True
        z=abs(cs[0][0])
        return search(cs,{**a,z:False}) or search(cs,{**a,z:True})
    return search(cnf,{})
def local_pair(b,p,pn):
    vals=[]
    for a,c in itertools.product((0,1),repeat=2):
        if any((x or y) and ((not x) or c) and (x^y^a)==b
               for x,y in itertools.product((0,1),repeat=2)):
            vals.append((a,c))
    return vals
def run():
    checked=0
    for b in (0,1):
        for a,c in itertools.product((0,1),repeat=2):
            expected=c or (a^b)
            actual=any((x or y) and ((not x) or c) and (x^y^a)==b
                       for x,y in itertools.product((0,1),repeat=2))
            assert bool(expected)==actual
            checked+=1
    for q in range(1,6):
        for bits in itertools.product((0,1),repeat=q):
            n,f=formula(q,bits)
            assert sat(f,n)==(0 in bits)
            assert len(f)==6*q+4
            checked+=2
            if q>=2:
                _,h=formula(q,bits,linked=True)
                assert sat(h,n)==(bits[0]==0)
                assert len(h)==8*q+2
                checked+=2
    for bits,expected in [((1,0),False),((0,1),True)]:
        n,f=formula(2,bits,linked=True)
        assert sat(f,n)==expected
        checked+=1
    return {"status":"COMPUTATIONAL","checks":checked,"failures":0,
            "source":"LOCAL-AFFINE-JOIN74","limits":
            "finite tests and a restricted policy, not a P vs NP lower bound"}
if __name__=="__main__":
    print(json.dumps(run(),indent=2))
