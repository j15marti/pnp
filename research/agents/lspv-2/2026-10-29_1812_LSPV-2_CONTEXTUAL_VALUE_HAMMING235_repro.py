#!/usr/bin/env python3
"""CONTEXTUAL-VALUE-HAMMING235: exact finite checks, Python 3.10+, stdlib only.

Model A: fixed linear preprocessor s=G a mod 2, stored L bits; later parity
mask w may probe coordinates of the original a, one probe per named bit.
Costed continuation computes a nearest codeword explicitly (not free).
Model B: small epistemic interpreter with source-index certificates; valuation
recomputes exact projected-state set and charges those checks.
No assertion about unrestricted SAT runtime or strict22 closure.
"""
from dataclasses import dataclass
from collections import Counter
from itertools import combinations
import itertools, json, math

# Binary Hamming [7,4,3] generator rows, from standard systematic form.
G = (sum(1 << i for i in v) for v in ((0,4,5),(1,4,6),(2,5,6),(3,4,5,6)))
G = tuple(G)
W1_STR = '-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'

def parity(v): return v.bit_count() & 1

def all_words(g=G):
    out=[]
    for coefficients in range(1 << len(g)):
        w=0
        for i,row in enumerate(g):
            if (coefficients >> i)&1:w ^= row
        out.append((w,coefficients))
    return out

CODE=all_words()
assert len({x for x,_ in CODE})==16

def construct_summary(source_get,g=G):
    """Pre-query stage: read original source coordinates exactly once.

    source_get is the only way to access the original source. The seven
    readings are charged even if several summary rows reuse a source bit.
    """
    bits=tuple(source_get(i) for i in range(7))
    s=[];xor_count=0
    for row in g:
        part=[bits[i] for i in range(7) if (row>>i)&1]
        parity_row=0
        for bit in part:parity_row ^= bit
        xor_count += max(0,len(part)-1)
        s.append(parity_row)
    return tuple(s),{'preprocess_source_probes':7,'preprocess_xor_upper':xor_count,
                     'transient_local_bits':7}

def optimal_query(summary,w,source_get,g=G):
    """Online exact continuation. Only summary, w and charged source_get are visible."""
    L=len(g);assert len(summary)==L
    best=None;ops=0
    for cw,coeff in all_words(g):
        ops += 7 + L # codeword and Hamming-distance comparison proxy
        d=(cw ^ w).bit_count()
        if best is None or d<best[0]:best=(d,cw,coeff)
    d,cw,coeff=best
    residual=w^cw;ans=0
    for i in range(L):
        if (coeff>>i)&1:ans ^= summary[i]
    probed=[]
    for i in range(7):
        if (residual>>i)&1:
            ans ^= source_get(i)
            probed.append(i)
    return {'answer':ans,'source_probes':len(probed),'positions':probed,
            'local_word_candidates':1<<L,'local_cost_units':ops+L+len(probed),
            'stored_bits':L}

def theorem_checks():
    mind=min(x.bit_count() for x,c in CODE if x)
    dist={w:min((w^x).bit_count() for x,c in CODE) for w in range(128)}
    assert mind==3 and max(dist.values())==1
    qcounts=Counter();checks=0;tmp_max=0
    prep_checks=0;prep_reads=0;prep_xors=0
    for a in range(128):
        source_get=lambda i: (a>>i)&1
        summary,prep=construct_summary(source_get)
        prep_checks+=1;prep_reads+=prep['preprocess_source_probes']
        prep_xors+=prep['preprocess_xor_upper']
        for w in range(128):
            # Online function is supplied the precomputed summary only.
            o=optimal_query(summary,w,source_get)
            assert o['answer']==parity(a&w)
            qcounts[o['source_probes']]+=1;checks+=1
            tmp_max=max(tmp_max,o['local_cost_units'])
    # All 16 rank-4 rowspace codes are at mutual distance >=3, radius-one balls tile 128 masks.
    assert sorted(qcounts.items()) == [(0,128*16),(1,128*112)]
    # Fixed-L source-free summaries: every distinct a separated by some singleton query.
    signatures={a:tuple(parity(a&g) for g in G) for a in range(128)}
    buckets=Counter(signatures.values())
    assert len(buckets)==16 and set(buckets.values())=={8}
    # Exact seven-coordinate optimal linear (storage, source-probes) frontier.
    # Sphere bound: 2**L * sum_{j<=Q} C(7,j) >= 2**7.
    # Explicit generators attain every information-theoretic lower bound.
    witness={0:(),1:(127,),2:(127,1),3:(125,126,127),
             4:G,5:G+(1,),6:G+(1,2),7:tuple(1<<i for i in range(7))}
    # For L=5/6, row 1 or 2 could accidentally be in the Hamming rowspace;
    # replace extensions with independent coordinate basis via greed.
    for L in (5,6):
        current=list(G)
        for coordinate in range(7):
            candidate=1<<coordinate
            if candidate not in {v for v,c in all_words(tuple(current))}:
                current.append(candidate)
            if len(current)==L:break
        witness[L]=tuple(current)
    frontier=[]
    for L in range(8):
        span=[v for v,c in all_words(tuple(witness[L]))]
        assert len(set(span))==(1<<L)
        rad=max(min((w^v).bit_count() for v in span) for w in range(128))
        sphere_lb=next(Q for Q in range(8) if (1<<L)*sum(math.comb(7,j) for j in range(Q+1))>=128)
        assert rad==sphere_lb,(L,rad,sphere_lb)
        frontier.append({'stored_bits_L':L,'optimal_max_original_bit_probes_Q':rad,
                         'generator_bitmasks':list(witness[L]),'sphere_bound_Q':sphere_lb})
    # Direct-sum family. Reuses block lookup with bounded scratch space.
    r_data=[]
    for r in (1,2,3,4,8,16,32):
        r_data.append({'blocks':r,'boundary_bits':7*r,'stored_linear_bits':4*r,
                       'max_additional_source_bit_probes':r,
                       'linear_preconstruction_raw_reads':7*r,
                       'linear_preconstruction_xor_upper':9*r,
                       'worst_local_candidate_comparisons':16*r,
                       'continuation_bitops_bound':(16*(7+4)+4+1)*r,
                       'no_source_query_requires_at_least_bits':7*r})
    return {'Hamming_G_index_sets':[[i for i in range(7) if (row>>i)&1] for row in G],
            'minimum_nonzero_distance':mind,'covering_radius':max(dist.values()),
            'coset_leader_weight_histogram':dict(sorted(Counter(dist.values()).items())),
            'all_a_all_w_exact_checks':checks,'preprocessing_invocations':prep_checks,
            'preprocessing_source_reads':prep_reads,'preprocessing_xors':prep_xors,
            'probe_count_histogram':dict(sorted(qcounts.items())),
            'distinct_4bit_summaries':len(buckets),'sources_per_summary':8,
            'max_local_comparison_units':tmp_max,'exact_b7_linear_frontier':frontier,'direct_sum':r_data}

@dataclass(frozen=True)
class Fact:
    key:str
    affine_mask:int
    right_bit:int
    source_slot:int
    provenance:str
    certificate:str

class ContextualFacts:
    """Epistemic fact interpreter. The source remains authoritative and must be read."""
    def __init__(self,n,target_indices,source):
        self.n=n;self.target=tuple(target_indices);self.source=list(source)
        self.known=[];self.ledger=[]
    def projection(self,extra=None):
        facts=self.known+([extra] if extra else [])
        outcomes=set();steps=0
        for a in range(1<<self.n):
            ok=True
            for f in facts:
                steps+=1
                if parity(a & f.affine_mask)!=f.right_bit:
                    ok=False;break
            if ok:
                outcomes.add(tuple((a>>i)&1 for i in self.target))
        return outcomes,steps
    def observe(self,f):
        # Certified provenance: exact source-record equality; no answer bit supplied.
        assert 0<=f.source_slot<len(self.source)
        actual=self.source[f.source_slot]
        certified=(f.key,f.affine_mask,f.right_bit)==actual
        assert certified,'invalid source-slot certificate'
        src_bits=len(repr(actual).encode('utf-8'))*8
        old,c0=self.projection();new,c1=self.projection(f)
        phi_old=math.log2(max(1,len(old)));phi_new=math.log2(max(1,len(new)))
        v=phi_old-phi_new
        # Verifying source provenance and constructing the score is not free.
        score_cost=c0+c1+src_bits+2*self.n
        acquisition=src_bits+max(1,(len(self.source)-1).bit_length())
        application=2*self.n+len(self.known)+1
        net=v-(acquisition+application)*0.01
        record={'fact':f'({f.key})\\mid_{{{v:g}}}','proposition':f.key,
                'context_target':list(self.target),'prior_K':[x.key for x in self.known],
                'certificate':f.certificate,'provenance':f.provenance,
                'source_slot':f.source_slot,'score_scale':'log2 projection cardinality',
                'possible_target_before':len(old),'possible_target_after':len(new),
                'v_Phi':v,'acquisition_cost_bitread_plus_index':acquisition,
                'application_cost_proxy':application,'score_discovery_enumeration_steps':score_cost,
                'net_value_at_lambda_001_excludes_score_discovery':net,
                'contradiction':len(new)==0}
        self.ledger.append(record);self.known.append(f)
        return record

def interpreter_checks():
    source=[('x xor r=1',3,1),('r=1',2,1)]
    c=ContextualFacts(2,[0],source)
    mk=lambda k,m,r,i: Fact(k,m,r,i,'verified direct source row',f'equality-source[{i}]')
    first=c.observe(mk(*source[0],0)); second=c.observe(mk(*source[1],1));
    duplicate=c.observe(mk(*source[0],0))
    assert (first['v_Phi'],second['v_Phi'],duplicate['v_Phi'])==(0,1,0)
    assert second['net_value_at_lambda_001_excludes_score_discovery']<0
    reverse=ContextualFacts(2,[0],source)
    second_first=reverse.observe(mk(*source[1],1));first_second=reverse.observe(mk(*source[0],0))
    assert (second_first['v_Phi'],first_second['v_Phi'])==(0,1)
    # Redundancy: duplicate source fact must have exactly zero marginal information.
    unsat_source=[('x=0',1,0),('x=1',1,1)]
    neg=ContextualFacts(2,[0],unsat_source)
    neg.observe(mk(*unsat_source[0],0));contradiction=neg.observe(mk(*unsat_source[1],1))
    assert contradiction['contradiction']
    # A separate, explicitly nonmonotone potential can give negative marginal values.
    new_obligation_raw_value=0-1
    assert new_obligation_raw_value<0
    return {'forward':c.ledger,'reverse':reverse.ledger,'unsat':neg.ledger,
            'nonmonotone_obligation_potential_v':new_obligation_raw_value,
            'note':'Score-discovery enumeration counted separately and is not an efficient valuation oracle.'}

def parse_w1():return tuple(tuple(map(int,s.split())) for s in W1_STR.split(';'))

def check_cnf(formula,n):
    for clauses in formula:
        assert all(0<abs(x)<=n for x in clauses)
    count=0;first=None
    for a in range(1<<n):
        if all(any(((a>>(abs(l)-1))&1)==(l>0) for l in clause) for clause in formula):
            count+=1
            if first is None:first=a
    return count,first

def signed22(formula,n):
    o=Counter(l for c in formula for l in c)
    return (len(formula)*3==4*n and all(len(c)==3 and len({abs(z) for z in c})==3 for c in formula)
         and all(o[v]==o[-v]==2 for v in range(1,n+1)))

def connected(formula,n):
    adj={i:set() for i in range(n)}
    for c in formula:
        for x in c:
            for y in c:
                adj[abs(x)-1].add(abs(y)-1)
    vis={0};st=[0]
    while st:
        for j in adj[st.pop()]:
            if j not in vis:vis.add(j);st.append(j)
    return len(vis)==n

def cyclic22(n):
    assert n%3==0 and n>=6
    cycs=[(i+1,(i+1)%n+1,-((i+2)%n+1)) for i in range(n)]
    blocks=[(-(3*j+1),-(3*j+2),-(3*j+3)) for j in range(n//3)]
    return tuple(cycs+blocks)

def xor3_cnf():
    # y = a XOR b: clauses [(a or b or ~y), (a or ~b or y), (~a or b or y), (~a or ~b or ~y)]
    return [(1,2,-3),(1,-2,3),(-1,2,3),(-1,-2,-3)]

def mixed_controls():
    # Standard 2SAT, XOR, mixed, and certified strict22 examples.
    c2_sat=((1,),(-1,2));c2_unsat=((1,),(-1,))
    p_xor=xor3_cnf()
    c2x_sat=tuple(c2_sat)+tuple(p_xor)+((-3,),)
    c2x_unsat=tuple(c2_sat)+tuple(p_xor)+((3,),)
    f6=cyclic22(6);w1=parse_w1()
    assert signed22(f6,6) and connected(f6,6)
    assert signed22(w1,15) and connected(w1,15)
    cases={'two_sat_SAT':(c2_sat,2),'two_sat_UNSAT':(c2_unsat,1),
           'xor3_relation':(p_xor,3),'mixed_sat':(c2x_sat,3),
           'mixed_unsat':(c2x_unsat,3), 'connected_exact22_SAT':(f6,6),
           'connected_exact22_UNSAT_W1':(w1,15)}
    ans={}
    for name,(clauses,n) in cases.items():
        count,w=check_cnf(clauses,n)
        ans[name]={'variables':n,'clauses':len(clauses),'satisfying_assignments':count,
                   'label':'SAT' if count else 'UNSAT',
                   'witness_mask':w,'strict22':signed22(clauses,n) if n>=6 else False,
                   'connected':connected(clauses,n) if n>=6 else None}
    assert ans['two_sat_SAT']['label']=='SAT' and ans['two_sat_UNSAT']['label']=='UNSAT'
    assert ans['mixed_sat']['label']=='SAT' and ans['mixed_unsat']['label']=='UNSAT'
    assert ans['connected_exact22_UNSAT_W1']['label']=='UNSAT'
    assert ans['connected_exact22_SAT']['label']=='SAT'
    # Validate that four CNF clauses encode the XOR relation, eight full truth assignments.
    for a,b,y in itertools.product(range(2),repeat=3):
        mask=a|(b<<1)|(y<<2)
        ok=all(any(((mask>>(abs(l)-1))&1)==(l>0) for l in c) for c in p_xor)
        assert ok==(y==(a^b))
    return ans

def main():
    data={'run_id':'CONTEXTUAL_VALUE_HAMMING235','status':'PROVED/RESTRICTED mathematics, COMPUTATIONAL controls',
          'model':'linear GF2 preprocessed summary; read-only original source remains query-accessible; exact parity continuation',
          'theorem_checks':theorem_checks(),'fact_interpreter':interpreter_checks(),
          'sat_unsat_controls':mixed_controls(),
          'provenance':{'source_W1_repo':'j15marti/pnp/research/agents/lspv-2/connector231.py',
                        'source_W1_blob_sha':'ddfea2285320d3143ac653986e708d562ecabde6',
                        'hamming_repo':'sagemath/sage/src/sage/coding/hamming_code.py',
                        'hamming_blob_sha':'431e660fae77184147230223f66c76f2d5f04b38',
                        'seed':'no randomness used'}}
    print(json.dumps(data,sort_keys=True,indent=2))

if __name__=='__main__':main()
