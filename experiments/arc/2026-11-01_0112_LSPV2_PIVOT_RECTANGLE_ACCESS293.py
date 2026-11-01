#!/usr/bin/env python3
"""LSPV-2 293: exact signed pivot rectangle, virtual mixed-width child,
canonical suffix-peel physical event streams, and original-source controls.
Python standard library; deterministic exhaustive n=6 census.
"""
from __future__ import annotations
import ast, collections, gzip, hashlib, itertools, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
UFILE=ROOT/'U198.txt'
Y=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
U=[tuple(row) for row in ast.literal_eval(''.join(x for x in UFILE.read_text().splitlines() if not x.startswith('#')))]
V=[list(c) for c in U];V[2][-1],V[44][-1]=V[44][-1],V[2][-1];V=[tuple(c) for c in V]

def gamma(n):
    assert n>0
    b=format(n,'b');return '0'*(len(b)-1)+b

def valid(F):
    if not F:return False
    seen=set(); count=collections.Counter();n=max(abs(x) for c in F for x in c)
    if n==0 or 4*n!=3*len(F):return False
    for c in F:
        if len(c)!=3 or len({abs(v) for v in c})!=3:return False
        if not(all(v>0 for v in c) or all(v<0 for v in c)):return False
        t=tuple(sorted(c))
        if t in seen:return False
        seen.add(t)
        for v in c: count[v]+=1
    return all(count[i]==count[-i]==2 for i in range(1,n+1))

def encode_can(F):
    n=max(abs(l) for c in F for l in c);w=n.bit_length()
    return gamma(n)+gamma(len(F))+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(l),f'0{w}b') for l in c) for c in F)

def encode_tag(F,n):
    w=n.bit_length()
    return gamma(n)+gamma(len(F))+''.join(('0' if len(c)==3 else '1')+''.join(('1' if l>0 else '0')+format(abs(l),f'0{w}b') for l in c) for c in F)

def get_pivot(F,x):
    p=[i for i,c in enumerate(F) if x in c];q=[i for i,c in enumerate(F) if -x in c]
    assert len(p)==len(q)==2
    pairs=[]
    for i in p:
        for j in q:
            ap=tuple(l for l in F[i] if abs(l)!=x)
            bn=tuple(l for l in F[j] if abs(l)!=x)
            taut=bool({abs(t) for t in ap}&{abs(t) for t in bn})
            pairs.append((i,j,ap,bn,taut))
    return p,q,pairs

def child(F,x):
    p,q,pairs=get_pivot(F,x)
    exclude=set(p+q)
    keep=[c for j,c in enumerate(F) if j not in exclude]
    out=keep+[a+b for i,j,a,b,t in pairs if not t]
    assert all(len(c) in (3,4) for c in out)
    return out

def eval_cnf(F,a):return all(any(a[abs(l)-1]==(l>0) for l in c) for c in F)

def local_provenance(F,x):
    p,q,pairs=get_pivot(F,x)
    return {'pivot':x,'positive_clause_ids':p,'negative_clause_ids':q,
      'resolvent_pairs':[{'source_clause_ids':[i,j],'literals':list(a+b),
        'tautology':t,'guard_cube':[[abs(k),int(k<0)] for k in a+b] if not t else None}
         for i,j,a,b,t in pairs]}

def validator_flags(F):
    return {'is_target_valid':valid(F),'clauses':len(F),
            'variables':max(abs(l) for c in F for l in c)}

def equal_local(F,x):
    p,q,pairs=get_pivot(F,x)
    vars_=sorted({abs(z) for i in p+q for z in F[i]}-{x})
    C=[F[i] for i in p+q]
    Q=[a+b for i,j,a,b,t in pairs if not t]
    for bits in itertools.product((False,True),repeat=len(vars_)):
        a={v:b for v,b in zip(vars_,bits)}
        good=any(all(any((bit if v==x else a[v])==(z>0) for z in c for v in [abs(z)]) for c in C) for bit in (False,True))
        rhs=all(any(a[abs(z)]==(z>0) for z in c) for c in Q)
        assert good==rhs,(x,a,C,Q)
    return 1<<len(vars_)

def enumerate_six():
    triples=list(itertools.combinations(range(1,7),3))
    fam=[f for f in itertools.combinations(triples,4) if all(sum(i in c for c in f)==2 for i in range(1,7))]
    assert len(fam)==75
    hist=collections.Counter();fullex=0;cn=0;models=collections.Counter()
    examples=[]
    for pp in fam:
        for nn in fam:
            F=tuple(pp)+tuple(tuple(-v for v in c) for c in nn)
            assert valid(F)
            ct=0
            for x in range(1,7):
                t=sum(r[-1] for r in get_pivot(F,x)[2]); hist[t]+=1
                if t==4:
                    fullex+=1;ct+=1
                    if len(examples)<3:examples.append({'positive':[list(c) for c in pp], 'negative':[list(c) for c in nn], 'pivot':x})
                cn+=equal_local(F,x)
            models[ct]+=1
    return {'positive_families':75,'negative_families':75,'target_formulas':5625,
        'pivot_trials':33750,'local_assignment_checks':cn,
        'resolvent_tautology_count_histogram':dict(sorted(hist.items())),
        'formulas_by_full_pivot_count':dict(sorted(models.items())),
        'full_pivot_occurrences':fullex,'examples':examples}

class Accessor:
    """One selected pivot, parent virtual tagged bits are read from canonical source.
    Descriptor is FOUR original clause indices and their literal field orders.
    Querying arbitrary child bit does not construct target child.
    """
    def __init__(self,F,x):
        self.F=F;self.x=x;self.n=max(abs(l) for c in F for l in c)
        self.w=self.n.bit_length();self.c3=1+3*(self.w+1);self.c4=1+4*(self.w+1)
        self.p,self.q,self.pairs=get_pivot(F,x);self.kill=sorted(self.p+self.q)
        self.keep=len(F)-4
        self.rpairs=[r for r in self.pairs if not r[-1]]
        self.parent_can=encode_can(F);self.parent_tag=encode_tag(F,self.n)
        self.parent_header=gamma(self.n)+gamma(len(F));self.child_header=gamma(self.n)+gamma(self.keep+len(self.rpairs))
        self.output_len=len(self.child_header)+self.keep*self.c3+len(self.rpairs)*self.c4
        self.source_queries=0;self.local_ops=0
        self.part='virtual_gnc_3or4_cnf'
    def canonical_bit(self,addr):
        assert 0<=addr<len(self.parent_can)
        self.source_queries+=1
        return self.parent_can[addr],addr
    def parent_tag_bit(self,q):
        """Use one indexed canonical source read; zero tag synthesized."""
        self.local_ops+=1
        if q<len(self.parent_header):return self.canonical_bit(q)
        j,t=divmod(q-len(self.parent_header),self.c3)
        if t==0:return '0',None
        k,d=divmod(t-1,self.w+1)
        canon_start=len(self.parent_header)+j*(1+3*self.w)
        if d==0:return self.canonical_bit(canon_start)
        return self.canonical_bit(canon_start+1+k*self.w+d-1)
    def bit(self,q):
        assert 0<=q<self.output_len
        self.local_ops+=1
        if q<len(self.child_header):return self.child_header[q],None, 'header'
        b=q-len(self.child_header)
        if b<self.keep*self.c3:
            j,t=divmod(b,self.c3)
            src=j
            for skipped in self.kill:
                if src>=skipped:src+=1
                else:break
            z,addr=self.parent_tag_bit(len(self.parent_header)+src*self.c3+t)
            return z,addr,f'original:C{src}'
        v=b-self.keep*self.c3
        j,t=divmod(v,self.c4)
        srcp,srcn,a,b,_=self.rpairs[j]
        if t==0:return '1',None,f'resolvent:C{srcp},C{srcn}'
        k,d=divmod(t-1,self.w+1)
        src=srcp if k<2 else srcn
        lit=(a+b)[k]
        fk=list(self.F[src]).index(lit)
        pos=len(self.parent_header)+src*self.c3+1+fk*(self.w+1)+d
        z,addr=self.parent_tag_bit(pos)
        return z,addr,f'resolvent:C{srcp},C{srcn}'
    def emit(self):return ''.join(self.bit(i)[0] for i in range(self.output_len))

def source_extremes(F):
    count=collections.Counter()
    for c in F:
        for lit in c:
            count['occurrence_extrema']+=1
            # source-indexed ALL-TRUE/ALL-FALSE target is a LOCAL constraint only.
            assert (int(lit>0)^1)==int(lit<0)
    for j in range(len(F)):
        for k in range(j+1,len(F)):
            a,b=F[j],F[k]
            same=bool({abs(v) for v in a}&{abs(v) for v in b}) and ((a[0]>0)==(b[0]>0))
            opp=bool({abs(v) for v in a}&{abs(v) for v in b}) and ((a[0]>0)!=(b[0]>0))
            # On monotone target, the mixed same+opposite relation cannot arise.
            assert not(same and opp)
            mask=(not opp,not same,not same,not opp)
            count['clause_pairs']+=1
            count['compatible_modes']+=sum(mask)
    return dict(count)

def flip_trail(F, start, order):
    a=start[:];states=[]
    for k in [None]+order:
        if k is not None:a[k-1]^=1
        counts=[sum(a[abs(z)-1]==int(z>0) for z in c) for c in F]
        states.append({'flip':k,'counts':[counts.count(t) for t in range(4)],
                       'satisfied':not counts.count(0)})
    return states

def physical_peel(F,run_id,cap=99999999):
    """Target-valid canonical suffix-delete Y6. Fixed index/child writable tapes,
    source ROM; source probes indexed and charged; offline XOR from real writes."""
    n=max(abs(z) for c in F for z in c)
    assert valid(F) and n>6
    C=F[:-8]
    assert valid(C)
    parent=encode_can(F);target=encode_can(C)
    # canonical child source bits are not naive prefix: headers change, width may change
    # descriptor map is virtual row numbering and gamma header; code scans source output
    nch=max(abs(z) for c in C for z in c);wc=nch.bit_length();wp=n.bit_length()
    hp=gamma(n)+gamma(len(F));hc=gamma(nch)+gamma(len(C))
    assert len(target)==len(hc)+len(C)*(1+3*wc)
    ti=collections.defaultdict(int);tb=collections.defaultdict(int)
    qwidth=(len(parent)-1).bit_length();m={'step_records':0,'phys_changes':0,'source_queries':0,
         'unchanged_writes':0,'index_writes':0,'buffer_writes':0,'head_moves':0,'jump_erases':0}
    fpath=ROOT/(run_id+'_phys_events.jsonl.gz')
    trace=gzip.open(fpath,'wt',encoding='utf8')
    def wr(tape,pos,val,rid):
        d=ti if tape=='index' else tb
        prev=d[pos]
        ch=int(prev!=val)
        d[pos]=val
        m['step_records']+=1;m['phys_changes']+=ch
        if not ch:m['unchanged_writes']+=1
        m['index_writes' if tape=='index' else 'buffer_writes']+=1
        trace.write(json.dumps([tape,pos,prev,val,rid],separators=(',',':'))+'\n')
    def read(addr,rid):
        assert 0<=addr<len(parent)
        bits=f'{addr:0{qwidth}b}'
        for k,b in enumerate(bits):wr('index',k,int(b),rid);m['head_moves']+=1
        m['source_queries']+=1;m['jump_erases']+=1
        v=parent[addr]
        for k in range(qwidth):wr('index',k,0,rid);m['head_moves']+=1
        return v
    out=[]
    for i in range(len(target)):
        if i<len(hc):b=hc[i];rid='child_header'
        else:
            j,t=divmod(i-len(hc),1+3*wc)
            rid=f'C{j}'
            if t==0:b=read(len(hp)+j*(1+3*wp),rid)
            else:
                k,z=divmod(t-1,wc)
                b=read(len(hp)+j*(1+3*wp)+1+k*wp+(wp-wc)+z,rid)
        out.append(b);wr('buffer',i,int(b),rid)
    trace.close()
    assert ''.join(out)==target
    m['endpoint_phys_xor']=sum(ti.values())+sum(tb.values())
    m['sum_adjacent_phys_xor']=m['phys_changes'];m['parent_bits']=len(parent)
    m['child_bits']=len(target);m['index_tape_peak_cells']=qwidth;m['child_buffer_peak_cells']=len(target)
    m['peak_writable_cells_bound']=qwidth+len(target)
    m['source_bits_sha256']=hashlib.sha256(parent.encode()).hexdigest()
    m['child_sha256']=hashlib.sha256(target.encode()).hexdigest()
    m['event_file']=str(fpath.name)
    m['changed_record_ids']=['removed_original:C'+str(i) for i in range(len(C),len(F))]
    m['scope']='explicit materialized child buffer; not the FLMV output-excluded space model'
    return m

def main():
    assert all(valid(F) for F in (Y,U,V))
    census=enumerate_six()
    same={};access={}
    for name,F in [('Y6',Y),('U198',U),('V198',V)]:
        n=max(abs(z) for c in F for z in c)
        hist=collections.Counter();peels=[];checks=0
        for x in range(1,n+1):
            t=sum(r[-1] for r in get_pivot(F,x)[2]);hist[t]+=1
            checks+=equal_local(F,x)
            if t and len(peels)<2:peels.append(local_provenance(F,x))
        source=source_extremes(F)
        a=Accessor(F,peels[0]['pivot'] if peels else 1)
        virtual=a.emit();expected=encode_tag(child(F,a.x),n)
        assert virtual==expected
        tag_len=len(encode_tag(F,n));canon_len=len(encode_can(F));actual=len(virtual)
        access[name]={'selected_pivot':a.x,'descriptor':peels[0] if peels else local_provenance(F,1),
          'original_target_bits':canon_len,'generic_tag_parent_bits':tag_len,
          'generic_tag_child_bits':actual,'delta_vs_generic_tag_parent':actual-tag_len,
          'delta_vs_original_canonical_input':actual-canon_len,
          'all_bits_verified':len(virtual),'indexed_original_source_bit_reads':a.source_queries,
          'lookup_local_operations_proxy':a.local_ops,
          'virtual_child_sha256':hashlib.sha256(virtual.encode()).hexdigest(),
          'explicit_child_sha256':hashlib.sha256(expected.encode()).hexdigest()}
        same[name]={'variables':n,'clauses':len(F),'tautology_histogram':dict(sorted(hist.items())),
          'pivot_local_truth_table_checks':checks,'original_extreme_controls':source,
          'zero_endpoint':[sum(sum((0==(z>0)) for z in c)==t for c in F) for t in range(4)],
          'one_endpoint':[sum(sum((1==(z>0)) for z in c)==t for c in F) for t in range(4)],
          'flip_trail':flip_trail(F,[0]*n,list(range(1,min(n,6)+1)))}
    work={}
    for name,F in [('Y6_Y6_SAT',Y+[tuple((1 if l>0 else -1)*(abs(l)+6) for l in c) for c in Y]),
                   ('U198_Y6_UNSAT',U+[tuple((1 if l>0 else -1)*(abs(l)+198) for l in c) for c in Y]),
                   ('V198_Y6_SAT',V+[tuple((1 if l>0 else -1)*(abs(l)+198) for l in c) for c in Y])]:
        work[name]=physical_peel(F,name)
    # Independent connected easy-family adversarial control: all-pivot t=0.
    easy=[]
    for k in (7,9,11):
        F=[]
        for shift in range(4):
            for i in range(k):
                C0=(i+1,k+(i+shift)%k+1,2*k+(i+2*shift)%k+1)
                F.append(C0 if shift<2 else tuple(-z for z in C0))
        assert valid(F)
        assert all(sum(r[-1] for r in get_pivot(F,x)[2])==0 for x in range(1,3*k+1))
        witness=[1]*k+[0]*(2*k)
        assert eval_cnf(F,witness)
        easy.append({'k':k,'variables':3*k,'clauses':4*k,
                     'every_pivot_zero_tautologies':True,'witness_verified':True,
                     'sha256':hashlib.sha256(json.dumps(F,separators=(',',':')).encode()).hexdigest()})
    raw={'run_id':'PIVOT_RECTANGLE_ACCESS293','census6':census,'same_source':same,
         'indexed_accessor':access,'canonical_peel_physical':work,'easy_connected_all_zero':easy,
         'status':{'local_exact_resolution':'KNOWN THEOREM, independently proved restriction',
                   'canonical_pivot_histograms':'COMPUTATIONAL','indexed_bit_access':'PROVED/EXACT in declared encoding',
                   'hereditary_canonical_child':'OPEN','arbitrary_A_to_Phi_A':'OPEN','P_vs_NP':'OPEN'},
         'warnings':['generic tagged CNF children are not in the canonical NP-complete target',
                     'a t=1 ordinary child is 1 bit smaller in tagged representation but longer than canonical encoded parent',
                     'physical traces include a writable child buffer and do not supply native FLMV space exponents',
                     'SAT/UNSAT U/V labels depend on independently checked original-source certificate and witness; no timeout proof']}
    (ROOT/'results293.json').write_text(json.dumps(raw,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'census':{k:v for k,v in census.items() if k!='examples'},
                      'same':{k:v['tautology_histogram'] for k,v in same.items()},
                      'access':{k:{s:v[s] for s in ('selected_pivot','original_target_bits','generic_tag_parent_bits','generic_tag_child_bits','delta_vs_generic_tag_parent','delta_vs_original_canonical_input')} for k,v in access.items()},
                      'physical':{k:{s:v[s] for s in ('step_records','phys_changes','endpoint_phys_xor','source_queries','parent_bits','child_bits')} for k,v in work.items()}},indent=2))
    print('END_OF_PRODUCER::PIVOT_RECTANGLE_ACCESS293::P_VS_NP_OPEN')
if __name__=='__main__':main()
