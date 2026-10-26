#!/usr/bin/env python3
"""A-LEAF-SPECTRUM135: finite source authenticated branch+exact-A controls.
Stdlib only; asymptotic proof uses independently published PCR hardness.
Run: python 2026-10-26_0829_A_LEAF_SPECTRUM135_repro.py [raw.json]
"""
import itertools, json, sys, collections, hashlib, math, random
seed=13520261026
rng=random.Random(seed)
checks=collections.Counter()

def check(test,tag):
    checks[tag]+=1
    if not test: raise AssertionError(tag)

def ser(clauses,n):
    return f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)

def parse(s):
    lines=s.splitlines(keepends=True)
    h=lines[0].split();check(len(h)==4 and h[:2]==['p','cnf'],'header_syntax')
    n,m=int(h[2]),int(h[3]);check(m==len(lines)-1,'clause_count')
    offset=len(lines[0].encode());out=[]
    for line in lines[1:]:
        v=[int(x) for x in line.split()]
        check(bool(v) and v[-1]==0,'trailer_zero')
        check(all(0<abs(x)<=n for x in v[:-1]),'literal_indices')
        out.append((tuple(v[:-1]),offset));offset+=len(line.encode())
    check(offset==len(s.encode()),'full_byte_length')
    return n,out

def eval_clause(clause,alpha):
    # None if still undetermined, False when falsified, True when satisfied
    flags=[alpha.get(abs(x)) for x in clause]
    if any(flag is not None and (flag==(x>0)) for x,flag in zip(clause,flags)):return True
    if all(flag is not None for flag in flags):return False
    return None

def restrict(clauses,alpha):
    out=[]
    for cl in clauses:
        if eval_clause(cl,alpha) is True:continue
        out.append(tuple(x for x in cl if abs(x) not in alpha))
    return out

def sat(clauses):
    # independent exact enumerator; family controls <=15 active names
    vars_=sorted({abs(x) for c in clauses for x in c})
    for bits in itertools.product((False,True),repeat=len(vars_)):
        alpha=dict(zip(vars_,bits))
        if all(eval_clause(c,alpha) is True for c in clauses):return True
    return False

def all_source(clause_ids,clauses):return [clauses[i] for i in clause_ids]

def verify_tree(root,raw,tree,source_n):
    """Exact proof grammar: complete binary branches, source-index A-leaves.
    A-leaf is accepted only if exact decider returns UNSAT on source subset
    after ancestor assignments; zero guest labels are supplied externally.
    """
    _,parsed=parse(raw)
    check([c for c,_ in parsed]==root,'original_source_match')
    allids=set(range(len(root)))
    stats={'branch_nodes':0,'leaves':0,'guest_calls':0,'guest_total_bytes':0,
           'guest_max_bytes':0,'max_depth':0,'accepted':True,'source_offset_reads':0,
           'child_records':[]}
    def rec(node,alpha,depth):
        if not isinstance(node,dict):return False
        if node.get('kind')=='branch':
            v=node.get('variable')
            if not isinstance(v,int) or v<1 or v>source_n or v in alpha or set(node)!={'kind','variable','zero','one'}:return False
            stats['branch_nodes']+=1
            left=rec(node['zero'],{**alpha,v:False},depth+1)
            right=rec(node['one'],{**alpha,v:True},depth+1)
            return left and right
        if node.get('kind')=='A-source':
            if set(node)!={'kind','ids'}:return False
            ids=node['ids']
            if not isinstance(ids,list) or len(set(ids))!=len(ids) or not all(type(i)==int and i in allids for i in ids):return False
            for i in ids:
                source_clause,offset=parsed[i]
                # Read actual source line, not an unauthenticated guessed clause.
                byte_line=raw.encode()[offset:].split(b'\n',1)[0].decode()
                check(tuple(map(int,byte_line.split()[:-1]))==source_clause,'line_offset_auth')
                stats['source_offset_reads']+=1
            residual=restrict(all_source(ids,root),alpha)
            child=ser(residual,source_n)
            nn,reparsed=parse(child)
            check(nn==source_n and [c for c,_ in reparsed]==residual,'ordinary_child_roundtrip')
            outcome=not sat(residual)
            stats['guest_calls']+=1;stats['leaves']+=1
            stats['guest_max_bytes']=max(stats['guest_max_bytes'],len(child.encode()))
            stats['guest_total_bytes']+=len(child.encode())
            stats['max_depth']=max(stats['max_depth'],depth)
            stats['child_records'].append({'depth':depth,'q':len(ids),'active_variables':len({abs(x) for c in residual for x in c}),
              'bytes':len(child.encode()),'UNSAT':outcome,'branch':''.join(f'{v}:{int(alpha[v])},' for v in sorted(alpha))})
            return outcome
        return False
    stats['accepted']=rec(tree,{},0)
    return stats

W1=[tuple(map(int,p.split())) for p in '''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''.split(';')]

def blocking3():
    return [tuple((-i if bit else i) for i,bit in zip((1,2,3),bits)) for bits in itertools.product((0,1),repeat=3)]

def full_tree(ids,variables):
    if not variables:return {'kind':'A-source','ids':ids[:]}
    x=variables[0]
    return {'kind':'branch','variable':x,'zero':full_tree(ids,variables[1:]),'one':full_tree(ids,variables[1:])}

def greedy_core(F,alpha):
    ids=list(range(len(F)))
    for i in ids[:]:
        if not sat(restrict([F[j] for j in ids if j!=i],alpha)):ids.remove(i)
    return ids



def implication_edge_list(residual):
    edges=collections.defaultdict(list)
    for source_id,clause in residual:
        if len(clause)==2:
            a,b=clause
            edges[-a].append((b,source_id));edges[-b].append((a,source_id))
        elif len(clause)==1:
            (a,)=clause
            edges[-a].append((a,source_id))
        elif len(clause)==0:
            return edges,source_id
        else:
            raise ValueError('source subset not 2CNF after branch')
    return edges,None

def bfs_implications(graph,start,target):
    frontier=collections.deque([start]);prev={start:None}
    while frontier:
        u=frontier.popleft()
        if u==target:break
        for v,idx in graph.get(u,()):
            if v not in prev:
                prev[v]=(u,idx);frontier.append(v)
    if target not in prev:return None
    out=[];v=target
    while v!=start:
        u,idx=prev[v];out.append((u,v,idx));v=u
    return list(reversed(out))

def derive_scc_leaf(F,alpha,ids):
    residual=[(idx,restrict([F[idx]],alpha)[0]) for idx in ids if restrict([F[idx]],alpha)]
    edges,empty=implication_edge_list(residual)
    if empty is not None:return {'kind':'EMPTY-source','id':empty}
    variables=sorted({abs(lit) for _,C in residual for lit in C})
    for x in variables:
        a=bfs_implications(edges,x,-x)
        b=bfs_implications(edges,-x,x)
        if a is not None and b is not None:return {'kind':'SCC-source','ids':ids,'vertex':x,'forth':a,'back':b}
    return None

def verify_scc_leaf(F,root_bytes,alpha,cert):
    _,parsed=parse(root_bytes)
    if cert is None:return False
    if cert.get('kind')=='EMPTY-source':
        i=cert.get('id')
        return isinstance(i,int) and 0<=i<len(F) and len(restrict([parsed[i][0]],alpha))==1 and len(restrict([parsed[i][0]],alpha)[0])==0
    if cert.get('kind')!='SCC-source':return False
    ids=cert.get('ids');x=cert.get('vertex')
    if not isinstance(ids,list) or len(set(ids))!=len(ids) or not all(type(i)==int and 0<=i<len(F) for i in ids):return False
    if not isinstance(x,int) or x<1:return False
    residual={i:restrict([parsed[i][0]],alpha)[0] for i in ids if restrict([parsed[i][0]],alpha)}
    if any(len(C)>2 for C in residual.values()):return False
    if any(len(C)==0 for C in residual.values()):return False
    def path(witness,start,finish):
        if not isinstance(witness,list):return False
        u=start
        for edge in witness:
            if not isinstance(edge,(list,tuple)) or len(edge)!=3:return False
            a,b,j=edge
            if u!=a or type(j)!=int or j not in residual:return False
            C=residual[j]
            valid= (len(C)==2 and ((-a==C[0] and b==C[1]) or(-a==C[1] and b==C[0]))) or (len(C)==1 and -a==b==C[0])
            if not valid:return False
            u=b
        return u==finish
    return path(cert.get('forth'),x,-x) and path(cert.get('back'),-x,x)

def w1_scc_audit():
    F=W1;n=15;raw=ser(F,n)
    B=[2,4,7,14,15]
    witnesses=[]
    for bits in itertools.product((False,True),repeat=len(B)):
        alpha=dict(zip(B,bits));cert=derive_scc_leaf(F,alpha,list(range(len(F))))
        check(cert is not None,'W1_SCC_certificate_existence')
        check(verify_scc_leaf(F,raw,alpha,cert),'W1_SCC_path_source_auth')
        check(not sat(restrict(F,alpha)),'W1_SCC_residual_unsat')
        if cert['kind']=='SCC-source':
            bad=dict(cert);bad['forth']=[(999,998,0)]+bad['forth']
            check(not verify_scc_leaf(F,raw,alpha,bad),'tampered_path_rejected')
        witnesses.append({'branch':''.join(str(int(y)) for y in bits),'kind':cert['kind'],
           'edges':len(cert.get('forth',[]))+len(cert.get('back',[]))})
    check(len(witnesses)==32,'W1_all_32_assignments')
    # Source subset SCC soundness survives an unrelated residual ternary.
    extended=F+[(16,17,18)]
    raw2=ser(extended,18)
    alpha=dict(zip(B,[False]*len(B)))
    cert=derive_scc_leaf(extended,alpha,list(range(len(F))))
    check(verify_scc_leaf(extended,raw2,alpha,cert),'SCC_even_with_unrelated_ternary')
    check(any(len(C)==3 for C in restrict(extended,alpha)),'unrelated_ternary_survives')
    return {'backdoor_variables':B,'leaves':len(witnesses),
       'edge_records':sum(w['edges'] for w in witnesses),
       'source_bytes':len(raw.encode()),'witnesses':witnesses}

def tseitin_k4_audit():
    edges=list(itertools.combinations(range(4),2))
    idx={e:i+1 for i,e in enumerate(edges)}
    clauses=[]
    for v in range(4):
        incident=[idx[e] for e in edges if v in e]
        charge=1 if v==0 else 0
        for bits in itertools.product((False,True),repeat=3):
            if sum(bits)%2!=charge:
                clauses.append(tuple((-x if b else x) for x,b in zip(incident,bits)))
    check(len(clauses)==16 and all(len(C)==3 for C in clauses),'odd_Tseitin_proper')
    check(not sat(clauses),'odd_Tseitin_UNSAT')
    check(all(sat(clauses[:i]+clauses[i+1:]) for i in range(16)),'odd_Tseitin_minimal')
    return {'vertices':4,'edge_vars':6,'clauses':16,'SAT':False}

def main():
    outcomes=[]
    for kind,F,n in [('blocking3_UNSAT',blocking3(),3),('blocking3_SAT_del0',blocking3()[1:],3),('W1_UNSAT',W1,15),('W1_SAT_del0',W1[1:],15)]:
        root=ser(F,n);pn,parsed=parse(root)
        check(pn==n and [c for c,_ in parsed]==F,'source_roundtrip')
        check(not sat(F) if 'UNSAT' in kind else sat(F),'independent_sat_status')
        coords=[1,2]
        tree=full_tree(list(range(len(F))),coords)
        st=verify_tree(F,root,tree,n)
        check(st['accepted']==(not sat(F)),'both_label_verifier_equivalence')
        check(st['leaves']==4 and st['branch_nodes']==3,'complete_depth2')
        # Every genuine second-level ordinary descendant is separately reparsed.
        for a,b in itertools.product((False,True),repeat=2):
            child1=ser(restrict(F,{1:a}),n)
            child2=ser(restrict(F,{1:a,2:b}),n)
            check(len(parse(child1)[1])==len(restrict(F,{1:a})),'level1_reparsed')
            check(len(parse(child2)[1])==len(restrict(F,{1:a,2:b})),'level2_reparsed')
            check((not sat(restrict(F,{1:a,2:b})))==all(x['UNSAT'] for x in st['child_records'] if x['branch']==f'1:{int(a)},2:{int(b)},'),'two_level_semantics')
        if not sat(F):
            # each path may authenticate just a selected UNSAT original source subset
            cores={}
            for a,b in itertools.product((False,True),repeat=2):
                path={1:a,2:b}
                core_ids=greedy_core(F,path)
                check(not sat(restrict([F[j] for j in core_ids],path)),'greedy_subcore_sound')
                cores[str((int(a),int(b)))]=len(core_ids)
            small_tree={'kind':'branch','variable':1,'zero':{'kind':'branch','variable':2,'zero':{'kind':'A-source','ids':greedy_core(F,{1:False,2:False})},'one':{'kind':'A-source','ids':greedy_core(F,{1:False,2:True})}},'one':{'kind':'branch','variable':2,'zero':{'kind':'A-source','ids':greedy_core(F,{1:True,2:False})},'one':{'kind':'A-source','ids':greedy_core(F,{1:True,2:True})}}}
            st2=verify_tree(F,root,small_tree,n)
            check(st2['accepted'],'compact_leaf_authenticated_UNSAT')
        else: cores=None
        outcomes.append({'case':kind,'root_bytes':len(root.encode()),'clauses':len(F),
          'root_sat':sat(F),'all_source_tree':{k:v for k,v in st.items() if k!='child_records'},'leaf_spectrum':st['child_records'],'greedy_leaf_q':cores})
        # No free A label and no single branch acceptance.
        tampered={'kind':'branch','variable':1,'zero':{'kind':'A-source','ids':list(range(len(F)))},'one':{'kind':'A-source','ids':[-1]}}
        check(not verify_tree(F,root,tampered,n)['accepted'],'tamper_source_id_rejected')
        absent={'kind':'branch','variable':1,'zero':{'kind':'A-source','ids':list(range(len(F)))}}
        check(not verify_tree(F,root,absent,n)['accepted'],'branch_missing_rejected')
    # Proper source signed (2,2) W1 and authenticated SAT/UNSAT controls.
    cnt=collections.Counter((abs(x),x>0) for C in W1 for x in C)
    check(len(W1)==20 and all(cnt[(v,True)]==cnt[(v,False)]==2 for v in range(1,16)),'W1_exact_2P2N')
    check(all(len(c)==3 and len({abs(x) for x in c})==3 for c in W1),'W1_proper_signed_3cnf')
    check(not sat(W1),'W1_independent_unsat')
    check(all(sat(W1[:i]+W1[i+1:]) for i in range(20)),'W1_minimally_unsat')
    # Weighted leaf-spectrum is a combinatorial expansion count, NOT a measured PCR-size lower bound.
    for item in outcomes:
        spectrum=item['leaf_spectrum']
        theoretical=sum(2**(3*record['q']) for record in spectrum)
        check(theoretical>=len(spectrum),'weighted_dpll_expansion_domination')
        item['weighted_expansion_upper']=theoretical
    scc=w1_scc_audit();tseitin=tseitin_k4_audit()
    res={'scc_source_auth':scc,'odd_tseitin':tseitin,'id':'A-LEAF-SPECTRUM135','time':'2026-10-26 08:29 America/Los_Angeles',
      'status':'restricted symbolic theorem + finite controls, no measured asymptotic hardness',
      'seed':seed,'checks':sum(checks.values()),'failures':0,'by_test':dict(sorted(checks.items())),
      'cases':outcomes,'source_A_model':'single fixed exact brute force decider; calls charged in audit only',
      'hardness_anchor':'Conneryd et al FOCS 2023/ECCC TR25-032, asymptotic all-field PCR size lower bound',
      'scope':['BRANCH + authenticated ordinary source-subformula UNSAT A leaves, no arbitrary new-variable projections',
              'full binary leaves and original signed clause IDs',
              'no arbitrary CP, shared DAG, encoded reductions or free truth labels'],
      'open':['uniform all-UNSAT near-boundary coverage','A-generated source-compatible child reduction','ARC-EDGE-90','P versus NP']}
    canonical=json.dumps(res,sort_keys=True,separators=(',',':')).encode()
    res['canonical_sha256']=hashlib.sha256(canonical).hexdigest()
    if len(sys.argv)>1:
        with open(sys.argv[1],'w') as out: json.dump(res,out,sort_keys=True,indent=2)
    print(json.dumps({'id':res['id'],'checks':res['checks'],'failures':0,
         'sha256':res['canonical_sha256'],'cases':[{k:v for k,v in c.items() if k in ('case','root_bytes','clauses','root_sat','greedy_leaf_q')} for c in outcomes]},sort_keys=True,indent=2))
if __name__=='__main__':main()
