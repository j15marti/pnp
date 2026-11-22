"""Finite accounting audit for the connected Latin-chain switch scan."""
from collections import Counter
from math import log2, isclose
import json


def entropy(values):
    total = len(values)
    return -sum((n/total)*log2(n/total) for n in Counter(values).values())


def audit(q):
    records = [tuple(int(j == location) for j in range(1, q+1))
               for location in range(q+1)]
    profiles = [tuple(int(any(bits[:j])) for j in range(1, q+1))
                for bits in records]
    decisions = [int(sum(bits) != 1) for bits in records]
    conditional_sum = 0.0
    for j in range(q):
        groups = {}
        for bits, profile in zip(records, profiles):
            prefix = profile[:j]
            groups.setdefault(prefix, []).append(profile[j])
            previous = prefix[-1] if prefix else 0
            assert profile[j] == int(bool(previous or bits[j]))
        conditional_sum += sum(len(group)/(q+1)*entropy(group)
                               for group in groups.values())
    assert isclose(conditional_sum, log2(q+1), abs_tol=1e-12)
    assert len(set(profiles)) == q+1
    assert len({profiles[i] for i in range(1, q+1)}) == q
    prefix_events = [set(range(j+1)) for j in range(q)]
    reuse = max(sum(event in events for events in prefix_events)
                for event in range(q))
    assert reuse == q
    singleton_events = [{j} for j in range(q)]
    assert sum(map(len, singleton_events)) == q
    marginal_sum = sum(entropy([p[j] for p in profiles]) for j in range(q))
    joint_entropy = entropy(profiles)
    assert joint_entropy <= q+1e-12
    # READY contains only the decision. All nonzero switch locations collide.
    assert len(set(decisions[1:])) == 1
    return dict(q=q, chain_entropy=conditional_sum,
                marginal_sum=marginal_sum, prefix_reuse=reuse,
                joint_entropy=joint_entropy, decision_entropy=entropy(decisions),
                hidden_profile_entropy=q/(q+1)*log2(q))


if __name__ == "__main__":
    rows = [audit(q) for q in range(1, 33)]
    print(json.dumps(dict(status="PASS", sizes=32,
                          total_prior_inputs=sum(q+1 for q in range(1, 33)),
                          examples=[rows[i-1] for i in (2, 8, 32)],
                          scope="source profiles and actual-event membership specification; no native tape"),
                     indent=2))
