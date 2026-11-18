#!/usr/bin/env python3
"""Compact independent CLOCKZEROGAUGE34 check. CPython, standard library."""
import itertools, random, json
rng = random.Random(202611180330)
passed=0

def evaluate(bits,z,o):
    s=0
    for i,b in enumerate(bits):s=(o[i] if b else z[i])[s]
    return s

def min_distance_to_baseline(N,K,h,z,o):
    # Dynamic programming over ALL source words, independently of loop erasure.
    dp={0:0}
    for i in range(N):
        nxt={}
        for state,cost in dp.items():
            for bit in (0,1):
                t=(o[i] if bit else z[i])[state]
                d=cost+(bit!=h[i])
                nxt[t]=min(d,nxt.get(t,10**9))
        dp=nxt
    return dp

for N in (4,8):
    for K in (2,3,4):
        for e in range(3):
            for _ in range(24):
                h=[rng.randrange(2) for _ in range(N)]
                ex=set(rng.sample(range(N),e))
                z=[];o=[]
                for i in range(N):
                    B=([0]*K if i in ex else rng.sample(range(K),K))
                    D=[rng.randrange(K) for _ in range(K)]
                    z.append(B if h[i]==0 else D)
                    o.append(B if h[i]==1 else D)
                dp=min_distance_to_baseline(N,K,h,z,o)
                for bits in itertools.product((0,1),repeat=N):
                    q=evaluate(bits,z,o)
                    assert dp[q]<=(e+1)*(K-1)+e
                    passed+=1
# e=0, K-1 is sharp, and a noninvertible zero map can demand >K-1 ones.
K=4;N=8;z=[list(range(K)) for _ in range(N)]
o=[[min(K-1,x+1) for x in range(K)] for _ in range(N)]
assert min_distance_to_baseline(N,K,[0]*N,z,o)[K-1]==K-1
K=2;z=[[1,1] for _ in range(N)];o=[[0,1] for _ in range(N)]
assert min_distance_to_baseline(N,K,[0]*N,z,o)[0]==N
print(json.dumps({'name':'CLOCKZEROGAUGE34 compact', 'source_checks':passed,
                  'model_count':2*3*3*24, 'failures':0},sort_keys=True))
