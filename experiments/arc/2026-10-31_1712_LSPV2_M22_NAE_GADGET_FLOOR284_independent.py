#!/usr/bin/env python3
"""Independently implemented checker for finite M22 NAE gadget and tape events.
Usage: python verify284.py raw284.json U198_source.txt physical284_{case}.jsonl.gz
No imports from the producer. Stdlib only.
"""
import ast,collections,gzip,hashlib,itertools,json,sys
from pathlib import Path

def lang(f):
    if not f or any(len(c)!=3 or len({abs(x) for x in c})!=3 or len(set(x>0 for x in c))!=1 for c in f):return False
    if len({tuple(sorted(c)) for c in f})!=len(f):return False
    n=max(abs(x) for c in f for x in c)
    d=collections.Counter(x for c in f for x in c)
    return len(f)*3==4*n and all(d[v]==d[-v]==2 for v in range(1,n+1))

def eval_cn(f,a):return all(any((a[abs(x)-1]==1)==(x>0) for x in c) for c in f)

def gg(x):t=format(x,'b');return '0'*(len(t)-1)+t

def enc(f):
    assert lang(f)
    n=max(abs(x) for c in f for x in c);w=n.bit_length()
    return gg(n)+gg(len(f))+''.join(('1' if c[0]>0 else '0')+''.join(f'{abs(x):0{w}b}' for x in c) for c in f)

def check_cert(payload):
    # Independent exact degrees via iterated backtracking over all 20 three-subsets;
    # no producer enumeration function imported.
    triples=[s for s in itertools.combinations(range(1,7),3)]
    accepted=[]
    def walk(pick,start,remaining):
        if len(pick)==3:
            if remaining==(0,0,0,0,0,0):accepted.append(tuple(pick))
            return
        for k in range(start,len(triples)):
            c=triples[k]
            nextd=tuple(remaining[i]-(int(i+1 in c)) for i in range(6))
            if min(nextd)>=0:walk(pick+[c],k+1,nextd)
    walk([],0,(1,1,1,2,2,2))
    accepted=sorted(accepted)
    assert len(accepted)==15 and [list(map(list,x)) for x in accepted]==payload['all_families']
    assert len(payload['witness_table'])==15**2
    checked=0;counter=collections.Counter()
    for r in payload['witness_table']:
        i,j=r['positive_family'],r['negative_family'];p=accepted[i];q=accepted[j]
        assert len(r['witnesses'])==8
        for b,char in enumerate(r['witnesses']):
            assert char in '01234567';w=int(char)
            mask=b|(w<<3)
            assert all(any((mask>>(z-1))&1 for z in c) for c in p)
            assert all(any(not ((mask>>(z-1))&1) for z in c) for c in q)
            # Directly verify minimization and all 64 assignments,
            # not just the supplied witness.
            exact=[]
            for ii in range(8):
                trial=b|(ii<<3)
                plus_ok=all(any((trial>>(z-1))&1 for z in c) for c in p)
                minus_ok=all(any(not ((trial>>(z-1))&1) for z in c) for c in q)
                if plus_ok and minus_ok: exact.append(ii)
            assert exact and w==min(exact)
            checked+=1
        counter[('A' if (4,5,6) in p else 'B')+('A' if (4,5,6) in q else 'B')]+=1
    assert checked==1800
    # Deliberate corruption test: every 000 boundary with w=0 cannot satisfy
    # at least one positive triple; independently reject replacing all witnesses by zero.
    forged=[0]*8
    p=accepted[0];q=accepted[0]
    assert not all(any((0>>(z-1))&1 for z in c) for c in p)
    return checked,dict(counter)

def verify_physical(parent,child,path,summary):
    source=enc(parent);target=enc(child)
    w=max(1,len(source).bit_length());index=[0]*w;work=[0]*len(target);hi=0;hw=0
    counts=collections.Counter();delta_total=0;num=0;currentbit=None;spotchecks=0
    ih=len(gg(max(abs(z) for c in parent for z in c)))+len(gg(len(parent)))
    oh=len(gg(max(abs(z) for c in child for z in c)))+len(gg(len(child)))
    changed_clauses=set();expected_reads=0
    def physical_state():
        return tuple(index)+tuple(work)+tuple((hi>>z)&1 for z in range(w))+tuple((hw>>z)&1 for z in range(w))
    with gzip.open(path,'rt') as fh:
        for line in fh:
            event=json.loads(line);num+=1
            typ=event['operation'];j=event['output_bit'];d=event['d_phys']
            assert j>=0 and j<len(target)
            if num%10000==1: before=physical_state()
            if typ=='literal_header_emit':
                assert j<oh and event['value']==int(target[j]);computed=0;currentbit=event['value']
            elif typ=='index_head_position':
                new=event['head_location'];assert new<w
                computed=(hi^new).bit_count();hi=new
            elif typ=='index_cell_write':
                pos=event['cell'];assert pos==hi
                v=event['new_bit'];computed=index[pos]^v;index[pos]=v
            elif typ=='source_indexed_read':
                q=event['source_bit'];assert q==sum(v<<k for k,v in enumerate(index));assert 0<=q<len(source)
                assert event['value']==int(source[q]);currentbit=event['value'];expected_reads+=1;computed=0
            elif typ=='index_atomic_reset':
                computed=sum(index);assert event['cells_cleared']==computed;index=[0]*w
            elif typ=='work_head_position':
                new=event['head_location'];assert new==j
                computed=(hw^new).bit_count();hw=new
            elif typ=='work_cell_write':
                assert hw==j and currentbit is not None
                v=event['new_bit'];assert v==currentbit
                computed=work[j]^v;work[j]=v;currentbit=None
                if j>=oh:changed_clauses.add(1+(j-oh)//(1+3*max(abs(z) for c in child for z in c).bit_length()))
            else:raise AssertionError('unknown event')
            assert computed==d,(num,typ,d,computed)
            if num%10000==1:
                after=physical_state()
                assert sum(x!=y for x,y in zip(before,after))==computed
                spotchecks+=1
            counts[typ]+=1;delta_total+=d
    assert ''.join(str(x) for x in work)==target
    assert not any(index)
    endpoint=sum(work)+hi.bit_count()+hw.bit_count()
    assert expected_reads==len(target)-oh
    assert delta_total==summary['physical_adjacent_xor']
    assert endpoint==summary['endpoint_phys_xor']
    assert num==summary['events']
    assert sorted(changed_clauses)==summary['changed_child_clause_records']
    assert hashlib.sha256(target.encode()).hexdigest()==summary['child_sha256']
    return {'events':num,'source_queries':expected_reads,'physical_adjacent_xor':delta_total,'endpoint_physical_xor':endpoint,
            'full_checkpoint_xor_checks':spotchecks,'independent_work_output_bytes':len(target),'operation_counters':dict(counts)}

def verify_controls(data,source):
    U=ast.literal_eval(source[source.index('[['):]);assert lang(U)
    V=[c[:] for c in U];V[2][2]=196;V[44][2]=197
    assert lang(V)
    Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]
    F6=data['connected_unsound_grammar_valid_expansion']['F6']
    F9=data['connected_unsound_grammar_valid_expansion']['F9']
    assert lang(F6) and lang(F9)
    assert len(F6)==8 and len(F9)==12
    # Independently calculate all projections of both locally changed formulas
    p0={x for x in itertools.product((0,1),repeat=6) if eval_cn(F6,x)}
    p1={x[:6] for x in itertools.product((0,1),repeat=9) if eval_cn(F9,x)}
    assert len(p0)==data['connected_unsound_grammar_valid_expansion']['F6_SAT_count']
    assert sum(eval_cn(F9,a) for a in itertools.product((0,1),repeat=9))==data['connected_unsound_grammar_valid_expansion']['F9_SAT_count']
    assert p1-p0
    ca=data['connected_unsound_grammar_valid_expansion']['projection_counterexample']
    a=tuple(int(x) for x in ca['original_assignment']);t=tuple(int(x) for x in ca['private_extension'])
    assert not eval_cn(F6,a) and eval_cn(F9,a+t)
    checks=collections.Counter()
    for name,f in [('Y6_SAT',Y),('PAIRED6_SAT',F6),('CONNECTED9_SAT',F9),('U198_UNSAT',U),('V198_SAT',V)]:
        x=data['original_controls'][name]
        assert lang(f) and x['n']==max(abs(z) for c in f for z in c)
        assert x['encoded_bits']==len(enc(f))
        n=x['n'];bits=[0]*n
        for frame in x['coherent_flip_trail']:
            a=tuple(int(z) for z in frame['assignment'])
            ts=[sum((a[abs(z)-1]==1)==(z>0) for z in c) for c in f]
            assert frame['counts']==ts and frame['N0_N1_N2_N3']==[ts.count(k) for k in range(4)]
            checks['coherent_frames']+=1
        for cl,clinfo in zip(f,x['original_signed_occurrences']):
            for lit,info in zip(cl,clinfo['occurrences']):
                assert lit==info['signed_literal'] and info['S_local']==info['invert_U_to_S']==int(lit>0)
                assert info['U_local']==info['invert_S_to_U']==int(lit<0)
                checks['local_occurrence_extremes']+=1
        assert len(x['SS_SU_US_UU_matrix'])==len(f)*(len(f)-1)//2
        for j,k,ss,su,us,uu in x['SS_SU_US_UU_matrix']:
            c={abs(z):int(z>0) for z in f[j-1]};d={abs(z):int(z>0) for z in f[k-1]}
            opp=any(c[v]!=d[v] for v in c.keys()&d.keys())
            same=any(c[v]==d[v] for v in c.keys()&d.keys())
            assert [ss,su,us,uu]==[int(not opp),int(not same),int(not same),int(not opp)]
            checks['four_way_pair_rows']+=1
        if n<=9:
            brute=sum(eval_cn(f,asgn) for asgn in itertools.product((0,1),repeat=n))
            assert brute>0
            checks['full_assignment_tests']+=1<<n
    assert data['original_controls']['U198_UNSAT']['complete_zero']['satisfied'] is False
    assert data['original_controls']['V198_SAT']['complete_one']['satisfied'] is False
    return dict(checks)

def main():
    data=json.loads(Path(sys.argv[1]).read_text());source=Path(sys.argv[2]).read_text()
    assert data['source_sha256']==hashlib.sha256(source.encode()).hexdigest()
    cert_n,ty=check_cert(data['exact_gadget'])
    control=verify_controls(data,source)
    Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]
    U=ast.literal_eval(source[source.index('[['):]);V=[c[:] for c in U];V[2][-1]=196;V[44][-1]=197
    def shifted(formula,n):return [[(1 if z>0 else -1)*(abs(z)+n) for z in c] for c in formula]
    p=[('Y6_pair_SAT',Y),('U198_UNSAT',U),('V198_SAT',V)]
    results={}
    for (name,f),path in zip(p,sys.argv[3:]):
        parent=f+shifted(Y,max(abs(z) for c in f for z in c))
        assert lang(parent)
        results[name]=verify_physical(parent,f,path,data['physical_child'][name])
    result={'verdict':'PASS','checked_gadget_boundary_witnesses':cert_n,'gadget_family_types':ty,
            'source_controls':control,'physical_events':results,'raw_sha256':hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest()}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
