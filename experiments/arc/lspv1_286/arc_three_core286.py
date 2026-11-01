#!/usr/bin/env python3
"""ARC-THREE-CORE286 exact restricted local conflict classification and controls.
Standalone stdlib. Original clauses and variable names retained. This is NOT
an FLMV native-machine simulator or a universal P-vs-NP lower bound.
"""
import ast,collections,hashlib,itertools,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
V198_WITNESS='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
work=collections.Counter()
def load_source():
    s=(HERE/'DOECKER61_original_source.txt').read_text();return tuple(tuple(c) for c in ast.literal_eval(s[s.index('[['):]))
def legal(F,n):
    if n%3 or 3*len(F)!=4*n:return False
    d=collections.Counter();seen=set()
    for c in F:
        if len(c)!=3 or len({abs(v) for v in c})!=3 or not(all(v>0 for v in c) or all(v<0 for v in c)):return False
        if any(abs(v)<1 or abs(v)>n for v in c):return False
        key=tuple(sorted(c));
        if key in seen:return False
        seen.add(key)
        for v in c:d[(abs(v), v>0)]+=1
    return all(d[(x,b)]==2 for x in range(1,n+1) for b in (True,False))
def partial_clause(c,rho):
    if any(rho[abs(l)-1] == int(l>0) for l in c):return None
    return tuple(l for l in c if rho[abs(l)-1]<0)
def local_cert(g):
    """Return ('empty'/'pair'/'triple', original indices, literals) or None;
    assumes g is list of (original index, residual clause)."""
    for i,c in g:
        work['core_empty_checks']+=1
        if not c:return ('empty',(i,),())
    units={}
    for i,c in g:
        if len(c)==1:
            l=c[0]
            if -l in units:return ('pair',(units[-l],i),(l,-l))
            units[l]=i
    # All pairs of same-sign units x,y and opposite-sign exact binary -x,-y.
    if len(g)>=3:
        for i,c in g:
            if len(c)!=2:continue
            a,b=c
            if -a in units and -b in units and abs(a)!=abs(b):
                return ('triple',(units[-a],units[-b],i),(a,b))
    return None
def truth(c,b):return any(b[abs(l)-1]==int(l>0) for l in c)
def sat_brute(g,allvars):
    # independent complete enumeration of relevant free variables
    vs=sorted({abs(l) for c in g for l in c});work['brute_core_tests']+=1
    for a in itertools.product((0,1),repeat=len(vs)):
        v=dict(zip(vs,a));work['brute_truth_rows']+=1
        if all(any(v[abs(l)]==int(l>0) for l in c) for c in g):return True
    return False
def signed_occurrence_targets(F):
    rows=[]
    for j,c in enumerate(F):
        rows.append({'original_index_0':j,'original_clause':list(c),
         'occurrences':[{'literal':l,'variable':abs(l),'S':int(l>0),'U':int(l<0),'invert_S_is_U':True,'invert_U_is_S':True} for l in c]})
    return rows
def pair_compat(F):
    pairs=[];cnt=collections.Counter()
    for j,a in enumerate(F):
        for k in range(j+1,len(F)):
            b=F[k]; common={abs(x) for x in a}&{abs(x) for x in b}
            opp=any(any(x==-y for x in a for y in b if abs(x)==v) for v in common)
            same=any(any(x==y for x in a for y in b if abs(x)==v) for v in common)
            code=(int(not opp),int(not same),int(not same),int(not opp))
            cnt[''.join(map(str,code))]+=1
            pairs.append({'j':j,'k':k,'SS':code[0],'SU':code[1],'US':code[2],'UU':code[3]})
            work['compat_pair_lit_checks']+=len(a)*len(b)
    return pairs,dict(cnt)
def t_hist(F,a):
    hist=[0,0,0,0]
    for c in F:
        t=sum(a[abs(l)-1]==int(l>0) for l in c)
        hist[t]+=1
    return hist
def flip_trails(F,n):
    a=[0]*n;out=[]
    for k in range(min(n,6)+1):
        if k:a[k-1]^=1
        out.append({'flip_index':k,'weight':sum(a),'N_0_to_N_3':t_hist(F,a), 'complement_hist':t_hist(F,[1-x for x in a])})
    return out
def encoded_clause_state(F,a,gray=False):
    # Complete aligned diagnostic: 1 assignment bit per variable + 2 true-count
    # bits + 1 satisfaction flag for each ORIGINAL source clause.
    b=list(a)
    for c in F:
        t=sum(a[abs(l)-1]==int(l>0) for l in c)
        q=t^(t>>1) if gray else t
        b.extend([q&1,(q>>1)&1,int(t>0)])
    return tuple(b)
def xor_activity(F,n):
    a=[0]*n; prev_B=encoded_clause_state(F,a);prev_G=encoded_clause_state(F,a,True)
    traces=[];total_B=total_G=0;initial_B=prev_B;initial_G=prev_G
    for x in range(min(n,6)):
        a[x]=1-a[x]
        new_B=encoded_clause_state(F,a);new_G=encoded_clause_state(F,a,True)
        db=sum(u!=v for u,v in zip(prev_B,new_B))
        dg=sum(u!=v for u,v in zip(prev_G,new_G))
        changed_clause_ids=[j for j,c in enumerate(F) if x+1 in {abs(l) for l in c}]
        assert len(changed_clause_ids)==4
        # In the canonical target every pivot appears in exactly 4 clauses.
        assert 5<=dg<=9 and dg<=db<=9
        total_B+=db;total_G+=dg
        traces.append({'original_variable_1':x+1,'changed_original_clause_ids_0':changed_clause_ids,
              'd_logic_binary':db,'d_logic_Gray':dg,
              'd_phys_FLMV':None,'read_only_source_bits_changed':0})
        prev_B=new_B;prev_G=new_G
    return {'aligned_vector_bits':len(initial_B),'steps':traces,
       'adjacent_total_binary':total_B,'adjacent_total_Gray':total_G,
       'endpoint_binary':sum(u!=v for u,v in zip(initial_B,prev_B)),
       'endpoint_Gray':sum(u!=v for u,v in zip(initial_G,prev_G)),
       'diagnostic_is_offline_not_native_FLMV':True}

def dpll(F,n,cap):
    nodes=0;prop=0;clause_visits=0
    def red(G,lit):return tuple(tuple(x for x in c if x!=-lit) for c in G if lit not in c)
    def go(G):
        nonlocal nodes,prop,clause_visits
        if nodes>=cap:return None
        nodes+=1
        while True:
            clause_visits+=len(G)
            if not G:return True
            if any(len(c)==0 for c in G):return False
            u=next((c[0] for c in G if len(c)==1),None)
            if u is None:break
            G=red(G,u);prop+=1
        pivot=abs(G[0][0]);l=go(red(G,pivot))
        if l is True:return True
        r=go(red(G,-pivot))
        if l is None or r is None:return None if r is not True else True
        return r
    z=go(F)
    return {'status':'SAT' if z is True else ('UNSAT' if z is False else 'UNRESOLVED'), 'nodes':nodes,'propagations':prop,'clause_visits':clause_visits,'limit':cap}
def witness(F,bits):return all(truth(c,tuple(int(x) for x in bits)) for c in F)
def analyze_Y():
    bucket=collections.Counter();example=None;examples=[];all_partial=0
    for rho in itertools.product((-1,0,1),repeat=6):
        all_partial+=1;g=[(j,q) for j,c in enumerate(Y) if (q:=partial_clause(c,rho)) is not None]
        # Actual declared controller: run local certificate detector BEFORE the
        # independent exhaustive answer check, with acquisition charged.
        work['policy_original_clause_scans']+=len(Y)
        work['policy_original_literal_tests']+=3*len(Y)
        cert=local_cert(g)
        # Exact all-completions check; 3^6 partials, <=64 complete assignments each.
        valid_ext=False
        for b in itertools.product((0,1),repeat=6):
            if all(rho[i]<0 or b[i]==rho[i] for i in range(6)) and all(truth(c,b) for c in Y):valid_ext=True;break
            work['full_assignment_ground_truth_tests']+=1
        if valid_ext:
            assert cert is None
            bucket['extendible']+=1;continue
        bucket['nonextendible']+=1
        if cert is None:bucket['no_3_core']+=1;continue
        z=cert[0];bucket['core_'+z]+=1
        if z=='triple':
            idx=cert[1];core=[(i,dict(g)[i]) for i in idx]
            if example is None:example={'rho':list(rho),'original_clause_indices_0':list(idx),'residual_clauses':[list(q) for _,q in core]}
            examples.append({'rho':list(rho),'indices_0':list(idx)})
        assert not sat_brute([dict(g)[i] for i in cert[1]],6)
        # Independently enumerate ALL original clause subsets of sizes 1 and 2.
        if z=='triple':
            for pair in itertools.combinations(g,2):
                assert sat_brute([c for _,c in pair],6)
                work['pair_nonconflict_controls']+=1
    assert all_partial==729
    assert bucket['no_3_core']==0
    return {'counts':dict(bucket),'three_core_example':example,'all_triple_core_restrictions':examples,'DPLL_original':dpll(Y,6,512)}
def main():
    assert legal(Y,6)
    U=load_source();V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=tuple(tuple(c) for c in V)
    assert legal(U,198) and legal(V,198) and len(V198_WITNESS)==198 and witness(V,V198_WITNESS)
    y=analyze_Y()
    cases={}
    for name,F,n in (('Y6_SAT',Y,6),('U198_UNSAT',U,198),('V198_SAT',V,198)):
        pairs,stats=pair_compat(F)
        cases[name]={'target_valid':legal(F,n),'n':n,'m':len(F),'source_sha256':hashlib.sha256(str(F).encode()).hexdigest(),
            'local_extremes':signed_occurrence_targets(F),'pair_compatibility_indexed':pairs,
            'compatibility_counts':stats,'zero_hist':t_hist(F,[0]*n),'one_hist':t_hist(F,[1]*n),
            'partial_flip_trail':flip_trails(F,n),'xor_flip_trail':xor_activity(F,n),'UP_DPLL':dpll(F,n,500 if n>6 else 512)}
    # Prove Y6 3-core: (x1 v x4 v x5), (x2 v x4 v x6), (-x1 v -x3 v -x6)
    rho=(-1,0,1,0,0,-1)
    assert [partial_clause(Y[i],rho) for i in (1,2,5)]==[(1,),(6,),(-1,-6)]
    # Result by two original-source resolution steps:
    # (x4 v x5 v -x3 v -x6), then (x2 v x4 v x5 v -x3).
    learned=(2,4,5,-3)
    for b in itertools.product((0,1), repeat=6):
        assert all(truth(c,b) for c in Y) <= truth(learned,b)
    cases['Y6_SAT']['all_models']=sum(all(truth(c,b) for c in Y) for b in itertools.product((0,1),repeat=6))
    assert cases['Y6_SAT']['all_models']==20
    data={'run':'ARC-MONOTONE-THREE-CORE286','date_pdt':'2026-10-31 16:55 PDT','status':'COMPUTATIONAL exact finite verified; unrestricted ARC OPEN',
          'statement':'For monotone residual CNF, any <=3-clause UNSAT core contains an empty clause, opposing unit pair, or two units same sign plus their opposite binary.',
          'Y6':y,'learned_clause_from_indices_0_1_2_5':list(learned),'cases':cases,'offline_diagnostic_counts':dict(work),
          'machine_cost_caveat':'Python clause visits/assignment checks are illustrative logical-operation counts, NOT indexed-FLMV native time/space. Diagnostics and validators must be charged when online.'}
    dest=HERE/'three_core286_full_raw.json';dest.write_text(json.dumps(data,separators=(',',':')))
    summary={k:v for k,v in data.items() if k not in ('cases',)}
    summary['cases']={name:{k:v for k,v in c.items() if k not in ('local_extremes','pair_compatibility_indexed','partial_flip_trail') } for name,c in cases.items()}
    (HERE/'three_core286_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps({'status':'PASS','Y6':y['counts'],'three_core_example':y['three_core_example'],
      'models':cases['Y6_SAT']['all_models'],'compat':{q:cases[q]['compatibility_counts'] for q in cases},
      'baseline_DPLL':{q:cases[q]['UP_DPLL'] for q in cases},'offline_counts':dict(work),
      'full_bytes':dest.stat().st_size},indent=2))
if __name__=='__main__':main()
