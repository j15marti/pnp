from fg15 import *
from math import prod

# Atoms (kind,v,u,c,w,d) use actual h: h[v] <= max(...) or >= min(...).
def compile_atoms(D,edges,tables,splits):
    atoms=[]
    for i,tab in enumerate(tables):
        B=set(sum(splits[i],[]))
        for mask in map(frozenset,it.product(*splits[i])):
            if mask in tab or mask_pin(D,edges,B,mask) is None:continue
            if len(mask)!=2:return None
            e,f=sorted(mask);p,q,m=edges[e];r,s,n=edges[f]
            if p==r and q!=s:atoms.append(('max',p,q,-m,s,-n))
            elif q==s and p!=r:atoms.append(('min',q,p,m,r,n))
            else:
                a0,b0=splits[i]
                if len(a0)!=3 or len(b0)!=3 or mask!=frozenset([a0[1],b0[1]]):return None
                a,b,na,nb=[edges[e] for e in [a0[0],b0[0],a0[2],b0[2]]]
                if (a[2],b[2],na[2],nb[2])!=(0,0,1,1):return None
                if a[1]==b[1]==na[0]==nb[0]:
                    u,w,v,z=a[0],b[0],na[1],nb[1];kind='max'
                elif a[0]==b[0]==na[1]==nb[1]:
                    u,w,v,z=a[1],b[1],na[0],nb[0];kind='min'
                else:return None
                if D[v,z]>0 or D[z,v]>0:return None
                expected=((v,u,0),(z,w,0)) if kind=='max' else ((u,v,0),(w,z,0))
                if (edges[a0[1]],edges[b0[1]])!=expected:return None
                atoms.append((kind,v,u,0,w,0))
    return sorted(set((k,v,u,c,w,d) if u<=w else (k,v,w,d,u,c) for k,v,u,c,w,d in atoms))

def pure(D,atoms,kind):
    flip=kind=='min';C=D.T if flip else D;lo=-C[:,0];h=C[0,:].copy()
    while True:
        old=h.copy();h=np.minimum(h,np.min(h[:,None]+C,axis=0))
        for k,v,u,c,w,d in atoms:
            assert k==kind
            h[v]=min(h[v],max(h[u]+(-c if flip else c),h[w]+(-d if flip else d)))
        if np.any(h<lo):return None
        if np.array_equal(h,old):return -h if flip else h

def simplify(D,atoms):
    # Every conversion is logically equivalent under the current DBM.
    while True:
        old=len(atoms);remaining=[]
        for k,v,u,c,w,d in atoms:
            if D[w,u]<=d-c: a,b=(w,d) if k=='max' else (u,c)
            elif D[u,w]<=c-d: a,b=(u,c) if k=='max' else (w,d)
            else:remaining.append((k,v,u,c,w,d));continue
            D=pin(D,a,v,b) if k=='max' else pin(D,v,a,-b)
            if D is None:return None,[]
        atoms=remaining
        if len(atoms)==old:return D,atoms

def intervals(D,atoms,retained):
    pairs=collections.defaultdict(set)
    for k,v,u,c,w,d in atoms:
        if k!=retained:pairs[u,w].add(d-c)
    out=[]
    for (u,w),cuts in sorted(pairs.items()):
        lo,hi=-int(D[u,w]),int(D[w,u]);parts=[]
        for t in sorted(cuts):
            if lo<=t<hi:parts.append((lo,t));lo=t+1
        parts.append((lo,hi));out.append((u,w,parts))
    return out

def solve_comparisons(D,atoms,cap=4096):
    D,atoms=simplify(D,atoms)
    if D is None:return 'NO',None,{'budget':0,'leaves':0}
    choices=[(prod(len(p) for u,w,p in intervals(D,atoms,k)),k,intervals(D,atoms,k)) for k in ('max','min')]
    cost,kind,groups=min(choices,key=lambda a:(a[0],a[1]));meta={'budget':cost,'leaves':0,'atoms':len(atoms),'groups':len(groups),'polarity':kind}
    if cost>cap:return 'UNKNOWN',None,meta
    for pat in it.product(*(p for u,w,p in groups)):
        C=D
        for (u,w,_),(a,b) in zip(groups,pat):
            C=pin(C,w,u,b)
            if C is not None:C=pin(C,u,w,-a)
            if C is None:break
        if C is None:continue
        C,R=simplify(C,atoms)
        if C is None:continue
        assert all(k==kind for k,*_ in R);meta['leaves']+=1
        h=pure(C,R,kind)
        if h is not None:
            assert np.all(h[None,:]-h[:,None]<=D)
            assert all((h[v]<=max(h[u]+c,h[w]+d) if k=='max' else h[v]>=min(h[u]+c,h[w]+d)) for k,v,u,c,w,d in atoms)
            return 'YES',h,meta
    return 'NO',None,meta

def native_job(T,P,A,rs,full=True):
    edges,D=chart(A[2],A[3]);P=dict(P);orig=dict(P)
    while True:
        tab,P,_=local_close(T,P,A,rs)
        if tab is None:return {'status':'NO','stage':'local'}
        if full:
            p=forced(T,P,A)
            if p is None:return {'status':'NO','stage':'affine/projection'}
            if p!=P:P=p;continue
        D,_,_,_=consensus(D,edges,tab,A[4])
        if D is None:return {'status':'NO','stage':'DBM'}
        new=dict(P)
        for e,(p,q,m) in edges.items():
            a=m-int(D[p,q]);b=m+int(D[q,p]);assert 0<=a<=b<=1
            if a==b:new[e]=a
        if new!=P:P=new;continue
        break
    atoms=compile_atoms(D,edges,tab,A[4])
    if atoms is None:return {'status':'UNKNOWN','stage':'compiler'}
    s,h,meta=solve_comparisons(D,atoms)
    result={'status':s,'stage':'comparison','pins':len(P),**meta}
    if s=='YES':
        w=lift(edges,h,tab,A,T,P);assert w is not None and verify(T,len(T)//3,orig,w)
        assert all(frozenset(w&A[5][i][1]) in S for i,S in rs.items());result['witness']=sorted(w)
    return result

def restrictions(A,exclusions):
    R={}
    for e,f in exclusions:
        i=next(i for i,(_,B,W) in enumerate(A[5]) if {e,f}<=B)
        R.setdefault(i,{w&A[5][i][1] for w in A[5][i][2]}).discard(frozenset([e,f]))
    return R

def main():
    rng=random.Random(26112616);out={'seed':26112616,'native':[],'abstract':[],'scales':[]}
    # Same FG15 UNKNOWN guards; all five original hull/cycle declines.
    for k in [3,4]:
        T,*_=mesh(k);A=acquire(T)
        for v in json.load(open('fg15_results.json'))['native']:
            if v.get('k')!=k or v.get('status')!='UNKNOWN':continue
            P={int(j):b for j,b in v['source_pins'].items()};rs={int(i):{frozenset(z) for z in S} for i,S in v['mode_tables'].items()}
            z=native_job(T,P,A,rs,full=True);z.update(k=k,case_id=v['case_id'],reference=v['reference'],kind='FG15 revisit');assert z['status']==v['reference'];out['native'].append(z)
    # SW11 exact original IDs; independent exhaustive macro enumeration.
    T,*_=mesh(2);A=acquire(T);bad=[[2,19],[1,20],[0,18],[56,74],[109,127],[108,126],[163,182]]
    for name,E in [('SW11 negative',bad),('SW11 neighbor',[p for p in bad if p!=[56,74]])]:
        rs=restrictions(A,E);tables=[{w&B for w in W if i not in rs or w&B in rs[i]} for i,(S,B,W) in enumerate(A[5])]
        count=0
        for masks in it.product(*tables):
            S=set().union(*masks);count+=int(len({A[2][e][1] for e in S})==len(S)==len(A[3]))
        z=native_job(T,{},A,rs);z.update(kind=name,tuples=len(T),macro_patterns=count,exclusions=E);assert z['status']==('YES' if count else 'NO');out['native'].append(z)
    # Random bounded integer systems, exact brute independent of DBM and pure solver.
    for _ in range(500):
        n=5;B=2;D=np.full((n,n),2*B,dtype=np.int64);np.fill_diagonal(D,0);D[0,:]=B;D[:,0]=B;D[0,0]=0
        raw=[]
        for j in range(rng.randrange(5)):
            u,v=rng.sample(range(n),2);c=rng.randrange(-2,3);raw.append((u,v,c));D0=pin(D,u,v,c)
            if D0 is None:D=None;break
            D=D0
        if D is None:continue
        atoms=[]
        for j in range(rng.randrange(1,12)):
            v,u,w=rng.sample(range(n),3);c,d=rng.randrange(-2,3),rng.randrange(-2,3)
            if u>w:u,w,c,d=w,u,d,c
            atoms.append((rng.choice(['min','max']),v,u,c,w,d))
        ans=any(all(h[v]-h[u]<=c for u,v,c in raw) and all(h[v]<=max(h[u]+c,h[w]+d) if k=='max' else h[v]>=min(h[u]+c,h[w]+d) for k,v,u,c,w,d in atoms) for rest in it.product(range(-B,B+1),repeat=n-1) for h in [(0,*rest)])
        s,h,m=solve_comparisons(D,atoms);assert s==('YES' if ans else 'NO');out['abstract'].append({'status':s,**m})
    # Many distinct offsets on one physical pair, both polarities; no source transfer.
    for B in [8,32,128,512]:
        D=np.full((5,5),2*B,dtype=np.int64);np.fill_diagonal(D,0);D[0,:]=B;D[:,0]=B;D[0,0]=0
        atoms=[(k,v,1,0,2,d) for d in range(-B,B+1) for k,v in [('min',3),('max',4)]]
        s,h,m=solve_comparisons(D,atoms,cap=4096);assert s=='YES';out['scales'].append({'B':B,'raw_atoms':len(atoms),**m})
    json.dump(out,open('fg16_results.json','w'),indent=2)
    print('native',[(x['kind'],x.get('case_id'),x['status'],x['stage'],x.get('budget'),x.get('leaves'),x.get('macro_patterns')) for x in out['native']]);print('abstract',collections.Counter(x['status'] for x in out['abstract']));print('scales',out['scales'])
if __name__=='__main__':main()
