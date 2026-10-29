#!/usr/bin/env python3
"""CHAIN_ORDINARY_CLOSURE213: exact fixed-width SAT relation contractions.
Standalone stdlib reproducer. No nonuniform tables or external SAT solver.
Run: python3 2026-10-29_0312_LSPV-2_CHAIN_ORDINARY_CLOSURE213_repro.py > raw.json
"""
import itertools as it, json, math, random
from collections import Counter

W=16
FULL=(1<<W)-1
ID=tuple(1<<i for i in range(W))

def nat(k):
    assert k>=1
    b=bin(k)[2:]
    return '1'*len(b)+'0'+b

def parse_nat(s,p):
    k=0
    while p<len(s) and s[p]=='1': k+=1;p+=1
    assert k and p+k+1<=len(s) and s[p]=='0'
    p+=1
    r=int(s[p:p+k],2)
    assert r>=1 and len(bin(r))-2==k
    return r,p+k

def b16(k):
    return format(k,'016b')

def encode_cycle(signs,n):
    assert n>=3 and n%3==0 and len(signs)==n+n//3
    assert all(len(c)==3 and all(t in (0,1) for t in c) for c in signs)
    return '0'+nat(n)+''.join(str(b) for c in signs for b in c)

def encode_chain(I,F,matrices):
    assert 0<=I<=FULL and 0<=F<=FULL and matrices
    assert all(len(M)==W and all(0<=r<=FULL for r in M) for M in matrices)
    return '1'+nat(len(matrices))+b16(I)+b16(F)+''.join(b16(r) for M in matrices for r in M)

def decode(s):
    assert s and set(s)<={'0','1'}
    typ=s[0];n,p=parse_nat(s,1)
    if typ=='0':
        assert n>=3 and n%3==0 and len(s)==p+4*n
        raw=s[p:]
        return 'cycle',n,[tuple(int(raw[i+j]) for j in range(3)) for i in range(0,len(raw),3)]
    assert typ=='1' and len(s)==p+32+256*n
    I=int(s[p:p+16],2); F=int(s[p+16:p+32],2);p+=32
    mats=[]
    for i in range(n):
        rows=tuple(int(s[p+256*i+16*j:p+256*i+16*(j+1)],2) for j in range(W))
        mats.append(rows)
    return 'chain',I,F,mats

def scopes(n):
    return [tuple((i+j)%n for j in range(3)) for i in range(n)]+[tuple(range(i,i+3)) for i in range(0,n,3)]

def check_exact22(signs,n):
    counts=[[0,0] for _ in range(n)]
    for vals,scope in zip(signs,scopes(n)):
        for sign,v in zip(vals,scope):counts[v][sign]+=1
    return all(c==[2,2] for c in counts)

def satisfied(signs, n, assignment):
    return all(any(assignment[v]==pol for v,pol in zip(scope,sgn)) for scope,sgn in zip(scopes(n),signs))

def dimacs_cycle(signs,n):
    cs=scopes(n)
    assert len(signs)==len(cs)
    return 'p cnf %d %d\n'%(n,len(cs))+''.join(' '.join(str((v+1) if pos else -(v+1)) for v,pos in zip(scope,sign))+' 0\n' for scope,sign in zip(cs,signs))

def parse_strict_dimacs_cycle(text):
    # No comments/extra tokens in canonical source, unlike general DIMACS.
    assert isinstance(text,str)
    lines=text.splitlines()
    assert lines and lines[0].startswith('p cnf ')
    header=lines[0].split()
    assert len(header)==4 and header[:2]==['p','cnf']
    n=int(header[2]);m=int(header[3])
    assert n>=3 and n%3==0 and m==4*n//3 and len(lines)==m+1
    cs=scopes(n); signs=[]
    for line,scope in zip(lines[1:],cs):
        toks=line.split()
        assert len(toks)==4 and toks[-1]=='0'
        ls=[int(t) for t in toks[:-1]]
        assert all(l!=0 for l in ls)
        assert tuple(abs(l)-1 for l in ls)==scope
        signs.append(tuple(int(l>0) for l in ls))
    assert check_exact22(signs,n)
    return n,signs

def canonical_signs(n):
    return [(1,1,0)]*n+[(0,0,0)]*(n//3)

def random_exact22(n,rng):
    cs=scopes(n)
    occurrences=[[] for _ in range(n)]
    signs=[[0]*3 for _ in cs]
    for ci,c in enumerate(cs):
        for p,v in enumerate(c):occurrences[v].append((ci,p))
    for occ in occurrences:
        assert len(occ)==4
        for ci,p in rng.sample(occ,2): signs[ci][p]=1
    assert check_exact22(signs,n)
    return [tuple(c) for c in signs]

def state(u,v,a,b): return (u<<3)|(v<<2)|(a<<1)|b

def bits(s): return (s>>3&1,s>>2&1,s>>1&1,s&1)

def clause_ok(sign,values): return any(p==v for p,v in zip(sign,values))

def cycle_matrices(signs,n):
    assert len(signs)==n+n//3
    I=0;F=0
    for u,v in it.product((0,1),repeat=2): I|=1<<state(u,v,u,v)
    for s in range(W):
        u,v,a,b=bits(s)
        if clause_ok(signs[n-2],(a,b,u)) and clause_ok(signs[n-1],(b,u,v)):
            F|=1<<s
    for j in range(2,n):
        C=signs[j-2]
        D=signs[n+(j-2)//3] if (j-2)%3==0 else None
        M=[0]*W
        for s in range(W):
            u,v,a,b=bits(s)
            for c in (0,1):
                ok=clause_ok(C,(a,b,c))
                if D is not None:ok=ok and clause_ok(D,(a,b,c))
                if ok:M[s]|=1<<state(u,v,b,c)
        yield I,F,tuple(M)

def composition(A,B):
    assert len(A)==len(B)==W
    out=[]
    for source in range(W):
        mask=A[source];reach=0
        for mid in range(W):
            if mask>>mid&1:reach|=B[mid]
        out.append(reach)
    return tuple(out)

def decide_chain(I,F,matrices):
    reach=I
    for M in matrices:
        nxt=0
        for a in range(W):
            if reach>>a&1:nxt |= M[a]
        reach=nxt
    return bool(reach & F)

def compact(I,F,matrices):
    m=len(matrices)
    k=max(1,math.isqrt(math.isqrt(m)))
    block=(m+k-1)//k
    child=[]
    for j in range(0,m,block):
        acc=ID
        for M in matrices[j:j+block]: acc=composition(acc,M)
        child.append(acc)
    assert len(child)<=k
    return I,F,child,block

def compile_cycle(s):
    typ,n,signs=decode(s)
    assert typ=='cycle'
    triples=list(cycle_matrices(signs,n))
    assert len(triples)==n-2
    I,F=triples[0][:2]
    return I,F,[t[2] for t in triples]

def shrink(s):
    typ,*args=decode(s)
    if typ=='cycle':
        n,signs=args
        I,F,matrices=compile_cycle(s)
    else:I,F,matrices=args
    I,F,child,block=compact(I,F,matrices)
    return encode_chain(I,F,child),block

def solve(s):
    typ,*args=decode(s)
    if typ=='cycle':
        n,signs=args
        I,F,matrices=compile_cycle(s)
    else:I,F,matrices=args
    return decide_chain(I,F,matrices)

def recursive(s):
    # For finite test instances, contract the relation chain until <=1 matrix.
    seen=[]
    while True:
        typ,*args=decode(s)
        if typ=='chain' and len(args[2])==1:
            return decide_chain(*args),seen
        child,block=shrink(s)
        assert decode(child)[0]=='chain'
        seen.append((len(s),len(child),block))
        s=child

def to_cnf(I,F,mats):
    m=len(mats); num=4*(m+1);clauses=[]
    def ban_bits(t, index):
        return [(-1 if (t>>j)&1 else 1)*(4*index+j+1) for j in range(4)]
    def add(c):
        nonlocal num
        assert len(c)>=3 and len(set(map(abs,c)))==len(c)
        if len(c)==3:clauses.append(tuple(c));return
        prev=None
        for j in range(len(c)-3):
            num+=1
            if j==0: clauses.append((c[0],c[1],num))
            else: clauses.append((-prev,c[j+1],num))
            prev=num
        clauses.append((-prev,c[-2],c[-1]))
    for t in range(W):
        if not (I>>t&1):add(ban_bits(t,0))
        if not (F>>t&1):add(ban_bits(t,m))
    for idx,M in enumerate(mats):
        for a,row in enumerate(M):
            for b in range(W):
                if not (row>>b&1):add(ban_bits(a,idx)+ban_bits(b,idx+1))
    assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in clauses)
    return num,clauses

def cnf_text(num,clauses):
    return 'p cnf %d %d\n'%(num,len(clauses))+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)

def encode_chain_as_ordinary_sat(I,F,matrices):
    m=len(matrices)
    hexdata=''.join(format(row,'04x') for M in matrices for row in M)
    header='c LSPV2_MATRIX_CHAIN_V1 %d %04x %04x %s\n'%(m,I,F,hexdata)
    num,clauses=to_cnf(I,F,matrices)
    return header+cnf_text(num,clauses)

def parse_chain_as_ordinary_sat(text):
    first,sep,body=text.partition('\n')
    assert sep and first.startswith('c LSPV2_MATRIX_CHAIN_V1 ')
    h=first.split()
    assert len(h)==6 and h[:2]==['c','LSPV2_MATRIX_CHAIN_V1']
    m=int(h[2]); I=int(h[3],16); F=int(h[4],16)
    assert m>0 and len(h[5])==64*m and set(h[5])<=(set('0123456789abcdef'))
    raw=h[5]
    rows=[int(raw[i:i+4],16) for i in range(0,len(raw),4)]
    matrices=[tuple(rows[i:i+W]) for i in range(0,len(rows),W)]
    assert encode_chain_as_ordinary_sat(I,F,matrices)==text
    return I,F,matrices

def parse_subclass_ordinary_sat(text):
    if text.startswith('c LSPV2_MATRIX_CHAIN_V1 '):
        I,F,M=parse_chain_as_ordinary_sat(text)
        return 'chain',I,F,M
    n,signs=parse_strict_dimacs_cycle(text)
    return 'cycle',n,signs

def shrink_ordinary_sat(text):
    typ,*rest=parse_subclass_ordinary_sat(text)
    if typ=='cycle':
        n,signs=rest
        I,F,matrices=compile_cycle(encode_cycle(signs,n))
    else:I,F,matrices=rest
    I,F,child,block=compact(I,F,matrices)
    return encode_chain_as_ordinary_sat(I,F,child),block

def solve_ordinary_sat(text):
    typ,*rest=parse_subclass_ordinary_sat(text)
    if typ=='cycle':
        n,signs=rest
        I,F,M=compile_cycle(encode_cycle(signs,n))
    else:I,F,M=rest
    return decide_chain(I,F,M)

def exhaustive_tseitin_clause(k):
    assert k in (4,8)
    for inp in range(1<<k):
        lits=[j+1 for j in range(k)]
        # Independently compile the single broad clause and quantify auxiliaries.
        num=k;out=[]
        prev=None
        for j in range(k-3):
            num+=1
            if j==0:out.append((lits[0],lits[1],num))
            else:out.append((-prev,lits[j+1],num))
            prev=num
        out.append((-prev,lits[-2],lits[-1]))
        # The chosen input assignment fixes every literal j+1 to true iff bit j is 1.
        valid=any((inp>>j)&1 for j in range(k))
        accepted=False
        for aux in range(1<<(k-3)):
            values={j+1:bool(inp>>j&1) for j in range(k)}
            for j in range(k-3):values[k+j+1]=bool(aux>>j&1)
            if all(any(values[abs(l)]==(l>0) for l in clause) for clause in out):
                accepted=True;break
        assert accepted==valid
    return (1<<k)

def exhaustive_exact22_signed_scopes(n):
    # Independent exhaustive SAT controls, using bitmask unions, not frontier DP.
    assert n in (3,6)
    cs=scopes(n);m=len(cs)
    occ=[[] for _ in range(n)]
    for i,cl in enumerate(cs):
        for p,v in enumerate(cl):occ[v].append((i,p))
    assert all(len(t)==4 for t in occ)
    exclusion=[]
    for ci,cl in enumerate(cs):
        by_sign=[]
        for sign in range(8):
            mask=0
            for a in range(1<<n):
                if all((a>>v&1)==((sign>>p)&1) for p,v in enumerate(cl)):
                    mask|=1<<a
            by_sign.append(mask)
        exclusion.append(by_sign)
    all_excluded=(1<<(1<<n))-1
    sat=unsat=0
    for picks in it.product(it.combinations(range(4),2),repeat=n):
        signs=[0]*m
        for v,choice in enumerate(picks):
            for j,(ci,p) in enumerate(occ[v]):
                if j not in choice:signs[ci]|=1<<p
        excluded=0
        for i,s in enumerate(signs):excluded|=exclusion[i][s]
        if excluded==all_excluded:unsat+=1
        else:sat+=1
    assert sat+unsat==6**n
    return dict(n=n,signings=6**n,SAT=sat,UNSAT=unsat)

def run():
    rng=random.Random(20261029)
    brute_checks=0; exact22_examples=0; chain_checks=0; unsat_controls=0; malformed_rejections=0; parsed_controls=0
    tables=[];ordinary_chain_checks=0;ordinary_controls=[]
    for n,count in ((3,20),(6,36),(9,40),(12,36),(15,8)):
        for j in range(count):
            signs=random_exact22(n,rng) if j%2 else [tuple(rng.randrange(2) for _ in range(3)) for _ in range(n+n//3)]
            source=encode_cycle(signs,n)
            assert decode(source)==('cycle',n,signs)
            got=solve(source)
            truth=any(satisfied(signs,n,[(a>>v)&1 for v in range(n)]) for a in range(1<<n))
            assert got==truth
            r,trace=recursive(source)
            assert got==r
            brute_checks+=1;exact22_examples+=check_exact22(signs,n)
            if check_exact22(signs,n):
                doc=dimacs_cycle(signs,n)
                assert parse_strict_dimacs_cycle(doc)==(n,signs)
                parsed_controls+=1
                for bad in (doc.replace('p cnf %d '%n,'p cnf %d '%(n+1),1), doc+'1 2 3 0\n',doc.replace(' 0\n',' 0 0\n',1),doc.replace(' 0\n',' 1\n',1)):
                    try:parse_strict_dimacs_cycle(bad)
                    except (AssertionError,ValueError):malformed_rejections+=1
                    else:raise AssertionError('malformed canonical DIMACS accepted')
            if not got:unsat_controls+=1
        signs=canonical_signs(n);src=encode_cycle(signs,n)
        assert check_exact22(signs,n)
        child,block=shrink(src)
        I,F,mats=compile_cycle(src)
        assert solve(src)==decide_chain(I,F,mats)==solve(child)
        doc=dimacs_cycle(signs,n)
        childsat,bl=shrink_ordinary_sat(doc)
        assert solve_ordinary_sat(doc)==solve_ordinary_sat(childsat)
        assert parse_chain_as_ordinary_sat(childsat)[0:2]==decode(child)[1:3]
        ordinary_chain_checks+=1
        ordinary_controls.append({'n':n,'ordinary_source_bits':8*len(doc),'ordinary_child_bits':8*len(childsat),'ordinary_child_clauses':len(to_cnf(*parse_chain_as_ordinary_sat(childsat))[1])})
        tables.append({'n':n,'dimacs_bits':8*len(dimacs_cycle(signs,n).encode('ascii')),'source_bits':len(src),'child_bits':len(child),'child_matrices':len(decode(child)[3]),'matrix_before':len(mats),'first_block_len':block})
    # Independently test arbitrary relations with both answer classes.
    for m in (1,2,3,4,8,16,64,256):
        for j in range(8):
            I=rng.getrandbits(16);F=rng.getrandbits(16)
            M=[tuple(rng.getrandbits(16) for _ in range(W)) for _ in range(m)]
            if j%4==0:M[m//2]=tuple([0]*W)
            inp=encode_chain(I,F,M)
            assert decode(inp)==('chain',I,F,M)
            child,block=shrink(inp)
            a=solve(inp);b=solve(child)
            assert a==b
            r,trace=recursive(inp)
            assert a==r
            chain_checks+=1
            if m in (1,4,16) and j in (0,1,2):
                physical=encode_chain_as_ordinary_sat(I,F,M)
                assert parse_chain_as_ordinary_sat(physical)==(I,F,M)
                smaller,bb=shrink_ordinary_sat(physical)
                assert solve_ordinary_sat(physical)==solve_ordinary_sat(smaller)==a
                ordinary_chain_checks+=1
            if not a:unsat_controls+=1
    # 4- and 8-literal clauses in the Tseitin re-encoding.
    gadget_checks=exhaustive_tseitin_clause(4)+exhaustive_tseitin_clause(8)
    # Concrete physical conversion of a nontrivial exact22 child back to ordinary 3CNF.
    signed=canonical_signs(30)
    s=encode_cycle(signed,30)
    child,block=shrink(s)
    _,I,F,M=decode(child)
    num,cl=to_cnf(I,F,M)
    text=cnf_text(num,cl)
    assert all(len(c)==3 for c in cl)
    cnf_sample={'input_bits':len(s),'chain_child_bits':len(child),'chain_matrices':len(M),'3cnf_bytes':len(text.encode('utf8')),'3cnf_bits':8*len(text.encode('utf8')),'cnf_variables':num,'cnf_clauses':len(cl),'cnf_aux_variables':num-4*(len(M)+1)}
    # Actual full canonical DIMACS-to-canonical-DIMACS physical sizes, including
    # every Tseitin auxiliary, clause, source comment, integer, and newline.
    ordinary_scaling=[]
    for n in (30,300,3000,30000):
        source=dimacs_cycle(canonical_signs(n),n)
        child,block=shrink_ordinary_sat(source)
        assert solve_ordinary_sat(source)==solve_ordinary_sat(child)
        ordinary_scaling.append({'n':n,'ordinary_source_bits':8*len(source),'ordinary_child_bits':8*len(child),'child_matrices':len(parse_chain_as_ordinary_sat(child)[2]),'child_to_parent_ratio':round(len(child)/len(source),6)})
    # Exact analytic physical lengths for binary sign streams and chain outputs.
    analytic=[]
    for n in (30,300,3000,30000,300000,3000000):
        m=n-2
        k=max(1,math.isqrt(math.isqrt(m)))
        inbits=1+len(nat(n))+4*n
        outbits=1+len(nat(k))+32+256*k
        analytic.append({'n':n,'source_bits':inbits,'child_bits_upper':outbits,'ratio_upper':round(outbits/inbits,6),'below_N_to_3over4':outbits<=inbits**.75})
    return {'status':'PASS','experiment':'CHAIN_ORDINARY_CLOSURE213','brute_cycle_checks':brute_checks,'parsed_exact22_dimacs_controls':parsed_controls,'malformed_dimacs_rejections':malformed_rejections,'exact22_cycle_controls':exact22_examples,'unsat_controls':unsat_controls,'arbitrary_matrix_chain_checks':chain_checks,'ordinary_3cnf_closed_grammar_tests':ordinary_chain_checks,'ordinary_3cnf_physical':ordinary_controls,'ordinary_3cnf_scaling':ordinary_scaling,'tseitin_gadget_assignments':gadget_checks,'exhaustive_exact22_cycle_signings':[exhaustive_exact22_signed_scopes(3),exhaustive_exact22_signed_scopes(6)],'small_physical':tables,'3cnf_conversion':cnf_sample,'large_length_bounds':analytic,'claim':'restricted bounded-frontier class only; no general SAT shrinker','limitations':['Python unit costs are not native TM transition counts','The closed canonical ordinary-3CNF subclass is not all SAT','Below a fixed asymptotic threshold physical encodings can expand','General exact summaries need not have 16 states.']}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
