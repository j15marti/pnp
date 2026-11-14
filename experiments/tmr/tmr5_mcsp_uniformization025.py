#!/usr/bin/env python3
"""TMR-5/025 finite verifier: sparse ordered residuals and toy diagonal controls.

This is finite evidence only. The unrestricted uniform non-P theorem is symbolic
and is proved in the companion report, not by these loops.
"""
import json
from collections import Counter


def residual_partition(N, accepted, cut):
    """Map a prefix to its exact set of accepting suffixes."""
    width = N-cut
    found = {}
    for prefix in range(1<<cut):
        suffixes = tuple(s for s in range(1<<width)
                         if (prefix<<width | s) in accepted)
        found[prefix] = suffixes
    return found


def check_language(N, accepted):
    maxwidth = 0
    transitions = 0
    for d in range(N+1):
        residuals = residual_partition(N,accepted,d)
        maxwidth=max(maxwidth,len(set(residuals.values())))
        assert len(set(residuals.values()))<=len(accepted)+1
        if d<N:
            nr=residual_partition(N,accepted,d+1)
            half=1<<(N-d-1)
            for p,r in residuals.items():
                assert nr[2*p] == tuple(x for x in range(half) if x in r)
                assert nr[2*p+1] == tuple(x for x in range(half) if x+half in r)
                transitions+=2
    assert len(accepted)==sum(bool(residual_partition(N,accepted,N)[i]) for i in range(1<<N))
    return maxwidth,transitions


def nu2(n):
    assert n>0
    return (n & -n).bit_length()-1


def toy_machine(i,n):
    return [lambda z:0,lambda z:1,lambda z:z&1][i](n) if i<3 else (i+n)&1


def toy_h(n):
    return 1-toy_machine(nu2(n), n)


def main():
    count=0; transitions=0; bound_equal=0; width_hist=Counter(); size_hist=Counter()
    for N in range(1,5):
        all_strings=1<<N
        for mask in range(1<<all_strings):
            Y={x for x in range(all_strings) if mask>>x&1}
            w,t=check_language(N,Y)
            assert w<=len(Y)+1
            width_hist[str(w)]+=1
            size_hist[str(len(Y))]+=1
            count+=1; transitions+=t
            if w==len(Y)+1:bound_equal+=1
    toy_samples=[]; singular_checks=0
    for N in range(1,129):
        h=toy_h(N)
        assert h != toy_machine(nu2(N),N)
        if N<=8:
            Y={0 if h==0 else (1<<N)-1}
            w,t=check_language(N,Y)
            assert w==2
            singular_checks+=1
        if N<=24 or N in (32,64,96,128):
            toy_samples.append([N,nu2(N),h])
    print(json.dumps({
        'artifact':'TMR5_UNIFORMIZATION025','status':'FINITE_COMPUTATIONAL',
        'all_boolean_languages_N_le_4':count,
        'all_prefix_successor_checks':transitions,
        'num_width_equals_size_plus_one':bound_equal,
        'width_histogram':dict(sorted(width_hist.items(),key=lambda kv:int(kv[0]))),
        'accepted_size_histogram':dict(sorted(size_hist.items(),key=lambda kv:int(kv[0]))),
        'toy_diagonal_n_le_128':128,'singleton_width_two_checks':singular_checks,
        'toy_samples':toy_samples,'failures':0
    },sort_keys=True,indent=2))

if __name__=='__main__':
    main()
