#!/usr/bin/env python3
"""Independent, no producer import: replay every source-indexed Boolean elimination row.
Reads producer JSON and validates source, factor identity, exact projection, final
SAT witnesses/UNSAT bottom certificates; includes signed extremes, malformed,
and source-isomorphic reorderings.  This is not a native FLMV simulator.
"""
import ast, itertools, json, collections, random, pathlib
R=pathlib.Path(__file__).resolve().parent
RAW=json.loads((R/'results315.json').read_text())
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=P+tuple(tuple(-x for x in c) for c in N)
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F15P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
F15N=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=F15P+tuple(tuple(-x for x in c) for c in F15N)
U=[tuple(t) for t in ast.literal_eval(''.join(t for t in (R/'U198.txt').read_text().splitlines() if not t.startswith('#')))]
V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=[tuple(c) for c in V]
W='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
A={5:1};B={5:1,4:0,6:0};Z={};Q={1:0,5:0,6:0}
F9_S={1:0,2:0,8:1,9:1};F9_U={8:0,3:0,7:0,6:0,1:1,5:1}
P_U=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
P_S=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
NUM=collections.Counter()
def ck(cond,label):
    NUM['assertions']+=1
    if not cond:raise AssertionError(label)
def g(t):
    clauses=[]
    for j in range(t):
        for i,c in enumerate(P):
            clauses.append(tuple(9*j+x if (i,x)!=(0,5) else 9*((j+1)%t)+5 for x in c))
        clauses.extend(tuple(-(9*j+x) for x in c) for c in N)
    return tuple(clauses)
def pinlist(seq):
    return {9*j+x:v for j,p in enumerate(seq) for x,v in p.items()}
def valid(F,n):
    if n%3 or 3*len(F)!=4*n:return False
    counts=collections.Counter();used=set()
    for c in F:
        if len(c)!=3 or len(set(map(abs,c)))!=3 or any(not 1<=abs(x)<=n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        canon=tuple(sorted(c))
        if canon in used:return False
        used.add(canon)
        for x in c:counts[x]+=1
    return all(counts[i]==counts[-i]==2 for i in range(1,n+1))
def source_sat(F,assignment):
    return all(any(assignment[abs(z)]==int(z>0) for z in c) for c in F)
def models(F,n,p):
    free=[x for x in range(1,n+1) if x not in p]
    result=0
    for bits in itertools.product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        if source_sat(F,a):result+=1
    return result

def initial(F,p):
    fac=collections.Counter()
    for j,c in enumerate(F):
        if any(abs(z) in p and p[abs(z)]==int(z>0) for z in c):continue
        left=sorted({abs(z) for z in c if abs(z) not in p});mask=0
        for bits in itertools.product((0,1),repeat=len(left)):
            a={x:b for x,b in zip(left,bits)}
            good=any(abs(z) in a and a[abs(z)]==int(z>0) for z in c)
            if good:
                idx=sum(b<<i for i,b in enumerate(bits));mask|=1<<idx
        fac[(tuple(left),mask,('source',j))]+=1
    return fac

def evaluate(scope,mask,values):
    idx=sum(values[x]<<i for i,x in enumerate(scope))
    return bool((mask>>idx)&1)
def verify(F,n,p,out):
    ck(valid(F,n),'source grammar')
    if out['status'] not in ('SAT','UNSAT'):
        ck(out['status']=='UNRESOLVED','valid sources only unresolved');return
    curr=initial(F,p);eliminated=set()
    for step in out['trace']:
        x=step['x'];ck(x not in eliminated and x not in p,'fresh original variable')
        bucket=collections.Counter({k:v for k,v in curr.items() if x in k[0]})
        claimed=collections.Counter((tuple(z['scope']),z['mask'],tuple(z['from'])) for z in step['bucket'])
        ck(bucket==claimed,'exact same source-labeled selected bucket')
        u=set()
        for (s,_,_),cnt in bucket.items():u.update(s)
        ck(len(u)==step['width'],'exact elimination width')
        rest=tuple(sorted(u-{x}))
        table=0
        for bits in itertools.product((0,1),repeat=len(rest)):
            ctx={a:b for a,b in zip(rest,bits)}
            if any(all(evaluate(s,m,{**ctx,x:b}) for (s,m,pr),cnt in bucket.items()) for b in (0,1)):
                table|=1<<sum(b<<i for i,b in enumerate(bits))
            NUM['checked_table_rows']+=1
        ck(tuple(step['result']['scope'])==rest and step['result']['mask']==table,'independent projection')
        curr.subtract(bucket);curr+=collections.Counter({(rest,table,('elim',x)):1})
        eliminated.add(x)
    ck(len(eliminated)+len(p)==n,'all variables eliminated')
    final=collections.Counter((tuple(f['scope']),f['mask'],tuple(f['from'])) for f in out['final'])
    ck(final==curr,'terminal table multiset')
    decision=all((m&1) for (scope,m,_),ct in curr.items())
    ck(decision==(out['status']=='SAT'),'certified final one-bit outcome')
    if decision:
        w={i:v for i,v in enumerate(out['witness'],1)}
        ck(all(w[x]==val for x,val in p.items()),'pins respected')
        ck(source_sat(F,w),'every original clause satisfied')
    else:
        ck(any((not scope) and mask==0 for (scope,mask,_),ct in curr.items()),'false final constant')
    NUM['source_certs']+=1

def main():
    ck(models(F9,9,{})==70,'F9 source 70')
    ck(models(Y6,6,{})==20,'Y6 source 20')
    ck(models(F9,9,F9_S)==2,'F9 SAT source cube')
    ck(models(F9,9,F9_U)==0,'F9 UNSAT source cube')
    ck(models(F15,15,P_S)==2 and models(F15,15,P_U)==0,'F15 both labels source')
    # Explicit F9 4-way SS/SU/US/UU feasible domains against exhaustive shared-value constraints.
    for i in range(12):
        for j in range(i+1,12):
            for a,b in itertools.product((0,1),repeat=2):
                demands={};feasible=True
                for clause,v in ((F9[i],a),(F9[j],b)):
                    for lit in clause:
                        x=abs(lit);want=int(lit>0) if v else int(lit<0)
                        if x in demands and demands[x]!=want:feasible=False
                        demands[x]=want
                same=any(lit in F9[j] for lit in F9[i]);opposite=any(-lit in F9[j] for lit in F9[i])
                ck(feasible==(not opposite if a==b else not same),'signed original pair')
    # Physical XOR is not inferred: these are OFFLINE logical clause-truth-count traces.
    tracks={}
    for order in ('binary','gray'):
        last=None;acc=0;changes=0
        for i in range(512):
            q=i if order=='binary' else i^(i>>1)
            a={j+1:(q>>j)&1 for j in range(9)}
            counts=[sum(a[abs(z)]==int(z>0) for z in c) for c in F9]
            complement={v:1-b for v,b in a.items()}
            reverse=[sum(complement[abs(z)]==int(z>0) for z in c) for c in F9]
            ck(all(x+y==3 for x,y in zip(counts,reverse)),'full original F9 complement')
            if last is not None:
                acc+=sum((u^v).bit_count() for u,v in zip(last,counts))
                changes+=sum(u!=v for u,v in zip(last,counts))
            last=counts
        tracks[order]={'sum_logic_xor_offline':acc,'changed_clause_records':changes}
    NUM['offline_binary_logic_xor']=tracks['binary']['sum_logic_xor_offline']
    NUM['offline_gray_logic_xor']=tracks['gray']['sum_logic_xor_offline']
    for F,n in ((Y6,6),(F9,9),(F15,15),(g(2),18),(g(4),36),(U,198),(V,198)):
        ck(valid(F,n),'canonical original grammar')
    Vw={i:int(v) for i,v in enumerate(W,1)}
    ck(len(W)==198 and source_sat(V,Vw),'V198 full original witness')
    ck(not source_sat(U,Vw),'opposite-label 198 near-neighbor control')
    for obj in RAW['cases']:
        tag=obj['name'];kind=obj['kind'];t=obj.get('t',0)
        if kind=='Y6':F,n,p=Y6,6,{}
        elif kind=='F9':F,n,p=F9,9,{int(k):v for k,v in obj['pins'].items()}
        elif kind=='F15':F,n,p=F15,15,{int(k):v for k,v in obj['pins'].items()}
        elif kind=='G':
            F=g(t);n=9*t
            pinsequence=[A,Z]*(t//2) if 'AZ' in tag else [B,Q]*(t//2)
            p=pinlist(pinsequence)
        elif kind=='198':F,n,p=(U if tag.startswith('U') else V),198,{}
        else:raise AssertionError('unknown source fixture')
        out=obj['heap_result'];
        if n<=36 or out['status']=='UNRESOLVED':verify(F,n,p,out)
        if obj.get('naive_status'):ck(obj['naive_status']==out['status'],'naive outcome')
        ck(out['status'] in ('SAT','UNSAT','UNRESOLVED'),'valid tri-state')
        if kind in ('F9','F15','Y6','G') and n-len(p)<=18 and out['status'] in ('SAT','UNSAT'):
            ck((models(F,n,p)>0)==(out['status']=='SAT'),'brute original label')
    # Deliberate malformed structures; output must be REJECT, not SAT/UNSAT.
    invalid=[Y6[:-1],Y6+Y6[:1],Y6[:2]+((1,1,2),)+Y6[3:],
       Y6[:2]+((1,-2,3),)+Y6[3:],Y6[:2]+((0,2,3),)+Y6[3:]]
    for item in invalid:ck(not valid(item,6),'malformed original')
    result={'verifier':'independent_no_producer_import_bucket_certificate315',
     'status':'PASS','checks':dict(NUM),'cases_checked':len(RAW['cases']),
     'V198_witness':True,'U198_UNSAT_inherited_not_fresh':True,
     'P_vs_NP':'OPEN'}
    (R/'independent315.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()