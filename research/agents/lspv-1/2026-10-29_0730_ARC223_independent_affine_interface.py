#!/usr/bin/env python3
"""ARC223: independent-affine-interface exact 2SAT quotient.

Self-contained research reproducer. On a source-recognized XOR3-quartet +
unit/binary CNF, computes affine parametrization. If distinct nonzero forms
appearing in remaining clauses are linearly independent, reparametrizes those
forms as independent Boolean coordinates and decides the resulting 2SAT.

Answers: YES with source-checked assignment, NO with checkable affine XOR
conflict or two implication paths, otherwise UNKNOWN. It does NOT decide
arbitrary mixed 2SAT+XOR3 or prove anything about P versus NP.
"""
from collections import defaultdict, deque, Counter
from itertools import combinations, product
from hashlib import sha256
import random, json, math, time

SEED=22320261029
YES_BASE=b'p cnf 3 1\n1 2 3 0\n'
NO_BASE=b'p cnf 1 2\n1 0\n-1 0\n'

def canon(c):
    c=tuple(sorted(c,key=lambda x:(abs(x),x<0)))
    if not c or any(abs(c[i])==abs(c[j]) for i in range(len(c)) for j in range(i)):
        raise ValueError('empty/repeated-variable clause')
    return c

def encode(n,cs):
    return (f'p cnf {n} {len(cs)}\n'+''.join(' '.join(map(str,canon(c)))+' 0\n' for c in cs)).encode()

def parse(data):
    try:
        lines=data.decode('ascii').splitlines(keepends=True)
        if not lines or any(not line.endswith('\n') for line in lines):raise ValueError('newline')
        head=lines[0].split()
        if head[:2]!=['p','cnf'] or len(head)!=4: raise ValueError('header')
        n,m=map(int,head[2:]);
        if n<1 or m<0 or n>len(data)+1 or m>len(data) or len(lines)!=m+1:
            raise ValueError('size')
        cs=[];offs=[];pos=len(lines[0])
        for line in lines[1:]:
            z=list(map(int,line.split()))
            if not z or z[-1]!=0 or 0 in z[:-1] or len(z)>4:raise ValueError('clause')
            c=canon(z[:-1]);
            if any(abs(l)>n for l in c):raise ValueError('variable')
            cs.append(c);offs.append(pos);pos+=len(line)
        return n,cs,offs
    except (ValueError,UnicodeError,OverflowError,TypeError):return None

def parity(x):return x.bit_count()&1

def quartet(sc,rhs):
    return [canon(tuple(-v if mask>>j&1 else v for j,v in enumerate(sc)))
            for mask in range(8) if parity(mask)!=rhs]

def recover(cs,offs):
    groups=defaultdict(list);aliens=[]
    for i,c in enumerate(cs):
        if len(c)==3:groups[tuple(sorted(map(abs,c)))].append(i)
        else:aliens.append(i)
    rows=[]
    for sc,ids in sorted(groups.items()):
        if len(ids)!=4 or len({cs[i] for i in ids})!=4:return None
        if set(cs[i] for i in ids)==set(quartet(sc,0)):rhs=0
        elif set(cs[i] for i in ids)==set(quartet(sc,1)):rhs=1
        else:return None
        rows.append({'scope':sc,'rhs':rhs,'ids':ids,'offsets':[offs[i] for i in ids]})
    return rows,aliens

def source_auth(cs,offs,rows,aliens):
    used=set()
    for row in rows:
        ids=row['ids'];sc=row['scope'];rhs=row['rhs'];orig=row['offsets']
        if len(ids)!=4 or len(set(ids))!=4:return False
        if any(not 0<=i<len(cs) for i in ids) or used.intersection(ids):return False
        if [offs[i] for i in ids]!=orig or set(cs[i] for i in ids)!=set(quartet(sc,rhs)):
            return False
        used.update(ids)
    return len(set(aliens))==len(aliens) and all(0<=i<len(cs) and len(cs[i])<=2 for i in aliens) and not used.intersection(aliens) and used|set(aliens)==set(range(len(cs)))

def xor_mask(row):return sum(1<<(i-1) for i in row['scope'])

def affine_param(n,rows):
    """RREF with row provenance. x_i = constant_i XOR <coeff_i,t>.
    All operations exact GF(2); free variables are ordered by index.
    """
    eqs=[[xor_mask(row),row['rhs'],1<<j] for j,row in enumerate(rows)]
    p=0;piv=[];ops=0
    for col in range(n):
        j=next((j for j in range(p,len(eqs)) if eqs[j][0]>>col&1),None)
        if j is None:continue
        eqs[p],eqs[j]=eqs[j],eqs[p]
        for k in range(len(eqs)):
            if k!=p and eqs[k][0]>>col&1:
                eqs[k][0]^=eqs[p][0];eqs[k][1]^=eqs[p][1];eqs[k][2]^=eqs[p][2];ops+=1
        piv.append(col);p+=1
    for mask,rhs,prov in eqs[p:]:
        if mask==0 and rhs==1:
            return {'status':'NO','conflict':[i for i in range(len(rows)) if prov>>i&1], 'xor_ops':ops}
    free=[i for i in range(n) if i not in set(piv)]
    free_col={v:i for i,v in enumerate(free)}
    const=[0]*n;coeff=[0]*n
    for j,v in enumerate(free):coeff[v]=1<<j
    for i,col in enumerate(piv):
        mask,rhs,_=eqs[i];const[col]=rhs
        coeff[col]=sum(1<<free_col[v] for v in free if mask>>v&1)
    # Validate all equations symbolically, not by evaluating one witness.
    for row in rows:
        vmask=0;vrhs=0
        for v in row['scope']:
            vmask^=coeff[v-1];vrhs^=const[v-1]
        assert vmask==0 and vrhs==row['rhs']
    return {'status':'YES','const':const,'coeff':coeff,'free':free,'xor_ops':ops}

def check_xor_conflict(rows,indices):
    if not indices or len(set(indices))!=len(indices):return False
    mask=0;rhs=0
    for j in indices:
        if not isinstance(j,int) or not 0<=j<len(rows):return False
        mask^=xor_mask(rows[j]);rhs^=rows[j]['rhs']
    return mask==0 and rhs==1

def independence(forms):
    """Returns independent flag, exact dependency list for failures."""
    basis={};combo={};steps=0
    for j,vec in enumerate(forms):
        mask=vec;prov=1<<j
        while mask:
            k=(mask&-mask).bit_length()-1
            if k not in basis:
                basis[k]=mask;combo[k]=prov
                break
            mask^=basis[k];prov^=combo[k];steps+=1
        else:
            return False,[i for i in range(len(forms)) if prov>>i&1],steps
    return True,[],steps

def project(cs,aliens,const,coeff):
    forms=sorted({coeff[abs(l)-1] for i in aliens for l in cs[i] if coeff[abs(l)-1]!=0})
    ok,dep,steps=independence(forms)
    if not ok:return {'status':'DEPENDENT','forms':forms,'dependency':dep,'independence_steps':steps}
    index={v:i for i,v in enumerate(forms)}
    reduced=[];source=[]
    for sid in aliens:
        c=cs[sid];new=[];done=False
        for l in c:
            v=abs(l)-1;mask=coeff[v];c0=const[v];desired=int(l>0)
            if mask==0:
                if c0==desired:done=True;break
                continue
            lit=index[mask]+1
            if (c0^desired)==0:lit=-lit
            new.append(lit)
        if done:continue
        new=list(dict.fromkeys(new))
        if any(-l in new for l in new):continue
        reduced.append(tuple(new));source.append(sid)
    return {'status':'INDEPENDENT','forms':forms,'clauses':reduced,'sources':source,'independence_steps':steps}

def to_index(l):return 2*(abs(l)-1)+(0 if l>0 else 1)
def from_index(i):return (i//2+1) if i%2==0 else -(i//2+1)

def graph_2sat(clauses,sources,n):
    adj=[[] for _ in range(2*n)];rev=[[] for _ in range(2*n)]; edges=0
    for cl,sid in zip(clauses,sources):
        if not cl:return {'status':'NO','kind':'empty','source':sid,'edges':edges}
        a=cl[0];b=cl[1] if len(cl)==2 else cl[0]
        for u,v in ((to_index(-a),to_index(b)),(to_index(-b),to_index(a))):
            adj[u].append((v,sid));rev[v].append(u);edges+=1
    visited=[False]*(2*n);order=[]
    for root in range(2*n):
        if visited[root]:continue
        visited[root]=True;stack=[(root,0)]
        while stack:
            u,j=stack[-1]
            if j<len(adj[u]):
                stack[-1]=(u,j+1);v=adj[u][j][0]
                if not visited[v]:visited[v]=True;stack.append((v,0))
            else:order.append(u);stack.pop()
    component=[-1]*(2*n);cid=0
    for root in reversed(order):
        if component[root]>=0:continue
        stack=[root];component[root]=cid
        while stack:
            u=stack.pop()
            for v in rev[u]:
                if component[v]<0:component[v]=cid;stack.append(v)
        cid+=1
    def path(start,goal):
        q=deque([start]);prev={start:None}
        while q:
            u=q.popleft()
            if u==goal:break
            for v,sid in adj[u]:
                if v not in prev:prev[v]=(u,sid);q.append(v)
        if goal not in prev:return None
        out=[];node=goal
        while node!=start:
            par,sid=prev[node];out.append((from_index(par),from_index(node),sid));node=par
        return out[::-1]
    for i in range(n):
        if component[2*i]==component[2*i+1]:
            return {'status':'NO','kind':'scc','pivot':i+1,
                    'to_neg':path(2*i,2*i+1),'to_pos':path(2*i+1,2*i),'edges':edges}
    assignment=[int(component[2*i]>component[2*i+1]) for i in range(n)]
    assert all(any(assignment[abs(l)-1]==int(l>0) for l in c) for c in clauses)
    return {'status':'YES','assignment':assignment,'edges':edges}

def check_paths(projected,certificate):
    """Reconstruct each directed implication from a source-indexed 2CNF clause."""
    if certificate.get('kind')=='empty':
        return any(not c and sid==certificate['source'] for c,sid in zip(projected['clauses'],projected['sources']))
    p=certificate.get('pivot',0)
    if not 1<=p<=len(projected['forms']):return False
    def check_path(path,a,b):
        curr=a
        for u,v,sid in path:
            if u!=curr:return False
            matches=[c for c,s in zip(projected['clauses'],projected['sources']) if s==sid]
            if not matches:return False
            if not any(((-u in c and v in c) or (len(c)==1 and c[0]==v and u==-v)) and
                       (len(c)==1 or (len(c)==2 and ((-u==c[0] and v==c[1]) or (-u==c[1] and v==c[0])))) for c in matches):
                return False
            curr=v
        return curr==b
    return check_path(certificate['to_neg'],p,-p) and check_path(certificate['to_pos'],-p,p)

def solve_mask_rows(rows,freecount):
    """Solves independent, but not necessarily full-rank, linear rows (mask,rhs)."""
    basis={}
    for mask,rhs in rows:
        while mask:
            p=(mask&-mask).bit_length()-1
            if p not in basis:
                basis[p]=(mask,rhs);break
            old,ob=basis[p];mask^=old;rhs^=ob
        else:
            if rhs:return None
    value=0
    for p in sorted(basis,reverse=True):
        mask,rhs=basis[p]
        val=rhs^parity((mask & ~(1<<p))&value)
        value|=val<<p
    assert all(parity(m&value)==r for m,r in rows)
    return value

def eval_cs(cs,w):return all(any(((w>>(abs(l)-1))&1)==int(l>0) for l in c) for c in cs)

def decide(data):
    parsed=parse(data)
    if parsed is None:return {'status':'INVALID','route':'source-parser'}
    n,cs,offs=parsed; rec=recover(cs,offs)
    if rec is None:return {'status':'UNKNOWN','route':'unrecognized-ternary'}
    rows,aliens=rec
    assert source_auth(cs,offs,rows,aliens)
    aff=affine_param(n,rows)
    if aff['status']=='NO':
        out={'status':'NO','route':'affine-contradiction','certificate':{'rows':aff['conflict']},'child':NO_BASE}
        assert check_xor_conflict(rows,aff['conflict']);return out
    proj=project(cs,aliens,aff['const'],aff['coeff'])
    if proj['status']!='INDEPENDENT':
        return {'status':'UNKNOWN','route':'dependent-alien-support','number_forms':len(proj['forms']),
                'dependency':proj['dependency'],'child':data}
    q=graph_2sat(proj['clauses'],proj['sources'],len(proj['forms']))
    if q['status']=='NO':
        assert check_paths(proj,q)
        return {'status':'NO','route':'independent-affine-2sat','certificate':q,
                'number_forms':len(proj['forms']),'affine_nullity':len(aff['free']),
                'nonaffine':len(aliens),'child':NO_BASE}
    f=proj['forms'];qvals=q['assignment']
    t=solve_mask_rows(list(zip(f,qvals)),len(aff['free']))
    assert t is not None
    w=sum((aff['const'][j]^parity(aff['coeff'][j]&t))<<j for j in range(n))
    assert eval_cs(cs,w)
    return {'status':'YES','route':'independent-affine-2sat','witness':w,
            'number_forms':len(f),'affine_nullity':len(aff['free']),
            'nonaffine':len(aliens),'child':YES_BASE}

def portfolio(data):
    """One child for recognized sources; direct halting on exact base images."""
    if data==YES_BASE:return {'phase':'base','status':'YES','child':None}
    if data==NO_BASE:return {'phase':'base','status':'NO','child':None}
    r=decide(data)
    if r['status'] in ('YES','NO'):
        return {'phase':'successor','status':r['status'],'child':r['child'],
                'power_shrink_verified':(len(data)>=512 and len(r['child'])<=len(data)**.75)}
    return {'phase':'unknown','status':r['status'],'child':data}

def full_verify(data,result):
    p=parse(data)
    if p is None:return result['status']=='INVALID'
    n,cs,offs=p;rec=recover(cs,offs)
    if rec is None:return result['status']=='UNKNOWN'
    rows,aliens=rec
    if not source_auth(cs,offs,rows,aliens):return False
    aff=affine_param(n,rows)
    if result['status']=='UNKNOWN':return result.get('child')==data
    if result['status']=='YES':
        w=result['witness'];return isinstance(w,int) and 0<=w<(1<<n) and eval_cs(cs,w)
    if result['status']!='NO':return False
    if result['route']=='affine-contradiction':return check_xor_conflict(rows,result['certificate']['rows'])
    if aff['status']!='YES':return False
    proj=project(cs,aliens,aff['const'],aff['coeff'])
    if proj['status']!='INDEPENDENT':return False
    return check_paths(proj,result['certificate'])

def grid_family(L,unsat=False):
    """Connected grid of alien binary clauses and pairwise-disjoint parity quartets.
    Each vertex v uses x_v,y_v,p_v; its affine equation is x_v^y_v^p_v=0.
    Only x_v,p_v occur in alien unit/binary clauses. Thus all their
    nonzero affine forms are independent although affine nullity is 2L^2.
    """
    assert L>=2
    m=L*L;cs=[]
    for v in range(m):
        x,y,p=3*v+1,3*v+2,3*v+3
        cs.extend(quartet((x,y,p),0));cs.append((-p,))
    for r in range(L):
        for c in range(L):
            v=r*L+c;x=3*v+1
            if r+1<L:cs.append((x,3*((r+1)*L+c)+1))
            if c+1<L:cs.append((x,3*(r*L+c+1)+1))
    if unsat:
        x=1;y=4
        cs.extend([(x,y),(x,-y),(-x,y),(-x,-y)])
    return encode(3*m,cs)

def no_unit_grid(L,unsat=False,cycle=False):
    """Strong hostile control: there are NO unit clauses or private pinned units.

    Each site has six names (x,y,p,a,b,c) and four XOR3 quartets
      x^y^p=0, p^a^b=0, p^a^c=0, p^b^c=0.
    They force p=0 and x=y, with a=b=c free. Both x and y appear in
    Θ(L²) independent alien 2CNF clauses forming grid graphs. Every source
    variable-clause component is connected through x/y grid edges.
    Unit propagation on the original source has nothing to do.
    """
    assert L>=2
    m=L*L;cs=[]
    for v in range(m):
        x,y,p,a,b,c=(6*v+j for j in range(1,7))
        for scope in ((x,y,p),(p,a,b),(p,a,c),(p,b,c)):
            cs.extend(quartet(scope,0))
    for r in range(L):
        for c in range(L):
            v=r*L+c
            for u in ([((r+1)*L+c)] if r+1<L else []) + ([r*L+c+1] if c+1<L else []):
                cs.append((6*v+1,6*u+1))
                cs.append((6*v+2,6*u+2))
    if unsat:
        if cycle:
            for v in range(m-1):
                x,y=6*v+1,6*(v+1)+1
                cs.extend([(-x,y),(x,-y)])
            x,y=6*(m-1)+1,1
            cs.extend([(x,y),(-x,-y)])
        else:
            cs.extend([(1,7),(1,-7),(-1,7),(-1,-7)])
    assert all(len(c)>=2 for c in cs)
    return encode(6*m,cs)

def mixed_hard_reduction():
    # An arbitrary signed 3SAT clause is exactly ∃(y1,y2,y3)
    # (l1∨y1)&(l2∨y2)&(l3∨y3)&(y1^y2^y3=0).
    cs=[]
    for literals in ((1,2,3),(-1,2,-3),(-1,-2,-3)):
        y=(len(cs)+10,len(cs)+11,len(cs)+12) # distinct by clause counter
        cs.extend((l,v) for l,v in zip(literals,y));cs.extend(quartet(y,0))
    n=max(abs(l) for c in cs for l in c)
    return encode(n,cs)

def brute(n,cs):
    return next((w for w in range(1<<n) if eval_cs(cs,w)),None)

def run_tests():
    rng=random.Random(SEED);s=Counter();start=time.perf_counter()
    # Exhaust all possible 2CNF subformulas on three free variables,
    # with disjoint private quartet gadgets (n=9), to test both labels.
    for bit in range(1<<8):
        aliens=[(1,4),(1,-4),(-1,4),(-1,-4),
                (4,7),(-4,7),(4,-7),(-4,-7)]
        cs=[]
        for v in range(3):
            x,y,p=3*v+1,3*v+2,3*v+3
            cs.extend(quartet((x,y,p),0));cs.append((-p,))
        cs.extend(aliens[j] for j in range(8) if bit>>j&1)
        data=encode(9,cs); r=decide(data); p=parse(data)
        b=brute(p[0],p[1])
        assert r['status']==('YES' if b is not None else 'NO')
        assert full_verify(data,r)
        s['exhaustive_2cnf_samples']+=1;s['exhaustive_sat' if b is not None else 'exhaustive_unsat']+=1
    # Random independent-support instances with multiple parity quartets
    for i in range(240):
        m=rng.randint(2,4);cs=[]
        for v in range(m):
            x,y,p=3*v+1,3*v+2,3*v+3
            cs+=quartet((x,y,p),rng.randrange(2))
            cs.append((p if rng.randrange(2) else -p,))
        for _ in range(rng.randint(1,8)):
            a,b=rng.sample([3*v+1 for v in range(m)],2)
            cs.append((a*rng.choice((-1,1)),b*rng.choice((-1,1))))
        data=encode(3*m,cs);res=decide(data)
        assert res['status'] in ('YES','NO');truth=brute(3*m,parse(data)[1])
        assert (res['status']=='YES')==(truth is not None)
        assert full_verify(data,res)
        s['random_instances']+=1;s['random_sat' if truth is not None else 'random_unsat']+=1
    # Large alien-count, high-width, high-strong-backdoor grid controls
    for L in (4,8,12,24):
        for unsat in (False,True):
            data=grid_family(L,unsat);res=decide(data)
            assert res['status']==('NO' if unsat else 'YES')
            assert full_verify(data,res)
            m=L*L;cutoff=math.floor(math.log2(len(data)))
            assert m>cutoff if L>=8 else True
            assert res['number_forms']==2*m and res['affine_nullity']==2*m
            s['grid_cases']+=1;s['largest_grid_L']=L;s['largest_input_bytes']=len(data)
            s['largest_grid_alien_count']=res['nonaffine']
            s['largest_grid_rank']=res['number_forms']
            s['largest_backdoor_bound']=m;s['largest_treewidth_lower_bound']=L-1
    # No-unit, source-connected, large-width and large-backdoor controls:
    # each site has four interdependent XOR3 quartets, not a unit simplifier.
    for L in (4,8,12,24):
        for unsat in (False,True):
            data=no_unit_grid(L,unsat);res=decide(data)
            assert res['status']==('NO' if unsat else 'YES')
            assert full_verify(data,res)
            n,cs,_=parse(data)
            assert all(len(c)>=2 for c in cs)
            m=L*L;cutoff=math.floor(math.log2(len(data)))
            if L>=8:assert m>cutoff
            assert res['number_forms']==m and res['affine_nullity']==2*m
            s['no_unit_grid_cases']+=1
            s['no_unit_L_max']=L
            s['no_unit_input_bytes_max']=len(data)
            s['no_unit_binary_alien_count_max']=res['nonaffine']
            s['no_unit_var_count_max']=n
    for L in (4,12,24):
        data=no_unit_grid(L,True,cycle=True)
        res=decide(data)
        assert res['status']=='NO' and full_verify(data,res)
        s['no_unit_long_cycle_cases']+=1
        if L==24:
            s['no_unit_long_cycle_24_bytes']=len(data)
            s['no_unit_long_cycle_24_implication_steps']=(len(res['certificate']['to_neg'])+
                                                            len(res['certificate']['to_pos']))

    for unsat in (False,True):
        d=no_unit_grid(8,unsat)
        first=portfolio(d);assert first['phase']=='successor'
        assert first['power_shrink_verified']
        second=portfolio(first['child'])
        assert second['phase']=='base' and second['status']==first['status']
        s['two_level_termination_cases']+=1

    # Deliberate dependent forms should not be incorrectly compressed.
    cs=quartet((1,2,3),0)+[(1,),(2,),(3,)]
    dependent_data=encode(3,cs)
    assert decide(dependent_data)['status']=='UNKNOWN';s['dependent_rejects']+=1
    # Actual 3SAT gadget with dependent alien projections is rejected.
    hard=mixed_hard_reduction();assert decide(hard)['status']=='UNKNOWN';s['hard_gadget_rejects']+=1
    # Forged proof controls: mutate a source-indexed implication edge and witness.
    d=grid_family(4,True);r=decide(d);assert r['status']=='NO';assert full_verify(d,r)
    r['certificate']['to_neg'][0]=(*r['certificate']['to_neg'][0][:2],-999)
    assert not full_verify(d,r);s['forged_certificates_rejected']+=1
    d=grid_family(4,False);r=decide(d);assert r['status']=='YES'
    r['witness']=0
    assert not full_verify(d,r);s['forged_witnesses_rejected']+=1
    return {'status':'PASS','seed':SEED,'data_sha256_grid_L24_sat':sha256(grid_family(24,False)).hexdigest(),
            'tests':dict(s),'elapsed_wall_sec':round(time.perf_counter()-start,4),
            'limitations':['Python integer bitset operations are not measured TM steps.',
               'Independent affine support is a sufficient recognition condition, not necessary.',
               'UNSAT implication certificates checked in Python, not by a proof assistant.',
               'No general mixed-XOR/2SAT or general SAT contraction.']}

if __name__=='__main__':print(json.dumps(run_tests(),indent=2,sort_keys=True))
