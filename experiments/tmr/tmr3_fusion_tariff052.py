#!/usr/bin/env python3
"""TMR-3 FUSTAR052. Finite, independently replayable *restricted* multitape
source-fanout tariff laboratory. NOT a full SAT decider or proof system.
Physical steps are charged one transition, including simultaneous tape actions.
"""
from dataclasses import dataclass, replace
from fractions import Fraction as Q
import json
import random

@dataclass(frozen=True)
class C:
    x: int=0       # authenticated read-only source bit, head parked at cell 0
    subs: int=0    # length of unary subscriber-token tape, head at its end
    ready: bool=False # one cache symbol: unready/ready0/ready1
    value: int=0   # only meaningful if ready
    msg: tuple=()  # physical message tape: 1=unconsumed, 0=consumed
    head: int=0    # message tape head

def p(c):
    return (c.subs if not c.ready else 0,
            int(c.subs>0 and not c.ready),
            sum(c.msg))

def moves(c):
    out={}
    out['SUBSCRIBE'] = replace(c,subs=c.subs+1)
    if c.head==len(c.msg):
        out['PUSH'] = replace(c,msg=c.msg+(1,),head=c.head+1)
    if c.head>0:
        out['REWIND'] = replace(c,head=c.head-1)
    if c.head<len(c.msg) and c.msg[c.head]==0:
        out['ADVANCE'] = replace(c,head=c.head+1)
    if not c.ready:
        out['FILL'] = replace(c,ready=True,value=c.x)
    if c.head<len(c.msg) and c.msg[c.head]==1:
        msg=list(c.msg);msg[c.head]=0
        out['POP'] = replace(c,msg=tuple(msg),head=c.head+1)
        if not c.ready:
            out['FILL_POP'] = replace(c,msg=tuple(msg),head=c.head+1,
                                      ready=True,value=c.x)
    return out

def delta(before,after):
    return tuple(a-b for a,b in zip(p(before),p(after)))

def tariff_ok(weights,before,after):
    return sum((w*d for w,d in zip(weights,delta(before,after))),Q(0))<=1

def build(m,q,x):
    c=C(x=x)
    for _ in range(m):c=moves(c)['SUBSCRIBE']
    for _ in range(q):c=moves(c)['PUSH']
    for _ in range(q):c=moves(c)['REWIND']
    assert p(c)==(m,int(m>0),q)
    return c

def main():
    checks=0;states=0;edges=0;counts={}
    good=((Q(0),Q(3,5),Q(2,5)),(Q(0),Q(1,2),Q(1,2)),(Q(0),Q(0),Q(1)))
    failed=[]
    for x in (0,1):
        for m in range(0,18):
            for q in range(0,12):
                c=build(m,q,x); states+=1
                # Test every available real paid transition from each reachable state
                for rule,s in moves(c).items():
                    ds=delta(c,s)
                    for w in good:
                        assert tariff_ok(w,c,s),(w,rule,m,q,x,ds)
                        checks+=1
                    if rule=='FILL_POP' and m:
                        assert ds==(m,1,1)
                        assert moves(moves(c)['FILL'])['POP']==s
                        checks+=2
                    counts[rule]=counts.get(rule,0)+1;edges+=1
                # Also test write-stream states before the rewind: PUSH available
                c2=C(x=x,subs=m,ready=False,msg=(1,)*q,head=q)
                for rule,s in moves(c2).items():
                    for w in good:
                        assert tariff_ok(w,c2,s)
                        checks+=1
                    counts[rule]=counts.get(rule,0)+1;edges+=1
    # Deterministic random walks cover post-POP / READY / ADVANCE states, not only
    # pre-consumption seeds. Every event is re-evaluated against the tariff.
    rng=random.Random(202611141928)
    for run in range(180):
        c=C(x=run%2)
        for tick in range(90):
            legal=moves(c)
            legal={name:dst for name,dst in legal.items()
                   if not (name=='SUBSCRIBE' and c.subs>=20)
                   and not (name=='PUSH' and len(c.msg)>=16)}
            for name,dst in legal.items():
                for w in good:
                    assert tariff_ok(w,c,dst)
                    checks+=1
                counts[name]=counts.get(name,0)+1;edges+=1
            name=rng.choice(sorted(legal))
            c=legal[name]
        states+=1
    # Exact violating trace: 2 subscriptions, 1 queued message, single FILL_POP
    c=build(2,1,1); f=moves(c)['FILL_POP']
    assert delta(c,f)==(2,1,1)
    wrong=(Q(1,2),Q(1,2),Q(0))
    wrong2=(Q(0),Q(1),Q(1))
    assert not tariff_ok(wrong,c,f) and not tariff_ok(wrong2,c,f)
    checks+=3
    failed=[{'weights':list(map(str,w)), 'delta':[2,1,1], 'charge':1,
             'weighted_discharge':str(sum((a*b for a,b in zip(w,(2,1,1))),Q(0)))} for w in (wrong,wrong2)]
    # Nonzero subscriber weight fails for a sufficiently large physically reachable m.
    for den in (2,3,5,7,11,19,37,97):
        weight=Q(1,den);c=build(den+1,1,1);n=moves(c)['FILL_POP']
        assert weight*delta(c,n)[0]>1
        checks+=1
    # Exact rational endpoint arithmetic, separate from the physical tariff proof.
    cc=Q(241,200);beta=((cc+2)/(cc*cc)-cc)/2
    assert beta==Q(11642479,23232400) and beta>Q(1,2)
    checks+=2
    # A source-specific no-need-to-read trace: no subscriber, no message, goal already met.
    z=C(x=0)
    assert p(z)==(0,0,0)
    checks+=1
    return {'tag':'TMR3-FUSTAR052','status':'COMPUTATIONAL_FINITE_AUDIT',
            'checks':checks,'failed_assertions':0,'reachable_seed_states':states,
            'legal_paid_edges_checked':edges,'rule_counts':counts,
            'valid_rational_weights':[list(map(str,w)) for w in good],
            'counterexample':{'input_bit':1,'subscribers':2,'queued_bits':1,
                              'single_transition':'FILL_POP','delta':[2,1,1],
                              'bad_weights':failed},
            'asymptotic_dual_region':'lambda_occ=0, lambda_key>=0, lambda_msg>=0, lambda_key+lambda_msg<=1',
            'flmv_reference_c':'241/200','flmv_reference_beta':str(beta),
            'method':'exact rational state/edge evaluation; physical full-machine compilation unexecuted; no SAT computation'}

if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
