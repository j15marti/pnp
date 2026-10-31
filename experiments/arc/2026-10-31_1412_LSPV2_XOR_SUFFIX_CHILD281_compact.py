#!/usr/bin/env python3
"""Compact independently runnable cross-check for LSPV-2 XOR_SUFFIX_CHILD281.
Full event-sourced producer, replay checker, source proof verifier and all raw
gzip events are in the run archive. This compact checker reproduces the exact
restricted suffix-child map, parent/child lengths, and indexed resource totals.
Run: python experiments/arc/2026-10-31_1412_LSPV2_XOR_SUFFIX_CHILD281_compact.py
"""
from pathlib import Path
from collections import Counter
import ast, copy, json

SOURCE = Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt")
Y6 = [[1,2,3],[1,4,5],[2,4,6],[3,5,6],
      [-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]
V_MODEL = "001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101"

def parse():
    text = SOURCE.read_text()
    return ast.literal_eval(text[text.index('[['):])

def grammar(f):
    if not f: return False
    n = max(abs(z) for c in f for z in c)
    counts = Counter((abs(z), z > 0) for c in f for z in c)
    keys = [tuple(sorted(c)) for c in f]
    return (len(keys) == len(set(keys)) and len(f)*3 == 4*n
            and all(len(c) == 3 and len({abs(z) for z in c}) == 3
                    and len({z > 0 for z in c}) == 1 for c in f)
            and all(counts[v,sign] == 2 for v in range(1,n+1)
                    for sign in (False,True)))

def gamma(k):
    s = format(k,'b')
    return '0'*(len(s)-1) + s

def enc(f):
    n = max(abs(z) for c in f for z in c)
    w = n.bit_length()
    return gamma(n)+gamma(len(f))+''.join(
        ('1' if c[0] > 0 else '0') +
        ''.join(format(abs(z),f'0{w}b') for z in c) for c in f)

def product(a,b):
    off = max(abs(z) for c in a for z in c)
    return [c[:] for c in a] + [
        [(abs(z)+off) * (1 if z>0 else -1) for z in c] for c in b]

def satisfies(f,model):
    return all(any(bool(model[abs(z)-1]) == (z>0) for z in c) for c in f)

def audit(parent,child):
    p = enc(parent);q = enc(child)
    np = max(abs(z) for c in parent for z in c)
    nc = max(abs(z) for c in child for z in c)
    wp = np.bit_length();wc = nc.bit_length()
    hp = gamma(np)+gamma(len(parent))
    hc = gamma(nc)+gamma(len(child))
    index_width = len(p).bit_length()
    source_addresses = list(range(len(p)))  # charged membership scan
    for pos in range(len(hc),len(q)):
        cl,t = divmod(pos-len(hc),1+3*wc)
        src = len(hp) + cl*(1+3*wp)
        if t == 0:
            source_addresses.append(src)
        else:
            lit,_ = divmod(t-1,wc)
            source_addresses.extend(range(src+1+lit*wp,src+1+(lit+1)*wp))
    index_set_bits = 0
    head = 0
    index_head_moves = 0
    for src in source_addresses:
        assert 0 <= src < len(p)
        for bit_idx,digit in enumerate(format(src+1,f'0{index_width}b')):
            if digit == '1':
                index_set_bits += 1
                index_head_moves += abs(bit_idx-head)
                head = bit_idx
    work_head_moves = max(0,len(q)-1)
    moves = index_head_moves + work_head_moves
    time = len(q) + len(source_addresses) + index_set_bits + moves
    dphys = q.count('1') + 2*index_set_bits
    assert dphys <= 2*time
    return dict(parent_bits=len(p),child_bits=len(q),
                source_bit_reads=len(source_addresses),
                index_bit_writes=index_set_bits,index_erased_bits=index_set_bits,
                work_writes=len(q),work_unchanged_writes=q.count('0'),
                head_moves=moves,primitive_step_proxy=time,
                total_adjacent_xor=dphys,endpoint_xor=q.count('1'),
                strict_power_short=(len(q)*len(q)<=len(p)))

def main():
    u = parse()
    v = copy.deepcopy(u)
    assert 197 in v[2] and 196 in v[44]
    v[2][v[2].index(197)] = 196
    v[44][v[44].index(196)] = 197
    assert all(grammar(f) for f in (u,v,Y6))
    witness = list(map(int,V_MODEL))
    assert len(witness)==198 and satisfies(v,witness) and not satisfies(u,witness)
    y = next([k>>i&1 for i in range(6)] for k in range(64)
             if satisfies(Y6,[k>>i&1 for i in range(6)]))
    records = {}
    for name,child in (('Y6_SAT',Y6),('U198_UNSAT',u),('V198_SAT',v)):
        parent = product(child,Y6)
        assert grammar(parent) and grammar(child)
        assert parent[:-8] == child and parent[-8:] != child[-8:]
        records[name] = audit(parent,child)
        if name != 'U198_UNSAT':
            wm = y if name == 'Y6_SAT' else witness
            assert satisfies(child,wm) and satisfies(parent,wm+y)
    expected = {'Y6_SAT':(224,92,520,7463,3879,43),
                'U198_UNSAT':(6832,6632,57784,1562559,719784,3046),
                'V198_SAT':(6832,6632,57784,1562559,719784,3046)}
    for name,vals in expected.items():
        got=records[name]
        actual=tuple(got[x] for x in ('parent_bits','child_bits','source_bit_reads',
                   'primitive_step_proxy','total_adjacent_xor','endpoint_xor'))
        assert actual == vals, (name,actual,vals)
    print(json.dumps(records,indent=2))
    print('END_OF_VERIFIED_CHECKER::LSPV2_XOR_SUFFIX_CHILD281_COMPACT')

if __name__ == '__main__':
    main()
