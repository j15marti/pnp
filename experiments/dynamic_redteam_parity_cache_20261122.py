"""Audit local caches with destructive reads on one unit-speed tape."""
from itertools import permutations, product
from collections import Counter
import json

G = tuple(permutations(range(3)))
I = (0, 1, 2)


def compose(a, b):
    return tuple(a[b[i]] for i in range(3))


def sign(p):
    return sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3)) % 2


def oracle(word):
    return tuple(follow(word, i) for i in range(3)) == I


def follow(word, point):
    for p in reversed(word):
        point = p[point]
    return point


def run(word):
    r = len(word)
    tape = {0: "@", r+2: "|", 4*r+3: "$"}
    hidden = set()
    for j, p in enumerate(word):
        tape[j+2] = str(sign(p))
        hidden.add(j+2)
        for k, bit in enumerate(format(G.index(p), "03b")):
            address = r+3+3*j+k
            tape[address] = bit
            hidden.add(address)
    head, state, parity, partial, acc = 2, "signs", 0, "", I
    seen, record, reads = set(), [], []
    answer = None
    while state != "halt":
        old = tape.get(head, "_")
        reads.append(head)
        if head in hidden and head not in seen:
            record.append(old)
            seen.add(head)
        if state == "signs":
            if old == "|":
                state = "return" if parity else "tags"
                answer = False if parity else None
                head += -1 if parity else 1
            else:
                parity ^= int(old)
                tape[head] = "_"  # destructive read still records initial value
                head += 1
        elif state == "tags":
            if old == "$":
                assert partial == ""
                answer = acc == I
                state = "return"
                head -= 1
            else:
                partial += old
                if len(partial) == 3:
                    acc = compose(acc, G[int(partial, 2)])
                    partial = ""
                head += 1
        elif state == "return":
            if old == "@":
                tape[head] = str(int(answer))
                state = "terminate"
                head += 1
            else:
                head -= 1
        else:
            assert state == "terminate" and head == 1
            tape[head] = "!"
            state = "halt"
    assert tape[0] == str(int(answer)) and tape[1] == "!"
    assert all(abs(a-b) <= 1 for a, b in zip(reads, reads[1:]))
    return answer, "".join(record), len(reads), max(reads), len(seen)


def main():
    cases = []
    for r in (3, 4, 5):
        odd_fibers = Counter()
        accepting_records = set()
        times = set()
        for word in product(G, repeat=r):
            answer, record, steps, furthest, distinct = run(word)
            assert answer == oracle(word)
            parity = sum(sign(p) for p in word) % 2
            if parity:
                assert not answer and distinct == r
                assert furthest == r+2 and steps == 2*r+4
                odd_fibers[record] += 1
                times.add(steps)
            elif answer:
                assert record not in accepting_records
                accepting_records.add(record)
        assert len(odd_fibers) == 2**(r-1)
        assert set(odd_fibers.values()) == {3**r}
        assert len(accepting_records) == 6**(r-1)
        cases.append(dict(r=r, words=6**r, odd_records=len(odd_fibers),
                          products_per_odd_record=3**r,
                          odd_suffix_steps=sorted(times),
                          accepting_records=len(accepting_records)))
    print(json.dumps(dict(cases=cases, all_agree=True,
                          destructive_reads=True, unit_speed=True), indent=2))


if __name__ == "__main__":
    main()
