#!/usr/bin/env python3
"""CIRCUIT-OBLIVIOUS-INVERSE-SORT166 reproducible constructive audit.

No external packages or SAT oracle. Builds an O(N polylog N) fixed comparator
network plus inverse-route verifier for a total fixed-record proper 3CNF
encoding. Emits source-only input-pinned proper Tseitin 3CNF on demand and
samples TWO actual signed exact-(2,2) regularizer levels using the previously
published Q15/J recipe, with a fully charged finite occurrence table.

Invocation: python CIRCUIT_OBLIVIOUS_INVERSE_SORT166_repro.py --output raw.json
Prior 164 reproducer must be in the same directory; code from the separately
published 2026-10-26_0812 artifact; no outside solver.
"""
from __future__ import annotations
import argparse, collections, itertools, json, math, random, time
from pathlib import Path
from CIRCUIT_PARITY_TRANSPORT164_repro import R15View, StaticBase, Q, J, sl

class BoolCircuit:
    def __init__(self, N:int, q:int):
        self.N=N; self.q=q
        self.ng=N+q+2
        self.const0=N+q+1;self.const1=N+q+2
        self.gates=[]
    def gate(self,op:str,a:int,b:int):
        assert op in ('and','or') and a!=0 and b!=0
        assert abs(a)<=self.ng and abs(b)<=self.ng
        self.gates.append((op,a,b));self.ng+=1
        return self.ng
    def AND(self,a,b):return self.gate('and',a,b)
    def OR(self,a,b):return self.gate('or',a,b)
    def XOR(self,a,b):
        x=self.AND(a,-b);y=self.AND(-a,b)
        return self.OR(x,y)
    def EQ(self,a,b):return -self.XOR(a,b)
    def MUX(self,sw,a,b):
        # flag=1 chooses b, flag=0 chooses a
        return self.OR(self.AND(-sw,a),self.AND(sw,b))
    def ANDM(self,vals):
        assert vals
        while len(vals)>1:
            vals=[self.AND(vals[i],vals[i+1]) if i+1<len(vals) else vals[i] for i in range(0,len(vals),2)]
        return vals[0]
    def ORM(self,vals):
        assert vals
        while len(vals)>1:
            vals=[self.OR(vals[i],vals[i+1]) if i+1<len(vals) else vals[i] for i in range(0,len(vals),2)]
        return vals[0]
    def LTBITS(self,a,b):
        # Little-endian fixed-width UNSIGNED bitvectors
        assert len(a)==len(b)
        less=self.const0; eq=self.const1
        for x,y in zip(reversed(a),reversed(b)):
            less=self.OR(less,self.AND(eq,self.AND(-x,y)))
            eq=self.AND(eq,self.EQ(x,y))
        return less
    def EQBITS(self,a,b):
        assert len(a)==len(b)
        return self.ANDM([self.EQ(x,y) for x,y in zip(a,b)])
    def eval(self,xbits,zbits):
        assert len(xbits)==self.N and len(zbits)==self.q
        vals=[0]*(self.ng+1)
        vals[1:self.N+1]=xbits
        vals[self.N+1:self.N+self.q+1]=zbits
        vals[self.const0]=0;vals[self.const1]=1
        for gi,(op,a,b) in enumerate(self.gates):
            av=vals[abs(a)] if a>0 else 1-vals[-a]
            bv=vals[abs(b)] if b>0 else 1-vals[-b]
            vals[self.N+self.q+3+gi]=(av & bv) if op=='and' else (av|bv)
        return vals

class Builder:
    def __init__(self,q=3,m=1):
        assert q>=3 and m>=1
        self.q=q;self.m=m;self.w=math.ceil(math.log2(q+1));self.N=m*(1+3*(self.w+1))
        self.B=BoolCircuit(self.N,q)
        self.X=list(range(1,self.N+1))
        self.Z=list(range(self.N+1,self.N+q+1))
        self.layers=[]
        self.build()
    def constbits(self,v,bits):return [self.B.const1 if (v>>i)&1 else self.B.const0 for i in range(bits)]
    def input_record(self,c):
        w=self.w;step=1+3*(w+1);base=c*step
        active=self.X[base]
        req=[]
        for j in range(3):
            i=base+1+j*(w+1)
            idbits=self.X[i:i+w]
            sign=self.X[i+w]
            req.append((idbits,sign))
        return active,req
    def compare(self,A,B,ascending):
        # compare (key,kind) as unsigned lexicographic tuple.
        # key is little endian, kind bits little endian
        a=A[:self.w+2];b=B[:self.w+2]
        # key dominates kind: low order kind bits first, then key
        av=a[self.w:]+a[:self.w];bv=b[self.w:]+b[:self.w]
        return self.B.LTBITS(bv,av) if ascending else self.B.LTBITS(av,bv)
    def build(self):
        q,m,w,N=self.q,self.m,self.w,self.N
        B=self.B
        self.active=[];self.orig_req=[]
        for c in range(m):
            a,rs=self.input_record(c)
            self.active.append(a);self.orig_req.extend(rs)
        K=1<<((q+3*m-1).bit_length());self.K=K;h=K.bit_length()-1;self.h=h
        R=[]
        for v in range(1,q+1):R.append(self.constbits(v,w)+self.constbits(0,2)+[self.Z[v-1]])
        for idbits,s in self.orig_req:R.append(idbits+self.constbits(1,2)+[s])
        for _ in range(K-len(R)):R.append(self.constbits((1<<w)-1,w)+self.constbits(2,2)+[B.const0])
        self.comparator_count=0
        for level in range(1,h+1):
            size=1<<level
            stride=size//2
            while stride:
                new=R[:];pairs=[]
                for i in range(K):
                    j=i^stride
                    if i<j:
                        sw=self.compare(R[i],R[j],ascending=((i&size)==0))
                        new[i]=[B.MUX(sw,a,b) for a,b in zip(R[i],R[j])]
                        new[j]=[B.MUX(sw,b,a) for a,b in zip(R[i],R[j])]
                        pairs.append((i,j,sw));self.comparator_count+=1
                self.layers.append(pairs)
                R=new;stride//=2
        self.sorted_records=R
        # propagate nearest previous assignment value within one key block
        prev_key=None;prev_carry=B.const0;sorted_payloads=[]
        for rec in R:
            idbits=rec[:w];kind=rec[w:w+2];payload=rec[w+2]
            isassign=B.EQBITS(kind,self.constbits(0,2))
            isquery=B.EQBITS(kind,self.constbits(1,2))
            same=B.const0 if prev_key is None else B.EQBITS(idbits,prev_key)
            keep=B.AND(-isassign,B.AND(same,prev_carry))
            carry=B.OR(B.AND(isassign,payload),keep)
            sorted_payloads.append(B.AND(isquery,carry))
            prev_key=idbits;prev_carry=carry
        # Undo comparator swaps using the same Boolean switch wires,
        # recovering the lookup bit at ORIGINAL request slot positions.
        payloads=sorted_payloads
        for pairs in reversed(self.layers):
            nxt=payloads[:]
            for i,j,sw in pairs:
                nxt[i]=B.MUX(sw,payloads[i],payloads[j])
                nxt[j]=B.MUX(sw,payloads[j],payloads[i])
            payloads=nxt
        self.lookup=payloads[q:q+3*m]
        self.row_outputs=[]
        for c in range(m):
            reqs=self.orig_req[3*c:3*c+3]
            truth=[];valid=[]
            for j,(ids,sgn) in enumerate(reqs):
                nonzero=B.ORM(ids)
                leq=-B.LTBITS(self.constbits(q,w),ids)
                valid.append(B.AND(nonzero,leq))
                truth.append(B.EQ(sgn,self.lookup[3*c+j]))
            pairwise=[]
            for j,k in [(0,1),(0,2),(1,2)]:
                pairwise.append(-B.EQBITS(reqs[j][0],reqs[k][0]))
            row_ok=B.AND(B.ANDM(valid+pairwise),B.ORM(truth))
            self.row_outputs.append(B.OR(-self.active[c],row_ok))
        self.output=B.ANDM(self.row_outputs)
        self.G=len(B.gates)
        self.n0=9*self.G+3*N+q+8
        self.m0=13*self.G+4*N+12
        self.n1=33*self.m0+48*self.n0
        self.m1=44*self.m0+64*self.n0
        self.n2=3036*self.m0+4416*self.n0
        self.m2=4048*self.m0+5888*self.n0
        self.comp_expected=K*h*(h+1)//4
        assert self.comparator_count==self.comp_expected
    def bits(self,rows):
        assert len(rows)==self.m
        out=[]
        for active,triples in rows:
            out.append(int(active))
            assert len(triples)==3
            for v,s in triples:
                assert 0<=v<(1<<self.w)
                out.extend((v>>i)&1 for i in range(self.w))
                out.append(int(s))
        assert len(out)==self.N
        return out
    def direct(self,rows,z):
        for active,triples in rows:
            if not active:continue
            if not (all(1<=v<=self.q for v,_ in triples) and len({v for v,s in triples})==3):return 0
            if not any(z[v-1]==s for v,s in triples):return 0
        return 1

class CNFView:
    """Base proper 3CNF. Gates expanded with two private argument clones,
    preventing duplicate-variable clauses even when operands alias. 
    Literal positions source-controlled ONLY in U input bit pins.
    Finite R15 experiment builds an occurrence table; not low-space.
    """
    def __init__(self,model:Builder, xb):
        self.M=model;self.xb=xb;self.n=model.n0;self.m=model.m0
        self.G=model.G;self.N=model.N;self.q=model.q
        self.gatebase=self.N+self.q+3
        self.pinbase=self.N+self.q+2+9*self.G+1
        assert self.pinbase+2*self.N+4+2-1==self.n
        self.occ_cache=None
    def wire(self,w):
        sign=1 if w>0 else -1;v=abs(w)
        if v<=self.N+self.q+2:return sign*v
        g=v-(self.N+self.q+3)
        assert 0<=g<self.G
        return sign*(self.gatebase+9*g+2)
    def gate_clause(self,g,row):
        op,a,b=self.M.B.gates[g]
        ba=self.gatebase+9*g;u,v,y=ba,ba+1,ba+2
        a=self.wire(a);b=self.wire(b)
        if row<4:
            lit=(-u,a) if row<2 else (u,-a)
            pad=ba+3 if row<2 else ba+4
            return (lit[0],lit[1],pad if row%2==0 else -pad)
        if row<8:
            j=row-4;lit=(-v,b) if j<2 else (v,-b)
            pad=ba+5 if j<2 else ba+6
            return (lit[0],lit[1],pad if j%2==0 else -pad)
        if op=='and':
            if row==8:return (-u,-v,y)
            if row in (9,10):return (u,-y, (ba+7)*(1 if row==9 else -1))
            return (v,-y, (ba+8)*(1 if row==11 else -1))
        if row==8:return (u,v,-y)
        if row in (9,10):return (-u,y,(ba+7)*(1 if row==9 else -1))
        return (-v,y,(ba+8)*(1 if row==11 else -1))
    def lit(self,c,k):
        assert 0<=c<self.m and 0<=k<3
        if c<13*self.G:
            g,row=divmod(c,13);t=self.gate_clause(g,row)[k]
            return sl(abs(t),1 if t>0 else 0)
        c-=13*self.G
        if c<4*self.N:
            i,row=divmod(c,4)
            aux0=self.pinbase+2*i;aux1=aux0+1
            if k==0:return sl(i+1,self.xb[i])
            if k==1:return sl(aux0,1 if row<2 else 0)
            return sl(aux1,1 if row%2==0 else 0)
        c-=4*self.N
        pin_c=[(-self.M.B.const0, self.pinbase+2*self.N, self.pinbase+2*self.N+1),
               ( self.M.B.const1, self.pinbase+2*self.N+2, self.pinbase+2*self.N+3),
               ( self.M.output, self.pinbase+2*self.N+4, self.pinbase+2*self.N+5)]
        group,row=divmod(c,4);assert 0<=group<3
        pin,aux0,aux1=pin_c[group]
        if k==0:
            t=self.wire(pin);return sl(abs(t),t>0)
        if k==1:return sl(aux0,1 if row<2 else 0)
        return sl(aux1,1 if row%2==0 else 0)
    def occ(self,v):
        assert 1<=v<=self.n
        if self.occ_cache is None:
            self.occ_cache=[[] for _ in range(self.n+1)]
            for c in range(self.m):
                for k in range(3):
                    self.occ_cache[self.lit(c,k)[0]].append((c,k))
        return self.occ_cache[v]
    def signed_clause(self,c):
        return tuple((v if pol==1 else -v) for (v,idx,pol) in (self.lit(c,k) for k in range(3)))
    def values_from_gate(self,vals):
        n=self.n;A=[0]*(n+1)
        for v in range(1,self.N+self.q+3):A[v]=vals[v]
        for gi,(op,a,b) in enumerate(self.M.B.gates):
            base=self.gatebase+9*gi
            av=vals[abs(a)] if a>0 else 1-vals[-a]
            bv=vals[abs(b)] if b>0 else 1-vals[-b]
            A[base]=av;A[base+1]=bv
            A[base+2]=vals[self.N+self.q+3+gi]
        return A

def sat_clause(row,A):return any(A[abs(t)]==(1 if t>0 else 0) for t in row)

def run():
    t0=time.time();rng=random.Random(1661026)
    scenarios={
        'small_one_active_sat':(3,1,[(1,[(1,1),(2,0),(3,1)])]),
        'small_one_active_unsat_witness':(3,1,[(1,[(1,0),(2,0),(3,0)])]),
        'small_inactive_bad':(3,1,[(0,[(0,1),(0,0),(0,0)])]),
        'small_active_bad_zero':(3,1,[(1,[(0,1),(2,1),(3,1)])]),
        'small_active_bad_dup':(3,1,[(1,[(1,1),(1,0),(3,0)])]),
        'small_active_bad_range':(3,1,[(1,[(1,1),(2,0),(0,1)])]),
    }
    cube=[(1,[(1,(mask>>0)&1),(2,(mask>>1)&1),(3,(mask>>2)&1)]) for mask in range(8)]
    scenarios['full_cube_unsat']=(3,8,cube)
    scenarios['seven_cube_sat']=(3,8,cube[:-1]+[(0,[(0,0),(0,0),(0,0)])])
    scenarios['duplicated_sat']=(3,8,[cube[0]]*8)
    scenarios['all_inactive']=(3,8,[(0,[(0,0),(0,0),(0,0)])]*8)
    scenarios['active_bad_id']=(3,8,cube[:-1]+[(1,[(0,0),(1,1),(2,0)])])
    scenarios['inactive_bad_id']=(3,8,cube[:-1]+[(0,[(0,0),(0,0),(0,0)])])
    models={};summ={};checks=collections.Counter();samplehash=[]
    for name,(q,m,rows) in scenarios.items():
        mod=models.setdefault((q,m),Builder(q,m))
        x=mod.bits(rows)
        labels=[]
        for z in itertools.product((0,1),repeat=q):
            v=mod.B.eval(x,z)
            got=v[abs(mod.output)] if mod.output>0 else 1-v[-mod.output]
            want=mod.direct(rows,z)
            assert got==want,(name,z,got,want)
            labels.append(got);checks['complete_witness_comparisons']+=1
        got=int(any(labels));want=int(any(mod.direct(rows,z) for z in itertools.product((0,1),repeat=q)))
        assert got==want;checks['SAT_UNSAT_label_checks']+=1
        summ[name]={'sat':bool(got),'witness_count':sum(labels)}
        if name.startswith('small'):
            base=CNFView(mod,x)
            assert base.m==13*mod.G+4*mod.N+12
            for c in list(range(min(20,base.m))) + list(range(13*mod.G, min(13*mod.G+12,base.m))):
                row=base.signed_clause(c)
                assert len({abs(v) for v in row})==3
                checks['proper_3CNF_clause_checks']+=1
            # Complete source clause replay for one SAT witness, all 13G gate clauses, pins.
            if got:
                z=next(z for z in itertools.product((0,1),repeat=q) if mod.direct(rows,z))
                v=mod.B.eval(x,z);A=base.values_from_gate(v)
                for c in range(base.m):
                    assert sat_clause(base.signed_clause(c),A),(name,c)
                    checks['SAT_source_clause_replays']+=1
            # 2 actual virtual R15 levels; finite run knowingly materializes a base occurrence table.
            r1=R15View(base);r2=R15View(r1)
            assert (r1.n,r1.m,r2.n,r2.m)==(mod.n1,mod.m1,mod.n2,mod.m2)
            base.occ(1)
            targets=[0,1,base.m//2,base.m-1,r1.m//2,r1.m-1,r2.m//2,r2.m-1]
            for view in (r1,r2):
                for _ in range(30):
                    c=rng.randrange(view.m)
                    row=[view.lit(c,k) for k in range(3)]
                    assert len({t[0] for t in row})==3
                    checks['two_level_virtual_literal_reads']+=3
                for _ in range(25):
                    vID=rng.randrange(1,view.n+1)
                    occurrences=view.occ(vID)
                    assert len(occurrences)==4
                    signs=[view.lit(c,k)[2] for c,k in occurrences]
                    assert signs.count(1)==signs.count(0)==2
                    checks['two_level_signed_occurrence_checks']+=1
            # For one real bit flip, source controlled 4 sign positions -> 8 -> 16 descendants.
            for j in [0,min(1,mod.N-1),mod.N-1]:
                y=x[:];y[j]^=1;base_changed=CNFView(mod,y)
                source_slots=[]
                for rr in range(4):source_slots.append((13*mod.G+4*j+rr,0))
                assert len(source_slots)==4
                # Propagation through clone and J-source-port coordinates in R15: 
                def branches(vw,slots):
                    out=[]
                    for c,k in slots:
                        out.append((c,k))  # copied source clause
                        uid=3*c+k
                        out.append((vw.j0+7*uid,0)) # J port (row0/slot0)
                    return out
                first=branches(r1,source_slots)
                second=branches(r2,first)
                assert len(set(first))==8 and len(set(second))==16
                for c,k in first:
                    assert r1.lit(c,k)[0]==R15View(base_changed).lit(c,k)[0]
                    assert r1.lit(c,k)[2] != R15View(base_changed).lit(c,k)[2]
                    checks['first_level_actual_sign_changes']+=1
                for c,k in second:
                    assert r2.lit(c,k)[0]==R15View(R15View(base_changed)).lit(c,k)[0]
                    assert r2.lit(c,k)[2] != R15View(R15View(base_changed)).lit(c,k)[2]
                    checks['second_level_actual_sign_changes']+=1
                checks['second_level_bit_influence_positions']+=len(second)
            summ[name].update({'n0':mod.n0,'m0':mod.m0,'n1':mod.n1,'m1':mod.m1,'n2':mod.n2,'m2':mod.m2,'base_occurrence_entries':3*mod.m0})
    # Exhaustive COMPLETE input string and witness audit for q=3,m=1, all 1024*8 evaluations.
    mod=models[(3,1)]
    ex_counts=collections.Counter()
    for mask in range(1<<mod.N):
        x=[(mask>>j)&1 for j in range(mod.N)]
        assert len(x)==mod.N
        aa=[];rows=[];idx=0
        for c in range(mod.m):
            active=x[idx];idx+=1;trip=[]
            for j in range(3):
                vid=sum(x[idx+i]*(1<<i) for i in range(mod.w)); idx+=mod.w
                signbit=x[idx];idx+=1;trip.append((vid,signbit))
            rows.append((active,trip))
        for z in itertools.product((0,1),repeat=mod.q):
            v=mod.B.eval(x,z)
            ans=v[abs(mod.output)] if mod.output>0 else 1-v[-mod.output]
            expected=mod.direct(rows,z)
            assert ans==expected,('exhaustive',mask,z)
            checks['exhaustive_10bit_source_witness_checks']+=1
            aa.append(ans)
        ex_counts['sat' if any(aa) else 'unsat']+=1
    summ['all_1024_fixed_record_bitstrings']={'q':3,'m':1,'N':mod.N,'SAT_strings':ex_counts['sat'],'UNSAT_strings':ex_counts['unsat']}
    # Crosscheck sorted network against independent Python sorted-key lookup for random bitstrings and witnesses
    mod=models[(3,8)]
    for _ in range(100):
        x=[rng.randint(0,1) for _ in range(mod.N)]
        z=[rng.randint(0,1) for _ in range(mod.q)]
        vals=mod.B.eval(x,z)
        for t,(ids,s) in enumerate(mod.orig_req):
            v=sum(vals[abs(bit)]*(1<<j) for j,bit in enumerate(ids))
            expected=z[v-1] if 1<=v<=mod.q else 0
            result=vals[abs(mod.lookup[t])]
            if mod.lookup[t]<0:result^=1
            assert result==expected,('join',t,v,result,expected)
            checks['independent_sort_join_field_checks']+=1
    # Accessor arithmetic: each generator instruction uses explicit fields/stages; no data-dependent index.
    ret={
        'run_id':'CIRCUIT-OBLIVIOUS-INVERSE-SORT166', 'status':'PROVED restricted verifier; COMPUTATIONAL finite; unrestricted compression OPEN',
        'random_seed':1661026,'models':{f'q={q},m={m}':{'N':mdl.N,'q':q,'m':m,'w':mdl.w,'K':mdl.K,'h':mdl.h,'comparator_count':mdl.comparator_count,'predicted_comparators':mdl.comp_expected,'binary_AND_OR_gates':mdl.G,'base_variables':mdl.n0,'base_clauses':mdl.m0,'signed_level1_variables':mdl.n1,'signed_level1_clauses':mdl.m1,'signed_level2_variables':mdl.n2,'signed_level2_clauses':mdl.m2} for (q,m),mdl in models.items()},
        'controls':summ,'checks':dict(checks),'total_checks':sum(checks.values()),'elapsed_s':round(time.time()-t0,3),
        'independent_verifier':'exhaustive q=3 witness for every control, Python integer request lookup for 100 random inputs',
        'limitation':'Python experiment builds gate list and base occurrence table; these are not FLMV polylog workspace or an output-bit random access proof. The virtual level-2 CNF is sampled, not materialized.',
        'solver_calls':0,'failed_checks':0
    }
    return ret

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='CIRCUIT_OBLIVIOUS_INVERSE_SORT166_raw.json');a=p.parse_args()
    r=run();Path(a.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'models':r['models'],'checks':r['checks'],'total_checks':r['total_checks'],'elapsed_s':r['elapsed_s'],'failed_checks':0},indent=2))
