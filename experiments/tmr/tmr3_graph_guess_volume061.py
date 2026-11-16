#!/usr/bin/env python3
"""TMR-3/061: finite, exact source-to-output audit of a fixed Williams-style
movement-word enumeration. Scope: fixed lexicographic guess-and-FAIL
architecture, NOT a Cook-Mertz implementation or a generic time lower bound.
Python standard library only.
"""
from __future__ import annotations
from itertools import product
import json, hashlib, random, sys
from pathlib import Path

REV = "tmr3-graph-guess-volume061-v1"
SEED = 202611152119
rng = random.Random(SEED)
checks = 0

def check(c: bool, why: str):
    global checks
    checks += 1
    if not c:
        raise AssertionError(f"{why} at assertion {checks}")

def authentic_run(word: str, b: int):
    """Two locally moving heads: readonly source and blank work head.
    Each input bit advances both heads one cell; EOF halts without moving.
    A single control bit retains AND of all input symbols.
    Here time t = len(word)+1; require t divisible by b.
    """
    assert word and set(word)<=set('01') and b>=1
    t=len(word)+1
    assert t % b==0
    src=work=0
    accept=1
    moves=[]
    crossings=[]
    for i in range(1,t+1):
        if i<t:
            accept &= (word[i-1]=='1')
            a,beforework = src,work
            src+=1;work+=1
            for h,(old,new) in enumerate(((a,src),(beforework,work))):
                if new//b!=old//b:
                    check(i%b==0, 'only_boundary_cross')
                    crossings.append((i,h,old//b,new//b))
        if i%b==0:
            # Check end-of-time-block movement compared to start.
            # At final EOF transition both heads remain at their last cell.
            prev_idx = (i-b)//b
            mov = ((src//b)-prev_idx, (work//b)-prev_idx)
            # At the final time block, crossing at its BEGINNING already counted
            # from the preceding boundary. At this EOF step, we remain in block B.
            if i==t: mov=(0,0)
            check(mov in ((0,0),(1,1)), 'legal_movement_pair')
            moves.extend(mov)
    B=t//b
    expected=(1,1)*(B-1)+(0,0)
    check(tuple(moves)==expected, 'exact_authentic_movement')
    check(len(crossings)==2*(B-1), 'crossing_count')
    check(accept==int(all(c=='1' for c in word)), 'both_label_output')
    return {'B':B,'b':b,'t':t,'accept':int(accept),'movement':tuple(moves),'crossings':len(crossings)}

def rank_ternary(moves):
    v=0
    for m in moves:
        v=v*3+({-1:0,0:1,1:2}[m])
    return v

def checked_guess(g, genuine, output):
    # Abstract root semantics: FAIL unless every physical block movement
    # matches. This represents the Williams R_G guarantee, not the actual
    # Cook-Mertz evaluator or charged physical implementation of R_G.
    return output if g==genuine else 'FAIL'

records=[]
exhaustive=0
for B in range(1,6):
    for b in (2,3,5):
        N=b*B-1
        for kind in ('all_ones','first_zero','last_zero'):
            word = '1'*N if kind=='all_ones' else '0'+'1'*(N-1) if kind=='first_zero' else '1'*(N-1)+'0'
            result=authentic_run(word,b)
            target=result['movement']
            expected=3**(2*B)-4
            check(rank_ternary(target)+1==expected,'analytic_rank')
            found=False;calls=0
            for guessed in product((-1,0,1),repeat=2*B):
                calls+=1
                response=checked_guess(guessed,target,result['accept'])
                if response!='FAIL':
                    check(guessed==target,'root_soundness')
                    check(response==result['accept'],'root_correct_output')
                    found=True
                    break
            check(found and calls==expected,'exact_call_count')
            exhaustive+=1
            records.append(dict(B=B,b=b,kind=kind,calls=calls,output=result['accept'],crossings=result['crossings']))

# Two asymptotic parameter families, no infeasible enumeration.
family=[]
for m in (16,20,24,32,48,64):
    b=m; B=m*m; t=b*B
    check(b>=t.bit_length()-1 if (t & (t-1))==0 else b>=t.bit_length(), 'legal_cuberoot_width')
    q=3**(2*B)-4
    family.append({'mode':'cube_root','b':b,'B':B,'t':t,'calls_digits':len(str(q)), 'calls_bits':q.bit_length(), 'log2_over_t_pow_2_3':(q.bit_length()-1)/(m*m)})
for b in range(4,16):
    B=(2**(b-1)//b)+1
    t=b*B
    check((t-1).bit_length()==b,'exact_log_width')
    family.append({'mode':'minimum_log','b':b,'B':B,'t':t,'calls_bits':(3**(2*B)-4).bit_length()})

# Large varied TRUE and FALSE sources, checking physical head boundaries.
random_cases=0
for B,b in product(range(1,13),range(2,12)):
    N=b*B-1
    for _ in range(3):
        word=''.join(str(rng.randrange(2)) for _ in range(N))
        z=authentic_run(word,b)
        check(rank_ternary(z['movement'])+1==3**(2*B)-4,'random_rank')
        random_cases+=1

result={
    'revision':REV,'seed':SEED,'status':'COMPUTATIONAL','source_machine':'two heads move right on each data bit; at EOF halt with AND(data) and stay; blank work tape',
    'guess_order':'time-major two tapes, each movement alphabet (-1,0,+1), lexicographic',
    'exact_formula':'candidate_calls = 3^(2B)-4 for m=(+1,+1)^(B-1),(0,0)',
    'exhaustive_instances':exhaustive,'random_sources':random_cases,
    'assertions':checks,'failures':0,'sample_exhaustive':records[:8],
    'large_analytic_families':family,
    'limitations':['Graph candidate root semantics are modelled by sound equality/FAIL, not by executing Cook-Mertz Tree Evaluation.',
                   'Exponential conclusion is restricted to a specified lexicographic exhaustive scheme.',
                   'The source-aware direct solver makes the output easy; this is not an intrinsic lower bound.',
                   'Native locally headed TM microtransition compiler and HPV conversion were not executed.']}
if __name__=='__main__':
    output=Path(sys.argv[1]) if len(sys.argv)>1 else Path('tmr3_graph_guess_volume061_raw.json')
    output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['revision','assertions','exhaustive_instances','random_sources','failures']}))
