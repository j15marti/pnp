#!/usr/bin/env python3
"""LSPV-2 M22-NAE-GADGET284: exact finite boundary obstruction and charged XOR.
stdlib only.  python m22_gadget284.py U198_source.txt raw284.json trace284.jsonl.gz
"""
import ast, collections, gzip, hashlib, itertools, json, math, pathlib, sys
B=(1,2,3); I=(4,5,6)
P6=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
Q6=P6
Y6Q=((1,2,4),(1,3,6),(2,3,5),(4,5,6))
WITNESS_V='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'

def valid(f):
    if not f:return False
    try:
        if any(len(c)!=3 or len(set(map(abs,c)))!=3 or len(set(z>0 for z in c))!=1 or any(type(z)!=int or z==0 for z in c) for c in f):return False
        if len({tuple(sorted(c)) for c in f})!=len(f):return False
        n=max(abs(z) for c in f for z in c)
        if 3*len(f)!=4*n:return False
        counts=collections.Counter((abs(z),z>0) for c in f for z in c)
        return all(counts[v,True]==counts[v,False]==2 for v in range(1,n+1))
    except Exception:return False

def sat(f,a):return all(any(bool(a[abs(z)-1])==(z>0) for z in c) for c in f)
def make_y(p=P6,q=Y6Q):return [list(c) for c in p]+[[-z for z in c] for c in q]
def masks(f,a):return [sum(bool(a[abs(z)-1])==(z>0) for z in c) for c in f]
def hist(t):return [t.count(r) for r in range(4)]
def gamma(k):
    z=format(k,'b');return '0'*(len(z)-1)+z

def encode(f):
    assert valid(f)
    n=max(abs(z) for c in f for z in c)
    w=n.bit_length()
    return gamma(n)+gamma(len(f))+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(z),f'0{w}b') for z in c) for c in f)

def fams():
    triples=list(itertools.combinations(range(1,7),3))
    out=[]
    for cs in itertools.combinations(triples,3):
        if tuple(sum(v in c for c in cs) for v in range(1,7))==(1,1,1,2,2,2):out.append(cs)
    return out

def family_sat(p,q,b,i):
    mask=b|(i<<3)
    return all(any(mask&(1<<(v-1)) for v in c) for c in p) and all(any(not (mask&(1<<(v-1))) for v in c) for c in q)

def gadgets():
    fam=fams();rows=[];types=collections.Counter();exhaust=0
    for pidx,p in enumerate(fam):
        for qidx,q in enumerate(fam):
            wins=[]
            for b in range(8):
                vals=[i for i in range(8) if family_sat(p,q,b,i)]
                assert vals,(p,q,b)
                wins.append(min(vals));exhaust+=8
            rows.append({'positive_family':pidx,'negative_family':qidx,'witnesses':''.join(str(i) for i in wins)})
            types['P'+('A' if (4,5,6) in p else 'B')+'Q'+('A' if (4,5,6) in q else 'B')]+=1
    assert len(fam)==15 and len(rows)==225 and exhaust==14400
    return fam,rows,dict(types)

def degree_tag(f):
    return [{'clause_id':j+1,'occurrences':[{'variable':abs(z),'signed_literal':z,'S_local':int(z>0),'invert_S_to_U':int(z<0),'U_local':int(z<0),'invert_U_to_S':int(z>0)} for z in c]} for j,c in enumerate(f)]

def compatible(f):
    out=[]
    for j in range(len(f)):
        a={abs(z):int(z>0) for z in f[j]}
        for k in range(j+1,len(f)):
            b={abs(z):int(z>0) for z in f[k]}
            same=any(a[v]==b[v] for v in a.keys()&b.keys())
            opp=any(a[v]!=b[v] for v in a.keys()&b.keys())
            out.append([j+1,k+1,int(not opp),int(not same),int(not same),int(not opp)])
    return out

def logical_frame(f,a):
    t=masks(f,a)
    return {'assignment':''.join(map(str,a)),'counts':t,'N0_N1_N2_N3':hist(t),'satisfied':all(z>0 for z in t)}

def logical_bits(frame,style):
    a=frame['assignment'];counts=frame['counts'];return a+''.join(format((z^(z>>1)) if style=='gray' else z,'02b')+str(int(z>0)) for z in counts)

def trail(f):
    n=max(abs(z) for c in f for z in c)
    a=[0]*n;frames=[logical_frame(f,a)];flips=[]
    for v in ([1,2,3]+([4] if n>=4 else [])+[n]):
        if v in flips:continue
        prev=frames[-1];a[v-1]^=1
        nxt=logical_frame(f,a)
        ch=[j+1 for j,(x,y) in enumerate(zip(prev['counts'],nxt['counts'])) if x!=y]
        frames.append(nxt);flips.append(v)
        nxt['from_previous']={'flip_variable':v,'changed_source_clause_ids':ch,'delta_logic_gray':sum(x!=y for x,y in zip(logical_bits(prev,'gray'),logical_bits(nxt,'gray'))),'delta_logic_binary':sum(x!=y for x,y in zip(logical_bits(prev,'binary'),logical_bits(nxt,'binary')))}
    frames.append(logical_frame(f,[1]*n));frames[-1]['from_previous']={'operation':'complete_global_ones','is_single_flip':False}
    return frames

def full_pair_verify_small(f,pairs):
    ok=0
    for j,k,ss,su,us,uu in pairs:
        c=f[j-1];d=f[k-1];vs=sorted({abs(z) for z in c+d})
        table=[]
        for target_c,target_d in ((1,1),(1,0),(0,1),(0,0)):
            feasible=any(all(((b>>(vs.index(abs(z))))&1)==(int(z>0) if mode else int(z<0)) for cc,mode in ((c,target_c),(d,target_d)) for z in cc) for b in range(1<<len(vs)))
            table.append(int(feasible))
        assert table==[ss,su,us,uu]
        ok+=4
    return ok

def dpll(f):
    n=max(abs(z) for c in f for z in c)
    counts=collections.Counter()
    def solve(a):
        counts['nodes']+=1
        while True:
            changed=False
            for c in f:
                counts['clause_scans']+=1
                remaining=[];done=False
                for z in c:
                    counts['literal_tests']+=1
                    v=a[abs(z)-1]
                    if v<0:remaining.append(z)
                    elif bool(v)==(z>0):done=True;break
                if done:continue
                if not remaining:return None
                if len(remaining)==1:
                    z=remaining[0];idx=abs(z)-1;val=int(z>0)
                    if a[idx]>=0 and a[idx]!=val:return None
                    if a[idx]<0:a[idx]=val;counts['forced']+=1;changed=True
            if not changed:break
        if all(any(a[abs(z)-1]>=0 and bool(a[abs(z)-1])==(z>0) for z in c) for c in f):
            return [max(0,x) for x in a]
        v=next(i for i,x in enumerate(a) if x<0)
        for val in (0,1):
            b=a[:];b[v]=val
            r=solve(b)
            if r is not None:return r
        return None
    r=solve([-1]*n)
    return {'result':'SAT' if r is not None else 'UNSAT','witness':r,'measurements':dict(counts)}

def project(f,B_ids,I_ids):
    out={}
    for b in itertools.product((0,1),repeat=len(B_ids)):
        found=None
        for x in itertools.product((0,1),repeat=len(I_ids)):
            a=[0]*(max(B_ids+I_ids))
            for v,t in zip(B_ids,b):a[v-1]=t
            for v,t in zip(I_ids,x):a[v-1]=t
            if sat(f,a):found=list(x);break
        out[''.join(map(str,b))]=found
    return out

def shifted(f,k):return [[(1 if z>0 else -1)*(abs(z)+k) for z in c] for c in f]

def components(f):
    n=max(abs(z) for c in f for z in c)
    inc=[[] for _ in range(n+1)]
    for j,c in enumerate(f):
        for z in c:inc[abs(z)].append(j)
    unseen=set(range(len(f)));out=[];probes=0
    while unseen:
        todo=[next(iter(unseen))];cc=set()
        while todo:
            j=todo.pop()
            if j not in unseen:continue
            unseen.remove(j);cc.add(j)
            for z in f[j]:
                for h in inc[abs(z)]:
                    probes+=1
                    if h in unseen:todo.append(h)
        out.append(sorted(cc))
    return out,probes

def complete_physical_trace(parent,child,events):
    """Declared fixed index/work tape, with head-address register fields included
    in aligned diagnostic configuration; source is read-only, not writable.
    No claim of native FLMV transition-equivalence.
    """
    src=encode(parent);dst=encode(child)
    nparent=max(abs(z) for c in parent for z in c);nchild=max(abs(z) for c in child for z in c)
    w=max(1,len(src).bit_length()); wp=nparent.bit_length();wc=nchild.bit_length()
    hsrc=len(gamma(nparent))+len(gamma(len(parent)))
    hdst=len(gamma(nchild))+len(gamma(len(child)))
    istate=[0]*w;work=[0]*len(dst);head_index=0;head_work=0;phase=0
    counters=collections.Counter();dphys_total=0;record_ids=set();peak_live=len(work)+len(istate)+2*w+3
    emit=lambda x:events.write((json.dumps(x,separators=(',',':'))+'\n').encode())
    def step(kind,bitidx,d,changed=None,extra=None):
        nonlocal dphys_total
        dphys_total+=d;counters['events']+=1;counters['physical_adjacent_xor']+=d
        counters[kind]+=1
        z={'operation':kind,'output_bit':bitidx,'d_phys':d}
        if changed is not None:z['changed_location']=changed
        if extra is not None:z.update(extra)
        emit(z)
    for j in range(len(dst)):
        if j<hdst:
            bit=int(dst[j]);step('literal_header_emit',j,0,extra={'value':bit})
        else:
            payload=j-hdst;row,position=divmod(payload,1+3*wc)
            if position==0:q=hsrc+row*(1+3*wp)
            else:
                litidx,bitpos=divmod(position-1,wc)
                q=hsrc+row*(1+3*wp)+1+litidx*wp+(wp-wc)+bitpos
            # reset index tape one cell at a time and program new address in endian fixed positions
            for t in range(w):
                oldhead=head_index;head_index=t
                delta=(oldhead^head_index).bit_count()
                step('index_head_position',j,delta,extra={'head_location':t})
                bitreq=(q>>t)&1
                delta=istate[t]^bitreq;istate[t]=bitreq
                step('index_cell_write',j,delta,changed=f'index:{t}' if delta else None,extra={'cell':t,'new_bit':bitreq})
            bit=int(src[q]);step('source_indexed_read',j,0,extra={'source_bit':q,'value':bit})
            # reset index tape as one declared special random-access operation,
            # not as one standard single-cell TM write.
            reset=sum(istate);istate[:]=[0]*w
            step('index_atomic_reset',j,reset,extra={'cells_cleared':reset})
        prev=head_work;head_work=j
        dh=(prev^head_work).bit_count()
        step('work_head_position',j,dh,extra={'head_location':j})
        delta=work[j]^bit;work[j]=bit
        if j>=hdst:record_ids.add(1+(j-hdst)//(1+3*max(abs(z) for c in child for z in c).bit_length()))
        step('work_cell_write',j,delta,changed=f'work:{j}' if delta else None,extra={'new_bit':bit})
    assert ''.join(map(str,work))==dst
    endpoint_delta=sum(istate)+sum(work)+head_index.bit_count()+head_work.bit_count()
    return {'parent_bits':len(src),'child_bits':len(dst),'contracted_below_sqrt':len(dst)**2<=len(src),
            'events':counters['events'],'physical_adjacent_xor':dphys_total,'endpoint_phys_xor':endpoint_delta,
            'index_width_bits':w,'work_bits':len(dst),'min_declared_fixed_configuration_bits':peak_live,
            'changed_child_clause_records':sorted(record_ids),'counters':dict(counters),
            'read_only_source_bits':len(src),'head_position_encoding':'binary diagnostic registers; no native TM lower bound',
            'child_indexed_bit_accessor':'header direct else source[header_parent+(j-header_child)]',
            'child_sha256':hashlib.sha256(dst.encode()).hexdigest()}

def main():
    src=pathlib.Path(sys.argv[1]).read_text();U=ast.literal_eval(src[src.index('[['):]);assert valid(U)
    V=[c[:] for c in U];assert V[2][-1]==197 and V[44][-1]==196
    V[2][-1]=196;V[44][-1]=197;assert valid(V)
    assert sat(V,[int(v) for v in WITNESS_V]);assert len(WITNESS_V)==198
    F6=make_y(P6,Q6);assert valid(F6)
    p=((1,4,5),(2,4,6),(3,5,6));q=p
    # local boundary (1,2,3) and private (7,8,9); inside H has 6 clauses.
    hnew=[[v if v<=3 else v+3 for v in c] for c in p]+[[-(v if v<=3 else v+3) for v in c] for c in q]
    E=F6[:];E.remove([1,2,3]);E.remove([-1,-2,-3]);F9=E+hnew;assert valid(F9)
    c9,cc=components(F9);assert len(c9)==1
    # Check explicit counterexample: original x1...x6 assignment that cannot satisfy F6,
    # but admits an extension to the connected strict22 expansion.
    bad=None
    for a in itertools.product((0,1),repeat=6):
        if sat(F6,a):continue
        for private in itertools.product((0,1),repeat=3):
            if sat(F9,a+private):bad={'original_assignment':''.join(map(str,a)),'private_extension':''.join(map(str,private)),'original_bad_clause_ids':[j+1 for j,t in enumerate(masks(F6,a)) if t==0]};break
        if bad:break
    assert bad and bad['original_assignment'][:3]=='000'
    fam,wins,types=gadgets()
    data={'run':'M22-NAE-GADGET284','model':'canonical M22 bitstring, exact fixed 3B/3I gadget exhaustive classification; separate simulated physical tapes',
          'seed':284,'source_sha256':hashlib.sha256(src.encode()).hexdigest(),
          'exact_gadget':{'boundary_ids':list(B),'private_ids':list(I),'family_count':len(fam),'all_families':fam,'profile_exhaustive_pairs':225,'pairwise_boundary_cases':1800,'literal_assignment_tests':14400,'family_type_counts':types,'witness_table':wins,
                          'countercontrol_with_duplicates':{'positive':[[1,2,3],[4,5,6],[4,5,6]],'negative':[[-1,-2,-3],[-4,-5,-6],[-4,-5,-6]],'boundary_profile':'NAE','canonical_target_valid':False}},
          'connected_unsound_grammar_valid_expansion':{'F6':F6,'F9':F9,'F6_n':6,'F9_n':9,'F6_m':8,'F9_m':12,'F6_SAT_count':sum(sat(F6,a) for a in itertools.product((0,1),repeat=6)), 'F9_SAT_count':sum(sat(F9,a) for a in itertools.product((0,1),repeat=9)),'projection_counterexample':bad,'component_count':len(c9)},
          'original_controls':{},'physical_child':{}}
    Y=make_y();assert valid(Y)
    for name,f in [('Y6_SAT',Y),('PAIRED6_SAT',F6),('CONNECTED9_SAT',F9),('U198_UNSAT',U),('V198_SAT',V)]:
        pair=compatible(f)
        checks=full_pair_verify_small(f,pair) if len(f)<=12 else None
        data['original_controls'][name]={'n':max(abs(z) for c in f for z in c),'m':len(f),'original_signed_occurrences':degree_tag(f), 'SS_SU_US_UU_matrix':pair,
                                        'small_pair_extreme_enumeration_checks':checks,'coherent_flip_trail':trail(f),
                                        'complete_zero':logical_frame(f,[0]*max(abs(z) for c in f for z in c)),
                                        'complete_one':logical_frame(f,[1]*max(abs(z) for c in f for z in c)),
                                        'encoded_bits':len(encode(f)),'baseline':dpll(f) if len(f)<=12 else {'source':'verified prior TARGET-SCOPE278, both large cases cap-unresolved'}}
    # one parent and one child each SAT and UNSAT, source Y6 independent.
    for name,f in [('Y6_pair_SAT',Y),('U198_UNSAT',U),('V198_SAT',V)]:
        parent=f+shifted(Y,max(abs(z) for c in f for z in c));assert valid(parent)
        parts,probes=components(parent);assert len(parts)==2
        with gzip.open(sys.argv[3].replace('.jsonl.gz',f'_{name}.jsonl.gz'),'wb') as eventlog:
            phys=complete_physical_trace(parent,f,eventlog)
        phys['discovery_incidence_probes']=probes
        phys['policy_recognitions']=1;phys['failed_policies']=0;phys['source_validation_clause_literal_probes']=len(parent)*3
        data['physical_child'][name]=phys
    pathlib.Path(sys.argv[2]).write_text(json.dumps(data,indent=2))
    print(json.dumps({'status':'PRODUCER PASS','families':len(fam),'tested_boundary_cases':1800,'connected_counterexample':bad,
          'safe_children':{k:{q:v[q] for q in ('parent_bits','child_bits','physical_adjacent_xor','endpoint_phys_xor','events','contracted_below_sqrt')} for k,v in data['physical_child'].items()},
          'sha256':hashlib.sha256(pathlib.Path(sys.argv[2]).read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
