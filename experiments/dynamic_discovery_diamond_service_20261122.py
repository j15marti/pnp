"""Exhaust a one-edit synopsis and the identity-query reduction on S3 words."""
import itertools
import json

GROUP = tuple(itertools.permutations(range(3)))
IDENTITY = (0, 1, 2)


def compose(left, right):
    return tuple(left[i] for i in right)


def inverse(p):
    return tuple(p.index(i) for i in range(3))


def whole_word(word):
    # Independent oracle: follow each point through the factors right to left.
    images = []
    for point in range(3):
        for factor in reversed(word):
            point = factor[point]
        images.append(point)
    return tuple(images)


def repairs(word):
    prefix = IDENTITY
    tags = []
    for factor in word:
        tags.append(prefix)
        prefix = compose(prefix, factor)
    suffix = IDENTITY
    for j in reversed(range(len(word))):
        tags[j] = compose(inverse(tags[j]), inverse(suffix))
        suffix = compose(word[j], suffix)
    return tuple(tags)


def check(d):
    signatures = set()
    queries = 0
    tail_tests = 0
    words = 0
    for word in itertools.product(GROUP, repeat=d):
        words += 1
        product = whole_word(word)
        tags = repairs(word)
        for j, tag in enumerate(tags):
            for a in GROUP:
                changed = word[:j] + (a,) + word[j + 1:]
                assert (a == tag) == (whole_word(changed) == IDENTITY)
                queries += 1
        matches = [g for g in GROUP if whole_word(word + (inverse(g),)) == IDENTITY]
        assert matches == [product]
        tail_tests += len(GROUP)
        if product == IDENTITY:
            assert tags == word and tags not in signatures
            signatures.add(tags)
    assert len(signatures) == 6 ** (d - 1)
    return dict(d=d, words=words, replacement_booleans=queries,
                distinct_accepting_origin_signatures=len(signatures),
                identity_tail_booleans=tail_tests)


def main():
    swap = (1, 0, 2)
    original = (IDENTITY,) * 3
    changed = (swap,) + original[1:]
    assert repairs(original)[1] == IDENTITY
    assert repairs(changed)[1] == swap
    print(json.dumps(dict(cases=[check(d) for d in (3, 4)],
                          stale_tag_before=repairs(original)[1],
                          stale_tag_after=repairs(changed)[1]), indent=2))


if __name__ == "__main__":
    main()
