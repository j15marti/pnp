#!/usr/bin/env python3
"""GATE295 source-authenticated exact 9-variable domination-cache control."""
import itertools,json
from collections import Counter
F=[[1,4,7],[1,5,7],[2,3,9],[2,4,6],[3,5,8],[6,8,9],
[-1,-4,-8],[-1,-5,-7],[-2,-3,-9],[-2,-4,-6],[-3,-5,-7],[-6,-8,-9]]
N=9
def gram():
    h=Counter(); seen=set()
    assert len(F)*3==4*N
    for c in F:
        assert len(c)==3 and len(set(map(abs,c)))==3
        assert len({v>0 for v in c})==1
        key=tuple(sorted(c))
        assert key not in seen
        seen.add(key);h.update(c)
    assert all(h[i]==h[-i]==2 for i in range(1,N+1))
def sat(a):
    return all(any(a[abs(v)]==(v>0) for v in c) for c in F)
def main():
    gram()
    P={frozenset(c) for c in F if c[0]>0}
    Q={frozenset(-v for v in c) for c in F if c[0]<0}
    H=P&Q; B=sorted(set().union(*H))
    U=[c for c in F if frozenset(abs(v) for v in c) not in H]
    assert len(U)==4 and len(B)==9
    def factor(p):
        free=[x for x in B if x not in p]
        for bits in itertools.product([False,True],repeat=len(free)):
            w=dict(p);w.update(zip(free,bits))
            if all(0<sum(w[x] for x in tri)<3 for tri in H): return w
        return None
    equal={}; models=[];nogoods=[]
    coh=eq_calls=dom_calls=dom_hits=0
    for sel in itertools.product(range(3),repeat=len(U)):
        p={};bad=False
        for c,j in zip(U,sel):
            lit=c[j];x=abs(lit);value=lit>0
            if x in p and p[x]!=value:bad=True;break
            p[x]=value
        if bad:continue
        coh+=1
        key=tuple(sorted((x,v) for x,v in p.items() if x in B))
        if key not in equal:
            equal[key]=factor(dict(key));eq_calls+=1
        answer=None
        for w in models:
            if all(w[x]==v for x,v in key):
                answer=w;dom_hits+=1;break
        if answer is None and not any(all(dict(key).get(x)==v for x,v in q.items()) for q in nogoods):
            answer=factor(dict(key));dom_calls+=1
            if answer is None: nogoods.append(dict(key))
            else:models.append(answer)
        assert (answer is not None)==(equal[key] is not None)
        if answer is not None:
            full={i:False for i in range(1,N+1)}
            full.update(answer);full.update(p)
            assert sat(full)
    m=sum(sat({i:bool(mask>>(i-1)&1) for i in range(1,N+1)}) for mask in range(1<<N))
    assert (coh,eq_calls,dom_calls,dom_hits,m)==(32,32,11,21,88)
    print(json.dumps({'coherent':coh,'equal_factor_calls':eq_calls,
        'dominance_factor_calls':dom_calls,'dominance_hits':dom_hits,
        'complete_source_models':m,'r':len(U),'B':len(B)},indent=2))
if __name__=="__main__":main()
