#!/usr/bin/env python3
"""Independent no-producer-import verification for ARC-PAYLOAD-JUMP283.
Rebuilds source bitstreams and SAT/UNSAT certificates; replays each native
index/head/input event with full binary before/after XOR.
"""
from pathlib import Path
from collections import Counter
from itertools import product
from hashlib import sha256
from fractions import Fraction
import gzip,json

ROOT=Path(__file__).resolve().parent
checks=Counter()

def ck(condition,why):
    if not condition:raise AssertionError(why)
    checks['assertions']+=1

def make_sources():
    U=[tuple(map(int,C)) for C in json.loads((ROOT/'U_source.json').read_text())]
    V=[list(C) for C in U]
    V[1][0],V[7][0]=V[7][0],V[1][0]
    Y=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
    return {'Y6_SAT':Y,'U198_UNSAT':U,'V198_SAT':V}

def independently_encode(F):
    n=max(abs(z) for clause in F for z in clause)
    w=n.bit_length();m=len(F)
    first='1'*w+'0'+''.join(str((n>>b)&1) for b in range(w-1,-1,-1))
    rest=[]
    for clause in F:
        rest.append(str(int(clause[0]>0)))
        for literal in clause:
            v=abs(literal)-1
            rest.extend(str((v>>i)&1) for i in range(w-1,-1,-1))
    return first,''.join(rest)

def cnf_valid(F):
    n=max(abs(x) for clause in F for x in clause)
    ck(n%3==0 and len(F)==4*n//3,'target size')
    seen=set()
    c=Counter()
    for cl in F:
        ck(len(cl)==3 and len(set(map(abs,cl)))==3,'proper triple')
        ck(all(z>0 for z in cl) or all(z<0 for z in cl),'monotone')
        s=tuple(sorted(cl))
        ck(s not in seen,'no duplicate signed clause')
        seen.add(s)
        c.update(cl)
    for v in range(1,n+1):ck(c[v]==c[-v]==2,'degree 2+,2-')

def evalcl(C,a):
    return any((a[abs(l)-1]==1)==(l>0) for l in C)

def DPLL(F,stat):
    def solve(S):
        stat['nodes']+=1
        while True:
            if any(len(C)==0 for C in S):return False
            if not S:return True
            u=next((C[0] for C in S if len(C)==1),None)
            if u is None:break
            S=tuple(tuple(x for x in C if x!=-u) for C in S if u not in C)
        chosen=min(S,key=len)[0]
        for lit in (chosen,-chosen):
            Z=tuple(tuple(x for x in C if x!=-lit) for C in S if lit not in C)
            if solve(Z):return True
        return False
    return solve(tuple(tuple(x for x in C) for C in F))

def certified_labels(src,original):
    Y=src['Y6_SAT']; n=6
    model_count=sum(all(evalcl(C,a) for C in Y) for a in product((0,1),repeat=n))
    ck(model_count==20,'Y models exhaustive')
    U=src['U198_UNSAT']; V=src['V198_SAT']
    witness=tuple(int(c) for c in original['certificates']['V198_SAT']['witness'])
    ck(len(witness)==198 and all(evalcl(C,witness) for C in V),'full V198 SAT witness')
    blocks=[];exteriors=[]
    for b in range(6):
        lo=32*b+1;hi=32*(b+1)
        raw=U[2+42*b:2+42*(b+1)]
        core=[tuple(z for z in C if lo<=abs(z)<=hi) for C in raw]
        ext=tuple(sorted({z for C in raw for z in C if abs(z)>192}))
        ck(bool(ext),'each module has boundary interface')
        stats=Counter()
        ck(not DPLL(core,stats),'private module exact UNSAT')
        blocks.append(stats['nodes']);exteriors.append(ext)
    for a in product((0,1),repeat=6):
        full=[0]*192+list(a)
        ck(not evalcl(U[0],full) or not evalcl(U[1],full) or any(not any(evalcl((z,),full) for z in ext) for ext in exteriors),'all 64 boundary rows refuted')
    checks['U198_local_unsat_dpll_nodes']=blocks
    checks['Y6_model_count']=model_count
    return {'Y6_SAT':'SAT','U198_UNSAT':'UNSAT','V198_SAT':'SAT'}

def sum_binary_ones_below(n):
    out=0
    p=1
    while p<n:
        whole=n//(2*p)
        out+=whole*p+max(0,(n%(2*p))-p)
        p*=2
    return out

def check_original_indexed(sources,original):
    for name,F in sources.items():
        rec=original['sources'][name]
        ck(rec['raw_clauses']==[list(C) for C in F],'canonical original clause index source')
        n=rec['n'];m=rec['m']
        ck(n==max(abs(x) for C in F for x in C) and m==len(F),'source n,m')
        for j,C in enumerate(F,1):
            row=rec['signed_occurrence_targets'][j-1]
            for lit in C:
                x=str(abs(lit))
                ck(row['S_all_true_target'][x]==int(lit>0) and row['U_all_false_target'][x]==int(lit<0),'source S/U')
                ck(row['inverted_S'][x]==int(lit<0) and row['inverted_U'][x]==int(lit>0),'complement inversion')
        for pair in rec['clause_pair_SS_SU_US_UU']:
            j,k,*modes=pair
            A={abs(x):x>0 for x in F[j-1]};B={abs(x):x>0 for x in F[k-1]}
            shared=A.keys()&B.keys()
            same=any(A[x]==B[x] for x in shared)
            opp=any(A[x]!=B[x] for x in shared)
            ck(modes==[int(not opp),int(not same),int(not same),int(not opp)],'SS SU US UU independently')
        for s,a in [('all_zero',[0]*n),('all_one',[1]*n)]:
            hist=Counter(sum((a[abs(v)-1]==1)==(v>0) for v in C) for C in F)
            ck(rec['coherent_endpoints'][s]['buckets']==[hist[i] for i in range(4)],'consistent global extremes')
        for trail in rec['flip_and_complement_trails']:
            flip=set(trail['variable_flips'])
            a=[int(i in flip) for i in range(1,n+1)]
            b=[1-x for x in a]
            t=[sum((a[abs(v)-1]==1)==(v>0) for v in C) for C in F]
            u=[sum((b[abs(v)-1]==1)==(v>0) for v in C) for C in F]
            ck(all(x+y==3 for x,y in zip(t,u)),'complement identity')
            ck(trail['N_0_to_3']==[t.count(i) for i in range(4)],'original flip bucket')

def verify_trace(name,F):
    H,payload=independently_encode(F)
    src=H+payload
    report=json.loads((ROOT/(name+'_summary283.json')).read_text())
    n=len(src); width=n.bit_length();h=len(H)
    tape=0;idx_head=inp_head=0;total=0;erased=writes=read_count=0
    ops=Counter();sum_delta=0;covered=set();logical_delta=0
    with gzip.open(ROOT/(name+'_native_trace283.jsonl.gz'),'rt',encoding='utf-8') as f:
        for line in f:
            row=json.loads(line)
            total+=1;op=row['op'];a=row['address'];before=tape
            ck(row['step']==total,'time index')
            ck(row['before_index_bits']==format(tape,f'0{width}b'),'physical pre-state all bits')
            ck(row['before_index_head']==idx_head and row['before_input_head']==inp_head,'pre-heads')
            if op=='index_head_move_left':
                ck(idx_head>0,'left head cannot pass 0');idx_head-=1
            elif op=='index_head_move_right':
                ck(idx_head<width-1,'right head bound');idx_head+=1
            elif op=='index_write_one':
                ck(((tape>>idx_head)&1)==0,'write only blank')
                tape|=1<<idx_head;writes+=1
            elif op=='atomic_index_jump_erase':
                ck(tape==a,'index must be exact absolute binary address')
                erased+=tape.bit_count();tape=0;inp_head=a
            elif op=='input_read':
                ck(inp_head==a and h<=a<n,'ordered payload reads')
                ck(row['read_bit']==int(src[a]),'actual original source bit')
                ck(a==h+read_count,'each payload bit exactly once')
                read_count+=1;covered.add(a)
            else:raise AssertionError(op)
            diff=before^tape
            d=diff.bit_count()
            ck(row['after_index_bits']==format(tape,f'0{width}b'),'physical post-state all bits')
            ck(row['after_index_head']==idx_head and row['after_input_head']==inp_head,'post-heads')
            ck(row['d_phys']==d,'native adjacent physical popcount')
            ck(row['changed_index_cells']==[k for k in range(width) if diff&(1<<k)],'precise changed fixed cell IDs')
            ck(row['d_source_coverage']==int(op=='input_read') and row['d_logic_residual']==0,'logical type separation')
            ops[op]+=1;sum_delta+=d;logical_delta+=row['d_logic_residual']
    mathematical_sum=sum_binary_ones_below(n)-sum_binary_ones_below(h)
    ck(mathematical_sum==sum(x.bit_count() for x in range(h,n)),'independent popcount cycle formula')
    ck(read_count==len(payload)==report['payload_bits'],'all payload positions')
    ck(tape==0 and sum_delta==2*writes==2*erased==2*mathematical_sum,'exact indexed recharge/XOR')
    ck(report['sum_adjacent_d_phys']==sum_delta and report['endpoint_d_phys']==0,'physical path and endpoint')
    ck(report['native_abstract_steps']==total and report['native_event_counts']==dict(ops),'all time operations')
    ck(report['sum_adjacent_d_logic_residual']==logical_delta==0,'no residual SAT edits')
    ck(report['sum_source_coverage_delta_OFFLINE']==len(covered),'offline coverage only')
    ck(report['binary_input_sha256']==sha256(src.encode()).hexdigest(),'source hash')
    ck(report['trace_sha256']==sha256((ROOT/(name+'_native_trace283.jsonl.gz')).read_bytes()).hexdigest(),'trace bytes')
    checks['trace_steps_'+name]=total
    return {'name':name,'source_bits':n,'payload_bits':read_count,'indexed_direct_one_writes':writes,
            'indexed_erase_ones':erased,'exact_address_popcount_sum':mathematical_sum,
            'd_phys_sum':sum_delta,'d_phys_endpoint':0,'native_events':total,'event_counts':dict(ops),
            'd_logic_residual_sum':logical_delta,'offline_read_coverage':len(covered)}

def exact_envelope():
    ret=[]
    for c_str,expect in [('6/5','23/45'),('241/200','11642479/23232400')]:
        c=Fraction(c_str)
        v=[];f=Fraction(1)
        for k in range(1,4):
            f=c*f/(1+f)
            v.append(min((1/f-c)/k,c**(-k)))
        ck(str(v[1])==expect and v[1]>max(v[0],v[2],c**(-4)),'exact all-k tail exclusion')
        ret.append({'c':c_str,'d_star':expect,'k_star':2,'tail_bound':str(c**(-4))})
    return ret

def main():
    orig=json.loads((ROOT/'original_clause_controls_282.json').read_text())
    ck(sha256((ROOT/'original_clause_controls_282.json').read_bytes()).hexdigest()=='b59c55b5ad8a122b7b39d157717aaa749fe0610af8f3c991ba71650efc422687','verified prior controls SHA')
    sources=make_sources()
    for name,F in sources.items():cnf_valid(F)
    labels=certified_labels(sources,orig)
    check_original_indexed(sources,orig)
    outputs=[verify_trace(name,F) for name,F in sources.items()]
    summary={'status':'PASS','proof_status':'EXACT restricted indexed probe theorem; COMPUTATIONAL matched controls; P vs NP OPEN',
             'assertions':checks['assertions'],'certified_labels':labels,'U_local_DPLL_nodes':checks['U198_local_unsat_dpll_nodes'],
             'source_results':outputs,'FLMV':exact_envelope()}
    (ROOT/'verify_payload_jump283_results.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['status','assertions','certified_labels','U_local_DPLL_nodes']},indent=2))
if __name__=='__main__':main()
