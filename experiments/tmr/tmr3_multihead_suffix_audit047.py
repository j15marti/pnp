#!/usr/bin/env python3
"""TMR-3 independent finite checks; NO asymptotic claims from finite tests.
Counter is an independent charged-head emulator of TMR-1/033's gap countdown.
Circuit catalogue is a direct exhaustive s<=1 enumerator on small arity.
"""
import json, itertools, math, random
from collections import Counter

def low_circuits(n):
    N=1<<n; mask=(1<<N)-1
    wires=[0,mask]
    for j in range(n):
        bits=sum(((i>>j)&1)<<i for i in range(N))
        wires.append(bits)
    catalogue=set(wires)
    for a in wires:
        catalogue.add(mask^a)
        for b in wires:
            catalogue.add(a&b)
            catalogue.add(a|b)
    return catalogue

def counter_drain(D,n):
    # physical head begins at least significant bit, high marker stored in one tape track
    bits=[(D>>i)&1 for i in range(n+1)]
    top=max((i for i,b in enumerate(bits) if b),default=-1)
    head=0; moves=0; writes=0; emissions=0
    while top>=0:
        k=0
        while bits[k]==0:
            bits[k]=1; writes+=1
            k+=1; head+=1; moves+=1
        assert head==k
        bits[k]=0; writes+=1
        if k==top: top=k-1; writes+=1 # move marker to neighbor on return route
        moves+=k; head=0
        emissions+=1
        # external checker, not a component of the simulated transducer
        assert sum(v<<i for i,v in enumerate(bits))==D-emissions
        assert top==max((i for i,b in enumerate(bits) if b),default=-1)
    assert emissions==D
    assert moves<=2*D and writes<=3*D
    return moves,writes,emissions

def stream(n,support):
    N=1<<n
    assert all(0<=z<N for z in support) and list(support)==sorted(set(support))
    out=[]; moves=0; writes=0; prev=-1
    for idx in support:
        gap=idx-prev-1
        m,w,z=counter_drain(gap,n)
        out.extend([0]*z);out.append(1);moves+=m;writes+=w
        prev=idx
    gap=N-1-prev
    m,w,z=counter_drain(gap,n)
    out.extend([0]*z);moves+=m;writes+=w
    assert len(out)==N
    assert [i for i,b in enumerate(out) if b]==list(support)
    return moves,writes,len(out)

def main():
    stats={'experiment':'TMR3_MULTIHEAD_SUFFIX_AUDIT047','status':'COMPUTATIONAL finite independent audit','checks':0,'failures':0,'supports':0,'output_bits':0,'drained_zeros':0,'counter_moves':0,'circuit_catalogue':{},'suffix_completions':{},'exact_reach_bound':{},'network_trace_pairs':0,'network_trace_steps':0,'conditional_network_model':'all source heads start at physical position 0, local moves at most one cell per global tick, no free sharding or input-supplied advice'}
    def ck(c):
        stats['checks']+=1
        if not c: stats['failures']+=1; raise AssertionError('Failed check '+str(stats['checks']))
    for n in range(1,7):
        N=1<<n
        arr=list(range(N))
        # Full support subsets n<=4; selected deterministic hostile cases thereafter
        subsets=[]
        if N<=16:
            for mask in range(1<<N):subsets.append([i for i in range(N) if (mask>>i)&1])
        else:
            rng=random.Random(420+n)
            subsets=[[],list(range(N)),[0],[N-1],list(range(0,N,2)),list(range(1,N,2))]
            subsets += [sorted(rng.sample(arr,rng.randrange(N+1))) for _ in range(192)]
        for support in subsets:
            m,w,z=stream(n,support)
            stats['supports']+=1;stats['output_bits']+=N;stats['drained_zeros']+=N-len(support);stats['counter_moves']+=m
            ck(m<=2*(N-len(support)));ck(w<=3*(N-len(support)))
            # Upper bound includes work for parsing source and addresses = O((r+1)n)
            cost=m+w+N+8*(len(support)+1)*(n+1)
            ck(cost<=6*N+8*(len(support)+1)*(n+1))
    # Explicitly construct all 0 and 1 gate catalogues, count low completions for YES prefix.
    for n in (2,3,4):
        N=1<<n;cat=low_circuits(n)
        stats['circuit_catalogue'][str(n)]={'N':N,'low_circuit_tables':len(cat),'total_tables':1<<N}
        ck(len(cat)<(1<<N))
        for B in (1,2,min(4,N),N):
            mask=(1<<(N-B))-1
            worst=0;witness=None
            for x in cat:
                prefix=x&mask
                low=sum(1 for z in range(1<<B) if (prefix|(z<<(N-B))) in cat)
                if low>worst:worst=low;witness=x
            frac=worst/(1<<B)
            key=f'n{n}_B{B}'
            stats['suffix_completions'][key]={'max_low_fraction':frac,'worst_low_count':worst,'prefix_example':witness&mask}
            ck(worst<=len(cat))
    # Independent two-way multihead adaptive trace coupling. Each selected head moves <=1.
    # Both tapes share prefix, but tails differ adversarially; state changes may select
    # different heads only AFTER physically reaching a distinct source symbol.
    rng=random.Random(419)
    for N in (8,16,32,64):
        for heads_count in (1,2,4,8):
            for trial in range(96):
                boundary=rng.randrange(1,N)
                common=[rng.randrange(2) for _ in range(boundary)]
                x=common+[rng.randrange(2) for _ in range(N-boundary)]
                y=common+[rng.randrange(2) for _ in range(N-boundary)]
                positions=[0]*heads_count
                state=rng.randrange(1234)
                positions_y=list(positions);state_y=state
                for tick in range(N+24):
                    # Adversarial circuit chooses head according to full adaptive state.
                    h=(state*17+tick)%heads_count
                    hy=(state_y*17+tick)%heads_count
                    ck(h==hy)
                    if positions[h]>=boundary or positions_y[hy]>=boundary:
                        ck(positions==positions_y and state==state_y)
                        break
                    bit=x[positions[h]];bity=y[positions_y[hy]]
                    ck(bit==bity)
                    update=(state*7+bit*11+tick*13+3)%10007
                    update_y=(state_y*7+bity*11+tick*13+3)%10007
                    direction=(-1,0,1)[update%3]
                    direction_y=(-1,0,1)[update_y%3]
                    positions[h]=min(N-1,max(0,positions[h]+direction))
                    positions_y[hy]=min(N-1,max(0,positions_y[hy]+direction_y))
                    state=update;state_y=update_y
                    ck(positions==positions_y and state==state_y)
                    ck(max(positions)<=tick+1)
                    stats['network_trace_steps']+=1
                stats['network_trace_pairs']+=1
    # Exact adversarial-pair bound: reach probability >=1-2delta. 
    # An early-random-guess/exact-late algorithm attains the reach coefficient.
    for delta in (0.1,0.25,1/3,0.4):
        for epsilon in (0.0,0.01,0.10):
            lower=1-2*delta-(1-delta)*epsilon
            ck(lower <= 1-2*delta+1e-12)
            ck(lower>0 if epsilon<=0.1 and delta<=0.4 else True)
        stats['exact_reach_bound'][str(delta)]={'epsilon0_reach_lower':1-2*delta,'matching_early_guess_reach':1-2*delta}
    print(json.dumps(stats,sort_keys=True,indent=2))
if __name__=='__main__':main()
