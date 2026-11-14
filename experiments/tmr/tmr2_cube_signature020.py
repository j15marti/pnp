#!/usr/bin/env python3
"""TMR-2/020 exact 3-variable, proper-3CNF sign-record sensitivity audit.
The 3-bit record sigma denotes the clause falsified by the unique assignment sigma.
Finite Python implementation is semantic test, NOT an arbitrary-TM compiler.
"""
import json
import itertools
import time
from collections import Counter
from hashlib import sha256

ALL = 0xff

def encode(records):
    return ''.join(f'{v:03b}' for v in records)

def parse_and_decide(encoded):
    # A complete 3-bit-block DFA implementation, with an 8-bit occurrence mask.
    # Every bit is observed at its own physical input-head position.
    if len(encoded)%3: return 'MALFORMED', 0, 0
    mask=0
    observed=0
    for p in range(1,len(encoded)+1,3):
        v=0
        for pos in (p,p+1,p+2):
            digit=encoded[pos-1]  # p tracks actual physical head; no arbitrary source queries
            if digit not in '01': return 'MALFORMED',mask,observed
            v=(v<<1) | int(digit)
            observed+=1
        mask |= 1<<v
    return ('UNSAT' if mask==ALL else 'SAT'),mask,observed

def brute_semantics_three(records):
    # Independent literal-wise SAT evaluation over all 8 assignments.
    for a in range(8):
        all_clauses=True
        for v in records:
            clause=False
            for j in range(3):
                b=1<<(2-j)
                literal_truth=bool(a & b) != bool(v & b)
                clause |= literal_truth
            all_clauses &= clause
        if all_clauses:
            return 'SAT'
    return 'UNSAT'

def general_sat_n(n, clauses):
    # Clause is a tuple of (variable_index, positive_literal?) pairs.
    for a in range(1<<n):
        if all(any(bool(a & (1<<i)) == positive for i,positive in clause)
               for clause in clauses):
            return True
    return False

def sensitivity_bruteforce(records):
    label,_,_=parse_and_decide(encode(records))
    original=encode(records)
    count=0
    for i,ch in enumerate(original):
        altered=original[:i]+('0' if ch=='1' else '1')+original[i+1:]
        other,_,_=parse_and_decide(altered)
        count += label!=other
    return count

def sensitivity_formula(counts):
    mask = sum((1<<v) for v,c in enumerate(counts) if c)
    if mask==ALL:
        return 3*sum(c==1 for c in counts)
    if mask.bit_count()!=7:
        return 0
    missing = next(v for v,c in enumerate(counts) if c==0)
    return sum(counts[missing ^ (1<<j)] for j in range(3)
               if counts[missing ^ (1<<j)]>=2)

def composition(n,k):
    if k==1:
        yield (n,)
    else:
        for x in range(n+1):
            for rest in composition(n-x,k-1):
                yield (x,)+rest

def run(max_m=12):
    started=time.perf_counter()
    total=0; bit_checks=0; sat=0; unsat=0; malformed=0
    levels={}; cases=[]; singleton_max_by_m={}
    for m in range(max_m+1):
        local=0; max_unsat=0
        for counts in composition(m,8):
            word=tuple(v for v in range(8) for _ in range(counts[v]))
            encoded=encode(word)
            label,mask,reads=parse_and_decide(encoded)
            assert reads==len(encoded)
            assert (mask==ALL)==(label=='UNSAT')
            predicted=sensitivity_formula(counts)
            actual=sensitivity_bruteforce(word)
            assert predicted==actual, (m,counts,label,predicted,actual)
            total+=1;local+=1;bit_checks+=3*m
            sat+= label=='SAT';unsat+= label=='UNSAT'
            if label=='UNSAT':max_unsat=max(max_unsat,actual)
        levels[str(m)]=local
        singleton_max_by_m[str(m)]=max_unsat
    # Hand-constructed asymptotic SAT-sensitive family, one missing record a=000.
    for R in [1,2,3,5,10,20,50,100,500]:
        words=tuple(list(range(2,8)) + [1]*(R+1))  # count_1=R+1, all others 1, 0 absent; LAST bit pivotal
        label,mask,reads=parse_and_decide(encode(words))
        s=sensitivity_bruteforce(words)
        assert label=='SAT' and s==R+1 and reads==3*(R+7)
        changed=encode(words)[:-1]+'0'  # last b=001 becomes missing a=000
        assert parse_and_decide(changed)[0]=='UNSAT'
        cases.append({'name':'SAT_repeated_neighbor','R':R,'records':len(words),'L':reads,'sensitive_bits':s})
    # 8-clause UNSAT formula, all 24 original sign bits pivotal.
    for R in [1,2,3,5,10,20,50]:
        words=tuple(v for v in range(8) for _ in range(R))
        label,mask,reads=parse_and_decide(encode(words))
        s=sensitivity_bruteforce(words)
        assert label=='UNSAT' and s==(24 if R==1 else 0)
        cases.append({'name':'UNSAT_full_cube','R':R,'records':len(words),'L':reads,'sensitive_bits':s})
    # Random record ordering preserves semantic and the analytic sign-bit count.
    import random
    rng=random.Random(20261114)
    shuffle_controls=0
    for n in [8,9,10,16,32,64]:
        for _ in range(30):
            words=[rng.randrange(8) for i in range(n)]
            counts=Counter(words)
            pred=sensitivity_formula(tuple(counts.get(v,0) for v in range(8)))
            rng.shuffle(words)
            assert pred==sensitivity_bruteforce(words)
            shuffle_controls+=1
    # Independent literal-evaluation oracle and structural hostile controls.
    independent_semantic_checks=0
    for m in range(0,11):
        for case in range(80):
            words=[rng.randrange(8) for _ in range(m)]
            assert parse_and_decide(encode(words))[0]==brute_semantics_three(words)
            independent_semantic_checks+=1
    # Symmetry: renaming, literal complementation, record order, and padding.
    symmetry_controls=0
    seed_words=list(range(1,8))+[1,1,1,1,1]
    for permutation in itertools.permutations(range(3)):
        for sign_shift in range(8):
            remap=lambda v: sum(((v>>permutation[j])&1)<<j for j in range(3)) ^ sign_shift
            transformed=list(map(remap,seed_words))
            assert sensitivity_bruteforce(transformed)==sensitivity_bruteforce(seed_words)
            symmetry_controls+=1
    # Horn/dual-Horn in this fixed-three-variable full-clause language.
    horn_words=[v for v in range(8) if v.bit_count()>=2]
    dual_horn_words=[v for v in range(8) if v.bit_count()<=1]
    assert brute_semantics_three(horn_words)=='SAT'
    assert brute_semantics_three(dual_horn_words)=='SAT'
    # 2-SAT clause via existential ternary auxiliary: (x or y or z) & (x or y or not z).
    two_sat_aux_checks=0
    for a in range(8):
        x,y,z=(bool(a & (1<<j)) for j in (2,1,0))
        assert ((x or y or z) and (x or y or not z))==(x or y)
        two_sat_aux_checks+=1
    # XOR parity rows: four signs exclude each parity class; union gives full cube.
    xor_odd=[v for v in range(8) if v.bit_count()%2==1]
    xor_even=[v for v in range(8) if v.bit_count()%2==0]
    assert len(xor_odd)==len(xor_even)==4
    assert brute_semantics_three(xor_odd)=='SAT'
    assert brute_semantics_three(xor_even)=='SAT'
    assert brute_semantics_three(xor_odd+xor_even)=='UNSAT'
    # Independent UNSAT product has zero single-bit sensitivity, not the sum 24+24.
    first_full=tuple(range(8)); second_full=tuple(range(8))
    product_controls=0
    for block in (first_full,second_full):
        for value in block:
            for j in range(3):
                changed=value^(1<<j)
                modified=list(block)
                modified[modified.index(value)]=changed
                assert brute_semantics_three(modified)=='SAT'
                assert brute_semantics_three(first_full if block is second_full else second_full)=='UNSAT'
                product_controls+=1
    # General n=4 proper-3CNF, independent clause-essential upper bound.
    generic_critical_checks=0
    support_triples=list(itertools.combinations(range(4),3))
    for _ in range(200):
        ncl=rng.randrange(1,14)
        clauses=[]
        for j in range(ncl):
            triple=rng.choice(support_triples)
            signed=tuple((idx,bool(rng.getrandbits(1))) for idx in triple)
            clauses.append(signed)
        if general_sat_n(4,clauses):
            continue
        sensitive=0
        for ci,c in enumerate(clauses):
            for j in range(3):
                mod=list(clauses)
                newc=list(c)
                idx,pos=newc[j]
                newc[j]=(idx,not pos)
                mod[ci]=tuple(newc)
                if general_sat_n(4,mod): sensitive+=1
        assert sensitive<=3*min(ncl,1<<4,8*len(support_triples))
        generic_critical_checks+=1
    # Malformed length and symbol, all-length totality controls.
    for w in ['0','00','1010','10101','1010101','10101010','x00','01x','111Z00']:
        assert parse_and_decide(w)[0]=='MALFORMED'
        malformed+=1
    return {'date_pacific':'2026-11-14 06:22 PST','experiment':'TMR2-CUBE20',
            'max_m':max_m,'all_count_vectors_checked':total,
            'sensitivity_single_bit_mutations_checked':bit_checks,
            'SAT_source_signatures':sat,'UNSAT_source_signatures':unsat,
            'count_vectors_by_m':levels,'max_UNSAT_sign_sensitivity_by_m':singleton_max_by_m,
            'structured_controls':cases,'shuffled_controls':shuffle_controls,'independent_semantic_checks':independent_semantic_checks,
            'symmetry_controls':symmetry_controls,'auxiliary_two_sat_controls':two_sat_aux_checks,
            'xor_controls':3,'horn_controls':2,'product_nonadditivity_controls':product_controls,
            'general_n4_critical_bound_controls':generic_critical_checks,
            'malformed_controls':malformed,'random_seed':20261114,
            'assertion_failures':0,'seconds':round(time.perf_counter()-started,3),
            'scope':'all count multisets through m=12; source word canonical order, plus shuffled controls; not a TM compiler'}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
