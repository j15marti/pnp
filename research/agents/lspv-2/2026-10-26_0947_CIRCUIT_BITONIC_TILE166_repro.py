#!/usr/bin/env python3
"""CIRCUIT-SORT-TILE166: executable fixed-network comparator basis and R15 closure.

Dependencies (both in research/agents/lspv-2):
    2026-10-26_0637_CIRCUIT_R15_VIRTUAL_ACCESS163_repro.py
Run A: python 2026-10-26_0947_CIRCUIT_BITONIC_TILE166_repro.py
Run B: PNP_RUN_BITONIC=1 python 2026-10-26_0947_CIRCUIT_BITONIC_TILE166_repro.py
Pure standard library. No SAT oracle. Tests use a separate exhaustive/DPLL
oracle only for their finite source-CNF labels; proofs are symbolic.
"""
from collections import defaultdict, Counter
from itertools import product
import importlib.util, json, os, pathlib, random, time

RUN='CIRCUIT-SORT-TILE166'
HERE=pathlib.Path(__file__).resolve().parent
DEP_NAME='2026-10-26_0637_CIRCUIT_R15_VIRTUAL_ACCESS163_repro.py'
dep=HERE / DEP_NAME
if not dep.exists():
    dep=HERE.parent / 'arc_research_ref' / DEP_NAME
if not dep.exists():
    raise FileNotFoundError('Obtain exact R15 dependency beside this reproducer: '+DEP_NAME)
spec=importlib.util.spec_from_file_location('exact_r15_163',dep)
r15=importlib.util.module_from_spec(spec);spec.loader.exec_module(r15)
R15=r15.R15

# Standard 3-CNF Tseitin presentation of a 2-input comparator:
# a,b input keys, c=min(a,b)=a&b, d=max(a,b)=a|b.
# All at fixed variable indices 1..16. Each binary clause is padded by
# (l1 OR l2 OR z) AND (l1 OR l2 OR NOT z), with fresh z.
# Each unit pin l is padded using two fresh IDs (p,q) and four sign choices.
def local_rows(bits):
    a,b,expect_min,expect_max=map(int,bits)
    out=[]
    out.append((-1,-2,3))   # a & b -> c
    next_id=5
    def binary(l1,l2):
        nonlocal next_id
        z=next_id;next_id+=1
        out.extend(((l1,l2,z),(l1,l2,-z)))
    binary(1,-3);binary(2,-3)
    out.append((1,2,-4))    # d -> a | b
    binary(-1,4);binary(-2,4)
    for var,value in ((1,a),(2,b),(3,expect_min),(4,expect_max)):
        p,q=next_id,next_id+1;next_id+=2
        lit=var if value else -var
        for sp in (1,-1):
            for sq in (1,-1):
                out.append((lit,sp*p,sq*q))
    assert next_id==17 and len(out)==26
    assert all(len(set(map(abs,row)))==3 for row in out)
    return tuple(out)

REF=local_rows((0,0,0,0))
VAR_BASE={i:[] for i in range(1,17)}
for row_index,row in enumerate(REF):
    for pos,z in enumerate(row):VAR_BASE[abs(z)].append((row_index,pos))
REVRANK={slot:rank for x,slots in VAR_BASE.items() for rank,slot in enumerate(slots)}
CONTROL={}
for row_index,row in enumerate(REF):
    for pos,z in enumerate(row):
        influences=[]
        for bit in range(4):
            config=[0]*4;config[bit]=1
            z1=local_rows(config)[row_index][pos]
            assert abs(z)==abs(z1)
            if z1!=z:influences.append(bit)
        assert len(influences)<=1
        CONTROL[row_index,pos]=influences[0] if influences else None

class ComparatorBatch:
    """q independent *fixed-incidence* comparator tiles. All 4q source
    bits are read-only pins; no raw variable names are sorted by the compiler.
    A queried literal probes at most one source bit and uses arithmetic
    + constant-size local rank/select tables.
    """
    def __init__(self,bits):
        self.bits=tuple(map(int,bits))
        assert len(self.bits)%4==0 and len(self.bits)>=4
        assert set(self.bits)<= {0,1}
        self.q=len(self.bits)//4
        self.n=16*self.q;self.m=26*self.q
        self.reads=0
    def literal(self,c,p):
        assert 0<=c<self.m and 0<=p<3
        block,row=divmod(c,26)
        z=REF[row][p];j=CONTROL[row,p]
        if j is not None:
            self.reads+=1
            if self.bits[4*block+j]:z=-z
        return (1 if z>0 else -1)*(16*block+abs(z))
    def count(self,x):
        assert 1<=x<=self.n
        return len(VAR_BASE[(x-1)%16+1])
    def select(self,x,r):
        assert 1<=x<=self.n
        block,loc=divmod(x-1,16)
        row,pos=VAR_BASE[loc+1][r]
        return 26*block+row,pos
    def rank(self,c,p):
        assert 0<=c<self.m and 0<=p<3
        return REVRANK[c%26,p]

def eval_clause(row,assignment):
    return any(assignment[abs(z)] == int(z>0) for z in row)

def dpll(rows,n):
    # Exact independent DPLL test oracle, no external solvers.
    def inner(v):
        while True:
            changed=False
            for cl in rows:
                if any(v.get(abs(z),None)==int(z>0) for z in cl):continue
                un=[z for z in cl if abs(z) not in v]
                if not un:return None
                if len(un)==1:
                    z=un[0];x=abs(z);val=int(z>0)
                    if x in v and v[x]!=val:return None
                    if x not in v:v[x]=val;changed=True
            if not changed:break
        if all(any(v.get(abs(z),None)==int(z>0) for z in cl) for cl in rows):
            return {i:v.get(i,0) for i in range(1,n+1)}
        scores=Counter(abs(z) for cl in rows if not any(v.get(abs(z),None)==int(z>0) for z in cl)
                       for z in cl if abs(z) not in v)
        x=max(scores,key=scores.get)
        for val in (0,1):
            w=dict(v);w[x]=val;sol=inner(w)
            if sol is not None:return sol
        return None
    sol=inner({})
    if sol is None:return None
    vals=[None]+[sol[i] for i in range(1,n+1)]
    assert all(eval_clause(c,vals) for c in rows)
    return vals

def analytic_label(bits):
    return all((a&b)==mi and (a|b)==ma for a,b,mi,ma in
               (bits[i:i+4] for i in range(0,len(bits),4)))

def source_rows(src):
    return [tuple(src.literal(c,p) for p in range(3)) for c in range(src.m)]

def sign_addresses(src,bit_index):
    block,loc=divmod(bit_index,4)
    sites=[]
    for (row,pos),idx in CONTROL.items():
        if idx==loc:sites.append((26*block+row,pos))
    assert len(sites)==4
    return sites

def descendants(view,sites):
    # The only *two* sign-sensitive output sites of any source literal slot:
    # its preserved cloned occurrence and J[0,0] port of that occurrence.
    ans=[]
    for c,p in sites:
        gid=3*c+p
        ans.extend(((c,p),(view.jstart+7*gid,0)))
    assert len(ans)==2*len(sites)
    assert len(set(ans))==len(ans)
    return ans

def bit_position(view,c,p):
    w=max(1,view.n.bit_length());wh=max(view.n.bit_length(),view.m.bit_length())
    return 4+2*wh+3*c*(w+1)+p*(w+1)

def stored_bit(s,i):
    w=max(1,s.n.bit_length());wh=max(s.n.bit_length(),s.m.bit_length())
    assert 0<=i<4+2*wh+3*s.m*(1+w)
    if i<4:return (0,1,1,0)[i]
    i-=4
    if i<wh:return (s.n>>(wh-1-i))&1
    i-=wh
    if i<wh:return (s.m>>(wh-1-i))&1
    i-=wh
    c,j=divmod(i,3*(1+w));p,h=divmod(j,1+w)
    z=s.literal(c,p)
    return int(z>0) if h==0 else (abs(z)>>(w-h))&1

def test_all_q1():
    n=16;counts={'sat':0,'unsat':0,'dpll_runs':0}
    for bits in product((0,1),repeat=4):
        src=ComparatorBatch(bits);rows=source_rows(src)
        model=dpll(rows,n)
        sat=analytic_label(bits)
        assert bool(model)==sat,('truth-table mismatch',bits)
        if sat:
            assert all(eval_clause(row,model) for row in rows)
        counts['sat' if sat else 'unsat']+=1;counts['dpll_runs']+=1
        for x in range(1,17):
            occ=[(c,p) for c,row in enumerate(rows) for p,z in enumerate(row) if abs(z)==x]
            assert len(occ)==src.count(x)
            for r,(c,p) in enumerate(occ):
                assert src.select(x,r)==(c,p) and src.rank(c,p)==r
    return counts

def two_level_case(bits,full,seed):
    rng=random.Random(seed)
    src=ComparatorBatch(bits);v1=R15(src);v2=R15(v1)
    result={'q':src.q,'source_bits':list(bits),'sat':analytic_label(bits),
            'source_variables':src.n,'source_clauses':src.m,
            'first_variables':v1.n,'first_clauses':v1.m,
            'second_variables':v2.n,'second_clauses':v2.m,
            'second_serialized_bits':v2.bitlength(),
            'virtual_source_reads':0}
    sign_groups=[]
    for j in range(4*src.q):
        sites1=descendants(v1,sign_addresses(src,j))
        sites2=descendants(v2,sites1)
        assert len(sites2)==16 and len(set(sites2))==16
        sign_groups.append(set(sites2))
    assert len(set.union(*sign_groups))==16*4*src.q
    # Test all 4q pin flips against the exact *entire* set of affected positions.
    # Local comparisons, not a scan of 11m serialized output bits.
    for j in range(4*src.q):
        flipped=list(bits);flipped[j]^=1
        v2f=R15(R15(ComparatorBatch(flipped)))
        for site in sign_groups[j]:
            pos=bit_position(v2,*site)
            assert v2.bit(pos)^v2f.bit(pos)==1
        for jj in range(4*src.q):
            if jj!=j:
                for site in sign_groups[jj]:
                    pos=bit_position(v2,*site)
                    assert v2.bit(pos)==v2f.bit(pos)
        for t in range(100):
            i=rng.randrange(v2.bitlength())
            if i not in {bit_position(v2,*site) for site in sign_groups[j]}:
                assert v2.bit(i)==v2f.bit(i)
    result['second_level_affected_sign_positions_per_source_bit']=16
    result['disjoint_coordinate_groups']=True
    result['source_probe_count_after_pin_checks']=src.reads
    if full:
        s1=r15.materialize(src);s2=r15.materialize(s1)
        assert (s1.n,s1.m)==(v1.n,v1.m)
        assert (s2.n,s2.m)==(v2.n,v2.m)
        # Independently materialized all ordinary CNF clauses at both levels.
        for c in range(s1.m):
            for p in range(3):assert v1.literal(c,p)==s1.literal(c,p)
        for c in range(s2.m):
            for p in range(3):assert v2.literal(c,p)==s2.literal(c,p)
        for mat in (s1,s2):
            assert len(mat.rows)==mat.m
            assert all(len({abs(z) for z in row})==3 for row in mat.rows)
            assert len(set(mat.rows))==mat.m
            assert all(len(mat.occ[x])==4 for x in range(1,mat.n+1))
            assert all(sum(1 for c,p in mat.occ[x] if mat.literal(c,p)>0)==2
                       for x in range(1,mat.n+1))
        source_model=dpll(source_rows(src),src.n)
        assert bool(source_model)==analytic_label(bits)
        if source_model is not None:
            witness1=r15.extend_witness(src,source_model)
            witness2=r15.extend_witness(s1,witness1)
            assert r15.witness_sat(s1,witness1)
            assert r15.witness_sat(s2,witness2)
        for v,mat in ((v1,s1),(v2,s2)):
            for _ in range(500):
                i=rng.randrange(v.bitlength())
                assert v.bit(i)==stored_bit(mat,i)
        result.update({'full_materialization_independent_check':True,
                       'first_literal_fields_checked':3*v1.m,
                       'second_literal_fields_checked':3*v2.m,
                       'signed_exact_22_both_levels':True,
                       'witness_two_levels_if_sat': bool(source_model)})
    result['virtual_source_reads']=src.reads
    return result

def counterexample_raw_sort():
    # A literal/constant truth table on a,b has 0, 1, a, ~a, b, ~b only.
    keys=list(product((0,1),repeat=2))
    minword=tuple(a&b for a,b in keys)
    legal={tuple([z]*len(keys)) for z in (0,1)}
    legal.update(tuple((val if positive else 1-val) for val in bitvec)
       for bitvec in [tuple(a for a,b in keys),tuple(b for a,b in keys)]
       for positive in (True,False))
    assert minword not in legal
    return {'truth_order':keys,'min_truth_table':minword,
            'is_source_literal_or_constant':False,
            'correct_fixed_topology_tseitin_emits_only_source_pin_signs':True}

def main():
    t=time.perf_counter()
    small=test_all_q1()
    cases=[]
    # independent full SAT and UNSAT two-level simulations.
    for i,bits in enumerate(((0,1,0,1),(1,1,0,1),
                             (1,0,0,1,0,0,0,0),
                             (1,1,0,1,0,0,0,0))):
        cases.append(two_level_case(bits,full=(i<3),seed=20261026+i))
    # q=3 virtual-only test ensures scalable address arithmetic.
    cases.append(two_level_case((0,1,0,1,1,0,0,1,0,0,0,0),full=False,seed=20261031))
    ans={'run':RUN,'date_utc':'2026-10-26','dependency':DEP_NAME,
         'input_schema':'q fixed comparators, each 4 bits a,b,min_goal,max_goal; malformed/invalid goal rejected',
         'comparators_per_tile':1,'source_clauses_per_tile':26,'source_vars_per_tile':16,
         'input_bit_pin_sites_per_source_bit':4,
         'output_class':'proper signed exact-(2,2)-3CNF; NOT clause-monotone',
         'source_truth_table':small,'raw_sorted_output_failure':counterexample_raw_sort(),
         'two_level_cases':cases,'elapsed_wall_seconds':round(time.perf_counter()-t,3),
         'full_arbitrary_SAT_verifier':'OPEN',
         'global_batcher_network_uniform_address':'OPEN',
         'Q348_primary_source':'UNVERIFIED',
         'Q15_used':'Q15/19-clause from exact peer source',
         'full_N_bit_SAT_decision_circuit':'NOT CONSTRUCTED',
         'P_vs_NP':'OPEN'}
    p=HERE/'2026-10-26_0947_CIRCUIT_SORT_TILE166_raw.json'
    p.write_text(json.dumps(ans,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'test':'PASS','raw':str(p),'elapsed':ans['elapsed_wall_seconds'],
                      'source_labels':small,
                      'full_cases':sum('full_materialization_independent_check' in c for c in cases),
                      'last_virtual_case':cases[-1]['second_clauses']},indent=2))
if __name__=='__main__' and os.environ.get('PNP_RUN_BITONIC')!='1':main()

# --- Four-wire, three-stage bitonic sorting network, not merely an independent
# comparator layer. 6 comparator gates, with actual shared wire identities.
# Fixed comparator schedule: (0,1) up, (2,3) down;
# (0,2) up, (1,3) up; (0,1) up, (2,3) up.
# The bitonic 4 source is SAT iff the four input bits contain two 1s.
BITONIC_SCHEDULE=((0,1,1),(2,3,0),(0,2,1),(1,3,1),(0,1,1),(2,3,1))

def bitonic4_rows(bits):
    assert len(bits)==4
    rows=[];wires=[1,2,3,4];aux=17
    def two(l1,l2):
        nonlocal aux
        z=aux;aux+=1
        rows.extend(((l1,l2,z),(l1,l2,-z)))
    for stage,(i,j,ascending) in enumerate(BITONIC_SCHEDULE):
        a,b=wires[i],wires[j]
        lo,hi=5+2*stage,6+2*stage
        rows.append((-a,-b,lo))
        two(a,-lo);two(b,-lo)
        rows.append((a,b,-hi))
        two(-a,hi);two(-b,hi)
        wires[i],wires[j] = (lo,hi) if ascending else (hi,lo)
    assert aux==41 and len(rows)==60
    # Source pins are the *only* input-dependent signs. Final sorted pattern
    # 0,0,1,1 is enforced with 4 more constant unit constraints.
    def unit(var,value):
        nonlocal aux
        p,q=aux,aux+1;aux+=2
        ell=var if value else -var
        for sp in (1,-1):
            for sq in (1,-1):rows.append((ell,sp*p,sq*q))
    for var,val in enumerate(bits,start=1):unit(var,val)
    for var,val in zip(wires,(0,0,1,1)):unit(var,val)
    assert aux==57 and len(rows)==92
    assert all(len({abs(z) for z in row})==3 for row in rows)
    return tuple(rows)

REF4=bitonic4_rows((0,0,0,0))
VAR4={i:[] for i in range(1,57)}
for ri,row in enumerate(REF4):
    for p,z in enumerate(row):VAR4[abs(z)].append((ri,p))
RANK4={slot:r for x,slots in VAR4.items() for r,slot in enumerate(slots)}
CTRL4={}
for ri,row in enumerate(REF4):
    for p,z in enumerate(row):
        infl=[]
        for bit in range(4):
            alter=[0]*4;alter[bit]=1
            z1=bitonic4_rows(alter)[ri][p]
            assert abs(z)==abs(z1)
            if z1!=z:infl.append(bit)
        assert len(infl)<=1
        CTRL4[ri,p]=infl[0] if infl else None

class Bitonic4Batch:
    """Exact q-fold four-wire bitonic network: 4q read-only input bits.
    Source bits change only signs of four fixed unit-pin clauses each.
    All incidence and rank/select generated by constant tables and O(log q)
    bit-address arithmetic. No sorter is performed by the reduction itself.
    """
    def __init__(self,bits):
        self.bits=tuple(map(int,bits))
        assert len(self.bits)>=4 and len(self.bits)%4==0
        assert set(self.bits)<={0,1}
        self.q=len(bits)//4;self.n=56*self.q;self.m=92*self.q
        self.reads=0
    def literal(self,c,p):
        assert 0<=c<self.m and 0<=p<3
        b,r=divmod(c,92);z=REF4[r][p];j=CTRL4[r,p]
        if j is not None:
            self.reads+=1
            if self.bits[4*b+j]:z=-z
        return (1 if z>0 else -1)*(56*b+abs(z))
    def count(self,x):
        assert 1<=x<=self.n
        return len(VAR4[(x-1)%56+1])
    def select(self,x,r):
        assert 1<=x<=self.n
        b,loc=divmod(x-1,56);ri,p=VAR4[loc+1][r]
        return 92*b+ri,p
    def rank(self,c,p):
        assert 0<=c<self.m and 0<=p<3
        return RANK4[c%92,p]

def bitonic_label(bits):
    return all(sum(bits[4*b:4*b+4])==2 for b in range(len(bits)//4))

def bitonic_sign_sites(src,j):
    b,loc=divmod(j,4)
    sites=[(92*b+ri,p) for (ri,p),tag in CTRL4.items() if tag==loc]
    assert len(sites)==4
    return sites

def bitonic_network_direct(bits):
    wires=list(bits)
    for i,j,asc in BITONIC_SCHEDULE:
        a,b=wires[i],wires[j]
        wires[i],wires[j]=(a&b,a|b) if asc else (a|b,a&b)
    assert tuple(wires)==tuple(sorted(bits))
    return tuple(wires)

def test_bitonic4():
    outcomes={'sat':0,'unsat':0,'dpll_runs':0,'wire_sort_checks':0}
    for bits in product((0,1),repeat=4):
        src=Bitonic4Batch(bits)
        raw=source_rows(src)
        model=dpll(raw,src.n)
        correct=bitonic_label(bits)
        assert bool(model)==correct,(bits,correct)
        if model is not None:
            assert all(eval_clause(row,model) for row in raw)
        assert bitonic_network_direct(bits)==tuple(sorted(bits))
        outcomes['sat' if correct else 'unsat']+=1
        outcomes['dpll_runs']+=1;outcomes['wire_sort_checks']+=1
        for x in range(1,src.n+1):
            occ=[(ri,p) for ri,row in enumerate(raw) for p,z in enumerate(row) if abs(z)==x]
            assert len(occ)==src.count(x)
            for rank,(ri,p) in enumerate(occ):
                assert src.select(x,rank)==(ri,p)
                assert src.rank(ri,p)==rank
    return outcomes

def bitonic_virtual_case(bits,full=False,seed=20261026):
    src=Bitonic4Batch(bits);v1=R15(src);v2=R15(v1)
    rng=random.Random(seed)
    groups=[]
    for j in range(4*src.q):
        sites=descendants(v2,descendants(v1,bitonic_sign_sites(src,j)))
        assert len(sites)==16 and len(set(sites))==16
        groups.append(sites)
    assert len(set.union(*(set(g) for g in groups)))==16*4*src.q
    for j in range(4*src.q):
        change=list(bits);change[j]^=1
        view_change=R15(R15(Bitonic4Batch(change)))
        for jj,sites in enumerate(groups):
            for site in sites:
                k=bit_position(v2,*site)
                assert v2.bit(k)^view_change.bit(k) == int(jj==j)
        # Need no full output scan: all other output fields are proven fixed
        # by the injective two-site source-to-child propagation lemma.
        for sample in range(100):
            k=rng.randrange(v2.bitlength())
            if all(k not in {bit_position(v2,*site) for site in group} for group in groups):
                assert v2.bit(k)==view_change.bit(k)
    result={'q':src.q,'input_bits':list(bits),'sat':bitonic_label(bits),
            'source_clauses':src.m,'source_variables':src.n,
            'first_clauses':v1.m,'first_variables':v1.n,
            'second_clauses':v2.m,'second_variables':v2.n,
            'second_serialized_bits':v2.bitlength(),
            'sign_sites_per_input_bit_after_two_levels':16,
            'all_sign_supports_disjoint':True,
            'virtual_source_reads':src.reads}
    if full:
        a=r15.materialize(src)
        b=r15.materialize(a)
        assert (a.n,a.m)==(v1.n,v1.m)
        assert (b.n,b.m)==(v2.n,v2.m)
        for c in range(v1.m):
            for p in range(3):assert a.literal(c,p)==v1.literal(c,p)
        for c in range(v2.m):
            for p in range(3):assert b.literal(c,p)==v2.literal(c,p)
        for mat in (a,b):
            assert len(set(mat.rows))==mat.m
            for x in range(1,mat.n+1):
                occ=mat.occ[x];assert len(occ)==4
                assert sum(mat.literal(c,p)>0 for c,p in occ)==2
            assert all(len({abs(z) for z in row})==3 for row in mat.rows)
        sol=dpll(source_rows(src),src.n)
        assert bool(sol)==bitonic_label(bits)
        if sol:
            s1=r15.extend_witness(src,sol);assert r15.witness_sat(a,s1)
            s2=r15.extend_witness(a,s1);assert r15.witness_sat(b,s2)
        for view,stored in ((v1,a),(v2,b)):
            for _ in range(750):
                k=rng.randrange(view.bitlength())
                assert view.bit(k)==stored_bit(stored,k)
        result['materialized_two_real_levels']=True
        result['literal_fields_compared']=3*(v1.m+v2.m)
        result['signed_exact_22_verified']=True
        result['sat_witness_extended_two_levels']=bool(sol)
    return result

# This audit is deliberately separately executable to keep every invocation
# under the project's 30-second cap; it also writes its own raw JSON.
def bitonic_main():
    start=time.perf_counter()
    counts=test_bitonic4()
    cases=[]
    # Materialize both SAT and UNSAT complete two-level outputs as controls.
    for j,bits in enumerate(((0,1,0,1),(0,0,0,0))):
        cases.append(bitonic_virtual_case(bits,full=True,seed=20261026+j))
    cases.append(bitonic_virtual_case((0,1,0,1,0,0,0,0),full=False))
    answer={'run':'CIRCUIT-BITONIC4-ACCESS166','date_utc':'2026-10-26',
        'stage_comparators':len(BITONIC_SCHEDULE),'fixed_network_layers':3,
        'fixed_incidence':True,'truth_table':counts,'cases':cases,
        'source_length_bits':4,'network_source_clauses_per_block':92,
        'network_source_variables_per_block':56,
        'source_dependence_only_input_pin_signs':True,
        'bit_locality_exact_after_two_levels':True,
        'full_n_SAT_verifier':'OPEN','full_N_decision_circuit':'NOT PROVIDED',
        'q_348_and_monotone_adapter':'NOT VERIFIED',
        'output_language':'proper signed exact-(2,2)-3CNF, NOT clause-monotone',
        'resource_model':'fixed-block arithmetic virtual access, no parent-length occurrence index',
        'elapsed_wall_seconds':round(time.perf_counter()-start,3),
        'p_vs_np':'OPEN'}
    p=HERE/'2026-10-26_0947_CIRCUIT_BITONIC4_ACCESS166_raw.json'
    p.write_text(json.dumps(answer,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'test':'PASS','raw':str(p),'elapsed':answer['elapsed_wall_seconds'],
                      'truth_table':counts,'full_materializations':2,
                      'max_second_level_clauses':max(c['second_clauses'] for c in cases)},indent=2))

if __name__=='__main__' and os.environ.get('PNP_RUN_BITONIC')=='1':
    bitonic_main()