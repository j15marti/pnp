# Verifies the Step-1 construction: CSAT_{1,n} (single AND of two literals), n=2^k.
# Instance bits: index1 (k), sign1, index2 (k), sign2. SAT iff NOT(index1==index2 and sign1!=sign2).
import itertools, json
def f(k, bits):
    i1=bits[:k]; s1=bits[k]; i2=bits[k+1:2*k+1]; s2=bits[2*k+1]
    return int(not (i1==i2 and s1!=s2))
def brute_sat(k, bits):  # semantic definition: exists x with lit1 & lit2
    n=2**k
    toint=lambda b:int("".join(map(str,b)),2) if b else 0
    a,sa=toint(bits[:k]),bits[k]; b,sb=toint(bits[k+1:2*k+1]),bits[2*k+1]
    for x in itertools.product([0,1],repeat=n):
        if (x[a]^(1-sa)) and (x[b]^(1-sb)): return 1   # sign 1 = positive literal
    return 0
def circuit(k, bits):  # 2k+1 fan-in-2 gates
    i1=bits[:k]; s1=bits[k]; i2=bits[k+1:2*k+1]; s2=bits[2*k+1]
    g=0
    d=[a^b for a,b in zip(i1,i2)]; g+=k
    acc=d[0]
    for t in d[1:]: acc=acc|t; g+=1
    sx=s1^s2; g+=1
    out=acc|(1-sx); g+=1   # OR with negated input (negation absorbed into gate type)
    return out,g
res={}
for k in (1,2,3):
    ok=True; gates=None
    for bits in itertools.product([0,1],repeat=2*k+2):
        bits=list(bits)
        o,g=circuit(k,bits); gates=g
        if not (o==f(k,bits)==brute_sat(k,bits)): ok=False
    res[k]={"n":2**k,"inputs":2*k+2,"gates":gates,"lower_bound_gates":2*k+1,"wires":2*gates,"verified":ok}
print(json.dumps(res,indent=1)); json.dump(res,open("results/claude_circuitsat/step1_check.json","w"),indent=1)
