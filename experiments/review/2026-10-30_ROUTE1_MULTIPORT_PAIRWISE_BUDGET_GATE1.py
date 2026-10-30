#!/usr/bin/env python3
"""Exact pairwise-independent coordinate audit for fixed multiport CHMY-style difference recurrence."""
from itertools import product
from fractions import Fraction
from json import dumps
from pathlib import Path

RUN='2026-10-30_MULTIPORT_PAIRWISE_BRACKET_AND_MARGIN1'


def affine_masks(d):
    masks = []
    for u in range(1 << d):
        for b in (0,1):
            bits = sum((((u & a).bit_count() & 1) ^ b) << a for a in range(1 << d))
            masks.append(bits)
    return masks


def theoretical_probability(h, ports):
    p = Fraction(0)
    for i in range(h):
        p = 1 - p / 2 if ports & (1 << i) else p / 2
    return p


def do_audit():
    out={'run_id':RUN, 'model':'independent layers; each layer uniform affine coordinate mask giving exact pairwise independence, not full coordinate independence', 'families':[], 'total_portsets':0, 'total_seed_port_combinations':0, 'moment_checks':0, 'failed_checks':0, 'hostile_controls':{}}
    for d, maxh in ((2,5),(3,4),(4,2)):
        q=1<<d
        masks=affine_masks(d)
        for h in range(1,maxh+1):
            total=len(masks)**h
            allones=(1<<q)-1
            for ports in range(1,1<<h):
                s1=s2=0
                for seq in product(masks, repeat=h):
                    effective=0
                    for i,mask in enumerate(seq):
                        effective = (effective & mask) ^ (allones if ports & (1<<i) else 0)
                    z=effective.bit_count()
                    s1+=z
                    s2+=z*z
                prob=theoretical_probability(h,ports)
                assert Fraction(s1,total)==q*prob, (d,h,ports,'mean')
                assert Fraction(s2,total)==q*prob+q*(q-1)*prob**2, (d,h,ports,'second')
                latest=ports.bit_length()
                t=h-latest
                assert Fraction(1,2**(t+1)) <= prob <= Fraction(1,2**t)
                out['total_portsets']+=1
                out['total_seed_port_combinations']+=total
                out['moment_checks']+=3
            out['families'].append({'d':d,'coordinates':q,'layers':h,'sequences_per_port':total,'portsets':(1<<h)-1})
    # Adversarial reuse of the same unbiased mask in two layers: exact cancellation is possible.
    reused = [((1 ^ (b & 1)) & b) for b in (0,1)]
    assert reused==[0,0]
    out['hostile_controls']['repeated_T2_T3_for_ports_1_2_h3']={'values':reused,'proved_zero':True}
    # Markov sparse-correction margin: q_NO*2^-t divided by (s'-a)/n at selected symbolic instances.
    out['margin_checks']=[]
    for n,mu_num,beta_num,eps_num in ((40,7,3,1),(80,7,3,1),(200,7,3,1),(400,7,3,1),(600,7,3,1)):
        # mu=0.7, beta=0.3, eps=0.1; use integers for exponent arithmetic
        mu=Fraction(mu_num,10); beta=Fraction(beta_num,10); eps=Fraction(eps_num,10)
        N=1<<n
        s=1 << int(n*mu)
        sp=1 << int(n*beta)
        t=int(n*(mu-beta+eps))
        qNO=min(N, 100*s*(n+1))
        upper=Fraction(qNO, 1<<t)
        # A hypothetical baseline cost at most sp/2, point corrections cost at most 8*n gates per bit.
        spare=sp//2
        bound=Fraction(8*n)*upper/spare
        out['margin_checks'].append({'n':n,'mu':'7/10','beta':'3/10','epsilon':'1/10','t':t,'qNO':qNO,'expected_exposed_upper':str(upper),'markov_failure_bound':str(bound),'bound_lt_one':bound<1})
    return out


if __name__=='__main__':
    obj=do_audit()
    raw=Path('/mnt/data/2026-10-30_MULTIPORT_PAIRWISE_BRACKET_AND_MARGIN1_raw.json')
    raw.write_text(dumps(obj,sort_keys=True,indent=2)+'\n')
    print(dumps({'status':'PASS','path':str(raw),**{k:obj[k] for k in ('total_portsets','total_seed_port_combinations','moment_checks','failed_checks','margin_checks')}},indent=2))
