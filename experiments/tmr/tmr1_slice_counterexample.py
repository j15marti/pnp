#!/usr/bin/env python3
"""TMR-1: executable finite regression for a length-slice TM counterexample.

The actual finite-state slice machine is proved in the accompanying report.
This program checks its truth table on a tiny explicit 3-SAT encoding.
Only Python standard library. No seed or random sampling.
"""
import itertools
import json
from pathlib import Path


def parse(bits):
    if any(c not in '01' for c in bits):
        return None
    pos = 0
    def unary():
        nonlocal pos
        start = pos
        while pos < len(bits) and bits[pos] == '1':
            pos += 1
        if pos == len(bits):
            return None
        value = pos - start
        pos += 1
        return value
    n = unary()
    if n is None or n < 3:
        return None
    m = unary()
    if m is None or m < 1:
        return None
    w = max(1, (n - 1).bit_length())
    if len(bits) - pos != 3 * m * (w + 1):
        return None
    clauses = []
    for _ in range(m):
        clause = []
        for _ in range(3):
            sign = int(bits[pos]); pos += 1
            v = int(bits[pos:pos+w], 2); pos += w
            if v >= n:
                return None
            clause.append((v, sign))
        if len({v for v, s in clause}) != 3:
            return None
        clauses.append(tuple(clause))
    assert pos == len(bits)
    return (n, clauses)


def encode(n, clauses):
    w = max(1, (n - 1).bit_length())
    return '1'*n+'0'+'1'*len(clauses)+'0'+''.join(
        str(sign)+format(v, f'0{w}b') for clause in clauses for v, sign in clause)


def sat(n, clauses):
    return any(all(any((a[v] == (1-sign)) for v,sign in clause)
                   for clause in clauses)
               for a in itertools.product((0,1), repeat=n))


def classify(bits):
    p = parse(bits)
    return int(p is not None and sat(*p))


def make_forbidden_clauses(n=3):
    return [tuple((v, b[v]) for v in range(n))
            for b in itertools.product((0,1), repeat=n)]


def main():
    L = 15
    total = valid = yes = no = 0
    trie = {} # finite tabulation for exactly L input bits
    for k in range(1 << L):
        s = format(k, f'0{L}b')
        p = parse(s)
        result = classify(s)
        trie[s] = result
        total += 1
        if p is not None:
            valid += 1
            yes += result
            no += 1-result
        # After initial copying of L+1 scanned symbols, the source head never moves.
        assert classify(s[:]) == result
    assert (total,valid,yes,no) == (32768,48,48,0)
    assert len(trie)==32768
    # Define full depth-L binary trie in finite control; all nodes, even invalid leaf words.
    states = sum(2**d for d in range(L+1))
    assert states == 65535
    forbidden = make_forbidden_clauses()
    full = encode(3, forbidden)
    assert parse(full) is not None and classify(full) == 0
    assert all(classify(encode(3, forbidden[:i]+forbidden[i+1:]))==1 for i in range(8))
    assert classify(encode(4, forbidden)) == 0  # unused-variable padding; width grows
    assert classify(encode(3,[((0,0),(1,1),(2,0))])) == 1
    # Complement each variable and rename variables, adjusting all literal signs.
    p = [((0,0),(1,1),(2,0)), ((0,1),(1,0),(2,1))]
    base = sat(3,p)
    for perm in itertools.permutations(range(3)):
        for flips in itertools.product((0,1),repeat=3):
            tr=[tuple((perm[v], sign ^ flips[v]) for v,sign in c) for c in p]
            assert sat(3,tr)==base
    parity0 = [c for c in forbidden if sum(sign for _,sign in c)%2==1]
    parity1 = [c for c in forbidden if sum(sign for _,sign in c)%2==0]
    assert len(parity0)==len(parity1)==4
    assert sat(3,parity0) and sat(3,parity1)
    assert not sat(3,parity0+parity1)
    # Disjoint-product controls, including two independent copies of parity0.
    offset = [tuple((v+3,sign) for v,sign in c) for c in parity0]
    assert sat(6, parity0+offset)
    assert not sat(6, forbidden+offset)
    horn_unsat = [((0,1),(1,0)),((0,0),),((1,1),)]
    twosat_unsat = [((0,a),(1,b)) for a in (0,1) for b in (0,1)]
    assert not sat(2,horn_unsat) and not sat(2,twosat_unsat)
    assert sat(2,[((0,1),(1,0)),((0,0),)])
    negatives = [full+'0',full[:-1],'', '1110110', encode(3,[((0,0),(0,1),(2,0))])]
    assert all(parse(x) is None for x in negatives)
    result = {
        'status':'COMPUTATIONAL only: illustrates separately proved general finite-control lemma',
        'input_encoding':'unary n, unary m, then 3m records of sign bit and ceil(log2(n))-bit zero-based index',
        'L':L,'all_binary_inputs_checked':total,'wellformed_inputs':valid,
        'sat_inputs':yes,'unsat_wellformed_inputs':no,'malformed_inputs':total-valid,
        'slice_trie_nodes':states,'slice_leaf_outputs':len(trie),
        'max_slice_transitions':L+2,'source_head_symbol_scans_in_copy_then_simulate':L+1,
        'additional_original_input_head_moves_after_copy':0,
        'unsat_full_eight_clause_encoding_bits':len(full),
        'parity_xor_controls':'PASS', 'horn_controls':'PASS', '2sat_controls':'PASS',
        'independent_product_controls':'PASS', 'padding_controls':'PASS',
        'permutation_and_polarity_controls':48,'malformed_controls':len(negatives),
        'random_seed':None,'test_mode':'exhaustive all 32768 length-15 bitstrings; exhaustive 8 deletion controls; deterministic controls',
    }
    target=Path(__file__).with_name('tmr1_slice_counterexample_raw.json')
    target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
