#!/usr/bin/env python3
"""TOTAL-PIN-VERIFY165, October 26 2026.

Executable stdlib audit for an all-bitstrings finite-format signed-SAT verifier
whose proper 3-CNF incidence is input independent; actual TWO Q15/J
regularization levels are inspected virtually. No arbitrary encoded-SAT
polylogarithmic occurrence-access or subquadratic compiler claim.

Usage: python CIRCUIT_TOTAL_PIN_VERIFY165_repro.py --out raw.json
"""
from __future__ import annotations
import argparse,collections,itertools,json,math,random,time,hashlib

Q_RAW='''
 -1 3 -14      2 -8 9      10 -13 14      3 7 -13
 -4 -9 -11      5 8 -14       4 -8 -11     1 7 13
  1 -7 10     -5 -6 -15      -2 -6 12     -4 9 -10
 -2 5 -12     -3 6 -15       6 -7 11      2 -9 11
  4 8 -10     -3 12 15      -5 -12 15     -1 13 14
'''
QI=[int(t) for t in Q_RAW.split()]
W=tuple(tuple(QI[i:i+3]) for i in range(0,len(QI),3))
Q=tuple(c for c in W if c!=(1,7,13))
PORTS=(1,7,13)
J=((-1,-2,-3),(2,4,-5),(2,5,-6),(3,6,-4),(3,-5,-6),(-2,4,5),(-3,-4,6))
assert len(W)==20 and len(Q)==19 and len(J)==7

def sl(v,pol=1):return (v,-1,int(pol))
def ctl(v,i,flip=0):return (v,i,int(flip))
def invert(z):return (z[0],z[1],z[2]^1)
def revar(z,v):return (v,z[1],z[2])
def sign(z,bits):return z[2] if z[1]<0 else (bits[z[1]]^z[2])
def value(z,bits):return z[0] if sign(z,bits) else -z[0]

def U(l,a,b):
    return [(l,sl(a,sa),sl(b,sb)) for sa in (1,0) for sb in (1,0)]

class CircuitCNF:
    """Fixed gate/widen schedule independent of the N-bit input; x pins only polarity slots."""
    def __init__(self,q,m):
        self.q=q;self.mslots=m;self.w=max(1,(q).bit_length());self.rowwidth=1+3*(self.w+1)
        self.nbits=m*self.rowwidth
        self.rows=[];self.next_id=self.nbits+q+1
        self.gates=[];self.pin_locations={};self.output=None
        self.pad_vars=[];self.pin_aux=[]
        self.parsed=[]
        pos=0
        for c in range(m):
            active=pos+1; pos+=1
            names=[];signs=[]
            for k in range(3):
                names.append(tuple(range(pos+1,pos+self.w+1)));pos+=self.w
                signs.append(pos+1);pos+=1
            self.parsed.append((active,names,signs))
        assert pos==self.nbits
    def fresh(self):
        z=self.next_id;self.next_id+=1;return z
    def emit(self,*signed):
        assert len(signed)==3 and len({abs(z) for z in signed})==3,signed
        self.rows.append(tuple(sl(abs(z),z>0) for z in signed))
    def widen(self,a,b):
        assert abs(a)!=abs(b)
        z=self.fresh();self.pad_vars.append(z)
        self.emit(a,b,z);self.emit(a,b,-z)
    def gate(self,kind,a,b):
        if a==b:return a
        assert a!=-b,('opposite operands not built',kind,a,b)
        y=self.fresh();self.gates.append((kind,y,a,b))
        if kind=='and':
            self.emit(-a,-b,y)
            self.widen(a,-y);self.widen(b,-y)
        elif kind=='or':
            self.emit(a,b,-y)
            self.widen(-a,y);self.widen(-b,y)
        else:raise ValueError(kind)
        return y
    def AND(self,terms):
        ts=list(terms)
        assert ts
        while len(ts)>1:
            nxt=[]
            for i in range(0,len(ts),2):
                nxt.append(self.gate('and',ts[i],ts[i+1]) if i+1<len(ts) else ts[i])
            ts=nxt
        return ts[0]
    def OR(self,terms):
        ts=list(terms)
        assert ts
        while len(ts)>1:
            nxt=[]
            for i in range(0,len(ts),2):
                nxt.append(self.gate('or',ts[i],ts[i+1]) if i+1<len(ts) else ts[i])
            ts=nxt
        return ts[0]
    def XOR(self,a,b):
        return self.gate('and',self.gate('or',a,b),-self.gate('and',a,b))
    def EQ_const(self,bitids,num):
        return self.AND((bid if (num>>i)&1 else -bid) for i,bid in enumerate(bitids))
    def EQ_vec(self,bits_a,bits_b):
        return self.AND((-self.XOR(a,b)) for a,b in zip(bits_a,bits_b))
    def selected_value(self,bitids):
        tags=[self.EQ_const(bitids,v) for v in range(1,self.q+1)]
        valid=self.OR(tags)
        match=self.OR(self.gate('and',tag,self.nbits+v) for v,tag in enumerate(tags,1))
        return valid,match
    def build(self):
        checks=[]
        for active,namebits,signbits in self.parsed:
            matches=[self.selected_value(idbits) for idbits in namebits]
            valid=[pair[0] for pair in matches]
            wvals=[pair[1] for pair in matches]
            # sign==1 denotes positive literal; truth iff sign == assignment value.
            literal_truth=[-self.XOR(sb,wv) for sb,wv in zip(signbits,wvals)]
            distinct=[-self.EQ_vec(namebits[i],namebits[j])
                      for i,j in ((0,1),(0,2),(1,2))]
            ok=self.AND(valid+distinct+[self.OR(literal_truth)])
            checks.append(self.gate('or',-active,ok))
        self.output=self.AND(checks)
        # Input pins use four clauses each; locations fixed by wire index.
        for i in range(self.nbits):
            a=self.fresh();b=self.fresh();self.pin_aux.extend([a,b]);
            start=len(self.rows);self.rows.extend(U(ctl(i+1,i,0),a,b))
            self.pin_locations[i]=tuple((start+k,0) for k in range(4))
        a=self.fresh();b=self.fresh();self.pin_aux.extend([a,b]);self.rows.extend(U(sl(self.output),a,b))
        self.n=self.next_id-1;self.mc=len(self.rows)
        assert len(self.pin_locations)==self.nbits
        for row in self.rows:assert len({z[0] for z in row})==3
        return self
    def eval(self,bits,witness):
        assert len(bits)==self.nbits and len(witness)==self.q
        vals=[False]*(self.n+1)
        for i,z in enumerate(bits):vals[i+1]=bool(z)
        for i,z in enumerate(witness):vals[self.nbits+1+i]=bool(z)
        for kind,y,a,b in self.gates:
            av=vals[abs(a)] if a>0 else not vals[abs(a)]
            bv=vals[abs(b)] if b>0 else not vals[abs(b)]
            vals[y]=(av and bv) if kind=='and' else (av or bv)
        return vals[self.output],vals
    def extension(self,bits,witness):
        good,vals=self.eval(bits,witness)
        for z in self.pin_aux+self.pad_vars:vals[z]=False
        return good,vals
    def source_satisfied(self,bits,witness):
        good,vals=self.extension(bits,witness)
        passed=all(any((vals[z[0]] if sign(z,bits) else not vals[z[0]])
                       for z in row) for row in self.rows)
        return good,passed
    def semantic(self,bits,witness):
        ok=True;cl=[]
        for active,names,signbits in self.parsed:
            av=bits[active-1]
            if not av:continue
            ids=[sum(bits[t-1]<<j for j,t in enumerate(field)) for field in names]
            if min(ids)<1 or max(ids)>self.q or len(set(ids))!=3:return False
            signs=[bits[s-1] for s in signbits]
            cl.append(any(witness[v-1] if signbit else not witness[v-1]
                          for v,signbit in zip(ids,signs)))
        return all(cl)
    def pack(self,clauses,active_invalid=None):
        """Encode up to m clauses; each element is signed 3-tuple, or None inactive."""
        bits=[0]*self.nbits
        for c,row in enumerate(clauses):
            if row is None:continue
            active,names,signbits=self.parsed[c]
            bits[active-1]=1
            for k,z in enumerate(row):
                for j,t in enumerate(names[k]):bits[t-1]=(abs(z)>>j)&1
                bits[signbits[k]-1]=int(z>0)
        if active_invalid is not None:
            active,names,signbits=self.parsed[active_invalid]
            bits[active-1]=1
            for t in names[0]:bits[t-1]=0 # ID 0 malformed
        return tuple(bits)

class FixedBase:
    """Experimental base. Explicit occurrence list is charged. Not a local-access proof."""
    def __init__(self,C):
        self.C=C;self.n=C.n;self.m=C.mc;self.rows=C.rows
        self.occs=[[] for _ in range(self.n+1)]
        for c,row in enumerate(self.rows):
            for k,t in enumerate(row):self.occs[t[0]].append((c,k))
    def lit(self,c,k):return self.rows[c][k]
    def occ(self,v):return self.occs[v]

class R15View:
    """Exact virtual two-level R15; experimental base scans occurrence arrays."""
    def __init__(self,base):
        self.b=base;self.L=3*base.m+3*base.n;self.B=base.m+base.n
        self.n=33*base.m+48*base.n;self.m=44*base.m+64*base.n
        self.imp0=base.m;self.q0=self.imp0+self.L
        self.j0=self.q0+19*self.B;self.qend=self.L+15*self.B
        assert self.j0+7*(3*base.m+6*base.n)==self.m
        assert self.qend+5*(3*base.m+6*base.n)==self.n
    def next(self,u):
        b=self.b
        if u<=3*b.m:
            c,k=divmod(u-1,3);v=b.lit(c,k)[0];occ=b.occ(v)
            idx=occ.index((c,k))
            if idx+1<len(occ):
                cc,kk=occ[idx+1];return 3*cc+kk+1
            return 3*b.m+3*(v-1)+1
        v,t=divmod(u-3*b.m-1,3);v+=1
        if t<2:return u+1
        occ=b.occ(v)
        return 3*occ[0][0]+occ[0][1]+1 if occ else 3*b.m+3*(v-1)+1
    def prev(self,u):
        b=self.b
        if u<=3*b.m:
            c,k=divmod(u-1,3);v=b.lit(c,k)[0];occ=b.occ(v)
            idx=occ.index((c,k))
            if idx>0:
                cc,kk=occ[idx-1];return 3*cc+kk+1
            return 3*b.m+3*(v-1)+3
        v,t=divmod(u-3*b.m-1,3);v+=1
        if t>0:return u-1
        occ=b.occ(v)
        return 3*occ[-1][0]+occ[-1][1]+1 if occ else u+2
    def lit(self,c,k):
        b=self.b
        if c<b.m:return revar(b.lit(c,k),3*c+k+1)
        if c<self.q0:
            u=c-self.imp0+1
            if k==0:return sl(u,0)
            if k==1:return sl(self.next(u),1)
            block,s=divmod(u-1,3)
            return sl(self.L+15*block+PORTS[s],1)
        if c<self.j0:
            q,row=divmod(c-self.q0,19);t=Q[row][k]
            return sl(self.L+15*q+abs(t),t>0)
        j,row=divmod(c-self.j0,7);t=J[row][k]
        if abs(t)>=2:return sl(self.qend+5*j+(abs(t)-1),t>0)
        if j<3*b.m:
            cc,kk=divmod(j,3)
            port=invert(revar(b.lit(cc,kk),j+1))
        else:
            v,tidx=divmod(j-3*b.m,6)
            d=self.L-3*b.n+3*v+(tidx//2)+1
            port=sl(d,1 if tidx%2==0 else 0)
        return port if t<0 else invert(port)
    def occ(self,v):
        b=self.b;o=[]
        if v<=self.L:
            if v<=3*b.m:
                cc,k=divmod(v-1,3)
                o.append((cc,k));o.append((self.j0+7*(v-1),0))
            else:
                x,r=divmod(v-3*b.m-1,3)
                for e in (0,1):o.append((self.j0+7*(3*b.m+6*x+2*r+e),0))
            o.append((self.imp0+v-1,0))
            o.append((self.imp0+self.prev(v)-1,1))
        elif v<=self.qend:
            q,t=divmod(v-self.L-1,15);t+=1
            for row,rr in enumerate(Q):
                for k,z in enumerate(rr):
                    if abs(z)==t:o.append((self.q0+19*q+row,k))
            if t in PORTS:
                u=3*q+PORTS.index(t)+1
                o.append((self.imp0+u-1,2))
        else:
            j,t=divmod(v-self.qend-1,5);t+=2
            for row,rr in enumerate(J):
                for k,z in enumerate(rr):
                    if abs(z)==t:o.append((self.j0+7*j+row,k))
        o.sort();assert len(o)==4,(v,o)
        return o


def descendants(c,k,level):
    """One source slot is copied to original clause and opposite J port."""
    a=[(c,k)]
    for view in level:
        b=view.b
        a=[pos for (r,s) in a for pos in ((r,s),(view.j0+7*(3*r+s),0))]
    return a

def formula_meta(v):
    return {"variables":v.n,"clauses":v.m,"literal_fields":3*v.m,
            "encoded_bits_estimate":4+2*math.ceil(math.log2(max(v.n,v.m)+1))+
                    3*v.m*(1+math.ceil(math.log2(v.n+1)))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='CIRCUIT_TOTAL_PIN_VERIFY165_raw.json');args=ap.parse_args()
    tm=time.time();rng=random.Random(165);checks=collections.Counter();errors=[]
    # 3 names, up to eight clauses. A complete eight-clause 3-variable core is UNSAT.
    C=CircuitCNF(3,8).build();base=FixedBase(C)
    first=R15View(base);second=R15View(first)
    controls=[]
    core=list(itertools.product((1,-1),repeat=3))
    core=[tuple((i+1)*sig for i,sig in enumerate(ss)) for ss in core]
    tests=[('core_unsat',C.pack(core)),
           ('core_minus_one_sat',C.pack(core[:-1]+[None])),
           ('all_inactive_sat',C.pack([None]*8)),
           ('repeated_clauses_sat',C.pack([core[0]]*8)),
           ('duplicate_variable_invalid',C.pack([(1,1,-3)]+[None]*7)),
           ('core_swapped_unsat',C.pack([tuple(z if abs(z)==3 else ((2 if abs(z)==1 else 1)*(1 if z>0 else -1)) for z in row) for row in core])),
           ('bad_id_unsat',C.pack([core[0]]+[None]*7,active_invalid=0)),
           ('invalid_inactive_ignored',C.pack([None]*8,active_invalid=None))]
    # inactive malformed fields do not affect correctness.
    badinactive=list(tests[-1][1]);s=C.parsed[7][1][0]
    for bitloc in s:badinactive[bitloc-1]=0
    tests.append(('malformed_inactive_ignored',tuple(badinactive)))
    for j in range(12):
        seq=[]
        for c in range(8):
            if rng.random()<.25:seq.append(None)
            else:
                varlist=rng.sample((1,2,3),3)
                seq.append(tuple(v*(1 if rng.randrange(2) else -1) for v in varlist))
        tests.append((f'random_{j}',C.pack(seq)))
    cases=[]
    for label,bits in tests:
        expect=any(C.semantic(bits,w) for w in itertools.product((0,1),repeat=C.q))
        actual=[];witness_count=0
        for w in itertools.product((0,1),repeat=C.q):
            direct=C.semantic(bits,w);fromc,vals=C.eval(bits,w)
            checks['circuit_semantic_comparisons']+=1
            if direct!=fromc:errors.append(f'{label}: semantic/circuit disagreement {w}')
            if fromc:
                _,satcnf=C.source_satisfied(bits,w)
                checks['positive_source_assignment_checks']+=1
                if not satcnf:errors.append(f'{label}: no CNF extension on positive witness {w}')
                witness_count+=1
            actual.append(fromc)
        if expect!=any(actual):errors.append(f'{label}: overall label mismatched')
        cases.append({'case':label,'SAT':expect,'witness_count':witness_count})
    # Each x-bit has FOUR source sign supports and SIXTEEN after two real R15 levels.
    representative_bits=[0,1,C.nbits//2,C.nbits-1]
    affected=[]
    for bit in representative_bits:
        root=C.pin_locations[bit]
        p1=[pos for r,k in root for pos in ((r,k),(first.j0+7*(3*r+k),0))]
        p2=[pos for r,k in p1 for pos in ((r,k),(second.j0+7*(3*r+k),0))]
        assert len(set(root))==4 and len(set(p1))==8 and len(set(p2))==16
        b0=tests[0][1];b1=list(b0);b1[bit]^=1
        for v,positions in ((base,root),(first,p1),(second,p2)):
            for c,k in positions:
                z=v.lit(c,k)
                checks['controlled_child_polarity_checks']+=1
                if z[1]!=bit or sign(z,b0)==sign(z,b1):
                    errors.append(f'bad control at bit {bit}, level {v is first} {v is second},row {c} slot {k}')
        affected.append({'bit':bit,'levels':[len(root),len(p1),len(p2)]})
    # Random independent samples of virtual level-two clauses and occurrence completeness.
    for view in (first,second):
        for j in range(800):
            c=rng.randrange(view.m);k=rng.randrange(3)
            z=view.lit(c,k)
            checks['indexed_two_level_literal_samples']+=1
            if not (1<=z[0]<=view.n):errors.append('bad name bound')
            if z[1]>=0 and z[1]>=C.nbits:errors.append('bad source control')
            if k==0:
                ids=[view.lit(c,t)[0] for t in range(3)]
                checks['sampled_proper_three_clauses']+=1
                if len(set(ids))!=3:errors.append(f'improper output row {c}: {ids}')
        for j in range(150):
            v=rng.randrange(1,view.n+1)
            pos=view.occ(v)
            checks['indexed_two_level_occurrence_samples']+=1
            if len(pos)!=4:errors.append('bad occurrence count')
            polarities=[]
            for c,k in pos:
                lit=view.lit(c,k)
                if lit[0]!=v:errors.append('bad indexed occurrence address')
                polarities.append(sign(lit,tests[0][1]))
            checks['sampled_22_polarity_profiles']+=1
            if sorted(polarities)!=[0,0,1,1]:errors.append(f'bad (2,2) profile {v}:{polarities}')
    # Header-count caveat: variable binary bit of (2+x0+x1) is XOR(x0,x1).
    hdr=[{'x':list(x),'n':2+sum(x),'lowbit':(2+sum(x))&1}
         for x in itertools.product((0,1),repeat=2)]
    truth=[t['lowbit'] for t in hdr]
    projected=[(0,0,0,0),(1,1,1,1),(0,0,1,1),(1,1,0,0),
               (0,1,0,1),(1,0,1,0)]
    checks['header_nonlinearity_truth_table']=4
    if tuple(truth) in projected:errors.append('header parity unexpectedly a source literal')
    data={'id':'CIRCUIT-TOTAL-PIN-VERIFY165','date':'2026-10-26',
          'source':{'q':C.q,'m_slots':C.mslots,'input_bits':C.nbits,
                    'gate_count':len(C.gates),'widen_aux_vars':len(C.pad_vars),
                    'source':formula_meta(base),'first':formula_meta(first),
                    'second':formula_meta(second)},'cases':cases,
          'source_controls':affected,'header_counterexample':hdr,
          'checks':dict(checks),'failures':errors,
          'experiment_limitations':['one fixed q=3 m=8 shape, not arbitrary binary encoding',
            'source occurrence map constructed explicitly, not polylog source Rank/Select',
            'second-level formula virtual, not fully materialized',
            'UNSAT second-level label follows symbolic gadget correctness, not DPLL over millions of variables',
            'no all-N SAT decision-circuit size compression','no FLMV model bound from Python runtime'],
          'elapsed_seconds':round(time.time()-tm,3)}
    with open(args.out,'w') as f:json.dump(data,f,indent=2)
    print(json.dumps({'out':args.out,'case_labels':[(z['case'],z['SAT']) for z in cases],
                      'checks':data['checks'],'errors':errors,'sizes':data['source']},indent=2))
    if errors:raise AssertionError(errors[:10])

if __name__=='__main__':main()
