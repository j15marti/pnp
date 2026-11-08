#!/usr/bin/env python3
"""Independent exact finite gadget/K4/bit-PHP test. No JavaScript imports."""
import itertools,json

def val(l,d): return d[abs(l)] if l>0 else not d[abs(l)]
def clause(c,d): return any(val(l,d) for l in c)
def proper(c): return len(c)==3 and len({abs(v) for v in c})==3 and all(c)
def norm(c,j):
    seen={}
    for l in c:
        if abs(l) in seen and seen[abs(l)]!=(l>0): return [[4*(3*j+1+k)+1 for k in range(3)]]*8
        seen[abs(l)]=(l>0)
    x=[i if s else -i for i,s in seen.items()]
    p=[4*(3*j+1+k)+1 for k in range(3)]
    out=[]
    for r in range(8):
        if not x: row=[-v if (r>>k)&1 else v for k,v in enumerate(p)]
        elif len(x)==1 and r<4: row=[4*x[0],-p[0] if r&2 else p[0],-p[1] if r&1 else p[1]]
        elif len(x)==2 and r<2: row=[4*x[0],4*x[1],-p[0] if r else p[0]]
        elif len(x)==3 and r==0: row=[4*l for l in x]
        else: row=p[:]
        out.append(row)
    return out

counts=dict(clauses=0,gadget_checks=0,guard_checks=0)
for n in range(1,4):
    choices=[s*v for v in range(1,n+1) for s in (1,-1)]
    for w in range(4):
        for c in itertools.product(choices,repeat=w):
            counts['clauses']+=1
            j=1;g=norm(c,j)
            assert len(g)==8 and all(proper(row) for row in g)
            ids=[4*(3*j+1+k)+1 for k in range(3)]
            for bits in itertools.product((False,True),repeat=n):
                a={i+1:bits[i] for i in range(n)}
                exists=False
                for aux in itertools.product((False,True),repeat=3):
                    d={4*i:bits[i-1] for i in range(1,n+1)}
                    d.update(zip(ids,aux))
                    exists |= all(clause(row,d) for row in g)
                assert exists==clause(c,a)
                counts['gadget_checks']+=1
                for row in g:
                    for z in (False,True):
                        for mask in range(8):
                            d={abs(l):bool(mask>>k&1) for k,l in enumerate(row)}
                            av=4*(8*j+2)+2
                            works=False
                            for a0 in (False,True):
                                d[av]=a0;d[3]=z
                                works |= clause([row[0],row[1],av],d) and clause([-av,row[2],3],d)
                            assert works==(z or clause(row,d))
                            counts['guard_checks']+=1
edges=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
sat=unsat=0
for charge in range(16):
    F=[]
    for v in range(4):
        inc=[i+1 for i,e in enumerate(edges) if v in e]
        for assignment in range(8):
            if assignment.bit_count()%2!=(charge>>v)&1:
                F.append([-i if assignment>>k&1 else i for k,i in enumerate(inc)])
    assert len(F)==16 and all(proper(c) for c in F)
    ans=any(all(clause(c,{i+1:bool(a>>i&1) for i in range(6)}) for c in F) for a in range(64))
    assert ans==(charge.bit_count()%2==0)
    if ans:sat+=1
    else:unsat+=1
orig=[]
for i in range(5):
    for j in range(i+1,5):
        for h in range(4):
            orig.append([v if not (h>>k)&1 else -v for p in (i,j) for k in range(2) for v in [2*p+k+1]])
assert len(orig)==40
for holes in itertools.product(range(4),repeat=5):
    x={2*i+k+1:bool(holes[i]>>k&1) for i in range(5) for k in range(2)}
    assert not all(clause(c,x) for c in orig)
F=[];new=11
for c in orig:
    F.extend([[c[0],c[1],new],[-new,c[2],c[3]]]);new+=1
assert len(F)==80 and all(proper(c) for c in F)
print(json.dumps({'run':'LSPV-2/487','status':'COMPUTATIONAL','independent_python':counts,
 'K4_SAT':sat,'K4_UNSAT':unsat,'bitPHP_ell2_original':40,'bitPHP_ell2_strict3':80,
 'bitPHP_pigeon_assignments':1024,'native_FLMV':False},indent=2))
