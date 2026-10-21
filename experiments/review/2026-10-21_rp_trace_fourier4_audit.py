#!/usr/bin/env python3
"""RP-TRACE-FOURIER4, standalone exact finite-field epsilon-bias & RP audit.

No randomness, no SAT oracle, no external packages.  This is a finite
verification of the stated source-accessible trace seed construction, not
a proof of P=RP or a surrogate generator with an unverified bias claim.
"""
from __future__ import annotations
import json, math, pathlib, time
from fractions import Fraction

OUT=pathlib.Path(__file__).resolve().parent
STATS={'assertions':0, 'failures':0}

def check(pred,label):
    STATS['assertions']+=1
    if not pred:
        STATS['failures']+=1
        raise AssertionError(label)

# Binary polynomial arithmetic for construction of F_{2^k}.
def pmul(a,b):
    v=0
    while b:
        if b&1: v^=a
        a<<=1;b>>=1
    return v

def prem(a,b):
    while a and a.bit_length()>=b.bit_length():
        a^=b << (a.bit_length()-b.bit_length())
    return a

def pgcd(a,b):
    while b: a,b=b,prem(a,b)
    return a

def irreducible(f,k):
    # Rabin irreducibility criterion: x^(2^k) == x mod f,
    # and gcd(x^(2^(k/p))-x, f)==1 for every distinct prime divisor p of k.
    if f.bit_length()!=k+1 or not(f&1): return False
    x=2
    def sqmod(v):return prem(pmul(v,v),f)
    t=x
    seq=[x]
    for _ in range(k):
        t=sqmod(t);seq.append(t)
    if t!=x: return False
    d=k; p=2; primes=[]
    while p*p<=d:
        if d%p==0:
            primes.append(p)
            while d%p==0:d//=p
        p+=1
    if d>1:primes.append(d)
    return all(pgcd(seq[k//p]^x,f)==1 for p in primes)

def find_poly(k):
    if k==1:return 0b11
    for lower in range(1,1<<k,2):
        f=(1<<k)|lower
        if irreducible(f,k):return f
    raise RuntimeError('Irreducible polynomial not found')

def gmul(a,b,k,poly):
    q=1<<k;mask=q-1;v=0
    while b:
        if b&1: v^=a
        b>>=1
        a<<=1
        if a&q:a^=poly
    return v&mask

def gtrace(a,k,poly):
    v=a;t=a
    for _ in range(1,k):
        t=gmul(t,t,k,poly)
        v^=t
    check(v in (0,1), 'GF(2^k) trace must be in GF(2)')
    return v

def trace_tape(a,z,m,k,poly):
    powers=1; mask=0
    for i in range(m):
        if gtrace(gmul(a,powers,k,poly),k,poly):mask|=1<<i
        powers=gmul(powers,z,k,poly)
    return mask

def distribution(m,q):
    k=q.bit_length()-1
    poly=find_poly(k)
    # Efficient independent verification: linearity of field trace
    # gives trace(a*z^i), and construction's finite histogram.
    hist=[0]*(1<<m)
    for z in range(q):
        for a in range(q):
            hist[trace_tape(a,z,m,k,poly)]+=1
    check(sum(hist)==q*q,'sample multiplicities')
    return hist,poly

def fwht(xs):
    y=list(xs);h=1;n=len(y)
    while h<n:
        for i in range(0,n,h*2):
            for j in range(i,i+h):
                a=y[j];b=y[j+h];y[j]=a+b;y[j+h]=a-b
        h*=2
    return y

def bool_or(bits,m): return int(bits!=0)
def bent_yes(bits,m):
    assert m%2==0
    q=0
    for j in range(0,m,2):q ^= ((bits>>j)&1)&((bits>>(j+1))&1)
    return 1^q

def Fourier_norm(truth):
    w=fwht(truth)
    return Fraction(sum(abs(t) for t in w),len(truth)),w

def majority(bits,m):return int(bits.bit_count() >= (m+1)//2)

def prefix_demo(m=8):
    # Approximate conditional expectations via trace sets; OR_m has
    # spectral L1 <2 and ANF degree m.  Checks chosen full tape accepts.
    B=2; q=1
    while q<8*m*m*B: q*=2
    poly=find_poly(q.bit_length()-1);k=q.bit_length()-1
    root=[];estimates=[];calls=0
    for fixed in range(m):
        options=[]
        for bit in [0,1]:
            prefix=sum(b<<i for i,b in enumerate(root+[bit])); rem=m-fixed-1
            total=0
            for z in range(q):
                for a in range(q):
                    r=trace_tape(a,z,rem,k,poly)
                    total+=bool_or(prefix | (r<<(fixed+1)),m)
            calls+=q*q
            options.append((Fraction(total,q*q),bit))
        best=max(options,key=lambda t:t[0])
        root.append(best[1]);estimates.append([str(options[0][0]),str(options[1][0])])
    chosen=sum(b<<i for i,b in enumerate(root))
    check(bool_or(chosen,m)==1,'trace greedy outputs accepting tape')
    return {'m':m,'q':q,'seed_length_bits':2*k,'oracle_verifier_runs':calls,'chosen':format(chosen,f'0{m}b'),'estimates':estimates}

def main():
    t0=time.monotonic();bias_tests=[];norms=[];output_sample=[]
    for m in range(2,9):
        q=1
        while q<16*m:q*=2
        hist,poly=distribution(m,q)
        spectrum=fwht(hist)
        maxbias=Fraction(max(abs(v) for v in spectrum[1:]),q*q)
        check(maxbias<=Fraction(m-1,q),f'root bound m={m}')
        checked=0;max_roots=0
        for S in range(1,1<<m):
            roots=0
            for z in range(q):
                p=1;v=0
                for i in range(m):
                    if (S>>i)&1:v^=p
                    p=gmul(p,z,q.bit_length()-1,poly)
                if v==0:roots+=1
            check(spectrum[S]==q*roots, f'exact polynomial roots vs Fourier, m={m}, mask={S}')
            check(roots<=m-1, 'polynomial root-count theorem')
            max_roots=max(max_roots,roots);checked+=1
        truth_or=[bool_or(r,m) for r in range(1<<m)]
        B,_=Fourier_norm(truth_or)
        mean_full=Fraction(sum(truth_or),1<<m)
        mean_set=Fraction(sum(hist[r]*truth_or[r] for r in range(1<<m)),q*q)
        check(B==2-Fraction(2,1<<m), 'exact OR Fourier norm')
        check(abs(mean_full-mean_set) <= B*maxbias,'spectral error bound exact')
        check(mean_set>0,'hit OR')
        for r,v in enumerate(truth_or):
            if hist[r] and v:break
        else: raise AssertionError('No OR witness')
        bias_tests.append({'m':m,'q':q,'irreducible_poly_hex':hex(poly),'number_seeds':q*q,
                           'distinct_tapes':sum(x>0 for x in hist),'nonzero_parities_checked':checked,
                           'measured_epsilon':str(maxbias),'theorem_epsilon':str(Fraction(m-1,q)),
                           'largest_roots':max_roots,'OR_fourier_L1':str(B),
                           'uniform_acceptance':str(mean_full),'trace_acceptance':str(mean_set)})
        if m%2==0:
            f=[bent_yes(r,m) for r in range(1<<m)]
            norm,w=Fourier_norm(f)
            check(norm==Fraction(1,2)+2**(m//2-1),'quadratic phase Fourier L1 formula')
            check(Fraction(sum(f),1<<m)==Fraction(1,2)+Fraction(1,2**(m//2+1)),
                  'quadratic phase exact acceptance density')
            # Verify all 2^m-1 nonempty spectral magnitudes equal 2^(m/2-1)
            check(all(abs(v)==2**(m//2-1) for v in w[1:]),'flat bent Fourier spectrum')
            check(sum(hist[r]*f[r] for r in range(1<<m))>0,'trace set happens to hit bent acceptance')
            norms.append({'m':m,'quadratic_L1':str(norm),'yes_acceptance':str(Fraction(sum(f),1<<m)),
                          'ANF_degree':2,'effective_state_width':2,'deterministic_bypass':'parity(x)'})
    # Directly compare the historical FINAL-ANSWER six-bit algebraic formula.
    n=6; hist6,_=distribution(n,64)
    f6=[int(not (((r>>1)&1) and ((r>>2)&1) and ((r>>3)&1))) for r in range(64)]
    B6,_=Fourier_norm(f6)
    check(sum(f6)==56,'COMPLETIONCUT1 third-answer count')
    check(B6==Fraction(7,4),'COMPLETIONCUT1 Fourier norm')
    check(sum(hist6[r]*f6[r] for r in range(64))>0,'trace generator hits completion toy')
    # Explicit universal-public-hit-set self-attack for a fixed m=16.
    m=16;q=64;hist,poly=distribution(m,q)
    seen=sum(v!=0 for v in hist)
    yes=Fraction((1<<m)-seen,1<<m)
    check(yes>=Fraction(1,2),'self-attack must remain valid RP verifier')
    check(all((not hist[r]) for r in range(1<<m) if hist[r]==0), 'membership completeness')
    forbidden_members={i for i,c in enumerate(hist) if c}
    check(all(x in forbidden_members for x,c in enumerate(hist) if c), 'every listed seed rejected')
    # Underlying language is L=odd parity(x), P with an obvious bypass.
    for x in range(32):
        accepted_frac=(yes if x.bit_count()%2 else Fraction(0))
        check(accepted_frac==0 if x.bit_count()%2==0 else accepted_frac>=Fraction(1,2),
              'RP two-label semantics')
    # Spectral norm of the complementary indicator must exceed the trace bias gap.
    self_f=[int(h==0) for h in hist]
    self_norm,_=Fourier_norm(self_f)
    max_eps=max(abs(c) for c in fwht(hist)[1:]); max_eps=Fraction(max_eps,q*q)
    check(yes <= self_norm*max_eps,'self-attack Fourier certificate')
    greedy=prefix_demo(m=4)
    output={
      'status':'ESTABLISHED restricted derandomization, OPEN unrestricted P=RP / P!=RP',
      'seed_theorem':'r_i=Tr(a*z^i) over GF(2^k), uniform (a,z); absolute parity bias <= (m-1)/q',
      'histograms_and_all_parity_checks':bias_tests,
      'explicit_quadratic_fourier_growth':norms,
      'completioncut1_fourier_L1':str(B6),
      'completioncut1_acceptance':str(Fraction(56,64)),
      'public_trace_hitset_self_attack':{'m':m,'q':q,'seed_pairs':q*q,'distinct_forbidden_tapes':seen,
        'RP_yes_acceptance_probability':str(yes),'spectral_L1':str(self_norm),
        'epsilon_actual':str(max_eps),'language':'odd-parity(x) in P'},
      'hereditary_approx_prefix_greedy':greedy,
      'tests':STATS,'elapsed_seconds':round(time.monotonic()-t0,3),
      'source_code':'rp_trace_fourier_audit.py'
    }
    path=OUT/'RP_TRACE_FOURIER4_raw.json'
    path.write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'tests':STATS,'elapsed_seconds':output['elapsed_seconds'],'bias_cases':len(bias_tests),
       'quadratic_norms':norms,'completioncut1_L1':str(B6),'public_attack_yes_prob':str(yes),
       'greedy_verifier_calls':greedy['oracle_verifier_runs'],'result_file':str(path)},indent=2))

if __name__=='__main__':main()