"""Exact fixed-pair affine response pooling, with guarded original ID lifts."""
from affine_chart import *

def affine_intersect(A,B):
    a,U=A;b,V=B;z=solve_span(U+V,a^b)
    if z is None:return None
    return a^combination(U,z&((1<<len(U))-1)),intersection(U,V)

def union_hull(W,modes):
    # Exact inclusion-exclusion for at most four cosets; never substitutes a hull.
    A=[(a,basis(W+U)) for a,U in modes]
    a=A[0][0];H=basis([v for _,U in A for v in U]+[a^b for b,_ in A])
    if any(len(U)==len(H) for _,U in A):return a,H
    total=0;cache={}
    for m in range(1,1<<len(A)):
        b=m&-m;i=b.bit_length()-1
        z=A[i] if m==b else (None if cache[m^b] is None else affine_intersect(A[i],cache[m^b]))
        cache[m]=z
        if z is not None:total+=(-1)**(m.bit_count()+1)*(1<<len(z[1]))
    return (a,H) if total==1<<len(H) else None

def group_modes(F,I):
    for mode in it.product(*(range(len(F[i])) for i in I)):
        a=0;U=[];ls=[]
        for i,b in zip(I,mode):
            v,B=F[i][b];a^=v;ls.append(len(B));U+=B
        yield (a,U,mode,ls)

def pooled_join(F,target,cap=8,max_pair_checks=2000):
    common=[basis(f[0][1]) if len(f)==1 else intersection(f[0][1],f[1][1]) for f in F]
    W=basis([v for C in common for v in C]);shift=0;pending=list(range(len(F)));hist=[];st=Counter(initial_common_rank=len(W))
    def absorb(I,z):
        nonlocal W,shift
        a,V=z;hist.append((I,W,shift));W=V;shift^=a
        for i in I:pending.remove(i)
    while True:
        progress=False
        for i in pending[:]:
            st['single_checks']+=1;z=affine_union(W,F[i])
            if z is not None:absorb((i,),z);progress=True
        if progress:continue
        # Pair scan is explicitly capped; no claim of completeness beyond the admitted chart.
        for I in it.combinations(pending,2):
            if st['pair_checks']>=max_pair_checks:break
            st['pair_checks']+=1;G=list(group_modes(F,I));z=union_hull(W,[(a,U) for a,U,b,L in G])
            if z is not None:absorb(I,z);st['pair_merges']+=1;progress=True;break
        if not progress:break
    st.update(absorbed=len(F)-len(pending),kernel=len(pending),final_rank=len(W))
    if len(pending)>cap:return 'UNKNOWN',None,dict(st)
    for a,U,mode,ls in group_modes(F,pending):
        st['branches']+=1;z=solve_span(W+U,target^shift^a)
        if z is None:continue
        chosen={};p=target;pos=len(W)
        def recover(I,mode,ls,z,pos):
            nonlocal p
            for i,b,l in zip(I,mode,ls):
                a,U=F[i][b];r=a^combination(U,(z>>pos)&((1<<l)-1));chosen[i]=(b,r);p^=r;pos+=l
        recover(pending,mode,ls,z,pos)
        for I,V,s in reversed(hist):
            for a,U,mode,ls in group_modes(F,I):
                z=solve_span(V+U,p^s^a)
                if z is not None:recover(I,mode,ls,z,len(V));break
            else:raise AssertionError('group reverse')
        z=solve_span([v for C in common for v in C],p);assert z is not None;pos=0
        for i,C in enumerate(common):
            b,r=chosen[i];chosen[i]=(b,r^combination(C,(z>>pos)&((1<<len(C))-1)));pos+=len(C)
        assert combination([r for b,r in chosen.values()],(1<<len(chosen))-1)==target
        assert all(solve_span(F[i][b][1],r^F[i][b][0]) is not None for i,(b,r) in chosen.items())
        return 'YES',chosen,dict(st)
    return 'NO',None,dict(st)

def full_binary(D):
    G=nx.Graph();G.add_edges_from((('y',y),('z',z)) for y,z in D);assert max(dict(G.degree()).values())<=2
    M0=pm(D);assert M0 is not None
    M1=pm(D,{e:int(e in set(M0)) for e in D});assert M1 is not None and set(M0)|set(M1)==set(D)
    return M0,M1

def hard_formula(k,unsat):
    # Same C05-01 selector adapter. All signal variables have both polarities.
    C=[];sol={0:0};v=1
    for j in range(k):
        y=v;v+=1;sol[y]=0
        for a,b in it.product((0,1),repeat=2):
            if (a,b)==(0,0) and not(unsat and j==0):continue
            z=v;v+=1;sol[z]=0
            for c in (0,1):C.append(((0,1-a),(y,1-b),(z,c)))
    return C,sol

def main():
    rng=random.Random(261126053);abstract=Counter();fixture=None
    for _ in range(600):
        n=rng.randrange(2,8);F=[]
        for i in range(rng.randrange(1,7)):
            F.append([(rng.randrange(1<<n),[rng.randrange(1<<n) for _ in range(rng.randrange(3))]) for _ in range(rng.randrange(1,3))])
        t=rng.randrange(1<<n);s0,_,st0=join(F,t,cap=6);s,w,st=pooled_join(F,t,cap=6);assert s==s0
        S={0}
        for f in F:
            R=set()
            for a,U in f:R|={a^combination(U,m) for m in range(1<<len(U))}
            S={x^y for x in S for y in R}
        assert (s=='YES')==(t in S)
        abstract[s]+=1;abstract['pair_merges']+=st.get('pair_merges',0)
        if st['kernel']<st0['kernel']:abstract['kernel_improved']+=1;fixture=fixture or dict(F=F,target=t,before=st0,after=st)
    native=[]
    for k in [4,5,7,8,13]:
        T,R=sphere(k);A,B,W,c=close(T,R);assert A==T and R==B and not W;D=pairs(A);X={v for c,v in B if c==0};target=(1<<len(X))-1
        records=[]
        for j in range(12 if k<13 else 8):
            M0=pm(D,{e:rng.randrange(1000000) for e in sorted(D)});M1=pm(D,{e:rng.randrange(1000000) for e in sorted(D)})
            F,lifts,groups=chart(D,M0,M1,X);s0,_,st0=join(F,target,cap=8);s,C,st=pooled_join(F,target,cap=8)
            if s0!='UNKNOWN':assert s==s0
            if s=='YES':w=lift_chart(F,lifts,C);assert verify(T,R,w)
            else:w=None
            records.append(dict(before=s0,after=s,stats_before=st0,stats_after=st,initial_deficiency=[fixed_hall(D,M,X) for M in (M0,M1)],witness=w,chart0=M0,chart1=M1))
        native.append(dict(k=k,m=len(T),trials=records));print('sphere',k,Counter(r['after'] for r in records),'pair gains',sum(r['stats_after']['kernel']<r['stats_before']['kernel'] for r in records),flush=True)
    # Same authenticated native selector source, not an abstract hardness claim.
    from c05_join import direct,modeword,native_lift
    hard=[];neighbors=[]
    for k in [1,2,4,8]:
        for no in (False,True):
            C,sol=hard_formula(k,no);T,R,fac,mode,M,tabs,fs,aa,bb,S,old=direct(C);D=pairs(T);X={v for c,v in R if c==0};M0,M1=full_binary(D);F,lifts,groups=chart(D,M0,M1,X);t=(1<<len(X))-1
            s0,_,st0=join(F,t,cap=8);assert st0['initial_common_rank']==0 and st0['absorbed']==0
            s,w,st=pooled_join(F,t,cap=8,max_pair_checks=300)
            hit=None if no else native_lift(T,R,tabs,modeword(fac,len(M),sol))
            # Exact formula: all four assignments forbidden in first NO unit; YES x=y=0.
            assert s!='YES' or not no;assert s!='NO' or no
            if s=='YES':assert verify(T,R,lift_chart(F,lifts,w))
            hard.append(dict(k=k,m=len(T),truth=not no,full_chart=True,status=s,stats_before=st0,stats_after=st,witness=hit))
            if not no:
                # Delete a singleton pair tuple of required x=0 mode, forces x=1 in cycle.
                yp,d=mode[0];e=next(e for e in D if yp<=e[0]<yp+d and e[0]==e[1] and len(D[e])==1);i=next(iter(D[e].values()));assert i in hit
                Q={j:t0 for j,t0 in T.items() if j!=i};assert all(any(r in rows(t0) for t0 in Q.values()) for r in R)
                A,B,W,cl=close(Q,R);assert A is not None # actual postclosure negative, from exact original clause reduction
                # If remaining projection has <=2 domains, exact complete chart after guard.
                D0=pairs(A);M0,M1=full_binary(D0);X0={v for c,v in B if c==0};F0,L0,G0=chart(D0,M0,M1,X0);s1,w1,st1=pooled_join(F0,(1<<len(X0))-1,cap=8,max_pair_checks=300);assert s1!='YES'
                neighbors.append(dict(k=k,m=len(T),deleted=i,SAT_witness=hit,NO_closure=cl,NO_live=len(A),NO_chart=s1,stats=st1))
            print('hard',k,no,len(T),st0['kernel'],st['kernel'],s,flush=True)
    out=dict(seed=261126053,abstract=dict(abstract),fixture=fixture,native=native,hard=hard,neighbors=neighbors)
    json.dump(out,open('pooled_results.json','w'),indent=2);print(abstract,'neighbors',len(neighbors))
if __name__=='__main__':main()
