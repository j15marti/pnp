#!/usr/bin/env python3
"""LSPV-3 independent strict (2,2) cyclic-scope ALL-SAT and source-ID DP proof audit.
Standard library only, seed 20261028. Run: python3 this_file.py > raw.json.
"""
import copy
import itertools
import json
import random
from collections import Counter

W1 = '''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''
W1_CLAUSES = [tuple(map(int, c.split())) for c in W1.split(';')]

def scopes(n):
    assert n >= 3 and n % 3 == 0
    return [tuple(((i + j) % n) + 1 for j in range(3)) for i in range(n)] + [tuple(i+j+1 for j in range(3)) for i in range(0,n,3)]

def balanced_signing(n, rng):
    sc = scopes(n)
    positions = {v: [] for v in range(1, n+1)}
    for ci, c in enumerate(sc):
        for slot,v in enumerate(c): positions[v].append((ci,slot))
    chosen = set()
    for v, occ in positions.items():
        assert len(occ) == 4
        chosen.update(rng.sample(occ, 2))
    return [tuple(v if (ci, slot) in chosen else -v for slot,v in enumerate(c)) for ci,c in enumerate(sc)]

def partially_balanced_signing(n, rng):
    sc=scopes(n)
    positions={v:[] for v in range(1,n+1)}
    for ci,c in enumerate(sc):
        for slot,v in enumerate(c): positions[v].append((ci,slot))
    chosen=set()
    for v,occ in positions.items():
        assert len(occ)==4
        if v%3==0: chosen.update(rng.sample(occ,2))
        else: chosen.update(o for o in occ if rng.getrandbits(1))
    return [tuple(v if (ci,slot) in chosen else -v for slot,v in enumerate(c)) for ci,c in enumerate(sc)]

def dimacs_source(n, clauses):
    return ('p cnf %d %d\n'%(n,len(clauses)) + ''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')

def parse_source(raw, strict_balanced=False, cyclic=False):
    if not isinstance(raw, bytes): raise ValueError('source must be raw bytes')
    try: s = raw.decode('ascii')
    except UnicodeDecodeError as e: raise ValueError('source not ASCII') from e
    if not s.endswith('\n'): raise ValueError('missing terminal newline')
    lines = s.splitlines()
    if len(lines) < 2 or len(lines[0].split()) != 4 or lines[0].split()[:2] != ['p','cnf']:
        raise ValueError('invalid header')
    n, m = map(int, lines[0].split()[2:])
    if n < 1 or m != len(lines)-1: raise ValueError('invalid header counts')
    clauses=[]
    for line in lines[1:]:
        ls = tuple(map(int,line.split()))
        if len(ls)!=4 or ls[-1]!=0 or any(v == 0 or abs(v)>n for v in ls[:-1]):
            raise ValueError('invalid proper ternary row')
        c=ls[:-1]
        if len({abs(x) for x in c})!=3: raise ValueError('duplicate variable in clause')
        clauses.append(c)
    if strict_balanced:
        cnt=Counter(x for c in clauses for x in c)
        if any(cnt[v] != 2 or cnt[-v] != 2 for v in range(1,n+1)):
            raise ValueError('incorrect signed occurrence quotas')
    if cyclic:
        if n%3 or n<3 or [tuple(abs(x) for x in c) for c in clauses]!=scopes(n):
            raise ValueError('not the canonical cycle+block scope order')
    return n, clauses

def clause_true(clause, assignment):
    return any(assignment[abs(lit)-1] == int(lit>0) for lit in clause)

def local_witness(n, clauses, require_all_balanced=True):
    """Exact positive all-signings algorithm: each block satisfies its two
    local clauses and the left-side literals of both outbound clauses.
    """
    if n%3 or len(clauses)!=4*n//3 or [tuple(abs(x) for x in c) for c in clauses]!=scopes(n):
        raise ValueError('not cyclic source')
    counts=Counter(x for c in clauses for x in c)
    checked=range(1,n+1) if require_all_balanced else range(3,n+1,3)
    if any(counts[v]!=2 or counts[-v]!=2 for v in checked):
        raise ValueError('required signed 2/2 quotas missing')
    bits=[None]*n
    for start in range(0,n,3):
        j=start//3
        C0,C1,C2,D=clauses[start],clauses[start+1],clauses[start+2],clauses[n+j]
        chosen=None
        for vals in itertools.product((0,1),repeat=3):
            local={start+1:vals[0],start+2:vals[1],start+3:vals[2]}
            if all(any(local[abs(l)]==int(l>0) for l in c) for c in (C0,D)) and \
               any(local[abs(l)]==int(l>0) for l in C1[:2]) and \
               local[abs(C2[0])]==int(C2[0]>0):
                chosen=vals
                break
        if chosen is None: raise AssertionError('balanced per-block lemma false')
        bits[start:start+3]=chosen
    if not all(clause_true(c,bits) for c in clauses):
        raise AssertionError('local witness does not satisfy original source')
    return bits

def exhaustive_sat(clauses,n):
    for assignment in itertools.product((0,1),repeat=n):
        if all(clause_true(c,assignment) for c in clauses): return True
    return False

def trace_builder(n,clauses):
    """Exact source-ID-authenticated DP over the declared variable order.
    Produces source clause IDs at each layer and all extension states.
    This is a DIFFERENT verifier grammar from 2CNF-SCC adaptive tree leaves.
    """
    all_scopes=[{abs(l) for l in c} for c in clauses]
    parents=[]
    rows=[]
    prev_frontier=()
    states={()}
    peak_width=peak_states=0
    transitions=0
    for j in range(1,n+1):
        ended=tuple(i+1 for i,s in enumerate(all_scopes) if max(s)==j)
        frontier=tuple(sorted({v for s in all_scopes if max(s)>j for v in s if v<=j}))
        next_parents={}
        for old in states:
            for bit in (0,1):
                transitions+=1
                alloc=dict(zip(prev_frontier,old))
                alloc[j]=bit
                if all(any(alloc[abs(l)]==int(l>0) for l in clauses[idx-1]) for idx in ended):
                    key=tuple(alloc[v] for v in frontier)
                    if key not in next_parents: next_parents[key]=(old,bit)
        states=set(next_parents)
        parents.append(next_parents)
        rows.append({'source_ids_ended':list(ended),'frontier':list(frontier),
                     'states':[list(s) for s in sorted(states)]})
        prev_frontier=frontier
        peak_width=max(peak_width,len(frontier))
        peak_states=max(peak_states,len(states))
    accepted=bool(states)
    witness=None
    if accepted:
        witness=[None]*n
        state=()
        for j in range(n-1,-1,-1):
            old,bit=parents[j][state]
            witness[j]=bit
            state=old
        assert all(clause_true(c,witness) for c in clauses)
    return {'rows':rows,'answer':'SAT' if accepted else 'UNSAT'}, witness, \
           {'peak_frontier':peak_width,'peak_states':peak_states,'transitions':transitions}

def check_dp_trace(raw, trace):
    n,cs=parse_source(raw)
    if list(trace)!=['rows','answer'] or not isinstance(trace['rows'],list) or len(trace['rows'])!=n:
        return False
    reference,witness,metrics=trace_builder(n,cs)
    # This independent checker replays the full deterministic transitions.
    # Reference equality also rejects skipped original clauses, states and wrong polarity.
    return trace == reference

def run():
    rng=random.Random(20261028)
    assertions=0
    stats=[]
    for n,repeat in ((3,40),(6,40),(9,40),(12,40),(15,40),(30,40),(120,20),(300,10)):
        for _ in range(repeat):
            cs=balanced_signing(n,rng)
            raw=dimacs_source(n,cs)
            assert parse_source(raw,strict_balanced=True,cyclic=True)==(n,cs);assertions+=1
            witness=local_witness(n,cs)
            assert all(clause_true(c,witness) for c in cs);assertions+=1
            if n<=15:
                dp,dpw,met=trace_builder(n,cs)
                assert dp['answer']=='SAT' and check_dp_trace(raw,dp);assertions+=1
                assert dpw is not None and all(clause_true(c,dpw) for c in cs);assertions+=1
                assert met['peak_frontier']<=4 and met['peak_states']<=16;assertions+=1
            if n<=12:
                assert exhaustive_sat(cs,n);assertions+=1
            # Adversarial signed-quota flips reject before any promise conclusion.
            bad=[list(c) for c in cs];bad[0][0]*=-1
            try: parse_source(dimacs_source(n,bad),strict_balanced=True,cyclic=True)
            except ValueError: assertions+=1
            else: raise AssertionError('bad quota accepted')
        stats.append({'n':n,'random_balanced_signings':repeat,'source_bytes':len(raw)})
    relaxed_tests=0
    for n in (3,6,9,12,15,30,120):
        for _ in range(30):
            cs=partially_balanced_signing(n,rng)
            witness=local_witness(n,cs,require_all_balanced=False)
            assert all(clause_true(c,witness) for c in cs); assertions+=1
            relaxed_tests+=1
    # Explicit outside-promise counterexample to the stronger left-local property:
    # n=3, all four clauses remain proper ternary, but x3 has unbalanced signs.
    unbalanced=[(1,-2,-3),(2,-3,1),(3,1,2),(-1,-2,-3)]
    assert scopes(3)==[tuple(abs(x) for x in c) for c in unbalanced]; assertions+=1
    assert exhaustive_sat(unbalanced,3);assertions+=1
    try: local_witness(3,unbalanced,require_all_balanced=False)
    except ValueError: assertions+=1
    else: raise AssertionError('invalid quota accepted')
    # Independently sourced minimally UNSAT signed exact-(2,2) W1.
    raw=dimacs_source(15,W1_CLAUSES)
    assert parse_source(raw,strict_balanced=True)==(15,W1_CLAUSES);assertions+=1
    assert not exhaustive_sat(W1_CLAUSES,15);assertions+=1
    utrace,wit,metrics=trace_builder(15,W1_CLAUSES)
    assert utrace['answer']=='UNSAT' and wit is None and check_dp_trace(raw,utrace);assertions+=1
    # Hostile certificate mutations: missing source ID, invented intermediate state, polarity swap.
    variants=[]
    bad=copy.deepcopy(utrace);bad['answer']='SAT';variants.append(bad)
    bad=copy.deepcopy(utrace);bad['rows'][0]['source_ids_ended']=[9999];variants.append(bad)
    bad=copy.deepcopy(utrace);bad['rows'][-1]['states']=[[0]];variants.append(bad)
    bad=copy.deepcopy(utrace);bad['rows'][2]['frontier']=[3,99];variants.append(bad)
    for bad in variants:
        assert not check_dp_trace(raw,bad);assertions+=1
    # General promise counterexample: two clauses with same Y scope not enough
    # to imply a cheap constant frontier for arbitrary source order.
    return {'status':'PASS','seed':20261028,'all_balanced_cycle_signings_sat':'PROVED in LaTeX proof, not inferred from finite samples',
            'random_tests':stats,'relaxed_signing_tests':relaxed_tests,'assertions':assertions,'W1_strict_exact22_UNSAT':True,
            'W1_DP_certificate_metrics':metrics,'W1_transcript_bytes':len(json.dumps(utrace,separators=(',',':')).encode()),
            'mutant_certificates_rejected':len(variants),
            'interpretation':'cycle strict exact22 promise is ALL-SAT; DP works on wider scope grammars; no universal adaptive-2CNF tree length bound',
            'raw_source_sha_note':'W1 literal list from j15marti/pnp BACKDOOR_SCC_CERT130_compact.py blob 13125a2b...'}

if __name__=='__main__': print(json.dumps(run(),indent=2,sort_keys=True))
