#!/usr/bin/env python3
"""REFEREE289: exact recognizable-family bypass for mandatory representation work.

The theorem is elementary and source-level.  The U198/V198 base controls are
replayed from the authenticated original source.  No circuit, OBDD, or
semantic-equivalence cache is used by the family recognizer.
"""
from __future__ import annotations
import argparse, ast, collections, functools, itertools, json
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Z6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
V_WITNESS='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'

def load_u198(root:Path):
    p=root/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt'
    s=p.read_text(); return tuple(tuple(c) for c in ast.literal_eval(s[s.index('[['):]))

def make_v198(U):
    V=[list(c) for c in U]; V[2][2],V[44][2]=V[44][2],V[2][2]
    return tuple(tuple(c) for c in V)

def canonical(F,n):
    if n<=0 or n%3 or 3*len(F)!=4*n:return False
    seen=set(); q=collections.Counter()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if any(type(x) is not int or x==0 or abs(x)>n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        k=tuple(sorted(c))
        if k in seen:return False
        seen.add(k);q.update(c)
    return all(q[v]==q[-v]==2 for v in range(1,n+1))

def sat(F,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
def ass(n,z):return {i:(z>>(i-1))&1 for i in range(1,n+1)}

def family(base,t):
    out=list(base)
    for j in range(t):
        d=198+6*j
        out.extend(tuple((1 if x>0 else -1)*(abs(x)+d) for x in c) for c in Z6)
    return tuple(out),198+6*t

def recognize(F,n,U,V):
    """Recognize the declared block encoding; return SAT bit or None."""
    reads=0
    if not canonical(F,n):return ('MALFORMED',reads)
    if n<198 or (n-198)%6:return (None,reads)
    t=(n-198)//6
    if len(F)!=264+8*t:return (None,reads)
    head=tuple(F[:264]);reads+=264*3
    if head==U:label=False
    elif head==V:label=True
    else:return (None,reads)
    for j in range(t):
        d=198+6*j
        want=tuple(tuple((1 if x>0 else -1)*(abs(x)+d) for x in c) for c in Z6)
        got=tuple(F[264+8*j:264+8*j+8]);reads+=24
        if got!=want:return (None,reads)
    return (label,reads)

def cert_u198(U):
    mods=[]
    for i in range(6):
        V=set(range(1+32*i,33+32*i))
        G=[c for c in U[2:254] if any(abs(l) in V for l in c)]
        assert len(G)==42;mods.append(G)
    def dpll(G):
        while True:
            if not G:return True
            if any(not c for c in G):return False
            lit=next((c[0] for c in G if len(c)==1),None)
            if lit is None:break
            G=tuple(tuple(x for x in c if x!=-lit) for c in G if lit not in c)
        lit=G[0][0]
        return any(dpll(tuple(tuple(x for x in c if x!=-v) for c in G if v not in c)) for v in (lit,-lit))
    rows=calls=0
    for vals in itertools.product((False,True),repeat=6):
        a=dict(zip(range(193,199),vals));rows+=1
        if any(all(a[abs(l)]!=(l>0) for l in c) for c in U[:2]):continue
        failed=False
        for M in mods:
            H=tuple(tuple(l for l in c if abs(l)<=192) for c in M
                    if not any(abs(l)>=193 and a[abs(l)]==(l>0) for l in c))
            calls+=1
            if not dpll(H):failed=True;break
        assert failed
    assert (rows,calls)==(64,152);return rows,calls

def z6_witness():
    for z in range(64):
        a=ass(6,z)
        if sat(Z6,a):return tuple(a[i] for i in range(1,7))
    raise AssertionError

def obdd_extrema(F,n):
    tab=tuple(int(sat(F,ass(n,z))) for z in range(1<<n));cost={}
    for S in range(1<<n):
        pre=[i for i in range(n) if S>>i&1]
        for v in range(n):
            if S>>v&1:continue
            rest=[i for i in range(n) if not(S>>i&1) and i!=v];pairs=set()
            for pa in range(1<<len(pre)):
                base=sum(((pa>>k)&1)<<i for k,i in enumerate(pre));lo=hi=0
                for rb in range(1<<len(rest)):
                    z=base+sum(((rb>>k)&1)<<i for k,i in enumerate(rest))
                    lo|=tab[z]<<rb;hi|=tab[z|1<<v]<<rb
                if lo!=hi:pairs.add((lo,hi))
            cost[S,v]=len(pairs)
    full=(1<<n)-1
    @functools.lru_cache(None)
    def opt(S,sgn):
        if S==full:return 0
        a=[cost[S,v]+opt(S|1<<v,sgn) for v in range(n) if not(S>>v&1)]
        return (min if sgn<0 else max)(a)
    S=0;natural=0
    for v in range(n):natural+=cost[S,v];S|=1<<v
    return {'best':opt(0,-1),'natural':natural,'worst':opt(0,1)}

def f9_controls():
    gates=[];wires=[];dep={i:0 for i in range(1,10)}
    def add(op,x,y):
        q=10+len(gates);gates.append((q,op,x,y));dep[q]=1+max(dep[abs(x)],dep[abs(y)]);return q
    for c in F9:wires.append(add('OR',add('OR',c[0],c[1]),c[2]))
    while len(wires)>1:wires=[add('AND',wires[i],wires[i+1]) if i+1<len(wires) else wires[i] for i in range(0,len(wires),2)]
    root=wires[0];rows=0
    for z in range(512):
        a=ass(9,z);b=dict(a)
        for q,op,x,y in gates:
            X=b[abs(x)] if x>0 else 1-b[abs(x)];Y=b[abs(y)] if y>0 else 1-b[abs(y)]
            b[q]=int((X or Y) if op=='OR' else (X and Y))
        assert bool(b[root])==sat(F9,a);rows+=bool(b[root])
    assert rows==70 and len(gates)==35 and dep[root]==6
    common={3:0,5:1,6:0,7:0,8:0}
    def cnt(x1):
        return sum(sat(F9,{**common,1:x1,2:(z>>0)&1,4:(z>>1)&1,9:(z>>2)&1}) for z in range(8))
    pins=(cnt(0),cnt(1));assert pins==(2,0)
    cover=[]
    for z in range(8):
        a={**common,1:1,2:z&1,4:(z>>1)&1,9:(z>>2)&1}
        bad=[i for i,c in enumerate(F9) if not any(a[abs(x)]==int(x>0) for x in c)]
        assert bad;cover.append(bad)
    o=obdd_extrema(F9,9);assert o=={'best':52,'natural':66,'worst':80}
    return {'models':rows,'circuit_truth_rows_checked':512,'private_forward_gates':len(gates),'private_forward_depth':dep[root],
            'same_original_pins_models':pins,'unsat_leaf_cover':cover,'obdd':o}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
    root=Path(__file__).resolve().parents[3];U=load_u198(root);V=make_v198(U)
    assert canonical(U,198) and canonical(V,198)
    rows,calls=cert_u198(U)
    va={i:int(V_WITNESS[i-1]) for i in range(1,199)};assert sat(V,va)
    zw=z6_witness();zmap={i:zw[i-1] for i in range(1,7)};assert sat(Z6,zmap)
    fam=[]
    for t in range(5):
        for label,base in (('UNSAT',U),('SAT',V)):
            F,n=family(base,t);assert canonical(F,n)
            got,reads=recognize(F,n,U,V);assert got==(label=='SAT')
            fam.append({'t':t,'label':label,'n':n,'m':len(F),'literal_records':3*len(F),
                        'recognizer_literal_compares':reads,
                        'private_forward_gates':3*len(F)-1})
    bad=[]
    tests=[(),((1,1,2),),((1,-2,3),),U+(U[0],),tuple(reversed(U)),F9]
    for k,F in enumerate(tests):
        n=max((abs(x) for c in F for x in c),default=3)
        got,_=recognize(F,n,U,V);bad.append({'case':k,'result':str(got)})
    assert sum(x['result']=='MALFORMED' for x in bad)>=4
    result={
      'run':'RECOGNIZABLE-SOURCE-FAMILY-BYPASS-REFEREE289',
      'timestamp_pacific':'2026-11-02T05:48:00-08:00','P_vs_NP':'OPEN',
      'status':'PROVED_EXACT_RECOGNIZABLE_FAMILY_BYPASS_PLUS_COMPUTATIONAL_CONTROLS',
      'obstruction':'No representation-specific work can be called necessary on every canonical input when an unbounded both-label subfamily is exactly recognizable from the authenticated source and decidable before compiling that representation.',
      'theorem':'Let R_t^- = U198 AND t renamed Z6 blocks and R_t^+ = V198 AND t renamed Z6 blocks, in the declared block encoding. Every member is a valid duplicate-free proper monotone 3-SAT-(2,2) original. R_t^- is UNSAT and R_t^+ is SAT. A strict streaming template recognizer decides the family after O(N) source comparisons and O(log N) counters, without constructing C_F, an OBDD, a Shannon DAG, a Tseitin source, a semantic cache, or original-variable values. Composing it with any total exact fallback gives a correct all-input decider with this bypass.',
      'scope':'This refutes only every-input or mandatory-representation lower-bound claims. It does not refute a worst-case lower bound on other canonical inputs, and does not show that SAT is polynomial-time.',
      'proof_controls':{'U198_boundary_rows':rows,'U198_module_calls':calls,
                        'V198_witness_checked_clauses':len(V),'Z6_witness':zw},
      'family_controls':fam,'F9':f9_controls(),'malformed_and_nonfamily':bad,
      'charged_recurrence':{
        'all_input':'T_D(F)=T_grammar(F)+T_recognize(F)+[recognized]*T_output+[not_recognized]*T_fallback(F)',
        'recognized_family':'T=Theta(|F| source records)+output; no representation compilation',
        'peak':'strict declared block encoding: read-only source plus O(log n) counters and constant templates; a materializing parser instead pays O(N). Fallback peak is paid only on nonmembers.',
        'proof':'The offline U198 certificate and V198/Z6 witnesses establish the theorem; a decision-only online recognizer need not recover them. If constructive output is demanded, certificate/witness emission and checking are separately linear in t plus the fixed base artifact.',
        'guest_policy':'No guest is launched on recognized members. DELAY/COPY/RECOMP charges apply only after recognition fails and the exact fallback begins.'},
      'falsifiers':['all canonical inputs must compile C_F before decision','all canonical inputs must discover exact continuation equivalence','growing chosen OBDD/cofactor size lower-bounds every decider on that same source','post-answer constant circuits can be charged as discovery'],
      'literature_searches':[
        {'query':'instance complexity Orponen Ko Schoning Watanabe 1994','finding':'primary JACM notion studies special-case programs that are correct where they answer; background, not novelty evidence'},
        {'query':'Lynch complexity cores 1975','finding':'hardness must be located on a core; an easy infinite subfamily does not refute worst-case hardness'},
        {'query':'Peng Xiao bounded-occurrence SAT 2023','finding':'independent all-input d=4 exponential source bypass retained from REFEREE288'},
        {'query':'j15marti/pnp recognizable U198 V198 Z6 mandatory circuit','finding':'no exact prior family theorem hit; failed search is not novelty evidence'},
        {'query':'github.com/openai instance-specific SAT recognition','finding':'no relevant indexed implementation hit; failed search is not evidence'}],
      'explicit_gap':'No polynomial-total-work solver for every valid original, no representation-independent superpolynomial lower bound, no arbitrary-A power-short Phi(A), and no strict same-machine numerical FLMV transfer is proved.'}
    Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'run':result['run'],'family_cases':len(fam),'U198':[rows,calls],
                      'F9':result['F9'],'ok':True},sort_keys=True))

if __name__=='__main__':main()
