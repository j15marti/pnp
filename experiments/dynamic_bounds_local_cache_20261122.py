"""Finite checks for accepting transcript rectangles and global-cache failure."""
from itertools import permutations, product
import json

G = list(permutations(range(3)))
E = (0, 1, 2)


def mul(a, b):
    return tuple(a[b[i]] for i in range(3))


def inv(a):
    return tuple(a.index(i) for i in range(3))


def main():
    subsets = [tuple(G[i] for i in range(6) if mask >> i & 1)
               for mask in range(1, 64)]
    accepted = rejected = mixed = 0
    for left, right in product(subsets, repeat=2):
        answers = {mul(a, b) == E for a, b in product(left, right)}
        if answers == {True}:
            accepted += 1
            assert len(left) == len(right) == 1
        elif answers == {False}:
            rejected += 1
        else:
            mixed += 1
    # A scanner compares the right factor's three-bit code with inverse(left).
    # Stop at its first differing bit. Rejecting transcripts may hide right bits.
    fibers = {}
    for a, b in product(G, repeat=2):
        target = format(G.index(inv(a)), "03b")
        observed = format(G.index(b), "03b")
        prefix = ""
        answer = True
        for wanted, seen in zip(target, observed):
            prefix += seen
            if wanted != seen:
                answer = False
                break
        transcript = (G.index(a), prefix, answer)
        fibers.setdefault(transcript, []).append((a, b))
    for record, words in fibers.items():
        if record[2]:
            assert len(words) == 1
    rejection_max = max(len(words) for record, words in fibers.items() if not record[2])
    assert rejection_max > 1
    # One globally cached verdict merges all accepting factor tuples.
    identity_words = [(a, inv(a)) for a in G]
    assert len(identity_words) == 6
    a, b = identity_words[:2]
    assert mul(a[0], b[1]) != E
    print(json.dumps(dict(rectangles=len(subsets)**2, accepting=accepted,
                          rejecting=rejected, mixed=mixed,
                          transcript_fibers=len(fibers),
                          maximum_rejecting_fiber=rejection_max,
                          accepting_global_cache_fiber=len(identity_words),
                          hybrid_flips_answer=True), indent=2))


if __name__ == "__main__":
    main()
