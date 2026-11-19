#!/usr/bin/env python3
"""TMR-5/076. Independent, strict, label-sensitive reverse decoder for the
normalized nonempty image of the owned /074 signed-3CNF -> T5 compiler.

All decoder conditions and graph reconstructions are independent of the
producer in the predecessor evidence ZIP. That producer is imported only to
supply authentic test inputs, to test exact byte equality, and for witness lifts.
This is not a general T5 solver.
"""
import importlib.util, itertools, json, random, hashlib, pathlib, collections, sys
HERE=pathlib.Path(__file__).resolve().parent
REV='tmr5-t5-labelled-inverse076-v1'
SEED=20261117

class Invalid(ValueError): pass

def w(n): return max(1,(max(2,n)-1).bit_length())
def encbits(v,b): return ''.join('1' if (v>>i)&1 else '0' for i in range(b))
def enc3(k,clauses):
    return '1'*k+'0'+'1'*len(clauses)+'0'+''.join(str(s)+encbits(i,w(k)) for clause in clauses for i,s in clause)

def parse_t5(src):
    if not isinstance(src,str) or any(a not in '01' for a in src):raise Invalid('nonbinary')
    pos=0
    def num():
        nonlocal pos
        z=0
        while pos<len(src) and src[pos]=='1':z+=1;pos+=1
        if pos==len(src):raise Invalid('missing delimiter')
        pos+=1
        return z
    n=num();m=num();bits=w(n)
    if len(src)-pos!=2*bits*m:raise Invalid('record length')
    edges=[]
    for _ in range(m):
        u=sum((src[pos+i]=='1')<<i for i in range(bits));pos+=bits
        v=sum((src[pos+i]=='1')<<i for i in range(bits));pos+=bits
        if not(0<=u<n and 0<=v<n and u!=v):raise Invalid('invalid endpoints')
        if edges and edges[-1]>=(u,v):raise Invalid('unordered or duplicate arcs')
        edges.append((u,v))
    return n,tuple(edges)

def strict_inverse(src):
    n, arcs=parse_t5(src); arc_set=set(arcs); a=len(arcs)
    if n==0 and a==0:return dict(empty=True,k=0,m=0,clauses=[],quotient_n=0,quotient_m=0,quotient_rho=0,raw_rho=0)
    if not n or not a:raise Invalid('not in nonempty image')
    # Exactly recover normalized source's variable and clause counts.
    vnum=244*(n-57)-168*(a-80)
    mnum=36*(a-80)-52*(n-57)
    if vnum%48 or mnum%48:raise Invalid('count determinant')
    k=vnum//48; m=mnum//48
    if k<=0 or m<=0 or k>3*m:raise Invalid('normalized source parameters')
    n3=3+2*k+8*m; m3=3+3*k+15*m
    hn=5+2*n3+2*m3; he=5+2*n3+3*m3
    if hn+2*he!=n or 4*he!=a:raise Invalid('graph size')
    # Recover each 4-arc T5 gadget, and demand every arc is accounted for.
    E=[];expected=set()
    for ei in range(he):
        z=hn+2*ei; ww=z+1
        intoz=[u for u,v in arcs if v==z and u!=ww]
        intow=[u for u,v in arcs if v==ww]
        outw=[v for u,v in arcs if u==ww and v!=z]
        if len(intoz)!=1 or len(intow)!=1 or len(outw)!=1:raise Invalid('gadget degrees')
        u=intoz[0]; v=outw[0]
        if u!=intow[0] or not(0<=u<v<hn):raise Invalid('gadget endpoints')
        E.append((u,v))
        expected.update(((u,z),(u,ww),(ww,z),(ww,v)))
    if len(E)!=len(set(E)) or E!=sorted(E) or expected!=arc_set:raise Invalid('gadget arcs')
    H=set(E)
    # H consists of fixed anchor, N3 private source-to-anchor 2-paths,
    # and M3 private 3-paths encoding the sorted G3 edges.
    EH={tuple(sorted((i,(i+1)%5))) for i in range(5)}
    for i in range(n3):
        p=5+n3+i; EH.add(tuple(sorted((0,p))));EH.add(tuple(sorted((p,5+i))))
    G=[]
    for ei in range(m3):
        p=5+2*n3+2*ei;q=p+1
        up=[u for u in range(n3) if tuple(sorted((5+u,p))) in H]
        vp=[v for v in range(n3) if tuple(sorted((q,5+v))) in H]
        if len(up)!=1 or len(vp)!=1 or not(up[0]<vp[0]):raise Invalid('H 3-path endpoints')
        u,v=up[0],vp[0]
        G.append((u,v))
        EH.update((tuple(sorted((5+u,p))),tuple(sorted((p,q))),tuple(sorted((q,5+v)))))
    if len(G)!=len(set(G)) or G!=sorted(G) or EH!=H:raise Invalid('H source structure')
    # Decode clause-literal pins from signed 3-COLOR graph spokes.
    GG=set(G);NG=3+2*(k+m)+6*m
    if NG!=n3:raise Invalid('G3 size')
    EG={(0,1),(0,2),(1,2)}
    for b in range(k+m):
        p=3+2*b;q=p+1
        EG.update((tuple(sorted((2,p))),tuple(sorted((2,q))),(p,q)))
    triangles=[]
    base=3+2*(k+m)
    for j in range(2*m):
        tri=[base+3*j+i for i in range(3)]
        EG.update((tuple(sorted((tri[0],tri[1]))),tuple(sorted((tri[0],tri[2]))),tuple(sorted((tri[1],tri[2])))))
        pins=[]
        for t in tri:
            near=[u for u in range(base) if tuple(sorted((u,t))) in GG]
            if len(near)!=1:raise Invalid('triangle pin degree')
            pins.append(near[0]);EG.add(tuple(sorted((t,near[0]))))
        triangles.append(pins)
    if EG!=GG:raise Invalid('G3 exact source structure')
    def lit(p):
        if p<3 or p>=3+2*k:raise Invalid('non-core literal')
        return ((p-3)//2,(p-3)%2)
    clauses=[]
    for j in range(m):
        t1=triangles[2*j];t2=triangles[2*j+1]
        if t1[2]!=3+2*(k+j) or t2[0]!=4+2*(k+j) or t2[2]!=1:raise Invalid('splitter pin')
        clauses.append((lit(t1[0]),lit(t1[1]),lit(t2[1])))
    if clauses!=sorted(set(clauses)):raise Invalid('duplicate or out-of-order clauses')
    if set(i for cl in clauses for i,s in cl)!=set(range(k)):raise Invalid('unused compact variable')
    return dict(empty=False,k=k,m=m,clauses=clauses,quotient_n=hn,
                quotient_m=he,quotient_rho=he-hn+1,raw_rho=a-n+1,
                expected_qrho=4+3*k+15*m,
                normalized_source=enc3(k,clauses),D_n=n,D_a=a,
                H_n=hn,H_m=he,G_n=n3,G_m=m3,all_arcs=arcs,
                H_edges=tuple(E),G_edges=tuple(G))

def force_triads(n, arcs):
    """Unannotated directed transitive triangle index in O(sum_v outdeg(v)^2)."""
    outs=[set() for _ in range(n)]
    for a,b in arcs:outs[a].add(b)
    tris=[]
    for a in range(n):
        for b in outs[a]:
            for c in outs[a].intersection(outs[b]):tris.append((a,b,c))
    return sorted(tris)

def validate_quotient(src, inv):
    if inv['empty']:return (0,0)
    n=inv['D_n']; arcs=inv['all_arcs'];hn=inv['H_n'];he=inv['H_m']
    tris=force_triads(n,arcs)
    want=sorted((u,hn+2*ei+1,hn+2*ei) for ei,(u,v) in enumerate(inv['H_edges']))
    if tris!=want:raise AssertionError('extra/absent transitive triangles')
    # For each triad the implied potentials are p(w)=p(u)+3,p(z)=p(u)+1.
    # The only residual arc w->v gives (label[v]-label[u]) in {1,4}.
    if inv['quotient_rho']!=inv['expected_qrho'] or inv['raw_rho']-inv['quotient_rho']!=he:
        raise AssertionError('rank identity')
    return len(tris),he

def run():
    spec=importlib.util.spec_from_file_location('producer074',HERE/'tmr5_t5_full_3sat_chain074.py')
    producer=importlib.util.module_from_spec(spec);spec.loader.exec_module(producer)
    rng=random.Random(SEED);counts=collections.Counter();records=[]
    cases=[(0,[]),(5,[]),(1,[((0,0),)*3]),(1,[((0,0),)*3,((0,1),)*3]),(3,[((0,0),(1,1),(2,0))]),(1000,[((999,0),(999,1),(999,0))])]
    for k in range(1,5):
        lits=[(i,s) for i in range(k) for s in (0,1)]
        for j in range(20):
            cl=[tuple(rng.choice(lits) for _ in range(3)) for _ in range(rng.randrange(1,5))]
            if j%7==0:cl*=3
            cases.append((k,cl))
    for n,clauses in cases:
        source=producer.encode3(n,clauses)
        D=producer.compile_sat(source)
        inv=strict_inverse(D['out'])
        counts['source_cases']+=1
        if not clauses:
            assert inv['empty'];counts['empty']+=1;continue
        k= len(D['core']);m=len(D['cl'])
        assert (inv['k'],inv['m'])==(k,m)
        assert inv['clauses']==D['cl']
        assert inv['normalized_source']==producer.encode3(k,D['cl'])
        assert (inv['D_n'],inv['D_a'])==(D['Dn'],len(D['DE']))
        assert tuple(D['HE'])==inv['H_edges'] and tuple(D['E3'])==inv['G_edges']
        nt,ng=validate_quotient(D['out'],inv)
        assert nt==ng==len(D['HE'])
        counts['reduction_cases']+=1;counts['source_triads']+=nt
        counts['quotient_rho_sum']+=inv['quotient_rho']
        counts['raw_rho_sum']+=inv['raw_rho']
        max_orbit=5**min(k,3)
        # Compare original and normalized Boolean satisfiability on all
        # inputs for small n, including NO sources and duplicate clauses.
        if n<=4:
            for assignment in itertools.product((0,1),repeat=n):
                x=tuple(assignment[i] for i in D['core'])
                assert producer.sat3(D['cl0'],assignment)==producer.sat3(inv['clauses'],x)
                counts['source_assignment_checks']+=1
                if producer.sat3(D['cl0'],assignment):
                    lab=producer.lift(D,assignment)
                    assert all((lab[v]-lab[u])%5 in (1,3) for u,v in inv['all_arcs'])
                    assert producer.sat3(D['cl0'],producer.reverse(D,lab))
                    counts['witness_lifts']+=1
        # Arcs are independently checked; off-image bitstream modifications
        # must not be classified as authenticated compiler outputs.
        if len(D['DE'])>=4:
            arc=list(D['DE']); z=D['Hn'];wz=z+1
            # Introduce one valid lexicographic nonduplicate arc, so counts change.
            alt=set(arc);new=(0,1)
            if new not in alt:alt.add(new)
            else:
                for u in range(D['Dn']):
                    if (u,(u+1)%D['Dn']) not in alt:
                        alt.add((u,(u+1)%D['Dn']));break
            corrupted=producer.encodegraph(D['Dn'],sorted(alt),True)
            try:strict_inverse(corrupted)
            except Invalid:counts['corrupt_add_reject']+=1
            else:raise AssertionError('accepted invalid added arc')
            alt=set(arc);alt.remove(arc[-1]);
            corrupted=producer.encodegraph(D['Dn'],sorted(alt),True)
            try:strict_inverse(corrupted)
            except Invalid:counts['corrupt_delete_reject']+=1
            else:raise AssertionError('accepted deleted arc')
            # Same counts, legal sorted arcs, wrong gadget wiring.
            alt=set(arc);old=next((e for e in arc if e[1]>=D['Hn'] and e[0]<D['Hn']),None)
            alt.remove(old)
            replacement=next((u,v) for u in range(D['Hn']) for v in range(D['Hn'],D['Dn']) if (u,v) not in alt and (u,v)!=old)
            alt.add(replacement)
            corrupted=producer.encodegraph(D['Dn'],sorted(alt),True)
            try:strict_inverse(corrupted)
            except Invalid:counts['corrupt_preserve_counts_reject']+=1
            else:raise AssertionError('accepted wrong same-size gadget')
        if len(records)<8:
            records.append({"n_input":n,"m_input":len(clauses),"k":k,"m_prime":m,"n_D":D['Dn'],"a_D":len(D['DE']),"quotient_rho":inv['quotient_rho'],"raw_rho":inv['raw_rho'],"L_source":len(source),"L_D":len(D['out'])})
    # Fully independent algebraic checking for every nonnegative k,m up to 100.
    for k in range(1,101):
        for m in range(max(1,(k+2)//3),101):
            nd=57+36*k+168*m; ad=80+52*k+244*m
            assert 244*(nd-57)-168*(ad-80)==48*k
            assert 36*(ad-80)-52*(nd-57)==48*m
            hn=17+10*k+46*m; he=20+13*k+61*m
            assert nd==hn+2*he and ad==4*he
            assert (ad-nd+1)-(he-hn+1)==he
            assert he-hn+1==4+3*k+15*m
            counts['symbolic_integer_pairs_checked']+=1
    data={'rev':REV,'seed':SEED,'tested_counts':dict(counts),'records':records,'status':'COMPUTATIONAL test for unrestricted symbolic inverse proof','limitations':['Only exactly labelled nonempty /074 reduction image; graph isomorphism/relabelled images not recognized','No general T5 decision or counting algorithm','No exhaustive search of full target UNSAT labellings','No native bit-TM replay or external mathematical peer review']}
    raw=json.dumps(data,sort_keys=True,indent=2)+'\n'
    out=HERE/'TMR5_076_INVERSE_RAW.json';out.write_text(raw)
    print(json.dumps({'status':'PASS','rev':REV,'seed':SEED,'counts':dict(counts),'raw_sha256':hashlib.sha256(raw.encode()).hexdigest(),'examples':records[:3]},sort_keys=True))

if __name__=='__main__':run()
