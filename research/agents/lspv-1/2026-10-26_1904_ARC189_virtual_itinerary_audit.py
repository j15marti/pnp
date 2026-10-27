#!/usr/bin/env python3
"""ARC189: source-authenticated exact-(2,2) DISJ and virtual RAM input-address itineraries.
Python stdlib only; deterministic, exhaustive up to m=7. Run:
 python ARC189_virtual_itinerary_audit.py [output.json]
All tests are promise-scoped and do not establish a SAT decision-time bound.
"""
import itertools, json, sys, math
from collections import Counter
from pathlib import Path
W1 = [(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
      (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
      (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
      (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
AIDX = (6,11)
BIDX = (9,17)
GAPIDX = tuple(i for i in range(20) if i not in AIDX+BIDX)
assert len(GAPIDX)==16

def module(a,b,shift=0):
    out=[]
    for j,c in enumerate(W1):
        row=list(c)
        if j in AIDX and a==0: row[0]=-row[0]
        if j in BIDX and b==0: row[2]=-row[2]
        out.append(tuple((v+shift if v>0 else v-shift) for v in row))
    return out

def nmodels(clauses):
    count=0
    for bits in range(1<<15):
        if all(any(bool((bits>>(abs(v)-1))&1)==(v>0) for v in cl) for cl in clauses): count+=1
    return count

def encode(m,a,b):
    width=len(str(15*m))
    head=f'p cnf {15*m} {20*m}\n'
    recwidth=3*(width+1)+3
    clauses=[]; leftA=[]; rightB=[]
    per=[module(a[j],b[j],15*j) for j in range(m)]
    for j in range(m):
        for index in AIDX:
            if index==AIDX[0]: leftA.append(len(head)+len(clauses)*recwidth)
            clauses.append(per[j][index])
    gap_start=len(head)+len(clauses)*recwidth
    for j in range(m):
        for index in GAPIDX: clauses.append(per[j][index])
    gap_end=len(head)+len(clauses)*recwidth
    for j in range(m):
        for index in BIDX:
            if index==BIDX[0]: rightB.append(len(head)+len(clauses)*recwidth+2*(width+2))
            clauses.append(per[j][index])
    def fmt(lit):return ('+' if lit>0 else '-') + str(abs(lit)).zfill(width)
    enc=head+''.join(' '.join(fmt(v) for v in cl)+'\n' for cl in clauses)
    assert len(enc)==len(head)+len(clauses)*recwidth
    assert all(enc[leftA[j]] in '+-' and enc[rightB[j]] in '+-' for j in range(m))
    return enc,clauses,leftA,rightB,gap_start,gap_end

def quotas(clauses,m):
    cnt=Counter((abs(v),v>0) for row in clauses for v in row)
    return (len(clauses)==20*m and all(len(set(abs(v) for v in row))==3 for row in clauses)
            and len(set(frozenset(row) for row in clauses))==20*m
            and all(cnt[(i,True)]==cnt[(i,False)]==2 for i in range(1,15*m+1)))

def recover_a(src,p):
    return int(src[p]=='+')

def recover_b(src,p):
    return int(src[p]=='-')

def itinerary(m,a,b,B):
    src,clauses,ap,bp,gs,ge=encode(m,a,b)
    addresses=[]; states=[]; found=False
    for lo in range(0,m,B):
        buff=[]
        for i in range(lo,min(m,lo+B)):
            state=('A',lo,i,tuple(buff),found,ap[i])
            addresses.append(ap[i]);states.append(state)
            buff.append(recover_a(src,ap[i]))
        for i in range(lo,min(m,lo+B)):
            state=('B',lo,i,tuple(buff),found,bp[i])
            addresses.append(bp[i]);states.append(state)
            found=found or bool(buff[i-lo] & recover_b(src,bp[i]))
    assert found==any(x & y for x,y in zip(a,b))
    pos=[0]+addresses
    delta=[v-u for u,v in zip(pos,pos[1:])]
    D=sum(abs(v) for v in delta)
    signs=[1 if x>0 else -1 for x in delta if x]
    V=sum(x!=y for x,y in zip(signs,signs[1:]))
    def seq(c):
        return tuple((1 if u<=c<v else -1,states[j])
                     for j,(u,v) in enumerate(zip(pos,pos[1:]))
                     if (u<=c<v or v<=c<u))
    return {'N':len(src),'G':ge-gs,'D':D,'V':V,'Q':len(addresses),
            'cut_sequence':seq, 'gaps':(gs,ge),'truth':not found}

def run():
    audit={'run':'ARC189-VIRTUAL-ITINERARY','source':'experiments/review/early22_compiler_redteam_audit.py W1',
           'exhaustive_module_counts':{},'clauses_checked':0,'promise_pairs':0,
           'satisfying_fooling_inputs':0,'fooling_cut_injective_checks':0,
           'itineraries_checked':0,'comparison_results':[],'assertions':0,
           'random_seed':None,'errors':0}
    def ok(q):
        assert q
        audit['assertions']+=1
    for a in range(2):
        for b in range(2):
            vals=nmodels(module(a,b))
            audit['exhaustive_module_counts'][f'{a}{b}']=vals
            ok((vals==0)==(a==b==1))
    ok([audit['exhaustive_module_counts'][i] for i in ('00','01','10','11')]==[772,272,272,0])
    for m in range(1,8):
        strings=list(itertools.product(range(2),repeat=m))
        common=None
        for a in strings:
            for b in strings:
                s,cs,ap,bp,g0,g1=encode(m,a,b)
                ok(quotas(cs,m));ok(len(s)>g1>g0>len(f'p cnf {15*m} {20*m}\n'))
                ok([recover_a(s,p) for p in ap]==list(a));ok([recover_b(s,p) for p in bp]==list(b))
                ok(len(s)==len(encode(m,tuple(0 for _ in range(m)),tuple(0 for _ in range(m)))[0]))
                audit['clauses_checked']+=len(cs);audit['promise_pairs']+=1
                if common is None:common=(len(s),g1-g0)
                ok((len(s),g1-g0)==common)
        for B in sorted(set([1,2,3,m])):
            if B>m:continue
            trace_sets=None
            for a in strings:
                b=tuple(1-x for x in a)
                x=itinerary(m,a,b,B)
                ok(x['truth']);ok(x['Q']==2*m)
                ok(x['D']>=x['G']);ok(x['V']>=0)
                audit['itineraries_checked']+=1; audit['satisfying_fooling_inputs']+=1
                gs,ge=x['gaps']
                cuts=sorted({gs,gs+(ge-gs)//4,(gs+ge)//2,gs+3*(ge-gs)//4,ge-1})
                if trace_sets is None:trace_sets={c:set() for c in cuts}
                for c in cuts:
                    t=x['cut_sequence'](c)
                    ok(t not in trace_sets[c])
                    trace_sets[c].add(t)
                    audit['fooling_cut_injective_checks']+=1
            for c in trace_sets:ok(len(trace_sets[c])==2**m)
        if m in (1,2,4,7):
            for B in sorted(set([1,2,3,m])):
                a=tuple(0 for _ in range(m));b=tuple(1 for _ in range(m))
                x=itinerary(m,a,b,B)
                audit['comparison_results'].append({'m':m,'B':B,'N':x['N'],
                    'gap':x['G'],'Q':x['Q'],'D':x['D'],'V':x['V']})
    return audit

if __name__=='__main__':
    data=run()
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path('ARC189_virtual_itinerary_results.json')
    dest.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k!='comparison_results'},sort_keys=True))
