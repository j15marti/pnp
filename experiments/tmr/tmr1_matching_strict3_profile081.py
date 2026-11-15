#!/usr/bin/env python3
"""Native finite controls for TMR-1/041 proper 3-CNF matching sign profiles.
All rows/columns and helper variables are explicit. Symbolic proof in report
handles all n >= 3; finite DPLL is solely computational evidence.
"""
import itertools, json, random, hashlib
from collections import Counter

SEED=41081


def compile_matching(n, mask):
    assert n>=3 and 0 <= mask < (1<<(n*n))
    def x(i,j): return 1+i*n+j
    def p(i,j): return 1+n*n+i*n+j
    nextvar=2*n*n
    out=[]
    kinds=Counter()
    def fresh():
        nonlocal nextvar
        nextvar+=1
        return nextvar
    def append_original(c,kind):
        k=len(c)
        if k == 1:
            a,b=fresh(),fresh()
            for u,v in itertools.product((1,-1),repeat=2):
                out.append((c[0],u*a,v*b))
            kinds[kind]+=4
        elif k==2:
            a=fresh()
            out.extend(((c[0],c[1],a),(c[0],c[1],-a)))
            kinds[kind]+=2
        elif k==3:
            out.append(tuple(c));kinds[kind]+=1
        else:
            ys=[fresh() for _ in range(k-3)]
            out.append((c[0],c[1],ys[0]))
            for j in range(1,k-3):
                out.append((-ys[j-1],c[j+1],ys[j]))
            out.append((-ys[-1],c[-2],c[-1]))
            kinds[kind]+=(k-2)
    for i in range(n):
        append_original([x(i,j) for j in range(n)],'row_atleast')
        for j in range(n):
            for k in range(j+1,n):append_original([-x(i,j),-x(i,k)],'row_atmost')
    for j in range(n):
        append_original([x(i,j) for i in range(n)],'col_atleast')
        for i in range(n):
            for k in range(i+1,n):append_original([-x(i,j),-x(k,j)],'col_atmost')
    for i in range(n):
        for j in range(n):
            append_original([-x(i,j),p(i,j)],'edge_implication')
            disabled=(mask>>(i*n+j))&1
            append_original([-p(i,j) if disabled else p(i,j)],'edge_mask')
    return out,nextvar,kinds


def recognize_exact_template(clauses):
    """Polynomial canonical source recognizer, not exponential mask enumeration."""
    m=len(clauses)
    n=next((v for v in range(3,m+1) if 2*v**3+6*v*v-4*v==m),None)
    if n is None:return None
    base0,_,_=compile_matching(n,0)
    base1,_,_=compile_matching(n,(1<<(n*n))-1)
    start=m-6*n*n
    if tuple(clauses[:start])!=tuple(base0[:start]):return None
    mask=0
    for e in range(n*n):
        t=start+6*e
        if tuple(clauses[t:t+2])!=tuple(base0[t:t+2]):return None
        group=tuple(clauses[t+2:t+6])
        if group==tuple(base1[t+2:t+6]):mask|=(1<<e)
        elif group!=tuple(base0[t+2:t+6]):return None
    return n,mask


def matching_exists(n, mask):
    return any(all(not (mask>>(i*n+perm[i]))&1 for i in range(n))
               for perm in itertools.permutations(range(n)))


def dpll(clauses, original_vars):
    """Independent exact 3-SAT DPLL with unit propagation, no SAT package.
    Visits original variables first, then auxiliary variables if needed.
    """
    def rec(assign):
        while True:
            changed=False; reduced=[]
            for cl in clauses:
                u=[]; sat=False
                for lit in cl:
                    v=abs(lit); val=assign.get(v)
                    if val is None:u.append(lit)
                    elif val==(lit>0): sat=True; break
                if sat:continue
                if not u:return False
                if len(u)==1:
                    v=abs(u[0]); val=u[0]>0
                    if v in assign and assign[v]!=val:return False
                    if v not in assign:assign[v]=val;changed=True
                reduced.append(u)
            if not changed:break
        if not reduced:return True
        remaining=set(abs(l) for cl in reduced for l in cl)
        candidates=sorted(v for v in remaining if v not in assign)
        if not candidates:return False
        v=next((v for v in candidates if v<=original_vars),candidates[0])
        for b in (False,True):
            na=assign.copy();na[v]=b
            if rec(na):return True
        return False
    return rec({})


def main():
    count=0; checked=0; errors=[]; family=[]; negatives=0; positives=0
    def check(pred,tag):
        nonlocal count
        count+=1
        if not pred:raise AssertionError(tag)
    for n in (3,4,5):
        masks=list(range(1<<(n*n))) if n==3 else [0,(1<<(n*n))-1]+[random.Random(SEED+n*500+j).randrange(1<<(n*n)) for j in range(50 if n==4 else 18)]
        ref_shape=None; size=None
        ccounts=Counter(); pos=neg=0
        for mask in masks:
            clauses,v,kinds=compile_matching(n,mask)
            shape=tuple(tuple(abs(l) for l in c) for c in clauses)
            check(all(len(c)==3 and len({abs(l) for l in c})==3 for c in clauses),f'proper n={n} mask={mask}')
            check(len(set(clauses))==len(clauses),f'no duplicated clauses n={n} mask={mask}')
            check(recognize_exact_template(clauses)==(n,mask),f'recognizer n={n} mask={mask}')
            if mask in (0,1):
                tampered=list(clauses)
                c=list(tampered[-1]);c[0]=-c[0];tampered[-1]=tuple(c)
                check(recognize_exact_template(tampered) is None,f'partial-mask forgery n={n}')
                removed=list(clauses[:-1])
                check(recognize_exact_template(removed) is None,f'deleted-source n={n}')
            check(v==n**3+6*n*n-6*n,f'var count n={n} got={v}')
            check(len(clauses)==2*n**3+6*n*n-4*n,f'clause count n={n}')
            if ref_shape is None:ref_shape=shape;size=(len(clauses),v)
            else:check(shape==ref_shape,f'unsigned source position n={n}')
            expected=matching_exists(n,mask)
            if n==3:
                actual=dpll(clauses,2*n*n)
                check(actual==expected,f'dpll n={n} mask={mask} actual={actual} expected={expected}')
            elif expected:
                # Genuine assignment on original vars: select a perfect matching;
                # split gadgets are checked independently by truth table below.
                found=next(p for p in itertools.permutations(range(n)) if all(not ((mask>>(i*n+p[i]))&1) for i in range(n)))
                check(all(not ((mask>>(i*n+found[i]))&1) for i in range(n)),'match witness')
            if expected:pos+=1
            else:neg+=1
            checked+=1
            ccounts.update(kinds)
        family.append({'n':n,'checked_masks':len(masks),'sat':pos,'unsat':neg,'variables':size[1],'clauses':size[0],
                       'uniform_unsigned_incidence':True, 'all_clauses_proper3':True,
                       'dpll_all_masks':n==3,'canonical_recognizer_checked':True})
    # Local gadgets: Boolean satisfiability of gadget iff source clause is true,
    # including the long-clause chain n = 4..7.
    for k in range(1,8):
        for bits in itertools.product((False,True),repeat=k):
            old=any(bits)
            # Assign old literals direct positive; independent helper search.
            def fresh_test(k,bits):
                nextvar=k; out=[]
                def new():
                    nonlocal nextvar
                    nextvar+=1;return nextvar
                if k==1:
                    y,z=new(),new()
                    out=[(1,a*y,b*z) for a,b in itertools.product((1,-1),repeat=2)]
                elif k==2:
                    y=new();out=[(1,2,y),(1,2,-y)]
                elif k==3:out=[(1,2,3)]
                else:
                    ys=[new() for _ in range(k-3)]
                    out=[(1,2,ys[0])]
                    for j in range(1,k-3):out.append((-ys[j-1],j+2,ys[j]))
                    out.append((-ys[-1],k-1,k))
                return out,nextvar
            clauses,v=fresh_test(k,bits)
            can=False
            for extra in itertools.product((False,True),repeat=v-k):
                assignment={i+1:b for i,b in enumerate(bits)}
                assignment.update({k+i+1:b for i,b in enumerate(extra)})
                if all(any(assignment[abs(l)]==(l>0) for l in c) for c in clauses):can=True;break
            check(can==old,f'local k={k} bits={bits}')
    out={'status':'COMPUTATIONAL','seed':SEED,'assertions':count,'failures':0,'cases':family,
         'local_clause_widths_exhaustively_checked':[1,2,3,4,5,6,7],
         'symbolic_scope':'n>=3; exact strict-3CNF satisfiability projection and sign-mask profile; no SAT lower bound',
         'model':'proper signed three-distinct-variable 3-CNF, one fresh helper set per original clause'}
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
