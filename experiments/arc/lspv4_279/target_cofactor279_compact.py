#!/usr/bin/env python3
"""LSPV-4 279: independent target cofactor/UNSAT-module check.
From repository root: python experiments/arc/lspv4_279/target_cofactor279_compact.py
The target is valid duplicate-free monotone 3-SAT-(2,2), not all signed-(2,2).
Statuses: exact restricted assertions, finite computational replay, P vs NP OPEN.
"""
import ast, collections, itertools, json, pathlib

SOURCE=pathlib.Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt")
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
W="010110111001100010001111000101011110010101001111010001001011010000110010000100001001010111010000111010101010001101001010010010110001100011111001010101011011001110000100000001110110111000101100100001"

def valid(F):
    if not F: return False
    vs={abs(x) for C in F for x in C};n=max(vs)
    ct=collections.Counter(x for C in F for x in C)
    return (vs==set(range(1,n+1)) and len(F)*3==4*n
      and len(set(tuple(sorted(C)) for C in F))==len(F)
      and all(len(C)==3 and len({abs(x) for x in C})==3
          and (all(x>0 for x in C) or all(x<0 for x in C)) for C in F)
      and all(ct[x]==ct[-x]==2 for x in range(1,n+1)))

def cofactor(F,x,b):
    return tuple(tuple(l for l in C if abs(l)!=x)
        for C in F if not any(abs(l)==x and ((l>0)==b) for l in C))

def status(C,a):
    if any(abs(l) in a and a[abs(l)]==(l>0) for l in C):return True
    return tuple(l for l in C if abs(l) not in a)

def prove_and_verify_M(M):
    count=collections.Counter()
    def prove(a):
        count["nodes"]+=1
        forced=[]
        while True:
            bad=next((i for i,C in enumerate(M) if status(C,a)==()),None)
            if bad is not None:
                count["leaves"]+=1
                return ("leaf",forced,bad)
            unit=next(((i,r[0]) for i,C in enumerate(M)
                 if isinstance((r:=status(C,a)),tuple) and len(r)==1),None)
            if unit is None:break
            i,l=unit;forced.append((i,l));a={**a,abs(l):l>0};count["units"]+=1
        weights=collections.Counter()
        for C in M:
            r=status(C,a)
            if isinstance(r,tuple):
                for l in r:weights[abs(l)]+=4**(3-len(r))
        assert weights,"M was SAT"
        v=max(weights,key=weights.get)
        return ("split",forced,v,prove({**a,v:False}),prove({**a,v:True}))
    p=prove({})
    checked=collections.Counter()
    def verify(node,a):
        checked["nodes"]+=1
        for i,l in node[1]:
            assert abs(l) not in a
            assert l in M[i]
            assert all(abs(z) in a and a[abs(z)]!=(z>0) for z in M[i] if z!=l)
            a={**a,abs(l):l>0};checked["units"]+=1
        if node[0]=="leaf":
            assert all(abs(z) in a and a[abs(z)]!=(z>0) for z in M[node[2]])
            checked["leaves"]+=1
        else:
            v=node[2];assert v not in a
            verify(node[3],{**a,v:False})
            verify(node[4],{**a,v:True})
    verify(p,{})
    assert count==checked
    return dict(checked)

def main():
    U=tuple(tuple(C) for C in ast.literal_eval(
        "\n".join(t for t in SOURCE.read_text().splitlines() if t and not t.startswith("#"))))
    assert len(U)==264 and valid(U)
    h=0
    for C in U:
        for l in C:h=(131*h+l+512)%1000000007
    assert h==978258378
    V=[list(C) for C in U];V[1][0],V[7][0]=V[7][0],V[1][0]
    V=tuple(tuple(C) for C in V)
    assert valid(V) and valid(Y) and len(W)==198
    assert all(any((W[abs(l)-1]=="1")==(l>0) for l in C) for C in V)
    assert any(all((W[abs(l)-1]=="1")!=(l>0) for l in C) for C in U)
    M=[tuple(l for l in C if abs(l)<=32) for C in U[2:44]]
    assert len(M)==42
    proof=prove_and_verify_M(M)
    assert proof=={"nodes":89,"units":329,"leaves":45}
    core=[U[0],U[1]]
    for k in range(6):
        block=U[2+42*k:2+42*(k+1)]
        z=tuple(tuple((1 if k<3 else -1)*(1 if l>0 else -1)*
                 (abs(l)-32*k) for l in C
                 if 32*k<abs(l)<=32*(k+1)) for C in block)
        assert z==tuple(M)
        core.append(tuple(dict.fromkeys(l for C in block for l in C if abs(l)>192)))
    assert len(core)==8
    for a in itertools.product((False,True),repeat=6):
        assert any(all(a[abs(l)-193]!=(l>0) for l in C) for C in core)
    checks=[]
    for name,F in (("Y_SAT",Y),("U_UNSAT",U),("V_SAT",V)):
        n=max(abs(l) for C in F for l in C);m=len(F)
        o=[]
        for b in (False,True):
            H=cofactor(F,1,b)
            assert len(H)==m-2 and sum(map(len,H))==3*m-8
            assert collections.Counter(map(len,H))=={2:2,3:m-4}
            assert not valid(H)
            o.append((int(b),len(H)))
        modes=collections.Counter()
        for i,C in enumerate(F):
            for D in F[i+1:]:
                s={abs(x) for x in C}&{abs(y) for y in D}
                if not s:key="1111"
                elif (C[0]>0)==(D[0]>0):key="1001"
                else:key="0110"
                modes[key]+=1
        assert sum(modes.values())==m*(m-1)//2
        checks.append({"source":name,"n":n,"m":m,"cofactors":o,"pair_modes":dict(modes)})
    print(json.dumps({"scope":"Döcker valid monotone 3-SAT-(2,2)",
         "labels":{"Y":"SAT by 6-bit enumeration","U":"UNSAT by source-checked refutation",
                   "V":"SAT by independently checked 198-bit witness"},
         "M_refutation":proof,"core_assignments_checked":64,"sources":checks,
         "P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":main()
