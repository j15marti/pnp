"""Direct independent checker of C02-25 exact row-deletion histories.
Run using the full C02-25 archive; import original source row codec and exact dual checker.
This is the executed audit25.py, also supplied in the archive.
"""
from run25 import *
from audit24 import check_cert
from sympy.matrices.normalforms import hermite_normal_form

def inlattice(B,y):
    return hermite_normal_form(B.row_join(y))==hermite_normal_form(B)

def audit(z):
    checked=0;roots=0;lpchecks=0;deletions=0
    for mode in ('lp','lattice','hybrid','pair_hybrid'):
        if mode not in z:continue
        res=z[mode];gs=list(map(set,z['initial']));t=z['target'];li=iter(res['lp_certs']);si=iter(res['records']);
        lc=list(res['lp_certs']);sc=list(res['records']);lp_i=sn_i=0
        for h in res['history']:
            mod=h['method'];d=set(map(tuple,h.get('drops',[])));term=h.get('terminal',False)
            if mod=='forced':
                fixed=[(i,next(iter(g))) for i,g in enumerate(gs) if len(g)==1]
                assert d=={(j,y) for i,x in fixed for j,g in enumerate(gs) if j!=i for y in g if x&y}
            elif mod=='lp':
                if d or term:
                    cert=lc[lp_i];lp_i+=1;assert check_cert(cert,t,gs)==d;assert (cert['kind']=='NO')==term;lpchecks+=1
            elif mod=='lattice':
                rec=sc[sn_i];sn_i+=1;rows,cols,b=columns(gs,t);assert rows==list(map(tuple,rec['rows']));m=b.bit_length();n=len(rows)
                A=Matrix([[int(v>>i&1) for v in cols] for i in range(m)]);B=Matrix([1]*m)
                if term:assert not inlattice(A,B);roots+=1
                else:
                    claim=set()
                    for group in rec['groups']:
                        blocks=group['blocks'];I=[j for j,(i,x) in enumerate(rows) if i in blocks];J=[j for j in range(n) if j not in I];rest=A[:,J];H=hermite_normal_form(rest)
                        dead=set(group['drops']);seen=set()
                        for choice in product(*[[j for j in I if rows[j][0]==i] for i in blocks]):
                            if not dead.intersection(choice):continue
                            v=B-sum((A[:,j] for j in choice),zeros(m,1));assert hermite_normal_form(rest.row_join(v))!=H
                            checked+=1;seen.update(dead.intersection(choice))
                        assert dead==seen;claim.update(rows[j] for j in dead)
                    assert claim==d;deletions+=len(d)
            if term:break
            for i,x in d:gs[i].remove(x)
        assert lp_i==len(lc) and sn_i==len(sc)
        assert [sorted(g) for g in gs]==res['final']
        if res['status']=='NO':
            assert res['history'][-1].get('terminal') or not all(res['final'])
    return dict(job=z['job'],c=z['c'],conditioned_checks=checked,root_checks=roots,lp_certificates=lpchecks,lattice_deletions=deletions)

def control():
    n=4;g=[{(1<<j)|(1<<(n+(i+j)%n)) for j in range(n)} for i in range(n)];t=(1<<(2*n))-1
    assert parity(g,t,p.Clock(CAP25))[0]==set()
    a=lane25(g,t,'lattice');assert a['status']=='NO'
    assert not any(len({(i+j)%n for i,j in enumerate(q)})==n for q in __import__('itertools').permutations(range(n)))
    g=[{1,2},{1,2}];t=3;C=p.Clock(CAP25);assert lattice(g,t,C,[0],[],2)==set()
    return dict(cyclic_order4='NO via signed lattice; LP uniform and binary parity supported',equality_control='all genuine one-hot pair choices survive')

if __name__=='__main__':
    out=[]
    for j in map(int,sys.argv[1:]):
        for z in json.load(open(f'result25_{j}.json')):
            a=audit(z);out.append(a);print(a,flush=True)
    c=control();print(c);(P/f'audit25_{sys.argv[1]}.json').write_text(json.dumps(dict(native=out,control=c),indent=2))
