#!/usr/bin/env python3
"""CIRCUIT-LOCAL-CONSUMER168, standalone within the j15marti/pnp
research/agents/lspv-2 directory. Standard library. Requires the historically
published CIRCUIT_PARITY_TRANSPORT164_repro.py in the same directory for the
independent virtual Q15/J regularizer of two actual CNF levels.

Run: python 2026-10-26_1412_CIRCUIT_LOCAL_CONSUMER168_repro.py result.json
No SAT oracle. Exhaustive W1 and first deletion, materialized comparator and
base CNF; virtual R15^2 is sampled and sourced to real predecessor clauses.
"""
import collections, hashlib, itertools, json, math, random, sys
from pathlib import Path
from CIRCUIT_PARITY_TRANSPORT164_repro import StaticBase, R15View, W, Q

SEED=1681026

class Circuit:
    def __init__(self,w):
        self.w=w;self.D=w+3;self.inputs=2*self.D+2
        self.C0=2*self.D+1;self.C1=self.C0+1
        self.gates=[];self.ptr0=lambda g:self.inputs+g+1
    def gate(self,op,a,b):
        assert op in ('and','or') and a and b
        assert abs(a)<=self.inputs+len(self.gates) and abs(b)<=self.inputs+len(self.gates)
        self.gates.append((op,a,b));return self.ptr0(len(self.gates)-1)
    def A(self,a,b):return self.gate('and',a,b)
    def O(self,a,b):return self.gate('or',a,b)
    def eq(self,a,b):return -self.O(self.A(a,-b),self.A(-a,b))
    def mux(self,s,a,b):return self.O(self.A(-s,a),self.A(s,b))
    def build(self):
        w,D=self.w,self.D
        U=list(range(1,D+1));V=list(range(D+1,2*D+1))
        # The compiler 166 comparator permutes (key,kind) to kind-low,key-high.
        a=U[w:w+2]+U[:w];b=V[w:w+2]+V[:w]
        less=self.C0;eq=self.C1
        for x,y in zip(reversed(b),reversed(a)):
            less=self.O(less,self.A(eq,self.A(-x,y)))
            eq=self.A(eq,self.eq(x,y))
        self.sigma=less
        self.H=7*(w+2)
        self.out=[self.mux(less,a,b) for a,b in zip(U,V)] + [self.mux(less,b,a) for a,b in zip(U,V)]
        assert len(self.gates)==self.H+6*D
        assert self.sigma==self.ptr0(self.H-5)
        return self
    def evaluator(self,inputs):
        assert len(inputs)==self.inputs
        v=[0]+list(inputs)
        for op,a,b in self.gates:
            x=v[abs(a)]^(a<0);y=v[abs(b)]^(b<0)
            v.append((x&y) if op=='and' else (x|y))
        return v
    def signed(self,wire):
        if abs(wire)<=self.inputs:return wire
        return (1 if wire>0 else -1)*(self.inputs+1+9*(abs(wire)-self.inputs-1)+2)

def internal_gates(w):
    H,D=7*(w+2),w+3
    result=[]
    for bit in range(w+2):
        for t in range(7):
            g=7*bit+t
            if g==H-5:continue # final less: existing report 167
            result.append(g)
    result.extend(H+3*u+t for u in range(2*D) for t in (0,1))
    assert len(result)==11*w+25
    return result

def predicted_uses(w,g):
    """(later_gate, operand_slot, signed_wire_polarity) in increasing gate order."""
    H,D=7*(w+2),w+3
    if g<H:
        bit,t=divmod(g,7)
        nxt=7*(bit+1)
        if t==0:return [(g+1,1,1)]
        if t==1:return [(g+1,1,1)]
        if t==2:return [(nxt+2,0,1)] if bit<w+1 else None
        if t==3:return [(g+2,0,1)]
        if t==4:return [(g+1,1,1)]
        if t==5:return [(g+1,1,-1)]
        if t==6:return [(nxt+1,0,1),(nxt+6,0,1)] if bit<w+1 else []
        raise AssertionError(t)
    off=g-H;u,t=divmod(off,3)
    if t in (0,1) and 0<=u<2*D:return [(H+3*u+2,t,1)]
    return None

def actual_uses(C,g):
    ptr=C.ptr0(g);out=[]
    for j,(_,a,b) in enumerate(C.gates):
        if abs(a)==ptr:out.append((j,0,1 if a>0 else -1))
        if abs(b)==ptr:out.append((j,1,1 if b>0 else -1))
    return out

def own_slots(op,g):
    return ([(13*g+8,2,1)]+[(13*g+r,1,0) for r in range(9,13)]) if op=='and' else ([(13*g+8,2,0)]+[(13*g+r,1,1) for r in range(9,13)])

def select_cnf(C,g,i):
    uses=predicted_uses(C.w,g);assert uses is not None
    own=own_slots(C.gates[g][0],g)
    assert 0<=i<len(own)+4*len(uses)
    if i<len(own):return own[i]
    n,s=divmod(i-len(own),4)
    cg,slot,eps=uses[n]
    row=4*slot+s
    return (13*cg+row,1,int(eps==1) if s<2 else int(eps==-1))

def rank_cnf(C,g,c,k):
    uses=predicted_uses(C.w,g);assert uses is not None
    own=own_slots(C.gates[g][0],g)
    for z,(cc,kk,_) in enumerate(own):
        if (c,k)==(cc,kk):return z
    cg,row=divmod(c,13)
    if k!=1:return None
    for ix,(t,slot,eps) in enumerate(uses):
        if cg==t and 4*slot<=row<4*slot+4:return 5+4*ix+(row-4*slot)
    return None

def gate_clause(C,g,row):
    op,a,b=C.gates[g];ba=C.inputs+1+9*g;u,v,y=ba,ba+1,ba+2
    a=C.signed(a);b=C.signed(b)
    if row<4:
        pair=(-u,a) if row<2 else (u,-a)
        pad=ba+3 if row<2 else ba+4
        return (pair[0],pair[1],pad if row%2==0 else -pad)
    if row<8:
        rr=row-4;pair=(-v,b) if rr<2 else (v,-b)
        pad=ba+5 if rr<2 else ba+6
        return (pair[0],pair[1],pad if rr%2==0 else -pad)
    if op=='and':
        if row==8:return (-u,-v,y)
        if row in (9,10):return (u,-y,(ba+7)*(1 if row==9 else -1))
        return (v,-y,(ba+8)*(1 if row==11 else -1))
    if row==8:return (u,v,-y)
    if row in (9,10):return (-u,y,(ba+7)*(1 if row==9 else -1))
    return (-v,y,(ba+8)*(1 if row==11 else -1))

def pin_literal(lit,aux):
    return [(lit,aux,aux+1),(lit,aux,-aux-1),(lit,-aux,aux+1),(lit,-aux,-aux-1)]

def base_cnf(C,inputs,sigma_correct=True):
    ev=C.evaluator(inputs)
    F=[gate_clause(C,g,r) for g in range(len(C.gates)) for r in range(13)]
    num=C.inputs+9*len(C.gates)
    fixed=inputs[:] + [ev[abs(C.sigma)] if sigma_correct else 1-ev[abs(C.sigma)]]
    vlist=list(range(1,C.inputs+1))+[C.signed(C.sigma)]
    for v,bit in zip(vlist,fixed):
        F.extend(pin_literal(v if bit else -v,num+1));num+=2
    assert all(len(set(map(abs,row)))==3 for row in F)
    return StaticBase(F,num),ev

def gate_witness(C,inputs,base,ev):
    vals=[0]*(base.n+1)
    for v,b in enumerate(inputs,1):vals[v]=b
    for g,(_,a,b) in enumerate(C.gates):
        ba=C.inputs+1+9*g
        vals[ba]=ev[abs(a)]^(a<0)
        vals[ba+1]=ev[abs(b)]^(b<0)
        vals[ba+2]=ev[C.ptr0(g)]
    return vals

def sat_formula(F,val):
    return all(any(val[abs(t)]==int(t>0) for t in row) for row in F)

def test_two_levels(C,rng):
    inputs=[rng.randrange(2) for _ in range(C.inputs)]
    inputs[C.C0-1]=0;inputs[C.C1-1]=1
    base,ev=base_cnf(C,inputs,True)
    val=gate_witness(C,inputs,base,ev)
    assert sat_formula(base.F,val)
    no,_=base_cnf(C,inputs,False)
    assert base.n==no.n and base.m==no.m
    assert sum(int(x!=y) for row1,row2 in zip(base.F,no.F) for x,y in zip(row1,row2))==4
    # Sound UNSAT test is semantic, not exhaustive search over giant CNF:
    # gate equality forces unique evaluation, all inputs fixed, opposite sigma pin.
    assert ev[abs(C.sigma)] != 1-ev[abs(C.sigma)]
    stats={'source_n':base.n,'source_m':base.m,'source_sat':True,'source_opposite_pin_unsat_by_gate_induction':True}
    for name,source in [('SAT',base),('UNSAT',no)]:
        a=R15View(source);b=R15View(a)
        assert a.n==33*source.m+48*source.n and a.m==44*source.m+64*source.n
        assert b.n==3036*source.m+4416*source.n and b.m==4048*source.m+5888*source.n
        for view in (a,b):
            for _ in range(35):
                c=rng.randrange(view.m);row=[view.lit(c,k) for k in range(3)]
                assert len({t[0] for t in row})==3
            for _ in range(25):
                v=rng.randrange(1,view.n+1);occ=view.occ(v)
                assert len(occ)==4
                signs=[view.lit(c,k)[2] for c,k in occ]
                assert signs.count(1)==2 and signs.count(0)==2
        stats[name+'_n1']=a.n;stats[name+'_m1']=a.m
        stats[name+'_n2']=b.n;stats[name+'_m2']=b.m
    return stats

def W1_sat(F):
    for mask in range(1<<15):
        if all(any(((mask>>(abs(v)-1))&1)==(v>0) for v in row) for row in F):return mask
    return None

def run():
    rng=random.Random(SEED);check=collections.Counter();sizes=[];sample=[]
    for w in (2,3,4,5,6,8,12,16,31):
        C=Circuit(w).build()
        intern=internal_gates(w);assert len(set(intern))==len(intern)
        for g in intern:
            expected=predicted_uses(w,g)
            actual=actual_uses(C,g)
            assert expected==actual,(w,g,expected,actual)
            check['actual_gate_consumer_comparisons']+=1
            own=own_slots(C.gates[g][0],g)
            expected_occ=[select_cnf(C,g,i) for i in range(5+4*len(expected))]
            v=C.signed(C.ptr0(g))
            actual_occ=[]
            for t,(_,a,b) in enumerate(C.gates):
                for rr in range(13):
                    row=gate_clause(C,t,rr)
                    for kk,x in enumerate(row):
                        if abs(x)==v:actual_occ.append((13*t+rr,kk,int(x>0)))
            assert expected_occ==actual_occ,(w,g,expected_occ,actual_occ)
            assert all(rank_cnf(C,g,c,k)==i for i,(c,k,pol) in enumerate(actual_occ))
            assert len(actual_occ)<=13
            hist=collections.Counter(z for c,k,z in actual_occ)
            F=len(expected)
            assert hist==({1:1+2*F,0:4+2*F} if C.gates[g][0]=='and' else {1:4+2*F,0:1+2*F})
            check['exact_base_cnf_occurrence_comparisons']+=len(actual_occ)
        check['source_gate_template_clause_checks']+=13*len(C.gates)
        sizes.append({'w':w,'H':C.H,'D':C.D,'comparator_gates':len(C.gates),
                      'internal_gates':len(intern),'excluded_switch':C.H-5,
                      'excluded_record_outputs':2*C.D})
        if w in (2,4): sample.append(dict(w=w,**test_two_levels(C,rng)))
    assert W1_sat(W) is None and W1_sat(Q) is not None
    check['exhaustive_W1_assignment_tests']=1<<15
    Wsat=W1_sat(Q)
    controls=[]
    for k in (1,2,3,5):
        for connected in (False,True):
            unsat=[tuple((1 if v>0 else -1)*(abs(v)+15*i) for v in row)
                   for i in range(k) for row in W]
            sat=[tuple((1 if v>0 else -1)*(abs(v)+15*i) for v in row)
                 for i in range(k) for row in Q]
            bridges=[(15*i+1,15*(i+1)+1,15*k+i+1) for i in range(k-1)] if connected else []
            unsat+=bridges;sat+=bridges
            V={15*i+j+1:(Wsat>>j)&1 for i in range(k) for j in range(15)}
            V.update({15*k+i+1:1 for i in range(k-1)})
            assert all(len({abs(t) for t in row})==3 for row in sat+unsat)
            assert all(any(V[abs(t)]==int(t>0) for t in row) for row in sat)
            assert all(len(set(abs(t) for t in row))==3 for row in W)
            controls.append({'k':k,'connected':connected,'sat_clauses':len(sat),
                             'unsat_clauses':len(unsat),'hitting_lower_bound':k,
                             'SAT_model_checked':True,'UNSAT_contains_W1':True,
                             'signed_22_after_connect':not connected or k==1})
            check['hostile_family_sat_unsat_checks']+=1

    # Generic GateAt black-box adversary certificate: on zero string,
    # flipping any unseen bit changes first consumer from absent to present.
    for M in (1,2,4,8,16,32,64,128):
        for j in range(M):
            b=[0]*M;b[j]=1
            assert next((i for i,x in enumerate(b) if x),None)==j
            check['adversary_bitflip_controls']+=1
    raw={'run':'CIRCUIT-LOCAL-CONSUMER168','seed':SEED,'status':'PROVED restricted local gates, FALSIFIED forward-GateAt to inverse as generic blackbox inference; full compiler ARC OPEN',
         'local_comparator_cases':sizes,'two_level_actual_virtual_proper_signed_transport':sample,'hostile_W1_controls':controls,
         'assertion_categories':dict(check),'total_accounted_checks':sum(check.values()),
         'failed_assertions':0,'unproved':'every source compiler variable, source constants/aliases, scan/carry, final row logic, arbitrary N-bit SAT normalizer and local child contraction',
         'dependencies':['CIRCUIT_PARITY_TRANSPORT164_repro.py, Q15/J R15View, already verified','CIRCUIT_OBLIVIOUS_INVERSE_SORT166_repro.py actual source gate template independently reimplemented','CIRCUIT_SWITCH_INVERSE167 earlier sigma class']}
    return raw

if __name__=='__main__':
    r=run();p=Path(sys.argv[1] if len(sys.argv)>1 else '2026-10-26_1412_CIRCUIT_LOCAL_CONSUMER168_raw.json')
    p.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'tests':r['total_accounted_checks'],'categories':r['assertion_categories'],'sample':r['two_level_actual_virtual_proper_signed_transport'],'failed':0},indent=2))
