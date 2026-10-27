#!/usr/bin/env python3
"""CIRCUIT-SOURCE-SELECT-BARRIER172, 2026-10-27 UTC.

Standalone exact finite checks for a no-preprocessing inverse-occurrence lower bound on
proper signed exact-(2,2)-3CNF, and a contrasting canonical fixed-layout
O(log N)-space occurrence Rank/Select program. Includes indexed bit costs and
bounded-input-jump itineraries. Python 3 standard library; no external data.

  python3 CIRCUIT_SOURCE_SELECT_BARRIER172_repro.py --out evidence.json

Counters are explicitly specified abstract-machine events, NOT CPython RAM
measurements. No general SAT circuit lower bound is claimed.
"""
from __future__ import annotations
from collections import Counter
from itertools import permutations, product
from math import ceil
import argparse, json, hashlib, inspect

W1 = (
 (-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
 (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
 (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
 (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14),
)
AIDX=(6,11)
BIDX=(17,9)
FIXED=tuple(j for j in range(20) if j not in AIDX+BIDX)
MAGIC='1010111100010010'


def gadget(a,b):
    """a=b=1 yields W1 UNSAT. Both a,b=0 yield SAT H00."""
    clauses=[list(c) for c in W1]
    if a==0:
        for j in AIDX: clauses[j][0]=-clauses[j][0]
    if b==0:
        for j in BIDX: clauses[j][2]=-clauses[j][2]
    return tuple(tuple(c) for c in clauses)


def models15(cnf):
    count=0
    witness=None
    for bits in range(1<<15):
        if all(any(((bits>>(abs(l)-1))&1)==(l>0) for l in c) for c in cnf):
            count+=1
            if witness is None:witness=bits
    return count,witness


def structure_check(formula,n):
    p=Counter();q=Counter();seen=set()
    for row in formula:
        assert len(row)==3 and len(set(map(abs,row)))==3
        assert row not in seen
        seen.add(row)
        for lit in row:
            assert 1<=abs(lit)<=n
            (p if lit>0 else q)[abs(lit)]+=1
    assert len(formula)*3==4*n
    assert all(p[j]==q[j]==2 for j in range(1,n+1))
    return {'proper':True,'clause_distinct':True,'signed_2_2':True,
            'mixed_sign_clauses':sum(0<sum(l<0 for l in c)<3 for c in formula)}


def uniform_product(k,perm,source):
    """Physical block position p holds labeled component perm[p]."""
    assert sorted(perm)==list(range(k))
    return tuple(tuple((15*perm[p]+abs(l))*(1 if l>0 else -1)
                      for l in row)
                 for p in range(k) for row in source)


def encmeta(k):
    w=(20*k).bit_length()    # Header C=20k fits in w bits; all variable IDs do.
    H=len(MAGIC)+2*w
    stride=3*(w+1)
    return {'m':k,'w':w,'V':15*k,'C':20*k,'H':H,'stride':stride,
            'N':H+20*k*stride}


def clause_bits(row,w):
    return ''.join(('1' if l>0 else '0')+format(abs(l),f'0{w}b') for l in row)


def encode(formula,k):
    m=encmeta(k);assert len(formula)==20*k
    return (MAGIC+format(m['V'],f"0{m['w']}b")
             +format(m['C'],f"0{m['w']}b")
             +''.join(clause_bits(c,m['w']) for c in formula))


def positions_brute(formula,v):
    return tuple((ci,slot,lit) for ci,row in enumerate(formula)
                     for slot,lit in enumerate(row) if abs(lit)==v)


def template_support(local):
    out=[]
    for ci,row in enumerate(W1):
        for slot,lit in enumerate(row):
            if abs(lit)==local:out.append((ci,slot))
    assert len(out)==4
    return tuple(out)


def fixed_clause(k,a,b,ci):
    if ci<2*k:
        i,rank=divmod(ci,2); original=AIDX[rank]
    elif ci<18*k:
        i,rank=divmod(ci-2*k,16);original=FIXED[rank]
    else:
        i,rank=divmod(ci-18*k,2);original=BIDX[rank]
    return tuple((15*i+abs(l))*(1 if l>0 else -1)
                  for l in gadget(a[i],b[i])[original])


def fixed_formula(k,a,b):
    return tuple(fixed_clause(k,a,b,ci) for ci in range(20*k))


def phys_clause_index(k,component,original):
    if original in AIDX:
        return 2*component+AIDX.index(original)
    if original in BIDX:
        return 18*k+2*component+BIDX.index(original)
    return 2*k+16*component+FIXED.index(original)


def selector_local(k,v,abit,bbit):
    """Four signed occurrences with only TWO local control bits and log-size registers.

    No O(k) arrays are created; W1/AIDX/BIDX/FIXED are fixed program ROM.
    """
    assert 1<=v<=15*k
    i,j=divmod(v-1,15);j+=1
    variant=gadget(abit,bbit)
    items=[]
    for original,slot in template_support(j):
        clause=phys_clause_index(k,i,original)
        signed=variant[original][slot]
        lit=(15*i+abs(signed))*(1 if signed>0 else -1)
        m=encmeta(k)
        bitaddr=m['H']+clause*m['stride']+slot*(m['w']+1)
        items.append((clause,slot,lit,bitaddr))
    out=tuple(sorted(items))
    assert sum(x[2]>0 for x in out)==2
    assert sum(x[2]<0 for x in out)==2
    return out


def selector_fixed(k,a,b,v):
    i=(v-1)//15
    return selector_local(k,v,a[i],b[i])


def occ_rank_fixed(k,a,b,v,clause,slot):
    for r,x in enumerate(selector_fixed(k,a,b,v)):
        if x[0]==clause and x[1]==slot:return r
    return -1


def read_control_addr(k,side,i):
    m=encmeta(k)
    ci=2*i if side=='A' else 18*k+2*i
    slot=0 if side=='A' else 2
    return m['H']+ci*m['stride']+slot*(m['w']+1)


def indexed_select(k,source_bits,v):
    """One indexed bit read for each relevant A/B control (to infer polarity).

    Each address must be written bit-by-bit in RAT. Logword-RAM quotient uses
    O(1) arithmetic instructions per address plus fixed 20-row ROM scan.
    """
    m=encmeta(k)
    i=(v-1)//15
    address_width=(m['N']+1).bit_length()
    addresses=[read_control_addr(k,'A',i),read_control_addr(k,'B',i)]
    abits=[int(source_bits[p]) for p in addresses]
    out=selector_local(k,v,abits[0],abits[1])
    return out, {'indexed_bit_reads':2,'index_address_bit_writes':2*address_width,
                 'abstract_logword_operations_bound':128,
                 'max_live_logwords_bound':12,
                 'max_live_index_bits_bound':12*address_width,
                 'physical_bit_addresses':addresses}


def program_for_target(k,perm,v=1):
    """Give whole physical blocks as unit-cost blocks, stronger than bit reads.
    Return exact block query count until the target is found or last inferred.
    """
    c=(v-1)//15
    located=None;probes=0
    for idx in range(k-1):
        probes+=1
        if perm[idx]==c:
            located=idx
            break
    if located is None:located=k-1
    return located,probes


def direct_sign_input(k,a,b):
    return encode(fixed_formula(k,a,b),k)


def valid_header_and_template(k,a,b,word):
    """Exact bit-by-bit template test. This checker is for a declared image,
    not a decision algorithm on arbitrary signed exact22 CNF inputs.
    """
    if len(word)!=encmeta(k)['N']:return False
    for bitpos in range(len(word)):
        # Python materialization is instrumentation; abstract streaming verifier
        # uses arithmetic (ci,slot,field) and 20-entry ROM to compute the bit.
        if word[bitpos]!=virtual_fixed_bit(k,a,b,bitpos):return False
    return True


def virtual_fixed_bit(k,a,b,bitpos):
    m=encmeta(k)
    h=MAGIC+format(m['V'],f"0{m['w']}b")+format(m['C'],f"0{m['w']}b")
    if bitpos<m['H']:return h[bitpos]
    ci,inside=divmod(bitpos-m['H'],m['stride'])
    slot,r=divmod(inside,m['w']+1)
    return clause_bits((fixed_clause(k,a,b,ci)[slot],),m['w'])[r]



def promise_gate_at(k,g):
    """Index-only descriptor for the canonical disjointness-promise circuit.

    Input nodes 0..2k-1 represent the A,B sign-anchor bits. Gate IDs
    0..2k-1 live in a different typed namespace: use operand refs ('I',id)
    and ('G',id) to prevent wire/gate conflation.
    Gate IDs g=0..k-1 AND; g=k..2k-2 OR; g=2k-1 NOT.
    """
    assert k>=1 and 0<=g<2*k
    if g<k:return ('AND',(('I',2*g),('I',2*g+1)))
    if g==2*k-1:
        src=2*k-2 if k>1 else 0
        return ('NOT',(('G',src),))
    j=g-k+1  # g=k is OR(AND0,AND1), g=k+1 brings AND2
    left=('G',0 if j==1 else g-1)
    right=('G',j)
    return ('OR',(left,right))


def evaluate_promise_circuit(k,a,b):
    primary=tuple(z for ab in zip(a,b) for z in ab)
    gates=[]
    edge_count=0
    for g in range(2*k):
        op,refs=promise_gate_at(k,g)
        values=[primary[i] if typ=='I' else gates[i] for typ,i in refs]
        edge_count+=len(refs)
        if op=='AND':v=int(values[0] and values[1])
        elif op=='OR':v=int(values[0] or values[1])
        else:v=int(not values[0])
        gates.append(v)
    assert edge_count==4*k-1
    return bool(gates[-1]),{'AND':k,'OR':k-1,'NOT':1,
        'binary_or_unary_gates':2*k,'primary_input_nodes':2*k,
        'gate_output_nodes':2*k,'distinct_signal_nodes':4*k,
        'gate_operand_edges':edge_count,'output_bits':1,
        'id_width':(4*k).bit_length(),
        'minimum_fixed_width_operand_reference_bits':edge_count*(4*k).bit_length()}

def jump_itinerary(k,B,J):
    """Physical sign probes in block batches B on one augmented input head.
    Count J-bounded teleports, actual geometric distance separately, and
    landings within the fixed middle gap. This is a Promise algorithm.
    """
    assert J>=1 and B>=1
    m=encmeta(k)
    coords=[]
    for lo in range(0,k,B):
        hi=min(k,lo+B)
        coords.extend(read_control_addr(k,'A',i) for i in range(lo,hi))
        coords.extend(read_control_addr(k,'B',i) for i in range(lo,hi))
    head=0;command_count=0;geometric=0;reversals=0
    direction=0;gaplandings=0;landing_positions=[]
    gapstart=m['H']+2*k*m['stride']
    gapend=m['H']+18*k*m['stride']
    for target in coords:
        step=target-head
        if step and direction and (step>0)!=(direction>0):reversals+=1
        if step:direction=1 if step>0 else -1
        geom=abs(step);geometric+=geom
        while head!=target:
            off=min(J,abs(target-head))
            head+=direction*off
            command_count+=1
            if gapstart<head<gapend:gaplandings+=1
            if len(landing_positions)<16:landing_positions.append(head)
        assert head==target
    return {'m':k,'N':m['N'],'B':B,'J':J,
            'source_sign_probes':2*k,
            'input_jump_commands':command_count,
            'geometric_travel_cells':geometric,
            'input_direction_reversals':reversals,
            'landings_in_strict_fixed_middle_gap':gaplandings,
            'logwork_space_bound_bits':B+12*(m['N']+1).bit_length(),
            'jump_command_offset_bits_upper':command_count*(J+1).bit_length(),
            'first_16_landing_positions':landing_positions}


def exhaustive_run():
    evidence={}; assertions=0
    counts={}
    for a,b in product((0,1),repeat=2):
        G=gadget(a,b)
        summary=structure_check(G,15);assertions+=1
        count,_=models15(G)
        assert (count==0)==(a==b==1)
        counts[f'{a}{b}']={'models':count,'mixed':summary['mixed_sign_clauses']}
        assertions+=1
    assert [counts[f'{a}{b}']['models'] for a,b in product((0,1),repeat=2)]==[772,272,272,0]
    evidence['gadget_four_models']=counts
    block_cases=[]
    for k in range(1,6):
        allperms=list(permutations(range(k)))
        qdist=[]
        for typ,source in [('SAT',gadget(0,0)),('UNSAT',gadget(1,1))]:
            for perm in allperms:
                F=uniform_product(k,perm,source)
                structure_check(F,15*k);assertions+=1
                pos=positions_brute(F,1)
                expectedblock=perm.index(0)
                assert len(pos)==4 and all(ci//20==expectedblock for ci,sl,lit in pos)
                assert sum(lit>0 for ci,sl,lit in pos)==2
                assert sum(lit<0 for ci,sl,lit in pos)==2
                physical=encode(F,k);assert len(physical)==encmeta(k)['N']
                for r,(ci,sl,lit) in enumerate(pos):
                    loc=encmeta(k)['H']+ci*encmeta(k)['stride']+sl*(encmeta(k)['w']+1)
                    assert physical[loc]==('1' if lit>0 else '0')
                found,blocks=program_for_target(k,perm)
                assert found==expectedblock and blocks<=max(k-1,0)
                if typ=='SAT':qdist.append(blocks)
                assertions+=9
            # Preprocess arbitrary physical permutation only by a full scan;
            # otherwise the O(1) location formula is unavailable.
        if k>1:
            assert max(qdist)==k-1
            assert sum(qdist)*2*k==len(qdist)*(k-1)*(k+2)
        else:assert set(qdist)=={0}
        block_cases.append({'k':k,'both_label_permutations_checked':2*len(allperms),
                            'SAT_max_full_block_queries':max(qdist),
                            'SAT_average_full_block_queries':sum(qdist)/len(qdist),
                            'optimum_worst_queries':k-1})
    evidence['permutation_inverse_oracle']=block_cases
    # Source-index ambiguity has a direct same-input-bit firewall: two
    # permutations with identical header and all touched block bytes, but
    # target occurrence moving to a different untouched block.
    adversaries=[]
    for k in range(2,8):
        for t in range(k-1):
            # Inspected prefix is blocks 0..t-1, with target in last physical block.
            reference=tuple(list(range(1,k))+[0])
            variant=list(reference)
            variant[t],variant[-1]=variant[-1],variant[t]
            variant=tuple(variant)
            assert reference[:t]==variant[:t]
            for source in (gadget(0,0),gadget(1,1)):
                F=uniform_product(k,reference,source)
                H=uniform_product(k,variant,source)
                f=encode(F,k);h=encode(H,k)
                meta=encmeta(k)
                prefix=meta['H']+20*t*meta['stride']
                assert f[:prefix]==h[:prefix]
                assert positions_brute(F,1)!=positions_brute(H,1)
                assertions+=3
            adversaries.append({'k':k,'inspected_complete_blocks':t,
                                'unseen_compatible_targets':k-t})
    evidence['indistinguishable_unread_prefixes']=adversaries
    fixed=[]
    promise_circuit_evaluations=0
    for k in range(1,5):
        pairs=0
        for a in product((0,1),repeat=k):
            for b in product((0,1),repeat=k):
                cnf=fixed_formula(k,a,b)
                structure_check(cnf,15*k)
                promise_answer,circuit_metrics=evaluate_promise_circuit(k,a,b)
                assert promise_answer==(not any(x and y for x,y in zip(a,b)))
                assert circuit_metrics["binary_or_unary_gates"]==2*k
                promise_circuit_evaluations+=1
                word=encode(cnf,k)
                assert valid_header_and_template(k,a,b,word)
                assert len(word)==encmeta(k)['N']
                for v in range(1,15*k+1):
                    occ=selector_fixed(k,a,b,v)
                    truth=positions_brute(cnf,v)
                    assert tuple((x[0],x[1],x[2]) for x in occ)==truth
                    got,cost=indexed_select(k,word,v)
                    assert got==occ and cost['indexed_bit_reads']==2
                    for r,x in enumerate(occ):
                        assert occ_rank_fixed(k,a,b,v,x[0],x[1])==r
                        assert word[x[3]]==('1' if x[2]>0 else '0')
                    assertions+=7
                pairs+=1
        fixed.append({'k':k,'valid_source_pairs':pairs,'variable_rank_select_checks':pairs*15*k,
                      'N':encmeta(k)['N'],'word_width':encmeta(k)['w']})
    evidence['fixed_oblivious_source_inverse']=fixed
    evidence['promise_decision_circuit']={'evaluated_controls':promise_circuit_evaluations,
      'separate_primary_wire_and_gate_nodes':True,
      'gate_count':'2k','input_wire_nodes':'2k','operand_edges':'4k-1',
      'explicit_descriptor_bit_floor':'(4k-1)*ceil(log2(4k+1))',
      'full_ordinary_SAT_circuit':False}
    # Explicit rejection of a 1-bit malformed perturbation within otherwise
    # canonical word. Structural quota changes for a polarity flip at one port.
    k=3;a=(0,1,0);b=(1,0,1)
    reference=direct_sign_input(k,a,b)
    perturbed=list(reference)
    control=read_control_addr(k,'A',1)
    perturbed[control]='0' if perturbed[control]=='1' else '1'
    bad=''.join(perturbed)
    assert not valid_header_and_template(k,a,b,bad)
    affected_ci=2*1
    malformed=[fixed_clause(k,a,b,ci) for ci in range(20*k)]
    row=list(malformed[affected_ci]);row[0]=-row[0];malformed[affected_ci]=tuple(row)
    p=Counter();q=Counter()
    for row in malformed:
        for lit in row:(p if lit>0 else q)[abs(lit)]+=1
    assert sorted((p[15+4],q[15+4]))==[1,3]
    evidence['malformed_one_polarity']={'position':control,
      'canonical_membership_rejected':True,'signed_2_2_balance_destroyed':True,
      'source_parameter_promise_only':True}
    # Native augmented-jump itinerary and the cut-bypass falsifier.
    itineraries=[]
    for k in (2,4,8,16,32,64):
        N=encmeta(k)['N']
        for B in (1,max(1,k//4),k):
            for J in (1,2,8,max(1,N//8),N):
                r=jump_itinerary(k,B,J)
                assert r['input_jump_commands']<=r['geometric_travel_cells']
                if J==1:assert r['input_jump_commands']==r['geometric_travel_cells']
                if J==N:assert r['landings_in_strict_fixed_middle_gap']==0
                itineraries.append(r)
                assertions+=3
    evidence['jump_itineraries']=itineraries
    evidence['boundaries']={
        'M1': 'input-inclusive footprint P1>=N; one real read-write head',
        'Mk': 'one sequential read-only input head, k fixed work tapes; work space excludes input',
        'MJ': 'one charged radius-J input jump per command, target-only read; no crossing-sequence splice on skipped cells',
        'RAT': 'indexed read-only input with binary-address write cost; logword RAM operations separately counted',
        'full_SAT_decision_circuit': 'NOT constructed: only fixed promise/canonical witness location',
        'complete_gate_compiler_inverse': 'OPEN: nonfinal comparator sectors already done, scan/mux/aliases remain',
        'ARC_EDGE_90': 'OPEN','P_vs_NP':'OPEN'}
    evidence['audit']={'assertion_groups_at_least':assertions,
      'source_gadget_assignments_exhaustively_evaluated':4*(1<<15),
      'permutation_cnf_cases':sum(x['both_label_permutations_checked'] for x in block_cases),
      'tested_inverse_input_families':sum(x['valid_source_pairs'] for x in fixed),
      'tested_select_variables':sum(x['variable_rank_select_checks'] for x in fixed),
      'jump_cases':len(itineraries),
      'failed_assertions':0,'randomness':None}
    return evidence


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='CIRCUIT_SOURCE_SELECT_BARRIER172_raw.json')
    args=ap.parse_args()
    data=exhaustive_run()
    with open(args.out,'w',encoding='utf-8') as f:
        json.dump(data,f,indent=2,sort_keys=True)
        f.write('\n')
    print(json.dumps({'audit':data['audit'],
      'permutation_results':data['permutation_inverse_oracle'],
      'fixed_locator_results':data['fixed_oblivious_source_inverse'],
      'raw_file':args.out},indent=2))

if __name__=='__main__':main()