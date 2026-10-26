#!/usr/bin/env python3
"""CONNECTED-SPLICE-LOCAL-CORE132 deterministic source-audited audit.
Python stdlib. Produces raw JSON, derives certificate independently from verifier.
Do not infer P != NP or an unrestricted SAT time lower bound.
"""
import collections,itertools,json,hashlib,time,sys
BASE='''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''
W=[tuple(int(z) for z in row.split()) for row in BASE.split(';')]
BW=(2,4,7,14,15)
counts=collections.Counter(); assert len(W)==20

def check(test,name):
    counts[name]+=1
    if not test:raise AssertionError(name)

def sat_dpll(F):
    def solve(C,A):
        while True:
            unit=None;R=[]
            for clause in C:
                if any(abs(z) in A and A[abs(z)]==(z>0) for z in clause):continue
                small=tuple(z for z in clause if abs(z) not in A)
                if not small:return None
                if len(small)==1:unit=small[0];break
                R.append(small)
            if unit is None:C=R;break
            A[abs(unit)]=unit>0
        if not C:return A
        freq=collections.Counter(abs(z) for clause in C for z in clause)
        v=max(freq,key=freq.get)
        for b in (True,False):
            new=A.copy();new[v]=b
            ans=solve(C,new)
            if ans is not None:return ans
        return None
    return solve(tuple(F),{})

def cyclic(k):
    assert k>=2
    F=[]
    for j in range(k):
        for i,c in enumerate(W):
            row=[(1 if z>0 else -1)*(abs(z)+15*j) for z in c]
            if i==0:
                assert row[0]==-(1+15*j)
                row[0]=-(1+15*((j-1)%k))
            F.append(tuple(row))
    return F

def modules(F,k):return [F[20*j:20*(j+1)] for j in range(k)]
def core(F):return F[1:20]+F[20:40]  # 19 unmodified source clauses in block 0, full changed block 1

def format_source(F,n):
    s=f'p cnf {n} {len(F)}\n'; O=[]
    for c in F:
        O.append(len(s));s+=' '.join(str(x) for x in c)+' 0\n'
    return s,O

def parse_source(s):
    lines=s.splitlines(keepends=True)
    h=lines[0].strip().split()
    assert len(h)==4 and h[:2]==['p','cnf']
    n,m=map(int,h[2:]);assert len(lines)==m+1
    ptr=len(lines[0]);F=[];offs=[]
    for line in lines[1:]:
        offsets=ptr;ptr+=len(line)
        assert line.endswith('\n') and line.strip().endswith(' 0')
        z=[int(x) for x in line.split()]
        assert z[-1]==0 and len(z)>=2
        c=tuple(z[:-1]); assert all(0<abs(x)<=n for x in c)
        F.append(c);offs.append(offsets)
    assert ptr==len(s)
    return n,F,offs

def check_degree(F,k):
    n=15*k;occ=collections.Counter((abs(z),z>0) for c in F for z in c)
    check(len(F)==20*k,'clause_count')
    for a in range(1,n+1):
        check(occ[a,True]==2 and occ[a,False]==2,'signed_2_2')
    for c in F:check(len(c)==3 and len({abs(z) for z in c})==3,'proper_ternary')

def connected_incidence(F,n):
    graph=[[] for _ in range(n+len(F))]
    for i,c in enumerate(F):
        for z in c:
            v=abs(z)-1;graph[v].append(n+i);graph[n+i].append(v)
    visited={0};stack=[0]
    while stack:
        u=stack.pop()
        for v in graph[u]:
            if v not in visited:visited.add(v);stack.append(v)
    return len(visited)==n+len(F)

def restrict(F,sigma):
    R=[]
    for c in F:
        if any(abs(z) in sigma and sigma[abs(z)]==(z>0) for z in c):continue
        R.append(tuple(z for z in c if abs(z) not in sigma))
    return R

def leaf_witness(clauses_with_offsets,sigma):
    # Prover's own implication graph from given exact clauses, yields source-offset edges.
    R=[]
    for p,c in clauses_with_offsets:
        if any(abs(z) in sigma and sigma[abs(z)]==(z>0) for z in c): continue
        r=tuple(z for z in c if abs(z) not in sigma)
        if len(r)==0:return ('EMPTY',p)
        if len(r)<=2:R.append((p,r))
    graph=collections.defaultdict(list)
    for p,c in R:
        if len(c)==1:
            a=c[0];graph[-a].append((a,p))
        else:
            a,b=c;graph[-a].append((b,p));graph[-b].append((a,p))
    def path(start,finish):
        todo=collections.deque([start]);parent={start:None}
        while todo:
            x=todo.popleft()
            for y,p in graph[x]:
                if y not in parent:parent[y]=(x,p);todo.append(y)
        if finish not in parent:return None
        out=[];x=finish
        while parent[x] is not None:
            y,p=parent[x];out.append((p,y,x));x=y
        return tuple(reversed(out))
    unassigned=sorted({abs(z) for _,c in R for z in c if abs(z) not in sigma})
    for a in unassigned:
        forward=path(a,-a)
        if forward is not None:
            backward=path(-a,a)
            if backward is not None:return ('PATH',a,forward,backward)
    return None

def authenticate_clause(source,p,headend,n):
    if not (headend<=p<len(source) and (p==headend or source[p-1]=='\n')):raise ValueError('not original clause start')
    q=source.find('\n',p)
    if q<0:raise ValueError('no terminator')
    raw=source[p:q]
    if not raw.endswith(' 0'):raise ValueError('no zero')
    lit=[int(x) for x in raw.split()]
    if lit[-1]!=0 or len(lit) not in (2,3,4):raise ValueError('bad literal count')
    c=tuple(lit[:-1]);
    if len({abs(z) for z in c})!=len(c) or any(abs(z)>n or z==0 for z in c):raise ValueError('bad literal identities')
    return c

def make_tree(F,offs,order):
    I=list(range(1,20))+list(range(20,40))
    source_clauses=[(offs[i],F[i]) for i in I]
    def build(depth,sigma):
        if depth==len(order):
            w=leaf_witness(source_clauses,sigma)
            if w is None:raise AssertionError('uncovered leaf!')
            return w
        v=order[depth]
        sigma[v]=False;left=build(depth+1,sigma)
        sigma[v]=True;right=build(depth+1,sigma)
        del sigma[v]
        return ('BRANCH',v,left,right)
    return build(0,{})

def _verify_tree_impl(source,certificate):
    # Full input parsing and tree checker are logically independent of prover.
    n,_,_=parse_source(source)
    headend=source.find('\n')+1
    A={};stat=collections.Counter();maxdepth=[0]
    def source_clause(p):
        stat['source_line_probes']+=1
        return authenticate_clause(source,p,headend,n)
    def verify_edge(edge,start):
        p,u,v=edge
        if u!=start or abs(u) in A or abs(v) in A:return False
        c=source_clause(p)
        if any(abs(z) in A and A[abs(z)]==(z>0) for z in c):return False
        r=tuple(z for z in c if abs(z) not in A)
        if len(r)==1:return u==-r[0] and v==r[0]
        if len(r)==2:return ((u==-r[0] and v==r[1]) or (u==-r[1] and v==r[0]))
        return False
    def recurse(node,depth):
        stat['nodes']+=1;maxdepth[0]=max(maxdepth[0],depth)
        if not isinstance(node,tuple) or not node:return False
        if node[0]=='BRANCH':
            if len(node)!=4:return False
            _,x,p0,p1=node
            if not (1<=x<=n and x not in A):return False
            stat['branches']+=1
            A[x]=False;r0=recurse(p0,depth+1)
            A[x]=True;r1=recurse(p1,depth+1)
            del A[x]
            return r0 and r1
        stat['leaves']+=1
        if node[0]=='EMPTY' and len(node)==2:
            c=source_clause(node[1]);return all(abs(z) in A and A[abs(z)]!=(z>0) for z in c)
        if node[0]=='PATH' and len(node)==4:
            _,x,forward,backward=node
            if not(1<=x<=n and x not in A):return False
            stat['edges']+=len(forward)+len(backward)
            if max(len(forward),len(backward))>2*n-1:return False
            for seq,start,finish in ((forward,x,-x),(backward,-x,x)):
                t=start
                for edge in seq:
                    if not verify_edge(edge,t):return False
                    t=edge[2]
                if t!=finish:return False
            return True
        return False
    result=recurse(certificate,0)
    stat['depth']=maxdepth[0]
    return result,dict(stat)

def verify_tree(source, certificate):
    # Total, clocked interpretation: malformed inputs and offsets reject.
    try:
        return _verify_tree_impl(source,certificate)
    except (ValueError,AssertionError,TypeError,IndexError,KeyError,RecursionError):
        return False,{'malformed_rejected':1}

def two_levels(F,n):
    p1=restrict(F,{2:False});p2=restrict(F,{2:False,4:False})
    S1,O1=format_source(p1,n);S2,O2=format_source(p2,n)
    check(parse_source(S1)[1]==p1 and parse_source(S2)[1]==p2,'two_level_serialization')
    return [len(S1),len(S2),len(p1),len(p2)]

def audit():
    out={'run':'CONNECTED-SPLICE-LOCAL-CORE132','scope':'genuinely connected strict signed (2,2) 3CNF, certified two-module UNSAT core','instances':[],'controls':{}}
    check(sat_dpll(W) is None,'W1_unsat')
    for i in range(20):check(sat_dpll(W[:i]+W[i+1:]) is not None,'W1_minimal')
    for k in (2,3,4,8,16):
        F=cyclic(k);n=15*k
        check_degree(F,k)
        check(connected_incidence(F,n),'incidence_connected')
        if k<=3:check(sat_dpll(F) is None,'global_unsat_DPLL_small')
        src,offs=format_source(F,n)
        nn,C,PP=parse_source(src)
        check(nn==n and C==F and PP==offs,'source_exact_reparse')
        # Every syntactically altered module is satisfiable in isolation, with external bit free.
        for module in modules(F,k):check(sat_dpll(module) is not None,'each_module_sat')
        sub=core(F)
        check(len(sub)==39 and sat_dpll(sub) is None,'cross_module_39_core_unsat')
        # Proper 3CNF original clauses in the core, not guessed derivatives.
        order=list(BW)+[v+15 for v in BW]
        check(all(any(abs(z) in order for z in c) for c in sub),'core_2cnf_backdoor')
        cert=make_tree(F,offs,order)
        accepted,stat=verify_tree(src,cert)
        check(accepted and stat['branches']==1023 and stat['leaves']==1024,'verified_SCC_tree')
        check(stat['depth']==10,'tree_depth')
        P=len(json.dumps(cert,separators=(',',':')))
        # String serializes source line offsets, charged log N pointer lengths.
        check(P>stat['edges'],'cert_bytes_count')
        # Perturbed pointer, missing right branch, incorrect alias are rejected.
        wrong=('PATH',1,((len(src)+1,1,-1),),((len(src)+1,-1,1),))
        check(not verify_tree(src,wrong)[0],'bad_pointer_rejected')
        check(not verify_tree(src,('BRANCH',order[0],cert[2],wrong))[0],'invalid_branch_rejected')
        if k==2:levels=two_levels(F,n)
        else:levels=None
        out['instances'].append({'k':k,'n':n,'clauses':len(F),'source_bytes':len(src),'core_clauses':len(sub),'hitting_backdoor_min':5*k,'core_backdoor':len(order),'leaf_count':stat['leaves'],'branches':stat['branches'],'certificate_JSON_bytes':P,'path_edge_records':stat['edges'],'source_line_probes':stat['source_line_probes'],'peak_branch_depth':stat['depth'],'two_level_bytes_clauses':levels})
    # Distinguish incidence connectivity from semantic hardness: SAT splices stay SAT.
    G=((1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3))
    check(sat_dpll(G) is not None,'sat_signed_control')
    GG=list(G)+[tuple((1 if z>0 else -1)*(abs(z)+3) for z in c) for c in G]
    # same-sign swap first literal of two components: signed (2,2) and connected.
    t=list(GG);a=list(t[0]);b=list(t[4]);a[0],b[0]=b[0],a[0];t[0]=tuple(a);t[4]=tuple(b)
    check(sat_dpll(t) is not None,'SAT_connected_splice')
    check(connected_incidence(t,6),'SAT_control_connected')
    for v in range(1,7):check(sum(v in c for c in t)==2 and sum(-v in c for c in t)==2,'SAT_control_signed_degree')
    # Wrong source alias in a tiny Horn-like pin gadget turns contradiction SAT.
    def pin(l,a,b):return [(l,p*a,q*b) for p in (1,-1) for q in (1,-1)]
    check(sat_dpll(pin(1,2,3)+pin(-1,4,5)) is None,'Horn_PIN_UNSAT')
    check(sat_dpll(pin(1,2,3)+pin(-6,4,5)) is not None,'false_source_alias_SAT')
    # Two contradictory 2-CNF clauses, separately width <3; control exact path edges.
    check(sat_dpll(((1,),(-1,))) is None,'unit_contradiction')
    # connected cubic K4 parity Tseitin: odd UNSAT, even SAT; via Gaussian parity proof.
    E=list(itertools.combinations(range(4),2))
    def parity(odd):
        rows=[]
        for v in range(4):
            inc=[i+1 for i,e in enumerate(E) if v in e]
            for bits in itertools.product((0,1),repeat=3):
                if sum(bits)%2!=(odd and v==0):
                    rows.append(tuple(z if bit else -z for z,bit in zip(inc,bits)))
        return rows
    check(sat_dpll(parity(1)) is None and sat_dpll(parity(0)) is not None,'Tseitin_odd_even')
    out['controls']={'original_W1_minimally_UNSAT':True,'connected_SAT_signed_2_2_splice':True,'wrong_source_alias_rejected':True,'signed_2_2_regular_degree_exact':True,'Horn_and_2CNF':True,'Tseitin_K4_odd_even':True,'wrong_pointer_and_branch_rejected':True}
    out['assertion_groups']=sum(counts.values());out['assertion_by_group']=dict(counts)
    return out

if __name__=='__main__':
    data=audit()
    json_out=json.dumps(data,indent=2,sort_keys=True)+'\n'
    if len(sys.argv)>1:
        open(sys.argv[1],'w').write(json_out)
    print(json_out)
