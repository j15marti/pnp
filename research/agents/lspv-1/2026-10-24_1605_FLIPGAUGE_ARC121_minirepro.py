#!/usr/bin/env python3
"""FLIPGAUGE-ARC121: deterministic parity and full-configuration activity audit.
Abstract bit-event model, NOT a machine-exact FLMV timing simulation.
No third-party dependencies.
"""
from itertools import product

def bits(x): return x.bit_count()

def audit(seq):
    n=len(seq); width=max(1,n.bit_length())
    pos=0; acc=0; flips=0; binary=0; gray=0; work=0
    seen={(pos,acc,0)}
    for v in seq:
        assert v in (0,1)
        before=(pos,acc,0)
        prev=pos
        acc^=v
        pos+=1
        df=bits(prev^pos)
        binary+=df
        gray+=bits((prev^(prev>>1))^(pos^(pos>>1)))
        flips+=df+v
        work+=4+2*df+1
        after=(pos,acc,0)
        assert after!=before and after not in seen
        seen.add(after)
    assert acc==sum(seq)%2
    assert gray==n
    flips+=1
    work+=1
    assert n+1<=flips<=(n+1)*(width+2)
    return {"n":n,"parity":acc,"source_reads":n,"accumulator_writes":n,
            "accumulator_flips":sum(seq),"binary_address_flips":binary,
            "gray_address_flips":gray,"complete_configuration_flips":flips,
            "abstract_bit_work":work,"peak_live_bits":width+1,
            "cumulative_bit_time":(n+2)*(width+1)}
def exact_sat(cnf,n):
    return any(all(any(bool(a[abs(l)-1])==(l>0) for l in cl) for cl in cnf)
               for a in product((0,1),repeat=n))
def main():
    count=0
    for n in range(1,11):
        for seq in product((0,1),repeat=n):
            out=audit(seq); count+=1
            assert out["source_reads"]==n
            if not any(seq): assert out["accumulator_flips"]==0
    controls={"horn_sat":exact_sat([(1,),(-1,2)],2),
              "horn_unsat":exact_sat([(1,),(-1,)],1),
              "2sat_sat":exact_sat([(1,2),(-1,2)],2),
              "2sat_unsat":exact_sat([(1,),(-1,)],1),
              "padded_2sat_sat":exact_sat([(1,2,3),(1,2,-3)],3)}
    assert controls=={"horn_sat":True,"horn_unsat":False,
                     "2sat_sat":True,"2sat_unsat":False,
                     "padded_2sat_sat":True}
    assert count==2046
    print({"checks":count,"controls":controls,"failures":0,
           "zero_n10":audit((0,)*10),"ones_n10":audit((1,)*10)})
if __name__=="__main__":main()
