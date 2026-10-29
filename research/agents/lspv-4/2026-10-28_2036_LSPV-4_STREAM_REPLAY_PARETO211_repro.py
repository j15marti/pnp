#!/usr/bin/env python3
"""LSPV-4 STREAM/REPLAY LEDGER: independent research control, no formal TM kernel proof.
The source format is a precise self-authenticating REL16 proper-3CNF test grammar.
Its metadata precedes physical DIMACS clauses.  A replay verifier retains no
matrix table, only the contracted child and O(log N) counters.  Tests compare
an online sequential verifier with an independent materializing generator.
"""
import json, random, hashlib, sys, math, itertools
from collections import Counter

STATE=16

def maskhex(mask): return f'{mask:04x}'
def mathex(mat): return f'{mat:064x}'

def boolprod(a,b):
    # Adjacency on 16 states: bits 16*i+j encode edges i->j.
    out=0
    for i in range(16):
        for mid in range(16):
            if not (a>>(16*i+mid))&1: continue
            out |= ((b>>(16*mid))&65535) << (16*i)
    return out

def chain_value(mats, I, F):
    reach=I
    for mat in mats:
        nxt=0
        for i in range(16):
            if (reach>>i)&1:
                nxt|=(mat>>(16*i)) & 65535
        reach=nxt
    return bool(reach&F)

def contract(mats):
    m=len(mats)
    k=max(1,math.isqrt(math.isqrt(m))) # floor(fourth root), correct for integers except rounding -> corrected below
    while (k+1)**4<=m: k+=1
    while k**4>m: k-=1
    L=(m+k-1)//k
    out=[]
    for j in range(0,m,L):
        run=(1<<256)-1 # temporary overwritten by identity!
        run=sum(1<<(16*i+i) for i in range(16))
        for mat in mats[j:j+L]:
            run=boolprod(run,mat)
        out.append(run)
    assert len(out)<=k
    return out,k

def expand_clause(clause,nextvar):
    assert len(clause) in (4,8)
    aux=list(range(nextvar,nextvar+len(clause)-3))
    out=[]
    out.append((clause[0],clause[1],aux[0]))
    for p in range(1,len(aux)):
        out.append((-aux[p-1],clause[p+1],aux[p]))
    out.append((-aux[-1],clause[-2],clause[-1]))
    assert len(out)==len(clause)-2
    return out,nextvar+len(aux)

def forbids(states,vars_):
    for a in range(1<<len(vars_)):
        if not (states>>a)&1:
            yield tuple(( -var if (a>>i)&1 else var) for i,var in enumerate(vars_))

def all_clauses(mats,I,F):
    m=len(mats)
    nextvar=4*(m+1)+1
    for big in forbids(I,(1,2,3,4)):
        clauses,nextvar=expand_clause(big,nextvar)
        yield from clauses
    for block,mat in enumerate(mats):
        v0=4*block+1
        v1=4*(block+1)+1
        for src in range(16):
            for dst in range(16):
                if (mat>>(16*src+dst))&1: continue
                lits=tuple((-(v0+i) if src>>i&1 else v0+i) for i in range(4))+tuple((-(v1+i) if dst>>i&1 else v1+i) for i in range(4))
                clauses,nextvar=expand_clause(lits,nextvar)
                yield from clauses
    for big in forbids(F,tuple(4*m+i+1 for i in range(4))):
        clauses,nextvar=expand_clause(big,nextvar)
        yield from clauses

def get_counts(mats,I,F):
    no4=(16-I.bit_count())+(16-F.bit_count())
    no8=sum(256-mat.bit_count() for mat in mats)
    nvars=4*(len(mats)+1)+no4+5*no8
    nclauses=2*no4+6*no8
    return nvars,nclauses

def generate(mats,I,F):
    assert mats and all(0<=x<(1<<256) for x in mats)
    assert 0<=I,F<65536
    nvars,nclauses=get_counts(mats,I,F)
    lines=[f'c REL16 {len(mats)} {maskhex(I)} {maskhex(F)}\n']
    lines.extend(f'c M {j} {mathex(mat)}\n' for j,mat in enumerate(mats))
    lines.append(f'p cnf {nvars} {nclauses}\n')
    lines.extend(' '.join(map(str,c))+' 0\n' for c in all_clauses(mats,I,F))
    return ''.join(lines)

def metadata_header(raw):
    """Full structural syntax validation, without storing source-row offsets."""
    pos=0
    x=raw.find('\n',pos)
    if x<0: raise ValueError('missing header')
    p=raw[pos:x].split(' ')
    if len(p)!=5 or p[:2]!=['c','REL16']: raise ValueError('bad header')
    m=int(p[2]); I=int(p[3],16); F=int(p[4],16)
    if m<1 or p[2]!=str(m) or p[3]!=maskhex(I) or p[4]!=maskhex(F): raise ValueError('noncanonical header')
    pos=x+1
    for j in range(m):
        x=raw.find('\n',pos)
        if x<0: raise ValueError('missing matrix row')
        row=raw[pos:x].split(' ')
        if len(row)!=4 or row[:2]!=['c','M'] or row[2]!=str(j): raise ValueError('bad matrix row')
        mat=int(row[3],16)
        if row[3]!=mathex(mat): raise ValueError('noncanonical matrix')
        pos=x+1
    x=raw.find('\n',pos)
    if x<0: raise ValueError('missing p-header')
    h=raw[pos:x].split(' ')
    if len(h)!=4 or h[:2]!=['p','cnf'] or any(not t.isdigit() for t in h[2:]):
        raise ValueError('bad p-header')
    if h[2]!=str(int(h[2])) or h[3]!=str(int(h[3])): raise ValueError('noncanonical counts')
    return m,I,F,x+1,int(h[2]),int(h[3])

def scan_metadata(raw):
    """Sequential input-head scan with only one current row in live memory."""
    newline=raw.find('\n')
    if newline<0: raise ValueError('missing header')
    pos=newline+1; j=0
    while raw.startswith('c M ',pos):
        x=raw.find('\n',pos)
        if x<0: raise ValueError('missing newline')
        row=raw[pos:x].split(' ')
        if len(row)!=4 or row[:2]!=['c','M'] or row[2]!=str(j):
            raise ValueError('bad matrix row')
        mat=int(row[3],16)
        if row[3]!=mathex(mat): raise ValueError('bad matrix hex')
        yield j,pos,x+1,mat
        pos=x+1; j+=1

def lookup_matrix(raw,idx):
    """Locates matrix idx by a fresh sequential scan; no offset table."""
    for j,start,end,mat in scan_metadata(raw):
        if j==idx:return start,end,mat
    raise ValueError('missing matrix')

def replay_verify(raw):
    """Sequential-source low-memory algorithm sketch, tested on full bytes.

    The host Python string is the external read-only source, not writable TM
    memory.  Every metadata lookup scans from source start.  The only retained
    mathematical objects are k child matrices, current matrix, and counters.
    Full child output is charged as writable peak to avoid a free output tape.
    """
    m,I,F,body_start,nvar,nclauses=metadata_header(raw)
    k=1
    while (k+1)**4<=m:k+=1
    L=(m+k-1)//k
    child=[]
    identity=sum(1<<(16*i+i) for i in range(16))
    current=identity; reach=I
    meta_end=0
    for j,start,end,mat in scan_metadata(raw):
        reach_next=0
        for i in range(16):
            if (reach>>i)&1:reach_next|=(mat>>(16*i))&65535
        reach=reach_next
        current=boolprod(current,mat)
        meta_end=end
        if (j+1)%L==0 or j==m-1:
            child.append(current); current=identity
    if len(child)>k:raise AssertionError('more than k output matrices')
    source_truth=bool(reach&F)
    actual_pos=body_start
    head_pos=meta_end
    # Initial parse plus sequential metadata scan and footer-position arrival.
    moves=2*body_start
    clauses_checked=0
    nextvar=4*(m+1)+1
    def check_line(expected,where):
        nonlocal actual_pos,head_pos,moves,clauses_checked
        moves+=abs(head_pos-actual_pos)
        head_pos=actual_pos
        if not raw.startswith(expected,actual_pos):
            raise ValueError(f'bad clause at {where}')
        actual_pos+=len(expected)
        head_pos=actual_pos
        moves+=len(expected)
        clauses_checked+=1
    def emit_big(big,where):
        nonlocal nextvar
        clauses,nextvar=expand_clause(big,nextvar)
        for clause in clauses:
            check_line(' '.join(map(str,clause))+' 0\n',where)
    for big in forbids(I,(1,2,3,4)):
        emit_big(big,'initial')
    for block in range(m):
        # The new metadata access starts from position 0 and walks forwards.
        # Each lookup explicitly charges the travel and scanning distance.
        moves+=head_pos
        start,end,mat=lookup_matrix(raw,block)
        moves+=end
        head_pos=end
        v0=4*block+1;v1=4*(block+1)+1
        for src in range(16):
            for dst in range(16):
                if (mat>>(16*src+dst))&1: continue
                big=tuple((-(v0+i) if src>>i&1 else v0+i) for i in range(4))+tuple((-(v1+i) if dst>>i&1 else v1+i) for i in range(4))
                emit_big(big,block)
    for big in forbids(F,tuple(4*m+i+1 for i in range(4))):
        emit_big(big,'final')
    if raw[actual_pos:]: raise ValueError('trailing bytes')
    if nclauses!=clauses_checked or nvar!=nextvar-1: raise ValueError('incorrect p-header')
    child_raw=generate(child,I,F)
    return {'accept':True,'source_bits':len(raw)*8,'child_bits':len(child_raw)*8,
            'source_head_moves_upper':moves+len(raw),'m':m,'k':k,'child_m':len(child),
            'max_work_bits_upper':8*len(child_raw)+256*k+512*math.ceil(math.log2(len(raw)+2)),
            'child_sha256':hashlib.sha256(child_raw.encode()).hexdigest(),
            'source_truth':source_truth,'child_truth':chain_value(child,I,F)}


def verify_translator():
    checks=0
    for w in (4,8):
        orig=[i+1 for i in range(w)]
        aux_clauses,end=expand_clause(orig,w+1)
        for x in range(1<<w):
            target=bool(x)
            found=False
            for a in range(1<<(w-3)):
                bits={i+1:(x>>i)&1 for i in range(w)}
                bits.update({w+j+1:(a>>j)&1 for j in range(w-3)})
                if all(any((bits[abs(l)] if l>0 else not bits[abs(l)]) for l in c) for c in aux_clauses):
                    found=True;break
            assert found==target
            checks+=1
    return checks


def brute_chain(mats,I,F):
    m=len(mats)
    assert m<=2
    for path in itertools.product(range(16),repeat=m+1):
        if not ((I>>path[0])&1 and (F>>path[-1])&1):continue
        if all((mats[j]>>(16*path[j]+path[j+1]))&1 for j in range(m)):
            return True
    return False

def run():
    rng=random.Random(20261028+211)
    results=[]; count=0; failures=0; saw_sat=False; saw_unsat=False
    source_replay_checks=0; brute_checks=0
    for m in [1,2,3,4,5,6,8,16]:
        for trial in range(3 if m==16 else 12):
            # Mix sparse and dense, including all-zero and all-one transition rows.
            if trial==0: mats=[0]*m
            elif trial==1: mats=[(1<<256)-1]*m
            else:
                rate=(0.01,0.05,0.25,0.7,0.95)[trial%5]
                mats=[sum(1<<i for i in range(256) if rng.random()<rate) for _ in range(m)]
            I=(1<<16)-1 if trial%3 else rng.getrandbits(16)
            F=(1<<16)-1 if trial%4 else rng.getrandbits(16)
            source=generate(mats,I,F)
            audit=replay_verify(source)
            child,k=contract(mats)
            csource=generate(child,I,F)
            assert audit['child_sha256']==hashlib.sha256(csource.encode()).hexdigest()
            assert audit['child_bits']==len(csource)*8
            assert audit['source_truth']==audit['child_truth']==chain_value(mats,I,F)
            if m<=2:
                assert audit['source_truth']==brute_chain(mats,I,F)
                brute_checks+=1
            assert audit['k']==k
            assert audit['source_head_moves_upper'] <= 5*(m+2)*len(source)+10*len(source)
            assert audit['max_work_bits_upper'] < 12*len(csource)+256*k+800*math.log2(len(source)+2)
            count+=1
            saw_sat |= bool(audit['source_truth']);saw_unsat |= not audit['source_truth']
            if m in (1,4,8) and trial in (0,1,4):
                results.append({**audit,'trial':trial})
            # Adversarial malformed-body comparison. For generated source with
            # at least one clause, flip a physical clause byte without changing metadata.
            j=source.find('\np cnf ')
            if j<0: j=source.find('p cnf ')
            pos=source.find('\n',j+1)+1
            if pos<len(source):
                corrupted=source[:pos]+('x' if source[pos]!='x' else 'y')+source[pos+1:]
                try: replay_verify(corrupted)
                except ValueError: failures+=1
                else: raise AssertionError('tamper accepted')
            # Check metadata corruption independent of source body.
            h=source.find('c M 0 ')
            if h>=0:
                p=h+len('c M 0 ')
                corrupt=source[:p]+('x' if source[p]!='x' else 'y')+source[p+1:]
                try: replay_verify(corrupt)
                except (ValueError,AssertionError): failures+=1
                else: raise AssertionError('metadata tamper accepted')
    assert saw_sat and saw_unsat
    # Large, high-acceptance sparse-output source exercises fourth-root k>2.
    m=256; mats=[(1<<256)-1]*m;I=F=(1<<16)-1
    big=generate(mats,I,F);big_audit=replay_verify(big)
    assert big_audit['child_m']==4
    assert big_audit['source_truth'] and big_audit['child_truth']
    results.append({**big_audit,'trial':'large-all-one'})
    count+=1
    # Independent constructor test: existential Tseitin equivalence for
    # EVERY 4- and 8-variable assignment, with all auxiliary settings.
    translator_checks=verify_translator()
    return {'status':'PASS','random_seed':20261239,'canonical_chain_cases':count,
            'tamper_rejections':failures,'brute_chain_comparisons':brute_checks,
            'translator_truth_assignments':translator_checks,
            'both_polarities_covered':True,'sample_metrics':results,
            'caveats':['Host Python strings are not TM work tapes.',
                       'Counters give conservative head-movement bounds, not measured native TM transitions.',
                       'The grammar is restricted and may use arbitrary relation matrices, not unrestricted SAT.',
                       'The theoretical time-space recurrences require a separately specified fixed-tape implementation.']}

if __name__=='__main__':
    r=run();print(json.dumps(r,indent=2,sort_keys=True))
