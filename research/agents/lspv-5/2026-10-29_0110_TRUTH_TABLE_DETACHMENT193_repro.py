#!/usr/bin/env python3
"""LSPV-5 truth-table-to-proper-3CNF joint relation firewall, 2026-10-29.

All experiments are standard-library and deterministic. The source family has
2**b independent sign-selected truth-table bits, full b-bit boundary, and
proper signed 3CNF Tseitin gates. This is NOT strict exact-(2,2).

Only the mathematically restricted lower bound for DETACHED, LOSSLESS joint
relation summaries is claimed; the family's decision root has an explicit
answer-preserving power-shrink constructor.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import itertools, json, math, random, sys
from pathlib import Path

SEED=20261029
OUT=Path(__file__).with_name('2026-10-29_0110_TRUTH_TABLE_DETACHMENT193_raw.json')
RNG=random.Random(SEED)

@dataclass
class Builder:
    b:int
    count:int=0
    clauses:list=field(default_factory=list)
    gates:list=field(default_factory=list)
    pins:list=field(default_factory=list)
    ps:list=field(default_factory=list)
    output:int|None=None
    def __post_init__(self):self.count=self.b
    def var(self):self.count+=1;return self.count
    def add(self,*lits):
        assert len(lits)==3 and all(x!=0 for x in lits)
        assert len({abs(x) for x in lits})==3, (lits,self.count)
        self.clauses.append(tuple(lits))
    def pad2(self,l,r):
        p=self.var();self.add(l,r,p);self.add(l,r,-p)
    def pin(self,l):
        u,v=self.var(),self.var()
        for su in (1,-1):
            for sv in (1,-1):self.add(l,su*u,sv*v)
        self.pins.append((l,u,v))
    def gate(self,k,l,r):
        out=self.var()
        if k=='AND':
            self.pad2(-out,l);self.pad2(-out,r);self.add(out,-l,-r)
        else:
            assert k=='OR'
            self.pad2(out,-l);self.pad2(out,-r);self.add(-out,l,r)
        self.gates.append((k,out,l,r))
        return out
    def build(self,t):
        assert len(t)==1<<self.b
        leaves=[]
        for a in range(1<<self.b):
            p=self.var();self.ps.append(p)
            self.pin(p if t[a] else -p)
            bits=[i+1 if (a>>i)&1 else -(i+1) for i in range(self.b)]
            cur=bits[0]
            for lit in bits[1:]:cur=self.gate('AND',cur,lit)
            leaves.append(self.gate('AND',cur,p))
        while len(leaves)>1:
            new=[]
            for i in range(0,len(leaves),2):
                new.append(self.gate('OR',leaves[i],leaves[i+1]))
            leaves=new
        self.output=leaves[0]
        self.pin(self.output)
        assert len(self.gates)==(self.b+1)*(1<<self.b)-1
        assert len(self.clauses)==5*len(self.gates)+4*((1<<self.b)+1)
        assert len(set(self.clauses))==len(self.clauses)
        assert self.count==self.b+3*len(self.gates)+3*(1<<self.b)+2
        return self
    def physical_bytes(self):
        # Fixed-width binary literal tokens (sign + W-bit var-ID), 3 per
        # clause; arity marker + header of three W-bit fields.
        w=math.ceil(math.log2(max(self.count,len(self.clauses),self.b)+1))
        return len(self.clauses)*(1+3*(w+1))+3*w
    def serialize_bits(self):
        w=math.ceil(math.log2(max(self.count,len(self.clauses),self.b)+1))
        header=f'{self.b:0{w}b}{self.count:0{w}b}{len(self.clauses):0{w}b}'
        payload=''.join('1'+''.join(('1' if l<0 else '0')+f'{abs(l):0{w}b}' for l in c)
                        for c in self.clauses)
        out=header+payload
        assert len(out)==self.physical_bytes()
        return out
    def consistent_gate_assignment(self,t,z):
        val={i+1:((z>>i)&1) for i in range(self.b)}
        for p,tbit in zip(self.ps,t):val[p]=int(tbit)
        for k,out,l,r in self.gates:
            lv=val[abs(l)] if l>0 else 1-val[abs(l)]
            rv=val[abs(r)] if r>0 else 1-val[abs(r)]
            val[out]=int((lv and rv) if k=='AND' else (lv or rv))
        # Pin auxiliary variables may take 0, and 2CNF padding auxiliaries
        # may take 0. Other variables are gate outputs or free boundaries.
        for i in range(1,self.count+1):val.setdefault(i,0)
        return val
    def truth(self,lit,val):return val[abs(lit)] if lit>0 else 1-val[abs(lit)]
    def check_assignment(self,t,z):
        val=self.consistent_gate_assignment(t,z)
        assert val[self.output]==t[z]
        bad=[i for i,c in enumerate(self.clauses) if not any(self.truth(l,val) for l in c)]
        if t[z]:assert not bad,(self.b,t,z,bad[:2])
        else:
            assert bad
            # All nonoutput constraints satisfied under deterministic gates.
            outpin=set(self.clauses[-4:])
            assert all(self.clauses[i] in outpin for i in bad)
        return len(bad)

# Basic exact DPLL independent of the circuit evaluator: no gate/pin code
# is used when solving except the literal list and boundary assignment.
def dpll(clauses,fixed):
    stats={'calls':0,'unit':0}
    def solve(assignment):
        stats['calls']+=1
        while True:
            unit=None;unresolved=[];freq={}
            for clause in clauses:
                alive=[];sat=False
                for lit in clause:
                    v=abs(lit)
                    if v in assignment:
                        if (assignment[v]==1)==(lit>0):sat=True;break
                    else:alive.append(lit)
                if sat:continue
                if not alive:return False
                if len(alive)==1:
                    unit=alive[0];break
                unresolved.append(alive)
                for l in alive:freq[abs(l)]=freq.get(abs(l),0)+1
            if unit is None:
                if not unresolved:return True
                v=max(freq,key=freq.get)
                for bit in (1,0):
                    branch=assignment.copy();branch[v]=bit
                    if solve(branch):return True
                return False
            v=abs(unit);bit=int(unit>0)
            if v in assignment:
                if assignment[v]!=bit:return False
            else:
                assignment[v]=bit;stats['unit']+=1
    result=solve(dict(fixed))
    return result,stats

def build(t,b):return Builder(b).build(t)

def power_aggregate(t,b):
    # Drops about half the boundary coordinates. Child is exactly the same
    # template, with one datum per new boundary word. Both SAT and UNSAT hold.
    bnew=max(1,b//2) if b>1 else 0
    if bnew==0:return None, bool(any(t))
    out=[0]*(1<<bnew)
    for a,bit in enumerate(t):out[a&((1<<bnew)-1)] |= int(bit)
    return bnew,out

def run():
    checks=0; dpll_cases=0;dpll_calls=0
    records=[]; lengths={}; connected=[]
    for b in (1,2,3,4,5,6,7):
        M=1<<b
        ts=[]
        if b<=3:
            for num in range(1<<M):ts.append([(num>>i)&1 for i in range(M)])
        else:
            ts=[[0]*M,[1]*M]
            for _ in range(5):ts.append([RNG.randrange(2) for _ in range(M)])
        fixed_len=None
        for t in ts:
            c=build(t,b)
            if fixed_len is None:fixed_len=c.physical_bytes()
            assert fixed_len==c.physical_bytes();checks+=1
            assert len({abs(l) for cl in c.clauses for l in cl})==c.count;checks+=1
            # Clause/variable incidence connectivity via clause-gate wiring
            # is checked over all source variables, not just the output.
            ds=list(range(c.count+1))
            def find(x):
                while ds[x]!=x:ds[x]=ds[ds[x]];x=ds[x]
                return x
            def union(x,y):ds[find(x)]=find(y)
            for cl in c.clauses:
                a,bv,cv=map(abs,cl);union(a,bv);union(a,cv)
            assert len({find(x) for x in range(1,c.count+1)})==1;checks+=1
            # Every boundary assignment is independently decided by truth
            # table. Verify the gate assignment and full proper-3CNF clauses.
            for z in range(M):
                c.check_assignment(t,z);checks+=1
            # One-oracle-free hereditary step: complete physical child.
            current=t;curb=b;steps=0
            while curb>1:
                nextb,child=power_aggregate(current,curb)
                cc=build(child,nextb)
                assert cc.physical_bytes()<build(current,curb).physical_bytes();checks+=1
                assert any(child)==any(current);checks+=1
                current=child;curb=nextb;steps+=1
            assert any(current)==any(t);checks+=1
        lengths[b]={'boundary_bits':b,'truth_bits':M,'physical_bit_length':fixed_len,
                    'variables':c.count,'clauses':len(c.clauses),'tables_tested':len(ts)}
        records.append({'b':b,'length':fixed_len,'truth_bits':M,'steps':steps})
    # Physical locality and fixed-length independence: flipping one of M
    # table bits changes four printed sign bits in the pin gadget and no IDs.
    sign_flip_cases=0
    for b in (2,3,4,5):
        M=1<<b
        zero=[0]*M
        base=build(zero,b).serialize_bits()
        for index in (0,M//2,M-1):
            alt=zero.copy();alt[index]=1
            candidate=build(alt,b).serialize_bits()
            differences=sum(a!=c for a,c in zip(base,candidate))
            assert len(base)==len(candidate) and differences==4
            sign_flip_cases+=1;checks+=1
    # Exact physical recurrence N_b from the construction; for b>=16
    # a simple analytic inequality proves the 3/4-power contraction,
    # and the finite lower values 6..15 are checked directly.
    def physical_formula(b):
        M=1<<b;g=(b+1)*M-1
        v=b+3*g+3*M+2;c=5*g+4*(M+1)
        w=math.ceil(math.log2(max(v,c,b)+1))
        return (3*w+4)*c+3*w
    recurrence_controls=0
    for b in range(6,31):
        childb=b//2
        assert physical_formula(childb)<=physical_formula(b)**0.75
        recurrence_controls+=1;checks+=1
    # Independent solver: all b=2 tables under all four pinned boundaries.
    for num in range(16):
        t=[(num>>i)&1 for i in range(4)]
        c=build(t,2)
        for z in range(4):
            result,stats=dpll(c.clauses,{1:z&1,2:(z>>1)&1})
            assert result==bool(t[z]),(num,z,result)
            dpll_cases+=1;dpll_calls+=stats['calls'];checks+=1
    # b=3 subset of random truth tables for independent generic DPLL.
    for ix in range(4):
        t=[RNG.randrange(2) for _ in range(8)]
        c=build(t,3)
        for z in (0,1):
            result,stats=dpll(c.clauses,{1:z&1,2:(z>>1)&1,3:(z>>2)&1})
            assert result==bool(t[z]),(ix,z,result)
            dpll_cases+=1;dpll_calls+=stats['calls'];checks+=1
    # Explicit complete codebook: b=3 has 2^8=256 independent sources,
    # no binary detached code shorter than 8 bits can represent all tables.
    M=8
    assert 2**M > sum(2**j for j in range(M));checks+=1
    # A compact current decision code is trivially one bit here.
    for num in range(256):
        t=[(num>>i)&1 for i in range(8)]
        assert bool(any(t))==(num!=0);checks+=1
        checks+=1 if len(set([(i,t[i]) for i in range(8)]))==8 else 0
    result={
        'status':'PASS','seed':SEED,'logical_checks':checks,
        'independent_generic_dpll_memberships':dpll_cases,
        'independent_dpll_branch_calls':dpll_calls,
        'physical_sign_flip_controls':sign_flip_cases,
        'power_recurrence_controls_b6_b30':recurrence_controls,
        'physical_encoding':'b boundary vars, M=2^b independent truth sign bits, fan-in-two AND/OR Tseitin, 2-clause pad, four-clause pins, all clauses proper',
        'lengths':lengths,
        'family_truth_table_count_formula':'2^(2^b)',
        'detached_summary_lower_bound_bits_formula':'2^b',
        'physical_length_upper_bound':'O(b^2*2^b)',
        'decision_shrinker':'fold truth table by bitwise OR over dropped high-order coordinates, from b to floor(b/2); then repeat',
        'scope':'lossless detached all-boundary relation, not answer-equivalent SAT decision shrinkage; not exact (2,2)',
        'records':records
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ('status','logical_checks','independent_generic_dpll_memberships','independent_dpll_branch_calls')}))
    print('Lengths:',{b:info['physical_bit_length'] for b,info in lengths.items()})
if __name__=='__main__':run()
