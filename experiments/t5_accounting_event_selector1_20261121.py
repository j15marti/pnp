"""Actual finite tape-phase trace + strict-C source controls; no lower-bound benchmark."""
from itertools import product
import json

ALLOWED={frozenset((i,(i+1)%5,(i+2)%5)) for i in range(5)}
def C(a,b,c):return len({a,b,c})==3 and frozenset((a,b,c)) in ALLOWED
def gamma(k):
    s=bin(k)[2:];return '0'*(len(s)-1)+s

def source(h,u):
    m=1<<h
    bits=format(u,f'0{h}b')
    cs=[(1,0,2) if b=='1' else (0,1,2) for b in bits]+[(0,1,2)]*(m-h)
    wire='1110'+gamma(m+1)+''.join(format(x+1,'02b') for t in cs for x in t)
    assert len(wire)==6*m+2*h+5
    return cs,wire

def phase(u,origin):
    # Prepared unary extent is charged to the wrapper, not free advice.
    # Fixed states/alphabet; no clock input influences transitions.
    tape={origin+u+1:'E'}
    head=origin;state='START';time=0;events=[];trace=[]
    while state!='DONE':
        symbol=tape.get(head,'.');label=None
        if state=='START':
            tape[head]='S';state='RIGHT';label=0
        elif state=='RIGHT':
            if symbol=='E':head-=1;state='BACK'
            else:head+=1
        elif state=='BACK':
            if symbol=='S':tape[head]='F';state='DONE';label=1
            else:head-=1
        time+=1
        trace.append((time,head,state))
        if label is not None:events.append((time,label))
    return events,trace

def main():
    rows=[];raw=[];total=0
    for h in range(1,7):
        m=1<<h;records=set();payloads=set();wires=set()
        for u in range(m):
            cs,wire=source(h,u);N=len(wire);wires.add(wire)
            z=sum(all(C(*(a[x] for x in t)) for t in cs) for a in product(range(5),repeat=3))
            assert z==30
            events,trace=phase(u,0)
            relocated,rt=phase(u,2*N)
            assert events==relocated
            assert all(t==s and h2-h1==2*N and q==r for (t,h1,q),(s,h2,r) in zip(trace,rt))
            indices=tuple(t for t,_ in events);payload=tuple(l for _,l in events)
            gap=indices[1]-indices[0]
            decoded=(gap-3)//2
            assert indices==(1,2*u+4) and gap%2==1 and decoded==u
            assert len(trace)==2*u+4 and payload==(0,1)
            records.add(indices);payloads.add(payload)
            raw.append({'h':h,'u':u,'N':N,'event_indices':indices,'payload':payload,
                        'decoded_u':decoded,'phase_steps':len(trace),'count':z})
            total+=1
        assert len(records)==len(wires)==m and len(payloads)==1
        rows.append({'h':h,'m':m,'N':6*m+2*h+5,'inputs':m,
                     'conditional_U_entropy_bits':h,'selector_entropy_bits':h,
                     'payload_entropy_bits':0,'selected_events':2,'payload_capacity_bits_per_event':1,
                     'payload_only_bound':2,'payload_only_violated':h>2,
                     'max_phase_steps':2*m+2,'reuse_factor':1})
    print(json.dumps({'status':'PASS','scope':'finite trace and coding checks, not compulsory hardness',
                      'source_cases':total,'assignment_evaluations':125*total,
                      'rows':rows,'raw_records':raw,'seed':None},indent=2))
if __name__=='__main__':main()
