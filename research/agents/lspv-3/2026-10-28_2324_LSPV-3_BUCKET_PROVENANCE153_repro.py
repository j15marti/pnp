#!/usr/bin/env python3
"""LSPV-3, BUCKET-PROVENANCE153: proof-carrying existential variable elimination.
Usage: python3 2026-10-28_2324_LSPV-3_BUCKET_PROVENANCE153_repro.py
No third-party modules. Verification uses independent literal-level resolution.
"""
import collections
import copy
import hashlib
import itertools
import json
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSERTIONS=0

def check(x,why):
    global ASSERTIONS
    ASSERTIONS+=1
    if not x: raise AssertionError(why)

def canonical(c):
    s=set(c)
    if any(-x in s for x in s): return None  # tautological
    return tuple(sorted(s,key=lambda x:(abs(x),x<0)))

def eval_formula(formula,assignment):
    return all(any(assignment[abs(l)]==(l>0) for l in clause) for clause in formula)

def brute(formula,n):
    for bits in itertools.product((False,True),repeat=n):
        a={i+1:bits[i] for i in range(n)}
        if eval_formula(formula,a): return a
    return None

def source_valid(F,n):
    return all(len(c)==3 and len({abs(x) for x in c})==3 and all(1<=abs(x)<=n for x in c) for c in F)

def exact22(F,n):
    c=collections.Counter(x for clause in F for x in clause)
    return source_valid(F,n) and all(c[i]==c[-i]==2 for i in range(1,n+1))

def resolution(A,B,pivot):
    """Literal-level independent checker. Parent 1 has pivot, parent 2 has -pivot."""
    if pivot not in A or -pivot not in B: raise ValueError('pivot orientations missing')
    return canonical([x for x in A if x!=pivot]+[x for x in B if x!=-pivot])

def eliminate(F,n,order=None):
    """Original source clause IDs 1..m, derived nodes with two parents and pivot."""
    if order is None: order=tuple(range(1,n+1))
    if set(order)!=set(range(1,n+1)) or len(order)!=n:raise ValueError('bad order')
    if not all(all(1<=abs(l)<=n for l in c) for c in F):raise ValueError('bad source')
    database={}; active=set(); index={}; proof=[]; buckets=[]; max_width=0; total_pairs=0
    for i,c in enumerate(F,1):
        k=canonical(c)
        if k is None:continue
        database[i]=k
        if k not in index:
            index[k]=i
            active.add(i)
    next_id=len(F)+1
    peak_live=len(active); clause_inspections=0
    for x in order:
        clause_inspections+=2*len(active)
        pos=[i for i in sorted(active) if x in database[i]]
        neg=[i for i in sorted(active) if -x in database[i]]
        bucket=pos+neg
        buckets.append(bucket)
        neighbors={abs(l) for i in bucket for l in database[i]}-{x}
        max_width=max(max_width,len(neighbors))
        after={i for i in active if i not in bucket}
        for p in pos:
            for q in neg:
                total_pairs+=1
                c=resolution(database[p],database[q],x)
                if c is None:continue
                if c in index:
                    after.add(index[c]);continue
                id=next_id;next_id+=1
                database[id]=c;index[c]=id;after.add(id)
                proof.append({'id':id,'clause':list(c),'parents':[p,q],'pivot':x})
        active=after
        peak_live=max(peak_live,len(active))
        if any(database[i]==() for i in active):
            # Continue building buckets to the end only on SAT; for UNSAT the
            # empty clause already proves the source contradiction.
            break
    empty_ids=[i for i in active if database[i]==()]
    witness=None
    if not empty_ids:
        # For this branch, all x were eliminated. Reverse reconstruct from
        # the pre-elimination bucket with assigned higher-order variables.
        witness={}
        for x,bucket in reversed(list(zip(order,buckets))):
            for choice in (False,True):
                attempt={**witness,x:choice}
                if all(any(attempt[abs(l)]==(l>0) for l in database[id]) for id in bucket):
                    witness[x]=choice
                    break
            else: raise AssertionError('projection witness reconstruction failed')
        check(eval_formula(F,witness),'constructed SAT witness must satisfy original input')
    return {'label':'UNSAT' if empty_ids else 'SAT', 'witness':witness,
            'empty_id':min(empty_ids) if empty_ids else None,
            'steps':proof,'database':database,'width':max_width,
            'pairs':total_pairs, 'peak_live':peak_live,'clause_inspections':clause_inspections,'buckets':buckets,
            'order':list(order), 'source_len':len(F)}

def verify_result(F,n,result):
    """Independent verifier only trusts original clauses and resolution nodes."""
    try:
        database={i:k for i,c in enumerate(F,1) if (k:=canonical(c)) is not None}
        used_ids=set(range(1,len(F)+1))
        for node in result['steps']:
            key=node['id'];p,q=node['parents'];pivot=node['pivot']
            if not (isinstance(key,int) and key not in used_ids and key>len(F)):
                return False
            if p not in database or q not in database:return False
            predicted=resolution(database[p],database[q],pivot)
            if predicted is None or predicted!=tuple(node['clause']):return False
            database[key]=predicted;used_ids.add(key)
        if result['label']=='UNSAT':
            return result['empty_id'] in database and database[result['empty_id']]==()
        if result['label']=='SAT':
            w=result['witness']
            return isinstance(w,dict) and set(w)==set(range(1,n+1)) and eval_formula(F,w)
        return False
    except (KeyError,TypeError,ValueError,IndexError):return False

def one_step_projection(F,n,x):
    """Canonical exact CNF after one physical variable elimination."""
    db=[canonical(c) for c in F]
    db=[c for c in db if c is not None]
    pos=[c for c in db if x in c];neg=[c for c in db if -x in c]
    rest=[c for c in db if x not in c and -x not in c]
    return tuple(sorted(set(rest+[r for a in pos for b in neg if (r:=resolution(a,b,x)) is not None]), key=lambda c:(len(c),c)))

def threecnf(F,next_var):
    """Eqsatisfiable proper three-literal gadget for all clause widths.
    Empty clause becomes all 8 clauses on 3 fresh variables.
    """
    out=[];v=next_var
    for c in F:
        if len(c)==3:out.append(tuple(c));continue
        if len(c)==0:
            q=(v,v+1,v+2);v+=3
            for bits in itertools.product((-1,1),repeat=3):
                out.append(tuple(b*a for a,b in zip(q,bits)))
            continue
        if len(c)==1:
            a=c[0];u,w=v,v+1;v+=2
            out.extend([(a,s*u,t*w) for s in (-1,1) for t in (-1,1)])
            continue
        if len(c)==2:
            u=v;v+=1;out.extend([(*c,u),(*c,-u)]);continue
        # Long clause: linear Tseitin chain, not same-arity projection.
        vars_=list(range(v,v+len(c)-3));v+=len(c)-3
        out.append((c[0],c[1],vars_[0]))
        for j in range(1,len(vars_)):
            out.append((-vars_[j-1],c[j+1],vars_[j]))
        out.append((-vars_[-1],c[-2],c[-1]))
    check(all(len(x)==3 and len({abs(q) for q in x})==3 for x in out),'3CNF physical proper')
    return tuple(out),v


def export_dimacs(F,n):
    return 'p cnf %d %d\n'%(n,len(F))+''.join(' '.join(map(str,c))+' 0\n' for c in F)

def lrat_export(trace):
    return ''.join(str(node['id'])+' '+(' '.join(map(str,node['clause']))+' ' if node['clause'] else '')+
                   '0 '+' '.join(map(str,node['parents']))+' 0\n' for node in trace['steps'])

def verify_lrat_hints(F,proof_text,require_empty=True):
    """Independent explicit RUP hint replay. Not a formally verified kernel."""
    db={i:tuple(c) for i,c in enumerate(F,1)}
    for line in proof_text.splitlines():
        ints=[int(x) for x in line.split()]
        if len(ints)<4:return False
        id=ints[0]
        if id in db or id<=len(F):return False
        try:cut=ints.index(0,1)
        except ValueError:return False
        clause=tuple(ints[1:cut]);hints=ints[cut+1:-1]
        if ints[-1]!=0 or not hints:return False
        if canonical(clause)!=clause:return False
        # Assumption negates every literal of candidate resolvent.
        values={abs(x):(x<0) for x in clause}
        if len(values)!=len(clause):return False
        conflict=False
        for h in hints:
            if h not in db:return False
            lits=db[h]
            if any(abs(l) in values and values[abs(l)]==(l>0) for l in lits):return False
            remaining=[l for l in lits if abs(l) not in values]
            if not remaining:
                conflict=True
                break
            if len(remaining)!=1:return False
            unit=remaining[0];values[abs(unit)]=unit>0
        if not conflict:return False
        db[id]=clause
    return (not require_empty) or any(c==() for c in db.values())

def minfill_order(F,n):
    graph={i:set() for i in range(1,n+1)}
    for clause in F:
        nodes={abs(x) for x in clause}
        for x in nodes: graph[x].update(nodes-{x})
    order=[]
    while graph:
        def score(x):
            nbr=graph[x]
            missing=sum(y not in graph[z] for z in nbr for y in nbr if y!=z)//2
            return (missing,len(nbr),x)
        x=min(graph,key=score)
        nbr=graph[x].copy()
        for z in nbr:
            graph[z].discard(x)
            graph[z].update(nbr-{z})
        del graph[x]
        order.append(x)
    return order

def physical_bits(F,n):
    return len(('p cnf '+str(n)+' '+str(len(F))+'\n'+''.join(' '.join(map(str,c))+' 0\n' for c in F)).encode('ascii'))*8

def signed_controls():
    U=tuple(tuple(map(int,r.split())) for r in ('-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14').split(';'))
    S=tuple(tuple(map(int,r.split())) for r in '-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'.split(';'))
    return U,S

def random_balanced_signs(scopes,n,rng):
    pos={i:set(rng.sample([p for p,c in enumerate(scopes) if i in c],2)) for i in range(1,n+1)}
    return tuple(tuple(var if pos_idx in pos[var] else -var for var in clause)
                 for pos_idx,clause in enumerate(scopes))

def report():
    audit=HERE/'archive'/'audit.py'
    original=(HERE/'archive'/'results.json').read_bytes()
    output=subprocess.check_output([sys.executable,str(audit)])
    check(output==original,'archive auditor output byte identical')
    rng=random.Random(202610282324)
    U,S=signed_controls()
    results=[]; controls={'U':U,'S':S}
    for name,F in controls.items():
        check(exact22(F,15),name+' exact22 valid')
        trace=eliminate(F,15)
        check(verify_result(F,15,trace),name+' proof verifier')
        brute_w=brute(F,15)
        check((brute_w is None)==(trace['label']=='UNSAT'),name+' independent brute')
        if name=='U':check(trace['label']=='UNSAT','U unsat')
        if name=='S':check(trace['label']=='SAT','S sat')
        stats={k:trace[k] for k in ('label','width','pairs','peak_live','empty_id','clause_inspections')}
        order2=minfill_order(F,15)
        opt=eliminate(F,15,order2)
        check(verify_result(F,15,opt),'minfill proof valid')
        if opt['label']=='UNSAT':
            proof_text=lrat_export(opt)
            check(verify_lrat_hints(F,proof_text),'minfill LRAT RUP replay')
            # Prefix that deletes a necessary hint cannot be accepted.
            lines=proof_text.splitlines()
            corrupted=lines.copy()
            part=corrupted[0].split()
            part[-2]='1000000'
            corrupted[0]=' '.join(part)
            check(not verify_lrat_hints(F,'\n'.join(corrupted)),'LRAT bad hint rejected')
            (HERE/'2026-10-28_2324_EXACT22_U_minfill.cnf').write_text(export_dimacs(F,15))
            (HERE/'2026-10-28_2324_EXACT22_U_minfill.lrat').write_text(proof_text)
        else:
            check(not verify_lrat_hints(F,lrat_export(opt)), 'SAT has no empty proof')
        check(opt['label']==trace['label'],'minfill same-instance label')
        stats.update({'minfill_width':opt['width'],'minfill_pairs':opt['pairs'],
                      'minfill_nodes':len(opt['steps']),'minfill_order':order2})
        stats['proof_nodes']=len(trace['steps'])
        results.append({'source':name,**stats})
        # Tamper with every available kind of authenticated proof field.
        if trace['steps']:
            bad=copy.deepcopy(trace);bad['steps'][0]['pivot']*=-1
            check(not verify_result(F,15,bad),'corrupt pivot rejected')
            bad=copy.deepcopy(trace);bad['steps'][0]['parents'][0]=10**9
            check(not verify_result(F,15,bad),'corrupt parent rejected')
            bad=copy.deepcopy(trace);bad['steps'][0]['clause']=[-100]
            check(not verify_result(F,15,bad),'corrupt resolvent rejected')
        bad=copy.deepcopy(trace)
        if trace['label']=='UNSAT':bad['empty_id']=-1
        else:del bad['witness'][1]
        check(not verify_result(F,15,bad),'corrupt final claim rejected')
        # Two levels of genuine ordinary 3CNF children, not necessarily shorter.
        g1=one_step_projection(F,15,1)
        t1,next1=threecnf(g1,16)
        g2=one_step_projection(g1,15,2)
        t2,next2=threecnf(g2,16)
        child1=eliminate(t1,next1-1)
        child2=eliminate(t2,next2-1)
        check(child1['label']==trace['label'] and child2['label']==trace['label'],name+' descendants truth')
        check(verify_result(t1,next1-1,child1) and verify_result(t2,next2-1,child2),'descendant proof')
        results[-1]['original_3cnf_clauses']=len(F)
        results[-1]['child_level_1_clauses']=len(t1)
        results[-1]['child_level_2_clauses']=len(t2)
        results[-1]['children_proper']=source_valid(t1,next1-1) and source_valid(t2,next2-1)
        results[-1]['input_bits']=physical_bits(F,15)
        results[-1]['child_level_1_bits']=physical_bits(t1,next1-1)
        results[-1]['child_level_2_bits']=physical_bits(t2,next2-1)
    # Diverse signed exact22 samples on identical W1 scopes; independent 2^15 brute SAT.
    scopes=tuple(tuple(abs(l) for l in c) for c in U)
    labels=collections.Counter()
    for i in range(24):
        F=random_balanced_signs(scopes,15,rng)
        check(exact22(F,15),'balanced occurrence')
        trace=eliminate(F,15)
        check(verify_result(F,15,trace),'authenticated sample')
        w=brute(F,15)
        check((w is None)==(trace['label']=='UNSAT'),'independent brute sample')
        labels[trace['label']]+=1
    # Maliciously duplicated source clauses must not multiply active bucket
    # counts beyond the 3^w distinct-clause argument.
    dup=((1,2,3),)*10+((-1,2,3),)*10
    dup_trace=eliminate(dup,3)
    check(verify_result(dup,3,dup_trace) and dup_trace['pairs']<=27,'duplicate canonical bucketing')
    check(dup_trace['label']=='SAT','duplicate SAT control')
    taut=((1,-1,2), (1,2,3))
    taut_trace=eliminate(taut,3)
    check(verify_result(taut,3,taut_trace),'source tautology safely discarded')
    # False semantic certificate: a verifier checking only listed positive
    # frontier assignments accepts empty table vacuously even for SAT F.
    F=((1,2,3),)
    claimed_empty=[]
    check(all(eval_formula(F,{1:True,2:bool(y),3:bool(z)}) for y,z in claimed_empty),
          'vacuous positive-witness-only checker accepts counterfeit UNSAT')
    exact=one_step_projection(F,3,1)
    check(not exact and brute(F,3) is not None,'actual projected relation is true')
    return {
      'title':'BUCKET-PROVENANCE153',
      'archive_audit_sha256':hashlib.sha256(original).hexdigest(),
      'archive_reproduction':True,
      'archive_counts':json.loads(original),
      'controls':results,
      'signed_exact22_samples':dict(labels),
      'counterfeit_empty_table_passes_one_sided_verification':True,
      'assertion_groups':ASSERTIONS,
      'interpretation':'Restricted proof-carrying elimination for an authenticated supplied variable order, no general SAT contraction.'
    }

if __name__=='__main__':
    out=report()
    s=json.dumps(out,sort_keys=True,indent=2)+'\n'
    (HERE/'2026-10-28_2324_BUCKET_PROVENANCE153_raw.json').write_text(s)
    print(s,end='')
