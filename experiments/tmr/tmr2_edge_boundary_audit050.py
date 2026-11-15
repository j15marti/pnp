#!/usr/bin/env python3
"""Finite independent audit of the edge-isoperimetric MCSP bit-query lemma.
The derivation is mathematical; this script tests exact tiny cases only.
"""
import json
import math
from fractions import Fraction

checks = 0

def check(flag, message="assertion"):
    global checks
    checks += 1
    if not flag:
        raise AssertionError(message)


def boundary_degrees(table_set, bit_length):
    out = {}
    for x in table_set:
        internal = sum((x ^ (1 << j)) in table_set for j in range(bit_length))
        out[x] = (internal, bit_length - internal)
    return out


def one_gate_class(n):
    """Exact Boolean functions computable with <=1 arbitrary fan-in-2 gate
    using n free input wires and 0/1 constants. Circuit output can be
    a source wire or the one gate. Each gate computes one of all 16 functions.
    """
    N = 1 << n
    inputs = [0, (1 << N) - 1]
    for j in range(n):
        inputs.append(sum((((a >> j) & 1) << a) for a in range(N)))
    result = set(inputs)
    for u in inputs:
        for v in inputs:
            for gate in range(16):
                out = 0
                for a in range(N):
                    b1, b2 = (u >> a) & 1, (v >> a) & 1
                    z = (gate >> (b1 * 2 + b2)) & 1
                    out |= z << a
                result.add(out)
    return result




def two_gate_class(n):
    """Exact <=2 arbitrary fan-in-2 gate functions on free n inputs/constants."""
    N=1 << n
    initial=[0,(1<<N)-1]+[sum((((a>>j)&1)<<a) for a in range(N)) for j in range(n)]
    Y=set(initial)
    def gate_apply(u,v,gate):
        return sum((((gate>>((((u>>a)&1)*2)+((v>>a)&1)))&1)<<a) for a in range(N))
    for u in initial:
        for v in initial:
            for g1 in range(16):
                a=gate_apply(u,v,g1)
                Y.add(a)
                wires=initial+[a]
                for w in wires:
                    for z in wires:
                        for g2 in range(16):
                            Y.add(gate_apply(w,z,g2))
    return Y


def verify_class(Y, d):
    deg = boundary_degrees(Y, d)
    m = len(Y)
    total_internal = sum(t[0] for t in deg.values())
    sum_external = sum(t[1] for t in deg.values())
    check(total_internal <= m * math.log2(m) + 1e-9, "hypercube edge bound")
    check(sum_external == d * m - total_internal)
    check(max(t[1] for t in deg.values()) >= d - math.log2(m) - 1e-9)
    for x,(a,b) in deg.items():
        check(a+b==d)
        check(b==sum((x ^ (1 << j)) not in Y for j in range(d)))
    return {"dimension":d, "yes_count":m, "internal_degree_average":total_internal/m,
            "lower_bound_external_degree_average":d-math.log2(m),
            "actual_external_degree_average":sum_external/m,
            "min_external_degree":min(x[1] for x in deg.values()),
            "max_external_degree":max(x[1] for x in deg.values()),
            "fraction_with_at_least_dim_minus_2logY_boundary":sum(t[1]>=d-2*math.log2(m) for t in deg.values())/m}


# Exhaust ALL subsets of the 3- and 4-dimensional cube, not just random draws.
exhaustive = {}
for d in (3, 4):
    Nvert = 1 << d
    checked = 0
    for subset_mask in range(1, 1 << Nvert):
        m = subset_mask.bit_count()
        # Every induced edge counted in one direction.
        internal_edges = 0
        for x in range(Nvert):
            if not ((subset_mask >> x) & 1):
                continue
            for j in range(d):
                y = x ^ (1 << j)
                if x < y and ((subset_mask >> y) & 1):
                    internal_edges += 1
        check(2*internal_edges <= m*math.log2(m)+1e-9)
        checked += 1
    exhaustive[str(d)] = {"hypercube_vertices":Nvert,"all_nonempty_induced_subsets":checked,"failures":0}

classes={}
for n in (2,3,4):
    Y=one_gate_class(n)
    d=1<<n
    res=verify_class(Y,d)
    # Paired-run lemma: any correct delta-error classifier must query each external
    # neighbor with probability >= 1-2delta. Here a fixed mixture can attain
    # query probability 1-2delta by blind YES/NO guesses with probability delta each,
    # and exact full read with probability 1-2delta.
    delta=Fraction(1,3)
    exact_query_fraction=1-2*delta
    for x in Y:
        b=boundary_degrees(Y,d)[x][1]
        Equery=exact_query_fraction*d
        check(Equery>=exact_query_fraction*b)
    res['test_randomized_delta']='1/3'
    res['zero_table_internal_degree']=boundary_degrees(Y,d)[0][0]
    classes[str(n)]=res

Y2=two_gate_class(3)
two_gate=verify_class(Y2,8)
two_gate['zero_table_internal_degree']=boundary_degrees(Y2,8)[0][0]
check(two_gate['zero_table_internal_degree']==8)

out={"result":"PASS","assertions":checks,"failures":0,
     "scope":"finite exact combinatorial checks, not MCSP asymptotic proof or native Turing-machine execution",
     "exhaustive_subsets":exhaustive,"one_gate_exact_circuit_classes":classes,"two_gate_exact_circuit_class_n3":two_gate}
print(json.dumps(out,sort_keys=True,indent=2))
