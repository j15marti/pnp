"""Finite audit of parity in balanced strict-C encodings and left-side replay."""
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import t5_construction_balanced_polarity_20261121 as balanced
import t5_construction_positive_offset1_20261121 as compiler

assert sha256(Path(balanced.__file__).read_bytes()).hexdigest() == 'f6ec1cd05d672b74545dc937a8b9594291b1544ea0fad367cae6385be72bf976'


def circuit(switches):
    gates = [('not', 0), ('or', 0, 1)]
    previous = 2
    for swap in switches:
        left = 1 + len(gates)
        right = left + 1
        first, second = (right, left) if swap else (left, right)
        gates.extend([('not', previous), ('not', left), ('not', first), ('not', second)])
        previous = left + 2
    return gates, previous


def images(switches):
    gates, out = circuit(switches)
    return balanced.twins(1, gates, out)


def audit_cube(k, polarity):
    rows = []
    encodings = {}
    for word in product(range(2), repeat=k):
        n, clauses = images(word)[polarity]
        count, _ = compiler.generic_count(n, clauses)
        positive = (sum(word) + polarity) % 2 == 0
        assert count == 20 * positive
        num, split, links = compiler.split(n, clauses)
        assert (n, len(clauses), num, len(split), links) == (
            31 + 16*k, 51 + 28*k, 641 + 356*k, 783 + 436*k, 122 + 68*k)
        data = compiler.encode(num, split)
        assert compiler.decode(data) == (num, split)
        header = num + 2 + 2*((len(split)+1).bit_length()-1)
        cuts = 3*len(clauses)*num.bit_length()
        encodings[word] = data.encode()
        rows.append(dict(switches=word, unsplit_count=count,
                         split_count=count << links, sha256=sha256(data.encode()).hexdigest()))
    baseline = encodings[(0,)*k]
    blocks = []
    for j in range(k):
        unit = tuple(int(i == j) for i in range(k))
        blocks.append({i for i, (a,b) in enumerate(zip(baseline, encodings[unit])) if a != b})
    assert all(block and min(block) >= header + cuts for block in blocks)
    assert len(set.union(*blocks)) == sum(map(len, blocks))
    for word, data in encodings.items():
        difference = {i for i,(a,b) in enumerate(zip(data,baseline)) if a != b}
        assert difference == set().union(*(block for bit,block in zip(word,blocks) if bit))
    return dict(k=k, polarity=polarity, N=len(baseline), L=cuts, header=header,
                difference_blocks=[sorted(block) for block in blocks], rows=rows), encodings


# Concrete finite promise-machine for k=1, accepting pin. It writes a default
# decision and terminator, sweeps to one public differing cell, then either
# halts there or returns to correct the decision. Countdown states are finite
# for this fixed pair. It ignores neighboring fields only on this promise.
def step(state, symbol, sense, accept_symbol):
    phase, counter = state
    if phase == 'start':
        return '0', 1, ('term', 0)
    if phase == 'term':
        return '#', 1, ('out', 2)
    if phase == 'out':
        if counter < sense:
            return symbol, 1, ('out', counter + 1)
        if symbol != accept_symbol:
            return symbol, 0, ('halt', 0)
        return symbol, -1, ('back', counter - 1)
    if phase == 'back' and counter:
        return symbol, -1, ('back', counter - 1)
    assert phase == 'back'
    return '1', 0, ('halt', 0)


def exercise_replay(cube, pair):
    sense = cube['difference_blocks'][0][0]
    accept_symbol = chr(pair[(0,)][sense])
    traces = []
    for word, data in pair.items():
        tape = list(data.decode())
        cuts = [cube['header'], cube['header'] + cube['L']//2, cube['header'] + cube['L'] - 1]
        tokens = {c: [] for c in cuts}
        state, head = ('start', 0), 0
        while state[0] != 'halt':
            char, move, state = step(state, tape[head], sense, accept_symbol)
            tape[head] = char
            if move == -1 and head-1 in tokens:
                tokens[head-1].append(state)
            head += move
        for c in cuts:
            if head > c:
                tokens[c].append(None)
            source_left = list(pair[(0,)][:c+1].decode())
            head_left, state = 0, ('start', 0)
            record = iter(tokens[c])
            while state[0] != 'halt':
                char, move, state = step(state, source_left[head_left], sense, accept_symbol)
                source_left[head_left] = char
                head_left += move
                if head_left > c:
                    state = next(record)
                    if state is None:
                        break
                    head_left = c
            assert next(record, 'end') == 'end'
            assert source_left[:2] == tape[:2] == list('0#' if word[0] else '1#')
        traces.append(dict(switches=word, tokens_by_cut=tokens, answer=tape[0]))
    return traces


if __name__ == '__main__':
    cubes = []
    for k in range(1,5):
        for polarity in (0,1):
            cube, encodings = audit_cube(k, polarity)
            cubes.append(cube)
            if (k,polarity) == (1,0):
                traces = exercise_replay(cube, encodings)
    print(json.dumps(dict(cubes=cubes, finite_promise_machine=traces,
                          source_sha256=sha256(Path(__file__).read_bytes()).hexdigest()),
                     indent=2))
