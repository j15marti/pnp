"""T5-MARGINAL-MATCHING-PAIR1: new joint-distribution falsifier, no hardness claim."""
import hashlib,json
from pathlib import Path
from fractions import Fraction
import t5_construction_positive_offset1_20261121 as c
DEP="6cd122e55ab7150dff6c8a1a22099ec5b44b195395c9f83670965773417accdb"
assert hashlib.sha256(Path(c.__file__).read_bytes()).hexdigest()==DEP
def audit(p):
    enc=[];zs=[];meta=[]
    for j in (0,1):
        gates=(('or',0,j),)
        z=c.source_count(p,gates,p)
        assert z==((1<<(p-1)) if j==0 else 3*(1<<(p-2)))
        pp,gg,oo=c.lift(p,gates,p)
        n,cs=c.compile_circuit(pp,gg,oo)
        nn,ss,E=c.split(n,cs);x=c.encode(nn,ss)
        assert c.decode(x)==(nn,ss)
        enc.append(x);zs.append(10*(1<<E)*((1<<p)+z));meta.append((nn,len(ss),E))
    assert meta[0]==meta[1]
    n,m,E=meta[0];N=len(enc[0]);ell=3*N
    assert len(enc[1])==N
    assert (n,m,E)==(426+74*p,520+90*p,81+14*p)
    assert all(0<z<=5**n and z>10*(1<<(E+p)) for z in zs)
    i=next(i for i,(a,b) in enumerate(zip(*enc)) if a!=b)
    # Explicit AND/OR/NOT circuit; free input nodes and constants.
    gates=[]
    def gate(op,*args):
        gates.append((op,args));return N+ell+len(gates)-1
    selector=i if enc[1][i]=='1' else gate('not',i)
    def eq(z):
        w=format(z,f'0{ell}b')
        lits=[N+k if bit=='1' else gate('not',N+k) for k,bit in enumerate(w)]
        acc=lits[0]
        for v in lits[1:]:acc=gate('and',acc,v)
        return acc
    e0,e1=eq(zs[0]),eq(zs[1])
    out=gate('or',gate('and',gate('not',selector),e0),gate('and',selector,e1))
    assert len(gates)<=4*ell+3
    def evaluate(x,z):
        vals=[int(b) for b in x+format(z,f'0{ell}b')]
        for op,args in gates:
            a=vals[args[0]]
            vals.append(1-a if op=='not' else (a&vals[args[1]] if op=='and' else a|vals[args[1]]))
        return vals[out]
    matrix=[[evaluate(x,z) for z in zs] for x in enc]
    assert matrix==[[1,0],[0,1]]
    # All four Boolean predicates on the two-value output support.
    for mask in range(4):
        true=sum(Fraction((mask>>j)&1,2) for j in range(2))
        fake=sum(Fraction((mask>>k)&1,4) for j in range(2) for k in range(2))
        assert true==fake
    return dict(p=p,n=n,m=m,E=E,N=N,outputs=zs,selector_position=i,
                selector_bits=[x[i] for x in enc],circuit_gates=len(gates),
                gate_budget=12*N+3,joint_acceptance=matrix,true_acceptance="1",
                fake_acceptance="1/2",advantage="1/2",conditional_entropy_bits=1,
                encoding_sha256=[hashlib.sha256(x.encode()).hexdigest() for x in enc])
if __name__=='__main__':
    print(json.dumps(dict(lemma="T5-MARGINAL-MATCHING-PAIR1",rows=[audit(p) for p in range(2,9)],
        dependency_sha256=DEP,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        seed=None,split_count_method="published equality theorem; no expanded enumeration",
        status="PASS; exact finite joint-distribution and explicit circuit checks"),indent=2))
