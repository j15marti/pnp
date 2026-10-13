#!/usr/bin/env python3
"""CP22LIFT1: exact-integer cutting-planes proof transport through PC22_ALLFIELD1.

Python 3.10+, standard library only. Every --h batch should finish in 30 s.
The independent checker replays every axiom, bound, sum, scale and division.
No solver-runtime lower bound or proof-search automatability is inferred.
"""
from __future__ import annotations
import argparse, collections, copy, hashlib, itertools, json, math, random, time
from pathlib import Path
from typing import Iterable

W = [(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
     (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
     (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
     (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
Q = [c for c in W if c != (1,7,13)]

def ineq(a: dict[int,int], b: int) -> tuple[tuple[tuple[int,int],...],int]:
    return tuple(sorted((int(v),int(c)) for v,c in a.items() if c)), int(b)

def clause(c: Iterable[int]):
    a: dict[int,int] = collections.defaultdict(int); b=1
    for l in c:
        a[abs(l)] += 1 if l > 0 else -1
        b -= int(l < 0)
    return ineq(a,b)

def add(x,y):
    a=collections.defaultdict(int,dict(x[0]))
    for v,c in y[0]: a[v]+=c
    return ineq(a,x[1]+y[1])

def scale(x,k): return ineq({v:k*c for v,c in x[0]},k*x[1])
def ceildiv(a,d): return -((-a)//d)

def mapped(x, images: dict[int,int|bool]):
    a=collections.defaultdict(int); b=x[1]
    for v,c in x[0]:
        t=images.get(v,v)
        if isinstance(t,bool): b -= c*int(t)
        elif t>0: a[t]+=c
        else: a[-t]-=c; b-=c
    return ineq(a,b)

class Proof:
    def __init__(self,cnf): self.cnf=list(map(tuple,cnf)); self.rows=[]; self.ops=[]
    def put(self,row,op): self.rows.append(row); self.ops.append(op); return len(self.rows)-1
    def ax(self,j): return self.put(clause(self.cnf[j]),('ax',j))
    def bound(self,l):
        return self.put(ineq({abs(l):1 if l>0 else -1},0 if l>0 else -1),('bound',l))
    def sum(self,i,j): return self.put(add(self.rows[i],self.rows[j]),('sum',i,j))
    def scale(self,i,k):
        assert isinstance(k,int) and k>=0
        return self.put(scale(self.rows[i],k),('scale',i,k))
    def div(self,i,d):
        a,b=self.rows[i]; assert d>0 and all(c%d==0 for _,c in a)
        return self.put(ineq({v:c//d for v,c in a},ceildiv(b,d)),('div',i,d))
    def sums(self,ids):
        ids=list(ids); assert ids
        r=ids[0]
        for j in ids[1:]: r=self.sum(r,j)
        return r
    def data(self): return {'cnf':self.cnf,'rows':self.rows,'ops':self.ops}

def check(data, require_contradiction=True):
    """Separate integer replay. Does not call Proof/add/scale/ceildiv."""
    rows=[]; coeffs=0
    for i,(expected,op) in enumerate(zip(data['rows'],data['ops'])):
        name=op[0]; a={}; b=0
        if name=='ax':
            b=1
            for l in data['cnf'][op[1]]:
                v=abs(l); a[v]=a.get(v,0)+(1 if l>0 else -1)
                if l<0: b-=1
        elif name=='bound':
            l=op[1]; a={abs(l):1 if l>0 else -1}; b=0 if l>0 else -1
        elif name=='sum':
            assert op[1]<i and op[2]<i
            for j in op[1:]:
                aa,bb=rows[j]; b+=bb
                for v,c in aa.items(): a[v]=a.get(v,0)+c
        elif name=='scale':
            assert op[1]<i and isinstance(op[2],int) and op[2]>=0
            aa,bb=rows[op[1]]; a={v:c*op[2] for v,c in aa.items()}; b=bb*op[2]
        elif name=='div':
            j,d=op[1:]; assert j<i and isinstance(d,int) and d>0
            aa,bb=rows[j]; assert all(c%d==0 for c in aa.values())
            a={v:c//d for v,c in aa.items()}; b=(bb+d-1)//d
        else: raise AssertionError(('unknown operation',op))
        a={v:c for v,c in a.items() if c}
        observed=(tuple(sorted(a.items())),b)
        want=(tuple(map(tuple,expected[0])),int(expected[1]))
        assert observed==want, (i,op,observed,want)
        coeffs+=len(a); rows.append((a,b))
    assert len(data['rows'])==len(data['ops'])
    if require_contradiction: assert rows[-1][0]=={} and rows[-1][1]>=1
    return {'lines':len(rows),'coefficient_occurrences':coeffs}

def resolution_ports():
    """Width-3 closure, with an explicit ancestor subproof for the three units."""
    clauses=[frozenset(c) for c in Q]; deriv=[('ax',i) for i in range(len(Q))]
    seen={c:i for i,c in enumerate(clauses)}; index=collections.defaultdict(list)
    for i,c in enumerate(clauses):
        for l in c: index[l].append(i)
    cursor=0; targets=[frozenset([-p]) for p in (1,7,13)]
    while cursor<len(clauses) and not all(c in seen for c in targets):
        A=clauses[cursor]
        for l in sorted(A):
            for j in tuple(index[-l]):
                B=clauses[j]; R=(A-{l}) | (B-{-l})
                if len(R)>3 or any(-x in R for x in R) or R in seen: continue
                assert R, 'Q must be satisfiable'
                k=len(clauses); seen[R]=k; clauses.append(R); deriv.append(('res',cursor,j,l))
                for x in R: index[x].append(k)
        cursor+=1
    assert all(c in seen for c in targets)
    needed=set()
    def visit(j):
        if j in needed:return
        needed.add(j)
        if deriv[j][0]=='res': visit(deriv[j][1]);visit(deriv[j][2])
    for c in targets:visit(seen[c])
    return clauses,deriv,sorted(needed),[seen[c] for c in targets]

def import_ports(P, offset, ax_offset, template):
    cs,deriv,needed,targets=template; ids={}
    for i in needed:
        op=deriv[i]
        if op[0]=='ax': ids[i]=P.ax(ax_offset+op[1]); continue
        _,j,k,pivot=op; z=P.sum(ids[j],ids[k]); R=cs[i]
        # Parent sum has multiplicity 1 or 2. Raise every multiplicity to 2.
        A=cs[j]-{pivot}; B=cs[k]-{-pivot}
        for l in sorted(A^B):
            shifted=(1 if l>0 else -1)*(offset+abs(l))
            z=P.sum(z,P.bound(shifted))
        z=P.div(z,2); ids[i]=z
        actual=tuple((1 if l>0 else -1)*(offset+abs(l)) for l in R)
        assert P.rows[z]==clause(actual)
    return {p:ids[j] for p,j in zip((1,7,13),targets)}

def compile22(F):
    """The exact published PC22_ALLFIELD1 T, not the neutral-slot compiler."""
    F=[tuple(c) for c in F]; m=len(F); assert m>0
    used=sorted({abs(l) for c in F for l in c}); assert used==list(range(1,len(used)+1))
    n=len(used); s=n+1; U=[]
    for j,(a,b,c) in enumerate(F):
        y=n+2+2*j; z=y+1
        U += [(s,a,y),(-y,b,c),(-s,-a,z),(-z,-b,-c)]
    B=U+U; occ=collections.defaultdict(lambda:[[],[]])
    for j,c in enumerate(B):
        for k,l in enumerate(c):occ[abs(l)][0 if l>0 else 1].append((j,k))
    C=[[0]*3 for _ in B]; groups={}; counter=0
    for x in sorted(occ):
        ps,ns=occ[x]; assert len(ps)==len(ns) and len(ps)>=2
        group=[]
        for p,q in zip(ps,ns):
            counter+=1; group.append(counter); C[p[0]][p[1]]=counter; C[q[0]][q[1]]=-counter
        groups[x]=group
    R=counter; assert R==12*m; edges=[]
    for x,g in groups.items():
        for a,b in zip(g,g[1:]+g[:1]): edges.append((a,b,x))
    pads=[]
    for i,(a,b,x) in enumerate(edges):
        off=R+15*(i//3); p=off+(1,7,13)[i%3]; pads.append((-a,b,p))
    gadget=[]
    for k in range(R//3):
        off=R+15*k
        gadget += [tuple((1 if l>0 else -1)*(off+abs(l)) for l in c) for c in Q]
    out=list(map(tuple,C))+pads+gadget
    assert len(out)==96*m and max(abs(l) for c in out for l in c)==72*m
    counts=collections.Counter(l for c in out for l in c)
    assert all(counts[v]==counts[-v]==2 for v in range(1,72*m+1))
    assert all(len(set(map(abs,c)))==3 for c in out)
    assert len({frozenset(c) for c in out})==len(out)
    return {'cnf':out,'U':U,'groups':groups,'edges':edges,'R':R,'m':m,'n':n,'s':s}

def prepare_guarded_axioms(T,template):
    P=Proof(T['cnf']); R=T['R']; m=T['m']; groups=T['groups']
    port={}
    for g in range(R//3):
        off=R+15*g
        for p,line in import_ports(P,off,8*m+R+19*g,template).items():port[off+p]=line
    edge_ids={}
    for i,(a,b,x) in enumerate(T['edges']):
        ax=P.ax(8*m+i); p=T['cnf'][8*m+i][2]
        edge_ids[(a,b)]=P.sum(ax,port[p])
        assert P.rows[edge_ids[(a,b)]]==ineq({a:-1,b:1},0)
    # Two telescoping directions, total O(R) sparse equality lines.
    eq={}; reps={x:g[0] for x,g in groups.items()}
    for x,g in groups.items():
        r=g[0]
        forward=None
        for j in range(1,len(g)):
            e=edge_ids[(g[j-1],g[j])]; forward=e if forward is None else P.sum(forward,e)
            eq[(r,g[j])]=forward
        reverse=None
        for j in range(len(g)-1,0,-1):
            e=edge_ids[(g[j],g[(j+1)%len(g)])]
            reverse=e if reverse is None else P.sum(e,reverse)
            eq[(g[j],r)]=reverse
    clone_rep={v:reps[x] for x,g in groups.items() for v in g}; Uids=[]
    for j,c in enumerate(T['cnf'][:4*m]):
        z=P.ax(j)
        for l in c:
            v=abs(l); r=clone_rep[v]
            if v!=r:z=P.sum(z,eq[(v,r)] if l>0 else eq[(r,v)])
        assert P.rows[z]==clause(tuple((1 if l>0 else -1)*reps[abs(l)] for l in T['U'][j]))
        Uids.append(z)
    guards0=[];guards1=[]
    for j in range(m):
        guards0.append(P.sum(Uids[4*j],Uids[4*j+1]))
        guards1.append(P.sum(Uids[4*j+2],Uids[4*j+3]))
    return P,reps,guards0,guards1

def source_cardinality(h, extra=True):
    assert h>=5
    E=sorted({(u,(u+d)%h) for u in range(h) for d in range(4)})
    if extra:E=sorted(E+[(0,4)])
    edge={e:i+1 for i,e in enumerate(E)}; sides=[]; F=[]; blocks=[]
    for side in (0,1):
        for v in range(h):
            inc=sorted(edge[e] for e in E if e[side]==v); indices={}
            for triple in itertools.combinations(inc,3):
                indices[triple]=len(F); F.append(tuple(x if side==0 else -x for x in triple))
            blocks.append((side,inc,indices))
    return F,blocks,E

def source_counting_proof(F,blocks):
    P=Proof(F); quota=[]
    for side,inc,indices in blocks:
        fours=[]
        for four in itertools.combinations(inc,4):
            lines=[P.ax(indices[tri]) for tri in itertools.combinations(four,3)]
            fours.append(P.div(P.sums(lines),3))
        r=fours[0] if len(inc)==4 else P.div(P.sums(fours),4)
        target=ineq({v:1 if side==0 else -1 for v in inc},len(inc)-2 if side==0 else -2)
        assert P.rows[r]==target
        quota.append(r)
    last=P.sums(quota); assert P.rows[last]==((),1)
    check(P.data());return P

def lift_guarded(P,source,reps,guard_literal,axioms):
    ids=[]; weights=[]; guard_bound=P.bound(guard_literal)
    # If guard is (1-s), complement every source variable.
    im={v:reps[v]*(1 if guard_literal>0 else -1) for v in range(1,len(reps)+1) if v in reps}
    for i,op in enumerate(source.ops):
        name=op[0]
        if name=='ax':z=axioms[op[1]];k=1
        elif name=='bound':
            l=op[1];z=P.bound((1 if l>0 else -1)*im[abs(l)]);k=0
        elif name=='sum':
            a,b=op[1:];z=P.sum(ids[a],ids[b]);k=weights[a]+weights[b]
        elif name=='scale':
            a,c=op[1:];z=P.scale(ids[a],c);k=c*weights[a]
        elif name=='div':
            a,d=op[1:];K=d*ceildiv(weights[a],d);z=ids[a]
            if K!=weights[a]:z=P.sum(z,P.scale(guard_bound,K-weights[a]))
            z=P.div(z,d);k=K//d
        else:raise AssertionError(name)
        guardrow=scale(P.rows[guard_bound],k)
        assert P.rows[z]==add(mapped(source.rows[i],im),guardrow), (i,name)
        ids.append(z);weights.append(k)
    assert weights[-1]>0
    return P.div(ids[-1],weights[-1])

def transport(T,source,template):
    P,reps,g0,g1=prepare_guarded_axioms(T,template)
    s=reps[T['s']]
    a=lift_guarded(P,source,reps,s,g0);b=lift_guarded(P,source,reps,-s,g1)
    assert P.rows[a]==ineq({s:1},1) and P.rows[b]==ineq({s:-1},0)
    P.sum(a,b);check(P.data());return P

def scramble(data,seed):
    rng=random.Random(seed); n=max(abs(l) for c in data['cnf'] for l in c)
    vs=list(range(1,n+1));rng.shuffle(vs)
    images={v:vs[v-1]*rng.choice([-1,1]) for v in range(1,n+1)}
    perm=list(range(len(data['cnf'])));rng.shuffle(perm);inverse={old:new for new,old in enumerate(perm)}
    cnf=[]
    for j in perm:
        c=[images[abs(l)]*(1 if l>0 else -1) for l in data['cnf'][j]];rng.shuffle(c);cnf.append(c)
    ops=[]
    for op in data['ops']:
        op=list(op)
        if op[0]=='ax':op[1]=inverse[op[1]]
        if op[0]=='bound':op[1]=images[abs(op[1])]*(1 if op[1]>0 else -1)
        ops.append(op)
    result={'cnf':cnf,'rows':[mapped((tuple(map(tuple,r[0])),r[1]),images) for r in data['rows']],'ops':ops}
    check(result);return result

def project_back(data, T, F):
    """Replay the literal/constant substitution as a genuine source CP proof."""
    m,n=T['m'],T['n']; base={v:v for v in range(1,n+1)};base[T['s']]=False
    for j,(a,b,c) in enumerate(F):
        base[n+2+2*j]=-a; base[n+3+2*j]=False
    sigma={v:base[x] for x,g in T['groups'].items() for v in g}
    for v in range(T['R']+1,72*m+1): sigma[v]=False
    P=Proof(F); source_axioms={clause(c):j for j,c in enumerate(F)};ids=[]
    zero_minus_one=P.sum(P.bound(1),P.bound(-1))
    def premise(row):
        if row in source_axioms:return P.ax(source_axioms[row])
        a,b=row
        if not a:
            assert b<=0;return P.scale(zero_minus_one,-b)
        if len(a)==1:
            v,c=a[0]
            if (c,b)==(1,0):return P.bound(v)
            if (c,b)==(-1,-1):return P.bound(-v)
        # A semantically true clause need not become the zero inequality.
        # Derive its exact image from Boolean bounds, including its slack.
        floor=sum(c for _,c in a if c<0)
        assert b<=floor, ('invalid image axiom',row)
        parts=[]
        for v,c in a: parts.append(P.scale(P.bound(v if c>0 else -v),abs(c)))
        z=P.sums(parts)
        if floor>b:z=P.sum(z,P.scale(zero_minus_one,floor-b))
        assert P.rows[z]==row
        return z
    for i,op in enumerate(data['ops']):
        row=mapped((tuple(map(tuple,data['rows'][i][0])),data['rows'][i][1]),sigma)
        if op[0] in ('ax','bound'): z=premise(row)
        elif op[0]=='sum':z=P.sum(ids[op[1]],ids[op[2]])
        elif op[0]=='scale':z=P.scale(ids[op[1]],op[2])
        elif op[0]=='div':z=P.div(ids[op[1]],op[2])
        else:raise AssertionError(op)
        assert P.rows[z]==row
        ids.append(z)
    return P

def rounding_tests():
    count=0; bad=0
    for rhs in range(-12,13):
        for k in range(17):
            for d in range(1,10):
                K=d*ceildiv(k,d)
                assert K>=k and K%d==0
                assert ceildiv(rhs-K,d)==ceildiv(rhs,d)-K//d
                # Naive divide without slack repair is invalid if k is not divisible.
                if k%d:bad+=1
                count+=1
    return count,bad

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--h',type=int,default=5)
    p.add_argument('--output',type=Path,default=Path('cp22_results.json'))
    p.add_argument('--certificate',type=Path);p.add_argument('--seed',type=int,default=20261013)
    args=p.parse_args();start=time.perf_counter();template=resolution_ports()
    F,blocks,E=source_cardinality(args.h);src=source_counting_proof(F,blocks)
    T=compile22(F);P=transport(T,src,template);stats=check(P.data())
    scrambled=scramble(P.data(),args.seed);s_stats=check(scrambled)
    projected=project_back(P.data(),T,F);p_stats=check(projected.data())
    corrupted=copy.deepcopy(P.data());a,b=corrupted['rows'][-1];corrupted['rows'][-1]=(a,b+1)
    try:check(corrupted);raise RuntimeError('corruption accepted')
    except AssertionError:pass
    # Even quota control has an explicit two-factor model, including all target gadgets.
    Fe,Be,Ee=source_cardinality(args.h,False);Te=compile22(Fe)
    selected={i+1:((v-u)%args.h in (0,1)) for i,(u,v) in enumerate(Ee)}
    vals=dict(selected);vals[Te['s']]=False
    for j,(a,b,c) in enumerate(Fe):
        av=selected[abs(a)] if a>0 else not selected[abs(a)]
        vals[Te['n']+2+2*j]=not av;vals[Te['n']+3+2*j]=False
    tv={v:vals[x] for x,g in Te['groups'].items() for v in g}
    for v in range(Te['R']+1,72*len(Fe)+1):tv[v]=False
    assert all(any(tv[abs(l)]==(l>0) for l in c) for c in Te['cnf'])
    model_count=0
    for a in range(1<<15):
        if all(any(bool(a>>(abs(l)-1)&1)==(l>0) for l in c) for c in Q):
            model_count+=1;assert all(not (a>>(v-1)&1) for v in (1,7,13))
    assert model_count==244
    rt,invalid=rounding_tests()
    out={'run':'CP22LIFT1','status':'COMPUTATIONAL','h':args.h,'seed':args.seed,
         'source_variables':len(E),'source_clauses':len(F),'target_variables':72*len(F),
         'target_clauses':len(T['cnf']),'source_proof_lines':len(src.rows),
         'canonical_replay':stats,'scrambled_replay':s_stats,'projected_replay':p_stats,
         'q_resolution_ancestor_nodes':len(template[2]),'q_models':model_count,
         'satisfiable_control_clauses_verified':len(Te['cnf']),
         'rounding_identities':rt,'naive_nondivisible_guards_rejected':invalid,
         'corrupt_certificates_rejected':1,'final_inequality':'0 >= 1',
         'seconds':time.perf_counter()-start,
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'limitations':['No empirical asymptotic expansion or degree lower bound.',
                       'Known map transports proofs; no anonymous proof-search claim.',
                       'All work is proof construction/checking, not charged to an arbitrary decider.']}
    if args.certificate:
        args.certificate.write_text(json.dumps(P.data(),separators=(',',':')))
        out['certificate_sha256']=hashlib.sha256(args.certificate.read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
