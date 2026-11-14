#!/usr/bin/env python3
"""Finite exact fan-in-two AND/OR/NOT circuit minima with free constant wires.
No experimental count is offered as an asymptotic lower bound.
"""
from __future__ import annotations
import json, math
from itertools import combinations_with_replacement
from pathlib import Path

OUT = Path(__file__).with_name('tmr1_mcsp_padding024_raw.json')

def input_wires(n):
    mask=(1 << (1<<n))-1
    xs=[]
    for j in range(n):
        bits=0
        for a in range(1<<n):
            if (a >> (n-1-j)) & 1: bits |= (1<<a)
        xs.append(bits)
    return [0,mask]+xs

def all_circuits(n,max_gates):
    base=input_wires(n)
    mask=base[1]
    attained={v:0 for v in base}
    iterations=[0]*(max_gates+1)
    terminal_new=[0]*(max_gates+1)
    def rec(wires,depth):
        if depth==max_gates:return
        choices = set()
        for i,a in enumerate(wires):
            choices.add(mask ^ a)
            for b in wires[i:]:
                choices.add(a & b)
                choices.add(a | b)
        for v in sorted(choices):
            iterations[depth+1]+=1
            if v not in attained:
                attained[v]=depth+1
                terminal_new[depth+1]+=1
            rec(wires+[v],depth+1)
    # Important: at most 3-gate exhaustive enumeration for n <= 3, no pruning by equivalent gates
    rec(base,0)
    return attained, iterations, terminal_new

def padded_tt(tt,n,t):
    out=0
    for i in range(1<<n):
        if (tt>>i)&1:
            out|=((1<<(1<<t))-1) << (i<<t)
    return out

def verify_case(n,t,budget):
    a,it_a,new_a=all_circuits(n,budget)
    b,it_b,new_b=all_circuits(n+t,budget)
    found=0;fail=[]
    for tt in range(1<<(1<<n)):
        lo=a.get(tt, budget+1)
        hi=b.get(padded_tt(tt,n,t),budget+1)
        if lo<=budget or hi<=budget:
            found+=1
        if lo!=hi:fail.append({'tt':tt,'cc_n':lo,'cc_padded':hi})
    assert not fail, fail[:2]
    return {'arity':n,'dummy_variables':t,'gate_budget':budget,'all_truth_tables_tested':1<<(1<<n),
        'truth_tables_covered_by_budget':found,'source_circuit_enumerations':it_a,
        'padded_circuit_enumerations':it_b,'source_new':new_a,'padded_new':new_b,'failed_comparisons':len(fail)}

def test_reduction(mu_h_num,mu_h_den,mu_l_num,mu_l_den,ns):
    ratio_num=mu_h_num*mu_l_den
    ratio_den=mu_h_den*mu_l_num
    out=[]
    for n in ns:
        if (n*ratio_num)%ratio_den: continue
        m=n*ratio_num//ratio_den
        s_h=(1<<(mu_h_num*n//mu_h_den)) if (mu_h_num*n)%mu_h_den==0 else 2**(mu_h_num*n/mu_h_den)
        s_l=(1<<(mu_l_num*m//mu_l_den)) if (mu_l_num*m)%mu_l_den==0 else 2**(mu_l_num*m/mu_l_den)
        assert s_h==s_l
        out.append({'n':n,'padded_arity':m,'source_tt_bits':1<<n,'target_tt_bits':1<<m,
         'circuit_threshold':str(s_h),'output_length_exponent':m/n,
         'optimistic_solver_exponent':1.01*m/n,
         'materialization_already_N_1_99_or_worse':m/n>=1.99,
         'generic_solver_upper_bound_below_N_1_99':1.01*m/n<1.99})
    return out

def main():
    cases=[verify_case(1,1,3), verify_case(2,1,3), verify_case(3,1,2)]
    samples={
      'mu_3over4_to_1over4':test_reduction(3,4,1,4,[4,8,12,16]),
      'mu_4over5_to_2over5':test_reduction(4,5,2,5,[5,10,15]),
      'mu_3over4_to_1over2':test_reduction(3,4,1,2,[4,8,12,16]),
    }
    r={'status':'COMPUTATIONAL','basis':'AND OR NOT fanin2 with uncharged 0/1 input constants, wires, variable nodes; gates charged',
       'cases':cases,'exponents':samples,'exact_conclusion':'Full equality of CC under ignored-variable extension is symbolic, not inferred from finite cases.',
       'failed_assertions':0}
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'cases':cases,'ratios':{k:[(x['output_length_exponent'],x['optimistic_solver_exponent']) for x in v[:1]] for k,v in samples.items()},'failed_assertions':0},indent=2))
if __name__=='__main__':main()
