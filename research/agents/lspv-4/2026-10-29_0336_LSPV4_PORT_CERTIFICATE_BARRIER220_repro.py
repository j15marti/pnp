#!/usr/bin/env python3
"""Independent finite controls for LSPV-4 two-sided exact-port certificates.
No external packages; exhaustive 3-variable signed source-clause subsets and
all GF(2) systems with up to three rows and columns.
"""
import itertools
import json
import hashlib
from pathlib import Path

ALL_CLAUSES = tuple(tuple((1 if (s >> i) & 1 else -1)*(i+1) for i in range(3)) for s in range(8))
checks = 0

def confirm(condition, note='assertion'):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(note)

def lit_sat(lit, bits):
    return (bool((bits >> (abs(lit)-1)) & 1) == (lit > 0))

def cnf_sat(clauses, bits):
    return all(any(lit_sat(x, bits) for x in cl) for cl in clauses)

def source_sat(clauses):
    return any(cnf_sat(clauses, a) for a in range(8))

def guard(clauses):
    y = 4
    out = []
    for i,(a,b,c) in enumerate(clauses):
        u = i + 5
        out.extend(((-y,a,u),(-u,b,c)))
    return tuple(out)

def port_projection_bruteforce(clauses, yval):
    g = guard(clauses)
    for xb in range(8):
        for ub in range(1 << len(clauses)):
            bits = xb | (int(yval) << 3) | (ub << 4)
            if cnf_sat(g,bits):
                return True
    return False

def enforce_port(yval):
    # a=13, b=14, fresh for all test instances (max u=12)
    v = 4 if yval else -4
    return tuple((v, a, b) for a,b in itertools.product((13,-13),(14,-14)))

def port_context_bruteforce(clauses,yval):
    ctx=enforce_port(yval)
    g=guard(clauses)
    for xb in range(8):
        for ub in range(1 << len(clauses)):
            bits0=xb | (int(yval) << 3) | (ub << 4)
            if not cnf_sat(g,bits0): continue
            for ab in range(4):
                bits=bits0 | ((ab&1)<<12) | (((ab>>1)&1)<<13)
                if cnf_sat(ctx,bits): return True
    return False

def dimacs_text(clauses, nv):
    return ('p cnf %d %d\n' %(nv,len(clauses)) +
            ''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()

stats={"status":"PASS","source_cases":0,"source_sat":0,"source_unsat":0,
       "guard_projection_checks":0,"context_checks":0,"affine_cases":0,
       "affine_sat":0,"affine_unsat":0,"assertions":0}
for mask in range(256):
    cs=tuple(ALL_CLAUSES[i] for i in range(8) if mask & (1<<i))
    F_sat=source_sat(cs)
    stats['source_cases']+=1
    stats['source_sat' if F_sat else 'source_unsat']+=1
    confirm(port_projection_bruteforce(cs, False), 'guard y=0')
    confirm(port_projection_bruteforce(cs, True)==F_sat, 'guard y=1')
    stats['guard_projection_checks']+=2
    for yval in (0,1):
        confirm(port_context_bruteforce(cs,yval)==(not yval or F_sat), 'context')
        stats['context_checks']+=1
    for cl in guard(cs):
        confirm(len({abs(l) for l in cl})==3, 'proper 3CNF')
    for yval in (False,True):
        ctx=enforce_port(yval)
        for y in (False,True):
            good=any(cnf_sat(ctx,(int(y)<<3) | (ab<<12)) for ab in range(4))
            confirm(good==(y==yval), 'port unit gadget')

# Matched physical lengths for a proper 3CNF YES and NO source, and guards.
F_no=ALL_CLAUSES
F_yes=tuple(c for i,c in enumerate(ALL_CLAUSES) if i != 6)+(ALL_CLAUSES[5],)
confirm(not source_sat(F_no))
confirm(source_sat(F_yes))
source_lengths=tuple(len(dimacs_text(cs,3)) for cs in (F_no,F_yes))
guard_lengths=tuple(len(dimacs_text(guard(cs),12)) for cs in (F_no,F_yes))
confirm(source_lengths[0]==source_lengths[1])
confirm(guard_lengths[0]==guard_lengths[1])
stats['matched_source_bytes']=source_lengths[0]
stats['matched_guard_bytes']=guard_lengths[0]

# Row-reducing augmented GF(2) systems while tracking row multipliers.
def affine_certificate(rows, b, n):
    m=len(rows)
    work=[[rows[i], (b>>i)&1,1<<i] for i in range(m)]
    piv=[]; top=0
    for col in range(n):
        partner=next((i for i in range(top,m) if (work[i][0]>>col)&1),None)
        if partner is None:continue
        work[top],work[partner]=work[partner],work[top]
        for j in range(m):
            if j!=top and (work[j][0]>>col)&1:
                for k in range(3):work[j][k]^=work[top][k]
        piv.append(col);top+=1
        if top==m:break
    for r,c,mult in work:
        if r==0 and c==1:return ('NO',mult)
    ans=0
    for i,col in enumerate(piv):
        if work[i][1]:ans |= 1<<col
    return ('YES',ans)

def verified_affine(rows,b,n,cert):
    kind,val=cert
    if kind=='YES':
        return all((((row&val).bit_count()&1)==((b>>i)&1)) for i,row in enumerate(rows))
    if kind=='NO':
        c=0; rhs=0
        for i,row in enumerate(rows):
            if (val>>i)&1:c^=row;rhs^=(b>>i)&1
        return c==0 and rhs==1
    return False

for m in range(4):
    for n in range(4):
        for packed in range(1<<(m*n)):
            rows=tuple((packed>>(i*n))&((1<<n)-1) for i in range(m))
            for b in range(1<<m):
                cert=affine_certificate(rows,b,n)
                actually=any(all((((x&r).bit_count()&1)==((b>>i)&1)) for i,r in enumerate(rows)) for x in range(1<<n))
                confirm((cert[0]=='YES')==actually,'affine decision')
                confirm(verified_affine(rows,b,n,cert),'affine certificate')
                stats['affine_cases']+=1
                stats['affine_sat' if actually else 'affine_unsat']+=1

stats['assertions']=checks
archive=Path(__file__).parent/'original'/'results.json'
if archive.exists():
    original=archive.read_bytes()
    stats['original_audit_json_sha256']=hashlib.sha256(original).hexdigest()
    stats['original_audit_reproduced']= original == (Path(__file__).parent/'audit_stdout.txt').read_bytes()
print(json.dumps(stats,indent=2,sort_keys=True))