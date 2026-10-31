#!/usr/bin/env python3
"""LSPV-1 ARC-CHILD-SCAN-AMORTIZATION272, deterministic reproducible controls.
All controller input, output, and guest events are separately counted.
The proved theorem is architectural and does NOT prove any SAT hardness.
"""
import itertools, json, hashlib, pathlib
from collections import Counter
from fractions import Fraction

HERE=pathlib.Path(__file__).resolve().parent
REPO_DATA=HERE.parents[2]/'results'/'raw'/'arc' if HERE.name=='lspv-1' else None
DATA_DIR=REPO_DATA if REPO_DATA and REPO_DATA.is_dir() else HERE
RAW_NAME=('2026-10-31_0700_LSPV1_ARC_CHILD_SCAN_AMORTIZATION272_raw.json' if DATA_DIR!=HERE else 'arc_child_scan272_raw.json')
SUMMARY_NAME=('2026-10-31_0700_LSPV1_ARC_CHILD_SCAN_AMORTIZATION272_summary.json' if DATA_DIR!=HERE else 'arc_child_scan272_summary.json')
STAMP='2026-10-31_0700'

def norm(clause):
    d={abs(z):z for z in clause}
    if len(d)!=len(clause): raise ValueError('duplicate variable in clause')
    return tuple(clause)

def cnf(n, clauses):
    cs=[norm(c) for c in clauses]
    assert all(1<=abs(z)<=n for c in cs for z in c)
    return {'n':n,'clauses':cs}

def signed3(n=3, omit=None):
    allc=list(itertools.product((1,-1),repeat=3))
    return cnf(n,[tuple(sign*(i+1) for i,sign in enumerate(s)) for i,s in enumerate(allc) if s!=omit])

def parity3(bit):
    clauses=[]
    for vals in itertools.product((0,1),repeat=3):
        if (sum(vals)%2)!=bit:
            clauses.append(tuple(-(i+1) if v else (i+1) for i,v in enumerate(vals)))
    return clauses

def cases():
    h7=signed3(omit=(1,-1,1))
    h8=signed3()
    cases={
        'H7_sat':h7,
        'H8_unsat':h8,
        'signed_same_opposite_sat':cnf(3,[(1,2,3),(1,-2,-3)]),
        'xor_even_sat':cnf(3,parity3(0)),
        'xor_contradiction_unsat':cnf(3,parity3(0)+parity3(1)),
        'horn_sat':cnf(4,[(-1,-2,3),(-3,4),(1,),(-2,4)]),
        'dual_horn_sat':cnf(4,[(1,2,-3),(3,-4),(-1,2),(4,)]),
        'krom_unsat':cnf(2,[(1,2),(1,-2),(-1,2),(-1,-2)]),
        'signed_rename_sat':cnf(3,[tuple(((-1 if abs(v) in (1,3) else 1)*v) for v in c) for c in h7['clauses']]),
        'dense_sat':cnf(5,[(1,2,3),(-1,2,4),(-2,-3,5),(1,-4,-5),(-1,-3,4),(2,3,-5),(1,3,4)]),
        'dense_unsat':cnf(5,list(h8['clauses'])+[(4,5,1)]),
        'unit_unsat':cnf(3,[(1,),(-1,),(2,3,1)]),
    }
    return cases

def true_count(clause, a):
    return sum(int(a[abs(v)-1] == int(v>0)) for v in clause)

def status(form,a):
    ts=[true_count(c,a) for c in form['clauses']]
    return {'counts':ts,'bins':{str(k):sum(x==k for x in ts) for k in range(4)},'sat':all(t>0 for t in ts)}

def assignments(n):return itertools.product((0,1),repeat=n)

def is_sat(form):
    return any(status(form,a)['sat'] for a in assignments(form['n']))

def encode(form):
    return 'p cnf {} {}\n'.format(form['n'],len(form['clauses']))+''.join(' '.join(map(str,c))+' 0\n' for c in form['clauses'])

def parse(text):
    lines=[line.strip() for line in text.splitlines() if line.strip() and not line.startswith('c')]
    head=lines[0].split()
    assert head[:2]==['p','cnf']
    n,m=map(int,head[2:])
    clauses=[]
    for line in lines[1:]:
        z=list(map(int,line.split()))
        assert z[-1]==0
        clauses.append(tuple(z[:-1]))
    assert len(clauses)==m
    return cnf(n,clauses) if all(c for c in clauses) else {'n':n,'clauses':clauses}

def cofactor(form,rho):
    out=[]
    for clause in form['clauses']:
        if any(rho.get(abs(v))==int(v>0) for v in clause):continue
        out.append(tuple(v for v in clause if abs(v) not in rho))
    return {'n':form['n'],'clauses':out}

def models(form):
    return [a for a in assignments(form['n']) if status(form,a)['sat']]

def dpll(form):
    stats=Counter()
    def solve(cs, rho):
        stats['nodes']+=1
        while True:
            updated=[]
            for clause in cs:
                stats['clause_visits']+=1
                sats=False; undec=[]
                for z in clause:
                    stats['literal_visits']+=1
                    if abs(z) in rho:
                        if rho[abs(z)]==int(z>0):sats=True;break
                    else:undec.append(z)
                if not sats:
                    if not undec:return False
                    updated.append(tuple(undec))
            if not updated:return True
            units=[c[0] for c in updated if len(c)==1]
            if not units:break
            changed=False
            for z in units:
                x,v=abs(z),int(z>0)
                if x in rho:
                    if rho[x]!=v:return False
                else:
                    rho[x]=v;changed=True;stats['unit_assignments']+=1
            if not changed:break
            cs=updated
        pivot=abs(updated[0][0])
        for v in (0,1):
            branch=dict(rho);branch[pivot]=v
            if solve(updated,branch):return True
        return False
    answer=solve(form['clauses'],{})
    stats['selected_work']=stats['clause_visits']+stats['literal_visits']+stats['nodes']+stats['unit_assignments']
    return answer,dict(stats)

def pair_matrix(c,d):
    def targets(cl,kind):return {abs(z):int(z>0) if kind=='S' else int(z<0) for z in cl}
    return {a+b:all(targets(c,a)[v]==targets(d,b)[v] for v in targets(c,a).keys() & targets(d,b).keys()) for a,b in itertools.product('SU',repeat=2)}

def literal_detail(c,clause_index):
    return [{'occurrence':'x_{{{},{}}}'.format(abs(z),clause_index),
      'literal':z,'S_local':int(z>0),'inverted_S_local':int(z<0),
      'U_local':int(z<0),'inverted_U_local':int(z>0)} for z in c]

def source_resolvents(form):
    cs=form['clauses'];out=[]
    for i,c in enumerate(cs):
        for j in range(i+1,len(cs)):
            d=cs[j]
            for x in sorted({abs(z) for z in c if -z in d}):
                pivot=next(z for z in c if abs(z)==x)
                tail=[z for z in c if z!=pivot]+[z for z in d if z!=-pivot]
                if any(-z in tail for z in tail):continue
                resolvent=sorted(set(tail),key=lambda z:(abs(z),z))
                blocker={str(abs(z)):int(z<0) for z in resolvent}
                out.append({'parents':[i+1,j+1],'pivot':x,'resolvent':resolvent,'cube':blocker})
    return out

def exhaustive_extendible(form,rho):
    return any(all(a[i-1]==v for i,v in rho.items()) and status(form,a)['sat'] for a in assignments(form['n']))

def cold_controller(form,b):
    source=encode(form)
    vars_=list(range(1,min(b,form['n'])+1))
    guest=[];read_total=0;writes=0;guest_nodes=0;guest_lits=0;guest_clauses=0;guest_units=0;cofactor_lits=0;parse_tokens=0;policy_events=0;any_sat=False
    for vals in itertools.product((0,1),repeat=len(vars_)):
        rho=dict(zip(vars_,vals))
        policy_events+=1
        # 'cold' architecture reads all source characters independently for each child.
        scanned=''.join(source[j] for j in range(len(source)))
        read_total+=len(source)
        original=parse(scanned)
        parse_tokens+=2+sum(len(c)+1 for c in original['clauses'])
        # The source cofactor operation visits every original literal in this instrumented version.
        cofactor_lits+=sum(len(c) for c in original['clauses'])
        residual=cofactor(original,rho)
        child_str=encode(residual)
        writes+=len(child_str)
        child=parse(child_str)
        ans,counts=dpll(child)
        any_sat|=ans
        guest_nodes+=counts.get('nodes',0);guest_lits+=counts.get('literal_visits',0);guest_clauses+=counts.get('clause_visits',0);guest_units+=counts.get('unit_assignments',0)
        # exact join polarity by independent exhaustive model extension
        check=exhaustive_extendible(original,rho)
        assert ans==check,(form,rho,ans,check)
        guest.append({'cube':{str(k):v for k,v in rho.items()},'length':len(child_str),'answer':ans,'dpll':counts,'child_dimacs':child_str})
    assert any_sat==is_sat(form)
    q=len(guest)
    return {'q':q,'source_characters':len(source),'source_read_characters':read_total,
            'child_write_characters':writes,'guest_literal_visits':guest_lits,
            'guest_clause_visits':guest_clauses,'guest_nodes':guest_nodes,
            'guest_unit_assignments':guest_units,'source_cofactor_literal_visits':cofactor_lits,
            'source_parse_tokens':parse_tokens,'policy_selection_events':policy_events,
            'child_parse_character_reads':writes,
            'selected_total_events':read_total+writes+writes+cofactor_lits+parse_tokens+policy_events+guest_lits+guest_clauses+guest_nodes+guest_units,
            'hypothetical_serial_peak_child_characters':max(g['length'] for g in guest),
            'actual_audit_retained_child_characters':writes,
            'answer':any_sat,'children':guest}

def audit(form,name):
    n=form['n']; cs=form['clauses']; model_list=models(form)
    endpoints={'0'*n:status(form,(0,)*n),'1'*n:status(form,(1,)*n)}
    # Complete flip trail 0^n to 1^n and back to 0^n.
    a=[0]*n;trail=[{'assignment':''.join(map(str,a)),'status':status(form,a)}]
    for i in list(range(n))+list(reversed(range(n))):
        old=[true_count(c,a) for c in cs];old_a=list(a);a[i]^=1
        for j,c in enumerate(cs):
            if i+1 not in {abs(v) for v in c}:continue
            orig=next(z for z in c if abs(z)==i+1)
            was_true=old_a[i]==int(orig>0)
            predicted=old[j]+(-1 if was_true else 1)
            assert predicted==true_count(c,a)
        trail.append({'flipped_variable':i+1,'assignment':''.join(map(str,a)),'status':status(form,a)})
    modes=[]
    for i in range(len(cs)):
        for j in range(i+1,len(cs)):
            observed={pair:False for pair in ('SS','SU','US','UU')}
            for a in assignments(n):
                ta,tb=true_count(cs[i],a),true_count(cs[j],a)
                aa='S' if ta==len(cs[i]) else 'U' if ta==0 else '-'
                bb='S' if tb==len(cs[j]) else 'U' if tb==0 else '-'
                if aa+bb in observed:observed[aa+bb]=True
            mat=pair_matrix(cs[i],cs[j]);assert mat==observed,(name,i,j,mat,observed)
            modes.append({'clause_indices':[i+1,j+1],'SS_SU_US_UU':mat})
    for a in assignments(n):
        b=tuple(1-v for v in a)
        sa,sb=status(form,a),status(form,b)
        for c in cs:
            assert true_count(c,a)+true_count(c,b)==len(c)
        assert sa['sat']==all(v>0 for v in sa['counts'])
    res=source_resolvents(form)
    for item in res:
        cube={int(k):v for k,v in item['cube'].items()}
        assert not exhaustive_extendible(form,cube),(name,item)
    baseline,bs=dpll(form)
    assert baseline==bool(model_list)
    controller=cold_controller(form,b=2)
    assert controller['answer']==baseline
    return {'name':name,'formula':{'variables':n,'clauses':cs,'original_dimacs':encode(form)},
       'ground_truth_sat':bool(model_list),'models':[''.join(map(str,a)) for a in model_list],
       'per_clause':[{'source_index':j+1,'clause':c,
         'S_local':{str(abs(v)):int(v>0) for v in c},
         'invert_S_to_U':{str(abs(v)):int(v<0) for v in c},
         'U_local':{str(abs(v)):int(v<0) for v in c},
         'invert_U_to_S':{str(abs(v)):int(v>0) for v in c},
         'occurrences':literal_detail(c,j+1)} for j,c in enumerate(cs)],
       'pair_compatibility':modes,'endpoints':endpoints,'flip_trail':trail,
       'resolvents_and_prohibited_cubes':res,'baseline':bs,'cold_controller':controller}

def exponent_rec(K):return max(Fraction(11,10),Fraction(3,5)+Fraction(1,2)*K)

def exponent_audit():
    out=[]
    for start in [2,4,8,16,32,100]:
        K=Fraction(start)
        trace=[]
        for j in range(30):
            nextK=exponent_rec(K)
            trace.append({'level':j,'parent_K':str(K),'per_child_scan_lower_exponent':'8/5',
                'recurrence_upper_Kprime':str(nextK),
                'strict_architecture_collision':nextK<Fraction(8,5)})
            K=nextK
            if nextK<Fraction(8,5):break
        assert trace[-1]['strict_architecture_collision']
        out.append({'initial_K':start,'levels':trace})
    return {'alpha':'11/10','gamma':'3/5','lambda':'1/2','sigma':'1/2',
            'fixed_point_K':'6/5','cold_scan_lower_exponent':'8/5',
            'first_collision_for_start':out}

def main():
    full=[]
    for name,form in cases().items():full.append(audit(form,name))
    result={'run_id':'ARC_CHILD_SCAN_AMORTIZATION272','timestamp_pdt':'2026-10-31 07:00 PDT',
       'method':'deterministic exhaustive original formulas plus symbolic Fraction exponent proof',
       'seed':None,'source_count':len(full),'sat_sources':sum(r['ground_truth_sat'] for r in full),
       'unsat_sources':sum(not r['ground_truth_sat'] for r in full),
       'original_occurrences':sum(sum(len(c) for c in r['formula']['clauses']) for r in full),
       'pair_extreme_modes':sum(4*len(r['pair_compatibility']) for r in full),
       'source_resolvents':sum(len(r['resolvents_and_prohibited_cubes']) for r in full),
       'baseline_nodes':sum(r['baseline']['nodes'] for r in full),
       'baseline_selected_events':sum(r['baseline']['selected_work'] for r in full),
       'controller_nodes':sum(r['cold_controller']['guest_nodes'] for r in full),
       'controller_selected_events':sum(r['cold_controller']['selected_total_events'] for r in full),
       'cold_source_character_reads':sum(r['cold_controller']['source_read_characters'] for r in full),
       'child_output_characters':sum(r['cold_controller']['child_write_characters'] for r in full),
       'source_cofactor_literal_visits':sum(r['cold_controller']['source_cofactor_literal_visits'] for r in full),
       'policy_selection_events':sum(r['cold_controller']['policy_selection_events'] for r in full),
       'exponent_audit':exponent_audit(),'originals':full}
    raw=json.dumps(result,sort_keys=True,indent=2)+'\n'
    path=DATA_DIR/RAW_NAME;path.write_text(raw)
    compact={k:v for k,v in result.items() if k!='originals'}
    compact['raw_sha256']=hashlib.sha256(raw.encode()).hexdigest()
    (DATA_DIR/SUMMARY_NAME).write_text(json.dumps(compact,sort_keys=True,indent=2)+'\n')
    print(json.dumps(compact,sort_keys=True,indent=2))

if __name__=='__main__':main()