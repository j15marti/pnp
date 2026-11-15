#!/usr/bin/env python3
"""Independent TMR-5 audit of TMR-3 FUSTAR052, exact charged tapes.
Finite alphabet fixed-command interpreter, NOT a compiled SAT machine.
"""
from dataclasses import dataclass, replace
from fractions import Fraction as Q
import json

@dataclass(frozen=True)
class Tape:
    src: str = '0'             # immutable one-bit input, source head stationary
    subscribers: tuple = ()    # physical unary token cells, append-head at length
    cache: str = 'U'           # cache head stationary at symbol U,0,1
    messages: tuple = ()      # physically occupied message cells, 1 or 0; blank beyond
    h: int = 0                # message tape head

def vector(c):
    return (len(c.subscribers) if c.cache == 'U' else 0,
            int(c.cache == 'U' and bool(c.subscribers)),
            sum(c.messages))

def physical_step(c, opcode):
    """One command symbol on an authenticated read-only instruction tape.
    Each call charges one *simultaneous* multitape transition, including
    command-head movement and any 1-cell head reads/writes. Invalid guarded
    instructions are rejected rather than treated as legal moves.
    """
    if opcode == 'S':
        return replace(c, subscribers=c.subscribers + ('1',))
    if opcode == 'P' and c.h == len(c.messages):
        return replace(c, messages=c.messages + (1,), h=c.h + 1)
    if opcode == 'R' and c.h > 0:
        return replace(c, h=c.h - 1)
    if opcode == 'A' and c.h < len(c.messages) and c.messages[c.h] == 0:
        return replace(c, h=c.h + 1)
    if opcode == 'F' and c.cache == 'U':
        return replace(c, cache=c.src)
    if opcode in ('O', 'Z') and c.h < len(c.messages) and c.messages[c.h] == 1:
        arr = list(c.messages); arr[c.h] = 0
        if opcode == 'Z' and c.cache == 'U':
            return replace(c, messages=tuple(arr), h=c.h + 1, cache=c.src)
        if opcode == 'O':
            return replace(c, messages=tuple(arr), h=c.h + 1)
    raise ValueError('invalid opcode and guard: ' + opcode)

def feasible(w,c,d):
    return sum((a*(b-e) for a,b,e in zip(w,vector(c),vector(d))), Q(0)) <= 1

def setup(src,m,q):
    state=Tape(src)
    ticks=0
    for cmd in 'S'*m + 'P'*q + 'R'*q:
        state=physical_step(state,cmd); ticks+=1
    assert vector(state)==(m, int(m>0), q)
    assert state.h==0
    return state,ticks

def optimal_completion(c):
    q=sum(c.messages); m=int(c.cache=='U' and len(c.subscribers)>0)
    if q:
        commands=('Z' if m else 'O')+'O'*(q-1)
    elif m:
        commands='F'
    else:
        commands=''
    state=c
    for cmd in commands: state=physical_step(state,cmd)
    assert vector(state)==(0,0,0)
    return commands,state

def main():
    nchecks=0; nedges=0; best=[]; bad=[]
    good=(Q(0),Q(3,5),Q(2,5))
    badweights=((Q(1,2),Q(1,2),Q(0)),(Q(0),Q(1),Q(1)))
    rules='SPRAFOZ'
    for src in ('0','1'):
        for m in range(0,9):
            for q in range(0,7):
                c,setup_steps=setup(src,m,q)
                cmds,target=optimal_completion(c)
                expected=max(q,int(m>0))
                assert len(cmds)==expected
                assert setup_steps==m+2*q
                assert vector(target)==(0,0,0)
                # Every legal command is one charged physical transition.
                for op in rules:
                    try: d=physical_step(c,op)
                    except ValueError: continue
                    assert feasible(good,c,d),(src,m,q,op,vector(c),vector(d))
                    nchecks+=1; nedges+=1
                if m>0 and q>0:
                    d=physical_step(c,'Z')
                    assert tuple(a-b for a,b in zip(vector(c),vector(d)))==(m,1,1)
                    nchecks+=1
                    if m==2 and q==1:
                        for w in badweights:
                            assert not feasible(w,c,d)
                            bad.append({'weights':[str(a) for a in w],
                                        'weighted_drop':str(sum((a*b for a,b in zip(w,(2,1,1))),Q(0))),
                                        'charge':1,'source':src})
                            nchecks+=1
                best.append((m,q,expected))
    # Post-POP/ready, intervening queue, reused cached bit, and authentic guard checks.
    for src in ('0','1'):
        c,_=setup(src,2,3)
        c=physical_step(c,'F')
        for op in 'OOO':
            d=physical_step(c,op)
            assert feasible(good,c,d)
            c=d; nchecks+=1
        assert vector(c)==(0,0,0)
        try: physical_step(c,'Z')
        except ValueError: nchecks+=1
        else: raise AssertionError('unjustified zero-cost extra POP')
    # Analytic family: for each positive occurrence weight a, m >1/a is a violating witness.
    for denominator in (2,3,5,7,11,17,101,1009):
        c,_=setup('1',denominator+1,1)
        d=physical_step(c,'Z')
        assert Q(1,denominator)* (vector(c)[0]-vector(d)[0]) > 1
        nchecks+=1
    return {'tag':'TMR5-FUSTAR053-INDEPENDENT',
            'machine':'fixed finite-alphabet command-driven multitape event interpreter, not native TM compiler',
            'assertions':nchecks,'failures':0,'single_step_rows_checked':nedges,
            'distinct_initial_profiles_checked':len(best),'largest_subscriber_count':8,
            'largest_queue_length':6,'bad_weights':bad,
            'valid_weights':[str(a) for a in good],
            'initial_setup_cost':'m+2q charged transitions',
            'exact_optimal_remaining_cost':'max(q,1 if m>0 and cache unready else 0) for built profiles',
            'mathematical_proof':'q pending message symbols each require a separate erase, and m>0 unready cache needs fill; FILL_POP overlaps these two in one step',
            'scope':'restricted physical bit-cache laboratory only; SAT decision and same-system transfer OPEN'}

if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
