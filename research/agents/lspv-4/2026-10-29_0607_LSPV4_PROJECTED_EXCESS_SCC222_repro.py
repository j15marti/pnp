#!/usr/bin/env python3
"""LSPV-4 PROJECTED-EXCESS-SCC222 reproducibility audit.

Exact mixed GF(2) + 2CNF projection, rank-sensitive branching and SCC.
Standard-library only. Counts are Python-level assertions, not TM steps.
"""
import itertools
import json
import math
import random
from collections import defaultdict
from functools import reduce
from operator import xor

SEED=20261029
rng=random.Random(SEED)
counts=defaultdict(int)


def check(condition, kind):
    counts[kind]+=1
    if not condition:
        raise AssertionError(kind)


def parity(x):
    return x.bit_count() & 1


def equations_hold(equations, assignment):
    return all(parity(mask & assignment)==rhs for mask,rhs in equations)


def cnf_holds(clauses, assignment):
    return all(any(bool(assignment & (1 << (abs(lit)-1))) == (lit > 0) for lit in cl) for cl in clauses)


def rref_solution(n, equations):
    """Return a particular solution plus an independent nullspace basis; or None."""
    rows=[[mask,rhs] for mask,rhs in equations]
    pivots=[]
    r=0
    for col in range(n):
        j=next((k for k in range(r,len(rows)) if rows[k][0]>>col&1),None)
        if j is None:
            continue
        rows[r],rows[j]=rows[j],rows[r]
        for k in range(len(rows)):
            if k!=r and (rows[k][0]>>col&1):
                rows[k][0]^=rows[r][0]
                rows[k][1]^=rows[r][1]
        pivots.append(col)
        r+=1
        if r==len(rows):
            break
    if any(mask==0 and rhs==1 for mask,rhs in rows):
        return None
    pset=set(pivots)
    free=[v for v in range(n) if v not in pset]
    x0=sum(rows[j][1]<<c for j,c in enumerate(pivots))
    basis=[]
    for f in free:
        z=1<<f
        for j,p in enumerate(pivots):
            if rows[j][0]>>f&1:
                z|=1<<p
        basis.append(z)
    assert equations_hold(equations,x0)
    assert all(all(parity(mask&z)==0 for mask,_ in equations) for z in basis)
    return x0,basis


class DSU:
    def __init__(self, n):
        self.p=list(range(n)); self.s=[1]*n
    def find(self,x):
        while self.p[x]!=x:
            self.p[x]=self.p[self.p[x]]
            x=self.p[x]
        return x
    def union(self,x,y):
        x=self.find(x); y=self.find(y)
        if x!=y:
            if self.s[x]<self.s[y]: x,y=y,x
            self.p[y]=x;self.s[x]+=self.s[y]


def projected_affine_components(n, eqs, binary):
    ds=DSU(n)
    for mask,rhs in eqs:
        vars=[i for i in range(n) if mask>>i&1]
        for v in vars[1:]: ds.union(vars[0],v)
    comps=defaultdict(list)
    for i in range(n): comps[ds.find(i)].append(i)
    out=[]; idfor={}
    for ci,vars in enumerate(comps.values()):
        local={v:j for j,v in enumerate(vars)}
        sub=[]
        for mask,rhs in eqs:
            if mask and (mask>>vars[0]&1 or any(mask>>v&1 for v in vars)):
                check(all((mask>>v&1)==0 or v in local for v in range(n)),"equations_component_local")
                sub.append((sum(1<<local[v] for v in vars if mask>>v&1),rhs))
            elif mask==0:
                sub.append((0,rhs))
        answer=rref_solution(len(vars),sub)
        if answer is None: return None
        x0,basis=answer
        P=sorted({abs(lit)-1 for cl in binary for lit in cl if abs(lit)-1 in local})
        # Independent projected columns: span of all attainable port signatures.
        piv={}; selected=[]
        for j,basisvec in enumerate(basis):
            sig=sum((1<<k) for k,v in enumerate(P) if basisvec>>local[v]&1)
            v=sig
            while v:
                p=v.bit_length()-1
                if p in piv: v^=piv[p]
                else:
                    piv[p]=v;selected.append(j);break
        r=len(selected)
        component=dict(vars=vars,local=local,x0=x0,basis=basis,selected=selected,r=r,d=len(basis),P=P)
        for var in vars: idfor[var]=ci
        out.append(component)
        check(r<=len(basis),"projected_rank_le_nullity")
        # Every projected signature from an arbitrary affine solution is
        # represented by a unique choice of the selected columns.
        if len(basis)<=8 and len(P)<=8:
            signatures={sum((parity((x0^reduce(xor,(basis[j] for j in range(len(basis)) if mask>>j&1),0))>>local[v]&1))<<k for k,v in enumerate(P)) for mask in range(1<<len(basis))}
            selected_sigs={sum((parity((x0^reduce(xor,(basis[selected[j]] for j in range(r) if mask>>j&1),0))>>local[v]&1))<<k for k,v in enumerate(P)) for mask in range(1<<r)}
            check(signatures==selected_sigs,"port_image_exact")
    return out,idfor


def two_sat(n, clauses):
    # literals are signed 1-based indices; SCC assignment is witnessed.
    V=2*n
    adj=[[] for _ in range(V)]; rev=[[] for _ in range(V)]
    def node(lit): return 2*(abs(lit)-1)+(0 if lit>0 else 1)
    def edge(u,v): adj[u].append(v);rev[v].append(u)
    for clause in clauses:
        if len(clause)==0: return None
        if len(clause)==1:
            a=node(clause[0]); edge(a^1,a)
        else:
            assert len(clause)==2
            a=node(clause[0]); b=node(clause[1]); edge(a^1,b);edge(b^1,a)
    seen=[False]*V; order=[]
    for v in range(V):
        if seen[v]: continue
        seen[v]=True; stack=[(v,0)]
        while stack:
            u,j=stack[-1]
            if j==len(adj[u]):
                order.append(u);stack.pop();continue
            z=adj[u][j];stack[-1]=(u,j+1)
            if not seen[z]:seen[z]=True;stack.append((z,0))
    color=[-1]*V; c=0
    for v in reversed(order):
        if color[v]!=-1:continue
        color[v]=c;stack=[v]
        while stack:
            u=stack.pop()
            for z in rev[u]:
                if color[z]==-1:color[z]=c;stack.append(z)
        c+=1
    if any(color[2*i]==color[2*i+1] for i in range(n)): return None
    assignment=sum((color[2*i]>color[2*i+1])<<i for i in range(n))
    assert cnf_holds(clauses,assignment)
    return assignment


def mixed_solver(n,eqs,binary):
    """One uniform solver; rank discovered by paid GE, then exact SCC branches.

    Returns (witness or None, statistics).  Does not know the SAT label.
    """
    parsed=projected_affine_components(n,eqs,binary)
    if parsed is None:return None,dict(affine_inconsistent=True,branches=0)
    comps,idfor=parsed
    dc=DSU(len(comps))
    for cl in binary:
        vs=[idfor[abs(lit)-1] for lit in cl]
        for v in vs[1:]:dc.union(vs[0],v)
    groups=defaultdict(list)
    for i in range(len(comps)):groups[dc.find(i)].append(i)
    bygroup=defaultdict(list)
    for cl in binary:
        bygroup[dc.find(idfor[abs(cl[0])-1])].append(cl)
    global_port_values={};branches=0; Kvalues=[]
    for root,indices in groups.items():
        active=[i for i in indices if comps[i]['r']>0]
        assignname={i:j for j,i in enumerate(active)}
        prefix=[]
        for i in indices:
            prefix.extend((i,j) for j in range(max(0,comps[i]['r']-1)))
        Kvalues.append(len(prefix))
        succeeded=False
        for bitpattern in range(1<<len(prefix)):
            branches+=1
            chosen={(i,j):bool(bitpattern>>h&1) for h,(i,j) in enumerate(prefix)}
            child=[];invalid=False
            for cl in bygroup.get(root,[]):
                residual=[];sat=False
                for lit in cl:
                    v=abs(lit)-1;comp_id=idfor[v]; co=comps[comp_id]
                    local=co['local'][v]
                    truth=bool(co['x0']>>local&1) ^ (lit<0)
                    for j in range(max(0,co['r']-1)):
                        if (co['basis'][co['selected'][j]]>>local&1) and chosen[(comp_id,j)]:truth=not truth
                    remaining=(co['r']>0 and bool(co['basis'][co['selected'][-1]]>>local&1))
                    if not remaining:
                        if truth:sat=True;break
                        continue
                    zvar=assignname[comp_id]+1
                    residual.append(-zvar if truth else zvar)
                if sat:continue
                if not residual:invalid=True;break
                if len(residual)==2 and residual[0]==-residual[1]:continue
                if len(residual)==2 and residual[0]==residual[1]:residual=residual[:1]
                child.append(tuple(residual))
            if invalid:continue
            z=two_sat(len(active),child)
            if z is None:continue
            for i in indices:
                r=comps[i]['r']
                bits=0
                for j in range(max(r-1,0)):
                    if chosen[(i,j)]:bits|=1<<j
                if r and z>>assignname[i]&1:bits|=1<<(r-1)
                global_port_values[i]=bits
            succeeded=True;break
        if not succeeded:
            return None,dict(affine_inconsistent=False,branches=branches,projected_K=sum(Kvalues),cluster_K=Kvalues,old_K=sum(max(c['d']-1,0) for c in comps),dimensions=[(c['d'],c['r']) for c in comps],components=len(comps))
    witness=0
    for i,co in enumerate(comps):
        v=co['x0'];bits=global_port_values[i]
        for j,b in enumerate(co['selected']):
            if bits>>j&1:v^=co['basis'][b]
        for k,var in enumerate(co['vars']):
            if v>>k&1:witness|=1<<var
    check(equations_hold(eqs,witness) and cnf_holds(binary,witness),"witness_replay")
    return witness,dict(affine_inconsistent=False,branches=branches,projected_K=sum(Kvalues),cluster_K=Kvalues,old_K=sum(max(c['d']-1,0) for c in comps),dimensions=[(c['d'],c['r']) for c in comps],components=len(comps))


def dense_instance(q,h,unsat=False):
    """Connected affine components with d=h+1 and projected rank=1.
    All q port variables induce a dense complete graph of negative 2-CNF.
    """
    assert q>=2
    n=q*(2*h+1)
    def port(i):return i*(2*h+1)
    def u(i,j):return i*(2*h+1)+1+2*j
    def v(i,j):return i*(2*h+1)+2+2*j
    eq=[]
    for i in range(q):
        for j in range(h): eq.append(((1<<port(i))|(1<<u(i,j))|(1<<v(i,j)),0))
    B=[(-(port(i)+1),-(port(j)+1)) for i in range(q) for j in range(i+1,q)]
    B.append((port(0)+1,))
    B.append(((port(1)+1) if unsat else -(port(1)+1),))
    return n,eq,B


def source_bits(n,eqs,clauses):
    M=len(eqs)+len(clauses)
    w=max(1,(n+M+3).bit_length())
    out=('1'*w)+'0'+format(n,'0%db'%w)+format(M,'0%db'%w)
    for mask,rhs in eqs:
        vs=[i+1 for i in range(n) if mask>>i&1]
        assert len(vs)==3
        out+='00'+str(rhs)+''.join(format(v,'0%db'%w) for v in vs)
    for cl in clauses:
        if len(cl)==1:
            out+='10'+('1' if cl[0]<0 else '0')+format(abs(cl[0]),'0%db'%w)
        elif len(cl)==2:
            out+='01'+''.join(('1' if x<0 else '0')+format(abs(x),'0%db'%w) for x in cl)
        else:raise AssertionError
    return out


def parse_source_bits(data):
    """Independent strict parser for the typed self-delimiting source bits."""
    idx=0
    while idx<len(data) and data[idx]=='1':idx+=1
    if idx>=len(data) or data[idx]!='0' or idx==0: raise ValueError("invalid width header")
    w=idx;pos=w+1
    def read(k):
        nonlocal pos
        if pos+k>len(data):raise ValueError("truncated source")
        bits=data[pos:pos+k];pos+=k
        if any(c not in '01' for c in bits):raise ValueError("nonbinary source")
        return int(bits,2)
    n=read(w);M=read(w)
    if max(1,(n+M+3).bit_length())!=w:raise ValueError("noncanonical width")
    eq=[];B=[]
    for _ in range(M):
        tag=read(2)
        if tag==0:
            rhs=read(1);vars=[read(w) for z in range(3)]
            if any(v<1 or v>n for v in vars) or len(set(vars))!=3:raise ValueError("bad xor record")
            eq.append((sum(1<<(v-1) for v in vars),rhs))
        elif tag in (1,2):
            literals=[]
            for z in range(2 if tag==1 else 1):
                neg=read(1);var=read(w)
                if var<1 or var>n:raise ValueError("invalid variable")
                literals.append(-var if neg else var)
            B.append(tuple(literals))
        else:raise ValueError("bad tag")
    if pos!=len(data):raise ValueError("trailing data")
    return n,eq,B


def exhaustive_random_tests():
    # Completely independent brute-force labeling on small unrestricted inputs.
    labelcount={'SAT':0,'UNSAT':0}
    for n in range(1,7):
        for trial in range(110):
            eq=[]
            for _ in range(rng.randrange(0,8)):
                mask=rng.randrange(1<<n)
                rhs=rng.randrange(2)
                eq.append((mask,rhs))
            B=[]
            for _ in range(rng.randrange(0,12)):
                width=rng.choice((1,2))
                vs=rng.sample(range(n),min(width,n))
                B.append(tuple((v+1)*rng.choice((-1,1)) for v in vs))
            brute=next((x for x in range(1<<n) if equations_hold(eq,x) and cnf_holds(B,x)),None)
            witness,meta=mixed_solver(n,eq,B)
            check((brute is None)==(witness is None),"mixed_vs_bruteforce")
            if witness is not None:check(equations_hold(eq,witness) and cnf_holds(B,witness),"mixed_witness_valid")
            labelcount['SAT' if brute is not None else 'UNSAT']+=1
    return labelcount


def fano_test():
    lines=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    eq=[(sum(1<<i for i in line),1) for line in lines]
    clauses=[]
    for a,b,c in lines:clauses.extend(((-(a+1),-(b+1)),(-(a+1),-(c+1)),(-(b+1),-(c+1))))
    affine=[x for x in range(128) if equations_hold(eq,x)]
    binary=[x for x in range(128) if cnf_holds(clauses,x)]
    check(len(affine)==8 and len(binary)==8 and not set(affine).intersection(binary),"fano_separate_sat_joint_unsat")
    answer,meta=mixed_solver(7,eq,clauses)
    check(answer is None and meta['projected_K']==2 and meta['branches']==4,"fano_rank_two_branching")
    return meta


def dense_tests():
    result=[]
    for q in (3,4,5,6,7):
        h=q*q
        sizes=[];metas=[]
        for unsat in (False,True):
            n,eq,B=dense_instance(q,h,unsat)
            w,meta=mixed_solver(n,eq,B)
            check((w is None)==unsat,"dense_sat_unsat")
            check(meta['projected_K']==0 and meta['old_K']==q*h,"dense_new_K_zero_old_K_large")
            check(meta['components']==q and all(d==h+1 and r==1 for d,r in meta['dimensions']),"dense_exact_dimensions")
            src=source_bits(n,eq,B)
            check(parse_source_bits(src)==(n,eq,B),"source_bit_roundtrip")
            portclauses=tuple(tuple((1 if x>0 else -1)*(1+(abs(x)-1)//(2*h+1)) for x in cl) for cl in B)
            child=source_bits(q,[],portclauses)
            check(parse_source_bits(child)==(q,[],list(portclauses)),"child_bit_roundtrip")
            child_witness,child_meta=mixed_solver(q,[],portclauses)
            check((child_witness is None)==unsat and child_meta['projected_K']==0,"child_closed_exact_decision")
            check(len(child)<len(src),"dense_true_physical_contraction")
            check(len(child)<=len(src)**0.75,"dense_power_short_3over4")
            # every exposed port choice extends through the affine equations
            if q<=5:
                for pbits in range(1<<q):
                    full=0
                    for i in range(q):
                        if pbits>>i&1:full|=1<<(i*(2*h+1))
                        for j in range(h):
                            if pbits>>i&1:full|=1<<(i*(2*h+1)+2+2*j)
                    check(equations_hold(eq,full),"dense_all_port_values_lift")
                    check(cnf_holds(B,full)==cnf_holds(portclauses,pbits),"dense_exact_port_equivalence")
            sizes.append((len(src),len(child)));metas.append(meta)
        check(sizes[0]==sizes[1],"dense_matched_source_sizes")
        result.append(dict(q=q,h=h,components=q,affine_nullity_each=h+1,visible_rank_each=1,old_K=q*h,new_K=0,input_bits=sizes[0][0],child_bits=sizes[0][1],ratio=round(sizes[0][1]/sizes[0][0],6),source_signs_matched=True))
    return result


def internal_clause_counterexample():
    # The internal binary clauses must be included in the projected rank.
    eq=[((1<<0)|(1<<1),0)] # x=y
    B=[(1,2),(-1,-2)]
    check(rref_solution(2,eq) is not None,"internal_affine_feasible")
    check(two_sat(2,B) is not None,"internal_binary_feasible")
    witness,meta=mixed_solver(2,eq,B)
    check(witness is None and meta['projected_K']==0 and meta['dimensions'][0]==(1,1),"internal_binary_join_unsat")
    return meta


def main():
    random_labels=exhaustive_random_tests()
    fano=fano_test()
    dense=dense_tests()
    internal=internal_clause_counterexample()
    out=dict(status='PASS',research='PROJECTED-EXCESS-SCC222',seed=SEED,checks=dict(sorted(counts.items())),total_checks=sum(counts.values()),random_labels=random_labels,example_Fano=fano,example_dense=dense,example_internal=internal,limitations=["These are finite computational assertions, not TM transition counts or kernel-checked proofs.","The theorem is an upper bound for explicit affine-plus-2CNF; it does not solve unrestricted SAT.","Dense controls and the typed grammar are outside proper strict signed exact-(2,2)-3CNF.","One-child power shrinkage is guaranteed only on the declared dense redundant control."])
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__':main()
