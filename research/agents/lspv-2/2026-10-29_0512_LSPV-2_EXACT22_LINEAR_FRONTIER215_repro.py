#!/usr/bin/env python3
"""Self-contained finite controls for LSPV-2 EXACT22-LINEAR-FRONTIER215.
The theorem's asymptotic construction is NONEXPLICIT probabilistic existence.
The finite sample generator below does not certify the asymptotic guarantee.
No external libraries required.
"""
import itertools, math, random, json, hashlib, sys
from collections import deque

class Dinic:
    def __init__(self,n):
        self.g=[[] for _ in range(n)]
    def add(self,u,v,c):
        a=[v,c,len(self.g[v])]; b=[u,0,len(self.g[u])]
        self.g[u].append(a); self.g[v].append(b)
        return a
    def flow(self,s,t):
        tot=0
        while True:
            level=[-1]*len(self.g); level[s]=0; dq=deque([s])
            while dq:
                u=dq.popleft()
                for v,c,_ in self.g[u]:
                    if c>0 and level[v]<0:level[v]=level[u]+1; dq.append(v)
            if level[t]<0:break
            cursor=[0]*len(self.g)
            def send(u,f):
                if u==t:return f
                while cursor[u]<len(self.g[u]):
                    edge=self.g[u][cursor[u]]; v,c,back=edge
                    if c and level[v]==level[u]+1:
                        z=send(v,min(f,c))
                        if z:
                            edge[1]-=z; self.g[v][back][1]+=z; return z
                    cursor[u]+=1
                return 0
            while True:
                x=send(s,10**9)
                if not x:break
                tot+=x
        return tot

def sign_clause_family(n,groups):
    m=len(groups); assert 3*m==4*n
    source=0; clause_offset=1; var_offset=1+m; sink=var_offset+n
    fn=Dinic(sink+1); edges={}
    for j,tri in enumerate(groups):
        fn.add(source,clause_offset+j,1)
        for v in tri:
            edges[(j,v)]=fn.add(clause_offset+j,var_offset+v,1)
    for v in range(n):fn.add(var_offset+v,sink,2)
    assert fn.flow(source,sink)==m, 'b-matching failed'
    neg=set(); used=[0]*n
    for (j,v),edge in edges.items():
        if edge[1]==0:neg.add((j,v)); used[v]+=1
    assert all(x<=2 for x in used)
    for v in range(n):
        for j,tri in enumerate(groups):
            if used[v]==2:break
            if v in tri and (j,v) not in neg:
                neg.add((j,v)); used[v]+=1
    assert all(x==2 for x in used)
    clauses=[tuple(-(v+1) if (j,v) in neg else (v+1) for v in tri) for j,tri in enumerate(groups)]
    assert all(any(x<0 for x in c) for c in clauses)
    return clauses

def make_family(n,seed):
    assert n%6==0 and n>=6
    r=n//3
    A=[(3*j,3*j+1,3*j+2) for j in range(r)]
    B=[(3*j+1,3*j+2,3*((j+1)%r)) for j in range(r)]
    base=A+B; assert len(set(map(frozenset,base)))==len(base)
    rng=random.Random(seed)
    for trial in range(20000):
        C=[]; D=[]
        for layer in (C,D):
            order=list(range(n)); rng.shuffle(order)
            layer.extend(tuple(order[3*j:3*j+3]) for j in range(r))
        groups=base+C+D
        if len(set(map(frozenset,groups)))==len(groups):
            return groups,trial
    raise RuntimeError('could not find collision-free 4-partition source')

def verify_source(n,groups,clauses):
    assert len(groups)==len(clauses)==4*n//3
    counts=[[0,0] for _ in range(n)]
    for tri,c in zip(groups,clauses):
        assert len(set(tri))==3 and len(c)==3
        assert {abs(x)-1 for x in c}==set(tri)
        for lit in c:counts[abs(lit)-1][int(lit>0)]+=1
    assert all(a==b==2 for a,b in counts)
    assert all(any(lit<0 for lit in c) for c in clauses)
    adj=[set() for _ in range(n)]
    for tri in groups:
        for a,b in itertools.combinations(tri,2):adj[a].add(b);adj[b].add(a)
    seen={0};stack=[0]
    while stack:
        for w in adj[stack.pop()]:
            if w not in seen:seen.add(w);stack.append(w)
    assert len(seen)==n
    assert all(any(lit<0 for lit in c) for c in clauses), 'allzero witness fails'
    return counts

def dimacs(n,clauses):
    data=f'p cnf {n} {len(clauses)}\n'
    data+=''.join(' '.join(map(str,cl))+' 0\n' for cl in clauses)
    return data.encode('ascii')

def parse_dimacs(raw):
    try:
        lines=raw.decode('ascii').splitlines()
        if not lines or len(lines[0].split())!=4: return None
        p,cnf,ns,ms=lines[0].split()
        if (p,cnf)!=('p','cnf'):return None
        n=int(ns); m=int(ms)
        if n<=0 or m<0 or len(lines)!=m+1:return None
        clauses=[]
        for line in lines[1:]:
            vals=list(map(int,line.split()))
            if len(vals)!=4 or vals[-1]!=0 or any(v==0 or abs(v)>n for v in vals[:3]):return None
            if len({abs(v) for v in vals[:3]})!=3:return None
            clauses.append(tuple(vals[:3]))
        return n,clauses
    except (UnicodeError,ValueError):return None

def brute_sat(n,clauses):
    for word in range(1<<n):
        if all(any(((word>>(abs(lit)-1))&1)==int(lit>0) for lit in c) for c in clauses):
            return True
    return False

def all_prefix_midpoint(n,groups):
    masks=[sum(1<<v for v in tri) for tri in groups]
    bestB=n+1;bestX=len(masks)+1;winner=None
    mid=n//2;total=0
    for tup in itertools.combinations(range(n),mid):
        U=sum(1<<x for x in tup); front=0; crossing=0
        for e in masks:
            p=e&U
            if p and p!=e:
                front|=p;crossing+=1
        b=front.bit_count(); total+=1
        if b<bestB:bestB=b;winner=tup
        if crossing<bestX:bestX=crossing
    assert total==math.comb(n,mid)
    return {'midpoint_subsets_checked':total,'minimum_live_processed':bestB,
            'minimum_crossing_clauses':bestX,'witness_prefix':list(winner)}

def glued_core(core_n, core_clauses, shell_n, shell_clauses):
    """Connected proper 3CNF projected exactly to arbitrary connected core.
    This glue is not exact22: boundary variable receives an extra use.
    """
    assert core_n>=3 and shell_n>=6
    shell_shift=core_n
    shell=[tuple((1 if lit>0 else -1)*(abs(lit)+shell_shift) for lit in cl)
            for cl in shell_clauses]
    t=core_n+shell_n+1;u=t+1;v=t+2
    force=[(t, su*u, sv*v) for su in (1,-1) for sv in (1,-1)]
    link=(1,core_n+1,t)
    return core_n+shell_n+3, list(core_clauses)+shell+force+[link]

def eval_clauses(clauses, bits):
    return all(any(((bits>>(abs(lit)-1))&1)==int(lit>0) for lit in c)
               for c in clauses)

def projection_controls():
    shell_groups,_=make_family(6,2026102905+6)
    shell=sign_clause_family(6,shell_groups)
    yes=[(1,2,3)]
    no=[tuple(s_i*(i+1) for i,s_i in enumerate(signs))
        for signs in itertools.product((-1,1),repeat=3)]
    assert len(no)==8
    tests=[]
    for label,core in (('SAT',yes),('UNSAT',no)):
        n,allclauses=glued_core(3,core,6,shell)
        assert n==12
        assert len({abs(lit) for clause in allclauses for lit in clause})==n
        checked=0
        for a in range(1<<3):
            want=eval_clauses(core,a)
            got=False
            for ext in range(1<<(n-3)):
                if eval_clauses(allclauses,a|(ext<<3)):
                    got=True;break
            assert want==got,(label,a,want,got)
            checked+=1
        tests.append({'core_side':label,'core_assignments_projected':checked,
                      'full_variable_count':n,'full_clause_count':len(allclauses),
                      'input_bits':len(dimacs(n,allclauses))*8,
                      'core_bits':len(dimacs(3,core))*8})
    sizes=[]
    for q in (6,12,24,48,96,384,1536):
        # A connected, satisfiable proper ordinary-3CNF core.
        core=[(i+1,(i+1)%q+1,(i+2)%q+1) for i in range(q)]
        n,g=glued_core(q,core,6,shell)
        M=len(dimacs(q,core))*8
        N=len(dimacs(n,g))*8
        sizes.append({'core_variables':q,'core_bits':M,'parent_bits':N,
                      'core_to_parent_ratio':M/N,
                      'core_exceeds_parent_pow_0p75':M>N**.75})
    return {'exact_projection_SAT_UNSAT':tests,
            'glued_core_size_controls':sizes,
            'claim':'shell-only source simplification retains core and fails universal power shrink; closure on arbitrary core absent'}

def audit():
    result={'run':'EXACT22-LINEAR-FRONTIER215',
      'scope':'connected proper strict signed exact-(2,2)-3CNF, allzero-satisfied controls',
      'instances':[],'assertions_failed':0}
    for n in (6,12,18,24):
        g,retries=make_family(n,seed=2026102905+n)
        c=sign_clause_family(n,g)
        counts=verify_source(n,g,c)
        raw=dimacs(n,c)
        assert parse_dimacs(raw)==(n,c)
        for malformed in (raw+b'garbage\n',raw.replace(b'p cnf',b'p cng',1), raw.replace(b' 0\n',b' 4\n',1)):
            assert parse_dimacs(malformed)!=(n,c)
        if n<=12:assert brute_sat(n,c)
        mid=all_prefix_midpoint(n,g)
        assert mid['minimum_crossing_clauses']<=4*mid['minimum_live_processed']
        instance={'n':n,'m':len(c),'literal_occurrences':3*len(c),
           'bytes':len(raw),'bits':8*len(raw),'sha256_dimacs':hashlib.sha256(raw).hexdigest(),
           'rejected_duplicate_partition_attempts':retries,
           'positive_negative_counts_all_2':True,'connected':True,
           'allzero_witness_verified':True,'brute_force_sat_checked':n<=12,
           **mid}
        result['instances'].append(instance)
    p=0.01; h=-(3*p)*math.log2(3*p)-(1-3*p)*math.log2(1-3*p)
    beta=-1/3+(2/3)*h+2*p*math.log2(3)
    result['asymptotic_union_bound']={'epsilon':p,'H2_3epsilon':h,'exponent_beta':beta,
       'formula':'(n+1)^2*(n/3+1)^2*2^(beta*n)',
       'conclusion':'<1 for all sufficiently large multiples of 6; existence only'}
    result['connected_hard_core_glue']=projection_controls()
    result['no_unrestricted_SAT_claim']=True
    return result

if __name__=='__main__':
    print(json.dumps(audit(),indent=2,sort_keys=True))
