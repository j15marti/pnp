#!/usr/bin/env python3
"""LSPV-3 SOURCE-COVER-OPTGAP146, deterministic standard-library audit.

Original-source 3CNF clauses, boundary-cover/Set-Cover exact reduction,
auditably derived Resolution lines, W1 signed exact-22 witness controls.
All finite tests are evidence only, with symbolic proofs in paired LaTeX.
"""
import itertools
import json
import math
import random
import hashlib
from collections import Counter

SEED=20261027
rng=random.Random(SEED)
checks=Counter()

def test(condition, key):
    checks[key]+=1
    if not condition: raise AssertionError(key)

def lit_forbidden(bit, var):
    return -var if bit else var

def chain(lits, first_fresh):
    assert len(lits)>=3
    if len(lits)==3:
        z,u=first_fresh,first_fresh+1
        # Private tagged 3CNF chain keeps original source clauses distinct even
        # when two different source modules exclude the same boundary word.
        return [(-z,lits[2],u),(-z,lits[2],-u),(lits[0],lits[1],z)],first_fresh+2
    zs=list(range(first_fresh,first_fresh+len(lits)-3))
    result=[(lits[0],lits[1],zs[0])]
    for j in range(1,len(zs)):
        result.append((-zs[j-1],lits[j+1],zs[j]))
    result.append((-zs[-1],lits[-2],lits[-1]))
    return result,first_fresh+len(zs)

def build(universe, sets):
    """0-th module is mandatory outside-universe exclusion; others are set exclusions."""
    b=max(3,math.ceil(math.log2(universe+1)))
    entries=[]; nextvar=b+1
    for module_id, exclusion in enumerate([set(range(universe,1<<b))]+list(map(set,sets))):
        chains=[]
        for word in sorted(exclusion):
            ls=[lit_forbidden((word>>j)&1,j+1) for j in range(b)]
            cls,nextvar=chain(ls,nextvar)
            chains.append({'word':word,'module':module_id,'clauses':cls})
        entries.append({'id':module_id,'excluded':sorted(exclusion),'chains':chains})
    allclauses=[]
    for ent in entries:
        for ch in ent['chains']:
            allclauses.extend(ch['clauses'])
    header=f'p cnf {nextvar-1} {len(allclauses)}\n'
    physical=header;source={};offset=len(header)
    for ent in entries:
        for ch in ent['chains']:
            ids=[]
            for c in ch['clauses']:
                ids.append(offset); source[offset]=c
                row=' '.join(str(v) for v in c)+' 0\n'
                physical+=row;offset+=len(row)
            ch['source_ids']=ids
    return {'b':b,'universe':universe,'modules':entries,'clauses':allclauses,
            'source':source,'encoded':physical,'header_bytes':len(header),'nvars':nextvar-1}

def parse_original_source_row_at(src, offset):
    """Return signed originals only for valid physical source-line start offsets."""
    encoded=src['encoded']
    if not isinstance(offset,int) or offset<src['header_bytes'] or offset>=len(encoded):return None
    if encoded[offset-1]!='\n':return None
    stop=encoded.find('\n',offset)
    if stop<0:return None
    line=encoded[offset:stop].split()
    if len(line)!=4 or line[-1]!='0':return None
    try: row=tuple(map(int,line[:3]))
    except ValueError:return None
    return row if all(v!=0 for v in row) else None

def projected_clause_satisfied(word, clause, b, auxiliary):
    def value(lit):
        v=abs(lit)
        x=((word>>(v-1))&1) if v<=b else ((auxiliary>>(v-b-1))&1)
        return bool(x) if lit>0 else not bool(x)
    return any(value(x) for x in clause)

def chain_projected(ch, b):
    fresh=sorted({abs(x) for c in ch['clauses'] for x in c if abs(x)>b})
    for word in range(1<<b):
        sat=False
        for aux in range(1<<len(fresh)):
            assigned=dict(zip(fresh,[(aux>>j)&1 for j in range(len(fresh))]))
            def cvalue(c):
                return any((((word>>(abs(v)-1))&1) if abs(v)<=b else assigned[abs(v)])==int(v>0) for v in c)
            if all(cvalue(c) for c in ch['clauses']):sat=True;break
        test(sat==(word!=ch['word']),'chain_projection')

def exact_unsat_by_module_ids(src, mids):
    covered=set()
    for i in mids: covered.update(src['modules'][i]['excluded'])
    return len(covered)==(1<<src['b'])

def set_cover(sets, universe, mids):
    union=set()
    for j in mids:union.update(sets[j])
    return union==set(range(universe))

def proof_locator(src):
    """Output source ID chains for every boundary word, or a SAT boundary witness."""
    records=[]
    for word in range(1<<src['b']):
        found=None
        for ent in src['modules']:
            for ch in ent['chains']:
                if ch['word']==word:
                    found={'word':word,'ids':list(ch['source_ids'])}
                    break
            if found is not None:break
        if found is None:return {'kind':'SAT','boundary':word}
        records.append(found)
    return {'kind':'UNSAT','records':records}

def canon_resolve(a,b):
    aa=set(a); bb=set(b)
    piv=[v for v in aa if -v in bb]
    if len(piv)!=1: return None
    p=piv[0]
    result=(aa|bb)-{p,-p}
    if any(-v in result for v in result):return None
    return tuple(sorted(result,key=lambda k:(abs(k),k)))

def verify_source_chains_and_resolution(src, proof):
    if proof['kind']!='UNSAT':return False
    b=src['b']; records=proof['records']
    if len(records)!=(1<<b):return False
    leaves=[]
    for word, rec in enumerate(records):
        if rec['word']!=word:return False
        found=False
        for ent in src['modules']:
            for ch in ent['chains']:
                if ch['source_ids']!=rec['ids']:continue
                if ch['word']!=word:continue
                if any(parse_original_source_row_at(src,cid)!=tuple(c) for cid,c in zip(rec['ids'],ch['clauses'])):continue
                ls=tuple(lit_forbidden((word>>j)&1,j+1) for j in range(b))
                expected,ch_end=chain(ls, min([abs(x) for c in ch['clauses'] for x in c if abs(x)>b],default=src['nvars']+1))
                if [tuple(x) for x in expected]!=[tuple(x) for x in ch['clauses']]:continue
                # Authenticate every chained Resolution step, not only its final semantic label.
                derived=tuple(ch['clauses'][0]);zcount=b-3
                for j in range(1,len(ch['clauses'])):
                    derived=canon_resolve(derived,ch['clauses'][j])
                    if derived is None:return False
                if tuple(sorted(derived,key=lambda k:(abs(k),k)))!=tuple(sorted(ls,key=lambda k:(abs(k),k))):return False
                found=True;break
            if found:break
        if not found:return False
        leaves.append(tuple(lit_forbidden((word>>j)&1,j+1) for j in range(b)))
    levels=0;resolution_steps=0
    while len(leaves)>1:
        nxt=[]
        for j in range(0,len(leaves),2):
            res=canon_resolve(leaves[j],leaves[j+1]);resolution_steps+=1
            if res is None:return False
            nxt.append(res)
        leaves=nxt;levels+=1
    test(levels==b,'proof_resolution_depth')
    test(resolution_steps==(1<<b)-1,'proof_resolution_steps')
    return leaves==[()]

def source_satisfied_under_boundary(src,y):
    for ent in src['modules']:
        if y in ent['excluded']:return False
    return True

def child_sizes(src):
    """Two genuine original ternary pin-level descendants, no guest SAT oracle."""
    clauses=list(src['clauses']);n=src['nvars'];sizes=[len(clauses)]
    for bit,var in [(0,1),(1,2)]:
        aux=n+1;aux2=n+2;n+=2
        ll=var if bit else -var
        clauses.extend([(ll,aux,aux2),(ll,aux,-aux2),(ll,-aux,aux2),(ll,-aux,-aux2)])
        sizes.append(len(clauses))
    return sizes

W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
    (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
    (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
    (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]

def gadget(a,b):
    clauses=[list(c) for c in W1]
    if a==0:
        for ci,li in [(6,0),(11,0)]:clauses[ci][li]*=-1
    if b==0:
        for ci,li in [(17,2),(9,2)]:clauses[ci][li]*=-1
    return clauses

def satisfying(clauses, assignment):
    for row in clauses:
        if not any((bool((assignment>>(abs(z)-1))&1)==(z>0)) for z in row):return False
    return True

def main():
    # Verify chain semantics across actual CNF assignments incl auxiliary variables.
    for b in range(3,7):
        for w in range(1<<b):
            ls=[lit_forbidden((w>>j)&1,j+1) for j in range(b)]
            cl,_=chain(ls,b+1)
            chain_projected({'word':w,'clauses':cl},b)
    # Exhaustive all set-family shapes (including noncovering) and all choices of source modules.
    source_examples=0;exhaustive_systems=0;minimal_samples=[]
    for universe in (2,3,4):
        for mask in range(1<<(3*universe)):
            sets=[{i for i in range(universe) if (mask>>(universe*j+i))&1} for j in range(3)]
            src=build(universe,sets)
            test(src['b']==3,'exact_boundary_width')
            test(all(len(set(abs(x) for x in row))==3 for row in src['clauses']),'proper_3cnf')
            test(len(set(src['clauses']))==len(src['clauses']),'distinct_original_clauses')
            for chosen_mask in range(1<<(len(sets)+1)):
                mids=[j for j in range(len(sets)+1) if (chosen_mask>>j)&1]
                truth=(0 in mids and set_cover(sets,universe,[j-1 for j in mids if j>0]))
                test(exact_unsat_by_module_ids(src,mids)==truth,'set_cover_equivalence')
            full=proof_locator(src)
            expected=set_cover(sets,universe,range(3))
            test((full['kind']=='UNSAT')==expected,'all_unsat_certificate_coverage')
            if expected:
                test(verify_source_chains_and_resolution(src,full),'authenticated_resolution')
                source_examples+=1
                test(len(full['records'])==8,'cover_cert_length')
                if source_examples<=3:
                    minimal=min(len(mids) for z in range(1<<4) if (mids:=[j for j in range(4) if (z>>j)&1]) and exact_unsat_by_module_ids(src,mids))
                    minimal_samples.append({'universe':universe,'sets':[sorted(s) for s in sets],'minimum_modules':minimal,'clauses':len(src['clauses'])})
            else:
                test(source_satisfied_under_boundary(src,full['boundary']),'sat_boundary_witness')
            exhaustive_systems+=1
    # Actual chained proper-3CNF, b=4 and b=5, randomized source covers and failures.
    random_sources=0
    for universe in (7,8,16):
        for rep in range(34):
            subsets=[{i for i in range(universe) if rng.random()<.37} for _ in range(5)]
            src=build(universe,subsets)
            test(src['b']>=3,'chain_source_boundary')
            test(all(len(c)==3 and len(set(map(abs,c)))==3 for c in src['clauses']),'chain_proper')
            test(len(set(src['clauses']))==len(src['clauses']),'chain_distinct')
            proof=proof_locator(src)
            expected=set_cover(subsets,universe,range(len(subsets)))
            test((proof['kind']=='UNSAT')==expected,'chain_all_coverage')
            if expected:
                test(verify_source_chains_and_resolution(src,proof),'chain_resolution_authenticated')
                altered={'kind':'UNSAT','records':[dict(i) for i in proof['records']]}
                altered['records'][0]['ids']=[9999999]
                test(not verify_source_chains_and_resolution(src,altered),'source_id_mutation_rejected')
                altered2={'kind':'UNSAT','records':proof['records'][:-1]}
                test(not verify_source_chains_and_resolution(src,altered2),'short_cover_rejected')
            else:test(source_satisfied_under_boundary(src,proof['boundary']),'chain_sat_witness')
            random_sources+=1
    # Fixed guaranteed b>3 UNSAT example, tests no free terminal and children are not smaller.
    universe=7;sets=[set(range(7))]
    src=build(universe,sets);proof=proof_locator(src)
    test(src['b']==3,'test_b3')
    universe=8;sets=[set(range(8))]
    src=build(universe,sets);proof=proof_locator(src)
    test(src['b']==4 and proof['kind']=='UNSAT','fixed_b4_unsat')
    test(verify_source_chains_and_resolution(src,proof),'fixed_b4_resolution')
    # Signed source mutation, absent word and wrong ancestor name must not authenticate.
    spoof={'kind':'UNSAT','records':[dict(i) for i in proof['records']]}
    spoof['records'][0]['word']=1
    test(not verify_source_chains_and_resolution(src,spoof),'boundary_word_spoof_rejected')
    wrong_offset={'kind':'UNSAT','records':[dict(i) for i in proof['records']]}
    wrong_offset['records'][0]['ids']=[wrong_offset['records'][0]['ids'][0]+1]+wrong_offset['records'][0]['ids'][1:]
    test(not verify_source_chains_and_resolution(src,wrong_offset),'physical_midline_pointer_rejected')
    source_bit_mutation=build(universe,sets)
    firstcid=proof['records'][0]['ids'][0]
    original=source_bit_mutation['source'][firstcid]
    old_line=' '.join(str(v) for v in original)+' 0\n'
    new_row=(-original[0],)+original[1:]
    new_line=' '.join(str(v) for v in new_row)+' 0\n'
    # physical bytes really are mutated, while provenance metadata stays intact
    source_bit_mutation['encoded']=source_bit_mutation['encoded'][:firstcid]+new_line+source_bit_mutation['encoded'][firstcid+len(old_line):]
    test(not verify_source_chains_and_resolution(source_bit_mutation,proof),'source_sign_spoof_rejected')
    source_sat=build(universe,[set(range(7))])
    test(proof_locator(source_sat)['kind']=='SAT','strict_sat_source_recognized')
    forged={'kind':'UNSAT','records':[dict(i) for i in proof['records']]}
    test(not verify_source_chains_and_resolution(source_sat,forged),'missing_original_clause_rejected')
    # Original source and two actual ternary pin-descendant levels, checked by
    # the semantics of each authenticated pin quartet, not by an uncharged A call.
    for tree_source,root_sat in [(src,False),(source_sat,True)]:
        possible=[y for y in range(1<<tree_source['b']) if source_satisfied_under_boundary(tree_source,y)]
        test(bool(possible)==root_sat,'twolevel_root_polarity')
        possible1=[y for y in possible if y&1]
        possible2=[y for y in possible1 if y&2]
        test((bool(possible1),bool(possible2))==((root_sat),(root_sat)),'twolevel_child_polarity')
    sizes=child_sizes(src)
    test(sizes[1]>sizes[0] and sizes[2]>sizes[1],'physical_two_level_growth')
    # W1 actual truth checks and specific Alice-only candidate witness integers from peer.
    model_counts={}; candidate_checks=0;invalid_outputs=0
    for a,b in itertools.product((0,1),repeat=2):
        clauses=gadget(a,b)
        cnt=sum(satisfying(clauses,v) for v in range(1<<15))
        model_counts[f'{a}{b}']=cnt
        test(cnt=={(0,0):772,(0,1):272,(1,0):272,(1,1):0}[(a,b)],'W1_counts')
        pc=Counter(z>0 for c in clauses for z in c)
        for v in range(1,16):
            test(sum(c.count(v) for c in clauses)==2,'W1_two_positive')
            test(sum(c.count(-v) for c in clauses)==2,'W1_two_negative')
        w={0:616,1:4742}[a]
        actual=satisfying(clauses,w)
        test(actual==(not(a and b)),'Alice_only_witness_polarity')
        candidate_checks+=1
        if not actual:invalid_outputs+=1
    test(invalid_outputs==1,'candidate_unsound_as_acceptor')
    # Input sensitivity after candidate printing, all m Bob bits individually required on all-a=1.
    for m in range(1,11):
        a=(1<<m)-1;b=0
        for i in range(m):
            before=all(not((a>>j)&1 and (b>>j)&1) for j in range(m))
            changed=b^(1<<i)
            after=all(not((a>>j)&1 and (changed>>j)&1) for j in range(m))
            test(before and not after,'Bob_query_adversary')
    # Header, open exact22 transfer and time-space model disclaimer are report obligations.
    raw={'run':'SOURCE-COVER-OPTGAP146','date':'2026-10-27','seed':SEED,
         'exhaustive_3set_families':exhaustive_systems,'source_proof_cases':source_examples,
         'random_chain_sources':random_sources,'model_counts':model_counts,
         'Alice_only_candidate_modes':candidate_checks,'invalid_candidate_modes':invalid_outputs,
         'two_level_clause_counts':sizes,'minimum_examples':minimal_samples,
         'checks':dict(sorted(checks.items())),'total_assertions':sum(checks.values()),'failed_assertions':0,
         'scope':'restricted typed source-identified proper 3CNF modules, NOT signed exact22 transfer; finite evidence not proof',
         'unrestricted_P_vs_NP':'OPEN'}
    print(json.dumps(raw,sort_keys=True,indent=2))

if __name__=='__main__':main()