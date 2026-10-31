#!/usr/bin/env python3
"""Independent finite checker: direct bit-mask truth tables; avoids importing producer."""
import json,sys,random,math
from fractions import Fraction
from collections import Counter

def check_clause(cl,mask):
    return any(((mask>>(abs(l)-1))&1)==int(l>0) for l in cl)
def label(clause_set,mask):return all(check_clause(c,mask) for c in clause_set)
def extreme(cl,mask):return sum((((mask>>(abs(l)-1))&1)==int(l>0)) for l in cl)

def check(dat):
    total=Counter()
    for case in dat['cases']:
        F=case['source_clauses'];n=case['n'];m=case['m'];models=[]
        for mask in range(1<<n):
            if label(F,mask):models.append(mask)
            co=(1<<n)-1-mask
            for cl in F:
                assert extreme(cl,mask)+extreme(cl,co)==3
                total['complements']+=1
        assert len(models)==case['models']
        for target in case['targets']:
            j=target['j']-1
            for record in target['occurrences']:
                l=record['signed_literal']
                assert l in F[j] and record['i']==abs(l)
                assert (record['S'],record['invert_S'],record['U'],record['invert_U'])==(int(l>0),int(l<0),int(l<0),int(l>0))
                total['target_occurrences']+=1
        for pair in case['pair_modes']:
            i,j=(x-1 for x in pair['clauses']);A=F[i];B=F[j]
            v=sorted(set(map(abs,A+B)));expect=[]
            for u,vv in [(3,3),(3,0),(0,3),(0,0)]:
                found=False
                for bit in range(1<<len(v)):
                    mask=sum(((bit>>k)&1)<<(x-1) for k,x in enumerate(v))
                    if extreme(A,mask)==u and extreme(B,mask)==vv:
                        found=True;break
                expect.append(found)
            assert expect==[pair[z] for z in ['SS','SU','US','UU']]
            total['pair_modes']+=4
        for rec in case['endpoints_and_flips']:
            mask=rec['assignment_mask'];cc=[extreme(c,mask) for c in F]
            assert cc==rec['true_literal_counts']
            assert [cc.count(i) for i in range(4)]==rec['N0_to_N3']
            assert (0 not in cc)==rec['sat']
            total['flip_trail']+=1
        r=case['derived_forbidden_cube'];a,b=[F[x-1] for x in r['parents']];p=r['pivot'];
        assert any(x in a and -x in b or -x in a and x in b for x in [p])
        rr=set(a+b);rr.discard(p);rr.discard(-p)
        assert set(r['resolvent'])==rr and all(-x not in rr for x in rr)
        cube={int(k):v for k,v in r['forbidden_cube'].items()}
        assert cube=={abs(x):x<0 for x in rr}
        assert all(not all(((mask>>(k-1))&1)==int(v) for k,v in cube.items()) for mask in models)
        total['resolved_forbidden_cubes']+=1
        for partition in case['cofactor_partitions']:
            h=partition['h'];q=1<<h
            # Prove source-restriction identity against all global assignments for every leaf.
            for prefix in range(q):
                pins={k+1:(prefix>>(h-1-k))&1 for k in range(h)}
                rem=[];tests=0
                for cl in F:
                    vals=[pins.get(abs(l)) for l in cl]
                    if any(x is not None and x==int(l>0) for x,l in zip(vals,cl)):
                        continue
                    rem.append([l for l,x in zip(cl,vals) if x is None])
                for mask in range(1<<n):
                    if any(((mask>>(k-1))&1)!=v for k,v in pins.items()):continue
                    assert label(F,mask)==label(rem,mask)
                    total['cofactor_valuations']+=1
                if prefix<len(partition['leaves']):
                    row=partition['leaves'][prefix]
                    assert row['unhit_three_clauses']==sum(1 for cl in F if all(abs(l) not in pins for l in cl))
                    assert row['child_literal_count']==sum(len(c) for c in rem)
                    assert row['solver_sat']==any(label(F,x) and all(((x>>(k-1))&1)==v for k,v in pins.items()) for x in models)
                    total['solver_label_checks']+=1
            assert partition['observed']['sat']==bool(models)
        for block in case['all_leaf_partitions']:
            h=block['h'];rows=block['leaves'];assert len(rows)==2**h
            expected_sat=False; bits=0;visits=0
            for r in rows:
                pin={i+1:r['pin'][i]=='1' for i in range(h)}
                rem=[ [l for l in cl if abs(l) not in pin] for cl in F if not any(abs(l) in pin and pin[abs(l)]==(l>0) for l in cl) ]
                b=math.ceil(math.log2(n+1)); actual=sum(map(len,rem))*(b+1)
                assert r['materialized_child_bits']==actual
                assert r['long_clauses']==sum(1 for cl in F if all(abs(l) not in pin for l in cl))
                key=int(r['pin'],2) if h else 0
                sat=any(label(F,msk) and all(((msk>>(i-1))&1)==int(v) for i,v in pin.items()) for msk in models)
                assert r['guest_sat']==sat
                expected_sat |= sat; bits+=actual
                total['all_leaf_label_checks']+=1
            assert expected_sat==bool(models)
            assert bits==block['totals']['child_output_bits']
            assert bits>=block['totals']['output_lower_bound_bits']
        for block in case['adaptive_comb_partitions']:
            q=block['q']; assert len(block['leaf_depths'])==q
            assert block['leaf_depths']==list(range(1,q))+[q-1]
            assert sum(Fraction(1,2**d) for d in block['leaf_depths'])==1
            assert sum(block['all_child_bits'])==block['total_child_output_bits']
            assert all(x>=block['universal_all_leaf_lower_bits']/q for x in block['all_child_bits'])
            total['comb_labels']+=q
        total['source_label_checks']+=1
    for block in dat['scaled_combs']:
        q=block['q'];assert len(block['all_child_bits'])==q
        assert block['leaf_depths']==list(range(1,q))+[q-1]
        assert sum(Fraction(1,2**d) for d in block['leaf_depths'])==1
        assert all(x>=block['universal_all_leaf_lower_bits']/q for x in block['all_child_bits'])
        total['scaled_comb_trees']+=1
    for f in dat['flmv_exact']:
        c=Fraction(f['c']); rec=Fraction(1); best=Fraction(0); winner=0
        for k in range(1,f['tail_start_k']):
            rec=c*rec/(1+rec)
            d=min((1/rec-c)/k,c**(-k))
            if d>best:best=d;winner=k
        assert str(best)==f['maximum'] and winner==f['max_k']
        assert c**(-f['tail_start_k'])<best
        total['flmv_tail_certificates']+=1
    for x in dat['scaled_family']:
        n=x['n'];m=x['m'];N=x['fixed_width_bits_N'];b=(n+1).bit_length()-1 if (n+1)&n==0 else (n+1).bit_length()
        assert N==3*m*(b+1)
        d=x['max_short_leaf_depth'];q=x['polynomial_q_bound']
        assert 2**d<=q<2**(d+1)
        guaranteed=max(0,m-4*d)
        assert 3*(b+1)*guaranteed==x['guaranteed_direct_child_bits_lower']
        assert guaranteed==x['guaranteed_unhit_clauses']
        if x['copies']>=2:
            assert x['guaranteed_direct_child_bits_lower']**2 > N
        total['scaled_bounds']+=1
    rng=random.Random(264)
    for _ in range(2500):
        leaves=[]
        def visit(depth):
            if depth==10 or (depth>0 and rng.random()<0.53):
                leaves.append(depth);return
            visit(depth+1);visit(depth+1)
        visit(0)
        q=len(leaves)
        assert sum(Fraction(1,2**d) for d in leaves)==1
        assert min(leaves)<=math.floor(math.log2(q))
        H=sum(Fraction(d,2**d) for d in leaves)
        assert float(H)<=math.log2(q)+1e-9
        total['kraft_random_trees']+=1
    return dict(total)

if __name__=='__main__':
    p=sys.argv[1] if len(sys.argv)>1 else 'arc_kraft_cofactor264_raw.json'
    o=json.load(open(p));x=check(o);print(json.dumps({'status':'PASS','counts':x},indent=2))
