#!/usr/bin/env python3
"""LSPV-1 TWO-SIDED-DECISION312. Complete standard-library reproducer.
Runs in a j15marti/pnp checkout. Exact U198 proof, canonical V198 witness,
disjoint original-source SAT/UNSAT query adversaries, F9/Y6 controls.
No native FLMV time claim; P vs NP OPEN.
"""
import ast, collections, itertools, json, pathlib, re
ROOT=pathlib.Path(__file__).resolve().parents[3]
UFILE=ROOT/"experiments/arc/lspv2_296/U198.txt"
WFILE=ROOT/"experiments/arc/lspv1_286/verify_three_core286.py"
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
M=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=P+tuple(tuple(-x for x in c) for c in M)
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
def valid(C,n):
    if n<1 or n%3 or 3*len(C)!=4*n:return False
    seen=set();q=collections.Counter()
    for c in C:
        if len(c)!=3 or len(set(map(abs,c)))!=3:return False
        if any(x==0 or abs(x)>n or (x>0)!=(c[0]>0) for x in c):return False
        z=tuple(sorted(c))
        if z in seen:return False
        seen.add(z)
        for x in c:q[abs(x),x>0]+=1
    return all(q[i,b]==2 for i in range(1,n+1) for b in (False,True))
def sat(C,a):return all(any(a[abs(x)-1]==int(x>0) for x in c) for c in C)
def models(C,n,pins={}):
    return sum(sat(C,a) and all(a[i-1]==v for i,v in pins.items())
      for a in itertools.product((0,1),repeat=n))
def read_u():
    s=UFILE.read_text()
    return tuple(tuple(c) for c in ast.literal_eval(s[s.index("[["):]))
def red(C,lit):return tuple(tuple(x for x in c if x!=-lit) for c in C if lit not in c)
nodes=0
def dpll(C):
    global nodes
    nodes+=1
    while True:
        if not C:return True
        if () in C:return False
        u=next((c[0] for c in C if len(c)==1),None)
        if u is None:break
        C=red(C,u)
    v=min(C,key=len)[0]
    return dpll(red(C,v)) or dpll(red(C,-v))
def u_proof(U):
    modules=[]
    for i in range(6):
        lo,hi=1+32*i,32+32*i
        A=[c for c in U[2:254] if any(lo<=abs(v)<=hi for v in c)]
        assert len(A)==42
        modules.append(A)
    direct=refuted=calls=0
    for mask in range(64):
        pins={193+i:mask>>i&1 for i in range(6)}
        if any(all(pins[abs(x)]!=int(x>0) for x in c) for c in U[:2]):
            direct+=1;continue
        ok=False
        for A in modules:
            calls+=1
            B=tuple(tuple(x for x in c if abs(x)<193) for c in A
                 if not any(abs(x)>=193 and pins[abs(x)]==int(x>0) for x in c))
            if not dpll(B):ok=True;refuted+=1;break
        assert ok,mask
    assert (direct,refuted,calls)==(16,48,152)
    return dict(direct=direct,refuted=refuted,module_calls=calls,dpll_nodes=nodes)
def shift(C,z):
    return tuple(tuple((1 if x>0 else -1)*(abs(x)+z) for x in c) for c in C)
def gamma(z):
    b=bin(z)[2:]
    return "0"*(len(b)-1)+b
def enc(C,n):
    w=n.bit_length()
    return gamma(n)+gamma(len(C))+''.join(
      ('1' if c[0]>0 else '0')+''.join(f'{abs(x):0{w}b}' for x in c) for c in C)
def main():
    assert valid(F9,9) and models(F9,9)==70
    assert valid(Y6,6) and models(Y6,6)==20
    assert models(F9,9,{1:0,2:0,8:1,9:1})==2
    assert models(F9,9,{3:0,6:1,7:1,9:1})==0
    U=read_u();assert valid(U,198)
    V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2]
    V=tuple(map(tuple,V));assert valid(V,198)
    w=re.search(r"S='([01]{198})'",WFILE.read_text()).group(1)
    assert sat(V,tuple(map(int,w)))
    cert=u_proof(U)
    rows=[]
    for t in (1,2,3,4,8):
        n=198*t
        X=tuple(c for i in range(t) for c in shift(V,198*i))
        assert valid(X,n)
        x=enc(X,n);sets=[]
        for j in range(t):
            Y=tuple(c for i in range(t) for c in shift(U if i==j else V,198*i))
            assert valid(Y,n)
            y=enc(Y,n);D={i for i in range(len(x)) if x[i]!=y[i]}
            assert len(D)==2 and all(D.isdisjoint(d) for d in sets)
            sets.append(D)
        rows.append(dict(t=t,bits=len(x),valid_SAT_original=True,
             valid_UNSAT_originals=t,all_disjoint_two_bit_differences=True,
             exact_SAT_probe_floor=t,exact_UNSAT_mean_floor=f"{t+1}/2",
             randomized_SAT_floor_eps_third=f"{t}/3",
             randomized_UNSAT_mean_eps_third=f"{t+1}/6"))
    print(json.dumps(dict(run="LSPV1_TWO_SIDED_DECISION312",status="PASS",
      U198_complete_UNSAT=cert,V198_SAT_witness=True,
      F9_models=70,Y6_models=20,F9_SAT_UNSAT_pins=[2,0],rows=rows,
      P_vs_NP="OPEN"),indent=2))
if __name__=="__main__":main()
