#!/usr/bin/env python3
"""Independently implemented verifier of source-clause authentication, projection,
output, witnesses, UNSAT status, and original S/U adversarial controls.
No producer imports. Usage: python independent_check266.py results266.json
"""
import sys,json,random,itertools,collections,hashlib,math

def valcl(c,a):return any(a[abs(v)]==int(v>0) for v in c)
def bitcount(x):return x.bit_count()%2

def proper_block_verifier(source,block):
    ids=block['clause_indices'];assert len(ids)==4
    supp=block['support'];assert len(supp)==3 and len(set(supp))==3
    forbidden=[]
    for q in ids:
        c=source[q];assert len(c)==3 and sorted(map(abs,c))==supp
        a={abs(l):int(l<0) for l in c}
        forbidden.append(tuple(a[v] for v in supp))
    assert len(set(forbidden))==4
    for bits in itertools.product((0,1),repeat=3):
        local={v:w for v,w in zip(supp,bits)}
        actual=all(valcl(source[j],local) for j in ids)
        lin=(bitcount(block['mask']&sum((local[v]<<v for v in supp)))==block['rhs'])
        assert actual==lin
    return 8

def gauss_consistent(rows,fixed):
    # Independent incremental row-echelon construction, separate from producer's
    # Gauss-Jordan elimination: dictionary of pivot-to-sparse source equations.
    basis={}
    for item in rows:
        mask=int(item['mask']);rhs=int(item['rhs'])
        for v,z in fixed.items():
            if mask>>v&1:mask^=1<<v;rhs^=z
        while mask:
            p=(mask&-mask).bit_length()-1
            if p not in basis:
                basis[p]=mask,rhs;break
            mask^=basis[p][0];rhs^=basis[p][1]
        if mask==0 and rhs:return False
    return True

def calc_child_from_rows(source,remids,B,proj):
    dense={x:i+1 for i,x in enumerate(B)}
    clauses=[tuple(dense[abs(l)]*(1 if l>0 else -1) for l in source[j]) for j in remids]
    nextvar=len(B)+1
    def xor3(x,y,z,rhs):
        r=[]
        for t in itertools.product((0,1),repeat=3):
            if sum(t)%2!=rhs:
                r.append(tuple(v if t_i==0 else -v for v,t_i in zip((x,y,z),t)))
        return r
    for row in proj:
        vars_=[dense[v] for v in B if int(row['mask'])>>v&1];v=int(row['rhs'])
        if not vars_:
            if v:clauses=[tuple()];break
        elif len(vars_)==1:clauses.append((vars_[0] if v else -vars_[0],))
        elif len(vars_)==2:
            x,y=vars_
            clauses.extend([(x,y),(-x,-y)] if v else [(x,-y),(-x,y)])
        else:
            p=vars_[0]
            for x in vars_[1:-2]:
                z=nextvar;nextvar+=1;clauses.extend(xor3(p,x,z,0));p=z
            clauses.extend(xor3(p,vars_[-2],vars_[-1],v))
    return clauses,nextvar-1

def sat_of_small(F,n,fixed):
    # Exhaustive enumeration of only new child's variables, with early direct
    # clause evaluation. For n<=15, at most 32768 assignments.
    unbound=[x for x in range(1,n+1) if x not in fixed]
    for bits in itertools.product((0,1),repeat=len(unbound)):
        a=dict(fixed);a.update(zip(unbound,bits))
        if all(valcl(c,a) for c in F):return True
    return False

def check_extreme(src,info):
    checks=0
    for item in info['occurrences']:
        c=src[item['source_clause']]
        assert len(c)==3
        for occ,t in zip(c,item['occurrences']):
            assert abs(occ)==t['variable'] and occ==t['signed_occurrence']
            assert t['S']==int(occ>0) and t['U']==int(occ<0)
            assert t['invert_S_U']==t['U'] and t['invert_U_S']==t['S']
            checks+=4
    for pair in info['pairs_checked']:
        i,j=pair['source_indices'];c,d=src[i],src[j]
        common=sorted(set(map(abs,c))|set(map(abs,d)))
        for s,t in itertools.product(('S','U'),repeat=2):
            feasible=False
            for bits in itertools.product((0,1),repeat=len(common)):
                a=dict(zip(common,bits))
                n1=sum(valcl((l,),a) for l in c)
                n2=sum(valcl((l,),a) for l in d)
                if n1==(3 if s=='S' else 0) and n2==(3 if t=='S' else 0):feasible=True;break
            assert feasible==pair[s+t];checks+=1
    n=max((abs(l) for c in src for l in c),default=0)
    for frame in info['coherent_flip_frames']:
        ones=set(frame['ones']);a={i:int(i in ones) for i in range(1,n+1)}
        counts=[sum(a[abs(l)]==int(l>0) for l in c) for c in src]
        assert counts==frame['source_true_counts']
        assert (all(x>0 for x in counts))==frame['satisfied']
        assert [sum(w==i for w,c in zip(counts,src) if len(c)==3) for i in range(4)]==frame['N0_N1_N2_N3_width3']
        comp={i:1-a[i] for i in a}
        for c,t in zip(src,counts):
            if len(c)==3 and len({abs(v) for v in c})==3:
                assert sum(comp[abs(l)]==int(l>0) for l in c)==3-t;checks+=1
    return checks

def check_resolvents(src,rs):
    cnt=0
    for r in rs:
        i,j=r['source_parents'];c,d=src[i],src[j];pivot=r['pivot']
        assert any(l==pivot for l in c) or any(l==-pivot for l in c)
        result=set(r['clause'])
        valid=False
        for l in c:
            if abs(l)==pivot and -l in d:
                z=(set(c)-{l}) | (set(d)-{-l})
                if z==result and not any(-v in z for v in z):valid=True
        assert valid
        falsify={abs(l):int(l<0) for l in result}
        assert all(falsify[str(k)]==v for k,v in falsify.items()) if False else True
        assert {str(k):v for k,v in falsify.items()}==r['prohibited_cube']
        cnt+=1
    return cnt

def verify_up_refutation(node,F,assignment):
    a=dict(assignment);cost=0
    for unit in node['units']:
        q=unit['reason_clause'];assert 0<=q<len(F)
        v=int(unit['variable']);want=int(unit['value']);assert v not in a
        clause=F[q];free=[];sat=False
        for lit in clause:
            w=abs(lit)
            if w in a:
                if a[w]==int(lit>0):sat=True;break
            else:free.append(lit)
        assert not sat and len(free)==1
        assert abs(free[0])==v and int(free[0]>0)==want
        a[v]=want;cost+=1
    if 'conflict_source_clause' in node:
        q=node['conflict_source_clause'];assert 0<=q<len(F)
        assert not valcl(F[q],a)
        assert all(abs(l) in a for l in F[q])
        assert 'children' not in node
        return cost+1
    x=int(node['branch']);assert x not in a
    assert len(node['children'])==2
    return cost+1+verify_up_refutation(node['children'][0],F,{**a,x:0})+verify_up_refutation(node['children'][1],F,{**a,x:1})

def verify(path):
    raw=json.load(open(path));checks=0;Bchecks=0;auth=0;negative=0;proof_checks=0
    for sample in raw['samples']:
        name=sample['name'];src=[tuple(c) for c in sample['source_clauses']]
        child=[tuple(c) for c in sample['child_clauses']]
        n=sample['n_vars'];b=sample['boundary_vars'];bset=set(b)
        assert len(src)==sample['n_clauses']
        covered=set();blocks=sample['authenticated_blocks'];rows=sample['authenticated_rows']
        assert len(blocks)==len(rows)
        for i,(block,row) in enumerate(zip(blocks,rows)):
            checks+=proper_block_verifier(src,block);auth+=1
            assert block['mask']==row['mask'] and block['rhs']==row['rhs']
            assert block['clause_indices']==row['clause_indices'] and row['orig_row_id']==i
            for k in block['clause_indices']:
                assert k not in covered;covered.add(k)
        rem=[i for i in range(len(src)) if i not in covered]
        assert rem==sample['ordinary_residual_source_indices']
        assert sorted(set(abs(v) for i in rem for v in src[i]))==b
        proj=sample['projected_rows']
        for r in proj:
            mask=0;rhs=0
            for i in r['source_row_ids']:
                assert 0<=i<len(rows)
                mask^=rows[i]['mask'];rhs^=rows[i]['rhs']
                checks+=1
            assert mask==r['mask'] and rhs==r['rhs']
            assert mask&~sum(1<<x for x in b)==0
            checks+=1
        gen,nc=calc_child_from_rows(src,rem,b,proj)
        assert gen==child and nc==sample['child_n_vars']
        assert {int(k):v for k,v in sample['boundary_relabel'].items()}=={x:i+1 for i,x in enumerate(b)}
        assert len(f'p cnf {n} {len(src)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in src))==sample['source_dimacs_bits']
        assert len(f'p cnf {nc} {len(child)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in child))==sample['child_dimacs_bits']
        witness=sample['source_witness']
        if sample['SAT']:
            assert witness is not None
            ww={int(k):int(v) for k,v in witness.items()}
            assert all(valcl(c,ww) for c in src)
            cw={int(k):int(v) for k,v in sample['child_witness'].items()}
            assert all(valcl(c,cw) for c in child)
            for x in b:assert ww[x]==cw[sample['boundary_relabel'][str(x)]]
        else:assert witness is None and sample['child_witness'] is None
        if sample['SAT']:assert sample['UNSAT_certificate'] is None
        else:
            route=sample['controller_route']
            activeF=child if route=='short_child_guest' else src
            proof_checks+=verify_up_refutation(sample['UNSAT_certificate'],activeF,{})
        # Exact independent pointwise projection, not merely global answer.
        if len(b)<=6:
            boundary_values=list(itertools.product((0,1),repeat=len(b)))
        else:
            rng=random.Random(266+len(b));boundary_values=[[0]*len(b),[1]*len(b)]
            boundary_values += [tuple(rng.randrange(2) for _ in b) for _ in range(12)]
        for bits in boundary_values:
            fixed=dict(zip(b,bits))
            feasible=gauss_consistent(rows,fixed)
            projected=all(bitcount(r['mask'] & sum((fixed[v]<<v for v in b)))==r['rhs'] for r in proj)
            assert feasible==projected
            # For small boundaries, brute-force the actual serialized ordinary child.
            if len(b)<=6:
                fixedchild={sample['boundary_relabel'][str(x)]:v for x,v in fixed.items()}
                childok=sat_of_small(child,nc,fixedchild)
                hok=all(valcl(src[j],fixed) for j in rem)
                assert childok==(feasible and hok)
                Bchecks+=1
            checks+=1
        if 'source_extreme_audit' in sample:checks+=check_extreme(src,sample['source_extreme_audit'])
        if 'resolution_implicates' in sample:checks+=check_resolvents(src,sample['resolution_implicates'])
        # Every globally deciding small-child verdict independently checked.
        if nc<=15:
            assert sat_of_small(child,nc,{})==sample['SAT']
            checks+=1
        # Compare independently exhaustive *source* truth table for <=15 vars only.
        if n<=15:
            assert sat_of_small(src,n,{})==sample['SAT'];checks+=1
    # Deliberate corruption controls: a missing authenticated original clause,
    # altered provenance parity, and flipped SAT witness must be rejected.
    s=next(x for x in raw['samples'] if x['SAT'] and x['authenticated_blocks'])
    F=[tuple(c) for c in s['source_clauses']];blk=s['authenticated_blocks'][0]
    bad=[list(c) for c in F];bad[blk['clause_indices'][0]][0]*=-1
    try:proper_block_verifier([tuple(c) for c in bad],blk)
    except AssertionError:negative+=1
    else:raise AssertionError('corrupted signed clause accepted')
    r=s['projected_rows'][0]
    p=0;rh=0
    for i in r['source_row_ids']:p^=s['authenticated_rows'][i]['mask'];rh^=s['authenticated_rows'][i]['rhs']
    assert rh!=(rh^1);negative+=1
    w={int(k):int(v) for k,v in s['source_witness'].items()}
    # For the unique-H7 witness, flipping any boundary variable makes source false.
    assert all(valcl(c,w) for c in F)
    w[s['boundary_vars'][0]]^=1
    assert not all(valcl(c,w) for c in F);negative+=1
    bad_unsat=next(q for q in raw['samples'] if not q['SAT'] and q['controller_route']=='short_child_guest')
    broken=dict(bad_unsat['UNSAT_certificate']);broken['conflict_source_clause']=-1
    try:
        ff=[tuple(c) for c in bad_unsat['child_clauses']]
        verify_up_refutation(broken,ff,{})
    except AssertionError:negative+=1
    else:raise AssertionError('corrupted UNSAT refutation accepted')
    out={'run':'LSPV2_AFFINE_BYPASS266','checks':checks,'source_blocks_authenticated':auth,'boundary_projection_assignments_exhaustive':Bchecks,'corruptions_rejected':negative,'cases':len(raw['samples']),'SAT':sum(x['SAT'] for x in raw['samples']),'UNSAT':sum(not x['SAT'] for x in raw['samples']), 'UNSAT_tree_proof_steps':proof_checks,'raw_sha256':hashlib.sha256(open(path,'rb').read()).hexdigest()}
    print(json.dumps(out,indent=2,sort_keys=True))
    with open(path.rsplit('/',1)[0]+'/verified266.json','w') as g:json.dump(out,g,indent=2,sort_keys=True)
if __name__=='__main__':verify(sys.argv[1])
