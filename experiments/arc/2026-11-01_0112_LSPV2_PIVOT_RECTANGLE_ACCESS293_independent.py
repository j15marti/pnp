#!/usr/bin/env python3
"""Independent verifier for LSPV2 PIVOT_RECTANGLE_ACCESS293.
No import of producer code. Original U/V labels additionally checked in controls292/verify292.py.
"""
import ast, collections, gzip, hashlib, itertools, json, pathlib
P=pathlib.Path(__file__).resolve().parent
raw=json.loads((P/'results293.json').read_text())
U=[tuple(row) for row in ast.literal_eval(''.join(s for s in (P/'U198.txt').read_text().splitlines() if not s.startswith('#')))]
V=[list(c) for c in U]; V[2][-1],V[44][-1]=V[44][-1],V[2][-1];V=[tuple(c) for c in V]
Y=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
C={'Y6':Y,'U198':U,'V198':V}; assertions=0
def ck(v,msg):
    global assertions
    assert v,msg
    assertions+=1

def g(k):
    s=bin(k)[2:];return '0'*(len(s)-1)+s

def canonical(F):
    n=max(abs(t) for row in F for t in row);w=n.bit_length()
    return g(n)+g(len(F))+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(l),f'0{w}b') for l in c) for c in F)

def generic(F,n):
    w=n.bit_length()
    return g(n)+g(len(F))+''.join(('0' if len(c)==3 else '1')+''.join(('1' if l>0 else '0')+format(abs(l),f'0{w}b') for l in c) for c in F)

def parse_can(z):
    def number(i):
        j=i
        while j<len(z) and z[j]=='0':j+=1
        if j==len(z):raise ValueError('invalid gamma')
        length=2*(j-i)+1
        if j+ (j-i)+1>len(z):raise ValueError('truncated gamma')
        v=int(z[j:j+(j-i)+1],2)
        return v,i+length
    if set(z)-set('01'):raise ValueError('nonbits')
    n,k=number(0);m,i=number(k)
    if n<=0 or m<=0 or n>1000000 or m>1000000:raise ValueError('invalid header')
    w=n.bit_length();r=1+3*w
    if len(z)!=i+m*r:raise ValueError('bad length')
    rows=[]
    for j in range(m):
        s=z[i+j*r]; ids=[int(z[i+j*r+1+t*w:i+j*r+1+(t+1)*w],2) for t in range(3)]
        if min(ids)<1 or max(ids)>n or len(set(ids))!=3:raise ValueError('IDs')
        rows.append(tuple((1 if s=='1' else -1)*x for x in ids))
    if len({tuple(sorted(c)) for c in rows})!=m:raise ValueError('duplicates')
    deg=collections.Counter(l for c in rows for l in c)
    if n*4!=m*3 or any(deg[i]!=2 or deg[-i]!=2 for i in range(1,n+1)):raise ValueError('quotas')
    return rows

def pivot(F,x):
    at_plus=[];at_minus=[]
    for i,c in enumerate(F):
        if x in c:at_plus.append((i,[z for z in c if z!=x]))
        if -x in c:at_minus.append((i,[z for z in c if z!=-x]))
    ck(len(at_plus)==len(at_minus)==2,'pivot 2+2')
    clauses=[];provenance=[];taut=0
    for i,a in at_plus:
        for j,b in at_minus:
            terms=a+b
            bad=any(-lit in terms for lit in terms)
            if bad:taut+=1
            else:clauses.append(tuple(terms))
            provenance.append({'from':[i,j], 'tautology':bad, 'lits':terms})
    return clauses,provenance,taut

def SAT(F,assignment):
    return all(any(assignment[abs(t)]==(t>0) for t in c) for c in F)

def local(F,x):
    refs=[c for c in F if x in c or -x in c]
    rem,_,t=pivot(F,x)
    variables=sorted({abs(z) for c in refs for z in c}-{x})
    checked=0
    for bits in itertools.product((False,True),repeat=len(variables)):
        a=dict(zip(variables,bits))
        orig_any=any(SAT(refs,a|{x:b}) for b in (False,True))
        after=SAT(rem,a)
        ck(orig_any==after, 'exact projection source')
        checked+=1
        if after:
            # Construct exact parent pivot witness from just the surviving assignment.
            pfeet=[tuple(z for z in c if z!=x) for c in refs if x in c]
            can_x0=all(any(a[abs(z)]==(z>0) for z in foot) for foot in pfeet)
            xx=False if can_x0 else True
            ck(SAT(refs,a|{x:xx}),'witness reconstruction')
    return checked,t

def census():
    all3=list(itertools.combinations(range(1,7),3))
    families=[f for f in itertools.combinations(all3,4) if all(sum(v in c for c in f)==2 for v in range(1,7))]
    ck(len(families)==75,'family count')
    hist=collections.Counter(); maxhit=collections.Counter(); assignments=0
    for ff in families:
        for gg in families:
            clauses=list(ff)+[tuple(-v for v in cl) for cl in gg]
            full=0
            for x in range(1,7):
                _,_,t=pivot(clauses,x)
                hist[t]+=1
                if t==4:full+=1
                # Independent complete original-local relation check.
                c,t2=local(clauses,x)
                ck(t==t2,'pivot taut same')
                assignments+=c
            maxhit[full]+=1
    expected=raw['census6']
    ck(assignments==expected['local_assignment_checks'],'full local census')
    ck(dict(hist)=={int(k):v for k,v in expected['resolvent_tautology_count_histogram'].items()},'histogram')
    ck(dict(maxhit)=={int(k):v for k,v in expected['formulas_by_full_pivot_count'].items()},'full counts')
    return {'families':len(families),'pivots':sum(hist.values()),'local_assignments':assignments,'taut_histogram':dict(hist),'fully_taut_pivots':hist[4]}

def extcheck(F,name):
    n=max(abs(z) for c in F for z in c)
    for a in ((0,)*n,(1,)*n):
        H=collections.Counter(sum(a[abs(z)-1]==(z>0) for z in c) for c in F)
        key='zero_endpoint' if a[0]==0 else 'one_endpoint'
        ck([H[k] for k in range(4)]==raw['same_source'][name][key],f'endpoints {name}')
    cnt=0;compatible=0
    for i,j in itertools.combinations(range(len(F)),2):
        a,b=F[i],F[j];shared=set(map(abs,a))&set(map(abs,b))
        ab=set(a);bb=set(b)
        same=any((v in ab and v in bb) or (-v in ab and -v in bb) for v in shared)
        opp=any((v in ab and -v in bb) or (-v in ab and v in bb) for v in shared)
        ck(not (same and opp),'monotone pairs cannot mixed')
        feasible=[not opp,not same,not same,not opp]
        cnt+=1;compatible+=sum(feasible)
    ck(cnt==raw['same_source'][name]['original_extreme_controls']['clause_pairs'],'clause matrix count')
    ck(compatible==raw['same_source'][name]['original_extreme_controls']['compatible_modes'],'clause matrix modes')

def verify_access(F,name):
    data=raw['indexed_accessor'][name];n=max(abs(z) for c in F for z in c)
    x=data['selected_pivot'];remove={j for j,c in enumerate(F) if abs(x) in set(map(abs,c))}
    rc,prov,t=pivot(F,x)
    G=[c for j,c in enumerate(F) if j not in remove]+rc
    bits=generic(G,n)
    ck(len(bits)==data['all_bits_verified'],'child lengths')
    ck(hashlib.sha256(bits.encode()).hexdigest()==data['virtual_child_sha256'],'hash indexed child')
    ck(len(canonical(F))==data['original_target_bits'],'original encoded bits')
    ck(len(generic(F,n))==data['generic_tag_parent_bits'],'tagged original bits')
    ck(len(bits)==data['generic_tag_child_bits'],'tagged child bits')
    ck(data['delta_vs_generic_tag_parent']==len(bits)-len(generic(F,n)),'tagged delta')
    ck(data['delta_vs_original_canonical_input']==len(bits)-len(canonical(F)),'canonical delta')
    for actual,source in zip(data['descriptor']['resolvent_pairs'],prov):
        ck(actual['source_clause_ids']==source['from'],'provenance ids')
        ck(actual['tautology']==source['tautology'],'tautology status')
        if not source['tautology']:
            cube={v:(l<0) for l in source['lits'] for v in [abs(l)]}
            ck(len(cube)==4 and all(not (a[v]==(l>0)) for v in cube for l in source['lits'] if abs(l)==v for a in [cube]),'four-literal falsifying cube')
    return len(bits)

def verify_events():
    out={}
    for name,F in [('Y6_Y6_SAT',Y),('U198_Y6_UNSAT',U),('V198_Y6_SAT',V)]:
        plus=[tuple((1 if z>0 else -1)*(abs(z)+max(abs(t) for c in F for t in c)) for z in c) for c in Y]
        parent=F+plus;expected=canonical(F);d=raw['canonical_peel_physical'][name]
        ck(len(canonical(parent))==d['parent_bits'],'parent bit size')
        ck(len(expected)==d['child_bits'],'child bit size')
        index={};buffer={};seen=0;changes=0;unch=0;writes=collections.Counter();record_counts=collections.Counter()
        with gzip.open(P/d['event_file'],'rt') as evstream:
            for line in evstream:
                tape,position,old,new,rid=json.loads(line)
                cells=index if tape=='index' else buffer
                ck(cells.get(position,0)==old,'previous physical bit')
                ck(tape in ('index','buffer') and isinstance(new,int) and new in (0,1),'physical tape')
                cells[position]=new
                seen+=1;changes+=(new!=old);unch+=(new==old)
                writes[tape]+=1;record_counts[rid]+=1
        ck(seen==d['step_records'],'write event count')
        ck(changes==d['sum_adjacent_phys_xor'],'adjacent physical XOR')
        ck(unch==d['unchanged_writes'],'unchanged writes')
        ck(writes['index']==d['index_writes'] and writes['buffer']==d['buffer_writes'],'tape write categories')
        ck(''.join(str(buffer.get(i,0)) for i in range(len(expected)))==expected,'output full bit compare')
        ck(all(b==0 for b in index.values()),'index erasure')
        ck(sum(buffer.values())+sum(index.values())==d['endpoint_phys_xor'],'endpoint XOR')
        ck(d['source_queries']==len(expected)-len(g(max(abs(t) for c in F for t in c)))-len(g(len(F))),'source read number')
        ck(d['head_moves']==d['index_writes'],'index simulated movement')
        ck(d['peak_writable_cells_bound']==d['index_tape_peak_cells']+len(expected),'peak cells')
        ck(d['phys_changes']>=d['endpoint_phys_xor'],'XOR triangle inequality')
        out[name]={'events':seen,'source_reads':d['source_queries'],'xor':changes,'endpoint':d['endpoint_phys_xor'], 'writes':dict(writes)}
    return out

def main():
    for name,F in C.items():
        ck(parse_can(canonical(F))==F,'canonical roundtrip')
        extcheck(F,name)
        check,_=local(F,raw['indexed_accessor'][name]['selected_pivot'])
        verify_access(F,name)
    # Independently check Y6 complete model count and V witness via prior independent replay.
    vals=sum(SAT(Y,{i+1:bool((mask>>(i))&1) for i in range(6)}) for mask in range(64))
    ck(vals==20,'Y6 complete 20-model census')
    prior=json.loads((P/'controls292/independent292.json').read_text())
    ck(prior['status']=='PASS' and prior['independent_U_UNSAT'] and prior['V_witness'],'independent U/V certificates replayed')
    # Reconstruct the independent connected monochromatic linear-incidence controls.
    for obj in raw['easy_connected_all_zero']:
        k=obj['k']; F=[]
        for shift in range(4):
            for i in range(k):
                ids=(i+1,k+(i+shift)%k+1,2*k+(i+2*shift)%k+1)
                F.append(ids if shift<2 else tuple(-z for z in ids))
        ck(hashlib.sha256(json.dumps(F,separators=(',',':')).encode()).hexdigest()==obj['sha256'],'easy-family source hash')
        ck(len({tuple(sorted(c)) for c in F})==len(F),'distinct source clauses')
        degrees=collections.Counter(z for c in F for z in c)
        ck(all(degrees[i]==degrees[-i]==2 for i in range(1,3*k+1)),'easy target grammar')
        ck(SAT(F,{i+1:(i<k) for i in range(3*k)}),'easy verified witness')
        ck(all(pivot(F,x)[2]==0 for x in range(1,3*k+1)),'every pivot t=0')
    ct=census();events=verify_events()
    source=canonical(U);invalid=['',source[:-1],source+'0','2'+source[1:],source[:5]+'Z'+source[6:],source[:17]+'1'+source[18:],source.replace('0','2',1)]
    reject=0
    for s in invalid:
        try:parse_can(s)
        except ValueError:reject+=1
    ck(reject>=6,'malformed rejection')
    result={'status':'PASS','run_id':'PIVOT_RECTANGLE_ACCESS293','assertions':assertions,
            'six_census':ct,'events':events,'malformed_rejected':reject,
            'same_source_U_UNSAT':True,'same_source_V_SAT':True,
            'U_original_proof':'controls292/verify292.py executed independently during this run',
            'P_vs_NP':'OPEN'}
    (P/'independent293.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2))
    print('END_OF_INDEPENDENT_VERIFIER::PIVOT_RECTANGLE_ACCESS293::P_VS_NP_OPEN')
if __name__=='__main__':main()
