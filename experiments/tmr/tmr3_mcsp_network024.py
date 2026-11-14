#!/usr/bin/env python3
"""TMR-3/024: independent uniform network versus swept single-tape proxy.

Finite tests only. The swept simulation charges each adjacent sweep displacement,
node update, message delivery, and one-way source read; Python's indexing and
arrays are not themselves a native finite-alphabet Turing machine.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from hashlib import sha256
import json, math, random, sys
from pathlib import Path

@dataclass
class Unit:
    acc: int = 0
    head: int = 0
    cells: dict = None
    def __post_init__(self):
        if self.cells is None: self.cells={}


def step_network(units, links, bit):
    p=len(units)
    incoming=[0]+links
    next_links=[]
    for i,u in enumerate(units):
        u.acc = (u.acc | (bit if i==0 else incoming[i]))
        old=u.cells.get(u.head,0)
        new=old ^ u.acc ^ (i&1)
        if new: u.cells[u.head]=new
        elif u.head in u.cells: del u.cells[u.head]
        u.head += (1 if new else -1)
        if i<p-1: next_links.append(u.acc)
    return next_links


def direct_network(p, source):
    assert p>=1
    if any(b not in '01' for b in source):return {'valid':False,'answer':False}
    us=[Unit() for _ in range(p)]
    links=[0]*(p-1)
    rounds=len(source)+p-1
    cost={'input_reads':0,'updates':0,'messages':0,'rounds':rounds}
    for t in range(rounds):
        bit=int(source[t]) if t<len(source) else 0
        if t<len(source):cost['input_reads']+=1
        links=step_network(us,links,bit)
        cost['updates']+=p
        cost['messages']+=(p-1)
    return {'valid':True,'answer':bool(us[-1].acc),'cost':cost,
            'heads':[u.head for u in us],
            'states':[u.acc for u in us],
            'cells':[sorted(u.cells.items()) for u in us]}


def swept_proxy(p, source):
    if any(b not in '01' for b in source):return {'valid':False,'answer':False}
    heads=[0]*p
    acc=[0]*p
    # At each physical coordinate, one cell stores a fixed-p track vector.
    track={}  # coordinate -> immutable p-tuple of bits
    links=[0]*(p-1)
    cursor=0
    physical=0
    charge={'oneway_source_reads':0,'adjacent_head_moves':0,
            'swept_cell_reads':0,'local_track_writes':0,
            'finite_control_updates':0,'message_deliveries':0}
    rounds=len(source)+p-1
    for t in range(rounds):
        bit=int(source[t]) if t<len(source) else 0
        if t<len(source):charge['oneway_source_reads']+=1
        incoming=[0]+links
        out=[]
        # Precompute OLD positions. Treat the one-tape head as starting at 0.
        low=min(0,*heads)-1
        high=max(0,*heads)+1
        old_heads=heads.copy()
        # Reposition to left end, with physically adjacent moves.
        for coordinate in range(-1,low-1,-1):
            assert abs(coordinate-physical)==1
            physical=coordinate
            charge['adjacent_head_moves']+=1
        # Single left-to-right update sweep: no head is updated twice,
        # even if its new position occurs later in the sweep.
        for coordinate in range(low,high+1):
            if coordinate!=physical:
                assert abs(coordinate-physical)==1
                physical=coordinate
                charge['adjacent_head_moves']+=1
            val=list(track.get(coordinate,(0,)*p))
            charge['swept_cell_reads']+=1
            touched=False
            for i in range(p):
                if old_heads[i] == coordinate:
                    acc[i] |= bit if i==0 else incoming[i]
                    new=val[i]^acc[i]^(i&1)
                    val[i]=new
                    heads[i]+=(1 if new else -1)
                    charge['finite_control_updates']+=1
                    charge['local_track_writes']+=1
                    touched=True
            if touched:
                if any(val):track[coordinate]=tuple(val)
                else:track.pop(coordinate,None)
        # Return to the origin to make next-round source consumption simple.
        for coordinate in range(high-1,-1,-1):
            assert abs(coordinate-physical)==1
            physical=coordinate
            charge['adjacent_head_moves']+=1
        assert physical==0
        # Update messages simultaneously, after every node was processed.
        links=acc[:-1].copy()
        charge['message_deliveries']+=p-1
    cells=[sorted((x,v[i]) for x,v in track.items() if v[i]) for i in range(p)]
    return {'valid':True,'answer':bool(acc[-1]),'heads':heads,'states':acc,
            'cells':cells,'charge':charge,'rounds':rounds}


def run():
    cases=0;both={"yes":0,"no":0,"malformed":0};upper_checks=0
    max_sweep=0;total_movements=0
    for p in (1,2,3,4):
        for length in range(0,9):
            for bits in product('01',repeat=length):
                s=''.join(bits)
                direct=direct_network(p,s);swept=swept_proxy(p,s)
                assert direct['valid'] and swept['valid']
                assert direct['answer']==swept['answer']==('1' in s)
                for key in ('heads','states','cells'):
                    assert direct[key]==swept[key],(key,p,s,direct[key],swept[key])
                rounds=length+p-1
                # The swept head visits only coordinates within [-R,R], plus
                # one-cell guard. It returns to origin at every round.
                # Bound each round by <=4(R+1) + O(1) moves.
                assert swept['charge']['adjacent_head_moves']<=4*rounds*(rounds+2)
                upper_checks+=1
                max_sweep=max(max_sweep,swept['charge']['adjacent_head_moves'])
                total_movements+=swept['charge']['adjacent_head_moves']
                both['yes' if direct['answer'] else 'no']+=1
                cases+=1
        for malformed in ('2','0?1','1 0','x','01z'):
            assert not direct_network(p,malformed)['valid']
            assert not swept_proxy(p,malformed)['valid']
            both['malformed']+=1
    # Exact exponent firewall for a quadratic fixed-p simulator:
    # If T_sim <= const*R^2, CHMY N^1.99 lower => R >= N^.995.
    exponents=[{'N_power':n,'log2_N':n,'lower_round_log2_N':str(Fraction(199,200)*n),
                'linear_source_log2_N':n,'gap_from_linear_log2':str(Fraction(n,200))}
               for n in (10,20,40,100,200)]
    payload={'run':'TMR3_MCSP_NETWORK024','status':'COMPUTATIONAL',
             'native_tm_implementation':False,
             'n_tape_realization':'one-way source plus fixed p one-work-tape machines; delayed fixed-FIFO links',
             'tested_processors':[1,2,3,4], 'tested_lengths':list(range(9)),
             'source_cases':cases,'cases_by_label':both,
             'matching_full_configuration_checks':cases,
             'sweep_quadratic_ceiling_checks':upper_checks,
             'max_adjacent_sweep_moves':max_sweep,
             'total_adjacent_sweep_moves':total_movements,
             'asymptotic_exponent_controls':exponents,
             'all_assertions_passed':True}
    p=Path(__file__)
    payload['code_sha256']=sha256(p.read_bytes()).hexdigest()
    out=p.with_suffix('.json')
    out.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps(payload,indent=2))

if __name__=='__main__':run()
