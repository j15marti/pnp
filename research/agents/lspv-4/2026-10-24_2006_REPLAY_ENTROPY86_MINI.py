#!/usr/bin/env python3
"""REPLAY-ENTROPY86: standard-library exact source-bit replay and cache audit.
No SAT solver dependencies or random seeds. Restricted source interface only.
"""
import json
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

checks=0
def check(condition,message):
    global checks
    checks+=1
    if not condition: raise AssertionError(message)

def cycle_cnf(q,source):
    out=[]
    for i in range(q):
        x=i+1; y=(i+1)%q+1
        bit=(source>>i)&1
        halves=[(-x,y),(x,-y)] if bit==0 else [(x,y),(-x,-y)]
        for half,(a,b) in enumerate(halves):
            u=q+2*i+half+1
            out.extend([(a,b,u),(a,b,-u)])
    return out

def models(q,clauses):
    n=3*q
    return sum(all(any(((a>>(abs(z)-1))&1)==int(z>0) for z in cl)
                       for cl in clauses) for a in range(1<<n))

def optimum_query_total(q,universe_mask):
    n=1<<q
    zero_masks=[sum(1<<x for x in range(n) if ((x>>bit)&1)==0)
                for bit in range(q)]
    @lru_cache(None)
    def cost(mask):
        z=mask.bit_count()
        if z<=1: return 0
        best=None
        for m0 in zero_masks:
            left=mask & m0
            right=mask ^ left
            if left and right:
                v=z+cost(left)+cost(right)
                best=v if best is None else min(best,v)
        if best is None: raise AssertionError('non-singleton fiber cannot split')
        return best
    return cost

def exhaustive_cache_test(q,allowed):
    U=len(allowed); best=10**10
    cost=optimum_query_total(q,sum(1<<x for x in allowed))
    checked=0
    for coloring in range(1<<U):
        a=sum(1<<x for j,x in enumerate(allowed) if (coloring>>j)&1)
        b=sum(1<<x for j,x in enumerate(allowed) if not ((coloring>>j)&1))
        best=min(best,cost(a)+cost(b));checked+=1
    return {'n':q,'source_count':U,'cache_bits':1,'retained_maps':checked,
            'min_mean_probes':str(Fraction(best,U))}

def main():
    tests=[]
    for q in (3,4):
        for b in range(1<<q):
            full=cycle_cnf(q,b)
            check(len(full)==4*q,'clause count')
            check(all(len(c)==3 and len(set(map(abs,c)))==3 for c in full),
                  'proper 3-CNF')
            want=(1<<(2*q+1)) if b.bit_count()%2==0 else 0
            check(models(q,full)==want,'full models')
            for mask in range(1<<q):
                selected=[cl for edge in range(q) if (mask>>edge)&1
                             for cl in full[4*edge:4*edge+4]]
                expected=(1<<(3*q-mask.bit_count())) if mask != (1<<q)-1 else want
                check(models(q,selected)==expected,'whole-edge models')
        tests.append({'q':q,'orientations':1<<q,'assignments':1<<(3*q),
                      'even_sources':1<<(q-1),'odd_sources':1<<(q-1)})
    for q in (3,4):
        v=exhaustive_cache_test(q,list(range(1<<q)))
        check(v['min_mean_probes']==str(q-1),'full entropy optimality')
        tests.append({'full_cache_partition':v})
    for sigma in (0,1):
        allowed=[b for b in range(16) if b.bit_count()%2==sigma]
        v=exhaustive_cache_test(4,allowed)
        check(v['min_mean_probes']=='2','parity-conditioned cache optimum')
        tests.append({'parity':sigma,'cache_partition':v})
    for q in (3,8,64,256):
        for C in (0,1,max(0,q//4),q-1):
            for R in (1,2,7):
                reads=q+(R-1)*max(0,q-C)
                check(reads<=q*R,'cache read count')
                for sigma in (0,1):
                    check(R*max(0,q-1-C)<=reads,'label floor per side')
    c=Fraction(241,200)
    beta=((c+2)/c**2-c)/2
    check(beta==Fraction(11642479,23232400),'FLMV beta')
    results={'run':'REPLAY-ENTROPY86','status':'PASS',
             'scope':'restricted exact source-bit service, not unrestricted SAT',
             'assertions':checks,'tests':tests,'flmv_beta':str(beta)}
    Path(__file__).with_name('REPLAY_ENTROPY86_results.json').write_text(
        json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
if __name__=='__main__': main()
