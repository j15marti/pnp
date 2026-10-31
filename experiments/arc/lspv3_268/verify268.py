#!/usr/bin/env python3
"""Independent source-level finite verifier for Horn-support268 raw data.
Does not import arc268 or arc267. All answers are checked against original CNF.
"""
import json,sys,itertools,collections,pathlib,math,random
C=collections.Counter()

def chk(ok,tag):
    C['assertions']+=1
    if not ok:raise AssertionError(tag)

def nvars(F):return max((abs(x) for c in F for x in c),default=0)

def counts(F,a):return [sum(((a>>(abs(l)-1))&1)==(l>0) for l in c) for c in F]

def sat(F,a):return all(x>0 for x in counts(F,a))

def up(F,assume):
    a={abs(l):int(l>0) for l in assume}
    while True:
        changed=False
        for c in F:
            if any(abs(l) in a and a[abs(l)]==int(l>0) for l in c):continue
            u=[l for l in c if abs(l) not in a]
            if not u:return False
            if len(u)==1:
                l=u[0];a[abs(l)]=int(l>0);changed=True;break
        if not changed:return True

def audit(F,audit):
    n=nvars(F)
    chk(len(audit['clauses_and_occurrences'])==len(F),'clause count')
    for j,(c,info) in enumerate(zip(F,audit['clauses_and_occurrences']),1):
        chk(info['j']==j and info['clause']==c,'clause provenance')
        s={abs(l):int(l>0) for l in c};u={x:1-y for x,y in s.items()}
        chk(info['S_local']==[list(v) for v in sorted(s.items())],'S')
        chk(info['U_local']==[list(v) for v in sorted(u.items())],'U')
        chk(info['S_inverted_U']==[list(v) for v in sorted(u.items())],'S inverse')
        chk(info['U_inverted_S']==[list(v) for v in sorted(s.items())],'U inverse')
        for l,occ in zip(c,info['occurrences']):
            chk(occ['variable']==abs(l) and occ['signed_literal']==l,'signed occurrence')
            chk(occ['S_target']==int(l>0) and occ['U_target']==int(l<0),'occ polarity')
            chk(occ['S_inversion']==int(l<0) and occ['U_inversion']==int(l>0),'occ inverse')
    for row in audit['pair_matrix']:
        j,k=row['source_j']-1,row['source_k']-1
        chk(0<=j<k<len(F),'pair index')
        for a,b in itertools.product('SU',repeat=2):
            d={abs(l):int(l>0) if a=='S' else int(l<0) for l in F[j]}
            compatible=all(abs(l) not in d or d[abs(l)]==(int(l>0) if b=='S' else int(l<0)) for l in F[k])
            chk(row[a+b]==compatible,'pair compatibility')
    for end in audit['global_endpoints']:
        bit=end['bit'];val=(1<<n)-1 if bit else 0;ts=counts(F,val)
        chk(ts==end['t_by_original_clause'],'end clause counts')
        chk(end['status']==('SAT' if min(ts)>0 else 'UNSAT_ASSIGNMENT'),'end status')
        for r in range(max(map(len,F))+1):chk(end['N_r'][str(r)]==ts.count(r),'end histogram')
    for row in audit['flip_trail']:
        a=row['assignment_bits'];chk(row['true_literal_counts']==counts(F,a),'gray counts')
        chk(a==(row['gray_index']^(row['gray_index']>>1)),'gray index')
        chk(row['source_clause_sat_count']==sum(t>0 for t in counts(F,a)),'gray sats')
    for trace in audit['adaptive_flip_trails']:
        for f in trace['frames']:
            a=sum(b<<(v-1) for v,b in f['assignment'])
            chk(counts(F,a)==f['source_true_counts'],'adaptive counts')
            chk(f['violated_clauses']==counts(F,a).count(0),'adaptive unsats')
    C['audited_original_clauses']+=len(F)

def validate(raw):
    chk(raw['schema']=='horn-support268-v1','schema')
    for name,r in raw['cases'].items():
        sets=[set(x) for x in r['sets']];m=len(set.union(*sets));s=len(sets)
        d=list(range(1,s+1));e=list(range(s+1,s+m+1));t=s+m+1
        H=r['source_H'];chk(r['assumptions']==d and r['target']==t,'IDs')
        chk(all(sum(l>0 for l in c)<=1 and 1<=len(c)<=3 for c in H),'definite Horn 3CNF')
        expected=[]
        for i,S in enumerate(sets):
            for u in sorted(S):expected.append([-d[i],e[u]])
        if m==2:expected.append([-e[0],-e[1],t])
        else:
            z=t+1;expected.append([-e[0],-e[1],z]);prev=z
            for u in range(2,m):
                nxt=t if u==m-1 else t+u
                expected.append([-prev,-e[u],nxt]);prev=nxt
        chk(H==expected,'authenticated original Horn source')
        satF=H+[[v] for v in d]+[[t]]
        unsatF=H+[[v] for v in d]+[[-t]]
        chk(satF==r['sat_source'] and unsatF==r['unsat_source'],'paired original sources')
        chk(len(r['subset_implications'])==(1<<s),'all source assumption cubes')
        best=s+1
        for mask in range(1<<s):
            selected=[i for i in range(s) if mask>>i&1]
            covered=set.union(*(sets[i] for i in selected)) if selected else set()
            cov=(covered==set(range(m)))
            # Independently check logical implication by Horn UP on source + G + !t
            observed=not up(H,[d[i] for i in selected]+[-t])
            chk(cov==observed and r['subset_implications'][mask]==int(observed),'guard inference')
            if cov:best=min(best,len(selected))
        chk(len(r['optimal_guard_indices'])==best,'exact min guard')
        chk(set.union(*(sets[i] for i in r['optimal_guard_indices']))==set(range(m)),'optimal guard actually covers')
        greedy=r['greedy_guard_indices'];chk(set.union(*(sets[i] for i in greedy))==set(range(m)),'greedy covers')
        chk(len(greedy)>=best,'greedy >= min')
        for k in ('sat','unsat'):
            F=r[f'{k}_source'];n=nvars(F)
            # Complete enumeration, not a solver/proof-system assumption
            models=0
            for a in range(1<<n):
                if sat(F,a):models+=1
            label='SAT' if models else 'UNSAT'
            chk(label==('SAT' if k=='sat' else 'UNSAT'),'paired exhaustive correctness')
            chk(label==r[f'{k}_solver']['label']==r[f'{k}_dpll']['decision'],'solver labels')
            audit(F,r[f'audit_{k.upper()}'])
            C['exhaustive_assignments']+=1<<n
        C['cover_cases']+=1
    for name,row in raw['general_controls'].items():
        F=row['original_clauses'];n=nvars(F)
        count_models=sum(sat(F,a) for a in range(1<<n))
        chk(row['adaptive']['label']==('SAT' if count_models else 'UNSAT'),'general control both labels')
        audit(F,row['extrema'])
        C['control_assignments']+=1<<n;C['general_cases']+=1

def corruptions(raw):
    import copy
    bad=copy.deepcopy(raw)
    bad['cases']['greedy_gap6']['optimal_guard_indices']=[0]
    before=C.copy()
    try:validate(bad)
    except AssertionError:
        C.clear();C.update(before);C['corruptions_rejected']+=1
    else:raise AssertionError('corrupted min guard accepted')
    bad=copy.deepcopy(raw)
    bad['cases']['tiny3']['audit_UNSAT']['pair_matrix'][0]['SS']=not bad['cases']['tiny3']['audit_UNSAT']['pair_matrix'][0]['SS']
    before=C.copy()
    try:validate(bad)
    except AssertionError:
        C.clear();C.update(before);C['corruptions_rejected']+=1
    else:raise AssertionError('corrupted S/U accepted')
    bad=copy.deepcopy(raw)
    bad['cases']['tiny3']['unsat_solver']['label']='SAT'
    before=C.copy()
    try:validate(bad)
    except AssertionError:
        C.clear();C.update(before);C['corruptions_rejected']+=1
    else:raise AssertionError('false UNSAT accepted')

if __name__=='__main__':
    data=json.loads(pathlib.Path(sys.argv[1]).read_text())
    validate(data);corruptions(data)
    pathlib.Path(sys.argv[2]).write_text(json.dumps(dict(C),sort_keys=True,indent=2)+'\n')
    print(dict(C))