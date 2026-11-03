#!/usr/bin/env python3
"""LSPV-2 #351: exhaustive three-variable typed substitution audit.
Fixed-size operator audit, NOT a global minimum-DAG optimizer.
Use Python >=3.10, no dependencies. Run in a directory containing raw JSON.
"""
import itertools, json, pathlib, hashlib, time, resource

PATS=list(itertools.product((-1,0,1),repeat=3))
MASK=255
def table(fn):
    return sum(int(bool(fn([(a>>i)&1 for i in range(3)])))<<a for a in range(8))
def pin(t,p):
    out=0
    for a in range(8):
        j=sum(((a>>i)&1 if p[i]<0 else p[i])<<i for i in range(3))
        out|=((t>>j)&1)<<a
    return out
def support(t):
    v=0
    for i in range(3):
        if any(((t>>a)&1)!=((t>>(a^(1<<i)))&1) for a in range(8)):v|=1<<i
    return v
def row(mask,rhs):
    return table(lambda a: sum((mask>>i&1)*a[i] for i in range(3))%2==rhs)
def rowpin(mask,rhs,p):
    fixed=0
    for i in range(3):
        if (mask>>i&1) and p[i]>=0:
            fixed^=p[i];mask &=~(1<<i)
    return mask,rhs^fixed
def models(clauses,n):
    return sum(all(any(((a>>(abs(l)-1))&1)==int(l>0) for l in c) for c in clauses) for a in range(1<<n))
def parse(src):
    lines=[s.strip() for s in src.splitlines() if s.strip() and not s.lstrip().startswith('c')]
    if not lines:raise ValueError('empty')
    h=lines[0].split()
    if len(h)!=4 or h[:2]!=['p','cnf'] or not h[2].isdigit() or not h[3].isdigit():raise ValueError('header')
    n,m=int(h[2]),int(h[3])
    if len(lines)!=m+1:raise ValueError('count')
    clauses=[]
    for line in lines[1:]:
        toks=line.split()
        if len(toks)<2 or toks[-1]!='0' or '0' in toks[:-1]:raise ValueError('terminator')
        try:c=list(map(int,toks[:-1]))
        except:raise ValueError('literal')
        if not c or any(x==0 or abs(x)>n for x in c) or len(set(c))!=len(c):raise ValueError('literal')
        clauses.append(c)
    return clauses
def resolve(left,right,p):
    if p not in left or -p not in right:raise ValueError('bad pivot')
    c=set(left+right);c.discard(p);c.discard(-p)
    if any(-x in c for x in c):raise ValueError('tautology')
    return sorted(c,key=lambda l:(abs(l),l))
def main():
    t0=time.perf_counter()
    restricted=[[pin(f,p) for f in range(256)] for p in PATS]
    and_count=imp_count=support_count=0
    for r in restricted:
        for f in range(256):
            assert support(r[f])&~support(f)==0
            support_count+=1
            for g in range(256):
                assert r[f&g]==(r[f]&r[g]);and_count+=1
                if not(f&(~g&255)):
                    assert not(r[f]&(~r[g]&255))
                    imp_count+=1
    affine_count=0
    for p in PATS:
        for m1,b1,m2,b2 in itertools.product(range(8),range(2),range(8),range(2)):
            x,y=rowpin(m1,b1,p);u,v=rowpin(m2,b2,p)
            a,b=rowpin(m1^m2,b1^b2,p)
            assert (a,b)==(x^u,y^v)
            assert pin(row(m1,b1),p)==row(x,y)
            affine_count+=1
    gates=gc=gn=0
    for g in range(16):
        for s,t in itertools.product((-1,0,1),repeat=2):
            out={(g>>((s if s>=0 else a)+2*(t if t>=0 else b)))&1
                 for a,b in itertools.product((0,1),repeat=2)}
            gates+=1
            if s>=0 or t>=0:
                if len(out)==1:gc+=1
                else:gn+=1
    assert (and_count,imp_count,support_count,affine_count,gates,gc,gn)==(1769472,177147,6912,6912,144,96,32)
    z=table(lambda a:a[0]);a=table(lambda a:a[1]);b=table(lambda a:a[2])
    p=(0,-1,-1)
    assert pin(z|a,p)==a and pin((255^z)|b,p)==255
    assert pin(a|b,p)==(a|b) and (a|b)!=a
    assert (models([[1],[-1]],2),models([[1,2],[-1,2]],2))==(0,2)
    edges=list(itertools.combinations(range(4),2))
    def k4(charge):
        return sum(all(sum((x>>i)&1 for i,e in enumerate(edges) if v in e)%2==charge[v] for v in range(4)) for x in range(64))
    assert (k4([1,0,0,0]),k4([0,0,0,0]))==(0,8)
    invalid=['p cnf 1 2\n1 0','p cnf 1 1\n2 0','p cnf 1 1\n0',
             'p cnf 1 1\nx 0','q cnf 1 1\n1 0','p cnf 1 1\n1 1 0']
    for s in invalid:
        try:parse(s)
        except ValueError:pass
        else:raise AssertionError('accepted malformed')
    assert resolve([1],[-1],1)==[]
    for c,d,p in [([1],[-1],2),([1,2],[1,-2],1)]:
        try:resolve(c,d,p)
        except ValueError:pass
        else:raise AssertionError('forged pivot accepted')
    record=pathlib.Path(__file__).resolve().parents[2]/'results/raw/arc/2026-11-02_2216_LSPV2_LOCAL_RESTRICTION_PIVOT_FIREWALL351.json'
    if record.exists():
        raw=json.loads(record.read_text())
        for key,value in dict(and_commutations=and_count,
            local_implication_restrictions=imp_count,
            support_shrink_checks=support_count,
            affine_row_pair_restrictions=affine_count,
            gate_partial_cases=gates,gate_constant_outputs_after_pinning=gc,
            gate_nonconstant_outputs_after_pinning=gn).items():
            assert raw[key]==value
    print(json.dumps({'pass':True,'and':and_count,'implications':imp_count,
        'support':support_count,'affine':affine_count,
        'gates':gates,'constant_gate_restrictions':gc,
        'malformed_rejected':6,'forged_res_rejected':2,
        'odd_even_k4_models':[0,8],
        'wall_seconds':round(time.perf_counter()-t0,3),
        'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
if __name__=='__main__':main()
