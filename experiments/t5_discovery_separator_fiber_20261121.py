"""Finite full-witness audit of a one-separator strict-C shortcut."""
from collections import defaultdict
from itertools import product
from hashlib import sha256
from pathlib import Path
import json, random
import t5_construction_positive_offset1_20261121 as c
from t5_discovery_unary_fiber_20261121 import Diagram

def source(k):
    p=k+1; gates=[]
    def add(g):
        gates.append(g); return p+len(gates)-1
    zs=[add(('or',0,i)) for i in range(1,p)]
    out=zs[0]
    for z in zs[1:]:
        a=add(('not',out)); b=add(('not',z))
        d=add(('or',a,b)); out=add(('not',d))
    for i in range(1,p):
        a=add(('not',0)); b=add(('not',i)); d=add(('or',a,b)); t=add(('not',d))
        nt=add(('not',t)); taut=add(('or',t,nt))
        a=add(('not',out)); b=add(('not',taut)); d=add(('or',a,b)); out=add(('not',d))
    return p,gates,out

def row(p,gates,bits):
    wires=list(bits)
    for op,*args in gates:
        wires.append(1-wires[args[0]] if op=='not' else wires[args[0]]|wires[args[1]])
    names=list(range(5))+wires
    for bit in wires:
        for j in (2,3,4):
            hs=[h for h in range(5) if c.C(j,bit,h) and c.C((j+2)%5,(j+3)%5,h)]
            h,=hs; names.append(h)
    for op,*args in gates:
        if op=='or': names.extend((0 if wires[args[0]] else 3,2 if wires[args[1]] else 4))
    return names

def audit(k):
    p,gates,out=source(k); n,cs=c.compile_circuit(p,gates,out)
    nn,ss,E=c.split(n,cs); encoded=c.encode(nn,ss)
    # Admission from bytes: recover k from the unary n header and regenerate.
    def admitted(text):
        count=text.find('0')
        if count<0 or (count+264)%1669:return False
        kk=(count+264)//1669
        if kk<1:return False
        pp,gg,oo=source(kk); nc,cc=c.compile_circuit(pp,gg,oo)
        ns,sc,_=c.split(nc,cc)
        return c.encode(ns,sc)==text
    assert admitted(encoded)
    corrupted=encoded[:-1]+str(1-int(encoded[-1]))
    assert not admitted(corrupted)
    # First t=s AND x_1 is genuinely bivariate on accepting source rows.
    probes=[row(p,gates,[0]+[1]*k),row(p,gates,[1]+[0]*k),row(p,gates,[1]+[1]*k)]
    assert [r[5+6*k] for r in probes]==[0,0,1]
    assert (n,len(cs),E,nn,len(ss))==(74*k-9,131*k-20,319*k-51,1669*k-264,2045*k-326)
    copies=[[] for _ in range(n)]
    for j,t in enumerate(cs):
        for slot,v in enumerate(t): copies[v].append(3*j+slot)
    private=[]; cursor=3*len(cs)
    for xs in copies:
        private.append(list(range(cursor,cursor+4*(len(xs)-1),4)))
        cursor+=4*(len(xs)-1)
    assert cursor==nn
    anchors=[xs[0] for xs in copies[:5]]; separator=copies[5][0]
    dag=Diagram(); frames=[]
    for origin,step in product(range(5),(-1,1)):
        color=lambda v:(origin+step*v)%5
        branches=[]
        for s in (0,1):
            basebits=[s]+[1-s]*k; base=row(p,gates,basebits)
            singles={}
            if s:
                for i in range(1,p):
                    bits=basebits.copy();bits[i]^=1; singles[i]=row(p,gates,bits)
            groups=defaultdict(list)
            for v in range(n):
                changes=[i for i,r in singles.items() if r[v]!=base[v]]
                assert len(changes)<=1
                groups[changes[0] if changes else -1].append(v)
            root=1
            for group,vs in groups.items():
                selector=copies[5+group][0] if group>=0 else None
                options=[]
                for values in ([base,singles[group]] if group>=0 else [base]):
                    term=1
                    for v in vs:
                        port=color(values[v])
                        for cp in copies[v]:
                            if cp not in anchors and cp!=separator and cp!=selector:
                                term=dag.both(term,dag.truth([cp],[([port],1)]))
                        for start in private[v]:
                            variants=[([(port+d*j)%5 for j in (1,2,3,4)],1) for d in (-1,1)]
                            term=dag.both(term,dag.truth(range(start,start+4),variants))
                    if selector is None: root=dag.both(root,term)
                    else: options.append(([color(values[5+group])],term))
                if options:root=dag.both(root,dag.truth([selector],options))
            branches.append(([color(s)],root))
        frames.append(([color(i) for i in range(5)],dag.truth([separator],branches)))
    root=dag.truth(anchors,frames)
    counts=[0,1]
    for op,*args in dag.nodes[2:]:
        x,y=args[-2:]; counts.append(counts[x]*counts[y] if op=='and' else counts[x]+counts[y])
    expected=10*(2**k+1)*2**E
    assert counts[root]==expected
    # Exhaustive Boolean source rows, independent of diagram count.
    accepted=0
    for bits in product((0,1),repeat=p):
        vals=row(p,gates,bits); ok=all(c.C(*(vals[v] for v in t)) for t in cs)
        assert ok==all(bits[0] or x for x in bits[1:]); accepted+=ok
    assert accepted==2**k+1
    rng=random.Random(53); checked=0
    for _ in range(8):
        bits={};todo=[root]
        while todo:
            i=todo.pop()
            if i==1:continue
            op,*args=dag.nodes[i]
            if op=='and':todo.extend(args)
            else:
                bit,x,y=args;assert bit not in bits
                value=rng.choice([b for b,node in enumerate((x,y)) if counts[node]])
                bits[bit]=value;todo.append((x,y)[value])
        assert len(bits)==3*nn
        colors=[4*bits[3*i]+2*bits[3*i+1]+bits[3*i+2] for i in range(nn)]
        assert all(c.C(*(colors[v] for v in t)) for t in ss);checked+=1
    return dict(k=k,n_core=n,m_core=len(cs),E=E,n=nn,m=len(ss),N=len(encoded),nodes=len(dag.nodes),count=str(expected),source_count=accepted,source_rows=2**p,witnesses=checked,admission_checks=2,bivariate_values=[0,0,1],input_sha256=sha256(encoded.encode()).hexdigest())

if __name__=='__main__':
    print(json.dumps(dict(status='PASS',seed=53,results=[audit(k) for k in (1,2,3,5,8)],dependencies={Path(mod.__file__).name:sha256(Path(mod.__file__).read_bytes()).hexdigest() for mod in (c,) }),indent=2))
