#!/usr/bin/env python3
"""Independent exact-rational verification of a POST-UPDATE exponent-loss envelope.
Not an implementation of an FLMV machine or a SAT general-purpose decider.
"""
import json, time
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path

OUT = Path(__file__).resolve().parent
checks = 0

def ck(cond, msg):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(msg)


def beta(c):
    return ((c + 2) / (c*c) - c)/2

def critical_gap(e):
    c = Q(6,5) + 2*e
    return beta(c) - (Q(1,2)+e)

def poly(e):
    return 1000*e**3 + 1750*e**2 + 895*e - 2

def closed_form(e):
    return -poly(e)/(20*(5*e+3)**2)

def step(t,s,e):
    return max(Q(11,10), Q(3,5)+t/2)+e, max(Q(1,2),s/2)+e

def k4_packet_authentication(clauses, allowed_supports):
    """Independent packet-integrity control for the fixed K4 support layout.
    This is not the full general signed Tseitin recognizer of LSPV-2/442.
    """
    groups={}
    for cl in clauses:
        if len(cl)!=3 or any(not isinstance(x,int) or x==0 for x in cl): return False
        support=tuple(sorted(map(abs,cl)))
        if len(set(support))!=3 or support not in allowed_supports:return False
        groups.setdefault(support,[]).append(cl)
    if set(groups)!=allowed_supports:return False
    for support,cs in groups.items():
        if len(cs)!=4:return False
        forbidden=[]
        for cl in cs:
            d={abs(x):int(x<0) for x in cl}
            if len(d)!=3:return False
            forbidden.append(tuple(d[x] for x in support))
        if len(set(forbidden))!=4 or len({sum(a)%2 for a in forbidden})!=1:return False
    return True

def enumerate_K4():
    edges=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    inc={v:tuple(i for i,(a,b) in enumerate(edges) if a==v or b==v) for v in range(4)}
    total=0; sat_count=0; unsat_count=0; hostile=0
    allowed_supports={tuple(sorted(i+1 for i in inc[v])) for v in range(4)}
    for charges in range(16):
        clauses=[]
        for v in range(4):
            chi=(charges>>v)&1
            for a in range(8):
                if a.bit_count()%2==chi:
                    continue
                clauses.append(tuple((e+1) * (-1 if (a>>j)&1 else 1) for j,e in enumerate(inc[v])))
        ck(len(clauses)==16, 'original packet clause count')
        ck(all(len(cl)==3 and len(set(map(abs,cl)))==3 for cl in clauses),'proper ternary')
        ck(len(set(clauses))==16,'source duplicates')
        ck(k4_packet_authentication(clauses,allowed_supports),'K4 source facet authentication')
        if charges==0:
            mutations=[]
            mutations.append(clauses[:-1])
            mutations.append(clauses[:-1]+[clauses[0]])
            mutants=list(clauses); mutants[0]=tuple(-x if j==0 else x for j,x in enumerate(mutants[0])); mutations.append(mutants)
            mutants=list(clauses); mutants[0]=(999,)+mutants[0][1:];mutations.append(mutants)
            mutants=list(clauses);mutants[0]=mutants[0][:2];mutations.append(mutants)
            mutants=list(clauses);mutants[0]=(0,)+mutants[0][1:];mutations.append(mutants)
            for mut in mutations:
                ck(not k4_packet_authentication(mut,allowed_supports),'hostile original source accepted')
                hostile+=1
        satisfying=0
        for assign in range(64):
            orig=all(any((bool((assign>>(abs(l)-1))&1) == (l>0)) for l in clause) for clause in clauses)
            eqs=all(((sum((assign>>i)&1 for i in inc[v])&1) == ((charges>>v)&1)) for v in range(4))
            ck(orig==eqs,'original signed CNF vs parity mismatch')
            satisfying+=bool(orig)
        ck(satisfying==(8 if charges.bit_count()%2==0 else 0), 'charge parity classification')
        if satisfying: sat_count+=1
        else: unsat_count+=1
        total+=1
    ck((sat_count,unsat_count)==(8,8),'signed control labels')
    return {'family':'K4 original signed 3CNF 4 packets 16 clauses, 6 edge variables', 'charges':total,'SAT':sat_count,'UNSAT':unsat_count,'clause_assignment_evaluations':1024,'hostile_source_mutations_rejected':hostile}

def main():
    start=time.monotonic()
    l,h=Q(0),Q(1,100)
    ck(poly(l)<0 and poly(h)>0,'root bracket')
    for _ in range(90):
        m=(l+h)/2
        if poly(m)<0:l=m
        else:h=m
    ck(h-l < Q(1,10**25),'root precision')
    critical_decimal=(float(l)+float(h))/2
    ck(Q(2224,1000000)<l<h<Q(2225,1000000),'root rational bounding interval')
    eps=[Q(0),Q(1,10000),Q(1,1000),Q(1,500),Q(1,450),Q(1,400)]
    for e in eps:
        ck(critical_gap(e)==closed_form(e),'closed form rational identity')
        c,s=Q(6,5)+2*e,Q(1,2)+e
        ck(step(c,s,e)==(c,s),'fixed point')
        ck((critical_gap(e)>0)==(e<l),'threshold sign')
    L=Q(433,216)
    entries=[]; samples=0; first_entry_depths=[]; bound_validations=0
    for e in eps:
        gp=critical_gap(e)
        for a in range(1,16):
            for b in range(0,12):
                # include fractions on either side of both fixed points
                t0=Q(a,2)+Q(13,10)
                s0=Q(b,3)
                c=Q(6,5)+2*e
                sf=Q(1,2)+e
                A=L*max(Q(0),t0-c)+max(Q(0),s0-sf)
                t,s=t0,s0
                first=None
                for j in range(0,65):
                    gap=beta(t)-s
                    lower=gp - Q(1,2**j)*A
                    ck(gap>=lower,'mean value finite-depth lower bound')
                    ck(abs(t-c)<=Q(1,2**j)*abs(t0-c),'time Lipschitz')
                    ck(abs(s-sf)<=Q(1,2**j)*abs(s0-sf),'space Lipschitz')
                    bound_validations+=3
                    if gap>0 and first is None:first=j
                    t,s=step(t,s,e)
                if gp>0:
                    ck(first is not None, 'failure to enter strict FLMV region')
                    first_entry_depths.append(first)
                samples+=1
        entries.append({'epsilon':str(e),'fixed_t':str(Q(6,5)+2*e),'fixed_s':str(Q(1,2)+e),'gap':str(gp),'gap_decimal':float(gp),'positive':gp>0})
    # Beyond the threshold the upper-envelope trajectory from above never enters.
    e=Q(1,400)
    t=Q(40);s=Q(23);c=Q(6,5)+2*e; sf=Q(1,2)+e
    for j in range(100):
        ck(t>=c and s>=sf and beta(t)-s<=critical_gap(e)<0,'negative envelope above fixed point')
        t,s=step(t,s,e)
    result={
        'run':'LSPV-2/486 post-step exponent loss',
        'status':'PROVED/RESTRICTED exact arithmetic; COMPUTATIONAL controls; P vs NP OPEN',
        'critical_root_interval_rational':[str(l),str(h)],
        'critical_root_approx':critical_decimal,
        'distinct_from_LSPV4_482':'post-update additive loss, not common four physical channel tariff',
        'polynomial':'1000 e^3 + 1750 e^2 + 895 e - 2',
        'formula':'G(e)= -(1000e^3+1750e^2+895e-2)/(20(5e+3)^2)',
        'sample_initial_pairs_per_epsilon':180,
        'total_envelope_pairs':samples,
        'exact_rational_inequality_validations':bound_validations,
        'largest_first_strict_entry_depth':max(first_entry_depths),
        'epsilon_cases':entries,
        'original_source_controls':enumerate_K4(),
        'assertions':None,
        'elapsed_seconds':None,
        'native_FLMV_executed':False,
        'historical_Rmix341_checker_executed':False,
    }
    result['assertions']=checks
    result['elapsed_seconds']=round(time.monotonic()-start,4)
    out=OUT/'2026-11-07_LSPV2_486_POSTSTEP_SLACK_RAW.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'assertions':checks,'root':critical_decimal,'largest_depth':max(first_entry_depths),'cases':samples,'gap':[v['gap_decimal'] for v in entries], 'seconds':result['elapsed_seconds']},indent=2))

if __name__=='__main__':main()
