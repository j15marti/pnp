#!/usr/bin/env python3
"""Standard-library audit: strict signed occurrence, exact affine, source-ID branching.
Seed 202610252228. Finite tests only, no hardness claim.
"""
import collections, itertools, json, os, random
from fractions import Fraction
R=random.Random(202610252228); K=collections.Counter()
def ok(b,name):
    K['assertions']+=1
    if not b:raise AssertionError(name)
def parity(a):return sum(a)%2
def bundle(vs,b):
    return [tuple(-v if bit else v for v,bit in zip(vs,a))
            for a in itertools.product((0,1),repeat=3) if parity(a)!=b]
def holds(F,a):return all(any(a[abs(z)]==(z>0) for z in C) for C in F)
def sat(F,n):return any(holds(F,dict(enumerate(bits,1))) for bits in itertools.product((0,1),repeat=n))
def signed22(F,n):
    D=collections.defaultdict(lambda:[0,0])
    for C in F:
        if len(C)!=3 or len(set(map(abs,C)))!=3:return False
        for z in C:D[abs(z)][z<0]+=1
    return len(D)==n and all(D[i]==[2,2] for i in range(1,n+1))
def xor(A,B):return A^B
def mul(A,B):
    C=set()
    for x in A:
        for y in B:
            z=tuple(sorted(x+y)); C.symmetric_difference_update({z})
    return C
def polynomial(C):
    P={()}
    for z in C:P=mul(P,{()}|{(z,)} if z>0 else {(abs(z),)})
    return P
def linearized(F):
    P=set()
    for C in F:P=xor(P,polynomial(C))
    return P
def pin(L,a,b):return [(L,a,b),(L,a,-b),(L,-a,b),(L,-a,-b)]
# Certificates: ('branch', variable, left, right), ('leaf', original_clause_id),
# ('affine', disjoint tuples of four original clause ids), ('A',).
def verify(F,n,cert,assigned=None):
    if assigned is None:assigned={}
    if not isinstance(cert,tuple) or not cert:return False
    if cert[0]=='leaf' and len(cert)==2:
        j=cert[1]
        return type(j)==int and 0<=j<len(F) and all(abs(z) in assigned and assigned[abs(z)]!=(z>0) for z in F[j])
    if cert[0]=='branch' and len(cert)==4:
        _,v,l,r=cert
        if type(v)!=int or not 1<=v<=n or v in assigned:return False
        return verify(F,n,l,{**assigned,v:False}) and verify(F,n,r,{**assigned,v:True})
    if cert[0]=='A' and len(cert)==1:
        child=[tuple(z for z in C if abs(z) not in assigned) for C in F
               if not any(abs(z) in assigned and assigned[abs(z)]==(z>0) for z in C)]
        return not sat(child,n) # finite exact A, no claimed labels trusted
    if cert[0]=='affine' and len(cert)==2 and not assigned:
        used=set();P=set()
        for ids in cert[1]:
            if len(ids)!=4 or len(set(ids))!=4 or any(type(i)!=int or i<0 or i>=len(F) or i in used for i in ids):return False
            used.update(ids);Cs=[F[i] for i in ids]
            vs=tuple(sorted(set(map(abs,Cs[0]))))
            if len(vs)!=3 or not any(set(Cs)==set(bundle(vs,b)) for b in (0,1)):return False
            P=xor(P,linearized(Cs))
        return P=={()}
    return False
def build(F,n):
    def rec(i,a):
        for j,C in enumerate(F):
            if all(abs(z) in a and a[abs(z)]!=(z>0) for z in C):return ('leaf',j)
        if i>n:return None
        l=rec(i+1,{**a,i:False});r=rec(i+1,{**a,i:True})
        return ('branch',i,l,r) if l and r else None
    return rec(1,{})
for b in (0,1):
    F=bundle((1,2,3),b)
    ok(signed22(F,3),'single XOR bundle uses 2P2N')
    ok(linearized(F)=={(1,),(2,),(3,)}^({()} if b else set()),'degree-three field-2 identity')
    for x in itertools.product((0,1),repeat=3):
        ok(holds(F,dict(enumerate(x,1)))==(parity(x)==b),'parity truth table')
    K['xor_bundles']+=1
for b,c in itertools.product((0,1),repeat=2):
    shared=bundle((1,2,3),b)+bundle((1,4,5),c)
    ok(sum(1 for C in shared for z in C if z==1)==4 and sum(1 for C in shared for z in C if z==-1)==4,'shared degree saturates')
    ok(not signed22(shared,5),'shared direct gadgets not exact 2P2N')
    apart=bundle((1,2,3),b)+bundle((4,5,6),c)
    ok(signed22(apart,6) and sat(apart,6),'disjoint bundles SAT and strict 2P2N')
    K['paired_bundles']+=1
E=list(itertools.combinations(range(4),2)) # K4 cubic
incident={v:tuple(i+1 for i,e in enumerate(E) if v in e) for v in range(4)}
for t in range(16):
    G=sum((bundle(incident[v],(t>>v)&1) for v in range(4)),[])
    ok(sat(G,6)==(t.bit_count()%2==0),'K4 signed Tseitin parity')
    ok(all(sum(z==e for C in G for z in C)==4 and sum(z==-e for C in G for z in C)==4 for e in range(1,7)),'edge occurs 4P4N, not 2P2N')
    cert=('affine',tuple(tuple(range(i*4,(i+1)*4)) for i in range(4)))
    ok(verify(G,6,cert)==(t.bit_count()%2==1),'exact full-source GF2 cancellation')
    K['K4_charge_controls']+=1
odd=sum((bundle(incident[v],int(v==0)) for v in range(4)),[])
cert=('affine',tuple(tuple(range(i*4,(i+1)*4)) for i in range(4)))
ok(verify(odd,6,cert),'auditable odd Tseitin UNSAT')
ok(not verify(odd,6,('affine',cert[1][:-1])),'no free missing gadget')
ok(not verify(odd,6,('affine',((0,1,2,3),(0,5,6,7),(8,9,10,11),(12,13,14,15)))),'duplicate clause IDs rejected')
F=list(odd);F[0]=tuple(-z for z in F[0]);ok(not verify(F,6,cert),'mutated source rejected')
# Strict connected signed (2,2)-3CNF positive control, NAE pair on prism.
E=sorted({(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)})
prism=[]
for v in range(6):
    q=tuple(i+1 for i,e in enumerate(E) if v in e)
    prism += [q,tuple(-x for x in q)]
ok(signed22(prism,9) and sat(prism,9),'strict connected 2P2N SAT')
ok(not verify(prism,9,('A',)),'SAT leaf A cannot certify UNSAT')
join=pin(1,2,3)+pin(-1,4,5);alias=pin(1,2,3)+pin(-7,4,5)
ok(not sat(join,5) and sat(alias,7),'global source alias join')
ok(verify(join,5,('A',)) and not verify(alias,7,('A',)),'source-name A calls')
# Both-label hostile ordinary cases: complete branching iff UNSAT.
cases=[([(1,),(-1,)],1), ([(1,)],1), ([(1,2),(-1,2),(1,-2),(-1,-2)],2),
       ([(1,),(-1,2),(-2,)],2), (odd,6), (prism,9)]
for _ in range(80):
    n=R.randrange(2,7);F=[]
    for _ in range(R.randrange(1,18)):
        vs=R.sample(range(1,n+1),min(3,n))
        F.append(tuple(v if R.getrandbits(1) else -v for v in vs))
    cases.append((F,n))
for F,n in cases:
    c=build(F,n); label=sat(F,n)
    ok((c is None)==label,'complete branch existence exactly UNSAT')
    if c:ok(verify(F,n,c),'source-ID branch verifier sound')
    ok(verify(F,n,('A',))== (not label),'fixed A result not free')
    K['branch_controls']+=1
for _ in range(128):
    a=[R.randrange(1,30) for i in range(R.randrange(1,10))];d=Fraction(R.randrange(10,31),10)
    M=max(a);V=sum(a)
    ok(sum(x**float(d) for x in a)<=M**(float(d)-1)*V+1e-8,'sum m_i^d <= M^(d-1) V')
    K['leaf_ledger_controls']+=1
result={'run':'LSPV3_CERTIFICATE_PARITY_FIREWALL124','seed':202610252228,
        'checks':dict(K),'K4_odd_UNSAT':True,'prism_strict_2P2N_SAT':True,
        'strict_2P2N_UNSAT_source':'Döcker Appendix C repository original; structural-only check performed separately; brute-force status inherited',
        'scope':'finite truth tables, GF2 polynomial identities, source-ID certificate syntax; no asymptotic verification time bound'}
p=os.path.join(os.path.dirname(__file__),'2026-10-25_2228_CERT_PARITY124_raw.json')
with open(p,'w') as f:json.dump(result,f,indent=2,sort_keys=True)
print(json.dumps(result,indent=2,sort_keys=True))
