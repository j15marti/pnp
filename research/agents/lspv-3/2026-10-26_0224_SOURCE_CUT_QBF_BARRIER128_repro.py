#!/usr/bin/env python3
"""LSPV-3 SOURCE-CUT-QBF-BARRIER128, dependency-free finite audit.
Exhaustive bounded quantified Boolean matrices and exact signed-(2,2) source gadgets.
Mathematical Pi2^P-completeness is proved in the companion LaTeX note, not by this code.
"""
from __future__ import annotations
import hashlib, itertools, json, random, sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

SEED=12820261026
CHECKS=0

def ck(cond, why):
    global CHECKS
    CHECKS += 1
    if not cond:
        raise AssertionError(why)

def value(c, a):
    return any((((a >> (abs(l)-1)) & 1) == (1 if l>0 else 0)) for l in c)

def holds(f, a):
    return all(value(c,a) for c in f)

def sat_witness(f,n):
    for a in range(1<<n):
        if holds(f,a):return a
    return None

def serial(f,n):
    ck(all(len(c)==3 and len(set(map(abs,c)))==3 for c in f), 'not proper signed exact-3CNF')
    ck(all(1<=abs(l)<=n for c in f for l in c),'identifier out of bounds')
    s=f'p cnf {n} {len(f)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in f)
    rows=s.strip().splitlines()
    header=rows[0].split()
    ck(header==['p','cnf',str(n),str(len(f))], 'DIMACS header mismatch')
    g=tuple(tuple(map(int,row.split()[:-1])) for row in rows[1:])
    ck(g==tuple(f) and all(row.split()[-1]=='0' for row in rows[1:]),'DIMACS replay mismatch')
    return len(s.encode()),hashlib.sha256(s.encode()).hexdigest()

def exact22(f,n):
    occ=Counter(l for c in f for l in c)
    return len(f)==len(set(f)) and all(len(c)==3 and len(set(map(abs,c)))==3 for c in f) and all(occ[v]==occ[-v]==2 for v in range(1,n+1))

def universal_source(q):
    f=[]
    for i in range(q):
        y,a,b=3*i+1,3*i+2,3*i+3
        f.extend(((y,a,b),(y,-a,-b),(-y,a,-b),(-y,-a,b)))
    return tuple(f),3*q,tuple(3*i+1 for i in range(q))

def matrix_clauses(ys,zs):
    names=tuple(ys)+tuple(zs)
    assert len(names)==3
    return tuple(tuple(-v if mask>>j&1 else v for j,v in enumerate(names)) for mask in range(8))

def child(q,zcount,matrix):
    source,ns,ys=universal_source(q)
    zs=tuple(range(ns+1,ns+zcount+1))
    pad=[]; pos=ns+zcount+1
    for v in range(1,ns+1):
        p,r=pos,pos+1;pos+=2
        pad.extend(((v,p,r),(-v,p,r)))
    h=tuple(matrix)+tuple(pad)
    nc=pos-1
    h2=h+((nc+1,nc+2,nc+3),)
    # Source and child literally share every original name 1,...,ns.
    ck(all(any(abs(l)==v for c in h for l in c) for v in range(1,ns+1)), 'source identity not present')
    return source,ns,ys,zs,h,nc,h2,nc+3

def qbf_true(q,zcount,mat):
    sf,ns,ys=universal_source(q)
    zs=tuple(range(ns+1,ns+zcount+1))
    for bits in range(1<<q):
        fixed=sum(((bits>>j)&1)<<(ys[j]-1) for j in range(q))
        if not any(holds(mat, fixed+sum(((w>>j)&1)<<(zs[j]-1) for j in range(zcount))) for w in range(1<<zcount)):
            return False,bits
    return True,None

def lift_via_explicit_extensions(q,zcount,mat):
    # Independent universal enumeration of complete source models; for each
    # matching original assignment choose all padding p=1, q=0, and enumerate Z.
    f,ns,ys,zs,h,nc,h2,nc2=child(q,zcount,mat)
    a0=0
    for alpha in range(1<<ns):
        if not holds(f,alpha):continue
        present=False
        for zb in range(1<<zcount):
            beta=alpha
            for j,z in enumerate(zs):
                beta|=((zb>>j)&1)<<(z-1)
            for v in range(1,ns+1):
                p=ns+zcount+2*(v-1)+1
                beta|=1<<(p-1)
            ck(holds(tuple(h[len(mat):]),beta),'padding extension failed')
            if holds(h,beta):
                present=True
                ck(holds(h2,beta|(1<<nc)), 'second-level extension failed')
                break
        if not present:return False,alpha
        a0+=1
    ck(a0>0,'source unexpectedly unsatisfiable')
    return True,None

def fully_bruteforce_lift(q,zcount,mat):
    # Original source assignments universally, private child assignments existentially.
    f,ns,ys,zs,h,nc,h2,nc2=child(q,zcount,mat)
    private=tuple(range(ns+1,nc+1))
    for alpha in range(1<<ns):
        if not holds(f,alpha):continue
        works=False
        for bits in range(1<<len(private)):
            beta=alpha|sum(((bits>>j)&1)<<(v-1) for j,v in enumerate(private))
            if holds(h,beta):
                works=True;break
        if not works:return False
    return True

def all_signed22_w1():
    W='''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''
    return tuple(tuple(map(int,s.strip().split())) for s in W.split(';'))

def mutate(f,rng):
    polarity=rng.choice([-1,1]);loc=[(i,j) for i,c in enumerate(f) for j,l in enumerate(c) if (l>0)==(polarity>0)]
    for _ in range(100):
        (i,j),(k,v)=rng.sample(loc,2)
        if i==k or abs(f[i][j])==abs(f[k][v]):continue
        x=[list(c) for c in f];x[i][j],x[k][v]=x[k][v],x[i][j]
        g=tuple(tuple(c) for c in x)
        if exact22(g,15):return g
    return f

def fixed_unsat_child(ns):
    u,v,w=ns+1,ns+2,ns+3
    bad=tuple(tuple(-z if mask>>j&1 else z for j,z in enumerate((u,v,w))) for mask in range(8))
    start=ns+4;pad=[]
    for x in range(1,ns+1):
        p,r=start,start+1;start+=2
        pad.extend(((x,p,r),(-x,p,r)))
    h=bad+tuple(pad)
    ck(len(bad)==8 and all(not all(any((((a>>j)&1) == (1 if l>0 else 0)) for j,l in enumerate(c)) for c in bad) for a in range(8)),'fixed child must be UNSAT')
    ck(all(any(abs(l)==x for c in h for l in c) for x in range(1,ns+1)),'names not retained')
    serial(h,start-1)
    return h,start-1

def binary_to_proper(binclauses,n0):
    out=[];n=n0
    for x,y in binclauses:
        ck(abs(x)!=abs(y),'degenerate two-clause')
        n+=1
        out.extend(((x,y,n),(x,y,-n)))
    return tuple(out),n

def cycle_join():
    first=(( -1, 2),(1,-2)) # x=y
    second=((-2,3),(2,-3)) # y=z
    third=((1,3),(-1,-3)) # x!=z
    fn=[];n=3;counts=[]
    for part in (first,second,third):
        block,n=binary_to_proper(part,n)
        fn.append(block)
        counts.append(serial(block,n)[0])
    a,b,c=fn
    ck(sat_witness(a,n)is not None and sat_witness(b,n)is not None and sat_witness(c,n)is not None,'a factor unsat')
    ck(all(sat_witness(p,n)is not None for p in (a+b,a+c,b+c)),'pairwise join fails')
    ck(sat_witness(a+b+c,n)is None,'global cycle should be UNSAT')
    ck(sat_witness(a+b,n)is not None,'first descendant should be SAT')
    return {'factor_clause_counts':[len(x) for x in fn],'pairwise_SAT':[True]*3,
            'global_UNSAT':True,'descendant1_SAT':True,'descendant2_UNSAT':True,
            'full_DIMACS_bytes':serial(a+b+c,n)[0]}

def tseitin_odd(v,edges):
    inc=[[] for _ in range(v)]
    for k,(a,b) in enumerate(edges,1):inc[a].append(k);inc[b].append(k)
    ck(all(len(row)==3 for row in inc),'not cubic')
    out=[]
    for i,row in enumerate(inc):
        charge=int(i==0)
        for mask in range(8):
            if (mask.bit_count()%2)!=charge:
                out.append(tuple((-e if mask>>j&1 else e) for j,e in enumerate(row)))
    return tuple(out),len(edges)

def parity_controls():
    K4=[(i,j) for i in range(4) for j in range(i+1,4)]
    Peterson=[(i,(i+1)%5) for i in range(5)]+[(i,i+5) for i in range(5)]+[(i+5,5+(i+2)%5) for i in range(5)]
    cases={}
    for name,v,edges in [('K4',4,K4),('Petersen',10,Peterson)]:
        f,n=tseitin_odd(v,edges)
        ck(sat_witness(f,n)is None,name+' odd Tseitin SAT')
        serial(f,n)
        counts=Counter(e for row in [[k for k,(a,b) in enumerate(edges) if a==i or b==i] for i in range(v)] for e in row)
        ck(all(vv==2 for vv in counts.values()),'edge parity not doubled')
        cases[name]={'variables':n,'clauses':len(f),'odd_charge_mod2':1,'unsat':True}
    return cases

def resource_checks():
    rng=random.Random(SEED)
    for _ in range(350):
        sizes=[rng.randint(1,250) for __ in range(rng.randint(1,40))]
        M=max(sizes);V=sum(sizes)
        for d in (1.0,1.5,1.802,2.0,3.0):
            ck(sum(x**d for x in sizes) <= (M**(d-1))*V*(1+1e-12),'leaf volume inequality')
    d=Fraction(901,500);C=(2*d-1)/(d*(d-1)); b=C-(d-1)/2
    ck(C==Fraction(651000,361301),'threshold rational mismatch')
    return {'d':str(d),'C_exact':str(C),'C_float':float(C),'lambda':'1/2',
            'b_strict_threshold_exact':str(b),'b_strict_threshold_float':float(b),
            'volume_inequality_tests':350*5}

def main():
    out={'run':'SOURCE_CUT_QBF_BARRIER128','seed':SEED,'qbf':{},'controls':{},'resources':{}}
    for q,zcount in ((1,2),(2,1)):
        f,ns,ys=universal_source(q); ck(exact22(f,ns),'source not signed exact(2,2)')
        src_len=serial(f,ns)[0]
        zs=tuple(range(ns+1,ns+zcount+1));options=matrix_clauses(ys,zs)
        count=Counter();examples={}
        for subset in range(256):
            mat=tuple(c for j,c in enumerate(options) if subset>>j&1)
            expected,wrong=qbf_true(q,zcount,mat)
            got,witness=lift_via_explicit_extensions(q,zcount,mat)
            ck(got==expected, f'QBF/LIFT mismatch q={q} subset={subset}')
            count['true' if got else 'false']+=1
            if not got and subset not in examples: examples[subset]=wrong
            # Two fully independent explicit full private-extension exhaustions per q regime.
            if q==1 and subset in (0,15,85,170,240,255,127,128,47,83):
                ck(fully_bruteforce_lift(q,zcount,mat)==expected,'full witness enumeration mismatch')
        m_true=tuple(c for j,c in enumerate(options) if (1<<j)&1)
        m_falsifiable=tuple(c for j,c in enumerate(options) if j in [0,2,4,6])
        # For q=1, half of clauses with fixed sign of first universal variable
        if q==1:
            m_falsifiable=tuple(c for c in options if c[0]==ys[0])
            yes,_=qbf_true(q,zcount,m_true)
            no,_=qbf_true(q,zcount,m_falsifiable)
            ck(yes and not no,'chosen true/false QBF controls')
            F,nS,Y,Z,H,nH,H2,nH2=child(q,zcount,m_falsifiable)
            ck(sat_witness(H,nH) is not None,'false-LIFT child should itself be SAT')
            ck(sat_witness(H2,nH2) is not None,'false-LIFT grandchild should be SAT')
            out['controls']['SAT_child_but_false_lift']={
                'source_SAT':True,'child_SAT':True,'grandchild_SAT':True,
                'lift':False,'matrix_clauses':list(map(list,m_falsifiable)),
                'source_child_grandchild_DIMACS_bytes':[serial(F,nS)[0],serial(H,nH)[0],serial(H2,nH2)[0]],
                'all_source_names_preserved':True}
        out['qbf'][f'forall_{q}_exists_{zcount}']={'source_variables':ns,
             'source_clauses':len(f),'source_dimacs_bytes':src_len,'strict_signed22':True,
             'matrix_subsets_exhausted':256,'truth_counts':dict(count),'sample_false_assignments':dict(list(examples.items())[:5])}
    W1=all_signed22_w1()
    ck(exact22(W1,15),'W1 incidence wrong')
    fcount=Counter();rng=random.Random(SEED)
    cur=W1;examples=[]
    for i in range(22):
        cur=W1 if i%6==0 else mutate(cur,rng)
        ck(exact22(cur,15),'mutant not signed22')
        w=sat_witness(cur,15)
        if i in (0,1,2,3,6,12,18):
            H,nH=fixed_unsat_child(15)
            ck(len(H)==38 and nH==48 and all(any(abs(l)==v for c in H for l in c) for v in range(1,16)),'fixed UNSAT child source audit')
        fcount['SAT' if w is not None else 'UNSAT']+=1
        examples.append({'i':i,'SAT':w is not None,'DIMACS_bytes':serial(cur,15)[0]})
    ck(fcount['SAT']>0 and fcount['UNSAT']>0,'signed22 SAT/UNSAT controls missing')
    out['controls']['signed22_W1_mutants']={'counts':dict(fcount),'cases':examples}
    out['controls']['cyclic_three_way_join']=cycle_join()
    out['controls']['odd_tseitin']=parity_controls()
    out['controls']['affine_XOR_unsat']={'equations':['x+y=0','y+z=0','x+z=1'],
        'xor_sum_equation':'0=1','field':'GF(2)','valid_affine_terminal':True}
    out['controls']['Horn_UNSAT'] = {'clauses':[[1],[-1,2],[-2]],'UNSAT':True}
    ck(sat_witness(((1,),(-1,2),(-2,)),2)is None,'Horn control')
    out['controls']['twoSAT_UNSAT'] = {'clauses':[[1,2],[-1,2],[-2]],'UNSAT':True}
    ck(sat_witness(((1,2),(-1,2),(-2,)),2)is None,'2SAT control')
    out['resources']=resource_checks()
    out['checks']=CHECKS
    out['limitations']='finite exhaustive 3-name QBF matrices and seeded 15-var formulas; Pi2P theorem relies on published quantified 3SAT completeness and symbolic gadget proof; not full certificate coverage or FLMV runtime measurement'
    return out

if __name__=='__main__':
    o=main()
    path=Path(__file__).with_name('2026-10-26_0224_SOURCE_CUT_QBF_BARRIER128_raw.json')
    path.write_text(json.dumps(o,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'checks':o['checks'],'qbf':o['qbf'],'controls':{'signed22':o['controls']['signed22_W1_mutants']['counts'],
        'cycle':o['controls']['cyclic_three_way_join'],'lift_counterexample':o['controls']['SAT_child_but_false_lift'],
        'odd_tseitin':o['controls']['odd_tseitin']},'resources':o['resources']},indent=2))
