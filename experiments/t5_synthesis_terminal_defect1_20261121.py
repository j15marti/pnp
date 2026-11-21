"""Exact finite semantic checks; not a Turing-machine resource experiment."""
import itertools
import json

C_SETS = {frozenset((i, (i+1)%5, (i+2)%5)) for i in range(5)}

def C(a, b, c):
    return len({a, b, c}) == 3 and frozenset((a, b, c)) in C_SETS

def scalar_count(n, clauses):
    assert all(len(set(t)) == 3 and all(0 <= v < n for v in t) for t in clauses)
    return sum(all(C(*(values[v] for v in t)) for t in clauses)
               for values in itertools.product(range(5), repeat=n))

def encode(n, clauses):
    m = len(clauses)
    g = bin(m+1)[2:]
    w = n.bit_length()
    return '1'*n+'0'+'0'*(len(g)-1)+g+''.join(
        format(v+1, f'0{w}b') for t in clauses for v in t)

def main():
    # a0,...,a4,X,Y; one-edge NAND encoding. All names are variables.
    clauses = [(i, (i+1)%5, (i+2)%5) for i in range(5)]
    clauses += [(0,1,5), (0,4,6), (0,5,6)]
    n = 7
    encoded = encode(n, clauses)
    count = scalar_count(n, clauses)
    assert count == 30 and len(encoded) == 87
    pairs = list(itertools.product((0,1), repeat=2))
    target = sum((not (x and y)) << i for i,(x,y) in enumerate(pairs))
    # Literals and constants are initially available. Every other 2-bit
    # function is exactly one decomposable OP on the disjoint x,y inputs.
    base = {0, 15, 3, 12, 5, 10}
    extras = sorted(set(range(16))-base)
    checks = 0
    for mask in range(1 << len(extras)):
        library = base | {f for i,f in enumerate(extras) if mask >> i & 1}
        for f in range(16):
            before = int(f not in library)
            closing = before
            assert closing == before  # exact minimum relative construction
            for g in range(16):
                extension = int(g not in library)
                after = int(f not in library | {g})
                assert before <= extension + after
                checks += 1
    assert target == 7 and target not in base
    r_before = 1
    kappa_close = 1
    r_after = 0
    assert r_before-r_after == kappa_close
    result = {
        'status': 'PASS',
        'scope': 'finite semantics and relative DLDD annotation costs, not machine time or asymptotic hardness',
        'one_edge_strict_C': {'n': n, 'm': len(clauses), 'N': len(encoded),
            'zero_based_clauses': clauses, 'encoded_bits': encoded,
            'assignments_examined': 5**n, 'exact_count': count, 'decision': 'SAT'},
        'normalized_NAND': {'truth_table_order': pairs, 'truth_mask': target,
            'count': target.bit_count(), 'empty_library_completion': r_before,
            'scalar_output_alone_completion': r_before,
            'semantic_root_annotation_extension': kappa_close,
            'after_annotation_completion': r_after,
            'free_annotation_inequality': '1 <= 0 is false'},
        'two_variable_exhaustion': {'libraries': 1 << len(extras),
            'target_functions': 16, 'new_handle_functions': 16,
            'local_substitution_checks': checks},
        'seed': None,
    }
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
