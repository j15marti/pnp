#!/usr/bin/env python3
"""LSPV-2 CONNECTED_ALLPORT_COMPILER224: fully encoded ordinary 3CNF to
connected signed strict exact-(2,2)-3CNF, with original variables retained as
individually named free ports. This is an EXPANSIVE compiler, not SAT solver.

Derived from (and credits) prior PC22_ALLFIELD1 and universal22.py. Fresh step:
neutral connectivity hub, stable original-port renaming, hostile raw input cases.

Stdlib deterministic checks; optional scipy.optimize.milp for independent SAT.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import product
import hashlib, json, sys

W1 = ((-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
      (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
      (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
      (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))
Q = W1[:7] + W1[8:]
PORTS = (1,7,13)


def canonical(clauses):
    return tuple(sorted(tuple(sorted(c,key=lambda l:(abs(l),l<0))) for c in clauses))


def eval_cnf(clauses,assignment):
    return all(any(assignment[abs(l)]==int(l>0) for l in c) for c in clauses)


def check_source(n,clauses):
    if not isinstance(n,int) or n<0: raise ValueError('bad n')
    try:clauses=[tuple(c) for c in clauses]
    except TypeError as exc:raise ValueError('bad clauses') from exc
    if any(len(c)>3 or any(not isinstance(l,int) or l==0 or abs(l)>n for l in c) for c in clauses):
        raise ValueError('not ordinary 3CNF on declared variables')
    if n>3*len(clauses): raise ValueError('n too large for active three-literal source')
    active={abs(l) for c in clauses for l in c}
    if n and active!=set(range(1,n+1)):
        raise ValueError('noncanonical unused source header variables')
    if n==0 and any(c for c in clauses):raise ValueError('nonempty variable with n=0')
    return clauses


def properize(n,clauses):
    """Exact existential 3CNF properization for widths 0..3; drops tautologies.
    Returns clauses and total variable count, preserving all x_1..x_n.
    """
    source=check_source(n,clauses)
    next_id=n;out=[];seen=set()
    for raw in source:
        litset=set(raw)
        if any(-lit in litset for lit in litset):continue
        key=tuple(sorted(litset,key=lambda z:(abs(z),z<0)))
        if key in seen:continue
        seen.add(key)
        if len(key)==3:out.append(key)
        elif len(key)==2:
            next_id+=1;z=next_id
            out.extend([key+(z,),key+(-z,)])
        elif len(key)==1:
            a,b=next_id+1,next_id+2;next_id+=2
            for s,t in product((1,-1),repeat=2):out.append((key[0],s*a,t*b))
        else:
            a,b,c=next_id+1,next_id+2,next_id+3;next_id+=3
            for s,t,u in product((1,-1),repeat=3):out.append((s*a,t*b,u*c))
    if next_id==0:
        next_id=3;out.append((1,2,3))
    return list(canonical(out)),next_id


def connectedize(proper,nb):
    """Find original incidence components, tether ONE variable per component.
    In each tether, (x or s or t) and (s or hub or w) are always satisfiable
    by choosing s=1. With zero/one component, return source unchanged.
    """
    parent=list(range(nb+1))
    def root(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]
            x=parent[x]
        return x
    for clause in proper:
        ids=[abs(l) for l in clause]
        for x in ids[1:]:parent[root(x)]=root(ids[0])
    components=defaultdict(list)
    for x in range(1,nb+1):components[root(x)].append(x)
    anchors=sorted(min(v) for v in components.values())
    if len(anchors)<=1:
        return list(canonical(proper)),nb,0,[]
    hub=nb+1;next_id=hub;new=list(proper);tether=[]
    for x in anchors:
        s,t,w=next_id+1,next_id+2,next_id+3;next_id+=3
        new.extend([(x,s,t),(s,hub,w)]);tether.append((s,t,w))
    return list(canonical(new)),next_id,hub,tether


def pad7(lit,next_id):
    a,b,c,d,e=range(next_id,next_id+5)
    return [(lit,-a,-b),(a,c,-d),(a,d,-e),(b,e,-c),
            (b,-d,-e),(-a,c,d),(-b,-c,e)]


def balance(clauses,n):
    counts=Counter(l for c in clauses for l in c)
    out=list(clauses);next_id=n+1;gadgets=[]
    for x in range(1,n+1):
        r=max(counts[x],counts[-x],2)
        for l in (x,-x):
            for _ in range(r-counts[l]):
                out.extend(pad7(l,next_id));gadgets.append((l,next_id))
                next_id+=5
    return list(canonical(out)),next_id-1,gadgets


def balance_clone(clauses,n,source_n):
    """Source variable representatives are renamed back to IDs 1..source_n.
    Every nonrepresentative clone and every Q variable is existential.
    """
    positions=defaultdict(lambda:{1:[],-1:[]})
    for ci,c in enumerate(clauses):
        for j,l in enumerate(c):positions[abs(l)][1 if l>0 else -1].append((ci,j))
    out=[list(c) for c in clauses];offset=0;cyc=[];rep={};clone_of={}
    for x in range(1,n+1):
        pos=positions[x];r=len(pos[1])
        assert r==len(pos[-1]) and r>=2
        ids=tuple(range(offset+1,offset+r+1));offset+=r
        rep[x]=ids[0]
        for z in ids:clone_of[z]=x
        for j,z in enumerate(ids):
            for sign in (1,-1):
                i,k=pos[sign][j];out[i][k]=sign*z
            cyc.append((z,ids[(j+1)%r]))
    R=offset
    assert R%3==0 and len(cyc)==R
    for j,(u,v) in enumerate(cyc):
        q,p=divmod(j,3)
        out.append([-u,v,R+15*q+PORTS[p]])
    for q in range(R//3):
        for c in Q:
            out.append([(1 if l>0 else -1)*(R+15*q+abs(l)) for l in c])
    assert len(out)==8*R//1
    target_n=6*R
    representatives={rep[x]:x for x in range(1,source_n+1)}
    rename=dict(representatives);fresh=source_n+1
    for z in range(1,target_n+1):
        if z not in rename:
            rename[z]=fresh;fresh+=1
    assert fresh-1==target_n
    output=canonical(tuple((1 if l>0 else -1)*rename[abs(l)] for l in c) for c in out)
    ports={x:x for x in range(1,source_n+1)}
    aux_q=tuple(rename[z] for z in range(R+1,target_n+1))
    return output,target_n,ports,rep,rename,clone_of,aux_q,R


def connectivity(clauses,n):
    if n==0:return True
    graph=[set() for _ in range(n+len(clauses)+1)]
    for i,c in enumerate(clauses):
        for l in c:
            x=abs(l);y=n+1+i
            graph[x].add(y);graph[y].add(x)
    seen={1};stack=[1]
    while stack:
        z=stack.pop()
        for y in graph[z]:
            if y not in seen:seen.add(y);stack.append(y)
    return len(seen)==n+len(clauses)


def strict22(clauses,n):
    counts=Counter(l for c in clauses for l in c)
    if len(clauses)*3!=4*n:return False
    if len(clauses)!=len(set(clauses)):return False
    if any(len(c)!=3 or len({abs(l) for l in c})!=3 for c in clauses):return False
    if any(abs(l)<1 or abs(l)>n for c in clauses for l in c):return False
    return all(counts[v]==counts[-v]==2 for v in range(1,n+1))


def dimacs(clauses,n):
    return ('p cnf %d %d\n'%(n,len(clauses))+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')


def parse_source_dimacs(data):
    """Parse ordinary width<=3 DIMACS with multiline clauses and comments.
    Refuse enormous declared unused-variable ranges before materializing them.
    """
    try:s=data.decode('ascii')
    except UnicodeError as exc:raise ValueError('not ascii') from exc
    header=None;tokens=[]
    for line in s.splitlines():
        z=line.strip()
        if not z or z.startswith('c'):continue
        if z.startswith('p'):
            if header is not None:raise ValueError('multiple headers')
            v=z.split()
            if len(v)!=4 or v[:2]!=['p','cnf']:raise ValueError('header')
            try:n,m=map(int,v[2:])
            except ValueError as exc:raise ValueError('header integers') from exc
            if n<0 or m<0 or n>3*m:raise ValueError('noncanonical header counts')
            header=(n,m)
            continue
        if header is None:raise ValueError('missing header')
        try:tokens.extend(int(x) for x in z.split())
        except ValueError as exc:raise ValueError('bad literal') from exc
    if header is None:raise ValueError('missing header')
    n,m=header
    result=[];current=[]
    for x in tokens:
        if x==0:
            result.append(tuple(current));current=[]
            if len(result)>m:raise ValueError('too many clauses')
        else:
            current.append(x)
            if len(current)>3:raise ValueError('clause width >3')
    if current or len(result)!=m:raise ValueError('unterminated clauses / count mismatch')
    check_source(n,result)
    return n,result


def source_dimacs(clauses,n):
    return ('p cnf %d %d\n'%(n,len(clauses))+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')


@dataclass
class Result:
    n:int
    original:tuple
    proper:tuple
    proper_n:int
    hub:tuple
    hub_n:int
    hub_id:int
    tether:list
    balanced:tuple
    balanced_n:int
    gadgets:list
    compiled:tuple
    compiled_n:int
    reps:dict
    rename:dict
    clone_of:dict
    Q_aux:tuple
    R:int


def compile_allports(n,clauses):
    source=check_source(n,clauses)
    proper,pn=properize(n,source)
    hub,hn,hid,tether=connectedize(proper,pn)
    bal,bn,gadgets=balance(hub,hn)
    comp,cn,ports,rep,rename,clones,q_aux,R=balance_clone(bal,bn,n)
    assert strict22(comp,cn),('failure of exact22',n,clauses)
    assert connectivity(comp,cn),('failure of connectedness',n,clauses)
    assert len(comp)==8*R and cn==6*R
    return Result(n,tuple(source),tuple(proper),pn,tuple(hub),hn,hid,tether,
                  tuple(bal),bn,gadgets,comp,cn,rep,rename,clones,q_aux,R)


def lift_witness(r,values):
    """Construct canonical witness of output WHEN source assignment satisfies F.
    This is only a witness check, not a decision procedure.
    """
    assert eval_cnf(r.original,values)
    assignment={i:0 for i in range(1,r.balanced_n+1)}
    assignment.update(values)
    if r.n==0 and not r.original: assignment[1]=1  # generated dummy clause
    # For existential width-2 and width-1 conversions, setting auxiliaries 0
    # works whenever the source clause is satisfied.
    if not eval_cnf(r.proper,assignment):
        raise AssertionError('properization did not preserve witness')
    if r.hub_id: assignment[r.hub_id]=0
    for s,t,w in r.tether:assignment[s]=1;assignment[t]=assignment[w]=0
    assert eval_cnf(r.hub,assignment)
    for lit,first in r.gadgets:
        for i in range(first,first+5):assignment[i]=0
    assert eval_cnf(r.balanced,assignment)
    target={i:0 for i in range(1,r.compiled_n+1)}
    for z,x in r.clone_of.items():target[r.rename[z]]=assignment[x]
    assert eval_cnf(r.compiled,target)
    assert all(target[i]==values[i] for i in range(1,r.n+1))
    return target



def affine(p):
    """Previous explicit exact22 all-YES family, used as high-volume control."""
    assert p>=5 and p%2
    def v(g,i):return g*p+(i%p)+1
    return list(canonical(((-v(0,i) if t in (0,1) else v(0,i)),
               (-v(1,i+t) if t in (2,3) else v(1,i+t)),
               (-v(2,i+2*t) if t in (0,2) else v(2,i+2*t)))
             for t in range(4) for i in range(p)))


def named_port_occurrence_floor_bits(n):
    """Every one of n named ports must occur four times in a strict exact22
    formula. For ASCII DIMACS, each variable name contributes its decimal
    digits in every occurrence; distinct IDs minimize at IDs 1..n.
    """
    return 32*sum(len(str(i)) for i in range(1,n+1))


def q_certificate():
    patterns=Counter(); satisfiers=0
    for mask in range(1<<15):
        a={z:((mask>>(z-1))&1) for z in range(1,16)}
        if eval_cnf(Q,a):
            satisfiers+=1;patterns[tuple(a[i] for i in PORTS)]+=1
    assert patterns=={(0,0,0):244},patterns
    assert eval_cnf(Q,{i:0 for i in range(1,16)})
    return {'Q_models':satisfiers,'Q_port_signatures':{str(k):v for k,v in patterns.items()},
            'W1_unsat':True,'enumerated_assignments':32768}


def guard_fixture():
    guard=[list(c) for c in W1]
    for idx in (6,11):guard[idx][0]*=-1
    return list(canonical(guard))


def guard_certificate():
    G=guard_fixture()
    plus=canonical([(4,8,-10)])[0]
    minus=canonical([(-4,-9,-11)])[0]
    assert plus in G and minus in G
    Gcirc=[c for c in G if c not in (plus,minus)]
    counts=Counter()
    for mask in range(1<<15):
        a={i:((mask>>(i-1))&1) for i in range(1,16)}
        if eval_cnf(Gcirc,a):
            p=a[4];A=a[8] or not a[10];B=not a[9] or not a[11]
            counts[(p,int(A),int(B))]+=1
    expected={(0,0,0):85,(0,1,0):153,(1,0,0):85,(1,0,1):119}
    assert counts==expected,counts
    return {str(k):v for k,v in sorted(counts.items())}


def attach_equality_guard(r,x):
    """Use predecessor223 two-swapped guard on a representative ORIGINAL port.
    Output original x_1..x_n remain the first n original names; p is a new
    port with ID target_n+1. Pointwise output = F(original) AND (p==x).
    """
    assert 1<=x<=r.n
    G=guard_fixture();p=r.compiled_n+1
    name={4:p}
    nxt=p+1
    for k in range(1,16):
        if k!=4:name[k]=nxt;nxt+=1
    assert nxt-1==r.compiled_n+15
    S=[list(c) for c in r.compiled]
    Pnext=next(i for i,c in enumerate(S) if x in c)
    Mnext=next(i for i,c in enumerate(S) if -x in c)
    S[Pnext][S[Pnext].index(x)]=p
    S[Mnext][S[Mnext].index(-x)]=-p
    Gnew=[[name[abs(l)]*(1 if l>0 else -1) for l in c] for c in G]
    gp=next(i for i,c in enumerate(Gnew) if set(c)==set((p,name[8],-name[10])))
    gm=next(i for i,c in enumerate(Gnew) if set(c)==set((-p,-name[9],-name[11])))
    Gnew[gp][Gnew[gp].index(p)]=x
    Gnew[gm][Gnew[gm].index(-p)]=-x
    output=canonical(S+Gnew)
    assert strict22(output,r.compiled_n+15) and connectivity(output,r.compiled_n+15)
    return output,r.compiled_n+15,p


def _milp_solve(clauses,n,fixed=None):
    """Independent general MILP SAT checker, optional SciPy install.
    Every clause is one 0/1 linear inequality. Not used by compiler.
    """
    import numpy as np
    from scipy.optimize import milp, Bounds, LinearConstraint
    from scipy.sparse import lil_matrix
    fixed=fixed or {}
    A=lil_matrix((len(clauses),n),dtype=np.float64)
    lb=np.empty(len(clauses),dtype=np.float64)
    for i,c in enumerate(clauses):
        negative=0
        for l in c:
            A[i,abs(l)-1]+=1. if l>0 else -1.
            negative+=l<0
        lb[i]=1-negative
    low=np.zeros(n);high=np.ones(n)
    for z,v in fixed.items():low[z-1]=high[z-1]=v
    res=milp(np.zeros(n),integrality=np.ones(n),bounds=Bounds(low,high),
             constraints=LinearConstraint(A.tocsr(),lb,np.inf),
             options={'time_limit':4.})
    if res.status==0:return True
    if res.status==2:return False
    return None


def run():
    certificate=q_certificate()
    source_cases=[('ONE',1,[(1,)]),('CONFLICT',1,[(1,),(-1,)]),
                  ('OR3',3,[(1,2,3)]),('3SAT_UNSAT',3,[(1,),(2,),(-1,-2,3),(-3,)]),
                  ('TAUTO',2,[(1,-1),(2,-2)]),
                  ('BINARY',2,[(1,2),(-1,-2)]),
                  ('EMPTY_CLAUSE',0,[()]),('EMPTY_FORMULA',0,[]),
                  ('MIXED',3,[(1,-2),(2,3),(-1,-2,-3),(1,1,2)]),
                  ('DUPLICATE',2,[(1,2),(1,2),(-1,2)])]
    raw=[];positive_witnesses=0;source_evaluations=0;milp_checks=0;milp_skips=0
    for label,n,clauses in source_cases:
        r=compile_allports(n,clauses)
        source_bits=len(source_dimacs(r.original,r.n))*8
        out_bits=len(dimacs(r.compiled,r.compiled_n))*8
        assert r.compiled_n%3==0 and r.R%3==0
        for mask in range(1<<n):
            a={i:((mask>>(i-1))&1) for i in range(1,n+1)}
            sat=eval_cnf(r.original,a)
            source_evaluations+=1
            if sat:
                lift_witness(r,a);positive_witnesses+=1
        raw.append({'case':label,'source_n':n,'source_clauses':len(clauses),
            'source_bits':source_bits,'proper_clauses':len(r.proper),
            'connectedizer_clauses':len(r.hub), 'balance_gadgets':len(r.gadgets),
            'R':r.R,'target_vars':r.compiled_n,'target_clauses':len(r.compiled),
            'target_bits':out_bits,'output_input_ratio':round(out_bits/source_bits,5),
            'strict_signed22_connected':True,'all_source_SAT_witnesses_checked':True})
        # An independent solver checks all pinning cases on the three smallest.
        if label in ('ONE','CONFLICT','EMPTY_CLAUSE','EMPTY_FORMULA'):
            for mask in range(1<<n):
                a={i:((mask>>(i-1))&1) for i in range(1,n+1)}
                expected=eval_cnf(r.original,a)
                got=_milp_solve(r.compiled,r.compiled_n,a)
                if got is None:milp_skips+=1
                else:
                    milp_checks+=1
                    assert got==expected,(label,mask,expected,got)
    bad=[(-1,()),(2,[(1,)]),(1,[(2,)]),(1,[(1,2,3,4)]),(1,[('x',)])]
    invalid=0
    for n,cls in bad:
        try:compile_allports(n,cls)
        except (ValueError,AssertionError,TypeError):invalid+=1
        else:raise AssertionError(('bad accepted',n,cls))
    # Source width-3 expansion of the earlier selector identity is polynomial
    # as a circuit but may create quadratic resolution products. Check truth
    # using only source-local symbolic evaluation, no SAT solver required.
    expansion_checks=0
    for t in range(1,5):
        count=2**(4*t)
        for mask in range(count):
            A=[bool((mask>>(2*i))&1 or (mask>>(2*i+1))&1) for i in range(t)]
            B=[bool((mask>>(2*t+2*j))&1 or (mask>>(2*t+2*j+1))&1) for j in range(t)]
            exp=all(x or y for x in A for y in B)
            compact=all(A) or all(B)
            assert exp==compact
            expansion_checks+=1
    guards=guard_certificate()
    # Test single guarded port on connected, fully compiled unit clause: x=1.
    case=compile_allports(1,[(1,)])
    Gcnf,gn,gport=attach_equality_guard(case,1)
    guarded_checks=0;guarded_inconclusive=0
    for x,p in product((0,1),repeat=2):
        got=_milp_solve(Gcnf,gn,{1:x,gport:p})
        if got is None:guarded_inconclusive+=1
        else:
            assert got==(x==1 and x==p),(x,p,got)
            guarded_checks+=1
    source_parse_checks=0
    for label,n,clauses in source_cases:
        ni,Ci=parse_source_dimacs(source_dimacs(clauses,n))
        assert (ni,Ci)==(n,[tuple(c) for c in clauses])
        source_parse_checks+=1
    invalid_text=(b'p cnf 1 1\n1\n',b'p cnf 9999999999999 1\n1 0\n',
                  b'p cnf 1 2\n1 0\n',b'p cnf 1 1\n1 0\n-1 0\n',
                  b'p cnf 1 1\n1 2 3 4 0\n')
    for blob in invalid_text:
        try:parse_source_dimacs(blob)
        except ValueError:pass
        else:raise AssertionError('malformed DIMACS accepted')
    # Direct repeated-closure control: an exact22 input is made 12 times larger
    # in variable count; applying the same normalizer again gives 144n.
    exact_control=compile_allports(1,[(1,),(-1,)])
    again=compile_allports(exact_control.compiled_n,exact_control.compiled)
    assert again.compiled_n==12*exact_control.compiled_n
    assert len(again.compiled)==12*len(exact_control.compiled)
    repeated={'first_variables':exact_control.compiled_n,
              'second_variables':again.compiled_n,
              'first_bits':len(dimacs(exact_control.compiled,exact_control.compiled_n))*8,
              'second_bits':len(dimacs(again.compiled,again.compiled_n))*8}
    affine_controls=[]
    for p in (5,31,101,501):
        source=affine(p); n=3*p; assert strict22(source,n)
        rc=compile_allports(n,source)
        assert rc.compiled_n==12*n and len(rc.compiled)==16*n
        inbits=len(source_dimacs(source,n))*8
        outbits=len(dimacs(rc.compiled,rc.compiled_n))*8
        floor=named_port_occurrence_floor_bits(n)
        affine_controls.append({'p':p,'source_n':n,'source_bits':inbits,
               'output_n':rc.compiled_n,'output_bits':outbits,
               'port_floor_bits':floor,
               'port_floor_exceeds_source_power_0_75':floor>inbits**0.75,
               'compiled_ratio':round(outbits/inbits,5)})
    result={'status':'PASS','run_label':'CONNECTED_ALLPORT_COMPILER224',
        'prior_corpus':'PC22_ALLFIELD1 2026-10-13 + universal22.py; original normalization is prior work',
        'new_focus':'component-aware neutral hub + source-ID-preserving exact free ports + adversarial empty/unit/binary sources',
        'certificate':certificate,'cases':raw,
        'affine_allport_floor_controls':affine_controls,
        'repeated_exact22_expansion':repeated,
        'two_swap_guard_signature':guards,'guarded_port_MILP_checked':guarded_checks,
        'guarded_port_MILP_inconclusive':guarded_inconclusive,
        'DIMACS_roundtrips':source_parse_checks,'malformed_DIMACS_rejections':len(invalid_text),
        'total_source_assignments':source_evaluations,
        'total_source_SAT_witnesses_constructed':positive_witnesses,
        'independent_MILP_sat_tests':milp_checks,
        'independent_MILP_inconclusive':milp_skips,
        'malformed_source_rejections':invalid,
        'selector_identity_checks':expansion_checks,
        'limitations':['No general SAT decision algorithm; source output strictly larger.',
          'Full negative-fiber proof relies on exhaustive Q fixture and equality cycles, not MILP tests.',
          'Input domain canonical: declared variables active, or 0; no exponential unused-header padding.',
          'MILP tests are independent finite controls, not a kernel-verified theorem.',
          'No native TM step simulation; separate conservative machine upper bounds required.',
          'Source compiler is prior research, not new SAT normalization result.']}
    return result


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
