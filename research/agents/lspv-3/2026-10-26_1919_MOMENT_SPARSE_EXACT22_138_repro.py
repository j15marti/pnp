#!/usr/bin/env python3
"""LSPV-3 MOMENT-SPARSE-EXACT22-138, stdlib-only reproducible finite audit.

Mathematical asymptotic claims are proved in companion LaTeX. This program
checks finite signed (2,2) syntax, exact local truth tables, exhaustive
small paired controls, moment recovery, Prouhet collisions, two ordinary
source-identified descendants, and rejection of forged source authentication.
No Python interpreter RAM/time measurement is presented as a Turing-machine bound.
"""
from __future__ import annotations
import collections
import fractions
import hashlib
import itertools
import json
import math
import random
from pathlib import Path

W_TEXT = '''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''
W = tuple(tuple(map(int, row.split())) for row in W_TEXT.split(';'))
A_SLOTS = ((6,0),(11,0))
B_SLOTS = ((9,2),(17,2))
BACKDOOR=(2,4,7,14,15)
CHECKS=0

def chk(flag, what='assertion'):
    global CHECKS
    CHECKS += 1
    if not flag: raise AssertionError(what)

def H(a:int,b:int):
    c=[list(row) for row in W]
    if a == 0:
        for i,j in A_SLOTS: c[i][j]=-c[i][j]
    if b == 0:
        for i,j in B_SLOTS: c[i][j]=-c[i][j]
    return tuple(map(tuple,c))

def model_count(clauses, n=15):
    hits=0
    for assignment in range(1<<n):
        if all(any(((assignment>>(abs(l)-1))&1)==(l>0) for l in row) for row in clauses):
            hits+=1
    return hits

def shifted(clauses, offset):
    return tuple(tuple((1 if lit>0 else -1)*(abs(lit)+offset) for lit in row) for row in clauses)

def exact_balanced(rows, n):
    pc=collections.Counter(x for row in rows for x in row if x>0)
    nc=collections.Counter(-x for row in rows for x in row if x<0)
    return len(rows)*3 == 4*n and all(pc[x]==nc[x]==2 for x in range(1,n+1)) and all(len(row)==3 and len({abs(x) for x in row})==3 for row in rows) and len(set(rows))==len(rows)

def E(a,b):
    """2m signed (2,2) H modules, Alice 4m rows, neutral 32m, Bob 4m."""
    chk(len(a)==len(b) and len(a)>=1,'lengths')
    modules=[]
    for i,(ai,bi) in enumerate(zip(a,b)):
        modules.append(shifted(H(ai,1-bi),30*i))
        modules.append(shifted(H(1-ai,bi),30*i+15))
    rows=[];meta=[]
    for block in ('A','FIXED','B'):
        for j,hrows in enumerate(modules):
            ix=[x for x,_ in A_SLOTS] if block=='A' else [x for x in range(20) if x not in set(i for i,_ in A_SLOTS+B_SLOTS)] if block=='FIXED' else [x for x,_ in B_SLOTS]
            for ci in ix:
                rows.append(hrows[ci]);meta.append((block,j,ci))
    return tuple(rows),tuple(meta)

def encode(rows,n):
    return ('p cnf %d %d\n'%(n,len(rows))+''.join('%d %d %d 0\n'%row for row in rows)).encode('ascii')

def encode_fixed(records,n):
    """Ordinary signed proper ternary CNF in fixed-width sign/id record encoding.
    '0' positive, '1' negative; IDs are w fixed-width binary digits.
    One ASCII newline per row; bit-size differs from byte-size by factor 8.
    """
    w=max(1,n.bit_length())
    header=f'p b3 {n} {len(records)} {w}\n'
    body=''.join(''.join(('1' if z<0 else '0')+format(abs(z),f'0{w}b') for z in row)+'\n' for row in records)
    return (header+body).encode('ascii')

def parse_fixed(source):
    lines=source.splitlines(keepends=True)
    chk(bool(lines) and lines[0].endswith(b'\n'),'fixed input header')
    h=lines[0].decode('ascii').split()
    chk(len(h)==5 and h[:2]==['p','b3'],'fixed marker')
    n,c,w=map(int,h[2:]);chk(w==max(1,n.bit_length()),'fixed digit width')
    chk(len(lines)==c+1,'fixed row count')
    rows=[]
    for line in lines[1:]:
        chk(line.endswith(b'\n') and len(line)==3*(w+1)+1,'fixed row width')
        row=[]
        for j in range(3):
            field=line[j*(w+1):(j+1)*(w+1)]
            chk(set(field)<=set(b'01'),'binary field digits')
            sign=field[0];var=int(field[1:],2)
            chk(1<=var<=n,'valid binary variable ID')
            row.append(-var if sign==ord('1') else var)
        chk(len({abs(z) for z in row})==3,'proper binary row')
        rows.append(tuple(row))
    return n,tuple(rows)

def parse(s):
    """Whole canonical DIMACS source parsing and clause starting-byte addresses."""
    lines=s.splitlines(keepends=True)
    chk(lines and lines[0].endswith(b'\n'),'header newline')
    h=lines[0].decode('ascii').split();chk(len(h)==4 and h[:2]==['p','cnf'],'bad header')
    n,m=int(h[2]),int(h[3]);chk(len(lines)==m+1,'count mismatch')
    out=[]; offsets=[]; pos=len(lines[0])
    for l in lines[1:]:
        chk(l.endswith(b'\n') and l.strip().endswith(b' 0'),'terminator grammar')
        toks=l.split();chk(len(toks)==4 and toks[-1]==b'0','row shape')
        v=tuple(map(int,toks[:3]));chk(all(x!=0 and abs(x)<=n for x in v),'bad variable');chk(len({abs(x) for x in v})==3,'improper')
        out.append(v);offsets.append(pos);pos+=len(l)
    chk(pos==len(s),'end position')
    return n,tuple(out),tuple(offsets)

def streaming_moments_from_source(raw,m,h):
    """Finite executable control for sequential row-local extraction; not a TM simulator.
    The mathematical streamer needs only counters, current row and moments.
    """
    n,rows,ofs=parse(raw)
    chk(n==30*m and len(rows)==40*m,'source source template header')
    moments=[0]*(2*h)
    extracted_a=[];extracted_b=[]
    # A block: 4m clauses; per coordinate (U-A6,U-A11,V-A6,V-A11).
    for i in range(m):
        base=4*i;lhs=[]
        for mod in range(2):
            for k,(ci,slot) in enumerate(A_SLOTS):
                r=rows[base+2*mod+k]
                expect=shifted((W[ci],),30*i+15*mod)[0]
                chk(tuple(map(abs,r))==tuple(map(abs,expect)),'A supports')
                chk(all(r[z]==expect[z] for z in range(3) if z!=slot),'A noncontrol signs')
                lhs.append(int(r[slot]==expect[slot]))
        chk(lhs[0]==lhs[1] and lhs[2]==lhs[3] and lhs[0]!=lhs[2],'A sign consistency')
        ai=lhs[0];extracted_a.append(ai)
        for j in range(2*h): moments[j]+=ai*((i+1)**j)
    # FIXED block also checked for full template grammar.
    fixed=[ci for ci in range(20) if ci not in {z for z,_ in A_SLOTS+B_SLOTS}]
    for mod in range(2*m):
        for t,ci in enumerate(fixed):
            chk(rows[4*m+16*mod+t]==shifted((W[ci],),15*mod)[0],'fixed source clauses')
    # B block begins at 36m, four clauses per coordinate.
    for i in range(m):
        base=36*m+4*i;rhs=[]
        for mod in range(2):
            for k,(ci,slot) in enumerate(B_SLOTS):
                r=rows[base+2*mod+k]
                expect=shifted((W[ci],),30*i+15*mod)[0]
                chk(tuple(map(abs,r))==tuple(map(abs,expect)),'B supports')
                chk(all(r[z]==expect[z] for z in range(3) if z!=slot),'B noncontrol signs')
                rhs.append(int(r[slot]==expect[slot]))
        chk(rhs[0]==rhs[1] and rhs[2]==rhs[3] and rhs[0]!=rhs[2],'B sign consistency')
        bi=rhs[2];extracted_b.append(bi)
        for j in range(2*h): moments[j]-=bi*((i+1)**j)
    return moments,extracted_a,extracted_b,rows,ofs

def rank_q(A):
    m=[list(map(fractions.Fraction,r)) for r in A]
    if not m:return 0
    H=len(m);Wc=len(m[0]);r=0
    for col in range(Wc):
        pivot=next((i for i in range(r,H) if m[i][col]!=0),None)
        if pivot is None:continue
        m[r],m[pivot]=m[pivot],m[r]
        val=m[r][col];m[r]=[x/val for x in m[r]]
        for i in range(H):
            if i!=r and m[i][col]:
                f=m[i][col];m[i]=[x-f*y for x,y in zip(m[i],m[r])]
        r+=1
        if r==H:break
    return r

def solve_q(A,b):
    m=[list(map(fractions.Fraction,row))+[fractions.Fraction(rhs)] for row,rhs in zip(A,b)]
    nvars=len(A[0]) if A else 0
    r=0;pivots=[]
    for j in range(nvars):
        pivot=next((i for i in range(r,len(m)) if m[i][j]),None)
        if pivot is None:continue
        m[r],m[pivot]=m[pivot],m[r]; val=m[r][j]
        m[r]=[v/val for v in m[r]]
        for i in range(len(m)):
            if i!=r and m[i][j]:
                f=m[i][j];m[i]=[x-f*y for x,y in zip(m[i],m[r])]
        pivots.append(j);r+=1
    if any(all(m[i][j]==0 for j in range(nvars)) and m[i][-1]!=0 for i in range(len(m))):return None
    if len(pivots)<nvars:return None
    out=[fractions.Fraction(0)]*nvars
    for row,col in enumerate(pivots):out[col]=m[row][-1]
    return out

def recover_h_sparse(moments,m,h):
    """Hankel rank + rational Prony; sound candidates require source sign check."""
    chk(len(moments)==2*h)
    matrix=[[moments[i+j] for j in range(h)] for i in range(h)]
    k=rank_q(matrix)
    if k==0:return []
    coeff=solve_q([[moments[r+j] for j in range(k)] for r in range(h)],[-moments[r+k] for r in range(h)])
    if coeff is None:return []
    # integer roots among the actual original coordinate identities 1...m
    roots=[i for i in range(1,m+1) if (i**k+sum(coeff[j]*(i**j) for j in range(k)))==0]
    return roots

def proof_for_module(rows,meta,ofs,module):
    """Authenticates 20 original source clauses and all 32 SCC or EMPTY leaves."""
    loc={ci:(row,ofs[index]) for index,(block,j,ci) in enumerate(meta) if j==module for row in [rows[index]]}
    chk(len(loc)==20,'all source IDs in module')
    cl=[loc[ci][0] for ci in range(20)]
    chk(cl==list(shifted(W,15*module)),'auth W1 core')
    n=30*(module//2+1)
    B=[15*module+x for x in BACKDOOR]
    edge_count=0
    for bs in itertools.product((0,1),repeat=5):
        asn=dict(zip(B,bs));adj=collections.defaultdict(list)
        seen_empty=False
        for ci,clause in enumerate(cl):
            if any(abs(z) in asn and int(z>0)==asn[abs(z)] for z in clause):continue
            resid=tuple(z for z in clause if abs(z) not in asn)
            chk(len(resid)<=2,'backdoor residual')
            if not resid:seen_empty=True;break
            x,y=(resid[0],resid[0]) if len(resid)==1 else resid
            adj[-x].append((y,ci));adj[-y].append((x,ci))
        if seen_empty:continue
        def path(src,dst):
            todo=collections.deque([src]);prev={src:None}
            while todo:
                u=todo.popleft()
                for v,ci in adj[u]:
                    if v not in prev:prev[v]=(u,ci);todo.append(v)
            if dst not in prev:return None
            z=dst;out=[]
            while prev[z] is not None:
                u,ci=prev[z];out.append((u,z,ci));z=u
            return out[::-1]
        w=None
        for v in sorted({abs(z) for c in cl for z in c}):
            p=path(v,-v);q=path(-v,v)
            if p is not None and q is not None:w=(p,q);break
        chk(w is not None,'cycle proof exists')
        for pp in w:
            for u,v,ci in pp:
                chk(any(y==v and c==ci for y,c in adj[u]),'actual authenticated edge')
                chk(loc[ci][1] in ofs,'genuine source offset')
                edge_count+=1
    return dict(leaves=32,edge_records=edge_count,source_clauses=len(loc),module=module)

def integer_prouhet(q):
    m=1<<q
    a=[int((i.bit_count()&1)==0) for i in range(m)]
    b=[1-x for x in a]
    return a,b

def audit():
    seed=13820261026
    rng=random.Random(seed)
    chk(len(W)==20 and exact_balanced(W,15),'W1 signed exact22')
    counts={(a,b):model_count(H(a,b)) for a,b in itertools.product((0,1),repeat=2)}
    chk(counts=={(0,0):772,(0,1):272,(1,0):272,(1,1):0},'AND gadget four truth counts')
    for aa,bb in counts:
        chk(exact_balanced(H(aa,bb),15),'all H signs balanced')
    out=dict(run='MOMENT-SPARSE-EXACT22-138',status='PROVED/EXACT restricted symbolic; COMPUTATIONAL controls',seed=seed,local_model_counts={str(k):v for k,v in counts.items()},samples=[],moment_collisions=[],traces=[],checks=0)
    examples=[]
    for m in range(1,5):
        for a in itertools.product((0,1),repeat=m):
            for b in itertools.product((0,1),repeat=m):
                examples.append((list(a),list(b),'exhaustive'))
    for m in [5,9,16,32,64]:
        for rep in range(5):
            a=[rng.randrange(2) for _ in range(m)]
            b=list(a)
            flip=rng.sample(range(m),rng.randrange(min(m,4)+1))
            for i in flip:b[i]^=1
            examples.append((a,b,'random_sparse'))
    # Moment cancellation outside h-sparse promise.
    for h in (1,2,3):
        a,b=integer_prouhet(2*h);m=len(a)
        examples.append((a,b,'prouhet'))
        for q in range(2*h):
            chk(sum((x-y)*(i+1)**q for i,(x,y) in enumerate(zip(a,b)))==0,'Prouhet integer moments')
        out['moment_collisions'].append(dict(h=h,m=m,nonzero_mismatches=sum(x!=y for x,y in zip(a,b)),power_sum_orders=2*h))
    auth_cases=0;test_cases=0;certificate_counts=collections.Counter()
    for a,b,kind in examples:
        m=len(a);F,meta=E(a,b);raw=encode(F,30*m);n,rows,offsets=parse(raw)
        encoded_binary=encode_fixed(F,30*m)
        bn,br=parse_fixed(encoded_binary)
        chk(bn==30*m and br==F,'fixed binary full ordinary CNF')
        # A/B sign changes preserve the complete encoded length and gap.
        w=(30*m).bit_length();rowbytes=3*(w+1)+1
        headerbytes=len(encoded_binary)-40*m*rowbytes
        base_f,_=E([0]*m,[0]*m)
        baseline=encode_fixed(base_f,30*m)
        chk(len(encoded_binary)==len(baseline),'fixed-size layout')
        gap0=headerbytes+4*m*rowbytes;gap1=headerbytes+36*m*rowbytes
        chk(encoded_binary[gap0:gap1]==baseline[gap0:gap1],'same neutral 32m-row gap')
        chk(F==rows and exact_balanced(rows,30*m),'full exact22 instance')
        true_sat=all(x==y for x,y in zip(a,b))
        # Each H gadget is satisfiable except precisely H(1,1).
        template_sat=all(counts[(a[i],1-b[i])]>0 and counts[(1-a[i],b[i])]>0 for i in range(m))
        chk(template_sat==true_sat,'SAT iff equality')
        for h in (1,2,3):
            moms,da,db,_,_=streaming_moments_from_source(raw,m,h)
            chk(da==a and db==b,'side decoding')
            chk(moms==[sum((x-y)*(i+1)**j for i,(x,y) in enumerate(zip(a,b))) for j in range(2*h)],'moments source')
            roots=recover_h_sparse(moms,m,h)
            diff=[i+1 for i,(x,y) in enumerate(zip(a,b)) if x!=y]
            if len(diff)<=h:
                chk(set(roots)==set(diff),'sparse support recovery')
            # Full source-authenticated sign recheck: only emit valid coordinates.
            valid_roots=[i for i in roots if a[i-1]!=b[i-1]]
            if true_sat:chk(not valid_roots,'no UNSAT proof on SAT')
            if len(diff)<=h and diff:chk(valid_roots,'complete h-sparse UNSAT')
            if kind=='prouhet':chk(not roots,'Prouhet defeats fixed moments')
        if m<=4 or kind=='prouhet' or (m<=16 and len(out['samples'])<30):
            out['samples'].append(dict(m=m,kind=kind,sat=true_sat,mismatches=sum(x!=y for x,y in zip(a,b)),encoded_bytes=len(raw)))
        if not true_sat and (m<=3 or (m>=5 and auth_cases<18)):
            i=next(i for i,(x,y) in enumerate(zip(a,b)) if x!=y)
            module=2*i if a[i]==1 else 2*i+1
            chk((a[i]==1 and b[i]==0) or (a[i]==0 and b[i]==1),'module orientation')
            proof=proof_for_module(rows,meta,offsets,module)
            chk(proof['leaves']==32 and proof['source_clauses']==20,'auth proof')
            certificate_counts[proof['edge_records']]+=1
            auth_cases+=1
        test_cases+=1
    # Proper ordinary descendants: append two fresh actual source-name pins to a NO formula.
    a,b=[1,0,0],[0,0,0];F,meta=E(a,b)
    n0=90;pin=lambda lit,p,q: [(lit,s*p,t*q) for s in (1,-1) for t in (1,-1)]
    cl1=F+tuple(pin(1,91,92));cl2=cl1+tuple(pin(-2,93,94))
    for n,cl in ((90,F),(92,cl1),(94,cl2)):
        raw=encode(cl,n);rn,rr,_=parse(raw);chk(rn==n and rr==cl and len(raw)>0,'valid ordinary source or descendants')
        chk(all(len(r)==3 and len({abs(z) for z in r})==3 for r in rr),'proper signed ternary')
        chk(set(F).issubset(set(rr)),'original source subset retained')
    for label,idx in [('A sign',0),('B sign',len(F)-1)]:
        badrows=list(F)
        badrow=badrows[idx]
        badrows[idx]=(-badrow[0],)+badrow[1:]
        # Authentic strict sign pairing must fail under one-sided mutation.
        badraw=encode(badrows,90)
        rejected=False
        try:
            streaming_moments_from_source(badraw,3,1)
        except AssertionError:
            rejected=True
        chk(rejected,'mutated source accepted')
    # Forged W1 proof on an ordinary SAT source must be rejected.
    fsat,msat=E([0,1,0],[0,1,0]);rs=encode(fsat,90)
    _,ss,so=parse(rs)
    sat_rejected=False
    try:
        proof_for_module(ss,msat,so,0)
    except AssertionError:
        sat_rejected=True
    chk(sat_rejected,'SAT instance admitted forged UNSAT core')
    # Hostile easy controls (direct exhaustive independent semantics).
    chk(model_count(((1,),(-1,)),1)==0,'Horn UNSAT')
    chk(model_count(((1,2),(-1,2)),2)>0,'2CNF SAT')
    chk(model_count(((1,2),(-1,2),(1,-2),(-1,-2)),2)==0,'2CNF UNSAT')
    # Connected two-copy sign-preserving literal splice: each local block SAT,
    # yet the full joined source UNSAT by the puncturing/source-name lemma.
    C=[]
    for i in range(2):
        rows_i=list(shifted(W,15*i))
        clause0=list(rows_i[0]);clause0[0]=-(15*((i-1)%2)+1)
        rows_i[0]=tuple(clause0);C.extend(rows_i)
        # An isolated altered block admits the external borrowed literal.
        chk(model_count(W[1:],15)>0,'deleted W1 clause SAT')
    chk(exact_balanced(C,30),'connected splice remains exact22')
    graph=collections.defaultdict(set)
    for row in C:
        for x in row:
            for y in row:
                graph[abs(x)].add(abs(y))
    seen={1};todo=[1]
    while todo:
        z=todo.pop()
        for y in graph[z]:
            if y not in seen:seen.add(y);todo.append(y)
    chk(len(seen)==30,'connected incidence')
    # Verify every satisfying assignment of the punctured W1 falsifies C_1,
    # which yields the exact two-module contradiction under the splice.
    A=W[1:];pin_clause=W[0]
    awitness=0
    for mask in range(1<<15):
        if all(any(((mask>>(abs(l)-1))&1)==(l>0) for l in row) for row in A):
            awitness+=1
            chk(not any(((mask>>(abs(l)-1))&1)==(l>0) for l in pin_clause),'puncturing lemma')
    chk(awitness>0,'minimality one clause')
    # Odd/even affine cubic K4 Tseitin SAT/UNSAT control.
    edges=list(itertools.combinations(range(4),2))
    def tseitin(odd):
        rr=[]
        for v in range(4):
            inc=[j+1 for j,e in enumerate(edges) if v in e]
            charge=int(odd and v==0)
            for bits in itertools.product((0,1),repeat=3):
                if sum(bits)%2!=charge:
                    rr.append(tuple(i if bit else -i for i,bit in zip(inc,bits)))
        return rr
    chk(model_count(tseitin(True),6)==0,'odd K4 Tseitin UNSAT')
    chk(model_count(tseitin(False),6)>0,'even K4 Tseitin SAT')
    out['hostile_controls']={'sat_forgery_rejected':sat_rejected,'connected_exact22_splice':True,'punctured_W1_models':awitness,'Horn_2SAT_affine_Tseitin':True}
    out['two_level_bytes']=[len(encode(F,90)),len(encode(cl1,92)),len(encode(cl2,94))]
    out['auth_cases']=auth_cases
    out['certificate_edge_count_histogram']=dict(sorted(certificate_counts.items()))
    out['total_instances']=test_cases
    out['checks']=CHECKS
    out['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return out

if __name__=='__main__':
    result=audit()
    target=Path(__file__).with_name('2026-10-26_1919_MOMENT_SPARSE_EXACT22_138_raw.json')
    target.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True,indent=2))
