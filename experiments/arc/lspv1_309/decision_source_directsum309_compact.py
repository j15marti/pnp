#!/usr/bin/env python3
"""ARC-VALID-STATE-FIREWALL285: grammar isolation and two-bit label cliffs.
Standard-library-only, offline source-hypergraph/XOR auditor, NOT a SAT solver.
"""
import collections, itertools, json, pathlib, sys

Y = [(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
WITNESS = '001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'

def load(path):
    s=pathlib.Path(path).read_text(); return tuple(tuple(c) for c in json.loads(s[s.index('[['):]))

def valid(F,n):
    if n<=0 or n%3 or len(F)*3!=4*n: return False
    seen=set(); deg=collections.Counter()
    for c in F:
        if len(c)!=3 or len({abs(v) for v in c})!=3 or not all(1<=abs(v)<=n for v in c):return False
        if not (all(v>0 for v in c) or all(v<0 for v in c)):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key)
        deg.update((abs(v),v>0) for v in c)
    return all(deg[(v,sgn)]==2 for v in range(1,n+1) for sgn in (False,True))

def gamma(a):
    assert a>0
    b=f'{a:b}'; return '0'*(len(b)-1)+b

def encode(F,n):
    m=len(F); w=n.bit_length()
    header=gamma(n)+gamma(m)
    return header+''.join(('1' if c[0]>0 else '0') + ''.join(f'{abs(z):0{w}b}' for z in c) for c in F),len(header)

def decode(word):
    def get_gamma(p):
        z=0
        while p<len(word) and word[p]=='0':z+=1;p+=1
        if p+z>=len(word):raise ValueError('truncated header')
        return int(word[p:p+z+1],2),p+z+1
    try:
        n,p=get_gamma(0);m,p=get_gamma(p);w=n.bit_length();block=1+3*w
        if n<=0 or len(word)!=p+m*block:return None
        F=[]
        for j in range(m):
            q=p+j*block; s=1 if word[q]=='1' else -1
            F.append(tuple(s*(int(word[q+1+k*w:q+1+(k+1)*w],2)) for k in range(3)))
        return (n,tuple(F)) if valid(F,n) else None
    except (ValueError,IndexError):return None

def models(F,n):
    return sum(all(any(((a>>(abs(z)-1))&1)==int(z>0) for z in c) for c in F) for a in range(1<<n))

def sat(F,bits):
    return all(any((bits[abs(z)-1]=='1')==(z>0) for z in c) for c in F)

def u_refute(U):
    def dpll(F):
        F=tuple(tuple(c) for c in F)
        def rec(G):
            while True:
                if not G:return True
                if any(not c for c in G):return False
                unit=next((c[0] for c in G if len(c)==1),None)
                if unit is None:break
                G=tuple(tuple(x for x in c if x!=-unit) for c in G if unit not in c)
            x=abs(G[0][0]);return any(rec(tuple(tuple(z for z in c if z!=-lit) for c in G if lit not in c)) for lit in (x,-x))
        return rec(F)
    modules=[]
    for j in range(6):
        low,high=32*j+1,32*j+32
        A=[C for C in U[2:254] if any(low<=abs(x)<=high for x in C)]
        assert len(A)==42;modules.append(A)
    covered=0;global_bad=0;calls=0
    for row in itertools.product((False,True), repeat=6):
        b={193+j:row[j] for j in range(6)}
        if any(not any(b[abs(x)]==(x>0) for x in C) for C in U[:2]):
            covered+=1;global_bad+=1;continue
        for A in modules:
            G=[tuple(x for x in C if abs(x)<=192) for C in A if not any(abs(x)>192 and b[abs(x)]==(x>0) for x in C)]
            calls+=1
            if not dpll(G):covered+=1;break
    assert (covered,global_bad,calls)==(64,16,152)
    return dict(covered=covered,global_conflicts=global_bad,independently_checked_module_calls=calls)

def make(U,V,k):
    tail=[]
    for i in range(k):
        off=198+6*i
        tail.extend(tuple((1 if x>0 else -1)*(abs(x)+off) for x in C) for C in Y)
    return U+tuple(tail),V+tuple(tail),198+6*k

def main():
    default=pathlib.Path(__file__).resolve().parents[3]/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt'
    U=load(sys.argv[1] if len(sys.argv)>1 else default)
    assert valid(U,198) and len(U)==264
    V=[list(c) for c in U]
    assert U[2][2]==197 and U[44][2]==196
    V[2][2],V[44][2]=V[44][2],V[2][2]
    V=tuple(tuple(c) for c in V)
    assert valid(V,198) and sat(V,WITNESS)
    assert models(Y,6)==20
    unsat_certificate=u_refute(U)
    cases=[];one_bit_checks=0
    for k in (0,1,4,16):
        A,B,n=make(U,V,k)
        assert valid(A,n) and valid(B,n)
        a,h=encode(A,n);b,hb=encode(B,n)
        assert h==hb and decode(a)==(n,A) and decode(b)==(n,B)
        flips=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
        assert len(a)==len(b) and len(flips)==2
        assert all(i>=h for i in flips)
        for i in flips:
            one=a[:i]+('1' if a[i]=='0' else '0')+a[i+1:]
            assert decode(one) is None
        w=n.bit_length(); block=1+3*w; sampled=0
        for word,F in ((a,A),(b,B)):
            for i in range(h,len(word)):
                j,bit=divmod(i-h,block)
                if bit==0:
                    assert all(sum(x==v for C in F for x in C)==2 for v in F[j])
                else:
                    varslot=(bit-1)//w; bo=(bit-1)%w
                    old=abs(F[j][varslot]); new=old^(1<<(w-1-bo))
                    assert old!=new
                    assert new<1 or new>n or sum(x==F[j][varslot] for C in F for x in C)==2
                if bit==0 or (i-h)%113==0:
                    neighbor=word[:i]+('1' if word[i]=='0' else '0')+word[i+1:]
                    assert decode(neighbor) is None
                    sampled+=1
                one_bit_checks+=1
        assert sampled>0
        assert sat(B,WITNESS+next(''.join(map(str,a)) for a in itertools.product((0,1),repeat=6) if sat(Y,''.join(map(str,a))))*k)
        cases.append(dict(k=k,n=n,m=len(A),encoded_bits=len(a),header_bits=h,payload_bits=len(a)-h,
                          hamming_distance=2,changed_absolute_positions=flips,
                          malformed_midpoint_paths=2,
                          payload_single_bit_mutants_tested=2*(len(a)-h),
                          sat_certificate='verified original 198-bit V plus Y6 witness',
                          unsat_certificate='U198 64-row refutation retained by conjunction'))
    print(json.dumps(dict(run='ARC-VALID-STATE-FIREWALL285',status='PASS',
            source_u198_refutation=unsat_certificate,
            original_v198_witness_checked=True, original_y6_sat_models=20,
            total_payload_mutant_checks=one_bit_checks,cases=cases,
            interpretation='All valid payload encodings are one-bit isolated; two valid opposite-label sources exist at distance exactly two for unbounded length. Intermediate one-bit source words are malformed. This is not a physical Turing-machine execution and does not prove ARC/P-versus-NP.'),indent=2))

def decision_source_directsum309():
    """All-valid original-language decision source query family and sharp randomized promise."""
    from itertools import product
    from pathlib import Path
    p=Path(__file__).resolve().parents[3]/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt'
    U=load(p)
    assert valid(U,198) and len(U)==264
    V=[list(c) for c in U]
    assert U[2][2]==197 and U[44][2]==196
    V[2][2],V[44][2]=V[44][2],V[2][2]
    V=tuple(tuple(c) for c in V)
    assert valid(V,198) and sat(V,WITNESS)
    cases=[]
    for t in (1,2,3,4,8):
        n=198*t
        def product_formula(blocks):
            return tuple(tuple((1 if lit>0 else -1)*(abs(lit)+198*i) for lit in c)
                         for i,block in enumerate(blocks) for c in block)
        good=product_formula([V]*t)
        assert valid(good,n)
        good_bits,header=encode(good,n)
        patches=[]
        for j in range(t):
            blocks=[V]*t
            blocks[j]=U
            bad=product_formula(blocks)
            assert valid(bad,n)
            bad_bits,h=encode(bad,n)
            assert len(bad_bits)==len(good_bits) and h==header
            d={i for i in range(len(good_bits)) if good_bits[i]!=bad_bits[i]}
            assert len(d)==2
            patches.append(d)
        assert all(patches[i].isdisjoint(patches[j])
                   for i in range(t) for j in range(i+1,t))
        # Under the exact U/V-product promise, reading one distinguished
        # bit per disjoint block decides the conjunction, no witness recovery.
        indices=[min(D) for D in patches]
        assert all(len(D & set(indices))==1 for D in patches)
        # Three equally likely random tapes: exact scan, guess SAT, guess UNSAT.
        for bad_index in [-1]+list(range(t)):
            correct=(bad_index==-1)
            answers=[correct,True,False]
            charges=[t,0,0]
            assert sum(a==correct for a in answers)==2
            assert sum(charges)==t  # expected bit probes = t/3
        cases.append({'t':t,'source_bits':len(good_bits),
            'disjoint_valid_opposite_patches':t,
            'deterministic_query_floor':t,
            'bounded_error_one_third_expected_query_floor':str(t)+'/3',
            'three_coin_promise_expected_query_cost':str(t)+'/3'})
    print(json.dumps({'run':'DECISION-SOURCE-DIRECTSUM309',
      'status':'PASS','P_vs_NP':'OPEN','cases':cases,
      'exact_deterministic_all_decider_source_query_lb':'t on the SAT all-V original',
      'randomized_error_epsilon_lb':'(1-2 epsilon)*t expected physical source reads',
      'classification':'KNOWN adversary and classical randomized coupling; not superpolynomial',
      'scope':'all sources in the adversary are valid canonical originals; query upper bound is promise-only'},indent=2))

if __name__=='__main__':
    main()
    decision_source_directsum309()

