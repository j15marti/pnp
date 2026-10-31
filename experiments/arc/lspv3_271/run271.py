#!/usr/bin/env python3
"""LSPV-3 ARC271 strict22-backdoor barrier and adaptive SAT controls.
Deterministic, original-source preserving. Python event counts are not FLMV TM costs.
"""
import argparse, collections, itertools, json, math, random, time
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

HERE = Path(__file__).resolve().parent
SEED = 2711031

class Meter:
    def __init__(self): self.t=collections.Counter(); self.peak_bits=0
    def add(self, key, k=1): self.t[key]+=k
    def total(self): return sum(self.t.values())
    def as_dict(self): return dict(sorted(self.t.items()))

def orbit(k):
    assert k>=7 and k%2
    c=[]
    for i in range(k):
        for s in range(4):
            sign=1 if s<2 else -1
            c.append([sign*(i+1), sign*(k+(i+s)%k+1),sign*(2*k+(i+2*s)%k+1)])
    return {'n':3*k, 'original_clauses':c}

def scrambled(src,seed):
    rng=random.Random(seed); n=src['n']; p=list(range(1,n+1)); rng.shuffle(p)
    flip=[rng.choice([-1,1]) for _ in range(n)]
    clauses=[]
    for c in src['original_clauses']:
        row=[(1 if lit>0 else -1)*flip[abs(lit)-1]*p[abs(lit)-1] for lit in c]
        rng.shuffle(row); clauses.append(row)
    rng.shuffle(clauses)
    return {'n':n,'original_clauses':clauses,'scramble':{'permutation':p,'signs':flip}}

def prism(q,unsat=False):
    assert q%2==0 and q>=6
    h=q//2; edges=[]
    for layer in (0,1):
        for i in range(h): edges.append((layer*h+i,layer*h+(i+1)%h))
    for i in range(h): edges.append((i,h+i))
    incid={i:[] for i in range(q)}
    for e,(u,v) in enumerate(edges,1):incid[u].append(e);incid[v].append(e)
    assert all(len(v)==3 for v in incid.values())
    charges=[0]*q
    charges[0]=1
    if not unsat:charges[1]=1
    clauses=[]
    for v in range(q):
        vs=incid[v]
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2!=charges[v]:
                clauses.append([z if b==0 else -z for z,b in zip(vs,bits)])
    return {'n':len(edges),'original_clauses':clauses,'charge':charges}

def is_strict22(n,clauses):
    if any(len(c)!=3 or len({abs(x) for x in c})!=3 for c in clauses):return False
    oc=[[0,0] for _ in range(n)]
    for c in clauses:
        for lit in c:
            if not 1<=abs(lit)<=n:return False
            oc[abs(lit)-1][lit>0]+=1
    return all(a==2 and b==2 for a,b in oc)

def true_count(c, assignment):
    return sum(assignment[abs(lit)-1] == (lit>0) for lit in c)

def status(clauses,a,met=None):
    if met:met.add('clause_status_literals',sum(map(len,clauses)))
    v=[true_count(c,a) for c in clauses]
    return {'true_counts':v, 'N': [v.count(t) for t in range(4)], 'satisfied':0 not in v}

def extrema(clauses):
    out=[]
    for j,c in enumerate(clauses,1):
        s={str(abs(x)):int(x>0) for x in c}; u={str(abs(x)):int(x<0) for x in c}
        out.append({'clause_id':j,'signed_occurrences':[{'x':abs(x),'literal':x,'S':int(x>0),'invert_S':int(x<0),'U':int(x<0),'invert_U':int(x>0)} for x in c],
                    'S_all_literals_true':s,'invert_S_equals_U':u,'U_all_literals_false':u,'invert_U_equals_S':s})
    return out

def compatible(c,d,ls,rs):
    targets={abs(lit):(lit>0)==(ls=='S') for lit in c}
    for lit in d:
        v=(lit>0)==(rs=='S')
        if abs(lit) in targets and targets[abs(lit)]!=v:return False
    return True

def pair_modes(clauses,met):
    out=[]
    for i in range(len(clauses)):
        a={abs(x):int(x>0) for x in clauses[i]}
        for j in range(i+1,len(clauses)):
            b={abs(x):int(x>0) for x in clauses[j]}; shared=set(a)&set(b)
            same=any(a[v]==b[v] for v in shared); opposite=any(a[v]!=b[v] for v in shared)
            modes={p:compatible(clauses[i],clauses[j],*p) for p in ('SS','SU','US','UU')}
            assert modes['SS']==modes['UU']==(not opposite)
            assert modes['SU']==modes['US']==(not same)
            out.append({'C_i':i+1,'C_j':j+1,'shared_same':same,'shared_opposite':opposite,**modes})
            met.add('pair_compat_mode_tests',4)
    return out

def gray_trail(n,clauses,steps,met):
    a=[False]*n; out=[]
    for t in range(steps):
        mask=t^(t>>1)
        if t:
            changed=(mask^( (t-1)^((t-1)>>1))).bit_length()-1
            a[changed]=not a[changed]
        else:changed=None
        x=status(clauses,a,met)
        out.append({'step':t,'gray_mask':mask,'flipped_var':changed+1 if changed is not None else None,'N':x['N'],'satisfied':x['satisfied']})
    return out

def resolve_one(clauses,met):
    for i,c in enumerate(clauses):
        for j in range(i+1,len(clauses)):
            d=clauses[j]; met.add('resolvent_pair_scans',len(c)+len(d))
            for lit in c:
                if -lit in d:
                    R=list(dict.fromkeys([z for z in c if z!=lit]+[z for z in d if z!=-lit]))
                    if any(-z in R for z in R):continue
                    if len(R)>5:continue
                    cube={str(abs(z)):int(z<0) for z in R}
                    # A resolvent is entailed by its two parents; fully verify locally.
                    vars_=sorted({abs(z) for z in c+d})
                    for bits in itertools.product((False,True),repeat=len(vars_)):
                        a=dict(zip(vars_,bits))
                        sc=lambda cl:any(a[abs(z)]==(z>0) for z in cl)
                        assert not (sc(c) and sc(d) and not sc(R))
                    return {'from_C': [i+1,j+1], 'pivot':abs(lit),'resolvent':R,'forbidden_cube':cube,'proof':'single non-tautological resolution step'}
    return None

def integer_backdoor(n,clauses,typ):
    rows=[];rhs=[]
    for c in clauses:
        if typ=='Krom': vars_=[abs(x) for x in c]; k=max(0,len(c)-2)
        elif typ=='Horn': vars_=[abs(x) for x in c if x>0]; k=max(0,len(vars_)-1)
        else: vars_=[abs(x) for x in c if x<0]; k=max(0,len(vars_)-1)
        if k:
            row=[0.0]*n
            for v in vars_:row[v-1]=1.0
            rows.append(row); rhs.append(k)
    if not rows:return {'size':0,'set':[],'mip_gap':0,'rows':0,'elapsed_seconds':0}
    t=time.perf_counter()
    A=np.array(rows,dtype=float)
    result=milp(c=np.ones(n),integrality=np.ones(n,dtype=int),bounds=Bounds(np.zeros(n),np.ones(n)),
                constraints=LinearConstraint(A,np.array(rhs),np.full(len(rhs),np.inf)),
                options={'time_limit':12.0,'mip_rel_gap':0})
    elapsed=time.perf_counter()-t
    if result.x is None or result.status!=0:
        return {'solver_status':int(result.status),'rows':len(rows),'elapsed_seconds':round(elapsed,5)}
    picked=[i+1 for i,z in enumerate(result.x) if z>0.5]
    assert all(sum(v in picked for v in [i+1 for i,a in enumerate(row) if a])>=k for row,k in zip(rows,rhs))
    return {'size':len(picked),'set':picked,'rows':len(rows),'mip_gap':float(result.mip_gap),
            'solver_status':int(result.status),'elapsed_seconds':round(elapsed,5)}

def simplify(clauses,assign,met):
    out=[]
    for j,c in enumerate(clauses):
        met.add('dpll_literal_reads',len(c))
        alive=[]; satisfied=False
        for lit in c:
            v=assign.get(abs(lit))
            if v is None:alive.append(lit)
            elif v==(lit>0):satisfied=True;break
        if not satisfied:
            if not alive:return None,j
            out.append((j,alive))
    return out,None

def propagate(clauses,partial,met):
    a=dict(partial)
    while True:
        active,conf=simplify(clauses,a,met)
        if conf is not None:return a,conf,[]
        units=[(j,c[0]) for j,c in active if len(c)==1]
        met.add('unit_candidates_examined',len(active))
        if not units:return a,None,active
        changed=False
        for j,lit in units:
            val=lit>0;v=abs(lit)
            if v in a:
                if a[v]!=val:return a,j,[]
                continue
            a[v]=val;changed=True;met.add('unit_assignments')
        if not changed:return a,None,active

def dpll(n,clauses,policy='first',node_limit=200000):
    met=Meter(); nodes=0;root=None
    def rec(partial):
        nonlocal nodes
        nodes+=1;met.add('dpll_nodes')
        if nodes>node_limit:return 'LIMIT',None,None
        a,conf,active=propagate(clauses,partial,met)
        if conf is not None:return 'UNSAT',None,{'conflict_clause':conf+1,'decisions':[[k,int(v)] for k,v in sorted(partial.items())]}
        if not active:
            candidate=[a.get(i,False) for i in range(1,n+1)]
            assert all(true_count(c,candidate)>=1 for c in clauses)
            met.add('witness_validation_literals',sum(len(c) for c in clauses))
            return 'SAT',candidate,None
        if policy=='max':
            cnt=collections.Counter(abs(l) for _,c in active for l in c if abs(l) not in a)
            met.add('branch_policy_candidates',sum(map(len,(c for _,c in active))))
            v=min([z for z,val in cnt.items() if val==max(cnt.values())])
        else:v=min(abs(l) for _,c in active for l in c if abs(l) not in a)
        c1=dict(a);c1[v]=False
        label,model,proof0=rec(c1)
        if label=='SAT' or label=='LIMIT':return label,model,None
        c2=dict(a);c2[v]=True
        label,model,proof1=rec(c2)
        if label=='SAT' or label=='LIMIT':return label,model,None
        return 'UNSAT',None,{'branch_var':v,'low':proof0,'high':proof1,'decisions':[[k,int(val)] for k,val in sorted(partial.items())]}
    label,model,proof=rec({})
    return {'label':label,'model':[int(v) for v in model] if model is not None else None,'nodes':nodes,'events':met.as_dict(),
            'total_events':met.total(),'proof':proof}

def horn_solve(n,clauses,dual=False,met=None):
    F=[[-x for x in c] if dual else c for c in clauses];truth=set()
    for loop in range(n+1):
        changed=False
        for c in F:
            if met:met.add('horn_literal_reads',len(c))
            neg=[abs(z) for z in c if z<0];pos=[z for z in c if z>0]
            if not all(z in truth for z in neg):continue
            if not pos:return 'UNSAT',None
            if pos[0] not in truth:truth.add(pos[0]);changed=True
        if not changed:break
    cand=[(i in truth)^dual for i in range(1,n+1)]
    assert all(true_count(c,cand)>0 for c in clauses)
    return 'SAT',[int(z) for z in cand]

def twosat(n,clauses,met):
    edges=[[] for _ in range(2*n)]; rev=[[] for _ in range(2*n)]
    def node(lit):return 2*(abs(lit)-1)+(0 if lit>0 else 1)
    def edge(a,b):
        u,v=node(a),node(b);edges[u].append(v);rev[v].append(u);met.add('scc_edge_writes')
    for c in clauses:
        met.add('scc_source_literal_reads',len(c))
        if len(c)==0:return 'UNSAT',None
        if len(c)==1:edge(-c[0],c[0]);continue
        assert len(c)==2
        a,b=c;edge(-a,b);edge(-b,a)
    seen=set(); order=[]
    def dfs(v):
        seen.add(v)
        for w in edges[v]:
            met.add('scc_edge_visits')
            if w not in seen:dfs(w)
        order.append(v)
    for v in range(2*n):
        if v not in seen:dfs(v)
    comp=[-1]*(2*n)
    def dfs2(v,k):
        comp[v]=k
        for w in rev[v]:
            met.add('scc_reverse_visits')
            if comp[w]<0:dfs2(w,k)
    count=0
    for v in reversed(order):
        if comp[v]<0:dfs2(v,count);count+=1
    if any(comp[2*i]==comp[2*i+1] for i in range(n)):return 'UNSAT',None
    cand=[comp[2*i]>comp[2*i+1] for i in range(n)]
    assert all(true_count(c,cand)>0 for c in clauses)
    return 'SAT',[int(v) for v in cand]

def xor_recognizer(n,clauses,met):
    groups=collections.defaultdict(list)
    for c in clauses:
        met.add('xor_literal_reads',len(c))
        if len(c)!=3 or len(set(map(abs,c)))!=3:return None
        groups[tuple(sorted(map(abs,c)))].append(c)
    eq=[]
    for vars_,block in groups.items():
        if len(block)!=4:return None
        bad=[]
        for c in block:
            wanted={abs(v):int(v<0) for v in c}
            bad.append(tuple(wanted[v] for v in vars_))
        if len(set(bad))!=4 or len({sum(x)%2 for x in bad})!=1:return None
        rhs=1-sum(bad[0])%2
        mask=sum(1<<(v-1) for v in vars_);eq.append([mask,rhs])
    pivot={}
    for mask,rhs in eq:
        while mask:
            col=mask.bit_length()-1;met.add('gaussian_row_ops')
            if col not in pivot:pivot[col]=(mask,rhs);break
            mask^=pivot[col][0];rhs^=pivot[col][1]
        else:
            if rhs:return 'UNSAT',None,{'type':'GF2 contradiction','equations':len(eq),'rank':len(pivot)}
    x=0
    for col,(mask,rhs) in sorted(pivot.items()):
        par=((x&(mask^(1<<col))).bit_count())%2
        if rhs^par:x|=1<<col
    cand=[int(bool(x&(1<<i))) for i in range(n)]
    assert all(true_count(c,cand)>0 for c in clauses)
    return 'SAT',cand,{'type':'GF2 source-authenticated','equations':len(eq),'rank':len(pivot)}

def cheap_controller(n,clauses,canonical_k=None,source_witness=None):
    """Three stages: coherent endpoints, paid exact recognition, bounded repair/fallback.
    A syntactic strict22 gate avoids repeated Gray probes after failed recognition.
    The gate is a heuristic budget, NOT evidence of hardness or UNSAT.
    """
    met=Meter(); phases=[];zero=[False]*n;one=[True]*n
    for label,a in [('ZERO',zero),('ONE',one)]:
        r=status(clauses,a,met);phases.append({'name':label,'N':r['N'],'sat':r['satisfied']})
        if r['satisfied']:
            met.add('witness_validation_literals',sum(map(len,clauses)))
            return {'label':'SAT','model':[int(x) for x in a],'method':label,'phases':phases,
                    'nodes':0,'events':met.as_dict(),'total_events':met.total()}
    met.add('class_discovery_literal_reads',sum(map(len,clauses)))
    lab,model,method=None,None,None
    if all(len(c)<=2 for c in clauses):
        lab,model=twosat(n,clauses,met);method='2SAT-SCC'
    elif all(sum(x>0 for x in c)<=1 for c in clauses):
        lab,model=horn_solve(n,clauses,False,met);method='HORN'
    elif all(sum(x<0 for x in c)<=1 for c in clauses):
        lab,model=horn_solve(n,clauses,True,met);method='DUALHORN'
    else:
        found=xor_recognizer(n,clauses,met)
        if found:
            lab,model,_=found;method='XOR-GE'
        elif canonical_k is not None:
            met.add('canonical_source_literal_reads',sum(map(len,clauses)))
            if clauses==orbit(canonical_k)['original_clauses']:
                model=[1]*canonical_k+[0]*(2*canonical_k)
                lab='SAT';method='CANONICAL-ORBIT'
        if lab is None and source_witness is not None:
            met.add('source_witness_validation_literals',sum(map(len,clauses)))
            if all(true_count(c,source_witness)>0 for c in clauses):
                lab,model='SAT',[int(z) for z in source_witness]
                method='SOURCE-SUPPLIED-WITNESS'
    nodes=0
    if lab is None:
        # Post-recognition speculative repairs have no UNSAT authority.
        if is_strict22(n,clauses):
            met.add('policy_gate_strict22_scans',sum(map(len,clauses)))
            met.add('policy_skipped_gray')
        else:
            for t in range(1,min(2*n+1,2**min(n,8))):
                mask=t^(t>>1);a=[bool(mask&(1<<i)) for i in range(n)]
                r=status(clauses,a,met);met.add('failed_gray_candidates')
                if r['satisfied']:
                    lab,model,method='SAT',[int(x) for x in a],'GRAY'
                    break
        if lab is None:
            d=dpll(n,clauses,policy='max')
            lab,model,method=d['label'],d['model'],'UP-DPLL-MAX'
            met.t.update(d['events']);nodes=d['nodes']
    if lab=='SAT':
        assert all(true_count(c,model)>0 for c in clauses)
        met.add('witness_validation_literals',sum(map(len,clauses)))
    return {'label':lab,'model':model,'method':method,'phases':phases,
            'nodes':nodes,'events':met.as_dict(),'total_events':met.total()}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default=str(HERE/'raw271.json'));args=ap.parse_args()
    fixtures=json.loads((HERE/'fixtures271.json').read_text())
    cases={k:v for k,v in fixtures.items()};
    cases['KROM_BOTH_ENDS_FAIL_SAT']={'n':2,'original_clauses':[[1,2],[-1,-2]]}
    cases['HORN_BOTH_ENDS_FAIL_SAT']={'n':3,'original_clauses':[[1],[-1,-2,3],[-3]]}
    cases['HORN_WIDTH3_UNSAT']={'n':3,'original_clauses':[[1],[2],[-3],[-1,-2,3]]}
    for k in (7,9,11):cases[f'ORBIT_K{k}_SAT']=orbit(k)
    cases['ORBIT_K7_SCRAMBLED_SAT']=scrambled(orbit(7),SEED)
    cases['PRISM_Q6_SAT']=prism(6,False);cases['PRISM_Q6_UNSAT']=prism(6,True)
    raw={'seed':SEED,'model':'source-authenticated proper-CNF, host-language events only','cases':{},'solver_limits':{'node_limit':200000},'formulas_sources':cases}
    for label,rec in cases.items():
        n=rec['n'];clauses=rec['original_clauses'];met=Meter()
        assert all(all(1<=abs(l)<=n for l in c) and len({abs(l) for l in c})==len(c) for c in clauses)
        is22=is_strict22(n,clauses)
        r={'n':n,'m':len(clauses),'strict22':is22,'source_extrema':extrema(clauses),
           'pair_compatibility':pair_modes(clauses,met),'forbidden_resolvent':resolve_one(clauses,met),
           'endpoints':{'ZERO':status(clauses,[False]*n,met),'ONE':status(clauses,[True]*n,met)},
           'gray_trail':gray_trail(n,clauses,min(2*n+1,2**min(n,6)),met)}
        r['complement_checks']=[]
        for i in range(min(24,2**min(n,6))):
            a=[bool((i^(i>>1))&(1<<v)) for v in range(n)]
            u=status(clauses,a,met)['N'];v=status(clauses,[not z for z in a],met)['N']
            
            if all(len(c)==3 for c in clauses):assert u==list(reversed(v))
            else:
                for c in clauses:assert true_count(c,a)+true_count(c,[not z for z in a])==len(c)
            r['complement_checks'].append({'mask':i^(i>>1),'N':u,'Ncomplement':v})
        if n<=15:
            count=0
            for mask in range(1<<n):
                a=[bool(mask&(1<<i)) for i in range(n)]
                if all(true_count(c,a)>0 for c in clauses):count+=1
            r['exact_models']=count
        else:r['exact_models']=None
        if is22:
            m=len(clauses)
            assert m*3==4*n
            r['backdoors']={x:integer_backdoor(n,clauses,x) for x in ('Krom','Horn','DualHorn')}
            r['analytic_lb']={'Krom':math.ceil(m/4),'Horn':math.ceil(n/3),'DualHorn':math.ceil(n/3)}
            assert all(z.get('size',10**10)>=r['analytic_lb'][name] for name,z in r['backdoors'].items())
            r['explicit_pair_flags_bits']=2*m*(m-1)
            r['explicit_status_bits']=2*m
            r['serialization_bits']=3*m*(1+math.ceil(math.log2(n+1)))+2*math.ceil(math.log2(n+m+2))
        if n<=21:
            r['baseline']=dpll(n,clauses,policy='max')
            assert r['baseline']['label']!='LIMIT', (label,r['baseline']['nodes'])
        else:r['baseline']=None
        k=int(label.split('_K')[1].split('_')[0]) if label.startswith('ORBIT_K') and 'SCRAMBLED' not in label else None
        r['controller']=cheap_controller(n,clauses,canonical_k=k)
        if r['baseline']:assert r['baseline']['label']==r['controller']['label'],label
        if r['exact_models'] is not None:assert (r['exact_models']>0)==(r['controller']['label']=='SAT'),label
        if label.startswith('ORBIT_K'):
            if 'SCRAMBLED' in label:
                s=rec['scramble'];k=7;initial=[1]*k+[0]*2*k;w=[0]*n
                for i in range(n):w[s['permutation'][i]-1]=initial[i] if s['signs'][i]>0 else 1-initial[i]
            else:
                w=[1]*(n//3)+[0]*(2*n//3)
            r['source_known_witness_cost_literals']=sum(map(len,clauses))
            assert all(true_count(c,w)>0 for c in clauses)
        r['diagnostic_events']=met.as_dict()
        r['with_audit_events']=met.total()+r['controller']['total_events']
        raw['cases'][label]=r
        bd={name:v.get('size') for name,v in r.get('backdoors',{}).items()}
        print(label,'strict22',is22,'models',r['exact_models'],'backdoors',bd,'base_nodes',r['baseline']['nodes'] if r['baseline'] else None,'controller',r['controller']['method'],'label',r['controller']['label'])
    out=Path(args.output);out.write_text(json.dumps(raw,sort_keys=True,indent=2)+'\n')
    print('WROTE',out,'bytes',out.stat().st_size)
    compact={k:{'n':v['n'],'m':v['m'],'label':v['controller']['label'],'model_count':v['exact_models'],'backdoors':v.get('backdoors'),
                'analytic_lb':v.get('analytic_lb'),'baseline_nodes':v['baseline']['nodes'] if v['baseline'] else None,
                'baseline_events':v['baseline']['total_events'] if v['baseline'] else None,'controller_nodes':v['controller']['nodes'],
                'controller_events':v['controller']['total_events'],'controller_method':v['controller']['method'],
                'explicit_pair_flags_bits':v.get('explicit_pair_flags_bits'),'serialization_bits':v.get('serialization_bits'),'with_audit_events':v['with_audit_events']} for k,v in raw['cases'].items()}
    (HERE/'summary271.json').write_text(json.dumps({'seed':SEED,'cases':compact},indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
