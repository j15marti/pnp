#!/usr/bin/env python3
"""LSPV-2 VIRTUAL-SORT-BIT254: full indexed-bit emitter for the intermediate
existential bitonic consistency CNF, NOT the final signed exact-(2,2) child.

All virtual formulas are proper ternary CNFs encoded as
0110 | n (wh bits) | m (wh bits) | m x 3 x (sign + wb-bit positive ID),
with wh=max(bit_length(n),bit_length(m)), wb=bit_length(n).
Input source is an indexed read-only proper 3-CNF.  The in-memory tuples in
this program are a test oracle for indexed source records, NOT a measured
low-space implementation of the input device on the FLMV Turing machine.

Output-bit lookup never constructs a gate/clause/occurrence table.  The
independent finite oracle below builds the clauses stage by stage.
No standard SAT solver/FLMV source parser compatibility is assumed.
"""
from __future__ import annotations
import itertools
import json
import random
import time
import tracemalloc
from collections import defaultdict
from dataclasses import dataclass
from typing import Sequence

RUN='VIRTUAL-SORT-BIT254'


def and_raw(a:int,b:int,y:int):
    return [(-a,-b,y),(a,-y),(b,-y)]


def or_raw(a:int,b:int,y:int):
    return [(a,b,-y),(-a,y),(-b,y)]


def xnor_raw(a:int,b:int,y:int):
    return [(-a,-b,y),(a,b,y),(-a,b,-y),(a,-b,-y)]


def mux_raw(s:int,a:int,b:int,y:int):
    """Force y= a if s=0, b if s=1."""
    return [(-s,-b,y),(-s,b,-y),(s,-a,y),(s,a,-y)]


def raw_gate(kind,a,b,y):
    return {'AND':and_raw,'OR':or_raw,'XNOR':xnor_raw}[kind](a,b,y)


def properize(raw:tuple|list, pads:Sequence[int]):
    """Return exact 3-CNF expansion of a unit/binary/ternary clause."""
    r=tuple(raw)
    if len(r)==3:return [r]
    if len(r)==2:
        z=pads[0]
        return [(r[0],r[1],z),(r[0],r[1],-z)]
    if len(r)==1:
        p,q=pads[:2]
        return [(r[0],p,q),(r[0],p,-q),(r[0],-p,q),(r[0],-p,-q)]
    raise ValueError('only length 1..3 supported')


@dataclass(frozen=True)
class Source:
    clauses: tuple[tuple[int,int,int], ...]
    n: int

    def __post_init__(self):
        if self.n<1 or len(self.clauses)<1:raise ValueError('nonempty CNF required')
        for c in self.clauses:
            if len(c)!=3 or len(set(map(abs,c)))!=3:
                raise ValueError('proper 3CNF distinct names required')
            if not all(1<=abs(x)<=self.n for x in c):raise ValueError('bad ID')
        if {abs(x) for c in self.clauses for x in c}!=set(range(1,self.n+1)):
            raise ValueError('active source IDs must be dense')

    @property
    def m(self):return len(self.clauses)

    def literal(self,c,p):return self.clauses[c][p]


def source_models(s:Source):
    return [bits for bits in itertools.product((0,1),repeat=s.n)
            if all(any(bits[abs(l)-1]==int(l>0) for l in C) for C in s.clauses)]


class VirtualSort:
    def __init__(self,source:Source):
        self.src=source
        self.L=3*source.m
        self.P=1<<(self.L-1).bit_length()
        self.d=self.P.bit_length()-1
        self.w=(source.n+1).bit_length()  # ceil log2(n+2), sentinel n+1
        self.Q=self.P*self.d*(self.d+1)//4
        self.stages=self.d*(self.d+1)//2
        self.pins=self.P*self.w+self.P-self.L
        self.own_cmp=7*self.w+4
        self.rows_cmp=32*self.w+16
        self.own_eq=2*self.w-1
        self.rows_eq=9*self.w-3
        self.vrec=self.P*(self.w+1)
        self.vcmp_start=self.vrec+1
        self.veq_start=self.vcmp_start+self.Q*self.own_cmp
        self.pad_pin_start=self.veq_start+(self.P-1)*self.own_eq
        self.pad_cmp_start=self.pad_pin_start+2*self.pins
        self.pad_eq_start=self.pad_cmp_start+self.Q*(4+8*self.w)
        self.n=self.pad_eq_start+(self.P-1)*2*(self.w-1)-1
        self.m=source.m+4*self.pins+self.Q*self.rows_cmp+(self.P-1)*self.rows_eq
        self.wh=max(self.n.bit_length(),self.m.bit_length())
        self.wb=self.n.bit_length()
        self.bits=4+2*self.wh+3*self.m*(1+self.wb)
        assert self.Q==self.stages*(self.P//2)

    def rec(self,r,field):
        return r*(self.w+1)+field+1

    def cv(self,c,t):
        return self.vcmp_start+c*self.own_cmp+t

    def ev(self,g,t):
        return self.veq_start+g*self.own_eq+t

    def stage(self,s):
        if not 0<=s<self.stages:raise IndexError(s)
        h=1
        while s>=h*(h+1)//2:h+=1
        before=h*(h-1)//2
        pos=s-before
        return 1<<h,1<<(h-1-pos)

    def pair(self,c):
        stage,rank=divmod(c,self.P//2)
        k,j=self.stage(stage)
        lo=(rank//j)*(2*j)+(rank%j)
        hi=lo+j
        asc=(lo&k)==0
        return stage,lo,hi,asc

    def wire(self,stage,wire,field):
        """Arithmetically invert wire address to prior gate output in O(log P)."""
        if stage==0:return self.rec(wire,field)
        _,j=self.stage(stage-1)
        lo=wire & ~j
        rank=(lo//(2*j))*j+(lo%j)
        c=(stage-1)*(self.P//2)+rank
        side=int(bool(wire&j))
        return self.cv(c,2+5*self.w+side*(self.w+1)+field)

    def unit_expand_row(self,lit,p,q,t):
        return (lit,p if t<2 else -p,q if t%2==0 else -q)

    def gate_expand_row(self,kind,a,b,y,pads,rr):
        """Return one 3CNF row of 4-row XNOR or 5-row AND/OR."""
        raw=raw_gate(kind,a,b,y)
        if kind=='XNOR':return raw[rr]
        if rr==0:return raw[0]
        rawslot=(rr-1)//2+1
        sign=1 if (rr-1)%2==0 else -1
        z=pads[rawslot-1]
        return (*raw[rawslot],sign*z)

    def pin_clause(self,row):
        pin,t=divmod(row,4)
        if pin<self.P*self.w:
            r,f=divmod(pin,self.w)
            if r<self.L:
                z=self.src.literal(r//3,r%3)
                key=abs(z)
            else:key=self.src.n+1
            v=(key>>(self.w-1-f))&1
            var=self.rec(r,f)
        else:
            r=self.L+pin-self.P*self.w
            var=self.rec(r,self.w)
            v=0
        pad=self.pad_pin_start+2*pin
        return self.unit_expand_row(var if v else -var,pad,pad+1,t)

    def comparator_clause(self,c,row):
        w=self.w
        cb=self.pad_cmp_start+c*(4+8*w)
        if row<8:
            t,j=divmod(row,4)
            v=self.cv(c,t)
            lit=v if t==0 else -v
            return self.unit_expand_row(lit,cb+2*t,cb+2*t+1,j)
        row-=8
        s,lo,hi,asc=self.pair(c)
        if row<24*w:
            b,rr=divmod(row,24)
            # b is key-field (most significant first)
            A=self.wire(s,lo,b);B=self.wire(s,hi,b)
            eqp=self.cv(c,0) if b==0 else self.cv(c,2+5*(b-1)+4)
            flagp=self.cv(c,1) if b==0 else self.cv(c,2+5*(b-1)+3)
            xnor=self.cv(c,2+5*b)
            cmpbit=self.cv(c,2+5*b+1)
            term=self.cv(c,2+5*b+2)
            flagn=self.cv(c,2+5*b+3)
            eqn=self.cv(c,2+5*b+4)
            if rr<4:return xnor_raw(A,B,xnor)[rr]
            rr-=4
            gid,sub=divmod(rr,5)
            if gid==0:
                spec=('AND',A if asc else -A,-B if asc else B,cmpbit)
            elif gid==1:spec=('AND',eqp,cmpbit,term)
            elif gid==2:spec=('OR',flagp,term,flagn)
            else:spec=('AND',eqp,xnor,eqn)
            pad0=cb+4+8*b+2*gid
            return self.gate_expand_row(*spec,(pad0,pad0+1),sub)
        row-=24*w
        out_idx,rr=divmod(row,4)
        side,field=divmod(out_idx,w+1)
        A=self.wire(s,lo,field);B=self.wire(s,hi,field)
        flag=self.cv(c,2+5*(w-1)+3)
        y=self.cv(c,2+5*w+side*(w+1)+field)
        if side==0:return mux_raw(flag,A,B,y)[rr]
        return mux_raw(flag,B,A,y)[rr]

    def equality_clause(self,g,row):
        w=self.w
        if row<4*w:
            f,rr=divmod(row,4)
            A=self.wire(self.stages,g,f)
            B=self.wire(self.stages,g+1,f)
            return xnor_raw(A,B,self.ev(g,f))[rr]
        row-=4*w
        if row<5*(w-1):
            a,rr=divmod(row,5)
            x=self.ev(g,0) if a==0 else self.ev(g,w+a-1)
            y=self.ev(g,a+1)
            z=self.ev(g,w+a)
            pad=self.pad_eq_start+g*2*(w-1)+2*a
            return self.gate_expand_row('AND',x,y,z,(pad,pad+1),rr)
        rr=row-5*(w-1)
        e=self.ev(g,2*w-2)
        a=self.wire(self.stages,g,w)
        b=self.wire(self.stages,g+1,w)
        return (-e,-a,b) if rr==0 else (-e,a,-b)

    def clause(self,c):
        if not 0<=c<self.m:raise IndexError(c)
        if c<self.src.m:
            return tuple((1 if self.src.literal(c,p)>0 else -1)*self.rec(3*c+p,self.w)
                         for p in range(3))
        c-=self.src.m
        if c<4*self.pins:return self.pin_clause(c)
        c-=4*self.pins
        if c<self.Q*self.rows_cmp:
            q,row=divmod(c,self.rows_cmp)
            return self.comparator_clause(q,row)
        c-=self.Q*self.rows_cmp
        g,row=divmod(c,self.rows_eq)
        return self.equality_clause(g,row)

    def literal(self,c,p):return self.clause(c)[p]

    def bit(self,i):
        if not 0<=i<self.bits:raise IndexError(i)
        if i<4:return (0,1,1,0)[i]
        i-=4
        if i<self.wh:return (self.n>>(self.wh-1-i))&1
        i-=self.wh
        if i<self.wh:return (self.m>>(self.wh-1-i))&1
        i-=self.wh
        c,r=divmod(i,3*(1+self.wb))
        p,h=divmod(r,1+self.wb)
        lit=self.literal(c,p)
        return int(lit>0) if h==0 else (abs(lit)>>(self.wb-h))&1


def reference_materialize(source:Source):
    """Independent stagewise enumeration of actual source-indexed clauses.
    TEST ORACLE ONLY. Builds full clause list and wire vectors."""
    e=VirtualSort(source)
    rows=[]
    wires=[]
    for r in range(e.P):
        wires.append([e.rec(r,f) for f in range(e.w+1)])
    for c in range(source.m):
        rows.append(tuple((1 if z>0 else -1)*e.rec(3*c+p,e.w)
                          for p,z in enumerate(source.clauses[c])))
    for pin in range(e.pins):
        if pin<e.P*e.w:
            rec,f=divmod(pin,e.w)
            key=abs(source.literal(rec//3,rec%3)) if rec<e.L else source.n+1
            b=(key>>(e.w-1-f))&1
            lit=e.rec(rec,f)*(1 if b else -1)
        else:
            rec=e.L+pin-e.P*e.w
            lit=-e.rec(rec,e.w)
        pad=e.pad_pin_start+2*pin
        rows.extend(properize((lit,),(pad,pad+1)))
    c=0
    for h in range(1,e.d+1):
        k=1<<h
        for power in range(h-1,-1,-1):
            j=1<<power
            nxt=[None]*e.P
            for lo in range(e.P):
                if lo&j:continue
                hi=lo^j
                asc=(lo&k)==0
                A=wires[lo];B=wires[hi]
                cb=e.pad_cmp_start+c*(4+8*e.w)
                eq0=e.cv(c,0);fl0=e.cv(c,1)
                rows.extend(properize((eq0,),(cb,cb+1)))
                rows.extend(properize((-fl0,),(cb+2,cb+3)))
                eqprev,flagprev=eq0,fl0
                for f in range(e.w):
                    xn=e.cv(c,2+5*f)
                    cmpb=e.cv(c,2+5*f+1)
                    term=e.cv(c,2+5*f+2)
                    flag=e.cv(c,2+5*f+3)
                    eq=e.cv(c,2+5*f+4)
                    rows.extend(xnor_raw(A[f],B[f],xn))
                    pad=cb+4+8*f
                    for gid,(kind,u,v,y) in enumerate((
                            ('AND',A[f] if asc else -A[f],-B[f] if asc else B[f],cmpb),
                            ('AND',eqprev,cmpb,term),
                            ('OR',flagprev,term,flag),
                            ('AND',eqprev,xn,eq))):
                        for rr,raw in enumerate(raw_gate(kind,u,v,y)):
                            if len(raw)==3:rows.append(raw)
                            else:rows.extend(properize(raw,(pad+2*gid+(rr-1),)))
                    eqprev,flagprev=eq,flag
                low=[];high=[]
                for side in (0,1):
                    for f in range(e.w+1):
                        y=e.cv(c,2+5*e.w+side*(e.w+1)+f)
                        aa=A[f] if side==0 else B[f]
                        bb=B[f] if side==0 else A[f]
                        rows.extend(mux_raw(flagprev,aa,bb,y))
                        (low if side==0 else high).append(y)
                nxt[lo]=low;nxt[hi]=high
                c+=1
            assert all(x is not None for x in nxt)
            wires=nxt
    assert c==e.Q
    for g in range(e.P-1):
        ex=[]
        for f in range(e.w):
            t=e.ev(g,f)
            rows.extend(xnor_raw(wires[g][f],wires[g+1][f],t))
            ex.append(t)
        current=ex[0]
        for a in range(e.w-1):
            nxt=e.ev(g,e.w+a)
            pad=e.pad_eq_start+g*2*(e.w-1)+2*a
            for rr,raw in enumerate(and_raw(current,ex[a+1],nxt)):
                if len(raw)==3:rows.append(raw)
                else:rows.extend(properize(raw,(pad+rr-1,)))
            current=nxt
        a=wires[g][e.w];b=wires[g+1][e.w]
        rows.extend(((-current,-a,b),(-current,a,-b)))
    assert len(rows)==e.m, (len(rows),e.m)
    return rows,e


def evaluate_clause(row,values):
    return any(values[abs(z)]==int(z>0) for z in row)


def check_proper_rows(rows,n):
    return all(len(c)==3 and len(set(map(abs,c)))==3 and all(1<=abs(z)<=n for z in c)
               for c in rows)


def evaluate_gate_truth_tables():
    checked=0
    for a,b,y in itertools.product((0,1),repeat=3):
        for name,fn,val in [('AND',and_raw,a&b),('OR',or_raw,a|b),('XNOR',xnor_raw,int(a==b))]:
            ass={1:a,2:b,3:y}
            z=all(any(ass[abs(l)]==int(l>0) for l in cl)
                  for cl in fn(1,2,3))
            assert z==(y==val),(name,a,b,y)
            checked+=1
    for s,a,b,y in itertools.product((0,1),repeat=4):
        ass={1:s,2:a,3:b,4:y}
        z=all(any(ass[abs(l)]==int(l>0) for l in cl)
              for cl in mux_raw(1,2,3,4))
        assert z==(y==(b if s else a)),(s,a,b,y)
        checked+=1
    return checked


def selected_work_baseline(source:Source,search_all=False):
    """Simple UP-DPLL exact baseline, with selected literal accesses charged."""
    ops=0;nodes=0;failed=0
    def visit(vals):
        nonlocal ops,nodes,failed
        nodes+=1
        while True:
            changed=False
            for cl in source.clauses:
                open_lits=[];true=False
                for z in cl:
                    ops+=1
                    x=abs(z)
                    if x in vals:
                        if vals[x]==int(z>0):true=True;break
                    else:open_lits.append(z)
                if true:continue
                if not open_lits:
                    failed+=1;return None
                if len(open_lits)==1:
                    z=open_lits[0];x=abs(z);want=int(z>0)
                    if x in vals and vals[x]!=want:
                        failed+=1;return None
                    if x not in vals:
                        vals[x]=want;changed=True
            if not changed:break
        variable=next((abs(z) for cl in source.clauses for z in cl if abs(z) not in vals),None)
        if variable is None:return dict(vals)
        for v in (0,1):
            nv=dict(vals);nv[variable]=v
            out=visit(nv)
            if out is not None and not search_all:return out
        if search_all:return None
        return None
    witness=visit({})
    if witness is not None:
        a={x:witness.get(x,0) for x in range(1,source.n+1)}
        assert all(any(a[abs(z)]==int(z>0) for z in cl) for cl in source.clauses)
    return {'SAT':witness is not None,'witness':witness,'nodes':nodes,'conflicts':failed,'literal_tests':ops}


def source_extremes(source:Source):
    out=[]
    for j,C in enumerate(source.clauses,1):
        local_S={abs(z):int(z>0) for z in C}
        local_U={abs(z):int(z<0) for z in C}
        out.append({'C':j,'literals':list(C),'S':local_S,'not_S':local_U,
                    'U':local_U,'not_U':local_S})
    pairs=[]
    for j,C in enumerate(source.clauses):
        for k,D in enumerate(source.clauses[:j]):
            pairs.append({'indices':[k+1,j+1],
                          'SS':not any(x==-y for x in C for y in D),
                          'SU':not any(x==y for x in C for y in D),
                          'US':not any(x==y for x in C for y in D),
                          'UU':not any(x==-y for x in C for y in D)})
    trails=[]
    for bits in [tuple(0 for _ in range(source.n)),tuple(1 for _ in range(source.n))]+[
        tuple(int(i in flips) for i in range(1,source.n+1))
        for flips in [set([1]),set(range(1,min(source.n,2)+1))]]:
        counts=[sum(bits[abs(z)-1]==int(z>0) for z in C) for C in source.clauses]
        trails.append({'a':list(bits),'t':counts,'N':[counts.count(q) for q in range(4)],
                       'SAT':all(counts)})
    return {'clauses':out,'pairs':pairs,'global_trails':trails}


def quick_suite(seed=20261030):
    rng=random.Random(seed)
    gate_truth=evaluate_gate_truth_tables()
    sources={
      'sat_single':Source(((1,2,3),),3),
      'sat_mixed':Source(((1,-2,3),(-1,2,3)),3),
      'sat_horn':Source(((1,-2,-3),(-1,-2,-3)),3),
      'sat_xor_even':Source(((1,2,-3),(1,-2,3),(-1,2,3),(-1,-2,-3)),3),
      'unsat_8':Source(tuple(tuple((1 if ((q>>i)&1)==0 else -1)*(i+1)
                         for i in range(3)) for q in range(8)),3),
      'sat_7':Source(tuple(tuple((1 if ((q>>i)&1)==0 else -1)*(i+1)
                         for i in range(3)) for q in range(7)),3),
      'sat_renamed':Source(((3,-1,2),(-3,1,2)),3),
      'unsat_renamed':Source(tuple(tuple((1 if ((q>>i)&1)==0 else -1)*((i+1)%3+1)
                         for i in range(3)) for q in range(8)),3)
    }
    for t in range(4):
        m=rng.randint(1,4)
        rows=[]
        for _ in range(m):
            v=[1,2,3];rng.shuffle(v)
            rows.append(tuple(x*(1 if rng.randint(0,1) else -1) for x in v))
        sources['seeded_%d'%t]=Source(tuple(rows),3)
    results=[];tot_rows=0;tot_bits=0;tot_match_rows=0;tot_sample_bits=0
    for name,source in sources.items():
        t0=time.perf_counter()
        tracemalloc.start()
        base=selected_work_baseline(source)
        base_peak=tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        models=source_models(source)
        assert base['SAT']==bool(models)
        em=VirtualSort(source)
        # Materialization is an independent test oracle, NOT charged to virtual lookup.
        rows,reff=reference_materialize(source)
        assert em.m==reff.m and em.n==reff.n
        assert check_proper_rows(rows,em.n)
        for c,row in enumerate(rows):
            assert row==em.clause(c),(name,c,row,em.clause(c))
        tot_match_rows+=len(rows)
        # Full bit-by-bit comparisons on modest sources; bounded deterministic
        # address probes on larger controls to limit each run to <30 sec.
        if em.bits<100000:
            bit_tests=list(range(em.bits))
        else:
            bit_tests=list(range(min(1000,em.bits)))
            bit_tests += [em.bits-1,em.bits//2,em.bits//3]
            bit_tests += [rng.randrange(em.bits) for _ in range(400)]
        for b in bit_tests:
            got=em.bit(b)
            if b<4: want=(0,1,1,0)[b]
            elif b<4+em.wh:want=(em.n>>(em.wh-1-(b-4)))&1
            elif b<4+2*em.wh:want=(em.m>>(em.wh-1-(b-4-em.wh)))&1
            else:
                off=b-4-2*em.wh
                c,z=divmod(off,3*(1+em.wb));p,field=divmod(z,1+em.wb)
                lit=rows[c][p]
                want=int(lit>0) if field==0 else (abs(lit)>>(em.wb-field))&1
            assert got==want,(name,b,got,want)
        tot_sample_bits+=len(bit_tests)
        t_virtual=time.perf_counter()
        # Charge attempted recognitions and actual synthesis+output-bit queries,
        # plus fallback exact DPLL; do NOT charge separate test oracle.
        trace=[];tested=0
        for class_name,predicate in [('2SAT',lambda C:len(C)<=2),
                                     ('Horn',lambda C:sum(z>0 for z in C)<=1),
                                     ('dualHorn',lambda C:sum(z<0 for z in C)<=1)]:
            good=True
            for C in source.clauses:
                tested+=len(C)
                if not predicate(C):good=False
            trace.append({'policy':class_name,'recognized':good,'source_literal_tests':tested})
        # A bit-access sample incurs full addressing and source literal reads.
        virtual_digest=0
        probe_count=min(100,em.bits)
        for q in range(probe_count):
            b=(q*7919+13)%em.bits
            virtual_digest=(virtual_digest*131+em.bit(b))%1000000007
        t_after=time.perf_counter()
        result={'control':name,'source_n':source.n,'source_m':source.m,'source_models':len(models),
                'source_sat':bool(models),'emitted_variables':em.n,
                'emitted_clauses':em.m,'emitted_bits':em.bits,
                'pairwise_modes':len(source.clauses)*(len(source.clauses)-1)//2,
                'matched_independent_rows':len(rows),'matched_bits':len(bit_tests),
                'baseline':{k:v for k,v in base.items() if k!='witness'},
                'class_attempts':trace,'charged_source_tests':tested+base['literal_tests'],
                'charged_virtual_reads':probe_count,'virtual_digest':virtual_digest,
                'baseline_elapsed_s':None,'portfolio_plus_emitter_elapsed_s':None,
                'test_elapsed_s':round(t_after-t0,6),
                'baseline_python_peak_B':base_peak}
        # Re-measure matched baseline and staged attempt outside the oracle cost.
        t0b=time.perf_counter();selected_work_baseline(source)
        result['baseline_elapsed_s']=round(time.perf_counter()-t0b,8)
        t0v=time.perf_counter()
        for C in source.clauses:
            _=len(C)<=2
            _=sum(z>0 for z in C)<=1
            _=sum(z<0 for z in C)<=1
        ec=VirtualSort(source)
        for q in range(probe_count):ec.bit((q*7919+13)%ec.bits)
        a=selected_work_baseline(source)
        assert a['SAT']==bool(models)
        result['portfolio_plus_emitter_elapsed_s']=round(time.perf_counter()-t0v,8)
        results.append(result)
        tot_rows+=len(rows);tot_bits+=em.bits
    return {'status':'COMPUTATIONAL','run':RUN,'seed':seed,
            'symbolic_claim':'Source-authenticated indexed bit accessor for intermediate proper3 E(F) only',
            'gate_truth_tables':gate_truth,'source_cases':len(results),
            'SAT_cases':sum(x['source_sat'] for x in results),
            'UNSAT_cases':sum(not x['source_sat'] for x in results),
            'materialized_rows_matched':tot_match_rows,
            'virtual_bits_exercised':tot_sample_bits,
            'controls':results,
            'nonclaims':['Not final signed exact-(2,2) normalized child',
                         'No N^lambda output shrink',
                         'Python source tuple not measured same-machine indexed-TM input',
                         'Parent-to-child SAT/UNSAT equivalence proved symbolically, transformed UNSAT not decided by DPLL',
                         'No universal arbitrary-A ARC contractor']}


if __name__=='__main__':
    report=quick_suite()
    print(json.dumps(report,indent=2))