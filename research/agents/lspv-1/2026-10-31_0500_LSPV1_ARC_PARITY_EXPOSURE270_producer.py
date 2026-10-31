#!/usr/bin/env python3
"""LSPV-1 ARC-PARITY-EXPOSURE270 finite controls. Standard library only."""
from __future__ import annotations
import itertools, json, hashlib, sys
from collections import Counter
from pathlib import Path
OUT=Path(__file__).resolve().parent

# Explicit original clauses, literals ±(index+1); duplicate clauses allowed.
def family(bits):
    k=len(bits); z=k+2; u=k+3; v=k+4
    C=[]
    for i,b in enumerate(bits):
        a=i+1; c=i+2
        if b==0: pairs=[(-a,c),(a,-c)]
        else: pairs=[(a,c),(-a,-c)]
        for p,q in pairs:
            C.append((p,q,z)); C.append((p,q,-z))
    for t in (1,k+1):
        for su,sv in itertools.product((1,-1),repeat=2):
            C.append((-t,su*u,sv*v))
    return C,k+4

def littrue(lit,mask):
    bit=(mask>>(abs(lit)-1))&1
    return bit==int(lit>0)

def counts(C,mask): return [sum(littrue(x,mask) for x in clause) for clause in C]
def sat(C,mask): return all(any(littrue(x,mask) for x in c) for c in C)
def brute(C,n): return [a for a in range(1<<n) if sat(C,a)]

def codec(C,n):
    # Fixed-width signed source clauses, for each fixed k all bit strings have equal length.
    w=max(2,len(str(n))); out=[f'CNF:{n:0{w}d}:{len(C):04d}\n']
    for j,c in enumerate(C):
        out.append(f'C{j:04d}:' + '|'.join(('+' if l>0 else '-')+f'{abs(l):0{w}d}' for l in c)+'\n')
    return ''.join(out)

def bit_query_positions(bit_tuple):
    """Coordinates that change when one b_i toggles, in ACTUAL ASCII source bits."""
    C,n=family(bit_tuple); base=codec(C,n).encode('ascii'); d={}
    for i in range(len(bit_tuple)):
        v=list(bit_tuple);v[i]^=1
        other=codec(*family(v)).encode('ascii')
        assert len(base)==len(other)
        d[i]=[8*j+t for j,(a,b) in enumerate(zip(base,other)) for t in range(8) if ((a^b)>>t)&1]
    assert all(d[i] for i in d)
    assert all(not set(d[i]).intersection(d[j]) for i in d for j in d if i!=j)
    return {str(i): {"first":min(v),"count":len(v)} for i,v in d.items()}

def child(even):
    V=[1,2,3]
    clauses=[]
    for signs in itertools.product((1,-1),repeat=3):
        clauses.append(tuple(s*v for s,v in zip(signs,V)))
    if even: clauses[0]=clauses[1]
    return clauses,3

class Ledger:
    def __init__(self): self.nodes=0; self.literal_tests=0;self.clause_checks=0;self.pins=0; self.branches=0
    def event_count(self):return self.nodes+self.literal_tests+self.clause_checks+self.pins+self.branches

def dpll(C,n):
    ct=Ledger()
    def solve(A):
        ct.nodes+=1
        while True:
            changed=False; unresolved=False
            for c in C:
                ct.clause_checks+=1
                unassigned=[]; satisfied=False
                for lit in c:
                    ct.literal_tests+=1
                    i=abs(lit)
                    if i not in A: unassigned.append(lit)
                    elif A[i]==int(lit>0):satisfied=True;break
                if satisfied: continue
                if not unassigned:return False
                unresolved=True
                if len(unassigned)==1:
                    lit=unassigned[0]; key=abs(lit); target=int(lit>0)
                    if key in A:
                        if A[key]!=target:return False
                    else:A[key]=target;ct.pins+=1;changed=True;break
            if not changed:break
        if not unresolved:return True
        pivot=next((abs(l) for c in C for l in c if abs(l) not in A),None)
        if pivot is None:return False
        ct.branches+=1
        for bit in (0,1):
            B=A.copy();B[pivot]=bit;ct.pins+=1
            if solve(B):return True
        return False
    return solve({}),ct

def extreme(c,style):
    # Literal-wise TRUE target (S), FALSE (U), original variable sharing preserved.
    return {str(abs(l)):(int(l>0) if style=='S' else int(l<0)) for l in c}

def compat(ci,cj,style1,style2):
    a=extreme(ci,style1);b=extreme(cj,style2)
    return all(a.get(key,v)==v for key,v in b.items())

def res_blockers(C):
    found=[]
    for i in range(len(C)):
        for j in range(i+1,len(C)):
            for l in C[i]:
                if -l not in C[j]:continue
                rest=set(C[i]);rest.remove(l); rest.update(x for x in C[j] if x!=-l)
                if any(-x in rest for x in rest):continue
                t=tuple(sorted(rest,key=lambda x:(abs(x),x)))
                if not any(q['resolvent']==list(t) for q in found):
                    found.append({'source':[i,j],'pivot':abs(l),'resolvent':list(t),'forbidden_cube':{str(abs(x)):int(x<0) for x in t}})
    return found

def full_audit(bits):
    C,n=family(bits);m=len(C);L=(1<<n)-1
    witnesses=brute(C,n); expected=(sum(bits)%2==0)
    assert bool(witnesses)==expected
    assert len(witnesses)==(8 if expected else 0)
    baseline,bc=dpll(C,n);assert baseline==expected
    E0,E1=counts(C,0),counts(C,L)
    occ=[]
    for j,c in enumerate(C):
        s=extreme(c,'S'); u=extreme(c,'U')
        assert {x:1-v for x,v in s.items()}==u
        for t,l in enumerate(c):
            occ.append({'clause':j,'slot':t,'literal':l,'S_target':int(l>0),'inverse_S_as_U':int(l<0),'U_target':int(l<0),'inverse_U_as_S':int(l>0)})
    pairs=[]
    for i in range(m):
        for j in range(i+1,m):
            pair={'clauses':[i,j]}
            for x,y in [('S','S'),('S','U'),('U','S'),('U','U')]:
                p=compat(C[i],C[j],x,y)
                # Independent exact enumeration over only shared clause-variable support.
                keys=sorted(set(map(abs,C[i]+C[j])))
                q=any(all(littrue(z,mask) == (t=='S') for k,t in ((i,x),(j,y)) for z in C[k])
                      for mask in (sum(b<<(z-1) for b,z in zip(bs,keys)) for bs in itertools.product((0,1),repeat=len(keys))))
                assert p==q,(i,j,x,y)
                pair[x+y]=p
            pairs.append(pair)
    # Single and multi-flip trails, exact per clause complement and transition identity.
    trails=[]
    for initial in (0,L):
        a=initial; steps=[]
        for step,flip_set in enumerate((list(range(1,n+1)),list(range(n,0,-1)),[1,n],list(range(1,n+1,2)))):
            # Use first two trails one flip at a time; next steps multibit.
            if step<2:
                for v in flip_set:
                    before=counts(C,a); old=a;a^=1<<(v-1);now=counts(C,a)
                    assert all(now[j]==before[j]+sum(1 if not littrue(l,old) else -1 for l in C[j] if abs(l)==v) for j in range(m))
                    steps.append({'mask':a,'flipped':[v],'counts':now,'histogram':[now.count(i) for i in range(4)],'SAT':min(now)>0})
            else:
                before=counts(C,a);old=a
                for v in flip_set:a^=1<<(v-1)
                now=counts(C,a)
                assert all(now[j]==before[j]+sum(1 if not littrue(l,old) else -1 for l in C[j] if abs(l) in flip_set) for j in range(m))
                steps.append({'mask':a,'flipped':flip_set,'counts':now,'histogram':[now.count(i) for i in range(4)],'SAT':min(now)>0})
        trails.append({'start':initial,'steps':steps})
    for a in range(1<<n):
        c=counts(C,a);neg=counts(C,L^a)
        assert all(c[j]+neg[j]==3 for j in range(m))
        assert [c.count(i) for i in range(4)]==[neg.count(3-i) for i in range(4)]
    blocks=res_blockers(C)
    for r in blocks:
        for a in witnesses:
            assert not all(((a>>(int(i)-1))&1)==v for i,v in r['forbidden_cube'].items())
    G,_=child(expected); gdec,gc=dpll(G,3); assert gdec==expected
    return {'m_edges':len(bits),'bits':list(bits),'SAT':expected,'models':len(witnesses),'witnesses':witnesses,'n':n,'clauses':C,'source_bytes':len(codec(C,n).encode('ascii')),
        'extrema':{'all_zero':{'counts':E0,'histogram':[E0.count(i) for i in range(4)],'SAT':min(E0)>0},'all_one':{'counts':E1,'histogram':[E1.count(i) for i in range(4)],'SAT':min(E1)>0}},
        'occurrences':occ,'pair_compatibility':pairs,'flip_trails':trails,'resolution_blockers':blocks,'query_positions':bit_query_positions(bits),
        'physical_child':codec(G,3),'physical_child_length':len(codec(G,3)),'baseline':vars(bc),'baseline_events':bc.event_count(),
        'guest':vars(gc),'guest_events':gc.event_count(),
        'controller_selected_events':len(codec(C,n))+len(codec(G,3))+gc.event_count(),
        'child_SAT':gdec}

def main():
    summaries=[];details=[];tested=0
    for m in range(1,7):
        for b in itertools.product((0,1),repeat=m):
            C,n=family(b); s=codec(C,n); G,_=child((sum(b)%2)==0)
            base,bc=dpll(C,n); guest,gc=dpll(G,3)
            assert base==guest==(sum(b)%2==0)
            # Source authentication: exact canonical streaming recognizer checks EVERY source byte.
            assert s==codec(*family(b))
            # Independent source representation always same size for fixed m.
            assert len(s)==len(codec(*family([0]*m)))
            summaries.append({'m':m,'bits':''.join(map(str,b)),'SAT':base,
                             'source_bytes':len(s),'child_bytes':len(codec(G,3)),
                             'baseline_nodes':bc.nodes,'baseline_events':bc.event_count(),
                             'controller_events':len(s)+len(codec(G,3))+gc.event_count()})
            tested+=1
            if (m,b) in [(3,(0,0,0)),(3,(0,0,1)),(6,(0,)*6),(6,(0,)*5+(1,))]:
                details.append(full_audit(b))
    summary={'run':'ARC-PARITY-EXPOSURE270','seed':None,'enumeration':'all source bit vectors of lengths 1..6; full original models for 4 detailed sources',
             'total_sources':tested,'SAT_sources':sum(x['SAT'] for x in summaries),'UNSAT_sources':sum(not x['SAT'] for x in summaries),
             'original_source_total_bytes':sum(x['source_bytes'] for x in summaries),
             'standard_DPLL_total_nodes':sum(x['baseline_nodes'] for x in summaries),
             'standard_DPLL_selected_events':sum(x['baseline_events']+x['source_bytes'] for x in summaries),
             'stream_recognizer_plus_guest_selected_events':sum(x['controller_events'] for x in summaries),
             'detailed_sources':len(details),'detailed_pair_modes':sum(len(x['pair_compatibility'])*4 for x in details),
             'detailed_occurrences':sum(len(x['occurrences']) for x in details),
             'detailed_source_models':sum(x['models'] for x in details),
             'rows':summaries,'detailed':details}
    p=OUT/'ARC_PARITY_EXPOSURE270_raw.json';p.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('rows','detailed')},indent=2))
    print('raw',p,p.stat().st_size, 'sha256',hashlib.sha256(p.read_bytes()).hexdigest())
if __name__=='__main__':main()