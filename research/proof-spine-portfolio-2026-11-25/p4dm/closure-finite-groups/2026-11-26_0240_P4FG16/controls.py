from cover import *
from fractions import Fraction as F

def comparator_instance(clauses):
    # Each variable represented by x, nx; each gate has four distinct names.
    cells=[];pins={};xs=list(range(6));counter=6
    def fresh(val=None):
        nonlocal counter
        z=counter;counter+=1
        if val is not None:pins[z]=val
        return z
    for x in range(3):cells.append((fresh(0),2*x,2*x+1,fresh(1)))
    for clause in clauses:
        a,b,c=[2*i+s for i,s in enumerate(clause)]
        y=fresh();cells.append((fresh(),a,b,y));cells.append((fresh(),y,c,fresh(1)))
    return cells,pins,counter

def gate(a,b):return min(a,b),max(a,b)

def check_comparator():
    results=[];clauses=list(it.product(range(2),repeat=3))
    for name,C in [('all8',clauses),('delete_one',clauses[1:])]:
        cells,pins,n=comparator_instance(C);rows=[(min(a,b),a,b,max(a,b)) for a,b in it.product(range(2),repeat=2)]
        domains=[{pins[i]} if i in pins else {0,1} for i in range(n)];passes=0
        while True:
            passes+=1;old=[set(x) for x in domains]
            for cell in cells:
                W=[r for r in rows if all(b in domains[i] for i,b in zip(cell,r))]
                for j,i in enumerate(cell):domains[i]&={r[j] for r in W}
            if domains==old:break
        assert all(domains)
        truth=0
        for x in it.product(range(2),repeat=3):
            h={2*i:x[i] for i in range(3)};h.update({2*i+1:1-x[i] for i in range(3)})
            ok=True
            for H,a,b,c in cells:
                for i,v in zip((H,c),gate(h[a],h[b])):
                    if i in pins and pins[i]!=v:ok=False
                    h[i]=v
            truth+=ok
        # Linear conservation plus local order admits a half-integral point in BOTH cases.
        q={i:F(1,2) for i in range(6)}
        for j,(H,a,b,c) in enumerate(cells):
            if j<3 or (j-3)%2==0:q[H],q[c]=F(0),F(1)
            else:q[H],q[c]=F(1,2),F(1)
        assert all(q[i]==v for i,v in pins.items())
        assert all(q[H]<=min(q[a],q[b])<=max(q[a],q[b])<=q[c]<=q[H]+1 and q[H]+q[c]==q[a]+q[b] for H,a,b,c in cells)
        results.append({'case':name,'cells':len(cells),'variables':n,'GAC_passes':passes,'GAC_unpinned':sum(len(x)==2 for x in domains),'Boolean_models':truth,'fractional_conservation_feasible':True})
    assert [r['Boolean_models'] for r in results]==[0,1]
    return results

def native_scales():
    result=[]
    for k in [3,4,6,8]:
        T,*_=mesh(k);A=acquire(T);edges,D=chart(A[2],A[3]);rs={};minority=False
        for i,p in A[4].items():
            if len(p)!=2:continue
            a,b=edges[p[0][0]],edges[p[1][0]]
            # Exclude one diagonal, choose actual max polarity except at first pair.
            normal=a[1]==b[1];wantmin=not minority
            prev=normal==wantmin
            mask=frozenset([p[0][0 if prev else 1],p[1][0 if prev else 1]])
            S,B,W=A[5][i];rs[i]={w&B for w in W}-{mask};minority=True
        s=native_job(T,{},A,rs,full=k<=4);assert s['status']=='YES'
        s.update(k=k,tuples=len(T),guarded_regions=len(rs),full_implemented_closure=k<=4)
        result.append(s);print('scale',k,{k:v for k,v in s.items() if k!='witness'},flush=True)
    return result
if __name__=='__main__':
    ans={'abstract_comparator':check_comparator(),'native_scales':native_scales()};json.dump(ans,open('controls_results.json','w'),indent=2);print(ans['abstract_comparator'])
