#!/usr/bin/env python3
"""Matched-scope high-treewidth SAT/UNSAT strict exact(2,2)-3CNF families.
Independent implementation of the composition in CONNECTED-AND-CONNECTOR231.
All finite truth tables and model verification are executed from raw clauses.
Requires only Python 3 standard library; deterministic seed, no SAT oracle.
Run: python 2026-10-29_1414_LSPV-2_MATCHED_TORUS_BRIDGE232_repro.py > results.json
"""
import json, random, hashlib, itertools
from collections import Counter, defaultdict

W1 = [
(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
G = [tuple(-l if abs(l)==4 and i in (6,11) else l for l in clause)
     for i,clause in enumerate(W1)]
# A DIFFERENT balanced two-sign flip from the supplied 60-mutation control.
# This v9 mutation preserves BOTH signed component-size spectra of W1.
V = [tuple(-l if abs(l)==9 and i in (4,11) else l for l in clause)
     for i,clause in enumerate(W1)]

def sat_clause(clause, valuation):
    return any(valuation[abs(l)] == int(l>0) for l in clause)

def sat_formula(clauses, valuation):
    return all(sat_clause(c,valuation) for c in clauses)

def from_bits(mask,n):
    return {i+1:(mask>>i)&1 for i in range(n)}

def all_models(clauses,n):
    return [mask for mask in range(1<<n) if sat_formula(clauses,from_bits(mask,n))]

def verify_strict(cs,n):
    assert len(cs)*3 == n*4, (len(cs),n)
    occ=Counter(l for c in cs for l in c)
    assert all(occ[x]==occ[-x]==2 for x in range(1,n+1))
    assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in cs)
    assert set(abs(x) for c in cs for x in c)==set(range(1,n+1))
    assert len(cs)==len(set(tuple(sorted(c)) for c in cs))
    byvar=defaultdict(list)
    for j,c in enumerate(cs):
        for l in c:byvar[abs(l)].append(j)
    seen_v={1};seen_c=set();stack=[1]
    while stack:
        x=stack.pop()
        for c_id in byvar[x]:
            seen_c.add(c_id)
            for l in cs[c_id]:
                y=abs(l)
                if y not in seen_v:seen_v.add(y);stack.append(y)
    assert len(seen_v)==n and len(seen_c)==len(cs)

def torus(L):
    assert L>=6 and L%6==0
    n=L*L
    var=lambda r,c: 1+(r%L)*L+(c%L)
    clauses=[]
    for r in range(L):
        for offset in (0,1):
            for j in range(L//3):
                clauses.append(tuple(var(r,offset+3*j+t) for t in range(3)))
    for c in range(L):
        for offset in (0,1):
            for j in range(L//3):
                clauses.append(tuple(-var(offset+3*j+t,c) for t in range(3)))
    verify_strict(clauses,n)
    witness={var(r,c):int(r%3==c%3) for r in range(L) for c in range(L)}
    assert sat_formula(clauses,witness)
    # Every grid adjacent pair must belong to a source clause.
    edges={tuple(sorted((abs(a),abs(b)))) for c in clauses for a,b in itertools.combinations(c,2)}
    for r in range(L):
        for c in range(L):
            assert tuple(sorted((var(r,c),var(r+1,c)))) in edges
            assert tuple(sorted((var(r,c),var(r,c+1)))) in edges
    return clauses,witness

def shift(cs,d):
    return [tuple((1 if l>0 else -1)*(abs(l)+d) for l in c) for c in cs]

def first_negative(cs):
    return next((j,k,abs(l)) for j,c in enumerate(cs) for k,l in enumerate(c) if l<0)

def connector(a,b):
    na=max(abs(l) for c in a for l in c)
    nb=max(abs(l) for c in b for l in c)
    verify_strict(a,na);verify_strict(b,nb)
    A=list(a);B=shift(b,na)
    ai,ak,x=first_negative(A)
    bi,bk,y=first_negative(B)
    g1_offset=na+nb
    g2_offset=g1_offset+15
    C1=shift(G,g1_offset)
    C2=shift(G,g2_offset)
    g1p,g2p=g1_offset+4,g2_offset+4
    g1u,g2u=g1_offset+8,g2_offset+8
    # Full-preserving negative incidence exchanges, no SAT answer consulted.
    A[ai]=tuple(-g1p if k==ak else v for k,v in enumerate(A[ai]))
    B[bi]=tuple(-g2p if k==bk else v for k,v in enumerate(B[bi]))
    C1[4]=tuple(-x if k==0 else v for k,v in enumerate(C1[4]))
    C2[4]=tuple(-y if k==0 else v for k,v in enumerate(C2[4]))
    C1[6]=tuple(-g2u if k==1 else v for k,v in enumerate(C1[6]))
    C2[6]=tuple(-g1u if k==1 else v for k,v in enumerate(C2[6]))
    out=A+B+C1+C2
    verify_strict(out,na+nb+30)
    return out, {'n_a':na,'n_b':nb,'a_port':(ai,ak,x),'b_port':(bi,bk,y),
                 'g1_offset':g1_offset,'g2_offset':g2_offset,'total_variables':na+nb+30}

def interface_a(cs,port,valuation):
    i,k,x=port
    return int(any(valuation[abs(l)]==int(l>0) for j,l in enumerate(cs[i]) if j!=k))

def independent_profile():
    full_counts={};counts={};samples={}
    mask_valuations=[from_bits(mask,15) for mask in range(1<<15)]
    reduced=[m for m,v in enumerate(mask_valuations) if sat_formula([c for i,c in enumerate(G) if i not in (4,6)],v)]
    for x,a in itertools.product((0,1),repeat=2):
        bucket=Counter()
        for m in reduced:
            v=mask_valuations[m]
            if (not x or sat_clause((-9,-11),v)) and (not v[4] or a):
                u=int(not v[8])
                w=int((not v[4]) or (not v[11]))
                bucket[(u,w)]+=1
                samples.setdefault((x,a,u,w),m)
        counts[(x,a)]=bucket
        full_counts[f'{x}{a}']={f'{u}{w}':c for (u,w),c in sorted(bucket.items())}
    expected={'00':{'01':153},'01':{'00':178,'01':153,'10':170,'11':34},
              '10':{},'11':{'00':25,'10':85,'11':34}}
    assert full_counts==expected,(full_counts,expected)
    # Purely Boolean composition, all 16 input pairs, independently of any source models.
    for x,a,y,b in itertools.product((0,1),repeat=4):
        possible=any((w1 or u2) and (w2 or u1)
            for u1,w1 in counts[(x,a)] for u2,w2 in counts[(y,b)])
        assert possible==bool((not x or a) and (not y or b))
    return full_counts,samples,{'G_models':sum(sat_formula(G,v) for v in mask_valuations),
                                'W1_models':sum(sat_formula(W1,v) for v in mask_valuations),
                                'reduced_G_models':len(reduced),'input_pairs':16}

def lift_sat_witness(a,b,wa,wb,info,samples):
    pa=info['a_port'];pb=info['b_port']
    va={**wa,**{i+info['n_a']:bit for i,bit in wb.items()}}
    x=wa[pa[2]];a0=interface_a(a,pa,wa)
    y=va[pb[2]];b0=interface_a(shift(b,info['n_a']),pb,va)
    g1mask=next(m for (xx,aa,u,v),m in samples.items() if xx==x and aa==a0 and v==1)
    g2mask=next(m for (yy,bb,u,v),m in samples.items() if yy==y and bb==b0 and v==1)
    for offset,mask in [(info['g1_offset'],g1mask),(info['g2_offset'],g2mask)]:
        va.update({offset+i:(mask>>(i-1))&1 for i in range(1,16)})
    return va

def gf2_rank(cs,n,select='all'):
    basis={}
    for c in cs:
        mask=0
        for lit in c:
            if select=='all' or (select=='positive' and lit>0) or (select=='negative' and lit<0):
                mask ^= 1<<(abs(lit)-1)
        while mask:
            j=mask.bit_length()-1
            if j not in basis: basis[j]=mask;break
            mask^=basis[j]
    return len(basis)

def dimacs_bits(cs,n):
    s=f'p cnf {n} {len(cs)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in cs)
    return 8*len(s.encode('ascii'))

def clause_distribution(cs):
    return dict(sorted(Counter(str(sum(l>0 for l in c)) for c in cs).items()))

def frontier(cs,n):
    # Source-declared row-major ordering, applies to arbitrary additional gadgets.
    neigh=[set() for _ in range(n+1)]
    for c in cs:
        for x in c:
            neigh[abs(x)].update(abs(y) for y in c if abs(y)!=abs(x))
    maxfront=0
    for split in range(1,n):
        front=sum(any(v>split for v in neigh[x]) for x in range(1,split+1))
        maxfront=max(maxfront,front)
    return maxfront

def random_recode_pair(sat,unsat,n,seed):
    rng=random.Random(seed)
    perm=list(range(1,n+1));rng.shuffle(perm)
    flip={i:rng.randint(0,1) for i in range(1,n+1)}
    ix=list(range(len(sat)));rng.shuffle(ix)
    out=[]
    for cs in (sat,unsat):
        transformed=[]
        for j in ix:
            lits=[(1 if ((l>0)^bool(flip[abs(l)])) else -1)*perm[abs(l)-1] for l in cs[j]]
            transformed.append(tuple(lits))
        out.append(transformed)
    return out,perm,flip

def signed_clause_components(cs,n,polarity):
    """Clauses are vertices; each signed twice-occurring variable is an edge."""
    assert polarity in (-1,+1)
    edges=defaultdict(list)
    for j,c in enumerate(cs):
        for l in c:
            if (l>0)==(polarity>0):
                edges[abs(l)].append(j)
    assert len(edges)==n and all(len(es)==2 for es in edges.values())
    adj=[set() for _ in cs]
    for a,b in edges.values():
        adj[a].add(b);adj[b].add(a)
    unseen=set(range(len(cs)));components=0
    while unseen:
        components+=1
        stack=[unseen.pop()]
        while stack:
            for v in adj[stack.pop()]:
                if v in unseen: unseen.remove(v); stack.append(v)
    return components

def component_sizes(adj,marked=None):
    unseen=set(range(len(adj)));sizes=[];marked_size=None
    while unseen:
        seed=unseen.pop();stack=[seed];size=0;hit=False
        while stack:
            x=stack.pop();size+=1;hit |= (x==marked)
            for y in adj[x]:
                if y in unseen:unseen.remove(y);stack.append(y)
        sizes.append(size)
        if hit:marked_size=size
    return tuple(sorted(sizes)),marked_size

def signed_clause_spectrum(cs,n,polarity):
    occ=defaultdict(list)
    for j,c in enumerate(cs):
        for l in c:
            if (l>0)==(polarity>0):occ[abs(l)].append(j)
    assert len(occ)==n and all(len(z)==2 for z in occ.values())
    adj=[set() for _ in cs]
    for i,j in occ.values():adj[i].add(j);adj[j].add(i)
    return component_sizes(adj)[0]

def core_negative_components(source,return_spectrum=False):
    """Fixed 61-vertex quotient of the bridge negative-clause graph.
    Contract the touched torus column to node 60; all other torus clauses
    are removed after accounting for their independent components.
    """
    K=list(source);Q1=shift(G,15);Q2=shift(G,30)
    # Source K is represented on variables 1..15, guards on 16..45.
    ci,sl,y=first_negative(K)
    assert (ci,sl,y)==(0,0,1)
    K[ci]=tuple(-34 if j==sl else v for j,v in enumerate(K[ci]))
    # Guard1 D has port x=46; guard2 D has y=1.
    Q1[4]=tuple(-46 if j==0 else v for j,v in enumerate(Q1[4]))
    Q2[4]=tuple(-1 if j==0 else v for j,v in enumerate(Q2[4]))
    # Cross exchange of g8 negative occurrences.
    Q1[6]=tuple(-38 if j==1 else v for j,v in enumerate(Q1[6]))
    Q2[6]=tuple(-23 if j==1 else v for j,v in enumerate(Q2[6]))
    nodes=K+Q1+Q2
    assert len(nodes)==60
    occ=defaultdict(list)
    for j,c in enumerate(nodes):
        for lit in c:
            if lit<0: occ[abs(lit)].append(j)
    for v in range(1,47):
        # x=46 and first guard p1=19 have one occurrence in the core;
        # their other occurrences are in the touched torus column.
        if v in (19,46):
            assert len(occ[v])==1
            occ[v].append(60)
        else:
            assert len(occ[v])==2,(v,occ[v])
    adj=[set() for _ in range(61)]
    for a,b in occ.values():adj[a].add(b);adj[b].add(a)
    sizes,t_size=component_sizes(adj,60)
    return (sizes,t_size) if return_spectrum else len(sizes)

def core_positive_spectrum(source):
    """Component sizes of all 60 core clause vertices in positive graph."""
    K=list(source);Q1=shift(G,15);Q2=shift(G,30)
    ci,slot,y=first_negative(K)
    assert (ci,slot,y)==(0,0,1)
    K[ci]=tuple(-34 if j==slot else v for j,v in enumerate(K[ci]))
    Q1[4]=tuple(-46 if j==0 else v for j,v in enumerate(Q1[4]))
    Q2[4]=tuple(-1 if j==0 else v for j,v in enumerate(Q2[4]))
    Q1[6]=tuple(-38 if j==1 else v for j,v in enumerate(Q1[6]))
    Q2[6]=tuple(-23 if j==1 else v for j,v in enumerate(Q2[6]))
    nodes=K+Q1+Q2
    positive=defaultdict(list)
    for j,c in enumerate(nodes):
        for l in c:
            if l>0:positive[l].append(j)
    assert len(positive)==45 and all(len(z)==2 for z in positive.values())
    adj=[set() for _ in nodes]
    for i,j in positive.values():adj[i].add(j);adj[j].add(i)
    return component_sizes(adj)[0]

def run():
    tables,samples,prof=independent_profile()
    assert prof['G_models']==272 and prof['W1_models']==0
    baseline=next(from_bits(mask,15) for mask in range(1<<15) if sat_formula(G,from_bits(mask,15)))
    core_sat=core_negative_components(V);core_unsat=core_negative_components(W1)
    assert (core_sat,core_unsat)==(19,19)
    core_neg_sat=core_negative_components(V,True);core_neg_unsat=core_negative_components(W1,True)
    assert core_neg_sat==core_neg_unsat
    core_pos_sat=core_positive_spectrum(V);core_pos_unsat=core_positive_spectrum(W1)
    assert core_pos_sat==core_pos_unsat
    # Positive core consists of all 60 source/guard clauses; no torus-positive
    # occurrence is touched by the all-negative bridge.
    Vmodels=all_models(V,15)
    assert len(Vmodels)==54 and Vmodels[0]==616
    out={'constant_negative_core_components':{'SAT':core_sat,'UNSAT':core_unsat},
         'constant_negative_core_distinguished_size':core_neg_sat[1],
         'constant_negative_core_size_histogram':dict(sorted(Counter(core_neg_sat[0]).items())),
         'constant_positive_core_size_histogram':dict(sorted(Counter(core_pos_sat).items())),
         'source_mutation_V':{'variable':9,'flipped_clauses':[4,11],
             'models':len(Vmodels),'first_model':Vmodels[0]},
         'source_gadget':prof,'table':tables,'reference_sha':'ddfea2285320d3143ac653986e708d562ecabde6',
         'seed':20261029,'cases':[]}
    for L in (6,12,18,24):
        T,wT=torus(L)
        SAT,meta=connector(T,V)
        UNSAT,metaU=connector(T,W1)
        assert meta==metaU
        n=meta['total_variables'];m=len(SAT)
        assert n==L*L+45 and m==(4*L*L)//3+60
        assert len(SAT)==len(UNSAT)
        assert all(tuple(map(abs,c))==tuple(map(abs,d)) for c,d in zip(SAT,UNSAT))
        differences=[(i,j,SAT[i][j],UNSAT[i][j]) for i in range(m) for j in range(3)
                     if SAT[i][j]!=UNSAT[i][j]]
        assert len(differences)==2 and {abs(x[2]) for x in differences}=={L*L+9}
        assert {x[2] for x in differences}=={L*L+9,-(L*L+9)}
        witness=lift_sat_witness(T,V,wT,from_bits(Vmodels[0],15),meta,samples)
        assert len(witness)==n and sat_formula(SAT,witness)
        assert sat_formula(T,wT) and sat_formula(V,from_bits(Vmodels[0],15))
        assert not all_models(W1,15)
        # Original torus has only one altered vertical clause, column of its negative port.
        port_col=(meta['a_port'][2]-1)%L
        scopes={tuple(sorted((abs(c[i]),abs(c[j])))) for c in SAT for i,j in ((0,1),(0,2),(1,2))}
        def var(r,c):return 1+r*L+c
        kept_cols=[c for c in range(L) if c!=port_col]
        kept_rows=list(range(L-1))
        for r in kept_rows:
            for c,d in zip(kept_cols,kept_cols[1:]):
                assert tuple(sorted((var(r,c),var(r,d)))) in scopes
        for r,s in zip(kept_rows,kept_rows[1:]):
            for c in kept_cols:
                assert tuple(sorted((var(r,c),var(s,c)))) in scopes
        metrics={
            'L':L,'n':n,'m':m,'original_torus_n':L*L,
            'same_unsigned_scopes':True,'sign_differences':differences,
            'SAT_model_checked':True,'UNSAT_by_fixed_gadget_truth_table':True,
            'certified_grid_side':L-1,'certified_treewidth_lower_bound':L-2,
            'row_major_frontier_torus':frontier(T,L*L),
            'row_major_frontier_join':frontier(SAT,n),
            'unsigned_scope_rank':gf2_rank(SAT,n),
            'unsigned_dependency_excess':m-gf2_rank(SAT,n),
            'negative_components_SAT':signed_clause_components(SAT,n,-1),
            'negative_spectrum_identical':signed_clause_spectrum(SAT,n,-1)==signed_clause_spectrum(UNSAT,n,-1),
            'positive_spectrum_identical':signed_clause_spectrum(SAT,n,+1)==signed_clause_spectrum(UNSAT,n,+1),
            'clause_polarity_histogram_identical':clause_distribution(SAT)==clause_distribution(UNSAT),
            'negative_components_UNSAT':signed_clause_components(UNSAT,n,-1),
            'positive_components_SAT':signed_clause_components(SAT,n,+1),
            'positive_components_UNSAT':signed_clause_components(UNSAT,n,+1),
            'positive_rank_SAT':gf2_rank(SAT,n,'positive'),
            'positive_rank_UNSAT':gf2_rank(UNSAT,n,'positive'),
            'negative_rank_SAT':gf2_rank(SAT,n,'negative'),
            'negative_rank_UNSAT':gf2_rank(UNSAT,n,'negative'),
            'positive_clause_count_SAT':clause_distribution(SAT),
            'positive_clause_count_UNSAT':clause_distribution(UNSAT),
            'physical_dimacs_bits_SAT':dimacs_bits(SAT,n),
            'physical_dimacs_bits_UNSAT':dimacs_bits(UNSAT,n)
        }
        assert metrics['negative_spectrum_identical']
        assert metrics['positive_spectrum_identical']
        assert metrics['clause_polarity_histogram_identical']
        assert metrics['negative_components_SAT']==2*L*L//3+(L-1)+core_sat
        assert metrics['negative_components_UNSAT']==2*L*L//3+(L-1)+core_unsat
        assert metrics['positive_components_SAT']==m-metrics['positive_rank_SAT']
        assert metrics['positive_components_UNSAT']==m-metrics['positive_rank_UNSAT']
        assert metrics['negative_components_SAT']==m-metrics['negative_rank_SAT']
        assert metrics['negative_components_UNSAT']==m-metrics['negative_rank_UNSAT']
        if L in (6,12):
            recoded,perm,flip=random_recode_pair(SAT,UNSAT,n,20261029+L)
            for zz in recoded:verify_strict(zz,n)
            rp=[(i,j) for i in range(m) for j in range(3) if recoded[0][i][j]!=recoded[1][i][j]]
            assert len(rp)==2
            wrec={perm[i-1]:int(b^flip[i]) for i,b in witness.items()}
            assert sat_formula(recoded[0],wrec)
            metrics['adversarial_permutation_complement_checks']=True
            metrics['adversarial_hamming_sign_slots']=len(rp)
        out['cases'].append(metrics)
    return out

if __name__=='__main__':
    data=run()
    print(json.dumps(data,indent=2,sort_keys=True))
