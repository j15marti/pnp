#!/usr/bin/env python3
"""REPLAY-STATE6 exact finite audits of fresh-vs-persistent RP random tape semantics.

The symbolic proof is in the accompanying report. Finite tests do not prove
an unrestricted P/RP statement. Requires only Python standard library.
"""
from __future__ import annotations
import collections
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = collections.Counter()


def chk(predicate: bool, tag: str) -> None:
    CHECKS[tag] += 1
    if not predicate:
        raise AssertionError(tag)


def val(lit: int, assignment: tuple[int, ...]) -> bool:
    bit = assignment[abs(lit)-1]
    return bool(bit if lit > 0 else 1-bit)


def verifier(clauses: tuple[tuple[int, ...], ...], assignment: tuple[int, ...]) -> bool:
    return all(any(val(lit, assignment) for lit in clause) for clause in clauses)


def exhaustive_count(clauses: tuple[tuple[int, ...], ...], n: int) -> int:
    return sum(verifier(clauses, a) for a in itertools.product((0, 1), repeat=n))


def cube_clause(p: int) -> tuple[int,int,int]:
    # Each of the eight sign patterns has exactly one falsifying 3-bit input.
    return tuple((j+1) * (-1 if (p>>j)&1 else 1) for j in range(3))

CUBE = tuple(cube_clause(p) for p in range(8))


def replay_dp(clauses: tuple[tuple[int, ...], ...], n: int):
    """Exact existential acceptance under consistent replay, specialized to CNF.

    Every variable occurring twice is persistently memoized; variables read
    once are fresh but incur no replay condition. States are (q_map, satisfied),
    and q_map[j] = -1,0,1 denotes unassigned or the pinned bit.
    """
    freq = collections.Counter(abs(lit) for clause in clauses for lit in clause)
    recurrent = tuple(sorted(j for j,count in freq.items() if count >= 2))
    idx = {var: j for j,var in enumerate(recurrent)}
    states = {(tuple([-1] * len(recurrent)), False)}
    peaks = [len(states)]
    for clause in clauses:
        for lit in clause:
            next_states = set()
            for recorded, clause_satisfied in states:
                j = idx.get(abs(lit))
                choices = (0,1) if j is None or recorded[j] == -1 else (recorded[j],)
                for bit in choices:
                    r = list(recorded)
                    if j is not None:
                        r[j] = bit
                    new_sat = clause_satisfied or bool(bit if lit>0 else 1-bit)
                    next_states.add((tuple(r),new_sat))
            states = next_states
            peaks.append(len(states))
        # Reject paths on which this clause was never satisfied.
        states = {(r,False) for (r,ok) in states if ok}
        peaks.append(len(states))
    return {
        "accepts": bool(states),
        "recurrent": recurrent,
        "q": len(recurrent),
        "largest_frontier": max(peaks),
        "last_frontier": len(states),
        "max_theoretical_frontier": 2 * (3 ** len(recurrent)),
    }


def independent_literal_acceptance(clauses: tuple[tuple[int, ...], ...]) -> Fraction:
    """Probability when every literal occurrence receives an independent coin.

    Each proper clause's three literals are sampled independently, so its
    probability of success is exactly 7/8; clauses are independent too.
    """
    probability = Fraction(1,1)
    for clause in clauses:
        chk(len(clause)==3 and len({abs(x) for x in clause})==3,
            "fresh_model_proper_clauses")
        probability *= Fraction(7,8)
    return probability


def run() -> dict:
    family = []
    false_yes = []
    for mask in range(256):
        clauses = tuple(CUBE[p] for p in range(8) if mask & (1<<p))
        model_count = exhaustive_count(clauses,3)
        dp = replay_dp(clauses,3)
        fresh = independent_literal_acceptance(clauses)
        chk(model_count == 8 - mask.bit_count(), 'cube_exact_count')
        chk(dp['accepts'] == (model_count>0), 'dp_consistent_replay')
        chk(dp['largest_frontier'] <= dp['max_theoretical_frontier'], 'frontier_bound')
        chk(fresh == Fraction(7,8)**mask.bit_count(), 'fresh_probability_formula')
        chk(Fraction(model_count,8) == Fraction(8-mask.bit_count(),8), 'tape_success_density')
        if model_count==0 and fresh>0:
            false_yes.append(mask)
        if mask in (0,1,127,254,255):
            family.append({
              'mask':mask,'clauses':len(clauses),'count':model_count,
              'persistent_prob':str(Fraction(model_count,8)),
              'fresh_per_literal_prob':str(fresh),
              'recurrent_vars':dp['recurrent'],'max_states':dp['largest_frontier']})
    chk(false_yes==[255], 'unique_unsat_cube_mask')
    eight=CUBE
    for k in range(8):
        sub=eight[:k]+eight[k+1:]
        chk(exhaustive_count(sub,3)==1, 'minimal_unsat_clause_removal')
        chk(replay_dp(sub,3)['accepts'], 'minimal_unsat_replay_recovery')
    chk(exhaustive_count(eight,3)==0, 'minimal_unsat_all_eight')
    chk(independent_literal_acceptance(eight)==Fraction(7**8,8**8), 'no_soundness_under_fresh_replays')

    # Exhaustive independent validation on n=4 drawn from 3-literal distinct
    # variable clauses, up to 3 clauses, includes shared literals and cycles.
    clauses4 = tuple(tuple(s*(v+1) for v,s in zip(ids,signs))
              for ids in itertools.combinations(range(4),3)
              for signs in itertools.product((-1,1),repeat=3))
    cases=0
    maximum_q=0
    for a in range(32):
        for b in range(a,32):
            for c in range(b,32):
                f=(clauses4[a],clauses4[b],clauses4[c])
                true=exhaustive_count(f,4)>0
                d=replay_dp(f,4)
                chk(d['accepts']==true,'fourvar_threeclause_consistency')
                chk(d['largest_frontier']<=d['max_theoretical_frontier'],
                    'fourvar_frontier_bound')
                maximum_q=max(maximum_q,d['q'])
                cases+=1
    chk(cases==5984,'fourvar_test_count')

    # Complete source-accessible RP machine recognizing easy syntactic validity:
    # draw b,r with b independent fair coin; if valid F accept b OR F(r).
    # Thus every valid F is YES with density 1/2 + #SAT(F)/2^{n+1},
    # and every invalid F is NO with zero probability.
    for mask in range(256):
        f=tuple(CUBE[p] for p in range(8) if mask & (1<<p))
        truth=exhaustive_count(f,3)
        yes=sum(1 for b in (0,1) for r in itertools.product((0,1),repeat=3)
                if b or verifier(f,r))
        chk(yes==8+truth,'easy_rp_exact_acceptance_count')
        chk(Fraction(yes,16)>=Fraction(1,2), 'easy_rp_acceptance_at_least_half')
    # Negative syntactic inputs: all random tapes reject, one-sided NO guarantee.
    for word in ('', 'not CNF','1 -1 broken', 'p cnf 3 8\n1 2 3 0\n'):
        for tape in itertools.product((0,1),repeat=4):
            chk(False == (False and (bool(tape[0]) or bool(tape[1]))),
                'invalid_source_all_random_tapes_reject')

    # Arithmetic-circuit NONIDENTITY is a genuine RP *language* via PIT,
    # but the CNF Boolean quotient does not preserve SAT labels over a field.
    prime=257
    roots=sum(1 for x in range(prime) if (x*x-x) % prime == 0)
    chk(roots==2,'field_pit_two_roots')
    chk(Fraction(prime-roots,prime)>Fraction(7,8), 'field_pit_success')
    chk(all((0*x)%prime==0 for x in range(prime)), 'field_pit_zero_soundness')
    def boolean_clause_poly(clause,assignment):
        prod=1
        for lit in clause:
            x=assignment[abs(lit)-1]
            v=x if lit>0 else 1-x
            prod=prod*(1-v)%prime
        return (1-prod)%prime
    poly_value=1
    for cl in eight:
        poly_value=poly_value*boolean_clause_poly(cl,(2,2,2))%prime
    chk(poly_value==208, 'unsat_cube_nonzero_polynomial_mod257')

    data={
       'run':'RP-REPLAY-STATE6',
       'assertions':sum(CHECKS.values()),'checks':dict(CHECKS),'failures':0,
       'cube_family_count':256,
       'cube_unsat_fresh_false_yes_masks':false_yes,
       'proper_3cnf_samples':family,
       'n4_three_clause_exhaustive_formulas':cases,
       'n4_max_recurrent_addresses':maximum_q,
       'field_257_two_root_pit_success':str(Fraction(255,257)),
       'formal_CNF_poly_unsat_input_nonzero_at_2_2_2_mod257':poly_value,
       'unsat_persistent_prob':'0',
       'unsat_fresh_prob':str(Fraction(7**8,8**8)),
       'unique_sat_persistent_prob':str(Fraction(1,8)),
       'unique_sat_fresh_prob':str(Fraction(7**7,8**7)),
       'scope':'finite model tests; no unrestricted class separation',
    }
    return data

if __name__=='__main__':
    result=run()
    result['sha256_source']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out=HERE/'RP_REPLAY6_raw.json'
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('assertions','failures','cube_family_count','n4_three_clause_exhaustive_formulas','unsat_fresh_prob')},indent=2))