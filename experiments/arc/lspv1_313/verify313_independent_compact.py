#!/usr/bin/env python3
"""No-producer-import independent verifier of canonical source controls for LSPV1_313."""
import itertools as it, json, collections, sys
F9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]
Y6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
def valid(F,n):
    ids=collections.Counter()
    if len(F)*3!=n*4 or len(set(map(lambda c:tuple(sorted(c)),F)))!=len(F):return False
    for c in F:
        if len(c)!=3 or len(set(abs(v) for v in c))!=3:return False
        if min(abs(v) for v in c)<1 or max(abs(v) for v in c)>n:return False
        if len(set(v>0 for v in c))>1:return False
        for v in c:ids[abs(v),v>0]+=1
    return all(ids[v,s]==2 for v in range(1,n+1) for s in (False,True))
def sat_count(F,n,p):
    answer=0
    for bits in it.product((0,1),repeat=n):
        a={v:bits[v-1] for v in range(1,n+1)}
        if any(a[v]!=bit for v,bit in p.items()):continue
        answer+=all(any(a[abs(x)]==int(x>0) for x in clause) for clause in F)
    return answer
def connected_source(t):
    F=[]
    for block in range(t):
        for j,clause in enumerate(F9):
            if j==0:F.append((9*block+1,9*block+6,9*((block+1)%t)+5))
            else:F.append(tuple((1 if x>0 else -1)*(9*block+abs(x)) for x in clause))
    return F
def path_ok(F,t):
    blocks=[set(range(9*i+1,9*i+10)) for i in range(t)]
    bags=[blocks[0]|blocks[i]|blocks[i+1] for i in range(t-1)]
    if any(not any(set(abs(x) for x in c)<=bag for bag in bags) for c in F):return False
    for x in range(1,9*t+1):
        j=[i for i,b in enumerate(bags) if x in b]
        if not j or j[-1]-j[0]+1!=len(j):return False
    return max(map(len,bags))-1<=26
def source_extremes(F,n):
    all_a=[dict(zip(range(1,n+1),z)) for z in it.product((0,1),repeat=n)]
    cnt=0
    for i,j in it.combinations(range(len(F)),2):
        for mode in it.product((0,1),repeat=2):
            need={};can=True
            for clause,flag in zip((F[i],F[j]),mode):
                for lit in clause:
                    v=abs(lit);bit=int((lit>0)==bool(flag))
                    if v in need and need[v]!=bit:can=False
                    need[v]=bit
            actual=any(all(sum(a[abs(x)]==int(x>0) for x in clause)==3*flag
                         for clause,flag in zip((F[i],F[j]),mode)) for a in all_a)
            assert actual==can
            cnt+=1
    return cnt
def main():
    assert valid(F9,9) and valid(Y6,6) and not valid(F9[:-1],9)
    labels={'F9_root':sat_count(F9,9,{}),'F9_gap':sat_count(F9,9,{5:0,7:0}),
        'F9_S':sat_count(F9,9,{1:0,3:0,5:1,6:0,7:0,8:0}),
        'F9_U':sat_count(F9,9,{1:1,3:0,5:1,6:0,7:0,8:0}),
        'Y6_root':sat_count(Y6,6,{})}
    G2=connected_source(2)
    labels['G2_AZ']=sat_count(G2,18,{5:1})
    labels['G2_BQ']=sat_count(G2,18,{5:1,4:0,6:0,10:0,14:0,15:0})
    assert labels=={'F9_root':70,'F9_gap':13,'F9_S':2,'F9_U':0,'Y6_root':20,
                    'G2_AZ':2377,'G2_BQ':0}
    for t in (2,3,4,8,16):
        assert valid(connected_source(t),9*t) and path_ok(connected_source(t),t)
    modes=source_extremes(F9,9)+source_extremes(Y6,6)
    assert modes==376
    print(json.dumps({'status':'PASS','no_producer_import':True,'original_models':labels,
        'SU_modes':modes,'connected_bag_controls':5},indent=2))
if __name__=='__main__':main()
