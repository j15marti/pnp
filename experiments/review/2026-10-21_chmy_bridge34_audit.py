#!/usr/bin/env python3
"""CHMY BRIDGE34: Exact Bridge33 embedding test and certification feasibility.

This deliberately does NOT substitute an arbitrary toy PRG for Forbes-Kelley/CHMY.
The image distinguisher is certified for every possible source f, so it also
applies symbolically, without instantiating, to G_CHMY(z) for every real seed z.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def embedding_bit(f, n, target_index):
    """E(f)(x,y)=f(x) xor (y0 and (x0 xor y1)), x major, y minor."""
    source_len = 1 << n
    assert len(f) == source_len
    assert 0 <= target_index < source_len * source_len
    x, y = divmod(target_index, source_len)
    x0 = (x >> (n - 1)) & 1
    y0 = (y >> (n - 1)) & 1
    y1 = (y >> (n - 2)) & 1
    return f[x] ^ (y0 & (x0 ^ y1))


def serial_embedding(f, n):
    """One forward pass over the given f, emits N^2 bits, holds x,y counters."""
    N = 1 << n
    source_reads, writes, bits = 0, 0, []
    for x in range(N):
        source_bit = f[x]
        source_reads += 1
        for y in range(N):
            x0 = (x >> (n-1)) & 1
            y0 = (y >> (n-1)) & 1
            y1 = (y >> (n-2)) & 1
            bits.append(source_bit ^ (y0 & (x0 ^ y1)))
            writes += 1
    assert source_reads == N and writes == N*N
    return bits, {'source_reads':source_reads,'target_writes':writes,
                  'counter_bits_upper':2*n+4,'random_bits':0,
                  'source_dependent_advice_bits':0}


def exact_e_image_audit(n=3):
    N = 1 << n
    M = N*N
    functions = 1 << N
    equalities = 0
    injective = set()
    first8 = set()
    for encoded in range(functions):
        f = tuple((encoded >> j) & 1 for j in range(N))
        out, costs = serial_embedding(f,n)
        assert len(out) == M
        assert all(out[k] == embedding_bit(f,n,k) for k in range(M))
        # y=0 recovers f, hence E injective
        recovered = tuple(out[x*N] for x in range(N))
        assert recovered == f
        injective.add(tuple(out))
        first8.add(tuple(out[:8]))
        # y0,y1 unchanged when y_last changes => adjacent pairs equal for n>=3
        for x in range(N):
            for pair in range(N//2):
                a = x*N + 2*pair
                assert out[a] == out[a+1], (encoded,x,pair)
                equalities += 1
        assert all(out[2*j] == out[2*j+1] for j in range(4))
        assert costs['source_reads'] == N
    assert len(injective) == functions
    all_prefixes = list(product((0,1),repeat=8))
    uniform_accepts = sum(all(p[2*j] == p[2*j+1] for j in range(4)) for p in all_prefixes)
    assert uniform_accepts == 16
    # These values apply for the REAL published CHMY generator G, for every z,
    # since the check is universal over all possible N-bit output strings f.
    return {
        'source_truth_table_bits_N':N, 'target_truth_table_bits_M':M,
        'all_source_functions_enumerated':functions,
        'all_target_image_bit_checks':functions*M,
        'all_adjacent_pair_equalities':equalities,
        'image_injective_size':len(injective),
        'first8_distinct_image_prefixes':len(first8),
        'published_CHMY_G_composition':
          'symbolically universally certified for G(z) for each z; no PRG numerical instantiation',
        'one_tape_distinguisher':{
            'strategy':'read first 8 bits; accept iff each of four adjacent pairs equals',
            'input_moves':8,'work_tapes_used':0,'randomness_bits':0,
            'oracle_queries':0,'generator_seed_seen':False,
            'accept_probability_on_E_of_any_G_output':1,
            'accept_probability_on_uniform_target':f'{uniform_accepts}/{len(all_prefixes)}',
            'distinguishing_advantage':f'{len(all_prefixes)-uniform_accepts}/{len(all_prefixes)}'
        },
        'exact_total_variation_E_of_U_N_vs_U_M':f'1 - 2^(-{M-N})',
        'embedding_serial_cost_example': costs
    }



def public_mask_fiber_cancellation_audit(n=3):
    """Tests the entire public-xor-fiber family; no synthetic CHMY PRG used."""
    N=1<<n
    masks={
        'zero':lambda x,y:0,
        'parity_y':lambda x,y:y.bit_count()%2,
        'nonlinear_y':lambda x,y:(((y>>(n-1))&1)^((y>>(n-2))&1))& (y&1),
        'bridge33_original':lambda x,y:((y>>(n-1))&1)&(((x>>(n-1))&1)^((y>>(n-2))&1)),
    }
    out={}
    for name, h in masks.items():
        expected=tuple(h(0,2*j)^h(0,2*j+1) for j in range(N//2))
        passes=0
        tested=0
        for encoded in range(1<<N):
            f0=encoded&1
            firstblock=tuple(f0^h(0,y) for y in range(N))
            parity=tuple(firstblock[2*j]^firstblock[2*j+1] for j in range(N//2))
            assert parity==expected
            passes+=1
            tested+=N//2
        out[name]={
            'tested_source_functions':1<<N,
            'checked_pairs':tested,
            'image_tester_acceptance':'1',
            'uniform_tester_acceptance':f'1/{1<<(N//2)}',
            'distinguishing_advantage':f'{(1<<(N//2))-1}/{1<<(N//2)}',
            'expected_public_parities':list(expected)
        }
    return out



def public_reindexing_cancellation_audit(n=3):
    """Explicit two-query distinguisher for ANY public one-bit-source reindexing.

    For pi:[M]->[N], h:[M]->{0,1}, E(f)[i]=f[pi(i)] xor h(i).
    Among first N+1 outputs there is repeated pi value.  A finite-state
    one-way tester stores E[i], then checks E[i] xor E[j] == h[i] xor h[j].
    This is symbolic for any CHMY generator output, not a surrogate PRG.
    """
    N=1<<n
    M=N*N
    maps={
      'source_first_then_repeat':lambda i:i%N,
      'full_period_permuted':lambda i:(5*i+3)%N,
      'block_x_major':lambda i:i//N,
      'xor_scramble':lambda i:(i ^ (i>>3))%N,
    }
    masks={
      'alternating':lambda i:i%2,
      'nonlinear_public':lambda i: ((i>>1)&1)&((i>>2)&1),
    }
    output=[]
    for mapname, pi in maps.items():
      indexes={}
      duplicate=None
      for j in range(N+1):
        v=pi(j)
        assert 0<=v<N
        if v in indexes:
          duplicate=(indexes[v],j)
          break
        indexes[v]=j
      assert duplicate is not None
      i,j=duplicate
      assert j<=N
      for maskname,h in masks.items():
        expected=h(i)^h(j)
        for z in range(1<<N):
          fi=(z>>pi(i))&1
          fj=(z>>pi(j))&1
          assert (fi^h(i))^(fj^h(j))==expected
        # Under a uniform output, values at the two distinct indices independent.
        assert sum((a^b)==expected for a,b in product((0,1),repeat=2))==2
        output.append({'source_index_map':mapname,'mask':maskname,
            'witness_output_indices':[i,j],
            'input_positions_scanned_by_finite_state_test':j+1,
            'states_upper_bound':4*(j+3),
            'source_functions_verified':1<<N,
            'accepts_all_image_strings':True,
            'uniform_acceptance':'1/2',
            'distinguishing_advantage':'1/2',
            'work_tapes':0,'random_bits':0,'oracle_queries':0})
    return output


def fractional_parameter_audit(den=40):
    """Audits inequalities for CHMY-published seed certificate and full-stream E_r.

    nu<theta: seed locality sigma ~= N^nu fits source YES N^theta/log N.
    beta_prime=theta/r<1/2: target exponent falls below sqrt barrier.
    r<2nu: generating at least M=N^r bits fits under N^(2nu).
    """
    checks = 0
    admissible_above_half=0
    target_below_half_possible=0
    examples = []
    for nu_numer in range(den//2+1, den):
        nu = Fraction(nu_numer,den)
        for theta_numer in range(nu_numer+1, den):
            theta = Fraction(theta_numer,den)
            for r_numer in range(den+1, 2*den+1):
                r = Fraction(r_numer,den)
                checks += 1
                if r < 2*nu:
                    admissible_above_half+=1
                    beta_prime = theta/r
                    if beta_prime < Fraction(1,2):
                        target_below_half_possible+=1
                        examples.append([str(nu),str(theta),str(r),str(beta_prime)])
    assert target_below_half_possible == 0
    # Construct a nontrivial positive-margin example above 1/2,
    # to verify that the inequality solver is not vacuous.
    nu, theta, r = Fraction(17,20), Fraction(9,10), Fraction(8,5)
    beta_prime = theta/r
    assert nu<theta and 1<r<2*nu and beta_prime>Fraction(1,2)
    source_margin = 2*nu-1
    transferred_margin = 2*nu/r-1
    lam = Fraction(1,1)/r
    rho = transferred_margin/source_margin
    assert transferred_margin>0 and rho<lam
    return {'rational_grid_denominator':den,
            'tested_nu_theta_r_triples':checks,
            'within_source_hardness_time_window':admissible_above_half,
            'below_half_and_within_time_window':target_below_half_possible,
            'counterexamples_to_inequality':examples,
            'analytic_reason':'beta_prime<1/2 => r>2theta>2nu, contradicts r<2nu',
            'nonvacuous_above_half_example':{
                'nu':str(nu),'theta':str(theta),'r':str(r),
                'beta_prime':str(beta_prime),'source_g':str(source_margin),
                'transferred_g':str(transferred_margin),
                'lambda':str(lam),'rho':str(rho),
                'rho_less_than_lambda':rho<lam},
            'oracle_length_warning': 'Any positive query-length exponent delta increases the CHMY seed certificate exponent and only worsens feasibility'}


def explicit_gate_extension_audit():
    """Construct nine-gate extension of a chosen f with AND/OR/NOT fan-in <=2."""
    n=3
    # f(x)=x0 xor x1 using four AND/OR/NOT gates
    gates=[]
    def add(op, *args):
        gates.append((op,args)); return ('g',len(gates)-1)
    x0=('in',0);x1=('in',1); y0=('in',n);y1=('in',n+1)
    def gx(a,b):
        z_or=add('OR',a,b)
        z_and=add('AND',a,b)
        z_not=add('NOT',z_and)
        return add('AND',z_or,z_not)
    f_out=gx(x0,x1)
    base_gates=len(gates)
    inner=gx(x0,y1)
    h=add('AND',y0,inner)
    whole=gx(f_out,h)
    assert len(gates)-base_gates==9
    def eval_circ(inp):
        vals=[]
        def get(node):
            typ,i=node
            return inp[i] if typ=='in' else vals[i]
        for op,args in gates:
            av=[get(a) for a in args]
            vals.append((av[0]&av[1]) if op=='AND' else
                        (av[0]|av[1]) if op=='OR' else 1-av[0])
        return get(whole)
    source_f = tuple(((x>>(n-1))&1) ^ ((x>>(n-2))&1) for x in range(1<<n))
    for x in range(1<<n):
        for y in range(1<<n):
            inp=tuple((x>>i)&1 for i in range(n-1,-1,-1))+tuple((y>>i)&1 for i in range(n-1,-1,-1))
            assert eval_circ(inp)==embedding_bit(source_f,n,x*(1<<n)+y)
    return {'base_function':'x0 XOR x1','base_gates':base_gates,
            'extension_gates':len(gates)-base_gates,
            'total_gates':len(gates),
            'truth_table_entries_verified':(1<<n)**2,
            'gate_basis':'fan-in-2 AND/OR, fan-in-1 NOT',
            'restriction_y_zero_recovers_f':True}


def naive_single_tape_splice_counterexample():
    """Charge work-tape head motion in the naive parked-counter fusion."""
    # Native target sits at work cell L and reads one input symbol each step.
    # Naive source simulation returns to cell 0 for generator counter on each read.
    # This explicitly falsifies only that fusion layout, not every one-tape simulator.
    data=[]
    for M,L in [(64,8),(256,16),(1024,32)]:
        original_steps=L+M
        simulated_steps_at_least=L+2*M*L + M
        assert simulated_steps_at_least/original_steps>M//(2*(L+1))
        data.append({'M':M,'workhead_distance_L':L,
                     'native_one_tape_steps':original_steps,
                     'parked_counter_simulation_steps_lower':simulated_steps_at_least,
                     'slowdown':round(simulated_steps_at_least/original_steps,4)})
    return {'status':'FAIL for parked-counter two-region fusion ONLY', 'cases':data,
            'important_limitation':'No universal lower bound against all optimized one-tape encodings'}


def main():
    results={'status':'candidate direct CHMY-PRG lift FAIL / original CHMY true / full hardness transfer OPEN',
             'exact_embedding_audit':exact_e_image_audit(3),
             'rational_feasibility':fractional_parameter_audit(40),
             'mask_invariant_fiber_cancellation':public_mask_fiber_cancellation_audit(3),
             'reindexing_invariant_cancellation':public_reindexing_cancellation_audit(3),
             'nine_gate_extension':explicit_gate_extension_audit(),
             'one_tape_splice_falsifier':naive_single_tape_splice_counterexample()}
    path=HERE/'BRIDGE34_raw.json'
    path.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({
        'image_size':results['exact_embedding_audit']['image_injective_size'],
        'adjacent_constraints_tested':results['exact_embedding_audit']['all_adjacent_pair_equalities'],
        'CHMY_real_generator_status':'symbolic for every output of original G, not numerically instantiated',
        'distinguisher_advantage':results['exact_embedding_audit']['one_tape_distinguisher']['distinguishing_advantage'],
        'feasible_below_half':results['rational_feasibility']['below_half_and_within_time_window'],
        'triples_checked':results['rational_feasibility']['tested_nu_theta_r_triples'],
        'gate_cost':results['nine_gate_extension']['extension_gates'],
        'output':str(path)
    },indent=2))

if __name__=='__main__':
    main()