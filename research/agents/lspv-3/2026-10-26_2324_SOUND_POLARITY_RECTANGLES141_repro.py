#!/usr/bin/env python3
"""LSPV-3 141: source-authenticated 2P2N exact-SAT polarity audit.
No dependencies. Exhaustive for m <= 5, modules at most 15 vars each.
All audit counts describe finite tests, never a proof of a SAT time lower bound.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path

SEED = 14120261026
RAW = "-1 3 -14; 2 -8 9; 10 -13 14; 3 7 -13; -4 -9 -11; 5 8 -14; 4 -8 -11; 1 7 13; 1 -7 10; -5 -6 -15; -2 -6 12; -4 9 -10; -2 5 -12; -3 6 -15; 6 -7 11; 2 -9 11; 4 8 -10; -3 12 15; -5 -12 15; -1 13 14"
BASE = [tuple(int(x) for x in chunk.strip().split()) for chunk in RAW.split(';')]
A_ROWS = ((6,0), (11,0))
B_ROWS = ((9,2), (17,2))
N_CHECKS = 0

def check(x, description='check failed'):
    global N_CHECKS
    N_CHECKS += 1
    if not x:
        raise AssertionError(description)

def module(a: int,b: int):
    out = [list(c) for c in BASE]
    if not a:
        for r,j in A_ROWS: out[r][j] = -out[r][j]
    if not b:
        for r,j in B_ROWS: out[r][j] = -out[r][j]
    return [tuple(c) for c in out]

def is_model(clauses, x):
    return all(any(((x >> (abs(l)-1)) & 1) == int(l>0) for l in c) for c in clauses)

def models(clauses):
    return sum(is_model(clauses, x) for x in range(1<<15))

def exact22(clauses, n):
    counter=Counter((abs(l),int(l>0)) for c in clauses for l in c)
    return len(clauses)*3 == n*4 and all(counter[(v,s)]==2 for v in range(1,n+1) for s in (0,1)) and all(len({abs(l) for l in c})==3 for c in clauses)

def literal_translate(c,i):
    return tuple((1 if l>0 else -1)*(abs(l)+15*i) for l in c)

def encode_disj(a,b,m):
    clauses_by_key={}
    for i in range(m):
        rows=module((a>>i)&1,(b>>i)&1)
        for r,c in enumerate(rows):
            clauses_by_key[(i,r)] = literal_translate(c,i)
    A={r for r,j in A_ROWS};B={r for r,j in B_ROWS}
    sequence=[(i,r) for i in range(m) for r in sorted(A)]
    sequence += [(i,r) for i in range(m) for r in range(20) if r not in A|B]
    sequence += [(i,r) for i in range(m) for r in sorted(B)]
    bits=(f'p cnf {15*m} {20*m}\n').encode('ascii')
    field_width=len(str(15*m))+1  # padding spaces are ordinary DIMACS separators
    locations={}; spans=[]
    for key in sequence:
        content=(' '.join(f'{l:>{field_width}d}' for l in clauses_by_key[key])+' 0\n').encode('ascii')
        locations[key]=len(bits)
        spans.append((key,len(bits),len(bits)+len(content)))
        bits+=content
    return bits,locations,spans

def parse_dimacs(blob):
    """Independent strict parser, returns physical original clause offsets."""
    try:
        lines=blob.decode('ascii').splitlines(keepends=True)
        if not lines or not lines[0].endswith('\n'): return None
        head=lines[0].split()
        if len(head)!=4 or head[:2]!=['p','cnf']: return None
        n=int(head[2]);m=int(head[3]);
        if n<1 or m<1 or m!=len(lines)-1: return None
        records={};offset=len(lines[0].encode())
        for line in lines[1:]:
            if not line.endswith('\n'): return None
            parts=line.split()
            if len(parts)!=4 or parts[-1]!='0':return None
            c=tuple(map(int,parts[:3]))
            if any(l==0 or abs(l)>n for l in c):return None
            if len({abs(l) for l in c})!=3:return None
            records[offset]=c
            offset+=len(line.encode())
        return n,m,records
    except (ValueError,UnicodeDecodeError):
        return None

def certificate(i,locations):
    return [locations[(i,r)] for r in range(20)]

def full_source_authenticated_unsat(blob,offsets,i):
    """Sound on *all well-formed ordinary proper 3CNF*, not just the promise.
    This implementation stores the parser map; a streaming implementation
    uses 20 source seeks plus a charged full malformed-input validation pass.
    """
    parsed=parse_dimacs(blob)
    if parsed is None or i<0 or len(offsets)!=20 or len(set(offsets))!=20:return False
    n,m,src=parsed
    if any(o not in src for o in offsets):return False
    return [src[o] for o in offsets]==[literal_translate(c,i) for c in BASE]

def append_proper_pin(blob, literal):
    parsed=parse_dimacs(blob)
    if parsed is None:raise ValueError('invalid source')
    n,m,records=parsed
    if abs(literal)>n:raise ValueError('wrong original name')
    u,v=n+1,n+2
    pins=[(literal,u,v),(literal,u,-v),(literal,-u,v),(literal,-u,-v)]
    lines=blob.decode('ascii').splitlines(keepends=True)
    new=f'p cnf {n+2} {m+4}\n'+''.join(lines[1:])+''.join(' '.join(map(str,c))+' 0\n' for c in pins)
    return new.encode('ascii')

def two_actual_child_levels(m,a,b):
    src,_,_=encode_disj(a,b,m)
    # Choose first-module PIN values from the Alice-only valid assignment
    # only on SAT roots. UNSAT roots preserve UNSAT regardless of pins.
    w=616 if not(a&1) else 4742
    x1=1 if w&1 else -1
    x2=2 if w&2 else -2
    child1=append_proper_pin(src,x1)
    child2=append_proper_pin(child1,x2)
    p0,p1,p2=map(parse_dimacs,(src,child1,child2))
    check(all(q is not None for q in (p0,p1,p2)))
    check((p0[0],p1[0],p2[0])==(15*m,15*m+2,15*m+4))
    check((p0[1],p1[1],p2[1])==(20*m,20*m+4,20*m+8))
    check(list(p0[2].values())==list(p1[2].values())[:20*m])
    check(list(p0[2].values())==list(p2[2].values())[:20*m])
    check(len(src)<len(child1)<len(child2))
    if (a&b)==0:
        full=0
        for i in range(m):
            wi=616 if not((a>>i)&1) else 4742
            for j in range(15):
                if (wi>>j)&1:full |= 1<<(15*i+j)
        for c in p2[2].values():
            check(all(abs(l)<=15*m+4 for l in c))
            check(any(((full>>(abs(l)-1))&1)==int(l>0) for l in c), 'SAT descendant witness')
    return len(src),len(child1),len(child2)

def cover_checks(m):
    mask=(1<<m)-1
    sat_count=0;unsat_count=0
    for a in range(1<<m):
        for b in range(1<<m):
            d=(a&b)==0
            sat_count+=d; unsat_count+=not d
            # 2^m SAT rectangles: singleton Alice word a
            check((not d) or any(a==u and (u&b)==0 for u in range(1<<m)), 'SAT upper cover')
            # m UNSAT rectangles: common one-coordinate
            check(d or any((a>>i)&1 and (b>>i)&1 for i in range(m)), 'UNSAT upper cover')
    check(sat_count==3**m)
    check(unsat_count==4**m-3**m)
    # 2^m SAT fooling pairs (a, complement(a)).
    for a in range(1<<m):
        for u in range(a+1,1<<m):
            check(((a&(~u&mask)) != 0) or ((u&(~a&mask)) != 0),'SAT fooling pair')
    # m UNSAT fooling pairs (e_i,e_i).
    for i in range(m):
        for j in range(i+1,m):
            check(((1<<i)&(1<<j))==0, 'UNSAT fooling pair')
    return {'m':m,'sat_pairs':sat_count,'unsat_pairs':unsat_count,
            'sat_rectangle_cover_exact':1<<m,'unsat_rectangle_cover_exact':m}

def run():
    check(len(BASE)==20)
    check(BASE[6][0] == -BASE[11][0])
    check(BASE[9][2] == -BASE[17][2])
    model_counts={}
    for a,b in itertools.product((0,1),repeat=2):
        c=module(a,b);check(exact22(c,15))
        cnt=models(c)
        model_counts[f'{a}{b}']=cnt
        check(cnt=={(0,0):772,(0,1):272,(1,0):272,(1,1):0}[(a,b)])
    for pair in ((0,0),(0,1)):
        check(is_model(module(*pair),616),'Alice-zero local SAT witness')
    check(is_model(module(1,0),4742),'Alice-one local SAT witness')
    # This source-only witness fails whenever a_i=b_i=1 (UNSAT gadget).
    check(not is_model(module(1,1),4742),'witness printing is not acceptance')
    covers=[cover_checks(m) for m in range(1,7)]
    child_paths=[]
    for m in range(1,4):
        for a in range(1<<m):
            for b in range(1<<m):
                child_paths.append(two_actual_child_levels(m,a,b))
    counts=Counter();total_bytes=0;max_gap=0
    for m in range(1,6):
        for a in range(1<<m):
            for b in range(1<<m):
                blob,loc,spans=encode_disj(a,b,m)
                parsed=parse_dimacs(blob)
                check(parsed is not None, 'proper ordinary DIMACS')
                n,ncl,src=parsed
                check((n,ncl,len(src))==(15*m,20*m,20*m))
                check(exact22(list(src.values()),15*m),'strict source exact22')
                pos=[i for i in range(m) if (a>>i)&1 and (b>>i)&1]
                for i in range(m):
                    offs=certificate(i,loc)
                    got=full_source_authenticated_unsat(blob,offs,i)
                    check(got==(i in pos),'authenticated source local certificate')
                    counts['cert_verifications']+=1
                    if got:
                        # Removing either source input bit at singleton i toggles UNSAT to SAT.
                        if a==b==(1<<i):
                            for aa,bb in ((a&~(1<<i),b),(a,b&~(1<<i))):
                                check((aa&bb)==0, 'singleton sensitivity')
                                blob2,_,_=encode_disj(aa,bb,m)
                                check(not full_source_authenticated_unsat(blob2,offs,i), 'source no longer has W1')
                check(bool(pos)==(a&b!=0))
                # Mutated source control invalidates exact authenticated clauses.
                if pos:
                    bad=blob.replace(b' 0\n',b' 1\n',1)
                    check(not full_source_authenticated_unsat(bad,certificate(pos[0],loc),pos[0]), 'malformed mutation')
                    wrong=certificate(pos[0],loc)
                    wrong[0]+=1
                    check(not full_source_authenticated_unsat(blob,wrong,pos[0]),'shifted physical clause offset')
                A_rows={r for r,j in A_ROWS};B_rows={r for r,j in B_ROWS}
                fixed=[(key,s,e) for key,s,e in spans if key[1] not in A_rows|B_rows]
                gap=fixed[-1][2]-fixed[0][1]
                check(gap>0)
                max_gap=max(max_gap,gap)
                total_bytes+=len(blob)
                counts['sources']+=1
                counts['sat_sources']+=int(a&b==0)
                counts['unsat_sources']+=int(a&b!=0)
                counts['source_bytes_total']+=len(blob)
    check(counts['sources']==sum(4**m for m in range(1,6)))
    check(counts['sat_sources']==sum(3**m for m in range(1,6)))
    check(counts['unsat_sources']==sum(4**m-3**m for m in range(1,6)))
    # A-only witness is good on SAT sources, but is not a sound SAT acceptor.
    for m in range(1,4):
        # A sign flip changes ONLY the Alice source rows, with all other bytes
        # at identical physical positions. Likewise for Bob.
        for a in range(1<<m):
            for b in range(1<<m):
                blob,loc,spans=encode_disj(a,b,m)
                s_by_key={key:(start,end) for key,start,end in spans}
                for i in range(m):
                    for toggle,rows in ((0,{r for r,j in A_ROWS}), (1,{r for r,j in B_ROWS})):
                        next_a=a^(1<<i) if toggle==0 else a
                        next_b=b^(1<<i) if toggle==1 else b
                        altered,altered_loc,_=encode_disj(next_a,next_b,m)
                        check(len(altered)==len(blob),'ordinary padding exact bit length')
                        check(loc==altered_loc,'all physical offsets invariant')
                        sensitive={k for row in rows for k in range(*s_by_key[(i,row)])}
                        delta={k for k in range(len(blob)) if blob[k]!=altered[k]}
                        check(bool(delta) and delta <= sensitive,'bit-local source toggle')
    for a,b in itertools.product((0,1),repeat=2):
        candidate=616 if a==0 else 4742
        check(is_model(module(a,b),candidate)==(not bool(a&b)), 'candidate vs checked acceptance')
    out={'run_id':'SOUND_POLARITY_RECTANGLES141','seed':SEED,
         'status':'FINITE_EXHAUSTION_ONLY_AND_SEPARATE_FORMAL_PROOF',
         'source':'W1 original 20 clauses with A and B opposite-sign flips',
         'model_counts':model_counts,'covers':covers,'encoded_counts':dict(counts),
         'checked_assertion_groups':N_CHECKS,
         'max_middle_gap_bytes':max_gap, 'two_level_actual_child_controls':len(child_paths),
         'notes':['Exhaustive all 4^m choices for m=1..5 ordinary serialized sources.',
                  'Cover theorem for arbitrary m is proved mathematically in LaTeX.',
                  'No Python peak-memory/physical tape lower bound is inferred.',
                  'Source verifier is sound all proper ordinary CNF; subfamily gives completeness.',
                  'No all-ordinary UNSAT efficient certificate coverage claim.']}
    out['sha256_of_canonical_results_without_hash']=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    dest=Path(__file__).with_name('2026-10-26_2324_SOUND_POLARITY_RECTANGLES141_raw.json')
    dest.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__':run()
