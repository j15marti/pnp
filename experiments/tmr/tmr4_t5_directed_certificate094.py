#!/usr/bin/env python3
"""TMR-4/094 full loopless directed adjacency-matrix source bit-probe audit.

Counts all 2^[n(n-1)] directed sources for 1<=n<=5, retaining
both arcs of a two-cycle as distinct possible bits. Exact counts by
five-color assignment histogram + superset zeta transform.
"""
import hashlib,itertools,json,random,time
from array import array

R=lambda a,b: ((b-a)%5 in (1,3))
SEED=20261118*100+94

def arcs(n):return [(i,j) for i in range(n) for j in range(n) if i!=j]

def encode(n,mask):
    if not isinstance(n,int) or not 1<=n<=5:raise ValueError('invalid n for the tested representation')
    m=n*(n-1)
    if not isinstance(mask,int) or not 0<=mask<2**m:raise ValueError('invalid mask')
    return (str(n)+':'+(format(mask,'0%db'%m) if m else '')+'\n').encode()

def decode(b):
    if not isinstance(b,bytes) or not b.endswith(b'\n') or b.count(b'\n')!=1 or b.count(b':')!=1:raise ValueError('bad source')
    a,c=b[:-1].split(b':');
    if not a.isdigit() or a.startswith(b'0') or (len(c)!=int(a)*(int(a)-1)) or any(z not in b'01' for z in c):raise ValueError('bad source bits')
    n=int(a);v=int(c,2) if c else 0
    if encode(n,v)!=b:raise ValueError('noncanonical')
    return n,v

def counts(n):
    pairs=arcs(n);M=len(pairs);tab=array('I',[0])*(1<<M)
    for colors in itertools.product(range(5),repeat=n):
        good=0
        for k,(i,j) in enumerate(pairs):
            if R(colors[i],colors[j]):good|=1<<k
        tab[good]+=1
    for k in range(M):
        bit=1<<k
        for block in range(0,1<<M,2*bit):
            for j in range(block,block+bit):tab[j]+=tab[j+bit]
    return tab

def balanced_colors(n):return [i%5 for i in range(n)]

def witness_certificate(n):
    pairs=arcs(n);col=balanced_colors(n)
    allowed=0
    for k,(i,j) in enumerate(pairs):
        if R(col[i],col[j]):allowed|=1<<k
    return len(pairs)-allowed.bit_count(),allowed,col

def num_edges(n):return n*(n-1)

def directly(n,mask):
    edges=[(i,j) for k,(i,j) in enumerate(arcs(n)) if mask&(1<<k)]
    return sum(all(R(x[i],x[j]) for i,j in edges) for x in itertools.product(range(5),repeat=n))

def cnf(n,mask):
    clauses=[]
    def no_color(i,v):return [(-(3*i+b+1) if v&(1<<b) else 3*i+b+1) for b in range(3)]
    for i in range(n):
        for v in range(5,8):clauses.append(no_color(i,v))
    for k,(i,j) in enumerate(arcs(n)):
        if mask&(1<<k):
            for a in range(5):
                for b in range(5):
                    if not R(a,b):clauses.append(no_color(i,a)+no_color(j,b))
    return clauses

def cnf_val(clauses,x):
    bits=[(v>>b)&1 for v in x for b in range(3)]
    return all(any((bits[abs(l)-1]==1)==(l>0) for l in c) for c in clauses)

def run():
    rng=random.Random(SEED);start=time.perf_counter()
    malformed=[b'5:'+b'0'*19+b'\n',b'05:'+b'0'*20+b'\n',b'5:'+b'1'*21+b'\n',b'5:'+b'0'*20+b'X\n',b'5:'+b'0'*20,b'1:0\n',b'0:\n']
    gates={'source_sha256':0,'malformed_rejected':0,'exhaustive_source_graphs':0,
           'original_assignment_recounts':0,'complete_certificate_completions':0,
           'cnf_validity_checks':0,'invalid_codes':0,'domain_pairs':0}
    for b in malformed:
        try:decode(b)
        except ValueError:gates['malformed_rejected']+=1
        else:raise AssertionError('malformed source passed')
    rows=[]
    for n in range(1,6):
        tab=counts(n);M=num_edges(n);q,allowed,col=witness_certificate(n)
        assert decode(encode(n,0))==(n,0)
        sha=hashlib.sha256(encode(n,0)).hexdigest();gates['source_sha256']+=1
        assert tab[0]==5**n
        max_arcs=max(k.bit_count() for k,val in enumerate(tab) if val)
        t5=(2*n*n)//5
        assert max_arcs==t5,(n,max_arcs,t5)
        assert q==M-t5 and allowed.bit_count()==t5
        assert all(R(col[i],col[j]) for k,(i,j) in enumerate(arcs(n)) if allowed&(1<<k))
        sat_graphs=sum(x!=0 for x in tab)
        maximizers=sum(x!=0 and k.bit_count()==max_arcs for k,x in enumerate(tab))
        gates['exhaustive_source_graphs']+=len(tab)
        # Entire downset of any permitted-arc certificate remains satisfiable.
        positions=[k for k in range(M) if allowed&(1<<k)]
        for subset in range(1<<len(positions)):
            mask=sum(1<<p for b,p in enumerate(positions) if subset&(1<<b))
            assert tab[mask]>0
            gates['complete_certificate_completions']+=1
        for rep in range(20):
            mask=rng.randrange(len(tab))
            assert tab[mask]==directly(n,mask)
            gates['original_assignment_recounts']+=1
            cls=cnf(n,mask);assert len(cls)==3*n+15*mask.bit_count()
            for _ in range(20):
                vals=[rng.randrange(8) for _ in range(n)]
                want=all(v<5 for v in vals) and all(R(vals[i],vals[j]) for k,(i,j) in enumerate(arcs(n)) if mask&(1<<k))
                assert cnf_val(cls,vals)==want
                gates['cnf_validity_checks']+=1
                if any(v>=5 for v in vals):gates['invalid_codes']+=1
        rows.append({'n':n,'source_bits':M,'sha256_empty':sha,'all_sources':len(tab),
              'sat_sources':sat_graphs,'unsat_sources':len(tab)-sat_graphs,
              'max_sat_arcs':max_arcs,'max_sat_arc_graphs':maximizers,
              'certificate_queries':q,'unqueried_arcs':t5,
              'empty_assignment_count':str(tab[0]),'width_empty_complete_obdd':1,
              'nodes_empty_complete_obdd':n,'empty_fixed_cnf_clauses':3*n})
    for rev in (False,True):
      for X in range(32):
       for Y in range(32):
        a=b=A=B=0
        for x in range(5):
         for y in range(5):
          if X&(1<<x) and Y&(1<<y) and (R(y,x) if rev else R(x,y)):
           a|=1<<x;b|=1<<y
        for x in range(8):
         for y in range(8):
          if x<5 and y<5 and X&(1<<x) and Y&(1<<y) and (R(y,x) if rev else R(x,y)):
           A|=1<<x;B|=1<<y
        assert (a,b)==(A,B);gates['domain_pairs']+=1
    return {'experiment':'TMR4_094_FULL_DIRECTED_SOURCE','theorem':'C_SAT(empty)=n(n-1)-floor(2n^2/5)',
            'source':'loopless labeled digraph adjacency bits all ordered pairs distinct',
            'seed':SEED,'gates':gates,'rows':rows,
            'run_seconds':round(time.perf_counter()-start,3),'unexpected_failures':0}

if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
