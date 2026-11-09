#!/usr/bin/env python3
"""LSPV-1/536: finite controls for a conditional guest-space padding counterexample.
No external claimed subexponential SAT algorithm is implemented or executed.
"""
import itertools, json, math, os, sys, time

def truth(formula, bits):
    return all(any((bits[abs(l)-1] if l>0 else not bits[abs(l)-1]) for l in clause) for clause in formula)

def guest_bruteforce(formula, n):
    if not isinstance(n,int) or n<0 or not isinstance(formula,list):
        raise ValueError('malformed')
    for clause in formula:
        if not isinstance(clause,list) or len(clause)>3 or any(type(l)!=int or l==0 or abs(l)>n for l in clause):
            raise ValueError('malformed')
    return any(truth(formula,bits) for bits in itertools.product((False,True),repeat=n))

def padded_guest_finite(formula,n):
    # Deliberately exercise all 2^floor(sqrt(n)) scratch bits for tiny n only.
    scratch_bits = 1 << math.isqrt(n)
    if scratch_bits>1_000_000: raise ValueError('tiny-only execution guard')
    scratch=bytearray((scratch_bits+7)//8)
    for bit in range(scratch_bits): scratch[bit>>3] |= 1<<(bit&7)
    assert all(b==255 for b in scratch[:scratch_bits//8])
    result=guest_bruteforce(formula,n)
    return result, scratch_bits

def f(n,alpha=.5,d=2):
    return n * math.log2(math.log2(n+16))**d / math.log2(n+16)**alpha

def run():
    checks=0; finite=[]
    cases=[('SAT-units',[[1],[2]],2,True),('UNSAT-unit-conflict',[[1],[-1]],1,False),
           ('SAT-or',[[1,2,3]],3,True),('UNSAT-empty-clause',[[]],0,False),
           ('SAT-empty-formula',[],0,True),('UNSAT-8-all-triples',[[i*a,j*b,k*c] for i in (1,-1) for j in (1,-1) for k in (1,-1) for a,b,c in [(1,2,3)]],3,False)]
    for name,formula,n,expected in cases:
        native=guest_bruteforce(formula,n)
        padded,scratch=padded_guest_finite(formula,n)
        assert native==padded==expected;checks+=2
        finite.append({'case':name,'n':n,'answer':padded,'scratch_bits_written':scratch})
    rejected=[]
    for malformed,n in [([[0]],1),([[2]],1),([[1,2,3,4]],4),([[1.5]],2),('abc',2)]:
        try: padded_guest_finite(malformed,n)
        except ValueError: rejected.append(str(malformed));checks+=1
        else: raise AssertionError('malformed input accepted')
    # Symbolic high-water marks, NOT physical allocations or a SAT runtime test.
    grids=[]
    for alpha,d in [(0,0),(.5,2),(2,1)]:
        for m in [16,20,24,28,32,36,40]:
            n=1<<m
            space_log2=math.isqrt(n)  # S(n) = 2^floor(sqrt(n)) bits
            guest_exp=f(n,alpha,d)
            assert space_log2 < guest_exp
            checks+=1
            Nbits=16*n*m   # a legitimate O(n log n)-length source scale
            log2N=math.log2(Nbits)
            grids.append({'alpha':alpha,'d':d,'n':n,'log2_guest_extra_space_bits':space_log2,
                          'guest_time_exponent_budget':round(guest_exp,3),
                          'log2_Nbits':round(log2N,3),
                          'space_exceeds_N_to_4':space_log2>4*log2N})
    assert all(r['space_exceeds_N_to_4'] for r in grids)
    checks+=len(grids)
    return {'status':'FINITE_CONTROLS_ONLY','checks':checks,'cases':finite,
            'malformed_rejections':rejected,'resource_samples':grids,
            'qualification':'No external G executed; hypothetical G prime has 2^floor(sqrt(n)) scratch bits; symbolic math in report proves asymptotics.'}

if __name__=='__main__':
    t=time.monotonic(); data=run();data['elapsed_sec']=round(time.monotonic()-t,5)
    outfile=sys.argv[1] if len(sys.argv)>1 else None
    if outfile:
        with open(outfile,'w') as w:json.dump(data,w,indent=2);w.write('\n')
    print(json.dumps({'status':data['status'],'checks':data['checks'],'elapsed_sec':data['elapsed_sec'],'all_controls_passed':True}))
