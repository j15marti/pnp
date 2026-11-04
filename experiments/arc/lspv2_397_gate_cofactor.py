#!/usr/bin/env python3
"""LSPV2/397: two-cofactor removal for one binary conservatively defined gate.
Standalone no dependencies; raw certificate checks; Python >= 3.10.
All source clause IDs are preserved. Not an Rmix341 general-purpose checker.
"""
import itertools, json, hashlib, sys, time
from dataclasses import dataclass

def canon(c): return tuple(sorted(set(c),key=lambda a:(abs(a),a)))
def taut(c): return any(-a in c for a in c)
def res(a,b,p):
    assert p in a and -p in b
    return canon([v for v in a if v!=p]+[v for v in b if v!=-p])

def mapped(c, sigma):
    v=[]
    for lit in c:
        x=abs(lit)
        img=sigma.get(x,x)
        if isinstance(img,bool):
            assert isinstance(img,bool)
            if (img if lit>0 else not img):return None
            continue
        v.append((1 if lit>0 else -1)*img)
    out=canon(v)
    return None if taut(out) else out

def checker(sources,steps):
    lines=[c for c in sources]
    assert all(not taut(c) for c in lines)
    for a,b,p,c in steps:
        assert 0<=a<len(lines) and 0<=b<len(lines)
        assert res(lines[a],lines[b],p)==c and not taut(c)
        lines.append(c)
    assert lines[-1]==(),"not refuted"
    return len(steps)

def subst_proof(sources,steps,sigma,require_unsat=True):
    """Replay strict shared DAG under signed-literal/constant substitution."""
    newsrc=[]; link=[]; transformed=[]; transforms=[]; old=list(sources)
    for c in old:
        d=mapped(c,sigma)
        if d is None:link.append(None)
        else:
            link.append(len(newsrc));newsrc.append(d)
    derived=0
    for a,b,p,c in steps:
        target=mapped(c,sigma); old.append(c)
        if target is None:link.append(None);continue
        x=link[a];y=link[b]; chosen=None
        for id_ in [x,y]:
            if id_ is not None and set((newsrc+transformed)[id_]).issubset(target):
                chosen=id_;break
        if chosen is not None:link.append(chosen);continue
        if x is None or y is None:raise AssertionError('tautological parent but active target')
        cl=newsrc+transformed; left=cl[x];right=cl[y]
        piv=mapped((p,),sigma)
        if piv is None or len(piv)!=1:raise AssertionError('constant pivot with active target')
        s=piv[0]
        if s not in left or -s not in right:raise AssertionError('lost pivot but not subsumed')
        r=res(left,right,s)
        if taut(r) or not set(r).issubset(target):raise AssertionError('invalid substituted resolution')
        link.append(len(cl));transformed.append(r);transforms.append((x,y,s,r));derived+=1
    last=link[-1]
    if require_unsat: assert last is not None and (newsrc+transformed)[last]==()
    return {'sources':newsrc,'steps':transformed,'rows':transforms,'terminal':link[-1],'cost':derived,'old_cost':len(steps)}

def lift_and_combine(B, sections, alpha):
    """Lift 0/1 cofactor refutations back to B; source-only strict Resolution."""
    lines=list(B); out=[]; branch_tails=[]
    for val,sec in zip((False,True),sections):
        guard=alpha if not val else -alpha
        sub_sources=[mapped(c,{alpha:val}) for c in B]
        origins=[i for i,c in enumerate(sub_sources) if c is not None]
        assert sec['sources']==[c for c in sub_sources if c is not None]
        link={i:orig for i,orig in enumerate(origins)}
        curr=list(sec['sources'])
        for j,(a,b,p,r) in enumerate(sec['rows']):
            target=set(r)|{guard}
            A=lines[link[a]];D=lines[link[b]]
            if set(A).issubset(target): chosen=link[a]
            elif set(D).issubset(target): chosen=link[b]
            else:
                assert p in A and -p in D and abs(p)!=alpha
                C=res(A,D,p)
                assert not taut(C) and set(C).issubset(target)
                chosen=len(lines);out.append((link[a],link[b],p,C));lines.append(C)
            link[len(sec['sources'])+j]=chosen
        branch_tails.append(link[sec['terminal']])
        assert set(lines[branch_tails[-1]]).issubset({guard})
    p0,p1=branch_tails
    if lines[p0]==() or lines[p1]==():assert lines[p0]==() or lines[p1]==()
    else:
        assert lines[p0]==(alpha,) and lines[p1]==(-alpha,)
        out.append((p0,p1,alpha,()))
    checker(B,out)
    return {'cost':len(out),'steps':out,'sources':B,'branch_tails':branch_tails}

def gate_eliminate(sources,steps,a,b,y):
    assert y>0 and abs(a)!=abs(b) and y not in (abs(a),abs(b))
    assert tuple(sources[-3:])==(canon((-y,a)),canon((-y,b)),canon((y,-a,-b)))
    B=sources[:-3]
    proofs=[]
    for val in (False,True):
        aa=abs(a)
        first_true=(val if a>0 else not val)
        replacement=False if not first_true else b
        sigma={aa:val,y:replacement}
        out=subst_proof(sources,steps,sigma)
        base=[mapped(c,{aa:val}) for c in B]
        base=[c for c in base if c is not None]
        assert out['sources']==base,('sources diverge',out['sources'],base)
        proofs.append(out)
    lift=lift_and_combine(B,proofs,abs(a))
    return {'restricted':proofs,'lifted':lift,'bound':2*(len(steps)+1)-1}

def main():
    x,w,y=1,2,3
    src=[canon((x,)),canon((w,)),canon((-x,-w)),canon((-y,x)),canon((-y,w)),canon((y,-x,-w))]
    steps=[]
    steps.append((5,0,-x,res(src[5],src[0],-x)))
    steps.append((6,1,-w,res(steps[0][3],src[1],-w)))
    steps.append((3,2,x,res(src[3],src[2],x)))
    steps.append((4,8,w,res(src[4],steps[2][3],w)))
    steps.append((7,9,y,res(steps[1][3],steps[3][3],y)))
    q=checker(src,steps)
    e=gate_eliminate(src,steps,x,w,y)
    for sec in e['restricted']:
        assert sec['steps'][-1]==() if sec['steps'] else () in sec['sources']
        assert sec['cost']<=q
    z,w2=5,4
    src2=src+[canon((-z,y)),canon((-z,w2)),canon((z,-y,-w2))]
    shift=3
    st2=[(a+shift if a>=len(src) else a, b+shift if b>=len(src) else b,p,c) for a,b,p,c in steps]
    assert checker(src2,st2)==5
    first=gate_eliminate(src2,st2,y,w2,z)
    second=gate_eliminate(first['lifted']['sources'],first['lifted']['steps'],x,w,y)
    assert second['lifted']['cost']<=4*(len(st2)+1)-1
    assert second['lifted']['steps'][-1][3]==()
    sgate=[canon((-6,-1)),canon((-6,2)),canon((6,1,-2))]
    for va,vb in itertools.product((False,True),repeat=2):
        target=(not va) and vb
        assert all(any(((va if abs(l)==1 else vb if abs(l)==2 else target) if l>0 else not (va if abs(l)==1 else vb if abs(l)==2 else target)) for l in C) for C in sgate)
    ncase=0
    vars_=(1,2,3)
    clauses=[canon(c) for bits in itertools.product((-1,0,1),repeat=3) for c in [tuple((i+1)*bits[i] for i in range(3) if bits[i]!=0)] if not taut(c)]
    signatures=[None,False,True]+[i for i in vars_]+[-i for i in vars_]
    for A in clauses:
        for B in clauses:
            for p in vars_:
                if p not in A or -p not in B:continue
                C=res(A,B,p)
                if taut(C):continue
                for target in signatures:
                    if target is None:continue
                    for v in vars_:
                        sig={v:target}
                        ss=[A,B];rr=[(0,1,p,C)]
                        out=subst_proof(ss,rr,sig,require_unsat=False)
                        ncase+=1
                        assert out['cost']<=1
    summary={'model':'strict shared-DAG resolution, unit paid inference; complete signed 2-input AND gate bank as extra source','sample_original_sources':[list(c) for c in src],'sample_original_steps':[[a,b,p,list(c)] for a,b,p,c in steps],'sample_cost':q,'sample_section_costs':[s['cost'] for s in e['restricted']],'sample_section_source_counts':[len(s['sources']) for s in e['restricted']],'sample_lifted_cost':e['lifted']['cost'],'two_gate_nested_lifted_cost':second['lifted']['cost'],'two_gate_budget':4*(len(st2)+1)-1,'sample_lifted_strict_resolution_steps':[[a,b,p,list(c)] for a,b,p,c in e['lifted']['steps']],'general_fanin2_bound':'W_res(F) <= 2^g (r+1)-1 for any r-resolution derivation from F plus g complete acyclic binary functional definition banks','local_literal_substitution_cases':ncase,'synthetic_proof_checked':True,'bounded_experiments_are_not_global_minima':True}
    print(json.dumps(summary,indent=2));return summary
if __name__=='__main__':main()
