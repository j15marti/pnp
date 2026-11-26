from fg16 import *

# Physical-height cover: after pinning one RHS of each minority atom,
# reflect if needed, and solve only monotone upper bounds.
def cover_plan(D,atoms,kind):
    fixed={i for i in range(len(D)) if D[0,i]==-D[i,0]}
    E={(u,w) for k,v,u,c,w,d in atoms if k!=kind and u not in fixed and w not in fixed}
    W={i:int(D[0,i]+D[i,0]+1) for i in range(len(D))}
    R=set(E);S=set()
    while R:
        u,v=min(R);S.update([u,v]);R={p for p in R if not set(p)&{u,v}}
    R=set(E);Q=set()
    while R:
        counts=collections.Counter(i for p in R for i in p)
        u=min(counts,key=lambda i:(-counts[i],W[i],i));Q.add(u);R={p for p in R if u not in p}
    L=min([sorted(S),sorted(Q)],key=lambda s:(prod(W[i] for i in s),s))
    return prod(W[i] for i in L),kind,L

def monotone_mixed(D,atoms,kind):
    C=D.T if kind=='min' else D
    if kind=='min':atoms=[('max' if k=='min' else 'min',v,u,-c,w,-d) for k,v,u,c,w,d in atoms]
    lo=-C[:,0];hi=C[0,:];h=hi.copy();fixed={i:int(hi[i]) for i in range(len(h)) if hi[i]==lo[i]}
    while True:
        old=h.copy();h=np.minimum(h,np.min(h[:,None]+C,axis=0))
        for k,v,u,c,w,d in atoms:
            if k=='max':h[v]=min(h[v],max(h[u]+c,h[w]+d))
            else:
                if u not in fixed:u,w,c,d=w,u,d,c
                assert u in fixed
                if h[v]<fixed[u]+c:h[w]=min(h[w],h[v]-d)
        if np.any(h<lo):return None
        if np.array_equal(h,old):return -h if kind=='min' else h

def solve_cover(D,atoms,cap=4096):
    D,atoms=simplify(D,atoms)
    if D is None:return 'NO',None,{'budget':0,'leaves':0}
    cost,kind,L=min(cover_plan(D,atoms,k) for k in ('min','max'))
    meta={'budget':cost,'leaves':0,'cover':L,'polarity':kind,'atoms':len(atoms)}
    if cost>cap:return 'UNKNOWN',None,meta
    for vals in it.product(*(range(-int(D[i,0]),int(D[0,i])+1) for i in L)):
        C=D
        for i,val in zip(L,vals):
            C=pin(C,0,i,val)
            if C is not None:C=pin(C,i,0,-val)
            if C is None:break
        if C is None:continue
        meta['leaves']+=1;h=monotone_mixed(C,atoms,kind)
        if h is not None:
            assert np.all(h[None,:]-h[:,None]<=D)
            assert all((h[v]<=max(h[u]+c,h[w]+d) if k=='max' else h[v]>=min(h[u]+c,h[w]+d)) for k,v,u,c,w,d in atoms)
            return 'YES',h,meta
    return 'NO',None,meta

def main():
    # Reuse exact FG16 test harness with cover solver; all original-reference checks repeated.
    import fg16
    fg16.solve_comparisons=solve_cover
    fg16.main()
    import os;os.rename('fg16_results.json','cover_results.json')
    # Distinct comparison pairs with a common central height, all offsets zero.
    stars=[]
    for n in [8,16,32,64,128]:
        D=np.full((n+4,n+4),4,dtype=np.int64);np.fill_diagonal(D,0);D[0,:]=2;D[:,0]=2;D[0,0]=0
        A=[(k,v,1,0,u,0) for u in range(4,n+4) for k,v in [('min',2),('max',3)]]
        s,h,m=solve_cover(D,A);t,g,j=solve_comparisons(D,A)
        assert s=='YES' and (t=='YES' if j['budget']<=4096 else t=='UNKNOWN')
        stars.append({'pairs':n,'cover':m,'comparison':j,'cover_status':s,'comparison_status':t})
    json.dump(stars,open('cover_stars.json','w'),indent=2);print('stars',stars)
if __name__=='__main__':main()
