#!/usr/bin/env python3
"""Independent source/original clause certificate/S-U/grammar controls for forward_bridge.
No imports from producer or optimized circuit implementation.
"""
import json
from collections import Counter
from pathlib import Path

POS = [(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
NEG = [(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
clauses = [tuple(c) for c in POS]+[tuple(-v for v in c) for c in NEG]


def grammar_ok(cc,variables=9):
    if not isinstance(cc,(list,tuple)) or len(cc)*3!=4*variables:return False
    counts=Counter();seen=set()
    for c in cc:
        if len(c)!=3 or len(set(map(abs,c)))!=3 or not (all(z>0 for z in c) or all(z<0 for z in c)) or any(abs(z)<1 or abs(z)>variables for z in c):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key)
        for z in c:counts[(abs(z),z>0)]+=1
    return all(counts[(v,s)]==2 for v in range(1,variables+1) for s in [False,True])


def literal_value(v,assignment):
    x=bool(assignment>>(abs(v)-1)&1)
    return x if v>0 else not x


def counts(assignment):
    return [sum(literal_value(v,assignment) for v in c) for c in clauses]


def models_for_pins(pins):
    a=[]
    for mask in range(512):
        if all(bool(mask>>(k-1)&1)==bool(v) for k,v in pins.items()) and all(c>0 for c in counts(mask)):
            a.append(mask)
    return a


def binstr(a):return ''.join(str(a>>(v-1)&1) for v in range(1,10))

def main():
    assert grammar_ok(clauses)
    fail_cases = []
    bad=list(clauses);bad[0]=tuple(reversed(bad[1]));fail_cases.append(bad) # duplicate
    bad=list(clauses);bad[0]=(1,1,6);fail_cases.append(bad) # repeated literal
    bad=list(clauses);bad[0]=(1,-5,6);fail_cases.append(bad) # mixed clause
    bad=list(clauses);bad[0]=(1,5,10);fail_cases.append(bad) # wrong range
    bad=list(clauses[:-1]);fail_cases.append(bad) # bad clause count
    bad=list(clauses);bad[0]=(1,5,7);fail_cases.append(bad) # corrupted quota
    assert all(not grammar_ok(b) for b in fail_cases)
    p_u={1:1,3:0,5:1,6:0,7:0,8:0}
    p_s=dict(p_u);p_s[1]=0
    u_models=models_for_pins(p_u)
    s_models=models_for_pins(p_s)
    assert len(u_models)==0 and len(s_models)==2
    leaves=[]
    for free_bits in range(8):
        assignment=sum(p_u[v]<<(v-1) for v in p_u)
        for j,v in enumerate((2,4,9)):
            assignment |= ((free_bits>>j)&1) << (v-1)
        vals=counts(assignment)
        assert 0 in vals
        j=vals.index(0)
        leaves.append({'assignment_x1_to_x9':binstr(assignment),'false_original_clause_index_0based':j,'false_clause':clauses[j]})
    assert len(set(i['assignment_x1_to_x9'] for i in leaves))==8
    cert=[]
    for j,c in enumerate(clauses):
        sats={abs(z):(1 if z>0 else 0) for z in c}
        unsats={abs(z):(0 if z>0 else 1) for z in c}
        cert.append({'clause_index_0based':j,'signed_lits':c,'local_all_S':sats,'local_all_U':unsats,
                     'complement_S_is_U':all(1-v == unsats[k] for k,v in sats.items())})
    compatible=0
    for j in range(12):
        for k in range(j+1,12):
            for mode_j in ('S','U'):
                for mode_k in ('S','U'):
                    target_j={abs(z):int(z>0) if mode_j=='S' else int(z<0) for z in clauses[j]}
                    target_k={abs(z):int(z>0) if mode_k=='S' else int(z<0) for z in clauses[k]}
                    want=all(target_j.get(v,target_k[v])==target_k[v] for v in target_k)
                    got=any(all((a>>(v-1)&1)==val for v,val in target_j.items()) and
                            all((a>>(v-1)&1)==val for v,val in target_k.items()) for a in range(512))
                    assert want==got
                    compatible+=1
    assert compatible==264
    for a in range(512):
        ca=counts(a);cb=counts(a^511)
        assert all(ca[j]+cb[j]==3 for j in range(12))
    result={'source_m22_valid':True,'global_sat_models':len(models_for_pins({})),
            'pins_satisfiable':p_s,'pin_S_models':[binstr(a) for a in s_models],
            'pins_unsatisfiable':p_u,'U_8_leaf_exhaustive_falsifications':leaves,
            'local_targets':cert,'exact_su_clause_pair_modes_checked':compatible,
            'complement_clause_count_checks':512*12,
            'malformed_variants_rejected':len(fail_cases)}
    assert result['global_sat_models']==70
    out=Path(__file__).with_name('independent_controls.json')
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('local_targets','U_8_leaf_exhaustive_falsifications')},indent=2))
    print('WRITTEN',out)
if __name__=='__main__':main()
