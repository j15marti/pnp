#!/usr/bin/env python3
"""Grok 4.7 work 2026-11-28 17:05 KST -- T3/L05-36 triple-packing NAE4: exact PC4/PC5 status.
Single-file bundle (the connector allows few file attachments per commit). Subcommands:
  packgen | defect | yesctl | prove n d g|r edgefile [cert.json] | check cert.json |
  mincore n seed d1,d2,.. | scan nlist seed_lo seed_hi | corescan nlist seed_lo seed_hi | tables
The C closure mlclosure.c (compiled to ./mlclosure) is used by scan/mincore/corescan.
The checker (main_check) shares no polynomial code with the prover (run/main_prove)."""
import sys, json, itertools, subprocess, time, collections

# ==================== packgen ====================
# Greedy triple-packing 4-uniform hypergraphs (attempted reproduction of T3/L05-36 generator)
import itertools, sys
def lcg_variants():
    pass
def gen(n, seed, variant):
    subs = list(itertools.combinations(range(n), 4))
    s = seed & 0xffffffff
    def nxt():
        nonlocal s
        s = (s*1664525 + 1013904223) & 0xffffffff
        return s
    a = subs[:]
    if variant == 'down':      # for i=len-1..1, j = r % (i+1)
        for i in range(len(a)-1, 0, -1):
            j = nxt() % (i+1); a[i], a[j] = a[j], a[i]
    elif variant == 'up':      # for i=0..len-2, j = i + r % (len-i)
        for i in range(len(a)-1):
            j = i + nxt() % (len(a)-i); a[i], a[j] = a[j], a[i]
    elif variant == 'downf':   # j = floor(r/2^32*(i+1))
        for i in range(len(a)-1, 0, -1):
            j = (nxt()*(i+1)) >> 32; a[i], a[j] = a[j], a[i]
    elif variant == 'downpre': # use state before update
        for i in range(len(a)-1, 0, -1):
            j = s % (i+1); nxt(); a[i], a[j] = a[j], a[i]
    used = set(); E = []
    for e in a:
        tr = list(itertools.combinations(e, 3))
        if all(t not in used for t in tr):
            used.update(tr); E.append(e)
    return E
def main_packgen(argv):
    for v in ['down','up','downf','downpre']:
        print(v, len(gen(16,20261127,v)), len(gen(18,20261128,v)))


# ==================== defect ====================
import numpy as np
def main_defect(argv):
    for n,seed in [(16,20261127),(18,20261128)]:
        E=gen(n,seed,'down')
        w=np.arange(2**n,dtype=np.int64)
        bits=[(w>>i)&1 for i in range(n)]
        d=np.zeros(2**n,dtype=np.int32)
        for e in E:
            s=bits[e[0]]+bits[e[1]]+bits[e[2]]+bits[e[3]]
            d+=((s==0)|(s==4))
        m=d.min(); print(n,len(E),'min defect',m,'first minimiser word',int(np.argmin(d)),'#minimisers',int((d==m).sum()))

# ==================== yesctl ====================
def main_yesctl(argv):
    for n,s,dele,w in [(16,20261127,[14,96],9589),(18,20261128,[1,5,32,84],115123)]:
        E=gen(n,s,'down')
        mono=[k for k,e in enumerate(E) if len({(w>>v)&1 for v in e})==1]
        print(n,'monochromatic blocks under word',w,':',mono,'matches T3 deletion list:',mono==dele)
        F=[e for k,e in enumerate(E) if k not in dele]
        open(f'pack{n}_yes.txt','w').write('\n'.join(' '.join(map(str,e)) for e in F)+'\n')

# ==================== pcprove ====================
"""Degree-d multilinear F2 PC closure prover with derivation log (independent of mlclosure.c).
Polynomials: Python ints, bit j <-> monomial MON[j] (subset bitmask of variables, |m|<=d).
Writes a certificate JSON: axioms (edges), products [i, [ids...]] meaning row = x_i * sum(rows ids),
and final [ids...] whose sum is the constant 1."""
import sys, json, itertools
def run(n, d, edges, enc='g', certfile=None):
    MON = [m for k in range(d+1) for m in range(1<<n) if bin(m).count('1')==k]
    IDX = {m:j for j,m in enumerate(MON)}
    DEG = [bin(m).count('1') for m in MON]
    def poly(monos):
        v=0
        for m in monos: v ^= 1<<IDX[m]
        return v
    rows=[]   # all derived rows (polys), id = position
    axioms=[]
    for e in edges:
        allm=[sum(1<<e[j] for j in range(4) if s>>j&1) for s in range(16)]
        P=poly([allm[15]]) if d>=4 else 0
        Q=0
        for m in allm:
            if bin(m).count('1')<=d: Q^=1<<IDX[m]
        if enc=='g':
            if d>=4: Q^=P
            else: Q^=0  # top monomial absent: Q already is p_e with deg-4 term dropped (cancels)
            rows.append(Q); axioms.append(('g',list(e)))
        else:
            rows.append(P); axioms.append(('pos_false',list(e)))  # prod x_j  (all-negative clause)
            rows.append(Q); axioms.append(('neg_false',list(e)))  # prod(1+x_j) (all-positive clause)
    # basis: pivot (highest bit) -> (poly, prov)
    piv={}
    def insert(v,prov):
        while v:
            l=v.bit_length()-1
            if l not in piv: piv[l]=(v,prov); return True
            pv,pp=piv[l]; v^=pv; prov^=pp
        return False
    for k,r in enumerate(rows): insert(r,1<<k)
    MULT=[[None]*len(MON) for _ in range(n)]
    for i in range(n):
        for j,m in enumerate(MON):
            mm=m|(1<<i); MULT[i][j]=IDX.get(mm)
    MASK=[sum(1<<j for j,m in enumerate(MON) if DEG[j]==d and not (m>>i&1)) for i in range(n)]
    def mulx(i,v):
        out=0
        while v:
            l=v.bit_length()-1; v^=1<<l; out^=1<<MULT[i][l]
        return out
    products=[]
    log=[]
    sweep=0
    while True:
        sweep+=1; changed=False
        for i in range(n):
            M=MASK[i]; cp={}; K=[]
            for (v,p) in list(piv.values()):
                while True:
                    t=v&M
                    if not t: K.append((v,p)); break
                    l=t.bit_length()-1
                    if l not in cp: cp[l]=(v,p); break
                    cv,cpv=cp[l]; v^=cv; p^=cpv
            added=0
            for (v,p) in K:
                w=mulx(i,v)
                ids=[k for k in range(p.bit_length()) if p>>k&1]
                rid=len(rows)
                if insert(w,1<<rid):
                    rows.append(w); products.append([i,ids]); added+=1; changed=True
            if added: log.append((sweep,i,added,len(piv)))
            if 0 in piv:
                v,p=piv[0]; assert v==1
                final=[k for k in range(p.bit_length()) if p>>k&1]
                res=dict(n=n,d=d,enc=enc,edges=[list(e) for e in edges],products=products,final=final,verdict='REFUTED',sweep=sweep,var=i,rank=len(piv))
                if certfile: json.dump(res,open(certfile,'w'))
                return res,log
        if not changed:
            res=dict(n=n,d=d,enc=enc,edges=[list(e) for e in edges],verdict='FIXED_POINT',rank=len(piv),ambient=len(MON),sweeps=sweep)
            if certfile: json.dump(res,open(certfile,'w'))
            return res,log
def main_prove(argv):
    n=int(argv[1]); d=int(argv[2]); enc=argv[3]; ef=argv[4]; cf=argv[5] if len(argv)>5 else None
    edges=[tuple(map(int,l.split())) for l in open(ef) if l.strip()]
    res,log=run(n,d,edges,enc,cf)
    for x in log: print('sweep %d var %d +%d rank %d'%x)
    print(res['verdict'],{k:res[k] for k in res if k in('rank','sweep','var','sweeps','ambient')},'products',len(res.get('products',[])),'final_len',len(res.get('final',[])))


# ==================== pccheck ====================
"""Independent checker for pcprove.py certificates. Polynomials = Python sets of monomials
(monomial = variable bitmask), F2 addition = symmetric difference, x_i^2 = x_i.
Checks: axioms rebuilt from the hypergraph only; every product row x_i*S has all monomials of
degree <= d AND the multiplicand S has degree <= d; final sum == {empty monomial} (= constant 1).
Also checks that the hypergraph is NAE4-UNSAT is NOT assumed (soundness of PC suffices)."""
def main_check(argv):
    c=json.load(open(argv[1])); n,d,enc=c['n'],c['d'],c['enc']
    assert c['verdict']=='REFUTED'
    deg=lambda m: bin(m).count('1')
    rows=[]
    for e in c['edges']:
        assert len(set(e))==4 and all(0<=v<n for v in e)
        mons=[sum(1<<e[j] for j in range(4) if s>>j&1) for s in range(16)]
        allx={mons[15]}; allc=set(mons)     # prod x ; prod (1+x) expanded
        if enc=='g':
            p=allx ^ allc                     # NAE4 violation indicator, degree 3
            assert max(map(deg,p))<=d; rows.append(p)
        else:
            assert d>=4; rows.append(allx); rows.append(allc)
    # triple-packing property (every 3-set in at most one edge) - recorded, not needed for soundness
    tri={}
    for e in c['edges']:
        for k in range(4):
            t=tuple(sorted(set(e)-{e[k]})); tri[t]=tri.get(t,0)+1
    packing=max(tri.values())==1
    maxdeg_seen=0
    for i,ids in c['products']:
        assert all(0<=k<len(rows) for k in ids)
        S=set()
        for k in ids: S^=rows[k]
        assert S and max(map(deg,S))<=d
        P=set()
        for m in S: P^={m|(1<<i)}
        assert P and max(map(deg,P))<=d, 'inadmissible product'
        maxdeg_seen=max(maxdeg_seen,max(map(deg,P)))
        rows.append(P)
    F=set()
    for k in c['final']: F^=rows[k]
    assert F=={0}, 'final combination is not the constant 1'
    print('CERTIFICATE OK: degree-%d multilinear F2 PC refutation (%s encoding), n=%d, %d edges, %d product rows, final combination of %d rows; triple-packing=%s; max product degree %d'%(d,enc,n,len(c['edges']),len(c['products']),len(c['final']),packing,maxdeg_seen))

# ==================== mincore ====================
"""Shrink an UNSAT NAE4 hypergraph to an edge-minimal UNSAT sub-hypergraph (deletion-based, fixed order),
then test degree-d multilinear closure on the core."""
import sys, subprocess
from pysat.solvers import Cadical153
def sat(E):
    s=Cadical153()
    for e in E: s.add_clause([v+1 for v in e]); s.add_clause([-(v+1) for v in e])
    r=s.solve(); s.delete(); return r
def core(E):
    assert not sat(E); C=list(E); k=0
    while k<len(C):
        T=C[:k]+C[k+1:]
        if not sat(T): C=T
        else: k+=1
    return C
def main_mincore(argv):
    n=int(argv[1]); seed=int(argv[2])
    E=gen(n,seed,'down'); C=core(E)
    vs=sorted({v for e in C for v in e})
    # verify minimality
    assert all(sat(C[:k]+C[k+1:]) for k in range(len(C)))
    fn=f'core_{n}_{seed}.txt'; open(fn,'w').write('\n'.join(' '.join(map(str,e)) for e in C)+'\n')
    print(f'n={n} seed={seed} edges={len(E)} core_edges={len(C)} core_vertices={len(vs)}')
    for d in argv[3].split(','):
        r=subprocess.run(['./mlclosure',str(n),d,'g',fn],capture_output=True,text=True).stdout.strip().splitlines()[-1]
        print(' d=%s: %s'%(d,r))


# ==================== scan ====================
from pysat.solvers import Cadical153
def nae_sat(n,E):
    s=Cadical153()
    for e in E:
        s.add_clause([v+1 for v in e]); s.add_clause([-(v+1) for v in e])
    r=s.solve(); s.delete(); return r
def main_scan(argv):
    out=[]
    for n in map(int,argv[1].split(',')):
        for seed in range(int(argv[2]),int(argv[3])):
            E=gen(n,seed,'down'); fn=f'/tmp/scan_{n}_{seed}.txt'
            open(fn,'w').write('\n'.join(' '.join(map(str,e)) for e in E)+'\n')
            sat=nae_sat(n,E); t=time.time()
            r=subprocess.run(['./mlclosure',str(n),'4','g',fn],capture_output=True,text=True).stdout.strip().splitlines()[-1]
            rec=dict(n=n,seed=seed,edges=len(E),sat=sat,pc4=r.split()[0],detail=r,secs=round(time.time()-t,2))
            print(json.dumps(rec),flush=True); out.append(rec)

# ==================== corescan ====================
def main_corescan(argv):
    for n in map(int,argv[1].split(',')):
        for seed in range(int(argv[2]),int(argv[3])):
            E=gen(n,seed,'down')
            if sat(E): continue
            C=core(E); fn=f'/tmp/core_{n}_{seed}.txt'
            open(fn,'w').write('\n'.join(' '.join(map(str,e)) for e in C)+'\n')
            vs=len({v for e in C for v in e}); res={}
            for d in (3,4,5,6):
                r=subprocess.run(['./mlclosure',str(n),str(d),'g',fn],capture_output=True,text=True).stdout.strip().splitlines()[-1]
                res[d]=r.split()[0]
                if res[d]=='REFUTED': break
            mindeg=min([d for d in res if res[d]=='REFUTED'],default=None)
            print(json.dumps(dict(n=n,seed=seed,edges=len(E),core_edges=len(C),core_vertices=vs,pc=res,min_refuting_degree=mindeg)),flush=True)

# ==================== tables ====================
def main_tables(argv):
    R=[json.loads(l) for l in open('scan_results.jsonl') if l.startswith('{')]
    g=collections.defaultdict(list)
    for r in R: g[r['n']].append(r)
    L=['\\begin{tabular}{rrrrrrr}','\\toprule','$n$ & inst. & edges & UNSAT & PC4 refuted & refuted\\,\\&\\,SAT & UNSAT not refuted\\\\','\\midrule']
    for n in sorted(g):
        X=g[n]; u=[r for r in X if not r['sat']]
        L.append(f"{n} & {len(X)} & {min(r['edges'] for r in X)}--{max(r['edges'] for r in X)} & {len(u)} & {sum(r['pc4']=='REFUTED' for r in X)} & {sum(r['pc4']=='REFUTED' and r['sat'] for r in X)} & {sum(r['pc4']!='REFUTED' for r in u)}\\\\")
    L+=['\\bottomrule','\\end{tabular}']
    open('../scan_table.tex','w').write('\n'.join(L)+'\n')
    tot=len(R); print('scan total',tot,'unsat',sum(not r['sat'] for r in R),'max secs',max(r['secs'] for r in R))
    C=[json.loads(l) for l in open('corescan_results.jsonl') if l.startswith('{')]
    g=collections.defaultdict(list)
    for r in C: g[r['n']].append(r)
    L=['\\begin{tabular}{rrrrrrr}','\\toprule','$n$ & cores & core edges & core vertices & PC3 & PC4 & PC5\\\\','\\midrule']
    for n in sorted(g):
        X=g[n]
        f=lambda d,v: sum(r['pc'].get(str(d))==v for r in X)
        L.append(f"{n} & {len(X)} & {min(r['core_edges'] for r in X)}--{max(r['core_edges'] for r in X)} & {min(r['core_vertices'] for r in X)}--{max(r['core_vertices'] for r in X)} & {f(3,'FIXED_POINT')} fixed & {f(4,'FIXED_POINT')} fixed & {f(5,'REFUTED')} refuted\\\\")
    L+=['\\bottomrule','\\end{tabular}']
    open('../core_table.tex','w').write('\n'.join(L)+'\n')
    print('cores',len(C),collections.Counter(r['min_refuting_degree'] for r in C))

if __name__=='__main__':
    cmd=sys.argv[1]; argv=[sys.argv[0]]+sys.argv[2:]
    {'packgen':main_packgen,'defect':main_defect,'yesctl':main_yesctl,'prove':main_prove,'check':main_check,
     'mincore':main_mincore,'scan':main_scan,'corescan':main_corescan,'tables':main_tables}[cmd](argv)
