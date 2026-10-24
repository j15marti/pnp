#!/usr/bin/env python3
"""M22-WITNESS-VOLUME142 deterministic standard-library experiment.
Not a SAT decision lower bound. Exact counting of a deliberately unpruned
and independently replayed raw-exhaustive one-sided witness protocol.

Run: python /mnt/data/M22_WITNESS_VOLUME142_repro.py \
  --zip /mnt/data/TORUS_EXACT22_FRONTIER116_2026-10-24.zip \
  --out /mnt/data/M22_WITNESS_VOLUME142_results.json
"""
import argparse, ast, hashlib, itertools, json, math, pathlib, random, zipfile
from collections import Counter, deque

RUN='M22-WITNESS-VOLUME142'
SEED='none; deterministic'

def cell(h,i):
    return tuple(6*i+j for j in range(1,7))

def family(h):
    assert h>=1
    pos,neg=[],[]
    p_unmatched=[]
    for i in range(h):
        a,b,c,d,e,f=cell(h,i)
        e_next=cell(h,(i+1)%h)[4]
        P1=(a,b,c);P2=(d,e,f)
        Q1=(a,b,d);Q2=(c,e,f)
        H1=(a,b,e_next);H2=(c,d,f)
        pos.extend((P1,P2,H1,H2)); neg.extend((Q1,Q2,H1,H2))
        p_unmatched.extend((P1,P2))
    return [tuple(c) for c in pos]+[tuple(-v for v in c) for c in neg], p_unmatched

def grammar(F):
    if not F or any(len(c)!=3 or len(set(map(abs,c)))!=3 or not (all(v>0 for v in c) or all(v<0 for v in c)) for c in F):
        return dict(valid=False)
    normalized=[tuple(sorted(c, key=abs)) for c in F]
    if len(set(normalized))!=len(normalized):return dict(valid=False)
    vars_=sorted(set(abs(v) for c in F for v in c))
    counts=Counter((abs(v),v>0) for c in F for v in c)
    if any(counts[v,True]!=2 or counts[v,False]!=2 for v in vars_):return dict(valid=False)
    P=set(tuple(sorted(v for v in c)) for c in F if c[0]>0)
    Q=set(tuple(sorted(-v for v in c)) for c in F if c[0]<0)
    if len(P)!=len(Q):return dict(valid=False)
    H=P&Q
    q=len(P-H)
    con=connected(F)
    return dict(valid=True, k=len(vars_), m=len(F), positive=len(P),negative=len(Q),
                paired_supports=len(H),q=q, c_star=(q!=0), connected=con)

def connected(F):
    adj={abs(v):set() for c in F for v in c}
    for c in F:
        u=[abs(v) for v in c]
        for i in range(len(u)):
            for j in range(i):adj[u[i]].add(u[j]);adj[u[j]].add(u[i])
    if not adj:return False
    todo=[next(iter(adj))];seen=set(todo)
    for x in todo:
        for y in adj[x]:
            if y not in seen:seen.add(y);todo.append(y)
    return len(seen)==len(adj)

def sat(F, bits):
    return all(any((bool(bits[abs(v)-1]) if v>0 else not bool(bits[abs(v)-1])) for v in c) for c in F)

def count_models(F,k,limit=18):
    assert k<=limit
    total=0
    for mask in range(1<<k):
        bits=tuple((mask>>i)&1 for i in range(k))
        total+=sat(F,bits)
    return total

def restrict_true(F,v):
    ans=[]
    for c in F:
        if v in c:continue
        ans.append(tuple(x for x in c if x!=-v))
    return ans

def indexed_width(k,m):
    return max(1,(k+m+1).bit_length())

def encode(F,k,w):
    # Fixed source variable universe k, ordinary length-0..3 clause records,
    # 2-bit arity field, w-bit names, 1-bit sign per literal; no advice or free headers.
    assert len(F)<2**w and k<2**w
    s=f'{k:0{w}b}{len(F):0{w}b}1'
    for c in F:
        assert len(c)<=3
        s+=f'{len(c):02b}'
        for v in c:
            assert 1<=abs(v)<=k
            s+=('1' if v<0 else '0')+f'{abs(v):0{w}b}'
    return s

def count_unpruned(F,Pprime,k):
    # Deliberately count each source-consistent selected-occurrence branch
    # and all raw assignments to the other variables, without SAT pruning.
    cnt=0
    distinct_counts=Counter()
    for sigma in itertools.product(range(3),repeat=len(Pprime)):
        names={Pprime[i][a] for i,a in enumerate(sigma)}
        distinct_counts[len(names)]+=1
        cnt+=1<<(k-len(names))
    return cnt,distinct_counts

def y_source():
    p=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
    n=[(1,2,4),(1,3,6),(2,3,5),(4,5,6)]
    return [tuple(c) for c in p]+[tuple(-v for v in c) for c in n]

def load_published_U(zpath):
    if not zpath or not pathlib.Path(zpath).is_file():return {'status':'not_mounted'}
    with zipfile.ZipFile(zpath) as z:
        key='source_U.txt'
        if key not in z.namelist():return {'status':'not_found_in_zip'}
        original=z.read(key)
    s=original.decode('utf8'); s=s[s.index('[['):]
    F=ast.literal_eval(s)
    F=[tuple(int(x) for x in c) for c in F]
    g=grammar(F)
    return {'status':'parsed', 'archive':str(zpath),'source':key,'sha256':hashlib.sha256(original).hexdigest(),
            'grammar':g,'clauses':F}

def test():
    data={'run_id':RUN,'seed':SEED,'proof_scope':'unpruned raw enumeration protocol only',
          'family':[], 'two_levels':[], 'controls':{},'assertions':0,'failures':0}
    def ck(condition, reason):
        data['assertions']+=1
        if not condition:data['failures']+=1;raise AssertionError(reason)
    for h in (1,2,3,4,8,16,32):
        F,Pprime=family(h);k=6*h;q=2*h;m=len(F)
        info=grammar(F)
        ck(info['valid'] and info['k']==k and info['m']==8*h,'family grammar')
        ck(info['c_star'] and info['q']==q and info['paired_supports']==2*h and info['connected'],'family structure')
        ck(len(set(v for c in Pprime for v in c))==k,'pairwise disjoint partition')
        witness=tuple(x for i in range(h) for x in (1,0,0,1,0,0))
        ck(sat(F,witness),'direct witness')
        w=indexed_width(k,m)
        rootbits=encode(F,k,w)
        row={'h':h,'k':k,'m':m,'q':q,'N_bits':len(rootbits),
             'R_search_analytic':-q*math.log2(1.5),
             'Psi_analytic':'12^'+str(q),
             'distinct_Pprime_feasible':'7^'+str(q),
             'raw_duplication_ratio':'(12/7)^'+str(q)}
        if h<=4:
            exact,dist=count_unpruned(F,Pprime,k)
            ck(exact==12**q,'tight unpruned volume')
            ck(dist==Counter({q:3**q}),'every branch assigns distinct q')
            row['Psi_integer']=str(exact)
            row['branch_count']=3**q
            row['distinct_positive_feasible_integer']=7**q
        if h<=3:
            mods=count_models(F,k)
            ck(mods>0,'brute SAT')
            row['models']=mods
        data['family'].append(row)
    # Two actual syntax-preserving SAT restrictions, never typed Cstar children.
    for h in (1,2,4,8,16,32):
        F,Pprime=family(h);k=6*h;w=indexed_width(k,len(F))
        root=encode(F,k,w)
        L1=[];L2=[]
        first=[]; grand=[]
        for v in Pprime[0]:
            child=restrict_true(F,v); code=encode(child,k,w)
            first.append({'selected':[v],'m':len(child),'N_bits':len(code),'arity':dict(Counter(map(len,child))),
                          'ones_on_fresh_0_tape':code.count('1'),'in_Cstar':bool(grammar(child).get('c_star',False))})
            L1.append((v,child,code))
            for u in Pprime[1]:
                grandchild=restrict_true(child,u)
                code2=encode(grandchild,k,w)
                grand.append({'selected':[v,u],'m':len(grandchild),'N_bits':len(code2),
                              'arity':dict(Counter(map(len,grandchild))),
                              'ones_on_fresh_0_tape':code2.count('1'),
                              'in_Cstar':bool(grammar(grandchild).get('c_star',False))})
                L2.append((v,u,grandchild,code2))
        ck(len(L1)==3 and len(L2)==9,'two-level branching multiplicities')
        ck(all(not z['in_Cstar'] for z in first+grand),'all residuals outside target')
        ck(max(z['N_bits'] for z in first+grand)<len(root),'finite child reduction')
        ck(min(z['N_bits'] for z in grand)>0,'nontrivial children')
        # Disjoint clauses imply every branch assignment selects exactly two names:
        ck(all(v != u for v,u,_,_ in L2),'distinct second-stage sources')
        if h<=2:
            srcsat=count_models(F,k)>0
            childlabels=[count_models(child,k)>0 for _,child,_ in L1]
            grandlabels=[count_models(child,k)>0 for _,_,child,_ in L2]
            ck(srcsat==any(childlabels)==any(grandlabels),'both nested OR levels exact')
        data['two_levels'].append({'h':h,'source_N':len(root),'source_m':len(F),
            'three_children':first,'nine_grandchildren':grand,
            'min_leaf_N_over_source':min(z['N_bits'] for z in grand)/len(root),
            'sum_child_output_bit_writes_floor':sum(len(z[2]) for z in L1),
            'sum_grandchild_output_bit_writes_floor':sum(len(z[3]) for z in L2),
            'serial_one_child_workspace_floor_bits':max([len(z[2]) for z in L1]+[len(z[3]) for z in L2]),
            'two_levels_R_search':2-math.log2(9),
            'two_levels_raw_Psi_over_2k':9/4,
            'two_levels_or_correct':h<=2})
    # Controls: canonical Y SAT, fully paired Y (outside Cstar), and external archived U UNSAT.
    Y=y_source(); yg=grammar(Y);c_y=count_models(Y,6)
    ck(yg['valid'] and yg['c_star'] and yg['q']==4 and c_y==20,'Y anchor')
    ck(sat(Y,(1,1,1,0,0,0)),'Y witness')
    P_y=sorted({tuple(sorted(c)) for c in Y if c[0]>0})
    y_psi,y_dist=count_unpruned(Y,P_y,6)
    ck(y_psi>3**yg['q'] * 2**(yg['k']-yg['q']),'Y overlap strictly increases Psi')
    data['controls']['Y']={'grammar':yg,'models':c_y,'Psi_unpruned':y_psi,'d_distribution':dict(y_dist),'lower':3**yg['q']*2**(yg['k']-yg['q'])}
    fullp=Y[:4]+[tuple(-v for v in c) for c in Y[:4]]
    fg=grammar(fullp)
    ck(fg['valid'] and not fg['c_star'] and fg['q']==0,'paired non-target')
    data['controls']['fully_paired']={'grammar':fg,'models':count_models(fullp,6)}
    other={'2sat_unsat':[(1,2),(-1,2),(1,-2),(-1,-2)],
           'horn_unsat':[(1,),(-1,)],
           'xor3_sat':[(1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3)]}
    for name,F in other.items():
        actual=count_models(F,3)
        ck(not grammar(F)['valid'],'outside target grammar')
        data['controls'][name]={'valid_target':False,'models':actual}
    # Independent source-hypergraph (not necessarily M22) check of the exact
    # count-by-assignment identity, disjoint equality condition, and true
    # assignment union versus multiplicity. Seeded, bounded, and reproducible.
    rng=random.Random(202610241422)
    moment_trials=250; strict_overlap=0; equality_disjoint=0
    for trial in range(moment_trials):
        k=rng.randint(3,9);q=rng.randint(1,5)
        supports=[tuple(rng.sample(range(1,k+1),3)) for _ in range(q)]
        psi,dist=count_unpruned([],supports,k)
        moment=0;union=0
        for a in itertools.product((0,1),repeat=k):
            weights=[sum(a[v-1] for v in S) for S in supports]
            prod=math.prod(weights)
            moment+=prod
            union+=bool(prod)
        ck(moment==psi,'independent assignment-moment count')
        disjoint=len(set(v for S in supports for v in S))==3*q
        ck((psi==3**q*2**(k-q))==disjoint,'equality iff pairwise disjoint')
        ck(union<=psi,'multiplicity vs union')
        if disjoint:equality_disjoint+=1
        else:strict_overlap+=1
    data['controls']['seeded_abstract_hypergraph']={
        'seed':202610241422,'trials':moment_trials,
        'overlap_strict':strict_overlap,'disjoint_equal':equality_disjoint,
        'note':'not necessarily valid M22; finite independent mathematical identity controls'}
    return data

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default='/mnt/data/M22_WITNESS_VOLUME142_results.json')
    parser.add_argument('--zip',default='/mnt/data/TORUS_EXACT22_FRONTIER116_2026-10-24.zip')
    arg=parser.parse_args()
    ans=test()
    U=load_published_U(arg.zip)
    if U['status']=='parsed':
        clauses=U.pop('clauses')
        assert U['grammar']['valid'] and U['grammar']['c_star'] and U['grammar']['k']==198 and U['grammar']['m']==264
        assert U['grammar']['q']==132
        ans['assertions']+=1
        U['imported_UNSAT_status']='Previous certificate imported; same-runtime previous checker replay is separately recorded in report'
        P=sorted({tuple(sorted(c)) for c in clauses if c[0]>0})
        pair=next((a,b) for a in P for b in P if len(set(a)&set(b))==0)
        k=U['grammar']['k']; w=indexed_width(k,len(clauses))
        rootN=len(encode(clauses,k,w)); first=[];second=[]
        for v in pair[0]:
            child=restrict_true(clauses,v)
            first.append({'v':v,'N_bits':len(encode(child,k,w)),'clauses':len(child),
                          'typed_Cstar':bool(grammar(child).get('c_star',False))})
            for u in pair[1]:
                gc=restrict_true(child,u)
                second.append({'v':v,'u':u,'N_bits':len(encode(gc,k,w)),
                               'clauses':len(gc), 'typed_Cstar':bool(grammar(gc).get('c_star',False))})
        assert len(first)==3 and len(second)==9
        assert all(not r['typed_Cstar'] for r in first+second)
        ans['assertions']+=2
        U['two_level_literal_restriction']={'selected_clause_supports':pair,
            'root_bits':rootN,'first_children':first,'second_children':second,
            'derived_UNSAT_status':'each restricted source is UNSAT if the separately replayed parent certificate is correct',
            'no_independent_child_decision':True}

    ans['controls']['archived_Doecker_U']=U
    script=pathlib.Path(__file__).read_bytes()
    ans['script_sha256']=hashlib.sha256(script).hexdigest()
    ans['script_bytes']=len(script)
    path=pathlib.Path(arg.out)
    path.write_text(json.dumps(ans,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'assertions':ans['assertions'],'failures':ans['failures'],
                      'family_sizes':[f['h'] for f in ans['family']],
                      'two_level_sizes':[v['h'] for v in ans['two_levels']],
                      'Y_psi':ans['controls']['Y']['Psi_unpruned'],
                      'U':U['status'],'out':str(path)},indent=2))
if __name__=='__main__':main()
