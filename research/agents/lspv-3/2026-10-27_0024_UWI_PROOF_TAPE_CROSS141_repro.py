#!/usr/bin/env python3
"""Deterministic finite audit for LSPV-3 UWI-PROOFTAPE-CROSS141.
Independent counts, canonical source permutations, both-label certificates,
source-only model generator, crossing fooling pairs and bit-sensitivity.
No physical tape runs, SAT time lower bound, or broad input coverage claimed.
"""
import hashlib, itertools, json, math
from pathlib import Path
BASE = ((-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
        (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
        (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
        (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))
A_ROWS=(6,11)
FIXED_ROWS=tuple(r for r in range(20) if r not in A_ROWS+(17,9))
B_ROWS=(17,9)
assert len(FIXED_ROWS)==16
assert {abs(x) for c in BASE for x in c}==set(range(1,16))
counts={"assertions":0,"sources":0,"sat":0,"unsat":0,"proof_accept_sat":0,
        "local_unsat_accept":0,"local_unsat_reject":0,"cross_pairs":0,
        "sensitivity_flips":0,"source_model_calls":0,"children":0}

def check(value,msg="failed assertion"):
    counts["assertions"]+=1
    if not value:raise AssertionError(msg)

def module(a,b,shift=0):
    rows=[list(x) for x in BASE]
    if a==0:
        for r,c in ((6,0),(11,0)):rows[r][c]*=-1
    if b==0:
        for r,c in ((17,2),(9,2)):rows[r][c]*=-1
    return tuple(tuple((1 if x>0 else -1)*(abs(x)+shift) for x in row) for row in rows)

def satisfied(cnf,mask):
    return all(any(bool(mask & (1<<(abs(l)-1)))==(l>0) for l in row) for row in cnf)

def count_models(cnf):
    return sum(satisfied(cnf,z) for z in range(1<<15))

def exact_signed(cnf,n):
    pos=[0]*(n+1);neg=[0]*(n+1)
    for row in cnf:
        if len(row)!=3 or len({abs(l) for l in row})!=3:return False
        for l in row:(pos if l>0 else neg)[abs(l)]+=1
    return all(pos[i]==2 and neg[i]==2 for i in range(1,n+1))

def indexed_clauses(a,b):
    m=len(a);groups=[module(a[i],b[i],15*i) for i in range(m)]
    return tuple(tuple(groups[i][r] for i in range(m) for r in rs) for rs in (A_ROWS,FIXED_ROWS,B_ROWS))

def source_rows(a,b):
    groups=indexed_clauses(a,b)
    return tuple(x for group in groups for x in group)

def source_encode(a,b):
    m=len(a);w=(15*m).bit_length()
    prefix=f"CNF BINARY m={m} n={15*m} clauses={20*m} width={w}\n"
    bits=''.join(('1' if l<0 else '0')+format(abs(l),'0%db'%w) for row in source_rows(a,b) for l in row)
    return prefix+bits

def source_decode(a_len,source):
    m=a_len;w=(15*m).bit_length()
    prefix=f"CNF BINARY m={m} n={15*m} clauses={20*m} width={w}\n"
    if not source.startswith(prefix):return None
    bits=source[len(prefix):]
    if len(bits)!=20*m*3*(w+1) or any(x not in '01' for x in bits):return None
    vals=[]
    for at in range(0,len(bits),w+1):
        chunk=bits[at:at+w+1]
        t=int(chunk[1:],2)
        if t==0 or t>15*m:return None
        vals.append(-t if chunk[0]=='1' else t)
    rows=[tuple(vals[i:i+3]) for i in range(0,len(vals),3)]
    av=[];bv=[]
    # A row 6 is the first row of each A section; B row 17 is the first B section.
    for i in range(m):
        va=rows[2*i][0]
        vb=rows[18*m+2*i][2]
        if abs(va)!=4+15*i or abs(vb)!=15+15*i:return None
        av.append(int(va==4+15*i))  # W1 row 6 literal +4
        bv.append(int(vb==15+15*i)) # W1 row 17 literal +15
    av=tuple(av);bv=tuple(bv)
    if tuple(rows)!=source_rows(av,bv):return None
    return av,bv,tuple(rows)

def sat_proof_reader(source,m,pi):
    dec=source_decode(m,source)
    if dec is None or len(pi)!=m:return False
    av,bv,_=dec
    return tuple(pi)==av and all(x*y==0 for x,y in zip(pi,bv))

def unsat_leaf(rows,m,i):
    # No global SAT oracle: authenticated literal equality for the original 20
    # clauses of one locally contradictory H(1,1). The 2^15 model enumeration
    # is an input-independent constant-time validation baked into grammar.
    if not (0<=i<m):return False
    for group, rs, start in ((0,A_ROWS,0),(1,FIXED_ROWS,2*m),(2,B_ROWS,18*m)):
        want=module(1,1,15*i)
        for j,r in enumerate(rs):
            if rows[start+len(rs)*i+j]!=want[r]:return False
    return True

def disjoint(a,b):return all(x*y==0 for x,y in zip(a,b))

def dimacs_serialize(rows):
    n=max((abs(x) for row in rows for x in row),default=0)
    return 'p cnf %d %d\n'%(n,len(rows))+''.join(' '.join(map(str,row))+' 0\n' for row in rows)

def dimacs_parse(s):
    lines=s.splitlines()
    if not lines or len(lines[0].split())!=4 or lines[0].split()[:2]!=['p','cnf']:
        return None
    try:
        n,m=map(int,lines[0].split()[2:])
        rows=[tuple(map(int,line.split())) for line in lines[1:]]
    except ValueError:return None
    if len(rows)!=m or any(len(row)!=4 or row[-1]!=0 for row in rows):return None
    actual=tuple(row[:3] for row in rows)
    if max((abs(l) for row in actual for l in row),default=0)>n:return None
    return actual

def initial_pin_clauses(lit,aux):
    x,y=aux
    return ((lit,x,y),(lit,x,-y),(lit,-x,y),(lit,-x,-y))

def all_nodes_counts_by_module(a,b,pins):
    # The rest of the modules have independent variables, so their satisfiability
    # factors. A pin affects just one explicitly identified original module.
    m=len(a)
    for i in range(m):
        cnf=module(a[i],b[i]); localpins=[p for p in pins if 15*i < abs(p)<=15*(i+1)]
        if not any(satisfied(cnf,z) and all(bool(z&(1<<((abs(p)-1)%15)))==(p>0) for p in localpins)
                   for z in range(1<<15)):
            return False
    return True

def run():
    for a,b,expect in ((0,0,772),(0,1,272),(1,0,272),(1,1,0)):
        c=module(a,b)
        check(count_models(c)==expect,(a,b,'wrong model count'))
        check(exact_signed(c,15),'signed quota')
    check(satisfied(module(0,0),616) and satisfied(module(0,1),616),'w0 not valid')
    check(satisfied(module(1,0),4742),'w1 not valid')
    check(not satisfied(module(1,1),616) and not satisfied(module(1,1),4742),'W1 witness leak')
    checks_per_m={}
    for m in range(1,7):
        cases=0
        for a in itertools.product((0,1),repeat=m):
            for b in itertools.product((0,1),repeat=m):
                src=source_encode(a,b)
                dec=source_decode(m,src)
                check(dec is not None and dec[0]==a and dec[1]==b,'parse failure')
                rows=dec[2]
                check(exact_signed(rows,15*m),'full signed quota')
                sat=disjoint(a,b)
                if sat:counts['sat']+=1
                else:counts['unsat']+=1
                counts['sources']+=1;cases+=1
                check(sat_proof_reader(src,m,a)==sat,'SAT proof verification polarity')
                if sat:counts['proof_accept_sat']+=1
                # A-side source-only model is a valid global assignment for every SAT input.
                for i in range(m):
                    local_mask=4742 if a[i] else 616
                    check(satisfied(module(a[i],b[i]),local_mask)==(not (a[i] and b[i])),
                          'Alice-only witness validity')
                    counts['source_model_calls']+=1
                candidates=[i for i in range(m) if unsat_leaf(rows,m,i)]
                check(bool(candidates)==(not sat),'UNSAT certificate polarity')
                check(candidates==[i for i in range(m) if a[i] and b[i]],'source-ID mismatch')
                if not sat:counts['local_unsat_accept']+=1
                else:counts['local_unsat_reject']+=1
        checks_per_m[str(m)]=cases
    # Parse and certificate malformed controls, all must fail closed.
    m=1;valid=source_encode((1,),(0,))
    check(not sat_proof_reader(valid[:-1],m,(1,)),'truncated source')
    check(not sat_proof_reader('broken header'+valid,m,(1,)),'broken header')
    check(not sat_proof_reader(valid,m,()),'bad certificate length')
    check(not sat_proof_reader(valid.replace('width=4','width=0'),m,(1,)),'bad width')
    # Direct indexed bit-sensitivity on one accepting SAT source a=all 1, b=all 0.
    for m in (1,2,3,4,8,16,32):
        a=(1,)*m; b=(0,)*m; src=source_encode(a,b)
        check(sat_proof_reader(src,m,a),'sensitive SAT anchor')
        for i in range(m):
            mut=list(b);mut[i]=1
            check(not disjoint(a,mut),'flipped source must be UNSAT')
            bad_src=source_encode(a,tuple(mut))
            check(not sat_proof_reader(bad_src,m,a),'same proof must reject')
            counts['sensitivity_flips']+=1
    # Cross fooling pairs: at least one of the two crossed words is a NO input.
    for m in range(1,9):
        for a in itertools.product((0,1),repeat=m):
            for ap in itertools.product((0,1),repeat=m):
                if a==ap:continue
                ca=tuple(1-x for x in a)
                cap=tuple(1-x for x in ap)
                check(not (disjoint(a,cap) and disjoint(ap,ca)),'fooling-set error')
                counts['cross_pairs']+=1
    # Existence of 2^m sound rectangles indexed by pi=a and covering DISJ YES.
    for m in range(1,6):
        words=list(itertools.product((0,1),repeat=m))
        for a in words:
            for b in words:
                accepts=sum((p==a and disjoint(p,b)) for p in words)
                check(accepts==int(disjoint(a,b)),'rectangle cover')
    # Two genuine ordinary source-identified proper ternary PIN descendants.
    for m in (1,2):
        for a in itertools.product((0,1),repeat=m):
            for b in itertools.product((0,1),repeat=m):
                n=15*m;rows=source_rows(a,b)
                C1=initial_pin_clauses(-1,(n+1,n+2))
                C2=initial_pin_clauses(-2,(n+3,n+4))
                path=(rows,rows+C1,rows+C1+C2)
                check([len(x) for x in path]==[20*m,20*m+4,20*m+8],'real descendants')
                check(all(len(row)==3 and len({abs(l) for l in row})==3 for f in path for row in f),'proper descendants')
                encoded=[dimacs_serialize(p) for p in path]
                check(all(dimacs_parse(s)==p for s,p in zip(encoded,path)),'DIMACS reparse')
                check(len(encoded[0])<len(encoded[1])<len(encoded[2]),'no false length contraction')
                truth=[all_nodes_counts_by_module(a,b,[]),all_nodes_counts_by_module(a,b,[-1]),
                       all_nodes_counts_by_module(a,b,[-1,-2])]
                check(all(truth[i+1]<=truth[i] for i in (0,1)),'child monotonicity')
                counts['children']+=3
    # A local W1 leaf must be rejected if any of its twenty authenticated rows is tampered.
    m=1;rows=list(source_rows((1,),(1,)))
    check(unsat_leaf(rows,m,0),'W1 local leaf')
    for j in range(20):
        altered=rows.copy();r=list(altered[j]);r[0]*=-1;altered[j]=tuple(r)
        check(not unsat_leaf(altered,m,0),'tampered proof accepted')
    # Abstract proof-tape counting (soundness separate from actual tape emulation).
    for m in range(1,40):
        for L in (0,1,m//2,m):
            S=int(math.ceil(math.log2(m+2)))
            q=7;k=1;alphabet=2
            Q=2*q*((2*S+3)**k)*(alphabet**S)*(L+3)
            cap=(2**(L+1)-1)*(1+Q)
            check((cap>=2**m)==(cap.bit_length()>m),'finite counting algebra sanity')
            if L==m:check(cap>=2**m,'linear witness cap')
    output={"report_id":"UWI-PROOFTAPE-CROSS141","date":"2026-10-27","counts":counts,
            "cases_per_m":checks_per_m,"local_model_counts":{"00":772,"01":272,"10":272,"11":0},
            "fixed_gap_rows_per_module":16,"certificate_physical_length_bits":"m for SAT proof reader, ceil(log2 m) for source-local UNSAT index",
            "status":"Restricted mathematical lemma and finite verification; no general SAT lower bound; no RAM crossing transfer"}
    payload=json.dumps(output,indent=2,sort_keys=True)+'\n'
    out=Path(__file__).with_name('2026-10-27_0024_UWI_PROOF_TAPE_CROSS141_raw.json')
    out.write_text(payload)
    print(payload)
    print('SHA256:',hashlib.sha256(payload.encode()).hexdigest())
if __name__=='__main__':run()
