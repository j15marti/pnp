"""Unit-step suffix simulation with destructive reads; no source parser."""
from collections import Counter
from itertools import product
import json


def run(bits):
    tape = {0: "#", **{i+1: str(b) for i,b in enumerate(bits)}, len(bits)+1: "$"}
    head = 0
    state = ("start", 0, False)
    steps = cm = 0
    frontiers = {}
    while state[0] != "halt":
        symbol = tape.get(head, "_")
        phase, count, seen = state
        if phase == "start":
            head += 1
            state = ("scan", 0, False)
        elif phase == "scan":
            if symbol == "$":
                tape.pop(head)
                head -= 1
                state = ("return", 0, True)
            else:
                assert symbol in ("0", "1")
                tape.pop(head)
                seen = seen or symbol == "1"
                count += 1
                if count == 3 and not seen:
                    head -= 1
                    state = ("return", 0, False)
                else:
                    head += 1
                    state = ("scan", count % 3, seen if count < 3 else False)
        elif phase == "return":
            if symbol == "#":
                tape[0] = str(int(seen))
                head += 1
                state = ("finish", 0, seen)
            else:
                head -= 1
        else:
            tape[head] = "!"
            state = ("halt", 0, seen)
        steps += 1
        span = max([0, head, *tape]) - min([0, head, *tape]) + 1
        cm += span
        if head >= 1 and head <= len(bits) and (head-1) % 3 == 0:
            j = (head-1)//3
            if j not in frontiers:
                tail = tuple(tape.get(p, "_") for p in range(head, len(bits)+1))
                frontiers[j] = tail
    return int(tape[0]), steps, cm, frontiers


def main():
    all_cases = 0
    for m in range(1, 5):
        for bits in product((0, 1), repeat=3*m):
            verdict, _, _, _ = run(bits)
            assert verdict == all(any(bits[i:i+3]) for i in range(0,len(bits),3))
            all_cases += 1
    records = []
    for m in range(1, 8):
        counts = [Counter() for _ in range(m)]
        times, costs = set(), set()
        for witness in product(range(3), repeat=m):
            bits = tuple(int(d == a) for a in witness for d in range(3))
            verdict, time, cm, fronts = run(bits)
            assert verdict == 1 and len(fronts) == m
            times.add(time)
            costs.add(cm)
            for j, tail in fronts.items():
                assert tail == tuple(str(x) for x in bits[3*j:])
                counts[j][tail] += 1
        assert all(len(c) == 3**(m-j) and set(c.values()) == {3**j}
                   for j,c in enumerate(counts))
        records.append(dict(m=m, sparse_inputs=3**m, times=sorted(times),
                            physical_cm=sorted(costs),
                            tail_entropy_log3_coefficient=m*(m+1)//2))
    print(json.dumps(dict(all_label_cases=all_cases, sparse=records), indent=2))


if __name__ == "__main__":
    main()
