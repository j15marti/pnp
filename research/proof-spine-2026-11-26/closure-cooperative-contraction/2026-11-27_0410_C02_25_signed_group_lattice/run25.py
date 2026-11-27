"""C02-25 signed-lattice group support. Fixed one/two-group pin tests."""
from run24 import *
from sympy import Matrix, ZZ, zeros
from sympy.matrices.normalforms import smith_normal_decomp, hermite_normal_form
from itertools import combinations
import sys
CAP25=12_000_000
NF_CAP=500

def matlist(M): return [[int(v) for v in row] for row in M.tolist()]

def lattice(gs,t,C,nf,records,depth=1):
    rows,cols,b=columns(gs,t); m=b.bit_length(); n=len(rows)
    C.tick('matrix_cells',m*n)
    A=Matrix([[int(v>>i&1) for v in cols] for i in range(m)]); B=Matrix([int(b>>i&1) for i in range(m)])
    def normalform(fn,X):
        if nf[0]>=NF_CAP: raise p.Cap
        nf[0]+=1; C.tick('normal_form_cells',max(1,X.rows*X.cols));return fn(X)
    D,U,V=normalform(lambda X:smith_normal_decomp(X,domain=ZZ),A)
    C.tick('verify_smith_cells',m*m+m*n+n*n)
    assert U*A*V==D and abs(V.det(method='domain-ge'))==1 and abs(U.det(method='domain-ge'))==1
    assert all(D[i,j]==0 for i in range(m) for j in range(n) if i!=j)
    r=sum(bool(D[i,i]) for i in range(min(m,n)));assert all(D[i,i]!=0 for i in range(r))
    q=U*B; z=zeros(n,1)
    record=dict(rows=rows,D=matlist(D),U=matlist(U),V=matlist(V),groups=[],drops=[],kind='support')
    for i in range(m):
        if (i>=r and q[i]!=0) or (i<r and q[i]%D[i,i]!=0):
            record.update(kind='NO',bad_eq=i);records.append(record);return None
        if i<r:z[i]=q[i]//D[i,i]
    x=V*z;K=V[:,r:];assert A*x==B and A*K==zeros(m,n-r)
    idx=[[j for j,(k,_) in enumerate(rows) if k==i] for i in range(len(gs))]
    drop=set()
    for size in range(1,depth+1):
        for blocks in combinations(range(len(gs)),size):
            I=[j for i in blocks for j in idx[i]];L=K[I,:];o=x[I,0]
            H=normalform(hermite_normal_form,L) if L.cols else zeros(len(I),0)
            piv=list(H.T.rref()[1]);assert len(piv)==H.cols
            inv=H[piv,:].inv() if piv else zeros(0,0)
            Z=inv*L[piv,:] if piv else zeros(0,L.cols)
            C.tick('verify_projection_cells',max(1,len(I)*L.cols+len(I)*H.cols))
            assert H*Z==L and all(v.q==1 for v in Z)
            supported=set();bad=[]
            for choice in product(*(idx[i] for i in blocks)):
                C.tick('attained_guard_candidate',len(I))
                e=Matrix([int(j in choice) for j in I])-o
                a=inv*e[piv,0] if piv else zeros(0,1)
                if H*a==e and all(v.q==1 for v in a):supported.update(choice)
                else:bad.append(list(choice))
            d=set(I)-supported;drop.update(rows[j] for j in d)
            if d:record['groups'].append(dict(blocks=blocks,I=I,H=matlist(H),piv=piv,bad=bad,drops=sorted(d)))
    record['drops']=sorted(drop);records.append(record)
    return drop

def lane25(gs,t,mode,acq=0,depth=1):
    gs=[set(g) for g in gs];C=p.Clock(CAP25);C.tick('acquisition',acq);records=[];lp_rec=[];nf=[0];lim=[0];rounds=removed=0;status='UNKNOWN';s=time.monotonic();history=[]
    try:
        while True:
            rounds+=1
            if any(not g for g in gs):status='NO';break
            drop=set()
            for mod in (('lp','lattice') if mode=='hybrid' else (mode,)):
                if any(not g for g in gs):status='NO';break
                while True:
                    fixed=[(i,next(iter(g))) for i,g in enumerate(gs) if len(g)==1]
                    dead={(j,y) for i,x in fixed for j,g in enumerate(gs) if j!=i for y in g if x&y}
                    C.tick('forced_scan',max(1,sum(map(len,gs))*(1+len(fixed))))
                    if not dead:break
                    for i,y in dead:gs[i].remove(y)
                    removed+=len(dead);drop|=dead;history.append(dict(method='forced',drops=sorted(dead)))
                    if any(not g for g in gs):status='NO';break
                if status=='NO':break
                if mod=='lp':a=lp(gs,t,C,lp_rec,lim)
                elif mod=='lattice':a=lattice(gs,t,C,nf,records,depth)
                elif mod=='parity':a=parity(gs,t,C)[0]
                elif mod=='dp':
                    tr=tree(gs,C);cuts=allcuts(gs,tr,t,C)
                    if any(v is None for v in cuts.values()):a=None
                    else:
                        sol,_,_=localdp(gs,t,tr,C,cuts,{})
                        a=None if sol is None else set(); assert sol is None
                else:raise ValueError(mod)
                if a is None:status='NO';history.append(dict(method=mod,terminal=True));break
                for i,y in a:gs[i].remove(y)
                removed+=len(a);drop|=a;history.append(dict(method=mod,drops=sorted(a)))
                C.tick('delete',len(a))
            if status=='NO' or not drop:break
    except p.Cap:pass
    return dict(status=status,work=C.n,counts=dict(C.c),nf_calls=nf[0],lp_calls=lim[0],rounds=rounds,removed=removed,history=history,records=records,lp_certs=lp_rec,final=[sorted(g) for g in gs],seconds=time.monotonic()-s)

def main():
    old=json.load(open(P/'result24.json'));raw=json.load(open(P/'octa17.json'));out=[]
    for j in map(int,sys.argv[1:]):
        s=raw[j];T=list(map(tuple,s['triples']));n=s['n'];pins=s['pins'];assert p.old.authenticate(T,n)
        data=json.dumps(dict(q=n,T=T,guard=[i for i,b in pins if not b]),separators=(',',':')).encode();sha=hashlib.sha256(data).hexdigest()
        ref,_,nodes=p.native.direct_native(T,n,pins,cap=5000);assert ref=='NO'
        val,mc=p.old.close(T,n,pins);v2,queries=p.independent_closure(T,n,pins);assert val==v2;L=[i for i,v in enumerate(val) if v!=0]
        for c in range(3):
            C=p.Clock(CAP25);gs,t,ledger=acquire(T,L,n,c,C,'matching');prior=old[3*j+c];assert sha==prior['sha'] and [sorted(g) for g in gs]==prior['initial'] and L==prior['ids'];assert json.loads(json.dumps(ledger))==prior['ledger']
            z=dict(job=j,c=c,N=len(data)*8,sha=sha,ids=L,pins=pins,closure_calls=mc,closure_audit=queries,reference_nodes=nodes,acquire=C.n,initial=[sorted(g) for g in gs],target=t)
            for mode in ('lp','lattice','dp','hybrid'):
                z[mode]=lane25(gs,t,mode,C.n,depth=1)
            if z['hybrid']['status']=='UNKNOWN':z['pair_hybrid']=lane25(gs,t,'hybrid',C.n,depth=2)
            out.append(z);print(j,c,[(m,z[m]['status'],z[m]['removed'],z[m]['nf_calls'],round(z[m]['seconds'],2)) for m in ('lp','lattice','dp','hybrid','pair_hybrid') if m in z],flush=True)
            (P/f'result25_{sys.argv[1]}.json').write_text(json.dumps(out,separators=(',',':')))
if __name__=='__main__':main()
