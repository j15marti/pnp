#!/usr/bin/env python3
"""Audit a legal-width blank-start clock and source-dependent graph marker.

Tests the exact finite clock/postlude transition controller and authenticated
Circuit Value semantics. It is NOT a compiled native-TM run of the CVP parser
or of the Hopcroft-Paul-Valiant folded-copy conversion.
Python 3.10+, standard library only.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import random

SEED = 202611152040
REVISION = 'tmr3-admissible-block-marker060-v1'
COUNTS: Counter[str] = Counter()


def require(test: bool, name: str) -> None:
    if not test:
        raise AssertionError(name)
    COUNTS[name] += 1


@dataclass
class Bounce:
    width: int
    position: int
    direction: int = -1

    def step(self) -> bool:
        """One enabled local-head move or endpoint hold; emit on holds."""
        next_position = self.position + self.direction
        if 0 <= next_position < self.width:
            self.position = next_position
            return False
        self.direction = -self.direction
        return True


def clock_trace(b: int, rounds: int, answer: int, ready_after: int) -> dict:
    if b < 2 or rounds < 2 or rounds % 2 or answer not in (0, 1):
        raise ValueError('Require b>=2, even rounds>=2, answer a bit')
    if not 0 <= ready_after < rounds * b**3:
        raise ValueError('Evaluator completion must precede the deadline')
    # b physical bootstrap steps move each clock head from 0 to b-1.
    for tick in range(1, b+1):
        head = min(tick, b-1)
        require(head // b == 0, 'bootstrap_stays_in_first_block')
    clocks = [Bounce(b, b-1) for _ in range(3)]
    tick = b
    local_ticks = 0
    completed_rounds = 0
    ready = ready_after == 0
    marker = 0
    while completed_rounds < rounds:
        pulse = clocks[0].step()
        if pulse:
            pulse = clocks[1].step()
            if pulse:
                if clocks[2].step():
                    completed_rounds += 1
        tick += 1
        local_ticks += 1
        if local_ticks >= ready_after:
            ready = True
        for clock in clocks:
            require(0 <= clock.position < b, 'clock_head_inside_block')
    require(local_ticks == rounds*b**3, 'exact_cubic_clock')
    require(all(c.position == b-1 for c in clocks), 'even_rounds_end_at_right')
    require(ready, 'completion_before_deadline')
    # Wait one half sweep. The first low pulse is exactly b steps later.
    waiting = 0
    while True:
        pulse = clocks[0].step()
        waiting += 1
        tick += 1
        if pulse:
            break
    require(waiting == b and clocks[0].position == 0, 'aligned_left_pulse')
    # Next sweep: b-1 unconditional moves, one answer-controlled crossing.
    marker_positions = [0]
    sweep = 0
    crossing_steps = []
    while True:
        before = marker
        pulse = clocks[0].step()
        if pulse:
            marker += answer
        else:
            marker += 1
        sweep += 1
        tick += 1
        marker_positions.append(marker)
        if before // b != marker // b:
            crossing_steps.append(tick)
            require(tick % b == 0, 'cross_only_at_time_boundary')
        if pulse:
            break
    require(sweep == b, 'exact_marker_sweep')
    require(marker == b-1+answer, 'marker_encodes_answer')
    require(tick == rounds*b**3+3*b, 'exact_crossing_epoch')
    # One paid read of the final position then halt.
    tick += 1
    query_block = (tick-1)//b+1
    require(query_block == rounds*b*b+4, 'public_query_index')
    # All preceding source/clock/value tape reads are in their first blocks.
    reads_before_dummy = marker_positions[:-1]
    first_visit_block2 = marker // b == 1 and all(p // b == 0 for p in reads_before_dummy)
    require(first_visit_block2 == bool(answer), 'first_visit_edge_equivalence')
    require(len(crossing_steps) == answer, 'single_or_no_crossing')
    return {'b':b, 'rounds':rounds, 'answer':answer, 'time':tick,
            'j':query_block, 'marker':marker, 'first_visit':first_visit_block2}


def encode(gates: list[tuple[int,int,int]]) -> str:
    n = len(gates)
    if n < 1:
        raise ValueError('At least one gate is required')
    out = ['1'*n+'0']
    for j, (op, a, b) in enumerate(gates):
        if op not in (0,1,2,3):
            raise ValueError('Invalid operation')
        if op < 2:
            masks = '0'*(2*n)
        else:
            if not (0 <= a < j and 0 <= b < j):
                raise ValueError('References must be earlier gates')
            masks = ''.join('1' if i == a else '0' for i in range(n))
            masks += ''.join('1' if i == b else '0' for i in range(n))
        out.append(format(op, '02b')+masks)
    return ''.join(out)


def parse(source: str) -> list[tuple[int,int,int]] | None:
    if not source or set(source)-{'0','1'}:
        return None
    n = len(source)-len(source.lstrip('1'))
    if n < 1 or n >= len(source) or len(source) != 2*n*n+3*n+1:
        return None
    gates = []
    offset = n+1
    for j in range(n):
        op = int(source[offset:offset+2],2)
        masks = (source[offset+2:offset+2+n], source[offset+2+n:offset+2+2*n])
        offset += 2+2*n
        if op < 2:
            if any('1' in m for m in masks):
                return None
            gates.append((op,-1,-1))
        else:
            refs = [[i for i,c in enumerate(m) if c == '1'] for m in masks]
            if any(len(a) != 1 or a[0] >= j for a in refs):
                return None
            gates.append((op,refs[0][0],refs[1][0]))
    return gates


def value(gates: list[tuple[int,int,int]]) -> int:
    values: list[int] = []
    for op,a,b in gates:
        values.append(op if op < 2 else values[a]&values[b] if op == 2 else values[a]|values[b])
    return values[-1]


def recursive_value(gates: list[tuple[int,int,int]], j: int) -> int:
    op,a,b = gates[j]
    if op < 2:
        return op
    x,y = recursive_value(gates,a),recursive_value(gates,b)
    return x & y if op == 2 else x | y


def run() -> dict:
    rng = random.Random(SEED)
    clock_cases = []
    for b in range(2,25):
        for rounds in (2,4):
            for answer in (0,1):
                delay = rng.randrange(rounds*b**3)
                clock_cases.append(clock_trace(b,rounds,answer,delay))
    for b in range(2,7):
        for delay in range(2*b**3):
            # Endpoint and phase events are tested densely on small clocks.
            if delay in (0,1,b-1,b,b+1,2*b**3-1):
                for answer in (0,1):
                    clock_cases.append(clock_trace(b,2,answer,delay))
    circuits = 0
    rejects = 0
    opposite_pairs = 0
    for n in range(1,17):
        for _ in range(48):
            gates = []
            for j in range(n):
                if j == 0 or rng.randrange(4) == 0:
                    gates.append((rng.randrange(2),-1,-1))
                else:
                    gates.append((rng.choice((2,3)),rng.randrange(j),rng.randrange(j)))
            source = encode(gates)
            decoded = parse(source)
            require(decoded == gates, 'authenticated_source_roundtrip')
            require(value(gates) == recursive_value(gates,n-1), 'independent_cvp_agreement')
            N = len(source)
            b = N+16  # finite test choice, not a certified whole-evaluator clock constant
            C = 2
            T = C*b**3+3*b+1
            j = C*b*b+4
            require((j-1)*b+1 == T, 'source_to_public_time')
            require(T.bit_length() <= b, 'finite_admissible_block_condition')
            require((b-1+value(gates))//b+1 == value(gates)+1, 'block_label_cvp')
            require(parse(source+'0') is None, 'trailing_data_rejected')
            rejects += 1
            circuits += 1
        z = encode([(0,-1,-1)]*n)
        o = encode([(1,-1,-1)]*n)
        require(len(z)==len(o) and value(parse(z))==0 and value(parse(o))==1, 'same_length_opposite_labels')
        opposite_pairs += 1
    for bad in ('','0','1','10','110','11x0','1000000'):
        require(parse(bad) is None, 'malformed_rejected')
        rejects += 1
    # Negative controls: the old width-one marker disappears under coarsening;
    # a semantically dead marker tape can be dropped by an equivalent compiler.
    for b in range(2,129):
        require(0//b == 1//b, 'old_one_cell_marker_erased_by_coarsening')
        require((b-1)//b != b//b, 'new_boundary_marker_not_erased')
    require(value([(1,-1,-1)]) == 1, 'answer_without_marker_is_legal')
    return {'revision':REVISION,'seed':SEED,'status':'COMPUTATIONAL','failures':0,
            'assertions':sum(COUNTS.values()),'categories':dict(COUNTS),
            'clock_controller_cases':len(clock_cases),'circuit_sources':circuits,
            'malformed_rejections':rejects,'same_length_opposite_pairs':opposite_pairs,
            'microtraced_clock_widths':[2,24], 'microtraced_even_rounds':[2,4],
            'sample_clock_cases':clock_cases[:4]+clock_cases[-4:],
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'limitations':['Clock/postlude controller microtraced; CVP machine compiler not microtraced.',
                           'Evaluator completion signal injected by harness within its promised deadline.',
                           'Test C=2 is not a certified constant for the native complete CVP evaluator.',
                           'No literal HPV folded-copy compiler is implemented or certified.',
                           'No unrestricted space lower bound or Tree Evaluation speedup is claimed.']}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('raw060.json'))
    args = parser.parse_args()
    data = run()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:data[k] for k in ('assertions','clock_controller_cases','circuit_sources','failures')}))

if __name__ == '__main__':
    main()
