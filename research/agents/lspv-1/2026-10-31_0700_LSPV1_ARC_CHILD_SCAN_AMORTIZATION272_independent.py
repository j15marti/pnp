#!/usr/bin/env python3
"""Independent brute-force verifier of ARC_CHILD_SCAN_AMORTIZATION272 raw results.
No producer imports. Verifies both SAT and UNSAT sides, source pairing, child polarity,
source scan counts, all forbidden cubes and exact recurrence.
"""
import json, pathlib, itertools, hashlib
from fractions import Fraction

D=pathlib.Path(__file__).resolve().parent
R=json.loads((D/'arc_child_scan272_raw.json').read_text())
asserts=0

def check(v,why):
    global asserts
    asserts+=1
    if not v:raise AssertionError(why)

def counttrue(c,a):return sum(a[abs(z)-1]==(z>0) for z in c)

def satisfy(cs,a):return all(any(a[abs(z)-1]==(z>0) for z in c) for c in cs)

def brute(n,cs,rho=None):
    rho=rho or {}
    return any(all(a[k-1]==bool(v) for k,v in rho.items()) and satisfy(cs,a)
               for a in itertools.product((False,True),repeat=n))

def parse(s):
    lines=[l.split() for l in s.splitlines() if l and not l.startswith('c')]
    check(lines[0][0:2]==['p','cnf'],'bad dimacs header')
    n,m=map(int,lines[0][2:])
    clauses=[]
    for line in lines[1:]:
        vals=[int(t) for t in line]
        check(vals[-1]==0,'bad child terminator')
        clauses.append(vals[:-1])
    check(len(clauses)==m,'wrong number of clauses')
    return n,clauses

for r in R['originals']:
    n=r['formula']['variables'];cs=r['formula']['clauses']
    check(brute(n,cs)==r['ground_truth_sat'],'source label '+r['name'])
    check(len(r['per_clause'])==len(cs),'original clause count')
    for j,row in enumerate(r['per_clause']):
        check(row['source_index']==j+1 and row['clause']==cs[j],'source id')
        for z,p in zip(cs[j],row['occurrences']):
            check(p['literal']==z,'occ sign')
            check(p['S_local'] ==int(z>0) and p['U_local']==int(z<0),'local targets')
            check(p['inverted_S_local']==p['U_local'] and p['inverted_U_local']==p['S_local'],'local inversion')
    for pair in r['pair_compatibility']:
        i,j=[z-1 for z in pair['clause_indices']]
        for key,result in pair['SS_SU_US_UU'].items():
            observed=any(counttrue(cs[i],a)==(len(cs[i]) if key[0]=='S' else 0) and
                         counttrue(cs[j],a)==(len(cs[j]) if key[1]=='S' else 0)
                         for a in itertools.product((False,True),repeat=n))
            check(observed==result,'pair mismatch '+r['name'])
    for end,details in r['endpoints'].items():
        a=tuple(int(z) for z in end)
        check(details['counts']==[counttrue(c,a) for c in cs],'endpoint counts')
        check(details['sat']==satisfy(cs,a),'endpoint sat')
    for item in r['flip_trail']:
        a=tuple(int(z) for z in item['assignment'])
        check(item['status']['counts']==[counttrue(c,a) for c in cs],'flip counts')
    for item in r['resolvents_and_prohibited_cubes']:
        i,j=[z-1 for z in item['parents']]
        p=item['pivot']
        x=next(z for z in cs[i] if abs(z)==p)
        check(-x in cs[j],'source-res pivot')
        exp=set([z for z in cs[i] if z!=x]+[z for z in cs[j] if z!=-x])
        check(exp==set(item['resolvent']),'source-res outputs')
        check(not any(-z in exp for z in exp),'tautology source-res')
        cube={int(k):v for k,v in item['cube'].items()}
        check(all(cube[abs(z)]==int(z<0) for z in exp),'blocker assignment')
        check(not brute(n,cs,cube),'source blocker unsound')
    ctrl=r['cold_controller']
    check(ctrl['answer']==r['ground_truth_sat'],'controller label')
    check(ctrl['q']==len(ctrl['children']),'child count')
    check(ctrl['source_read_characters']==ctrl['q']*ctrl['source_characters'],'cold scan count')
    check(ctrl['child_write_characters']==sum(len(g['child_dimacs']) for g in ctrl['children']),'child output charge')
    check(ctrl['hypothetical_serial_peak_child_characters']==max(g['length'] for g in ctrl['children']),'serial peak child charge')
    check(ctrl['actual_audit_retained_child_characters']==ctrl['child_write_characters'],'retained audit data')
    for c in ctrl['children']:
        cube={int(k):v for k,v in c['cube'].items()}
        cn,child=parse(c['child_dimacs'])
        check(cn==n,'child vars')
        check(c['length']==len(c['child_dimacs']),'child length')
        check(c['answer']==brute(cn,child),'guest label')
        check(c['answer']==brute(n,cs,cube),'cofactor label')
        # independently verify FULL residual truth function for each extension, not only SAT bit
        for a in itertools.product((False,True),repeat=n):
            if all(a[k-1]==bool(v) for k,v in cube.items()):
                check(satisfy(cs,a)==satisfy(child,a),'cofactor pointwise')
    check(any(c['answer'] for c in ctrl['children'])==r['ground_truth_sat'],'OR join')

def rec(k):return max(Fraction(11,10),Fraction(3,5)+Fraction(1,2)*k)
for seq in R['exponent_audit']['first_collision_for_start']:
    k=Fraction(seq['initial_K'])
    for row in seq['levels']:
        check(Fraction(row['parent_K'])==k,'K parent')
        nk=rec(k)
        check(Fraction(row['recurrence_upper_Kprime'])==nk,'K next')
        check(row['strict_architecture_collision']==(nk<Fraction(8,5)),'K collision')
        k=nk
    check(k<Fraction(8,5),'missing collision')

check(sum(r['ground_truth_sat'] for r in R['originals'])==R['sat_sources'],'sat counts')
check(sum(not r['ground_truth_sat'] for r in R['originals'])==R['unsat_sources'],'unsat counts')
check(sum(r['baseline']['nodes'] for r in R['originals'])==R['baseline_nodes'],'node sum')
check(sum(r['cold_controller']['selected_total_events'] for r in R['originals'])==R['controller_selected_events'],'event sum')
raw=(D/'arc_child_scan272_raw.json').read_bytes()
summary=json.loads((D/'arc_child_scan272_summary.json').read_text())
check(hashlib.sha256(raw).hexdigest()==summary['raw_sha256'],'SHA')
print(json.dumps({'independent_assertions':asserts,'source_count':len(R['originals']),
 'sat_sources':R['sat_sources'],'unsat_sources':R['unsat_sources'],
 'verified_source_resolvents':R['source_resolvents'],
 'verified_pair_modes':R['pair_extreme_modes'],
 'verified_guest_children':sum(len(r['cold_controller']['children']) for r in R['originals']),
 'result':'PASS'},sort_keys=True))