#!/usr/bin/env python3
"""Exact growing-tournament r-extension checks and source-preserving NO controls.
Python standard library; deterministic seeds. No unrestricted SAT lower bound.
"""
import itertools, random, json, hashlib

def tournament(k, seed):
    rng = random.Random(seed)
    out = [0] * k
    for u in range(k):
        for v in range(u + 1, k):
            if rng.getrandbits(1):
                out[u] |= 1 << v
            else:
                out[v] |= 1 << u
    return out

def in_masks(out):
    k = len(out); full = (1 << k) - 1
    return [full ^ ((1 << u) | out[u]) for u in range(k)]

def check_r_extension(out, r):
    k = len(out); full = (1 << k) - 1; ins = in_masks(out)
    tests = 0; min_candidate = k
    for anchors in itertools.combinations(range(k), r):
        for sig in range(1 << r):
            candidates = full
            for i, u in enumerate(anchors):
                candidates &= out[u] if sig & (1 << i) else ins[u]
            cnt = candidates.bit_count()
            tests += 1
            if cnt < min_candidate: min_candidate = cnt
            if cnt == 0:
                return {"passes": False, "tests": tests,
                        "witness": {"anchors": anchors, "signature": sig},
                        "min_extensions": 0}
    return {"passes": True, "tests": tests, "min_extensions": min_candidate}

def vertex_cycle_counts(out):
    k = len(out); ins = in_masks(out)
    return tuple(sorted(sum((out[v] & ins[u]).bit_count()
                            for v in range(k) if out[u] >> v & 1)
                        for u in range(k)))

def score_sequence(out):
    return tuple(sorted(int(x).bit_count() for x in out))

def switch_triangle(out, u, v, w):
    new = out[:]
    for a, b in [(u, v), (v, w), (w, u)]:
        assert (out[a] >> b) & 1
        new[a] &= ~(1 << b)
        new[b] |= (1 << a)
    return new

def find_degree_preserving_nonisomorphic(out):
    k = len(out); before = vertex_cycle_counts(out)
    for u in range(k):
        for v in range(k):
            if not ((out[u] >> v) & 1): continue
            for w in range(k):
                if ((out[v] >> w) & 1) and ((out[w] >> u) & 1):
                    other = switch_triangle(out, u, v, w)
                    assert score_sequence(out) == score_sequence(other)
                    if vertex_cycle_counts(other) != before:
                        return (u, v, w), other
    return None, None

def serialized_digest(out):
    k = len(out)
    bits = bytes([((out[u] >> v) & 1) for u in range(k)
                  for v in range(u + 1, k)])
    return hashlib.sha256(bits).hexdigest()

def prefix_counts(target, source, depth_max):
    k = len(target); ins = in_masks(target); full = (1 << k) - 1
    levels = [0] * (depth_max + 1)
    def walk(chosen, used):
        t = len(chosen)
        levels[t] += 1
        if t == depth_max: return
        feasible = full ^ used
        for u, a in enumerate(chosen):
            feasible &= target[a] if (source[u] >> t) & 1 else ins[a]
        while feasible:
            bit = feasible & -feasible
            feasible ^= bit
            walk(chosen + [bit.bit_length() - 1], used | bit)
    walk([], 0)
    return levels

def run(k, r, seed):
    out = tournament(k, seed)
    prop = check_r_extension(out, r)
    tri, alter = find_degree_preserving_nonisomorphic(out)
    depths = prefix_counts(out, alter, 4) if alter is not None else None
    return {"k": k, "n": k, "r": r, "seed": seed,
            "template_sha256": serialized_digest(out),
            "extension": prop,
            "no_instance_locally_compatible_prefix_counts_depth_0_to_4": depths,
            "score_preserving_no": None if tri is None else {
                "reversed_cycle": tri, "no_sha256": serialized_digest(alter),
                "same_score_sequence": score_sequence(out) == score_sequence(alter),
                "nonisomorphism_certificate": "sorted per-vertex directed-3-cycle incidence differs",
                "before_triangle_incidence_sha256": hashlib.sha256(json.dumps(vertex_cycle_counts(out)).encode()).hexdigest(),
                "after_triangle_incidence_sha256": hashlib.sha256(json.dumps(vertex_cycle_counts(alter)).encode()).hexdigest()
            }}

def main():
    cases = [(31, 1, 2026111801), (63, 2, 2026111802), (127, 3, 2026111803)]
    controls = []
    for k in (5, 31, 63, 127):
        out = [sum(1 << ((u + d) % k) for d in range(1, (k-1)//2+1))
               for u in range(k)]
        controls.append({"k": k, "type": "regular cyclic tournament",
                         "r_2_extension": check_r_extension(out, 2)})
    data = {"model": "loopless complete tournament with all labeled pairs oriented",
            "mode": "exact exhaustive r-extension enumeration, no unrestricted SAT lower bound",
            "cases": [run(*case) for case in cases],
            "circulant_negative_controls": controls}
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
