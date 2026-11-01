#!/usr/bin/env python3
"""Independent, no-producer-import verifier of ARC-MONOTONE-THREE-CORE286.
Enumerates all monotone 1..3-clause subsets on four variables,
all Y6 partial assignments, and authenticates both U198/V198 labels.
Run arc_three_core286.py first to create three_core286_full_raw.json.
"""
import ast,collections,hashlib,itertools,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
S='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
assertions=0;checks=collections.Counter()
def chk(cond):
    global assertions
    assertions+=1
    if not cond:raise AssertionError(f'independent check {assertions}')
def inp():
    source=ROOT/'DOECKER61_original_source.txt'
    if not source.exists():
        source=ROOT.parents[2]/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt'
    s=source.read_text()
    return tuple(tuple(x) for x in ast.literal_eval(s[s.index('[['):]))
def valid(formula,n):
    tally=collections.Counter();seen=set()
    if len(formula)*3 != 4*n or n%3:return False
    for clause in formula:
        if len(clause)!=3 or len({abs(z) for z in clause})!=3:return False
        if any(abs(z)<1 or abs(z)>n for z in clause):return False
        if not (all(z>0 for z in clause) or all(z<0 for z in clause)):return False
        key=tuple(sorted(clause))
        if key in seen:return False
        seen.add(key)
        tally.update((abs(z),z>0) for z in clause)
    return all(tally[(i,p)]==2 for i in range(1,n+1) for p in (False,True))
def is_sat(formula):
    vs=sorted({abs(z) for clause in formula for z in clause})
    for a in itertools.product((False,True),repeat=len(vs)):
        state=dict(zip(vs,a))
        checks['ground_truth_rows']+=1
        if all(any(state[abs(z)] == (z>0) for z in clause) for clause in formula):return True
    return False
def predicted_bad(clauses):
    if any(not c for c in clauses):return True
    literals=[c[0] for c in clauses if len(c)==1]
    if any(-l in literals for l in literals):return True
    if len(clauses)!=3:return False
    for cl in clauses:
        if len(cl)==2:
            x,y=cl
            if x!=y and (-x in literals) and (-y in literals):return True
    return False
def cube_restrict(clause,a):
    if any(a[abs(l)-1] is not None and a[abs(l)-1]==(l>0) for l in clause):return None
    return tuple(l for l in clause if a[abs(l)-1] is None)
def y6_audit(raw):
    distr=collections.Counter();sample=None
    chk(valid(Y,6))
    for rho in itertools.product((None,False,True),repeat=6):
        resid=tuple((j,z) for j,c in enumerate(Y) if (z:=cube_restrict(c,rho)) is not None)
        # Independent exact full-completion oracle, only 64 assignments per rho.
        expandable=False
        for b in itertools.product((False,True),repeat=6):
            if all(rho[i] is None or rho[i]==b[i] for i in range(6)) and all(any(b[abs(z)-1]==(z>0) for z in c) for c in Y):expandable=True;break
        if expandable:distr['extendible']+=1;continue
        distr['nonextendible']+=1
        for sz in (1,2,3):
            found=None
            for choice in itertools.combinations(resid,sz):
                checks['Y6_subsets_checked']+=1
                cls=[c for _,c in choice]
                if not is_sat(cls):
                    chk(predicted_bad(cls))
                    found=choice
                    break
            if found:
                distr['core_'+('empty' if sz==1 else 'pair' if sz==2 else 'triple')]+=1
                if sz==3:
                    chk(all(is_sat([c for _,c in pair]) for pair in itertools.combinations(found,2)))
                    if sample is None:sample={'rho':[(-1 if x is None else int(x)) for x in rho], 'indices_0':[j for j,_ in found], 'clauses':[list(c) for _,c in found]}
                break
        else:chk(False)
    chk(distr==raw['Y6']['counts'])
    exp=raw['Y6']['three_core_example']
    chk(exp['rho']==[-1,0,1,0,0,-1])
    chk(exp['original_clause_indices_0']==[1,2,5])
    chk(exp['residual_clauses']==[[1],[6],[-1,-6]])
    chk(all(not (not any(int(b[abs(z)-1])==(z>0) for z in (2,4,5,-3)) and all(any(b[abs(l)-1]==(l>0) for l in c) for c in Y)) for b in itertools.product((False,True),repeat=6)))
    chk(sum(all(any(b[abs(z)-1]==(z>0) for z in c) for c in Y) for b in itertools.product((False,True),repeat=6))==20)
    return dict(distr),sample
def certificate_u198(U):
    # UNSAT proof: 2 boundary clauses, then six 42-clause modules.
    chk(len(U)==264)
    modules=[]
    for i in range(6):
        local=set(range(1+32*i,33+32*i))
        M=[c for c in U[2:254] if any(abs(z) in local for z in c)]
        chk(len(M)==42)
        chk(all(all(abs(z) in local or abs(z)>=193 for z in c) for c in M))
        modules.append(M)
    # Distinct original clause slots from each module are disjoint and cover 252.
    chk(sum(len(M) for M in modules)==252)
    visited=0;halted=0;nodes=0
    def dpll(clauses):
        nonlocal nodes
        nodes+=1
        while True:
            if not clauses:return True
            if any(not c for c in clauses):return False
            singleton=next((c[0] for c in clauses if len(c)==1),None)
            if singleton is None:break
            clauses=tuple(tuple(z for z in c if z!=-singleton) for c in clauses if singleton not in c)
        p=clauses[0][0]
        for lit in (p,-p):
            child=tuple(tuple(z for z in c if z!=-lit) for c in clauses if lit not in c)
            if dpll(child):return True
        return False
    for bits in itertools.product((False,True),repeat=6):
        boundary={193+i:bits[i] for i in range(6)}
        if any(all(boundary[abs(z)]!=(z>0) for z in c) for c in U[:2]):
            visited+=1;halted+=1;continue
        for M in modules:
            G=[]
            for c in M:
                if any(abs(z)>=193 and boundary[abs(z)]==(z>0) for z in c):continue
                G.append(tuple(z for z in c if abs(z)<=192))
            checks['U198_module_dpll_calls']+=1
            if not dpll(tuple(G)):
                visited+=1
                break
    # Properly count only searched rows: each uncovered row must have a failing module.
    chk(visited==64 and halted==16)
    return {'covered':visited,'boundary_direct':halted,'module_calls':checks['U198_module_dpll_calls'],'dpll_nodes':nodes}
def main():
    all_cl=[]
    for k in (1,2,3,4):
        for support in itertools.combinations(range(1,5),k):
            for polarity in (1,-1):all_cl.append(tuple(polarity*v for v in support))
    chk(len(all_cl)==30)
    count=0;types=collections.Counter()
    for k in (1,2,3):
        for clauses in itertools.combinations(all_cl,k):
            res=not is_sat(clauses);pred=predicted_bad(clauses)
            chk(res==pred)
            types[('UNSAT' if res else 'SAT',k)]+=1
            count+=1
    # Explicit empty clause is the only 1-clause UNSAT core; empty is absent above.
    chk(predicted_bad([()]) and not is_sat([()]))
    raw=json.loads((ROOT/'three_core286_full_raw.json').read_text())
    distro,sample=y6_audit(raw)
    U=inp();V=[list(c) for c in U]
    V[2][2],V[44][2]=V[44][2],V[2][2]
    V=tuple(tuple(c) for c in V)
    chk(valid(U,198) and valid(V,198))
    chk(len(S)==198 and all(any((S[abs(z)-1]=='1')==(z>0) for z in c) for c in V))
    proof=certificate_u198(U)
    for name,F in (('Y6_SAT',Y),('U198_UNSAT',U),('V198_SAT',V)):
        c=collections.Counter()
        for i,a in enumerate(F):
            for j in range(i+1,len(F)):
                b=F[j];q={abs(z) for z in a}&{abs(z) for z in b}
                if not q:tag='1111'
                elif a[0]*b[0]>0:tag='1001'
                else:tag='0110'
                c[tag]+=1
        chk(dict(c)==raw['cases'][name]['compatibility_counts'])
    report={'run':'ARC-MONOTONE-THREE-CORE286-INDEPENDENT','status':'PASS',
      'catalogue_monotone_clauses_n4':len(all_cl),'catalogue_1_to_3_clause_sets_checked':count,
      'catalogue_split':{str(k):v for k,v in types.items()},'Y6':distro,'Y6_minimal_three_core_example':sample,
      'original_U198_UNSAT_certificate':proof,'original_V198_SAT_verified':True,
      'independent_assertions':assertions,'other_checks':dict(checks)}
    (ROOT/'three_core286_independent.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
