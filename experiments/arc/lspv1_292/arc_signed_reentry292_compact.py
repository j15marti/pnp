#!/usr/bin/env python3
"""ARC-SIGNED-REENTRY-SLACK292 compact exact finite controls, stdlib only.
No guest A, no physical FLMV tape or general SAT complexity lower bound.
"""
import itertools,collections,math,json
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
Z=((1,2,4),(1,3,5),(2,3,6),(-1,-2,-7),(-1,-3,-8),(-2,-3,-9),
   (4,7,8),(5,7,9),(6,8,9),(-4,-5,-7),(-4,-6,-8),(-5,-6,-9))
S=((1,2,5),(2,3,6),(3,4,7),(4,1,8),(-1,-2,-9),(-2,-3,-10),(-3,-4,-11),
   (-4,-1,-12),(5,9,10),(6,10,11),(7,11,12),(8,12,9),
   (-9,-5,-6),(-10,-6,-7),(-11,-7,-8),(-12,-8,-5))
PU=(-1,-1,-1,0,0,0,1,1,1)
PS=(-1,-1,-1,0,0,0,0,1,1)
P12=(-1,-1,-1,-1,0,0,0,0,1,1,1,1)
def grammar(F,n):
    if n%3 or len(F)*3!=4*n:return False
    cnt=collections.Counter();seen=set()
    for c in F:
        if len(c)!=3 or len(set(map(abs,c)))!=3:return False
        if any(not 1<=abs(x)<=n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key);cnt.update(c)
    return all(cnt[x]==cnt[-x]==2 for x in range(1,n+1))
def stats(F,p):
    n=len(p);f=p.count(-1);u=[0,0]
    for c in F:
        if not any(p[abs(l)-1]==int(l>0) for l in c):
            u[int(c[0]>0)]+=1
    up,um=u[1],u[0];e=2*f-up-um
    child=3*((max(up,um)+1)//2)
    assert up>=2*n/3-2*p.count(1) and um>=2*n/3-2*p.count(0)
    assert child>=n-3*min(p.count(0),p.count(1))
    assert child-f>=f/2-3*e/4+3*abs(up-um)/4-1e-9
    return f,up,um,e,child
def holds(F,a):
    return all(any(a[abs(l)-1]==int(l>0) for l in c) for c in F)
def ext(F,p):
    free=[i for i,x in enumerate(p) if x<0]
    for vals in itertools.product((0,1),repeat=len(free)):
        a=list(p)
        for i,v in zip(free,vals):a[i]=v
        if holds(F,a):yield tuple(a)
def shifted(F,j):
    return tuple(tuple((1 if l>0 else -1)*(abs(l)+j) for l in c) for c in F)
def family(k,t):
    F=[];offset=0
    for _ in range(k):F+=shifted(S,offset);offset+=12
    F+=shifted(Z,offset);offset+=9
    for _ in range(t):F+=shifted(Y,offset);offset+=6
    return tuple(F)
def main():
    assert all(grammar(F,n) for F,n in ((Y,6),(Z,9),(S,12)))
    assert [sum(1 for _ in ext(F,(-1,)*n)) for F,n in ((Y,6),(Z,9),(S,12))]==[20,74,282]
    tests=0;strong={6:0,9:0}
    for F,n in ((Y,6),(Z,9)):
        for p in itertools.product((-1,0,1),repeat=n):
            f,up,um,e,ng=stats(F,p)
            assert ng>=3*math.ceil((up+um)/4)
            if ng>3*math.ceil((up+um)/4):strong[n]+=1
            tests+=1
    assert tests==20412 and strong=={6:82,9:5852}
    assert not list(ext(Z,PU)) and list(ext(Z,PS))
    assert len(list(ext(S,P12)))==2
    assert holds(Z,(1,1,0,0,0,0,0,1,1))
    assert holds(S,(0,1,0,1,0,0,0,0,1,1,1,1))
    fam=[]
    for k in (1,4,16,64,256):
        t=math.isqrt(k);F=family(k,t);n=12*k+9+6*t
        assert grammar(F,n)
        for name,pz,label in (('NO',PU,False),('YES',PS,True)):
            p=P12*k+pz+(-1,)*(6*t)
            f,up,um,e,ng=stats(F,p)
            assert bool(list(ext(Z,pz)))==label
            assert ng==6*k+6+6*t and ng-f==2*k+3
            assert e==4*t+(1 if label else 0)
            fam.append((k,t,name,n,f,e,ng))
    pairs=0
    for F in (Y,Z,S):
        for j,a in enumerate(F):
            for b in F[j+1:]:
                names=sorted({abs(l) for l in a+b})
                for am,bm in itertools.product((True,False),repeat=2):
                    demands={};compatible=True
                    for c,mode in ((a,am),(b,bm)):
                        for lit in c:
                            bit=int((lit>0)==mode);i=abs(lit)
                            if i in demands and demands[i]!=bit:compatible=False
                            demands[i]=bit
                    witness=False
                    for vals in itertools.product((0,1),repeat=len(names)):
                        q=dict(zip(names,vals))
                        if all(q[abs(l)]==int((l>0)==am) for l in a) and all(q[abs(l)]==int((l>0)==bm) for l in b):
                            witness=True;break
                    assert witness==compatible
                pairs+=1
    assert pairs==214
    print(json.dumps({'status':'PASS','P_vs_NP':'OPEN','partial_states':tests,
      'strict_polarity_improvement':strong,'original_pair_matrix_checks':pairs,
      'same_source_sat_unsat_families':fam,'source_model_counts':(20,74,282),
      'native_phys':'not measured'},sort_keys=True,indent=2))
if __name__=='__main__':main()
