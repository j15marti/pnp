#!/usr/bin/env python3
"""LSPV-3 ARC265: source-authenticated canonical prism XOR -> constant ordinary SAT child.
Reproducible finite controls and literal-level instrumentation, NOT a native FLMV benchmark.
"""
import itertools, json, collections, random, hashlib, math, pathlib
OUT=pathlib.Path(__file__).with_name('raw.json')
W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
SWAP6=list(W1);SWAP6[9]=(-5,6,-15);SWAP6[13]=(-3,-6,-15)

def expected_supports(k):
    # 2k prism vertices and 3k edges: top k-cycle, bottom k-cycle, k rungs
    return [tuple(sorted(((i-1)%k+1,i+1,2*k+i+1))) for i in range(k)]+[tuple(sorted((k+(i-1)%k+1,k+i+1,2*k+i+1))) for i in range(k)]

def create_prism(k, charge):
    F=[]
    for support,b in zip(expected_supports(k),charge):
        for a in itertools.product((0,1),repeat=3):
            if sum(a)%2 != b:
                F.append(tuple(v if z==0 else -v for v,z in zip(support,a)))
    return F

def output_child(sat):return [(1,)] if sat else [(1,),(-1,)]

def recognize_canonical(F,n):
    """Exact deterministic recognizer for a **syntactically canonical** connected prism grammar.
    Input is indexed, read-only in theoretical transducer. Python list is not a logspace implementation.
    """
    c=collections.Counter()
    c['policy_calls']+=1
    c['header_reads']+=2
    m=len(F)
    if m%8 or m<24 or n!=3*(m//8):return False,None,c
    k=m//8
    targets=expected_supports(k); syndrome=0
    for j,support in enumerate(targets):
        patterns=set();parity=None
        for clause in F[4*j:4*j+4]:
            c['clause_reads']+=1
            c['literal_reads']+=len(clause)
            if len(clause)!=3 or tuple(sorted(map(abs,clause)))!=support:
                return False,None,c
            signs=tuple(int(l<0) for l in sorted(clause,key=abs))
            if signs in patterns:return False,None,c
            patterns.add(signs)
            p=sum(signs)&1
            if parity is None:parity=p
            elif parity!=p:return False,None,c
        if len(patterns)!=4:return False,None,c
        syndrome ^= 1-parity
        c['syndrome_xors']+=1
    c['child_bits_written']+=sum(2+len(c0)*8 for c0 in output_child(syndrome==0))
    return True,syndrome==0,c

def recognize_generic_affine(F,n):
    """Exact grouped-parity plus incidence-graph detector; charges O(source) memory.
    Does NOT claim logspace. Verifies each four-clause block before using charge parity.
    """
    cost=collections.Counter({'policy_calls':1});groups=collections.defaultdict(list)
    for c in F:
        cost['clause_reads']+=1;cost['literal_reads']+=len(c)
        if len(c)!=3 or len({abs(l) for l in c})!=3:return False,None,cost
        sup=tuple(sorted(abs(l) for l in c))
        signs=tuple(int(l<0) for l in sorted(c,key=abs))
        groups[sup].append(signs)
    charges=[];adj=collections.defaultdict(list);inc=collections.defaultdict(list)
    for vid,(sup,patterns) in enumerate(groups.items()):
        cost['pattern_checks']+=len(patterns)
        if len(patterns)!=4 or len(set(patterns))!=4:return False,None,cost
        ps={sum(a)&1 for a in patterns}
        if len(ps)!=1:return False,None,cost
        charges.append(1-next(iter(ps)))
        for x in sup:inc[x].append(vid)
    if len(inc)!=n or set(inc)!=set(range(1,n+1)):return False,None,cost
    for x,vs in inc.items():
        if len(vs)!=2 or vs[0]==vs[1]:return False,None,cost
        a,b=vs;adj[a].append(b);adj[b].append(a);cost['incidence_checks']+=1
    visited=set();sat=True
    for v in range(len(groups)):
        if v in visited:continue
        frontier=[v];visited.add(v);parity=0
        while frontier:
            z=frontier.pop();parity ^= charges[z];cost['component_ops']+=1
            for nb in adj[z]:
                cost['component_ops']+=1
                if nb not in visited:visited.add(nb);frontier.append(nb)
        if parity:sat=False
    cost['child_bits_written']+=sum(2+len(c0)*8 for c0 in output_child(sat))
    cost['peak_aux_slots_proxy']=len(groups)+len(inc)+sum(len(v) for v in adj.values())
    return True,sat,cost

def solve_krom(F,n):
    cost=collections.Counter({'policy_calls':1});g=[[] for _ in range(2*n)];gr=[[] for _ in range(2*n)]
    def ix(l):return 2*(abs(l)-1)+int(l<0)
    for c in F:
        cost['clause_reads']+=1;cost['literal_reads']+=len(c)
        if len(c)>2:return False,None,cost
        if not c:return True,False,cost
        a,b=(c[0],c[0]) if len(c)==1 else c
        for u,v in [(-a,b),(-b,a)]:
            g[ix(u)].append(ix(v));gr[ix(v)].append(ix(u));cost['graph_edges']+=1
    visited=set();order=[]
    def dfs0(v):
        visited.add(v)
        for w in g[v]:
            cost['graph_traversals']+=1
            if w not in visited:dfs0(w)
        order.append(v)
    for v in range(2*n):
        if v not in visited:dfs0(v)
    scc={};cc=0
    def dfs1(v):
        scc[v]=cc
        for w in gr[v]:
            cost['graph_traversals']+=1
            if w not in scc:dfs1(w)
    for v in reversed(order):
        if v not in scc:dfs1(v);cc+=1
    sat=all(scc[2*i]!=scc[2*i+1] for i in range(n))
    cost['peak_aux_slots_proxy']=6*n+sum(map(len,g))+sum(map(len,gr))
    cost['child_bits_written']+=sum(2+len(c0)*8 for c0 in output_child(sat))
    return True,sat,cost

def solve_horn(F,n):
    cost=collections.Counter({'policy_calls':1});ones=[False]*(n+1)
    for c in F:
        cost['clause_reads']+=1;cost['literal_reads']+=len(c)
        if sum(l>0 for l in c)>1:return False,None,cost
    changed=True;sat=True
    while changed and sat:
        changed=False
        for c in F:
            cost['clause_reads']+=1;cost['literal_reads']+=len(c)
            if all(ones[abs(l)] for l in c if l<0):
                heads=[l for l in c if l>0]
                if not heads:sat=False;break
                v=heads[0]
                if not ones[v]:ones[v]=True;changed=True;cost['forced_assignments']+=1
    cost['peak_aux_slots_proxy']=n+1
    cost['child_bits_written']+=sum(2+len(c0)*8 for c0 in output_child(sat))
    return True,sat,cost

def portfolio(F,n):
    ledger=collections.Counter();attempts=[]
    for name,method in [('canonical',recognize_canonical),('generic_xor',recognize_generic_affine),('krom',solve_krom),('horn',solve_horn)]:
        recognized,label,cost=method(F,n)
        attempts.append({'policy':name,'recognized':recognized,'result':label if recognized else None,'cost':dict(cost)})
        ledger.update({k:v for k,v in cost.items() if k!='peak_aux_slots_proxy'})
        if recognized:
            return {'label':'SAT' if label else 'UNSAT','winner':name,'attempts':attempts,'ledger':dict(ledger),'selected_work_proxy':sum(ledger.values()),'peak_aux_slots_proxy':max(a['cost'].get('peak_aux_slots_proxy',8) for a in attempts)}
    base=up_dpll(F,n)
    ledger['fallback_work_proxy']=base['work'];ledger['fallback_calls']=1
    return {'label':base['label'],'winner':'dpll_fallback','attempts':attempts,'ledger':dict(ledger),'selected_work_proxy':sum(ledger.values()),'peak_aux_slots_proxy':'up to full input + DPLL recursion'}

def eval_full(F,a):return all(any(a[abs(l)-1]==int(l>0) for l in c) for c in F)

def endpoint_counts(F,n):
    def counts(bits):
        z=[0,0,0,0]
        for c in F:
            q=sum(bits[abs(l)-1]==int(l>0) for l in c)
            z[q]+=1
        return z
    return {'zero':counts([0]*n),'one':counts([1]*n)}

def gray_explore(F,n):
    inc=[[] for _ in range(n)]
    for j,c in enumerate(F):
        for l in c:inc[abs(l)-1].append((j,int(l>0)))
    a=[0]*n;t=[sum(int(l<0) for l in c) for c in F];false=sum(q==0 for q in t)
    cost=collections.Counter({'initial_clause_visits':len(F),'initial_literal_reads':sum(map(len,F))})
    first=(0 if false==0 else None); count=0 if false else 1;fliptrail=[];states=1
    for h in range(1,1<<n):
        v=(h&-h).bit_length()-1
        old=a[v];a[v]=1-old
        for j,pos in inc[v]:
            before=t[j]; delta=1 if a[v]==pos else -1
            after=before+delta; t[j]=after
            if before==0:false-=1
            if after==0:false+=1
            cost['literal_updates']+=1
        states+=1;cost['state_checks']+=1
        if len(fliptrail)<12:
            fliptrail.append({'flip':v+1,'num_falsified':false,'n0_n1_n2_n3':[sum(q==r for q in t) for r in range(4)]})
        if false==0:
            count+=1
            if first is None:first=h
    return {'model_count':count,'first_gray_index':first,'states':states,'cost':dict(cost),'first_flips':fliptrail}

def up_dpll(F,n):
    count=collections.Counter(); a={}
    def work():
        count['nodes']+=1
        while True:
            unit=None; pending=[]
            for j,c in enumerate(F):
                count['clause_scans']+=1
                live=[];sat=False
                for l in c:
                    count['literal_scans']+=1
                    v=abs(l)-1
                    if v in a:
                        if a[v]==int(l>0):sat=True;break
                    else:live.append(l)
                if sat:continue
                if not live:
                    count['contradictions']+=1
                    return None
                pending.append(c)
                if len(live)==1:unit=live[0];break
            if not pending:
                return dict(a)
            if unit is None:break
            v=abs(unit)-1;a[v]=int(unit>0);count['unit_forces']+=1
        v=next((x for x in range(n) if x not in a),None)
        if v is None:return None
        for b in (0,1):
            cp=dict(a); a[v]=b
            count['branches']+=1
            r=work()
            if r is not None:return r
            a.clear();a.update(cp)
        return None
    witness=work()
    if witness is not None:
        for v in range(n):witness.setdefault(v,0)
    count['witness_checks']+=sum(len(c) for c in F) if witness is not None else 0
    assert (witness is None or eval_full(F,[witness[i] for i in range(n)]))
    return {'label':'SAT' if witness is not None else 'UNSAT','nodes':count['nodes'],'literal_scans':count['literal_scans'],'work':sum(count.values()),'trace':dict(count)}

def extreme_audit(F,n,full=True):
    clauses=[]; allpairs=[]
    for j,c in enumerate(F):
        sat_target={str(abs(l)):int(l>0) for l in c}
        unsat_target={str(abs(l)):int(l<0) for l in c}
        clauses.append({'clause':j+1,'literals':list(c),'S':sat_target,'invert_S_to_U':unsat_target,'U':unsat_target,'invert_U_to_S':sat_target,'occurrences':[{'occurrence':f'x_{abs(l)},{j+1}','literal':l,'S':int(l>0),'inverted_S_is_U':int(l<0),'U':int(l<0),'inverted_U_is_S':int(l>0)} for l in c]})
    # Conditions apply to *local full-TRUE/full-FALSE literal extrema*, not to disjunction SAT.
    for j,c in enumerate(F):
        for h in range(j+1,len(F)):
            d=F[h];same=opp=False
            for l in c:
                for r in d:
                    if abs(l)==abs(r):
                        same|=(l==r);opp|=(l==-r)
            m={'SS':not opp,'SU':not same,'US':not same,'UU':not opp}
            if full:allpairs.append({'j':j+1,'k':h+1,'matrix':m,'same':bool(same),'opposite':bool(opp)})
    return {'source_extremes':clauses,'pair_modes':allpairs}

def rename(F,n,seed):
    r=random.Random(seed);p=list(range(1,n+1));r.shuffle(p);flip=[r.randrange(2) for _ in range(n)]
    return [tuple((1 if l>0 else -1)*(-1 if flip[abs(l)-1] else 1)*p[abs(l)-1] for l in c) for c in F]

def test_instance(name,F,n,exhaustive,extra=True):
    rec,label,rc=recognize_canonical(F,n)
    child=output_child(label) if rec else None
    baseline=up_dpll(F,n)
    if rec:assert baseline['label']==('SAT' if label else 'UNSAT')
    assert portfolio(F,n)['label']==baseline['label']
    entry={'name':name,'n':n,'m':len(F),'source_clauses':[list(c) for c in F],'portfolio':portfolio(F,n),'recognition':rec,'child':child,'child_clauses':len(child) if child else None,'recognized_label':('SAT' if label else 'UNSAT') if rec else None,'baseline':baseline,'recognition_work':dict(rc),'endpoints':endpoint_counts(F,n),'source_sha256':hashlib.sha256(json.dumps(F).encode()).hexdigest()}
    if exhaustive:
        g=gray_explore(F,n)
        entry['gray']=g
        assert (g['model_count']>0)==(baseline['label']=='SAT')
    if extra:entry['extremes']=extreme_audit(F,n,full=True)
    return entry

def main():
    raw={'protocol':'ARC265 CANONICAL PRISM SOURCE-GRAMMAR CONTROL','run_id':'2026-10-30_2124_LSPV-3_CANONICAL_XOR_CHILD_GATE265','seed':265,'model':'Python instrumented literal-event + separate theoretical read-only input transducer','cases':[]}
    for k in (3,4,5,6):
        q=2*k
        for odd in (False,True):
            charge=[0]*q;charge[0]=int(odd)
            F=create_prism(k,charge)
            raw['cases'].append(test_instance(f'prism_q{q}_{"UNSAT" if odd else "SAT"}',F,3*k,True,extra=True))
            if k<=4:
                Fn=rename(F,3*k,seed=265+k+int(odd))
                raw['cases'].append(test_instance(f'renamed_prism_q{q}_{"UNSAT" if odd else "SAT"}',Fn,3*k,True,extra=True))
    for name,F in [('W1_UNSAT',W1),('SWAP6_SAT',SWAP6)]:
        raw['cases'].append(test_instance(name,F,15,True,extra=True))
    for name,F,n in [
        ('Horn_easy_SAT',[(1,-2,-3),(-1,-2,3),(-2,-3,4)],4),
        ('Horn_forced_UNSAT',[(1,),(-1,2),(-2,-3,4),(-4,),(3,)],4),
        ('Krom_easy_SAT',[(1,2),(-1,2),(1,-2)],2),
        ('Krom_easy_UNSAT',[(1,2),(-1,2),(1,-2),(-1,-2)],2)]:
        raw['cases'].append(test_instance(name,F,n,True,extra=True))
    # Malicious local parity-block mutation must never be accepted.
    f=create_prism(3,[0]*6);f[0]=tuple(-x if idx==0 else x for idx,x in enumerate(f[0]));raw['cases'].append(test_instance('malformed_parity_nearmiss',f,9,True,extra=True))
    OUT.write_text(json.dumps(raw,indent=2)+'\n')
    print(json.dumps({'cases':len(raw['cases']),'SAT':sum(x['baseline']['label']=='SAT' for x in raw['cases']),'UNSAT':sum(x['baseline']['label']=='UNSAT' for x in raw['cases']),'recognized':sum(x['recognition'] for x in raw['cases']),'gray_assignments':sum(x['gray']['states'] for x in raw['cases']),'raw_bytes':OUT.stat().st_size},indent=2))
if __name__=='__main__':main()