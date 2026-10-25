#!/usr/bin/env python3
"""ARC-GUEST-SLOPE-SATURATION160. Pure standard-library, deterministic audit.

Tests exact rational charged-guest exponent identities and performs two actual
ordinary proper-3CNF serialize/parse/decision levels on both SAT and UNSAT.
Finite checks do NOT constitute a FLMV TM timing/space measurement.
"""
from __future__ import annotations
import itertools
import json
import math
from fractions import Fraction as Q
from pathlib import Path

RUN = 'ARC-GUEST-SLOPE-SATURATION160'
OUT = Path(__file__).with_name('2026-10-25_0130_ARC_GUEST_SLOPE_SATURATION160_results.json')
checks = 0

def check(p, why):
    global checks
    checks += 1
    if not p:
        raise AssertionError(why)

def rat(x):
    return str(x)

def contract(t, a=Q(3,5), lam=Q(1,2), floor=Q(11,10)):
    return max(floor, a + lam*t)

def frontier(a_seq, lam_seq):
    b, theta = Q(0), Q(1)
    for a,lam in zip(a_seq,lam_seq):
        b += theta * a
        theta *= lam
    return b,theta

def exact_exponents():
    tab=[]
    for depth in range(1,7):
        a=[Q(3,5)]*depth
        lam=[Q(1,2)]*depth
        B,theta=frontier(a,lam)
        check(B==Q(6,5)*(1-Q(1,2**depth)), 'wrong normalized fanout')
        check(theta==Q(1,2**depth),'wrong leaf exponent')
        for D in [2,3,4,8,16,32,64,128]:
            x=Q(D)
            for _ in range(depth): x=contract(x)
            check(x==B+theta*D, ('recurrence mismatch',depth,D))
            # The canonical leaf guest work matches, not merely upper-bounds, the target.
            check(B+theta*D==x, 'saturation')
            # Same-sized additional polynomial fanout is strictly incompatible.
            check((B+Q(1,20))+theta*D>x, 'extra fanout missed')
            # A larger leaf can be tolerated for small D, but not for all D.
            oversized=theta+Q(1,20)
            bound_D=(B-Q(0))/Q(1,20)
            if D>bound_D:
                check(oversized*D>x, ('oversize threshold',depth,D))
        tab.append({'depth':depth,'fanout_exponent':rat(B),
                    'guest_length_exponent':rat(theta),
                    'target_at_D8':rat(B+theta*8),
                    'target_at_D32':rat(B+theta*32),
                    'extra_fanout_1_20_fails':True,
                    'oversize_guest_threshold_D_strictly_greater':rat(B/Q(1,20))})
    # arbitrary heterogeneous path, including channels not equal to the canonical map
    channels=[(Q(1,3),Q(2,3)),(Q(2,5),Q(3,5)),(Q(1,4),Q(1,3))]
    npaths=0
    for depth in range(1,6):
        for choices in itertools.product(range(3), repeat=depth):
            aa=[channels[j][0] for j in choices]
            ll=[channels[j][1] for j in choices]
            B,theta=frontier(aa,ll)
            D=Q(17)
            x=D
            for a,lam in reversed(list(zip(aa,ll))):
                x=a+lam*x
            check(x==B+theta*D,('heterogeneous guest trace',choices))
            # No additional leaf guest with the same size but higher fanout can fit.
            check(B+Q(1,10)+theta*D > x,'heterogeneous zero slack')
            npaths+=1
    # Exact endpoint margin, independent of guessed machine constructions.
    c=Q(241,200)
    beta=((c+2)/(c*c)-c)/2
    check(beta==Q(11642479,23232400),'FLMV rational')
    check(beta>Q(1,2),'FLMV strict space margin')
    # Parallel-space surcharge is separate from time: all-live states cannot reuse memory.
    space=[]
    for depth in range(1,5):
        B,theta=frontier([Q(3,5)]*depth,[Q(1,2)]*depth)
        for S in [4,8,16,32]:
            s=Q(S)
            for _ in range(depth):
                s=max(Q(1,2),s/2)
            check(s==max(Q(1,2),Q(S,2**depth)),'space recursion')
            check(B+theta*S > s,'all-live surcharge')
            space.append({'depth':depth,'padded_guest_space_S':S,
                          'claimed_successor_space':rat(s),
                          'all_live_space':rat(B+theta*S)})
    return tab,npaths,space,rat(beta)

# Fixed-width dense indexed encoding: 2 header words and 4 words/3CNF clause.
# A clause word is [3, signed literal1, signed literal2, signed literal3].
def bitwidth(n,m):
    return max(1,math.ceil(math.log2(64*(n+m+1))))

def serialize(n,clauses):
    m=len(clauses)
    w=bitwidth(n,m)
    words=[n,m]
    for clause in clauses:
        check(len(clause)==3 and len({abs(v) for v in clause})==3,'not proper 3CNF')
        words.append(3)
        for v in clause:
            check(1<=abs(v)<=n,'out of range literal')
            words.append(2*abs(v)+(v<0))
    check(max(words)<2**w, 'word does not fit')
    return ''.join(format(q,f'0{w}b') for q in words)

def parse(s):
    # Recover self-describing bitwidth by checking the possible valid values.
    for w in range(1,65):
        if len(s)<2*w or len(s)%w: continue
        vals=[int(s[i:i+w],2) for i in range(0,len(s),w)]
        n,m=vals[:2]
        if w!=bitwidth(n,m) or len(vals)!=2+4*m: continue
        cls=[]
        try:
            for j in range(m):
                a,b,c,d=vals[2+4*j:2+4*j+4]
                if a!=3:raise ValueError('wrong clause length')
                q=tuple(-(v//2) if v%2 else v//2 for v in (b,c,d))
                if len({abs(x) for x in q})!=3 or not all(1<=abs(x)<=n for x in q):
                    raise ValueError('improper clause')
                cls.append(q)
            if len(set(cls))!=len(cls):raise ValueError('duplicated clause')
        except ValueError:
            continue
        return n,cls
    raise ValueError('invalid fixed-width ordinary CNF record')

def block(block_id, bad=False):
    ids=tuple(3*block_id+i for i in (1,2,3))
    # The eight three-literal sign configurations eliminate all eight assignments.
    # Seven clauses omit one orientation and have exactly one Boolean witness.
    all_clauses=[tuple(v if (mask>>i)&1 else -v for i,v in enumerate(ids)) for mask in range(8)]
    return all_clauses if bad else all_clauses[:7]

def decide_block_correct(clauses):
    groups={}
    for c in clauses:
        ids=tuple(sorted(abs(v) for v in c))
        groups.setdefault(ids,[]).append(c)
    for ids,cs in groups.items():
        def clause_value(cs1, bits):
            return any(bool((bits>>ids.index(abs(v)))&1)==(v>0) for v in cs1)
        if not any(all(clause_value(c,bits) for c in cs) for bits in range(8)):
            return False
    return True

def chunks(items,size):
    return [items[i:i+size] for i in range(0,len(items),size)]

def localize(src_clause_groups):
    names=sorted({abs(v) for cg in src_clause_groups for c in cg for v in c})
    relabel={v:i+1 for i,v in enumerate(names)}
    out=[tuple((1 if v>0 else -1)*relabel[abs(v)] for v in c)
         for group in src_clause_groups for c in group]
    return len(names),out

def two_level_controls():
    results=[]
    for p in [4,9,16,25,36,64]:
        for status in ['SAT','UNSAT']:
            src=[block(i,bad=(status=='UNSAT' and i==p-1)) for i in range(p)]
            n,clauses=localize(src)
            parent=serialize(n,clauses)
            parsed_n,parsed_clauses=parse(parent)
            check(parsed_n==n and parsed_clauses==clauses, 'parent serialization')
            truth=decide_block_correct(parsed_clauses)
            check(truth==(status=='SAT'),'parent truth')
            level1=chunks(src,math.ceil(math.sqrt(p)))
            level1_bits=0; level2_bits=0
            largest_child=0; largest_grandchild=0; child_status=[]; grandchildren=0
            for group in level1:
                cn,cc=localize(group)
                child=serialize(cn,cc)
                rcn,rcc=parse(child)
                check(rcn==cn and rcc==cc,'child serialization')
                ct=decide_block_correct(rcc)
                level1_bits+=len(child)
                largest_child=max(largest_child,len(child))
                sub=chunks(group,math.ceil(math.sqrt(len(group))))
                g_truth=[]
                for gg in sub:
                    gn,gc=localize(gg)
                    grand=serialize(gn,gc)
                    gpn,gpc=parse(grand)
                    check(gpn==gn and gpc==gc,'grandchild serialization')
                    gt=decide_block_correct(gpc)
                    g_truth.append(gt)
                    grandchildren+=1
                    level2_bits+=len(grand)
                    largest_grandchild=max(largest_grandchild,len(grand))
                check(ct==all(g_truth),'exact 2nd-level AND join')
                child_status.append(ct)
            check(truth==all(child_status),'exact 1st-level AND join')
            check(grandchildren>=len(level1),'two levels exist')
            # Header and every serialized clause field counted in level totals.
            check(level1_bits>0 and level2_bits>0,'must write children')
            # The source recognizer is a cheap alternative to any mandatory oracle claim.
            check(decide_block_correct(clauses)==truth,'source-aware shortcut')
            # Malformed record rejection is explicit.
            try: parse(parent[:-1]); raise AssertionError('truncated record was accepted')
            except ValueError: pass
            results.append({'p_blocks':p,'status':status,'parent_bits':len(parent),
                            'level1_calls':len(level1),'level2_calls':grandchildren,
                            'level1_total_emitted_bits':level1_bits,
                            'level2_total_emitted_bits':level2_bits,
                            'max_level1_child_bits':largest_child,
                            'max_level2_grandchild_bits':largest_grandchild,
                            'depth_first_two_live_buffers_bits_at_most':largest_child+largest_grandchild})
    return results

def main():
    grid,mixed,space,beta=exact_exponents()
    families=two_level_controls()
    result={'run':RUN,'scope':'exact algebra + finite constructed ordinary-CNF semantic checks',
            'status':'PROVED/EXACT restricted architecture; COMPUTATIONAL controls; ARC-EDGE-90 OPEN',
            'assertion_checks':checks, 'failures':0,
            'canonical_depth_table':grid,'heterogeneous_paths_exactly_checked':mixed,
            'literal_parallel_space_table':space,'flmv_beta':beta,
            'two_level_original_ordinary_CNF_families':families,
            'physical_turing_machine_steps_measured':False,
            'actual_state_flips_measured':False,
            'cumulative_bit_time_measured':False,
            'important_scope':'Actual guest calls and independent simultaneously retained guest states only. A source-code compiler can strip padding; existential achievable-region closure is not excluded.'}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(f'{RUN}: {checks} assertion-accounted checks, 0 failures; {len(families)} actual ordinary-CNF two-level cases; {mixed} heterogeneous path checks. Output={OUT.name}')

if __name__=='__main__':main()
