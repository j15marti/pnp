"""Independent exact compiler-image energy certificate checker. Python 3; companion check_compact.py for RUP.
Usage: python check_energy34.py NAME.eb.json NAME.cnf NAME.map.json NAME.energy34-cert.json [NAME.root34.json]
The certificate uses all signed edges and E vertices as hard; energy counts violated B vertices only.
"""
import json, hashlib, itertools as it, collections as co, sys
from pathlib import Path

def sha(b): return hashlib.sha256(b).hexdigest()
def check(raw, cnf, mraw, cert, proofraw=None):
    G=json.loads(raw); M=json.loads(mraw); T=G['types']; E=G['edges']; n=len(T)
    assert G['format']=='STRICT-EB4-v1' and set(T)<= {'E','B'}
    assert cert['instance_id']=='STRICT-EB4-v1:sha256:'+sha(raw) and cert['original_N_bits']==8*len(raw)
    assert cert['cnf_sha256']==sha(cnf) and cert['cnf_N']==8*len(cnf) and cert['source_map_sha256']==sha(mraw)
    assert cert['guard_id']=='EMPTY' and cert['residual_id']=='ROOT'
    assert cert['original_ids']=={'vertices':[0,n-1],'ports':[0,4*n-1],'edges':[0,len(E)-1]}
    L=cnf.decode('ascii').splitlines(); _,typ,nv,nc=L[0].split(); nv=int(nv);nc=int(nc);assert typ=='cnf'
    C=[list(map(int,q.split())) for q in L[1:]];assert len(C)==nc and all(q[-1]==0 and len(q)>1 and all(0<abs(l)<=nv for l in q[:-1]) for q in C);C=[q[:-1] for q in C]
    # Independent parity DSU, minimum original port roots, iterative path compression.
    par=list(range(4*n)); sign=[0]*(4*n)
    def root(a):
        p=a;z=0
        while par[p]!=p:z^=sign[p];p=par[p]
        r=p;p=a;t=z
        while par[p]!=p:
            q=par[p];old=sign[p];par[p]=r;sign[p]=t;t^=old;p=q
        return r,z
    def union(a,b,s):
        a,x=root(a);b,y=root(b);s^=x^y
        if a==b:assert s==0;return
        if a>b:a,b=b,a
        par[b]=a;sign[b]=s
    ports=set();adj=set()
    for a,b,s in E:
        assert 0<=a<4*n and 0<=b<4*n and a//4!=b//4 and a not in ports and b not in ports and s in (0,1)
        uv=tuple(sorted((a//4,b//4)));assert uv not in adj;adj.add(uv);ports.update((a,b));union(a,b,s)
    assert len(ports)==4*n
    for v,t in enumerate(T):
        if t=='E':
            for j in (1,2,3):union(4*v,4*v+j,0)
    rp=M['representative_ports'];rep={k:(*root(p),s) for k,(p,s) in rp.items()};assert len({r for r,z,s in rep.values()})==len(rep) and {r for r,z,s in rep.values()}=={root(p)[0] for p in range(4*n)}
    # Reconstruct the exact signed ternary chain, original clause ownership, and all B port constraints.
    U=[];owners=[];nextvar=nv;chains=[]
    for i,q in enumerate(C,1):
        if len(q)<=3:R=[q+[q[-1]]*(3-len(q))]
        else:
            R=[];prev=None
            for j in range(len(q)-3):
                nextvar+=1;R.append([q[0],q[1],nextvar] if j==0 else [-prev,q[j+1],nextvar]);prev=nextvar
            R.append([-prev,q[-2],q[-1]])
        U+=R;owners += [i]*len(R);chains.append(R)
    assert U==M['ternary_clauses'] and owners==M['original_clause_ids'] and M['original_n']==nv
    expected=set();pc=0
    def literal(l):return ('x'+str(abs(l)),int(l<0))
    for i,(a,b,c) in enumerate(U):
        for j,Q in enumerate(([literal(a),literal(b),('z'+str(i),0)],[('z'+str(i),1),literal(c),('f',0)])):
            for k in (0,1):
                v=4*i+2*j+k;expected.add(v);assert T[v]=='B' and M['vertex_provenance'][v]==['clause',owners[i],i,j,k]
                for h,(name,s) in enumerate(Q+[('w'+str(i)+'_'+str(j),0)]):
                    r,z=root(4*v+h);r0,z0,s0=rep[name];assert r==r0 and z^z0==s^s0;pc+=1
    assert expected=={v for v,t in enumerate(T) if t=='B'}
    # Exact gadget cost identity by exhaustive local truth table.
    for a,b,c in it.product((0,1),repeat=3):
        assert min(2*(int(a+b+z+w!=2)+int(1-z+c+w2!=2)) for z,w,w2 in it.product((0,1),repeat=3))==2*int(not(a or b or c))
    # Verify zero-energy impossibility when required.
    method=cert['lower_bound_method'];lower=0;local_checks=0
    if method=='native_root_RUP_and_duplicate_B_pair':
        from check_compact import check as rup_check
        assert proofraw is not None and 'CERT-v1:sha256:'+sha(proofraw) in cert['parents'];rup_check(raw,json.loads(proofraw));lower=2
    elif method=='XOR_exact_equal_scope_violation_polynomials_and_owner_transport':
        grouped=co.defaultdict(list)
        for q in C:grouped[tuple(sorted(set(map(abs,q))))].append(q)
        pol=set()
        for vs,clauses in grouped.items():
            assert len(vs)<=5
            # Independent Möbius coefficient formula: coefficient S = XOR of f(T) over T subset S.
            bad=[]
            for h in range(1<<len(vs)):
                A={v:bool(h>>j&1) for j,v in enumerate(vs)};bad.append(not all(any(A[abs(l)]==(l>0) for l in q) for q in clauses));local_checks+=1
            for mask in range(1<<len(vs)):
                v=mask;x=0
                while True:
                    x^=bad[v];local_checks+=1
                    if not v:break
                    v=(v-1)&mask
                if x:
                    term=tuple(v for j,v in enumerate(vs) if mask>>j&1)
                    if term in pol:pol.remove(term)
                    else:pol.add(term)
        assert pol=={()};lower=2
    else:assert method=='nonnegativity'
    # Reconstruct witness from source assignment, independently check original constraints.
    ones=set(cert['witness_source_ones']);assert ones<=set(range(1,nv+1));A={'x'+str(i):int(i in ones) for i in range(1,nv+1)};A['f']=0
    def val(l):return A['x'+str(abs(l))]^int(l<0)
    for q,R in zip(C,chains):
        if len(q)>3:
            for a,b,z in R[:-1]:A['x'+str(z)]=int(not(val(a) or val(b)))
    bad=[i for i,q in enumerate(C,1) if not any(map(val,q))];assert bad==cert['witness_bad_clauses']
    for i,(a,b,c) in enumerate(U):
        a,b,c=val(a),val(b),val(c);z=min((0,1),key=lambda z:int(a==b==z)+int((1-z)==c==0));A['z'+str(i)]=z;A['w'+str(i)+'_0']=int(a+b+z==1);A['w'+str(i)+'_1']=int(1-z+c==1)
    assert set(A)==set(rep);values={r:A[name]^z^s for name,(r,z,s) in rep.items()};bits=bytes(values[r]^s for p in range(4*n) for r,s in [root(p)])
    assert all(bits[a]^bits[b]==s for a,b,s in E)
    assert all(len(set(bits[4*v:4*v+4]))==1 for v,t in enumerate(T) if t=='E')
    defects=[v for v,t in enumerate(T) if t=='B' and sum(bits[4*v:4*v+4])!=2]
    assert sha(bits)==cert['witness_port_bit_bytes_sha256'] and defects==cert['witness_bad_B_vertices'] and len(defects)==2*len(bad)==lower==cert['minimum_B_energy']
    return {'minimum_B_energy':lower,'native_port_checks':pc,'native_hard_and_energy_checks':len(E)+n,'local_polynomial_checks':local_checks,'defects':defects}
if __name__=='__main__':
    r,c,m,q=[Path(p).read_bytes() for p in sys.argv[1:5]];proof=Path(sys.argv[5]).read_bytes() if len(sys.argv)>5 else None
    print('CERT-v1:sha256:'+sha(q),check(r,c,m,json.loads(q),proof))
