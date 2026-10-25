#!/usr/bin/env python3
"""ARC-SEMANTIC-CYLINDER116: exact two-level named erasure and QBF-gate audit.
Deterministic, no random source, standard library only. Finite evidence is not
an unrestricted SAT lower bound and is not a RAM primitive trace.
"""
import json
from itertools import product

DATA = {'run_id':'ARC-SEMANTIC-CYLINDER116','revision':'1.0.0',
        'seed':None,'method':'deterministic exhaustive boundary assignments and DPLL',
        'assertions':0,'sat_calls':0,'ordinary_roundtrips':0,
        'failure_count':0,'two_level':[],'qbf':[],'hostile':[],
        'source_identity_preserved':True,
        'time_space_FLVM_measured':False}

def ck(cond, descr):
    DATA['assertions'] += 1
    if not cond:
        DATA['failure_count'] += 1
        raise AssertionError(descr)

class Builder:
    def __init__(self,n=3): self.n=n
    def fresh(self): self.n+=1; return self.n
    def pin(self,l):
        p,q=self.fresh(),self.fresh()
        return [(l,p,q),(l,p,-q),(l,-p,q),(l,-p,-q)]
    def eq(self,x,y):
        a,b=self.fresh(),self.fresh()
        return [(-x,y,a),(-x,y,-a),(x,-y,b),(x,-y,-b)]
    def xor(self,x,y,z):
        c=[]
        for a,b,v in product((0,1),repeat=3):
            if v != (a ^ b):
                c.append(tuple((-u if bit else u) for u,bit in ((x,a),(y,b),(z,v))))
        return c
    def gate(self,x,clause):
        ck(len(clause)==3 and all(abs(q)!=x for q in clause),'gated source clause')
        h=self.fresh()
        return [(-x,clause[0],h),(-h,clause[1],clause[2])]

def serialize(clauses,n):
    m=len(clauses);h=(2*max(n,m)+1).bit_length()
    ck(n>=1 and m>=1, 'nonempty header')
    for c in clauses:
        ck(len(c)==3 and len(set(map(abs,c)))==3,'proper 3CNF')
        ck(all(0<abs(x)<=n for x in c),'name range')
    def field(z):return format(z,'0%db'%h)
    text='1'*h+'0'+field(n)+field(m)
    text+=''.join(field(2*(abs(l)-1)+int(l<0)) for c in clauses for l in c)
    ck(len(text)==1+(3+3*m)*h,'exact encoded body length')
    return text

def parse(text):
    h=0
    while h<len(text) and text[h]=='1':h+=1
    if h==0 or h>=len(text) or text[h]!='0':raise ValueError('malformed header')
    if len(text)<3*h+1:raise ValueError('short')
    n=int(text[h+1:2*h+1],2);m=int(text[2*h+1:3*h+1],2)
    if h!=(2*max(n,m)+1).bit_length() or n<1 or m<1 or len(text)!=1+(3+3*m)*h:
        raise ValueError('encoded length or header mismatch')
    c=[];p=3*h+1
    for i in range(m):
        row=[]
        for j in range(3):
            z=int(text[p:p+h],2);p+=h
            v=z//2+1
            if v>n:raise ValueError('out of range')
            row.append(-v if z%2 else v)
        if len(set(map(abs,row)))!=3:raise ValueError('not proper')
        c.append(tuple(row))
    return n,c

def roundtrip(c,n):
    t=serialize(c,n);n2,c2=parse(t)
    ck(n2==n and c2==list(map(tuple,c)),'exact ordinary roundtrip')
    DATA['ordinary_roundtrips']+=1
    return t,c2

def sat(clauses):
    DATA['sat_calls']+=1
    def rec(a):
        a=dict(a)
        while True:
            alive=[];units=[]
            for c in clauses:
                residual=[];satisfied=False
                for lit in c:
                    v=abs(lit)
                    if v in a:
                        if a[v]==(lit>0):satisfied=True;break
                    else:residual.append(lit)
                if satisfied:continue
                if not residual:return False
                alive.append(residual)
                if len(residual)==1:units.append(residual[0])
            if not alive:return True
            if units:
                progressed=False
                for lit in units:
                    v=abs(lit);b=lit>0
                    if v in a:
                        if a[v]!=b:return False
                    else:a[v]=b;progressed=True
                if progressed:continue
            v=abs(alive[0][0]);return rec({**a,v:False}) or rec({**a,v:True})
    return rec({})

def pinned_sat(P,n,assign):
    b=Builder(n);c=list(P)
    for v,val in sorted(assign.items()):c.extend(b.pin(v if val else -v))
    bits,child=roundtrip(c,b.n)
    return sat(child),len(bits),len(child)

def cylinder(P,n,x,Y):
    """ALL named Y assignments; each query is a complete ordinary proper-3CNF child."""
    size_max=0;decisions=[]
    for values in product((0,1),repeat=len(Y)):
        p=dict(zip(Y,values))
        a,len0,_=pinned_sat(P,n,{**p,x:0})
        b,len1,_=pinned_sat(P,n,{**p,x:1})
        decisions.append((list(values),a,b))
        size_max=max(size_max,len0,len1)
    return all(v==w for _,v,w in decisions),decisions,size_max

def rename_left(P,x,new):
    return [tuple((new if l==x else (-new if l==-x else l)) for l in c) for c in P]

def full_status(P,Q,n):
    bits,c=roundtrip(list(P)+list(Q),n)
    return sat(c),len(bits),len(c)

def run_twolevel(label,nonaffine=False):
    # Fixed shared x,y,z are original source names 1,2,3 in both modules.
    # P projects to exactly z=0; x,y are semantically independent and may be split.
    b=Builder(5)
    if nonaffine:
        # Formula has nonaffine-looking mixed clauses and is projected TRUE for x,y:
        # independently set private u=1 and v=0.
        P=[(1,2,4),(-1,-2,-5)]
    else:
        P=b.eq(1,4)+b.eq(2,5)
    P+=b.pin(-3)
    n=b.n
    q=Builder(n)
    Q=q.pin(1)+q.pin(-2)+q.pin(-3 if label=='SAT' else 3)
    n=q.n
    original,N0,m0=full_status(P,Q,n)
    ck(original==(label=='SAT'),'root ground truth '+label)
    cx,trace_x,L0=cylinder(P,n,1,[2,3])
    ck(cx,'x semantic cylinder')
    # First genuine ordinary child: rename x on the left and recalculate header.
    left_x=n+1
    P1=rename_left(P,1,left_x);n1=left_x
    first,N1,m1=full_status(P1,Q,n1)
    ck(first==original,'first genuine child preserves label')
    cy,trace_y,L1=cylinder(P1,n1,2,[3])
    ck(cy,'y semantic cylinder after first split')
    left_y=n1+1
    P2=rename_left(P1,2,left_y);n2=left_y
    second,N2,m2=full_status(P2,Q,n2)
    ck(second==original,'second genuine child preserves label')
    ck(not any(abs(l) in [1,2] for c in P2 for l in c),'left names are truly split')
    ck(any(abs(l)==3 for c in P2 for l in c),'unforgotten z still source named')
    ck(any(abs(l)==3 for c in Q for l in c),'suffix still contains original z')
    DATA['two_level'].append({'case':label+('_nonaffine' if nonaffine else '_affine'),
      'root_label':original,'child1_label':first,'child2_label':second,
      'n':[n,n1,n2],'m':[m0,m1,m2], 'encoded_N':[N0,N1,N2],
      'certified_names':[1,2], 'retained_source_name':3,
      'certificate_queries':2*(len(trace_x)+len(trace_y)),
      'max_cert_query_N':max(L0,L1),'prefix_relation':'z=0'})

def run_unsafe():
    b=Builder(3);P=b.pin(-1)+b.pin(-3);n=b.n
    q=Builder(n);Q=q.pin(1)+q.pin(-3);n=q.n
    ok,trace,L=cylinder(P,n,1,[3])
    ck(not ok,'unsafe x must fail semantic cylinder check')
    base,N0,_=full_status(P,Q,n)
    bad,N1,_=full_status(rename_left(P,1,n+1),Q,n+1)
    ck(base is False and bad is True,'unguarded split changes UNSAT to SAT')
    DATA['hostile'].append({'name':'unsafe_source_split','root_sat':base,
       'unguarded_child_sat':bad,'cylinder':ok,'pin_query_N':L,
       'encoded_N':[N0,N1]})
    # Same-name z join is essential: disjoint/renamed variable makes both independent blocks SAT.
    p=Builder(3);P=p.pin(-3);q=Builder(p.n);Q=q.pin(3);n=q.n
    u,_,_=full_status(P,Q,n);v,_,_=full_status(P,rename_left(Q,3,n+1),n+1)
    ck(not u and v,'source-named incompatible join')
    DATA['hostile'].append({'name':'same_original_z_glue','parent_sat':u,
                             'incorrectly_renamed_sat':v})
    # A raw formula XOR miter is not exact for existential projections:
    # P(x,u) = (x iff u), so exists-u P(x,u) = TRUE for both x.
    r=Builder(2);E=r.eq(1,2)
    cx,trace,L=cylinder(E,r.n,1,[])
    ck(cx and all(a==bb==True for _,a,bb in trace),'existential cylinder TRUE')
    # Witnesses with same u=0 disagree under x=0 and x=1.
    p0,_L,_=pinned_sat(E,r.n,{1:0,2:0})
    p1,_L,_=pinned_sat(E,r.n,{1:1,2:0})
    ck(p0 and not p1,'pointwise miter would falsely reject')
    DATA['hostile'].append({'name':'existential_miter_false_positive',
      'projection_cylinder':cx,'P_x0_u0':p0,'P_x1_u0':p1})

def run_qbf_reduction():
    # Baseline phi(y,u,v) with y=2 universal, u=3,v=4 existential.
    truephi=[(2,3,4),(-2,3,4)] # u=1 works for both y bits.
    falsephi=[(-2,3,4),(-2,3,-4),(-2,-3,4),(-2,-3,-4)] # y=1 forces all four patterns.
    for name,phi,truth in [('true',truephi,True),('false',falsephi,False)]:
        b=Builder(4);P=[]
        for c in phi:P.extend(b.gate(1,c))
        root,N,_=full_status(P,[],b.n)
        cy,trace,L=cylinder(P,b.n,1,[2])
        truth_by_enum=all(any(all(any((vals[abs(l)] if l>0 else not vals[abs(l)]) for l in c)
                      for c in phi)
                   for u,v in product((False,True),repeat=2)
                   for vals in [{2:y,3:u,4:v}])
                   for y in (False,True))
        ck(truth_by_enum==truth,'QBF truth enumeration')
        ck(cy==truth,'Pi2 reduction semantic cylinder')
        # x=0 is identically satisfiable, x=1 is phi after existential extension.
        ck(all(a==True for _,a,_ in trace),'universal x=0 arm')
        DATA['qbf'].append({'case':name,'forall_y_exists_uv_phi':truth,
            'cylinder':cy,'ordinary_gate_parent_N':N,'ordinary_query_max_N':L,
            'x0_x1_by_y':trace})

def main():
    for x in ['SAT','UNSAT']:
        run_twolevel(x,False)
        run_twolevel(x,True)
    run_unsafe()
    run_qbf_reduction()
    t=serialize([(1,2,3)],3)
    bad=False
    try:parse(t[:-1])
    except ValueError:bad=True
    ck(bad,'malformed encoded tail must reject')
    DATA['malformed_reject']=bad
    DATA['status']='PROVED/EXACT restricted symbolic theorem in report; COMPUTATIONAL finite audit; ARC all-input favorable edge OPEN'
    return DATA

if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
