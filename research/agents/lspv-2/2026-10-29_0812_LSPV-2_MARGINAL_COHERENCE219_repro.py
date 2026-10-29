#!/usr/bin/env python3
"""LSPV-2 marginal-only splice counterexample. Python stdlib, deterministic."""
from collections import Counter, defaultdict
from itertools import product
from math import ceil,log2
import json,hashlib

class Builder:
    def __init__(self): self.next=0;self.clauses=[];self.modules=[]
    def var(self): self.next+=1;return self.next
    def clause(self,*lits):
        assert len(lits)==3 and len({abs(x) for x in lits})==3
        self.clauses.append(tuple(lits))
    def binary(self,l,r):
        w=self.var();self.clause(l,r,w);self.clause(l,r,-w)
    def pin_zero(self,v):
        u,w=self.var(),self.var()
        for s,t in product((1,-1),repeat=2):self.clause(-v,s*u,t*w)
    def A(self,kind):
        a,b,c=(self.var() for _ in range(3))
        if kind=='E': self.binary(-a,b);self.binary(a,-b)
        else:
            assert kind=='X'
            self.binary(a,b);self.binary(-a,-b)
        self.pin_zero(c);self.modules.append((kind,a,b,c))
    def B(self):
        a,b,c=(self.var() for _ in range(3))
        for v in (a,b,c):self.pin_zero(v)
        self.modules.append(('B',a,b,c))
    def finish(self):
        M=self.modules
        for i,(_,a,b,c) in enumerate(M):
            previous_a=M[(i-1)%len(M)][1]
            self.clause(previous_a,b,c)
        return tuple(self.clauses),self.next

def family(k,sat=False,j=0):
    assert k>=1 and 0<=j<k
    b=Builder();b.B()
    for i in range(k):b.A('E' if sat and i==j else 'X')
    C,n=b.finish()
    return C,n,b.modules

def cnf_eval(C,assignment):
    return all(any((assignment[abs(l)]==1) == (l>0) for l in c) for c in C)

def dp_profile(kind):
    return ({(0,0),(1,1)} if kind=='E' else
            {(0,1),(1,0)} if kind=='X' else {(0,0)})

def transfer_trace(profiles):
    k=len(profiles)
    matrices=[]
    for p in profiles:
        matrices.append(tuple(tuple(int(any(v==a and (u or d) for a,d in p)) for v in (0,1)) for u in (0,1)))
    mat=((1,0),(0,1))
    for B in matrices:
        mat=tuple(tuple(int(any(mat[i][h] and B[h][j] for h in (0,1))) for j in (0,1)) for i in (0,1))
    return bool(mat[0][0] or mat[1][1]),mat,matrices

def dpll(C):
    calls=0;units=0
    def rec(C,assign):
        nonlocal calls,units
        calls+=1
        while True:
            residual=[];unit=None
            for clause in C:
                if any((abs(l) in assign and assign[abs(l)]==(l>0)) for l in clause):continue
                todo=[l for l in clause if abs(l) not in assign]
                if not todo:return False
                if len(todo)==1:unit=todo[0];break
                residual.append(todo)
            if unit is None:break
            v=abs(unit);p=unit>0
            if v in assign and assign[v]!=p:return False
            assign[v]=p;units+=1
        if not residual:return True
        sizes=Counter(abs(l) for cl in residual for l in cl)
        pivot=max(sizes,key=lambda v:(sizes[v],-v))
        for bit in (False,True):
            nxt=assign.copy();nxt[pivot]=bit
            if rec(C,nxt):return True
        return False
    ans=rec(C,{})
    return ans,calls,units

def connected(C,n):
    adj=[set() for _ in range(n+1)]
    for clause in C:
        a,b,c=map(abs,clause)
        adj[a].update((b,c));adj[b].update((a,c));adj[c].update((a,b))
    stack=[1];seen={1}
    while stack:
        for w in adj[stack.pop()]:
            if w not in seen:seen.add(w);stack.append(w)
    return len(seen)==n

def metrics(C,n):
    ct=Counter((abs(v),v>0) for c in C for v in c)
    scopes=Counter(tuple(sorted(abs(v) for v in c)) for c in C)
    return ct,scopes,max(sum(ct[(i,sg)] for sg in (True,False)) for i in range(1,n+1))

def encoding(C,n):
    w=ceil(log2(64*(n+len(C)+1)))
    return {'variables':n,'clauses':len(C),'fixed_record_word_bits':w,
            'source_bits':(4*len(C)+2)*w,'raw_clause_literals':3*len(C),
            'distinct_wire_name_occurrences':len(C)*3}

def small_exhaustive(C,n):
    assert n<=16
    satcount=0
    for mask in range(1<<n):
        a=[0]+[(mask>>(v-1))&1 for v in range(1,n+1)]
        if cnf_eval(C,a):satcount+=1
    return satcount

def profile_by_exhaustive(kind):
    C,n,M=family(1,sat=(kind=='E'))
    # Local A variables are names 10..16. Evaluate A-only constraints, without its designated clause.
    # Module B has 9 variables; A 7. Last clause is B's spliced clause, second-last is A's.
    apart=[cl for cl in C[:-2] if all(abs(l)>9 for l in cl)]
    a,b,c=M[1][1:]
    pairs=set()
    for mask in range(1<<7):
        val=[0]* (n+1)
        for j,v in enumerate(range(10,17)): val[v]=(mask>>j)&1
        if cnf_eval(apart,val):pairs.add((val[a],val[b] or val[c]))
    assert pairs==dp_profile(kind)
    return sorted([list(x) for x in pairs])

def validate_pair(C1,C2,n):
    A,sc1,m1=metrics(C1,n)
    B,sc2,m2=metrics(C2,n)
    assert A==B and sc1==sc2 and m1<=5 and m2<=5
    assert connected(C1,n) and connected(C2,n)
    assert len(set(C1))==len(C1)==len(C2)==len(set(C2))
    for C in (C1,C2):
        assert all(len({abs(x) for x in c})==3 for c in C)
    return m1

def yes_no_base_bits():
    w_yes=ceil(log2(64*(3+1+1)))
    w_no=ceil(log2(64*(3+8+1)))
    return {'YES':6*w_yes,'NO':34*w_no}


def encode_bits(C,n):
    w=ceil(log2(64*(n+len(C)+1)))
    words=[n,len(C)]
    for clause in C:
        words += [3]+[2*abs(v)+int(v<0) for v in clause]
    assert max(words)<(1<<w)
    return ''.join(format(v,f'0{w}b') for v in words)

def decode_bits(bits):
    if not bits or any(c not in '01' for c in bits):return None
    L=len(bits)
    for w in range(1,min(L,L.bit_length()+9)+1):
        if L%w:continue
        cnt=L//w
        if cnt<6 or (cnt-2)%4:continue
        n=int(bits[:w],2);m=int(bits[w:2*w],2)
        if n<3 or m<1 or cnt!=4*m+2:continue
        if w!=ceil(log2(64*(n+m+1))):continue
        C=[];good=True
        for i in range(m):
            fields=[int(bits[(2+4*i+j)*w:(3+4*i+j)*w],2) for j in range(4)]
            if fields[0]!=3:good=False;break
            lits=[]
            for field in fields[1:]:
                v=field//2
                if not (1<=v<=n):good=False;break
                lits.append(-v if field%2 else v)
            if not good or len({abs(v) for v in lits})!=3:good=False;break
            C.append(tuple(lits))
        if good:return tuple(C),n,w
    return None

def recognize_child(bits):
    source=decode_bits(bits)
    if source is None:return 'INVALID'
    C,n,w=source
    yes=((1,2,3),)
    no=tuple(tuple(s*(i+1) for i,s in enumerate(pattern))
            for pattern in product((1,-1),repeat=3))
    if n==3 and C==yes:return 'BASE_YES'
    if n==3 and C==no:return 'BASE_NO'
    if (n-9)%7:return 'INVALID'
    k=(n-9)//7
    if k<1 or len(C)!=9*k+13:return 'INVALID'
    U,_,_=family(k,False)
    if C==U:return 'SOURCE_NO'
    # All positive instances have exactly one E module. First match may terminate.
    for j in range(k):
        S,_,_=family(k,True,j)
        if C==S:return 'SOURCE_YES'
    return 'INVALID'

def certify_child(C,n):
    parent=encode_bits(C,n)
    label=recognize_child(parent)
    assert label in ('SOURCE_YES','SOURCE_NO')
    yes=((1,2,3),)
    no=tuple(tuple(s*(i+1) for i,s in enumerate(pattern))
            for pattern in product((1,-1),repeat=3))
    base=encode_bits(yes,3) if label=='SOURCE_YES' else encode_bits(no,3)
    assert recognize_child(base)==('BASE_YES' if label=='SOURCE_YES' else 'BASE_NO')
    return label,len(parent),len(base)

def hostile_encoding_checks():
    C,n,_=family(4,False)
    bitstring=encode_bits(C,n)
    assert decode_bits(bitstring)==(C,n,ceil(log2(64*(n+len(C)+1))))
    assert recognize_child(bitstring)=='SOURCE_NO'
    rejected=0
    for i in range(0,len(bitstring),max(1,len(bitstring)//43)):
        adversary=bitstring[:i]+('1' if bitstring[i]=='0' else '0')+bitstring[i+1:]
        if recognize_child(adversary)=='INVALID':rejected+=1
    assert rejected>=40
    assert recognize_child('x'+bitstring)=='INVALID'
    assert recognize_child(bitstring+'1')=='INVALID'
    return {'single_bit_mutations_rejected':rejected,'nonbit_header_rejected':True,'extra_bit_rejected':True}

def main():
    # Check handoff premises independently; this audit is for ordinary bounded-degree 3CNF, not exact22.
    cases=[];total_calls=0;checked=0
    for k in (1,2,3,4,5,8,16,32,64):
        C0,n,M0=family(k,sat=False)
        C1,n1,M1=family(k,sat=True,j=k//2)
        assert n==n1==7*k+9
        assert len(C0)==len(C1)==9*k+13
        maxocc=validate_pair(C0,C1,n)
        A0=[dp_profile(x[0]) for x in M0]
        A1=[dp_profile(x[0]) for x in M1]
        # For all A modules, both one-coordinate marginals equal {0,1}, same row counts.
        for profiles in (A0,A1):
            for i,P in enumerate(profiles):
                if i==0:assert P=={(0,0)}
                else:assert {a for a,_ in P}=={0,1} and {d for _,d in P}=={0,1} and len(P)==2
        v0,mat0,_=transfer_trace(A0)
        v1,mat1,_=transfer_trace(A1)
        assert (v0,v1)==(False,True)
        result={'k':k,'sources':encoding(C0,n),'max_occurrences':maxocc,'changed_module':k//2+1,
                'U_trace_matrix':mat0,'S_trace_matrix':mat1,
                'same_unsigned_clause_scope_multiset':True,
                'same_per_variable_signed_incidence':True,
                'all_module_one_coordinate_marginals_identical':True}
        if k<=8:
            d0,c0,u0=dpll(C0);d1,c1,u1=dpll(C1)
            assert (d0,d1)==(False,True)
            result['independent_DPLL']={'U':{'answer':d0,'calls':c0,'unit_prop':u0},'S':{'answer':d1,'calls':c1,'unit_prop':u1}}
            total_calls+=c0+c1
        if k==1:
            e0=small_exhaustive(C0,n);e1=small_exhaustive(C1,n)
            assert e0==0 and e1>0
            result['complete_truth_tables']={'assignments_per_source':2**n,'U_witnesses':e0,'S_witnesses':e1}
            checked+=2*(2**n)
        cases.append(result)
    assert profile_by_exhaustive('E')==[[0,0],[1,1]]
    assert profile_by_exhaustive('X')==[[0,1],[1,0]]
    hostile=hostile_encoding_checks()
    # The four changed sign flags are disjoint between modules, giving k probe adversary.
    for c in cases:
        k=c['k'];U,n,_=family(k,False);S,_,_=family(k,True,k//2)
        ub=encode_bits(U,n);sb=encode_bits(S,n)
        assert len(ub)==len(sb)==c['sources']['source_bits']
        diff=[i for i,(a,b) in enumerate(zip(ub,sb)) if a!=b]
        assert len(diff)==4
        assert all((i//c['sources']['fixed_record_word_bits'])>=2 for i in diff)
        c['physical_bit_hamming_distance']=len(diff)
        if True:
            a,p,ch=certify_child(U,n);b,p2,ch2=certify_child(S,n)
            assert (a,b)==('SOURCE_NO','SOURCE_YES') and p==p2
            c['authenticated_child_bits']={'U':ch,'S':ch2}
    base=yes_no_base_bits()
    for c in cases:
        c['N_bits_threshold_3_4']=(c['sources']['source_bits']**0.75)>=base['NO']
    assert cases[-1]['N_bits_threshold_3_4']
    obj={'run':'LSPV2-MARGINAL-COHERENCE219','status':'PASS','seed':'none exhaustive or deterministic',
         'exact_module_profiles':{'E':[[0,0],[1,1]],'X':[[0,1],[1,0]],'B':[[0,0]]},
         'base_child_bits':base,'malformed_controls':hostile,'cases':cases,'exhaustive_full_truth_table_evaluations':checked,
         'independent_DPLL_recursive_calls':total_calls,
         'limitations':['Ordinary proper connected 3CNF, bounded total occurrence 5, NOT strict exact-(2,2).',
                       'Marginal-only black-box failure does not constrain a source-aware SAT algorithm.',
                       'A recognizer for this fixed grammar is polynomial and can decide both labels easily.',
                       'Raw Python operations are not native TM steps.','P vs NP OPEN.']}
    print(json.dumps(obj,sort_keys=True,indent=2))
if __name__=='__main__':main()