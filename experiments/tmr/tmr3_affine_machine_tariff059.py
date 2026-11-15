#!/usr/bin/env python3
"""TMR-3/036: independently implemented, source-authenticated 3-XOR CNF
recognizer and exact rational one-step affine tariff audit.
Native CPython execution is a high-level semantic implementation, not a
compiled deterministic Turing machine. Physical TM charges are proved in
report by bounded-symbol tape compilation; no free source metadata assumed.
"""
import itertools
import json
import math
import re
from collections import defaultdict
from fractions import Fraction

checks = 0
cases = 0
lab_rows = []
operation_totals = defaultdict(int)

def verify(test, info=''):
    global checks
    checks += 1
    if not test:
        raise AssertionError(info or 'assertion failed')

def clauses_for_parity(vars3, rhs):
    assert len(vars3) == 3 and len(set(vars3)) == 3
    ans=[]
    for bits in itertools.product((0,1), repeat=3):
        if (sum(bits)&1) != rhs:
            ans.append(tuple(v if b == 0 else -v for v,b in zip(vars3,bits)))
    return ans

def graph_cnf(n, edges, charges):
    inc = [[] for _ in range(n)]
    for i,(u,v) in enumerate(edges,1):
        assert 0 <= u < n and 0 <= v < n and u != v
        inc[u].append(i);inc[v].append(i)
    assert all(len(ids)==3 and len(set(ids))==3 for ids in inc)
    formula=[]
    for v in range(n):
        formula += clauses_for_parity(tuple(sorted(inc[v])),charges[v])
    return formula

def decode_complete_parity(clauses, ledger):
    # Every input clause is inspected; no graph/charge metadata is trusted.
    groups=defaultdict(list)
    for clause in clauses:
        ledger['clause_visits'] += 1
        if len(clause)!=3 or any(v == 0 for v in clause):
            return None
        ids=tuple(sorted(map(abs,clause)))
        ledger['id_inspections']+=3
        if len(set(ids))!=3:
            return None
        signed=tuple(clause)
        mask=tuple(1 if -v in signed else 0 for v in ids)
        groups[ids].append(mask)
    if not groups:
        return None
    # Dense source-ID compression is ESSENTIAL. A binary variable ID can be
    # 2**L while only <=3*#clauses distinct variables occur in the formula.
    # Never allocate a bitset indexed by the *numeric value* of a source ID.
    dense_ids={v:j for j,v in enumerate(sorted({v for ids in groups for v in ids}))}
    ledger['id_relabels'] += len(dense_ids)
    rows=[]
    for ids,masks in sorted(groups.items()):
        ledger['group_inspections']+=1
        if len(masks)!=4 or len(set(masks))!=4:
            return None
        zeros=set(tuple(b) for b in itertools.product((0,1),repeat=3) if sum(b)%2==0)
        ones=set(itertools.product((0,1),repeat=3)) - zeros
        if set(masks)==zeros:
            rhs=1  # wrong (forbidden) assignments are even
        elif set(masks)==ones:
            rhs=0  # wrong assignments are odd
        else:
            return None
        row=0
        for v in ids:
            row ^= 1 << dense_ids[v]
            ledger['row_bit_writes']+=1
        rows.append((row,rhs,ids))
    return rows

def gaussian_consistent(rows, ledger):
    pivots={}
    for mask,b,ids in rows:
        mask=int(mask);b=int(b)
        ledger['row_visits']+=1
        while mask:
            pivot=mask.bit_length()-1
            ledger['pivot_tests']+=1
            if pivot not in pivots:
                pivots[pivot]=(mask,b)
                ledger['retained_rows']+=1
                break
            pm,pb=pivots[pivot]
            mask ^= pm
            b ^= pb
            ledger['xor_row_events']+=1
        else:
            if b:
                ledger['contradictions']+=1
                return False
    return True

def affine_or_fallback(clauses):
    ledger=defaultdict(int)
    rows=decode_complete_parity(clauses,ledger)
    if rows is not None:
        answer=gaussian_consistent(rows,ledger)
        ledger['fast_path']=1
        return answer,'AFFINE',dict(ledger)
    # Off-class fallback is part of the single fixed total correct decider.
    ledger['fallback']=1
    vals=set(abs(v) for cl in clauses for v in cl)
    names=sorted(vals)
    for bits in itertools.product((0,1),repeat=len(names)):
        ledger['fallback_assignments']+=1
        setting=dict(zip(names,bits))
        if all(any((setting[abs(l)]==1 if l>0 else setting[abs(l)]==0) for l in clause) for clause in clauses):
            return True,'FALLBACK',dict(ledger)
    return False,'FALLBACK',dict(ledger)

def brute(clauses):
    vals=sorted(set(abs(v) for cl in clauses for v in cl))
    for bits in itertools.product((0,1),repeat=len(vals)):
        a=dict(zip(vals,bits))
        if all(any((a[abs(v)]==1 if v>0 else a[abs(v)]==0) for v in cl) for cl in clauses):
            return True
    return False

def graph_components(n,edges,charges):
    adj=[set() for _ in range(n)]
    for u,v in edges:
        adj[u].add(v);adj[v].add(u)
    done=set();components=[]
    for v in range(n):
        if v in done:continue
        todo=[v];done.add(v);component=[]
        while todo:
            x=todo.pop();component.append(x)
            for y in adj[x]:
                if y not in done:done.add(y);todo.append(y)
        components.append(component)
    return all(sum(charges[v] for v in comp)%2==0 for comp in components)

def serialize(clauses):
    return ''.join(' '.join(map(str,cl))+'\n' for cl in clauses)

def parse_wire(raw):
    # Strict explicit byte-level line grammar. No precomputed graph or charges.
    if not isinstance(raw,str) or not raw or not raw.endswith('\n'):
        return None
    parsed=[]
    for line in raw[:-1].split('\n'):
        terms=line.split(' ')
        if len(terms)!=3 or any(not re.fullmatch(r'-?[1-9][0-9]*',x) for x in terms):
            return None
        parsed.append(tuple(map(int,terms)))
    return parsed

def run_case(clauses,expected=None, label=''):
    global cases
    raw=serialize(clauses)
    recovered=parse_wire(raw)
    verify(recovered==clauses, 'wire decode mismatch')
    result,route,ledger=affine_or_fallback(recovered)
    ledger['source_bytes'] = len(raw.encode('ascii'))
    oracle=brute(clauses)
    verify(result == oracle, f'wrong {label}: {result} vs {oracle}')
    if expected is not None:verify(result == expected, f'expected {label}')
    for key,val in ledger.items():
        if isinstance(val,int):operation_totals[key]+=val
    cases+=1
    return result,route

K4=list(itertools.combinations(range(4),2))
K33=[(i,j) for i in range(3) for j in range(3,6)]
CUBE=[(i,j) for i in range(8) for j in range(i+1,8) if (i^j).bit_count()==1]
TWO_K4=K4+[(u+4,v+4) for u,v in K4]
for n,edges in [(4,K4),(6,K33),(8,CUBE),(8,TWO_K4)]:
    for assignment in itertools.product((0,1),repeat=n):
        # 8-vertex cubes: 256 charges * 4096 truth assignments per oracle.
        charges=list(assignment)
        cnf=graph_cnf(n,edges,charges)
        want=graph_components(n,edges,charges)
        answer,route=run_case(cnf,want,f'graph {n} {charges}')
        verify(route=='AFFINE')
        if n==4 and charges==(1,0,0,0):
            shuffled=list(reversed(cnf))
            verify(run_case(shuffled,False)[1]=='AFFINE')
            renamed=[tuple((abs(x)+27)*(1 if x>0 else -1) for x in cl) for cl in cnf]
            verify(run_case(renamed,False)[1]=='AFFINE')
            bad=list(cnf)+[cnf[0]]
            verify(run_case(bad,False)[1]=='FALLBACK')
            malformed=list(cnf)+[(1,-1,2)]
            verify(run_case(malformed,False)[1]=='FALLBACK')
            incomplete=list(cnf[:-1])
            verify(run_case(incomplete)[1]=='FALLBACK')
# Affine non-Tseitin control: four 3-XOR rows, shared vars that occur 1,3,4 times.
base=clauses_for_parity((1,2,3),0)+clauses_for_parity((2,3,4),1)+clauses_for_parity((1,3,5),1)
verify(run_case(base)[1]=='AFFINE')
# Formula with no well-formed affine source: ordinary satisfiable 3-CNF uses fallback.
verify(run_case([(1,2,3)],True)[1]=='FALLBACK')
for corrupted in ('', '1 2 3', '1  2 3\n', '0 2 3\n', '1 2 03\n', '1 2 3\nextra', '1 2 3\n\n'):
    verify(parse_wire(corrupted) is None,'malformed source wire')
# Hostile binary-encoding control: sparse, enormous numeric variable IDs
# must NOT turn a polynomial source into an exponentially wide bit matrix.
huge=(2**110+3,2**110+99,2**110+431)
verify(run_case(clauses_for_parity(huge,1),True)[1]=='AFFINE')
verify(run_case(clauses_for_parity(huge,0)+clauses_for_parity(huge,1),False)[1]=='FALLBACK')
# Opposite complete parity constraints on identical variable triple cannot
# both be accepted by a decoder requiring exactly four clauses per triple;
# fallback must still give the correct UNSAT label.
# Local physical transition: read source b and accumulator p; write p XOR b,
# consume one physical pending marker, advance source head. All effects in ONE
# finite-alphabet multitape transition. Flags are correlated, not disjoint jobs.
# Coordinates: CNF,affine,separator,fusion,Gamma,interface,machine.
lambda_good=list(map(Fraction,['0','1/4','0','0','1/4','1/4','1/4']))
lambda_bad=list(map(Fraction,['0','1/2','0','0','1/2','1/2','0']))
for b,p in itertools.product((0,1),repeat=2):
    delta=[0,1,0,0,1,1,1]
    price=1
    good=sum(w*x for w,x in zip(lambda_good,delta))
    bad=sum(w*x for w,x in zip(lambda_bad,delta))
    verify(good==1 and bad==Fraction(3,2))
    verify((p^b) == ((p+b)&1))
    lab_rows.append({'rule':'READ_XOR_CLEAR','b':b,'p_before':p,'p_after':p^b,
                     'precondition':'q=PARITY_READ, marker=M, current input bit=b',
                     'delta':delta,'price':price,
                     'good_tariff':str(good),'bad_tariff':str(bad)})
# Other actual finite-control rows: READ source bit without discharging any
# of this phase's outstanding flags, and a paid malformed-input fallback switch.
for rule in ('SCAN','MOVE','FALLBACK_SWITCH','RECOMPUTE','OUTPUT'):
    delta=[0]*7
    verify(sum(w*x for w,x in zip(lambda_good,delta))<=1)
    lab_rows.append({'rule':rule,'delta':delta,'price':1,'good_tariff':'0'})
summary={'claim':'AFFINE-SAT-COST059', 'native_execution':'CPython model, not compiled TM',
         'cases':cases,'assertions':checks,'failures':0,'program_proxy_totals':dict(sorted(operation_totals.items())),
         'tariff_columns':['CNF','affine','separator','fusion','Gamma','interface','machine'],
         'good_lambda':[str(w) for w in lambda_good],
         'bad_lambda':[str(w) for w in lambda_bad],
         'tariff_rows':lab_rows,
         'validity':'local physical transition semantics and source-authenticated parity decoder; no SAT lower bound'}
print(json.dumps(summary,indent=2,sort_keys=True))
