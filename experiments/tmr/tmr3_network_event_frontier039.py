#!/usr/bin/env python3
"""TMR-3/030: finite semantic charged-network serializer and exponent arithmetic controls.
Not an implementation of MCSP or a physical single-head Turing machine.
"""
import itertools, json, hashlib
from fractions import Fraction

checks=0
net_cases=0
serial_events=0
record_visits=0
unif_desc_bits=0
frontier_checks=0

def check(b,why):
    global checks
    checks += 1
    if not b: raise AssertionError(why)

def reference_parity(bits,p):
    # One input read and local XOR per observed bit; messages gathered at end.
    local=[0]*p
    for i,v in enumerate(bits): local[i%p]^=v
    return sum(local)%2

def serialize_parity(bits,p):
    # Explicitly charge virtual source bit reads, local work updates,
    # messages and root aggregation, with serialized record search.
    N=len(bits)
    procs=[{'id':a,'parity':0,'next':a} for a in range(p)]
    desc=f'N={N}|P={p}|round_robin|one_symbol_events'
    global net_cases, serial_events, record_visits,unif_desc_bits
    unif_desc_bits+=len(desc)*8
    tape=list(bits)+[0]*p+[0]*p
    events=0; visits=0
    while any(z['next']<N for z in procs):
        for z in procs:
            i=z['next']
            if i>=N:continue
            # simulated head seeks input coordinate and local cell, charging record scans
            visits+=i+1
            val=tape[i]
            visits+=N+z['id']+1
            tape[N+z['id']] ^=val
            z['next']+=p
            events+=1
    # Send p one-bit messages, then receive p one-bit messages into root.
    root=0
    for z in procs:
        visits+=N+z['id']+1
        msg=tape[N+z['id']]
        events+=1  # transmit
        visits+=N+p+z['id']+1
        tape[N+p+z['id']]=msg
        events+=1  # receive/aggregate
        visits+=N+p+z['id']+1
        root ^=tape[N+p+z['id']]
        events+=1  # root XOR
    M= N+2*p+len(desc)*8+20 # conservative representation accounting
    # Each separate virtual event costs O(M) with explicit local buffer/description.
    check(visits<=3*(events+1)*M,'charged scan upper bound')
    check(events==N+3*p,'event count')
    check(root==reference_parity(bits,p),'network semantic replay')
    net_cases+=1;serial_events+=events;record_visits+=visits
    return root

for N in range(1,8):
    for p in range(1,5):
        for bits in itertools.product((0,1),repeat=N):
            check(serialize_parity(bits,p)==(sum(bits)%2),'parity')
# Formal exponent frontier arithmetic. d >= 1 because source copy N.
# CHMY contradiction if c < 1.99 and e+max(d,e) < 1.99.
R=Fraction(199,100)
for d in [Fraction(1),Fraction(6,5),Fraction(3,2),Fraction(99,50),Fraction(2)]:
    for c in [Fraction(1),Fraction(19,10),Fraction(2)]:
        for ei in range(0,221):
            e=Fraction(ei,100)
            forbidden=(c<R and e+max(d,e)<R)
            if d>=R or c>=R:
                check(not forbidden,'overhead saturates LB')
            if d==1 and c<R:
                check(forbidden == (e<Fraction(99,100)),'d=1 exact frontier')
            if d<R and c<R and e<=d:
                check(forbidden == (e<R-d),'general branch frontier')
            frontier_checks+=1
# under B,p=O(N), C=O(N), E=N^(0.98), serial time N^1.98 polylog = o(N^1.99).
check(Fraction(98,100)+max(Fraction(1),Fraction(98,100))<R,'positive transfer')
check(Fraction(99,100)+max(Fraction(1),Fraction(99,100))==R,'endpoint not excluded')
check(Fraction(3,5)+max(Fraction(3,2),Fraction(3,5))>R,'large descriptions escape')
result={
 'label':'TMR3_MCSP_HIGH_THRESHOLD_NETWORK_FRONTIER039',
 'status':'COMPUTATIONAL semantic tape-record proxy plus exact rational exponent controls; not a finite-state physical TM or a lower-bound experiment',
 'assertions_passed':checks,'failed':0,'exhaustive_parity_network_cases':net_cases,
 'charged_local_interface_events':serial_events,'charged_record_visits':record_visits,
 'constructor_description_bits_accounted':unif_desc_bits,
 'exact_fraction_exponent_cases':frontier_checks,
 'derived_conditional_contradiction':'if C=O(N), B,p=O(N), E=O(N^(0.99-eps)) then serialized one-way one-work-tape algorithm is O(N^(1.99-eps) polylog N), contradicting CHMY Theorem 2 for its high-mu MCSP',
 'does_not_prove':'P!=NP, low-mu CHMY antecedent, true machine-event asymptotic LB from finite tests'
}
print(json.dumps(result,indent=2))
