#!/usr/bin/env python3
"""CHMYADDSLOTBRACKET2: exact small-field additive-slot identities and bounds.

This is a reproducible finite TEST of the declared FK recurrence and a field-inner-
product mask primitive, NOT an instantiation of the full security parameters of
CHMY's gamma-almost-k-wise distributions.

The symbolic theorem in the accompanying report uses only independence ACROSS
layers, gamma-almost 2-wise uniform masks, and Boolean circuit counting.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, random, time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

FIELD_POLY = {3: 0b1011, 4: 0b10011, 5: 0b100101}
SEED = 202610201549


def gf_mul(a: int, b: int, h: int) -> int:
    poly = FIELD_POLY[h]
    mask = (1 << h) - 1
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & (1 << h):
            a ^= poly
    return out & mask


def gf_pow(a: int, j: int, h: int) -> int:
    acc = 1
    while j:
        if j & 1:
            acc = gf_mul(acc, a, h)
        a = gf_mul(a, a, h)
        j >>= 1
    return acc


def parity(a: int) -> int:
    return a.bit_count() & 1


def field_mask(a: int, b: int, h: int, N: int) -> int:
    """CHMY Thm 33 small-bias field-inner-product primitive, N<=2^h-1."""
    assert 0 <= a < (1 << h) and 0 <= b < (1 << h)
    assert N < (1 << h)
    return sum(parity(gf_pow(a, j, h) & b) << (j - 1) for j in range(1, N + 1))


def all_masks(h: int, N: int) -> list[int]:
    return [field_mask(a, b, h, N) for a in range(1 << h) for b in range(1 << h)]


def fk_base(G1: int, Ds: list[int], Ts: list[int], N: int) -> int:
    g = G1
    for d, t in zip(Ds, Ts):
        g = d ^ (t & g)
    return g & ((1 << N) - 1)


def fk_inject(f: int, G1: int, Ds: list[int], Ts: list[int], N: int, slot: int) -> int:
    """slot=0 replaces G1 by G1 XOR f; slot=j>=1 inserts f in additive D_j."""
    assert 0 <= slot <= len(Ts)
    g = G1 ^ (f if slot == 0 else 0)
    for j, (d, t) in enumerate(zip(Ds, Ts), start=1):
        g = (d ^ (f if j == slot else 0)) ^ (t & g)
    return g & ((1 << N) - 1)


def tail_mask(Ts: list[int], N: int, slot: int) -> int:
    acc = (1 << N) - 1
    # Slot j=0 in G1 is screened by every T_1,...,T_{r-1}.
    # Slot j>=1 added in D_j bypasses T_j, but not T_{j+1},...,T_{r-1}.
    for t in Ts[slot:]:
        acc &= t
    return acc


def enumerate_at_most_two_gate_functions(n: int) -> tuple[set[int], set[int]]:
    """AND/OR/NOT gate DAG, constants and n projections free as sources."""
    N = 1 << n
    allbits = (1 << N) - 1
    inputs = [sum(((j >> k) & 1) << j for j in range(N)) for k in range(n)]
    inputs += [0, allbits]
    less1 = set(inputs)
    less2 = set(inputs)
    def choices(vals):
        for x in vals:
            yield allbits ^ x
        for i in range(len(vals)):
            for j in range(i, len(vals)):
                yield vals[i] & vals[j]
                yield vals[i] | vals[j]
    for g1 in choices(inputs):
        less2.add(g1)
        for g2 in choices(inputs + [g1]):
            less2.add(g2)
    return less1, less2


def exhaustive_mask_audit(N: int, h: int, max_t: int, support_bits: tuple[int,...]):
    masks = all_masks(h, N)
    count = len(masks)
    m = (1 << N) - 1
    S = sum(1 << i for i in support_bits)
    assert count == (1 << (2*h))
    moments = []
    for t in range(max_t + 1):
        # up to 65,536 exact seed combinations for h=4, t=2
        combos = itertools.product(masks, repeat=t)
        dist, total, live = Counter(), 0, 0
        image_tests = 0
        for combo in combos:
            a = m
            for T in combo:
                a &= T
            overlap = (a & S).bit_count()
            dist[overlap] += 1
            live += overlap
            total += 1
            # For a fixed seed: all source tables supported on S yield exactly 2^overlap images.
            if image_tests < 512 or total % 997 == 0:
                outputs = {a & f for f in range(1 << N) if (f & ~S) == 0}
                assert len(outputs) == (1 << overlap)
                image_tests += 1
        marginal = (1 - 2**(-h)) / 2
        assert total == count**t
        assert abs(live / (total * len(support_bits)) - marginal**t) < 1e-10
        moments.append({"tail_layers":t,"seed_count":total,"support":list(support_bits),
                        "mask_coordinate_marginal":marginal,"mean_live_bits":live/total,
                        "expected_live_bits":len(support_bits)*marginal**t,
                        "live_histogram":{str(i):dist[i] for i in range(len(support_bits)+1)},
                        "image_cardinality_tests":image_tests})
    # Two independent layers vs deliberately reused identical mask.
    if max_t >= 2:
        indep = moments[2]["mean_live_bits"]
        same = sum((a&S).bit_count() for a in masks) / len(masks)
        assert same > indep
    else:
        same=None
    return {"N":N,"h":h,"total_distinct_seeds":count,"support":list(support_bits),
            "moments":moments,"reuse_same_mask_mean_live":same}


def randomized_recurrence_tests(rng, N:int, h:int, count:int):
    r = N.bit_length()-1
    assert 1 << r == N
    full = (1 << N)-1
    slots = range(0,r)
    checks=0
    malformed_rejected=0
    comp_checks=0
    sampled_tail=Counter()
    for _ in range(count):
        Ts=[field_mask(rng.randrange(1<<h),rng.randrange(1<<h),h,N) for _ in range(r-1)]
        Ds=[field_mask(rng.randrange(1<<h),rng.randrange(1<<h),h,N) for _ in range(r-1)]
        G1=rng.getrandbits(N)
        base=fk_base(G1,Ds,Ts,N)
        tested_f=[0,full,1,full ^1,rng.getrandbits(N)]
        tested_f += [1<<rng.randrange(N),rng.getrandbits(N)]
        for slot in slots:
            A=tail_mask(Ts,N,slot)
            sampled_tail[(slot,A.bit_count())] +=1
            for f in tested_f:
                actual=fk_inject(f,G1,Ds,Ts,N,slot)
                assert actual==(base^(A&f))
                assert actual^fk_inject(f^full,G1,Ds,Ts,N,slot)==A
                checks+=2
            if slot==r-1:
                assert A==full
                assert fk_inject(base,G1,Ds,Ts,N,slot)==0  # source DEPENDS ON seed: hostile
                comp_checks+=1
        try:
            fk_inject(1,G1,Ds,Ts,N,r)
        except AssertionError:
            malformed_rejected +=1
        else:
            raise AssertionError('invalid slot accepted')
    return {"N":N,"h":h,"trials":count,"algebra_identity_checks":checks,
            "seed_dependent_cancellation_controls":comp_checks,
            "invalid_slot_rejections":malformed_rejected,
            "tail_weight_histograms":{str(slot):{str(w):c for (s,w),c in sampled_tail.items() if s==slot}
                                       for slot in slots}}


def finite_no_control(n=3):
    yes0, yes2=enumerate_at_most_two_gate_functions(n)
    N=1<<n
    spike=1 << 0
    assert spike not in yes2
    assert 0 in yes0
    masks=all_masks(n+1,N)
    ones=len(masks)
    survivor=sum(bool(mask & spike) for mask in masks)/ones
    # For an independent 2-layer tail, the two-seed joint distributions
    # agree with probability >=1-p^2. With public seed the exact TV is p^2.
    p2=survivor**2
    assert p2 < 1/3
    return {"n":n,"N":N,"basis":"AND2,OR2,NOT; constants and projections free",
            "enumerated_at_most_zero_gate":len(yes0),
            "enumerated_at_most_two_gate":len(yes2),
            "source_yes":"all zero", "source_no":"single output spike at coordinate 0",
            "source_no_not_in_two_gate_class":True,
            "field_coordinate_survival_one_layer":survivor,
            "field_coordinate_survival_two_independent_layers":p2,
            "joint_public_seed_TV":p2,"required_gap_for_1_3_error":1/3,
            "therefore_two_sided_promise_cannot_hold":True}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--seed',type=int,default=SEED)
    ap.add_argument('--trials',type=int,default=3000)
    ap.add_argument('--output',default='/mnt/data/mcsp_20261020/2026-10-20_CHMYADDSLOTBRACKET2.json')
    a=ap.parse_args()
    tm=time.monotonic()
    rng=random.Random(a.seed)
    out={"run_id":"CHMYADDSLOTBRACKET2","seed":a.seed,
         "model":"modified FK recurrence with source added to D_j, plus field-inner-product toy masks",
         "not_claimed":"Full CHMY PRG pseudorandomness, a threshold descent, or exact asymptotic one-tape timings",
         "exhaustive":[exhaustive_mask_audit(4,3,1,(0,1)),
                        exhaustive_mask_audit(8,4,2,(0,1,3))],
         "random_recurrence":[randomized_recurrence_tests(rng,4,3,a.trials),
                              randomized_recurrence_tests(rng,8,4,a.trials),
                              randomized_recurrence_tests(rng,16,5,a.trials)],
         "finite_NO_control":finite_no_control(),
         "asymptotic_conditions":{"YES_no_go":"q=floor(s/(c*n)); q*2^{-t} >> s_prime*log(N); gamma*t=o(1)",
             "NO_no_go":"q=ceil(C*s*log(n+s)); q*2^{-t}<1/3",
             "threshold_parameters":"s=N^mu, s_prime=N^beta_prime, 0<beta_prime<mu<1",
             "proven_late_zone":"t <= (mu-beta_prime-epsilon)*log2(N)",
             "proven_early_zone":"t >= (mu+epsilon)*log2(N)",
             "unresolved_critical_window":"roughly (mu-beta_prime)*log2(N) < t < mu*log2(N)"},
         "status":"COMPUTATIONAL supporting symbolic proofs, independent review pending; P versus NP OPEN"}
    out['total_exhaustive_seed_combinations']=sum(sum(k['seed_count'] for k in x['moments']) for x in out['exhaustive'])
    out['total_exhaustive_image_checks']=sum(sum(k['image_cardinality_tests'] for k in x['moments']) for x in out['exhaustive'])
    out['total_recurrence_checks']=sum(x['algebra_identity_checks'] for x in out['random_recurrence'])
    out['elapsed_seconds']=round(time.monotonic()-tm,4)
    path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({"run_id":out['run_id'],"total_exhaustive_seed_combinations":out['total_exhaustive_seed_combinations'],
                      "total_exhaustive_image_checks":out['total_exhaustive_image_checks'],
                      "total_recurrence_checks":out['total_recurrence_checks'],
                      "finite_NO_control":out['finite_NO_control'],
                      "elapsed_seconds":out['elapsed_seconds'],"output":str(path)},indent=2))


if __name__=='__main__':main()
