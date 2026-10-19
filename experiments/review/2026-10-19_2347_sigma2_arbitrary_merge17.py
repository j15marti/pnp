#!/usr/bin/env python3
"""SIGMA2-ARBITRARY-MERGE17: exact finite circuit-streaming tests.

Tests bounded-fan-in AND/OR/NOT circuits.  The paper's oracle-A extension
is proved symbolically, not tested by this finite computation.
"""
import itertools
import json
import math
import random
from pathlib import Path

OPS=("AND", "OR", "NOT")
SEED=202610192336


def descriptions(n,s):
    yield (),0
    for out in range(1,n):
        yield (),out
    prefixes=[()]
    for g in range(1,s+1):
        nxt=[]
        for prefix in prefixes:
            for op in OPS:
                arity=1 if op=="NOT" else 2
                for inputs in itertools.product(range(n+g-1), repeat=arity):
                    desc=prefix+((op,inputs),)
                    nxt.append(desc)
                    for out in range(n+g):
                        yield desc,out
        prefixes=nxt


def table(n,desc,out):
    N=1<<n
    values=[]
    for i in range(n):
        values.append(sum((((j>>i)&1)<<j) for j in range(N)))
    mask=(1<<N)-1
    for op,inputs in desc:
        if op=="NOT":
            z=mask^values[inputs[0]]
        elif op=="AND":
            z=values[inputs[0]]&values[inputs[1]]
        else:
            z=values[inputs[0]]|values[inputs[1]]
        values.append(z)
    return values[out]


def encode(n,s,desc,out):
    width=max(1,math.ceil(math.log2(n+s)))
    b=''
    for j in range(s):
        if j>=len(desc):
            b+='00'+'0'*(2*width)
            continue
        op,inputs=desc[j]
        b+={"AND":"01","OR":"10","NOT":"11"}[op]
        b+=format(inputs[0],f'0{width}b')
        b+=format(inputs[1] if len(inputs)==2 else 0,f'0{width}b')
    b+=format(out,f'0{width}b')
    return b


def case(n,s,all_sources=False,seeded=30):
    rng=random.Random(SEED+n*100+s)
    items=[]
    for desc,out in descriptions(n,s):
        items.append((encode(n,s,desc,out),table(n,desc,out),len(desc)))
    items.sort()
    assert len({x[0] for x in items})==len(items)
    tables={x[1] for x in items}
    L=len(items[0][0]); N=1<<n
    assert all(len(x[0])==L for x in items)
    assert L==s*(2+2*max(1,math.ceil(math.log2(n+s))))+max(1,math.ceil(math.log2(n+s)))
    sources=list(range(1<<N)) if all_sources else rng.sample(range(1<<N),seeded)
    count={"source_cases":0,"prefix_steps":0,"feasibility_queries":0,"oracle_bit_queries":0,"candidate_constraints_checked":0,"witnesses_greater_than_min_gates":0,"nonminimal_repairs":0,"false_rejects":0,"false_accepts":0,"failures":0}
    example=None
    for source in sources:
        prev_min=items[0];prev_max=items[-1]
        failed_min=False;failed_max=False
        for t in range(N):
            count["prefix_steps"]+=1
            mask=(1<<t)-1
            nextbit=(source>>t)&1
            # P(v) = exists D (D agrees on every earlier bit with C,
            #                     and D(t) equals the next observed bit).
            def feasible(prev):
                out=[]
                for w in items:
                    count["candidate_constraints_checked"]+=1
                    if ((w[1]^prev[1]) & mask)==0 and ((w[1]>>t)&1)==nextbit:
                        out.append(w)
                count["feasibility_queries"]+=1
                return out
            if not failed_min:
                pool=feasible(prev_min)
                # Self-reduction by one bit of a genuine padded circuit encoding.
                if not pool:
                    failed_min=True
                else:
                    pfx=''
                    for i in range(L):
                        count["oracle_bit_queries"]+=1
                        count["candidate_constraints_checked"]+=len(pool)
                        zero=[w for w in pool if w[0][i]=='0']
                        if zero:
                            pool=zero; pfx+='0'
                        else:
                            pool=[w for w in pool if w[0][i]=='1'];pfx+='1'
                    assert len(pool)==1 and pool[0][0]==pfx
                    prev_min=pool[0]
                    if prev_min[2] > min(z[2] for z in items if ((z[1]^source)&((1<<(t+1))-1))==0):
                        count["witnesses_greater_than_min_gates"]+=1
            if not failed_max:
                pool=feasible(prev_max)
                if not pool:
                    failed_max=True
                else:
                    prev_max=pool[-1]
                    count["nonminimal_repairs"]+=int(prev_max[2]>min(z[2] for z in pool))
            expected_any=any(((w[1]^source) & ((1<<(t+1))-1))==0 for w in items)
            assert (not failed_min)==expected_any, (n,s,source,t,"min")
            assert (not failed_max)==expected_any, (n,s,source,t,"max")
        wanted=source in tables
        observed_min=not failed_min
        observed_max=not failed_max
        count["false_rejects"]+=int(wanted and not observed_min)
        count["false_accepts"]+=int(observed_min and not wanted)
        assert observed_min==wanted==observed_max
        if wanted:
            assert prev_min[1]==source and prev_max[1]==source
            if prev_max[2]>prev_min[2] and example is None:
                example={"source":source,"min_size":prev_min[2],"arbitrary_larger_size":prev_max[2]}
        count["source_cases"]+=1
    return {"n":n,"s":s,"N":N,"descriptor_bits":L,"circuits":len(items),"distinct_semantic_YES_words":len(tables),"counters":count,"different_cost_example":example}


def sampled_prefix_falsifier():
    n=3
    C=((('NOT',(0,)),),3)
    D=((('NOT',(1,)),),3)
    c=table(n,*C); d=table(n,*D)
    cfirst=[(c>>t)&1 for t in range(3)]
    dfirst=[(d>>t)&1 for t in range(3)]
    catalogue=[x for x in descriptions(n,1) if [((table(n,*x)>>t)&1) for t in range(3)]==[1,0,0]]
    assert cfirst==[1,0,1] and dfirst==[1,1,0]
    assert not catalogue
    return {"n":3,"s":1,"observed_prefix":[1,0,0],"previous_C_prefix":cfirst,"candidate_D_prefix":dfirst,"sampled_address_zero_matches":True,"new_bit_at_index_two_matches":True,"full_prefix_condition":False,"valid_size_one_circuit_for_true_prefix":False}


def main():
    cases=[case(2,1,True),case(3,2,True),case(4,2,False,32)]
    raw={"run":"SIGMA2_ARBITRARY_MERGE17","seed":SEED,"status":"PASS","model":"finite AND2/OR2/NOT1 circuit encodings with literal bitwise descriptor self-reduction","cases":cases,"sampled_prefix_attack":sampled_prefix_falsifier(),"quantifier_formula":"exists padded encoding d forall x<n-bit: (x<i => D(x)=C(x)) and block constraints","oracle_upper":"Sigma_2^{P,A} under MMW canonical O(s log s) witness encoding","actual_A_oracle_executed":False,"uniform_oracle_time_lower_bound_proven":False,"CHMY_descent_proven":False,"ARC_contractor_proven":False,"p_vs_np":"OPEN","unexpected_failures":sum(c['counters']['failures'] for c in cases)}
    out=Path(__file__).with_name('SIGMA2_ARBITRARY_MERGE17_raw.json')
    out.write_text(json.dumps(raw,indent=2)+"\n")
    print(json.dumps({"raw":str(out),"cases":[{k:v for k,v in c.items() if k!='counters'} for c in cases],"overall_counters":{k:sum(c['counters'][k] for c in cases) for k in cases[0]['counters']},"sampled_prefix_falsifier":raw['sampled_prefix_attack'],"unexpected_failures":raw['unexpected_failures']},indent=2))

if __name__=='__main__': main()
