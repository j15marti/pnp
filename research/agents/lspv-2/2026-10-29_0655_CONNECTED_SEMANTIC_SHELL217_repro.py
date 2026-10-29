#!/usr/bin/env python3
"""CONNECTED-SEMANTIC-SHELL217: rigorous finite audit of a connected
resolution-resistant SAT/UNSAT embedding and two real CNF strip levels.

No external dependencies, or oracle/truth-label shortcut. The genuine SAT
component H is retained byte-for-byte in its clause content and is decided
only by an independent exhaustive/DPLL checker for finite controls.

Run: python3 connected_embedding217.py > results.json
"""
from __future__ import annotations
from collections import Counter
from hashlib import sha256
import itertools
import json

W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
    (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
    (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
    (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]

def canon_clause(c):
    return tuple(sorted(c,key=lambda t:(abs(t),t<0)))

def canon(C):
    return tuple(sorted(canon_clause(c) for c in C))

def var(g,i,p): return g*p+(i%p)+1

def shell(p):
    assert p>=5 and p%2==1
    C=[]
    for s in range(4):
        for i in range(p):
            a,b,c=var(0,i,p),var(1,i+s,p),var(2,i+2*s,p)
            C.append(((-a if s in (0,1) else a),
                      (-b if s in (2,3) else b),
                      (-c if s in (0,2) else c)))
    return canon(C)

def core_w1(a,b):
    C=[list(c) for c in W1]
    if not a:
        for ci in (6,11): C[ci][0]=-C[ci][0]
    if not b:
        for ci in (17,9): C[ci][2]=-C[ci][2]
    return canon(C),15

def eval_cnf(C,assign):
    return all(any((assign[abs(x)] == (x>0)) for x in c) for c in C)

def count_w1_models(C):
    k=0
    for mask in range(1<<15):
        if all(any((bool(mask&(1<<(abs(x)-1)))==(x>0)) for x in c) for c in C): k+=1
    return k

def proper(C,n=None):
    if len(set(map(canon_clause,C))) != len(C):return False
    if any(len(c)!=3 or len(set(map(abs,c)))!=3 for c in C):return False
    if n is not None and any(not(1<=abs(x)<=n) for c in C for x in c):return False
    return True

def is_connected(C):
    names={abs(l) for c in C for l in c}
    if not names: return False
    adj={x:set() for x in names}
    for c in C:
        v=list(map(abs,c))
        for x in v:adj[x].update(v)
    seen={min(names)}; stack=list(seen)
    while stack:
        x=stack.pop()
        for y in adj[x]:
            if y not in seen:seen.add(y);stack.append(y)
    return seen==names

def sign_balanced(C,p):
    ct=Counter(l for c in C for l in c)
    return all(ct[i]==ct[-i]==2 for i in range(1,3*p+1))

def eq_clauses(x,y,z1,z2):
    assert len({x,y,z1,z2})==4
    return ((-x,y,z1),(-x,y,-z1),(x,-y,z2),(x,-y,-z2))

def offset_clauses(C,offset):
    return tuple(tuple((1 if l>0 else -1)*(abs(l)+offset) for l in c) for c in C)

def assemble(sizes,H,hvars):
    """Source namespace: shells first, H next, bridge pad variables last.
    Clause order: shell1, bridge1, shell2, bridge2, ..., H.
    Every H truth assignment extends to a source-shell assignment.
    """
    assert all(p%2==1 and p>=5 for p in sizes)
    assert proper(H,hvars)
    shellvars=sum(3*p for p in sizes)
    H2=offset_clauses(H,shellvars)
    y=shellvars+1
    pad_base=shellvars+hvars
    C=[];off=0
    for j,p in enumerate(sizes):
        C.extend(offset_clauses(shell(p),off))
        C.extend(eq_clauses(off+1,y,pad_base+2*j+1,pad_base+2*j+2))
        off+=3*p
    C.extend(H2)
    N=shellvars+hvars+2*len(sizes)
    assert proper(C,N) and is_connected(C)
    assert {abs(l) for c in C for l in c}==set(range(1,N+1))
    return tuple(C),N

def dimacs(C,n):
    return ('p cnf %d %d\n'%(n,len(C))+''.join(' '.join(map(str,c))+' 0\n' for c in C)).encode('ascii')

def parse_dimacs(data):
    """Strictly parse ordinary canonical DIMACS, including physical bytes.
    Return None on malformed encoding. Does not decide SAT.
    """
    try:
        s=data.decode('ascii',errors='strict')
        if not s.endswith('\n'):return None
        lines=s.splitlines()
        if not lines or len(lines[0].split())!=4:return None
        hd=lines[0].split()
        if hd[:2]!=['p','cnf']:return None
        n,m=int(hd[2]),int(hd[3])
        if n<=0 or m<=0 or len(lines)!=m+1:return None
        if lines[0]!='p cnf %d %d'%(n,m):return None
        C=[];allids=set();seen=set()
        for line in lines[1:]:
            words=line.split()
            if len(words)!=4 or words[-1]!='0':return None
            c=tuple(map(int,words[:3]))
            if ' '.join(map(str,c))+' 0'!=line:return None
            if len({abs(z) for z in c})!=3 or 0 in c:return None
            if any(abs(z)>n for z in c):return None
            allids.update(map(abs,c))
            key=canon_clause(c)
            if key in seen:return None
            seen.add(key);C.append(c)
        if allids!=set(range(1,n+1)):return None
        return tuple(C),n
    except (ValueError,UnicodeError,OverflowError):return None

def orbit_match(segment,p):
    """Recognize the full variable-complement orbit, regardless of clause order.

    Exact support indices are authenticated, and each signed variable must
    have the same flip at every occurrence. This reads all clauses and stores
    O(p log p) bits of scope/flip data; no free source lookup table is assumed.
    """
    R=shell(p)
    if len(segment)!=len(R):return None
    def byscope(C):
        out={}
        for c in C:
            ids=tuple(sorted(abs(t) for t in c))
            if ids in out:return None
            out[ids]=tuple(sorted(c,key=lambda t:abs(t)))
        return out
    actual=byscope(segment); original=byscope(R)
    if actual is None or set(actual)!=set(original):return None
    flip={}
    for ids in original:
        for l,q in zip(actual[ids],original[ids]):
            v=abs(l)
            f=int(l!=q)
            if v in flip and flip[v]!=f:return None
            flip[v]=f
    return flip if len(flip)==3*p else None

def next_shell_candidate(C):
    """Find sound self-authenticated leading shell and isolation conditions.
    Trials are fully charged. Any match can be stripped without querying SAT.
    """
    m=len(C);trials=0
    # The first clause of an unflipped canonical block identifies p directly.
    # This is merely a candidate hint, verified below; it may be wrong after
    # arbitrary complements, so the exhaustive source-authenticated fallback
    # remains complete and is charged.
    guess=abs(C[0][0])
    candidate_list=([guess] if guess>=5 and guess%2 and guess<=m//4 else [])
    candidate_list.extend(p for p in range(5,m//4+1,2) if p!=guess)
    for p in candidate_list:
        trials+=1
        j=4*p
        if j+4>=m:continue
        flips=orbit_match(C[:j],p)
        if flips is None:continue
        A,B,C1,D=C[j:j+4]
        # Require exact physical bridge convention, even under shell flips.
        if (len(A),len(B),len(C1),len(D))!=(3,3,3,3):continue
        x=1
        if A[0]!=-x or B[0]!=-x or C1[0]!=x or D[0]!=x:continue
        y=A[1]
        if y<=3*p or B[1]!=y or C1[1]!=-y or D[1]!=-y:continue
        z1=A[2];z2=C1[2]
        if min(z1,z2)<=3*p or z1==z2:continue
        if B[2]!=-z1 or D[2]!=-z2:continue
        rest=C[j+4:]
        if any(abs(l)<=3*p or abs(l) in (z1,z2) for c in rest for l in c):continue
        if y not in {abs(l) for c in rest for l in c}:continue
        # Source shell may be complemented at any names. Both x=0 and x=1
        # remain feasible because original all-0 and all-1 satisfy it.
        return {'p':p,'trials':trials,'flips':sum(flips.values()),'y':y,
                'z1':z1,'z2':z2,'prefix':j+4}
    return {'p':None,'trials':trials}

def strip_one(data):
    parsed=parse_dimacs(data)
    if parsed is None:return {'status':'MALFORMED','trials':0,'child':None}
    C,n=parsed
    meta=next_shell_candidate(C)
    p=meta['p']
    if p is None:return {'status':'NO_SHELL','trials':meta['trials'],'child':None}
    rest=C[meta['prefix']:]
    # Explicitly relabel all surviving names, charge the emitted entire body.
    surviving=sorted({abs(z) for c in rest for z in c})
    lookup={z:i+1 for i,z in enumerate(surviving)}
    child=tuple(tuple((1 if z>0 else -1)*lookup[abs(z)] for z in c) for c in rest)
    out=dimacs(child,len(surviving))
    assert parse_dimacs(out) is not None
    return {'status':'STRIPPED','trials':meta['trials'], 'child':out,
            'source_bytes':len(data),'child_bytes':len(out),
            'source_clauses':len(C),'child_clauses':len(child),
            'source_variables':n,'child_variables':len(surviving),
            'flipped_shell_vars':meta['flips'],
            'bits_read_upper_proxy':8*len(data)*meta['trials'],
            'bytes_written':len(out),
            'peak_writable_bytes_upper_proxy':len(data)+len(out)+32*len(C)}

def eliminate(C,pivot):
    P=[c for c in C if pivot in c]
    M=[c for c in C if -pivot in c]
    rest=[c for c in C if pivot not in c and -pivot not in c]
    R=[];taut=0
    for a in P:
        for b in M:
            S=(set(a)-{pivot}) | (set(b)-{-pivot})
            if any(-l in S for l in S):taut+=1;continue
            R.append(canon_clause(S))
    return tuple(rest),tuple(R),len(P),len(M),taut

def factor4(R):
    if len(R)!=4 or len(set(map(frozenset,R)))!=4 or any(len(c)!=4 for c in R):return None
    sets=list(map(set,R));best=None
    for ids in itertools.permutations(range(4)):
        a,b,c,d=[sets[z] for z in ids]
        fs=(a&b,c&d,a&c,b&d)
        if any(len(s)!=2 for s in fs):continue
        if len(set.union(*fs))!=8:continue
        pro={frozenset(x|y) for x in fs[:2] for y in fs[2:]}
        if pro!={frozenset(s) for s in sets}:continue
        packed=tuple(canon_clause(s) for s in fs)
        if best is None or packed<best:best=packed
    return best

def local_reentry(C,pivot,section_length):
    # Pivot belongs exclusively to the first shell, not its connector x=1.
    prefix=C[:section_length]
    rest,R,np,nm,taut=eliminate(prefix,pivot)
    assert (np,nm,taut,len(R))==(2,2,0,4)
    assert all(len(r)==4 for r in R)
    feet=factor4(R)
    assert feet is not None
    A,B,U,V=feet
    new=canon(tuple(rest)+((pivot,)+A,(pivot,)+B,(-pivot,)+U,(-pivot,)+V))
    assert len(new)==len(prefix)
    return new+tuple(C[section_length:])

def dpll(C,prefer=()):
    stats={'calls':0,'unit_iterations':0,'peak_unassigned':0}
    pref=list(prefer)
    def recurse(A):
        stats['calls']+=1
        while True:
            reduced=[];units=[];vset=set()
            for c in C:
                values=[];ok=False
                for l in c:
                    v=abs(l)
                    if v in A:
                        if A[v]==(l>0):ok=True;break
                    else:values.append(l);vset.add(v)
                if ok:continue
                if not values:return None
                reduced.append(values)
                if len(values)==1:units.append(values[0])
            stats['peak_unassigned']=max(stats['peak_unassigned'],len(vset))
            if not reduced:return dict(A)
            if not units:break
            stats['unit_iterations']+=1
            changed=False
            for lit in units:
                v=abs(lit);bit=lit>0
                if v in A:
                    if A[v]!=bit:return None
                else:A[v]=bit;changed=True
            if not changed:break
        source_vars={abs(l) for c in reduced for l in c}
        v=next((v for v in pref if v in source_vars),min(source_vars))
        for bit in (False,True):
            B=dict(A);B[v]=bit
            ans=recurse(B)
            if ans is not None:return ans
        return None
    sat=recurse({})
    return sat,stats

def graph_coloring_core(q,unsat=False):
    """Connected proper 3-CNF encoding of a graph 3-coloring instance.
    SAT graph: path. UNSAT graph: K4 followed by path from vertex 4.
    No truth labels are provided to the solver.
    """
    assert q>=4
    edges={(i,i+1) for i in range(1,q)}
    if unsat:
        for i in range(1,5):
            for j in range(i+1,5):edges.add((i,j))
    edges=sorted(edges)
    color=lambda v,k:3*(v-1)+k
    C=[];pad=3*q
    for v in range(1,q+1):
        C.append((color(v,1),color(v,2),color(v,3)))
        for a,b in ((1,2),(1,3),(2,3)):
            pad+=1;A=-color(v,a);B=-color(v,b)
            C.extend(((A,B,pad),(A,B,-pad)))
    for u,v in edges:
        for c in (1,2,3):
            pad+=1;A=-color(u,c);B=-color(v,c)
            C.extend(((A,B,pad),(A,B,-pad)))
    assert proper(C,pad) and is_connected(C)
    return tuple(C),pad

def checked_probe(C,shell_p,Hn,assignment):
    # Direct lift of an arbitrary H assignment into source formula.
    a={}
    v=assignment[1]
    for k in range(1,3*shell_p+1):a[k]=v
    for k in range(1,Hn+1):a[3*shell_p+k]=assignment[k]
    a[3*shell_p+Hn+1]=False;a[3*shell_p+Hn+2]=False
    return eval_cnf(C,a)

def source_syntax_tests():
    out=[]
    for p in (5,7,9,31,101):
        S=shell(p)
        assert len(S)==4*p and proper(S,3*p)
        assert is_connected(S) and sign_balanced(S,p)
        assert all(len(set(map(abs,a))&set(map(abs,b)))<=1
                   for i,a in enumerate(S) for b in S[i+1:])
        assert eval_cnf(S,{v:False for v in range(1,3*p+1)})
        assert eval_cnf(S,{v:True for v in range(1,3*p+1)})
        for v in range(1,3*p+1):
            rest,R,np,nm,t=eliminate(S,v)
            assert (np,nm,t,len(R))==(2,2,0,4)
            assert len(set(R))==4 and all(len(x)==4 for x in R)
            assert factor4(R) is not None
            assert all(not set(c).issubset(r) for c in rest for r in R)
        out.append({'p':p,'vars':3*p,'clauses':4*p,'no_short_pivots':3*p,
                    'two_opposite_uniform_models':True})
    return out

def test():
    source=source_syntax_tests()
    w_modes=[]
    for a,b in itertools.product((0,1),repeat=2):
        H,h=core_w1(a,b)
        assert proper(H,h) and is_connected(H)
        models=count_w1_models(H)
        w_modes.append({'switch':str(a)+str(b),'models':models,'sat':models>0})
    assert dict((x['switch'],x['models']) for x in w_modes)=={'00':772,'01':272,'10':272,'11':0}
    runs=[];summary={'dpll_calls':0,'semantic_assignment_tests':0,'local_reentry_checks':0}
    for mode in ((0,0),(1,1)):
        H,h=core_w1(*mode)
        Hsat=count_w1_models(H)>0
        for sizes in ((5,),(7,),(5,7),(7,5),(31,7)):
            F,n=assemble(sizes,H,h)
            inbits=dimacs(F,n)
            assert parse_dimacs(inbits)==(F,n)
            res1=strip_one(inbits)
            assert res1['status']=='STRIPPED'
            first,_=parse_dimacs(res1['child'])
            if len(sizes)>1:
                res2=strip_one(res1['child'])
                assert res2['status']=='STRIPPED'
                final=res2['child']
            else:
                res2=None;final=res1['child']
            assert final==dimacs(H,h)
            last=strip_one(final)
            assert last['status']=='NO_SHELL'
            # Both SAT and UNSAT finite controls independently decided by DPLL.
            core_prefer=range(sum(3*p for p in sizes)+1,
                              sum(3*p for p in sizes)+h+1)
            sol,stats=dpll(F,core_prefer)
            summary['dpll_calls']+=stats['calls']
            assert (sol is not None)==Hsat
            if sol is not None:assert eval_cnf(F,sol)
            # For each assignment on H, the explicit x0=H[1] lift exists.
            if sizes==(5,):
                for mask in range(1<<h):
                    A={i+1:bool(mask & (1<<i)) for i in range(h)}
                    assert checked_probe(F,5,h,A)==eval_cnf(H,A)
                    summary['semantic_assignment_tests']+=1
            # Try the actual source-free 2x2 elimination/factor/reentry twice,
            # on two independently chosen untouched affine-shell variables.
            if sizes[0] in (5,7) and len(sizes)>1:
                C=F
                for pivot in (2,3):
                    C=local_reentry(C,pivot,4*sizes[0])
                    assert orbit_match(C[:4*sizes[0]],sizes[0]) is not None
                    assert len(dimacs(C,n))==len(inbits)
                    summary['local_reentry_checks']+=1
                # Authenticated global removal survives these local rewrites.
                after=strip_one(dimacs(C,n))
                assert after['status']=='STRIPPED'
                assert after['child']==res1['child']
            runs.append({'mode':''.join(map(str,mode)),'p_shells':list(sizes),
                         'sat':Hsat,'parent_bytes':len(inbits),
                         'first_child_bytes':res1['child_bytes'],
                         'second_child_bytes':res2['child_bytes'] if res2 else None,
                         'final_core_bytes':len(final),
                         'first_ratio':round(res1['child_bytes']/len(inbits),8),
                         'first_discovery_trials':res1['trials'],
                         'second_discovery_trials':res2['trials'] if res2 else None,
                         'dpll':stats,
                         'first_peak_proxy':res1['peak_writable_bytes_upper_proxy']})
    graph_small=[]
    for q in (4,5):
        for unsat in (False,True):
            H,h=graph_coloring_core(q,unsat)
            F,n=assemble((5,),H,h)
            ans,stats=dpll(F,range(3*5+1,3*5+h+1))
            assert (ans is None)==unsat
            child=strip_one(dimacs(F,n))
            assert child['status']=='STRIPPED' and child['child']==dimacs(H,h)
            graph_small.append({'vertices':q,'K4_unsat':unsat,'H_vars':h,
                                'H_clauses':len(H),'dpll_nodes':stats['calls']})
    dominance=[]
    # Core dominates physical bytes even though the shell is fully eliminated.
    for q in (12,40,160,640):
        for unsat in (False,True):
            H,h=graph_coloring_core(q,unsat)
            F,n=assemble((5,),H,h)
            encoded=dimacs(F,n)
            res=strip_one(encoded)
            assert res['status']=='STRIPPED'
            assert res['child']==dimacs(H,h)
            ratio=len(res['child'])/len(encoded)
            dominance.append({'graph_vertices':q,'unsat_core':unsat,
                              'parent_bytes':len(encoded),'child_bytes':len(res['child']),
                              'ratio':round(ratio,8),
                              'lambda_3_4_fails':len(res['child'])>len(encoded)**.75})
    # Two genuine polynomial-power steps for a deliberately shell-dominated
    # authenticated subclass. The base W1 problem is fixed-size; this is not
    # an all-SAT shrinker, but all ordinary 3CNF physical bytes are counted.
    graded=[]
    for mode in ((0,0),(1,1)):
        H,h=core_w1(*mode)
        for sizes in ((501,), (5001,101)):
            F,n=assemble(sizes,H,h)
            src=dimacs(F,n)
            cur=src
            stages=[]
            for depth,_ in enumerate(sizes):
                step=strip_one(cur)
                assert step['status']=='STRIPPED'
                success=(len(step['child'])<=len(cur)**.75)
                assert success
                stages.append({'depth':depth+1,'parent_bytes':len(cur),
                               'child_bytes':len(step['child']),
                               'lambda_3_4_satisfied':success,
                               'discovery_trials':step['trials']})
                cur=step['child']
            assert cur==dimacs(H,h)
            graded.append({'mode':''.join(map(str,mode)),'shell_sizes':list(sizes),
                           'stages':stages})
    # An unbounded restricted closed class with actual one-child N^(3/4)
    # power-shortening at BOTH recursive levels for sufficiently large t:
    # p1=2*t**4+1, p2=2*t**2+1, and constant-size W1 as direct base.
    # These finite values are witnesses, not a proof of the asymptotic claim.
    graded_family=[]
    for t in (5,6,7):
        sizes=(2*t**4+1,2*t**2+1)
        H,h=core_w1(0,0)
        F,n=assemble(sizes,H,h)
        data=dimacs(F,n)
        first=strip_one(data)
        second=strip_one(first['child'])
        assert first['status']==second['status']=='STRIPPED'
        assert second['child']==dimacs(H,h)
        assert len(first['child'])<=len(data)**.75
        assert len(second['child'])<=len(first['child'])**.75
        graded_family.append({'t':t,'p1':sizes[0],'p2':sizes[1],
            'levels':[len(data),len(first['child']),len(second['child'])],
            'discovery_trials':[first['trials'],second['trials']],
            'lambda_3_4_both_levels':True})
    # Hostile control: a merely satisfiable shell cannot be stripped through
    # equality if it forces the connector bit. Here x=0 and y=1 are forced.
    p=5; R=list(shell(p))
    u,v=3*p+1,3*p+2
    force_x0=[(-1,a,b) for a,b in ((u,v),(u,-v),(-u,v),(-u,-v))]
    y=3*p+3;aa,bb=3*p+4,3*p+5
    force_y1=[(y,a,b) for a,b in ((aa,bb),(aa,-bb),(-aa,bb),(-aa,-bb))]
    eq=eq_clauses(1,y,3*p+6,3*p+7)
    misleading=tuple(R+force_x0+force_y1+list(eq))
    assert proper(misleading) and is_connected(misleading)
    fail,ref=dpll(misleading)
    assert fail is None
    assert dpll(force_y1)[0] is not None
    negative_connectivity={'rigid_shell_equivalence_fails':True,
             'h_alone_sat':True,'joined_unsat':True,
             'dpll_calls':ref['calls']}
    # Specific random misleading input: syntax of shell recognized but connector
    # isolation broken, so the unsafe local rewrite must not be applied.
    H,h=core_w1(0,0)
    F,n=assemble((5,),H,h)
    attacked=list(F)
    # Replace a core clause literal by an otherwise forbidden shell variable.
    c=list(attacked[-1]);c[0]=2;attacked[-1]=tuple(c)
    if proper(attacked,n):
        assert strip_one(dimacs(tuple(attacked),n))['status']=='NO_SHELL'
    malformed=[]
    good=dimacs(F,n)
    for label,bad in [('truncated',good[:-1]),('bad_header',b'x'+good[1:]),
                       ('out_of_range',good.replace(b' 0\n',b' 999999\n',1)),
                       ('bad_clause_width',good.replace(b' 0\n',b'\n',1))]:
        assert strip_one(bad)['status']=='MALFORMED'
        malformed.append(label)
    return {'status':'COMPUTATIONAL finite verification plus separate symbolic theorem',
            'source_shell_properties':source,'w1_modes':w_modes,
            'full_two_level_runs':runs,'small_3color_controls':graph_small,
            'core_dominance_controls':dominance,'graded_two_level_shrink':graded,
            'asymptotic_family_finite_controls':graded_family,
            'negative_connectivity_control':negative_connectivity,'malformed_controls':malformed,
            'summary':summary,
            'limitations':['H itself is retained, not solved or compressed',
                           'One shell stripping is an authenticated promise transformation',
                           'Resolution pivot no-short property only for shell variables other than connector',
                           'Reported operation proxies are not native TM step counts',
                           'No complete all-input single-child power-contraction or P vs NP proof']}

if __name__=='__main__':
    out=test()
    print(json.dumps(out,indent=2,sort_keys=True))
