#!/usr/bin/env python3
"""Independent LSPV-3 SPLIT-GAP344 referee. Python standard library only.
Input: results/raw/arc/2026-11-02_1442_LSPV3_SPLIT_GAP344.json
Does not import the JavaScript producer.
"""
import heapq, json, sys
from itertools import product
BASE=[[-3,1,4],[-1,2],[1,3],[-4,-3],[-2,-1,3],[-2,4]]
ASSERTIONS=0
def ck(cond,why):
    global ASSERTIONS
    ASSERTIONS+=1
    if not cond: raise AssertionError(why)
def norm(c): return sorted(set(c),key=lambda x:(abs(x),x))
def sat(c,a): return any(a[abs(x)]==(x>0) for x in c)
def source(t):
    h=[(0,0,())]; order=0
    for i in range(1,t+1):
        dep,_,path=heapq.heappop(h)
        for side in (0,1):
            order+=1
            heapq.heappush(h,(dep+1,order,path+((4+i,side),)))
    leaves=[norm(BASE[0]+[v if side==0 else -v for v,side in path]) for _,_,path in sorted(h,key=lambda x:x[2])]
    return leaves+[norm(c) for c in BASE[1:]]
def check_proof(form,steps):
    known={'s%d'%i:norm(c) for i,c in enumerate(form)}
    for j,s in enumerate(steps):
        a,b=s['parents']; p=s['pivot']
        ck(s['id']=='d%d'%j and s['rule']=='RES' and a in known and b in known,'bad order')
        ck((p in known[a] and -p in known[b]) or (-p in known[a] and p in known[b]),'bad pivot')
        result=set(known[a]+known[b])-{p,-p}
        ck(not any(-v in result for v in result),'tautological resolvent')
        ck(norm(result)==s['clause'],'wrong resolvent')
        known[s['id']]=norm(result)
    ck(bool(steps) and known[steps[-1]['id']]==[],'no contradiction')
def base_tree():
    def truth(c):
        return sum(1<<a for a in range(16) if sat(c,[False]+[bool((a>>j)&1) for j in range(4)]))
    def row(mask,rhs):
        return sum(1<<a for a in range(16) if ((a&mask).bit_count()&1)==rhs)
    ca={}
    for digits in product((0,1,-1),repeat=4):
        clause=[(i+1)*sgn for i,sgn in enumerate(digits) if sgn]
        ca[truth(clause)]=clause
    ra={row(mask,rhs):(mask,rhs) for mask in range(16) for rhs in (0,1)}
    def support(t):
        return sum(1<<i for i in range(4) if any(((t>>a)&1)!=((t>>(a^(1<<i)))&1) for a in range(16)))
    dp=[set() for _ in range(64)]
    for i,c in enumerate(BASE): dp[1<<i].add(truth(c))
    counts=[6];pairs=0
    for size in range(2,7):
        layer=0
        for mask in range(1,64):
            if mask.bit_count()!=size: continue
            a=(mask-1)&mask
            while a:
                b=mask^a
                if a<b:
                    for x in dp[a]:
                        for y in dp[b]:
                            pairs+=1
                            if (support(x)|support(y)).bit_count()<=3: dp[mask].add(x&y)
                            if x in ra and y in ra:
                                um,ur=ra[x];vm,vr=ra[y]
                                dp[mask].add(row(um^vm,ur^vr))
                            if x in ca and y in ca:
                                for pivot in ca[x]:
                                    if -pivot in ca[y]:
                                        r=set(ca[x]+ca[y])-{pivot,-pivot}
                                        if not any(-v in r for v in r): dp[mask].add(truth(r))
                a=(a-1)&mask
            layer+=len(dp[mask])
        counts.append(layer)
    ck(0 not in dp[63],'5-node mixed read-once refutation exists')
    ck(counts==[6,18,46,84,112,54] and pairs==844,'base optimizer mismatches')
def main(fn):
    obj=json.load(open(fn,encoding='utf-8'))
    ck(obj['version']=='LSPV3-SPLIT-GAP344/v1','version')
    check_cases=[0,1,2,3,7,15,31,63,127]
    ck([x['t'] for x in obj['cases']]==check_cases,'test cases')
    base_tree()
    controls=0;deletions=0;flips=0
    for rec in obj['cases']:
        t=rec['t'];F=source(t);n=t+4
        ck(len(F)==t+6==rec['m'] and rec['q']==t+6,'count')
        ck(sum(map(len,F))==rec['sourceLiterals'],'literal count')
        ck(max(map(len,F))==rec['maxWidth'],'max width')
        dimacs='p cnf %d %d\n'%(n,len(F))+''.join(' '.join(map(str,c))+' 0\n' for c in F)
        ck(len(dimacs.encode('ascii'))*8==rec['Nbits'],'bit encoding')
        controls+=1
        if t<=3:
            test=rec['sample']
            ck(test['source']==F,'wrong clauses')
            check_proof(F,test['nodes'])
            for i,w in enumerate(test['witnesses']):
                a=[False]+[v=='1' for v in w]
                ck(not sat(F[i],a) and all(sat(c,a) for j,c in enumerate(F) if j!=i),'bad witness')
            ck(not any(all(sat(c,[False]+[bool((a>>j)&1) for j in range(n)]) for c in F)
                       for a in range(1<<n)),'SAT formula called UNSAT')
            bad=[dict(r) for r in test['nodes']];bad[0]['pivot']=999
            try: check_proof(F,bad)
            except AssertionError: pass
            else: raise AssertionError('corrupted proof accepted')
        # Independent construction of deletion witnesses, for all sizes.
        Bw=[]
        for k in range(6):
            one=next(([False]+[bool((a>>j)&1) for j in range(4)] for a in range(16)
                      if not sat(BASE[k],[False]+[bool((a>>j)&1) for j in range(4)])
                      and all(sat(c,[False]+[bool((a>>j)&1) for j in range(4)])
                              for j,c in enumerate(BASE) if j!=k)),None)
            ck(one is not None,'base deletion witness');Bw.append(one)
        for i,c in enumerate(F):
            bits=[False]*(n+1);bits[:5]=Bw[0 if i<t+1 else i-t]
            if i<t+1:
                for lit in c:
                    if abs(lit)>4:bits[abs(lit)]=(lit<0)
            ck(not sat(c,bits) and all(sat(d,bits) for j,d in enumerate(F) if j!=i),'deletion failure')
            deletions+=1
            for j,lit in enumerate(c):
                changed=c[:];changed[j]=-lit
                ck(sat(changed,bits),'sign flip fails')
                flips+=1
    print(json.dumps({'status':'PASS','assertions':ASSERTIONS,'cases':controls,
                      'deletion_witnesses':deletions,'sign_flip_witnesses':flips,
                      'base_read_once_count_layers':[6,18,46,84,112,54],
                      'small_full_cubes':240,'corrupt_pivots_rejected':4},indent=2))
if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else
         'results/raw/arc/2026-11-02_1442_LSPV3_SPLIT_GAP344.json')
