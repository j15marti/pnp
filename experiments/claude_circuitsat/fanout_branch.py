"""Verify Lemma (fan-out branching): Circuit-SAT in O(2^f * s), f = #nodes of fan-out>=2.
Random B2 circuits, compare with brute force. Runs well under 30 s."""
import itertools, json, random
random.seed(1)
def rand_circ(n, s):
    gates = []  # (op_truthtable(4 bits), a, b); nodes 0..n-1 inputs, n.. gates
    for g in range(s):
        m = n + g
        gates.append((random.randrange(16), random.randrange(m), random.randrange(m)))
    return gates
def ev(n, gates, x):
    v = list(x)
    for tt, a, b in gates:
        v.append((tt >> (2 * v[a] + v[b])) & 1)
    return v[-1]
def brute(n, gates):
    return any(ev(n, gates, x) for x in itertools.product((0, 1), repeat=n))
def branch(n, gates):
    N = n + len(gates); out = N - 1
    fo = [0] * N
    for _, a, b in gates:
        fo[a] += 1; fo[b] += 1
    stems = [u for u in range(N) if fo[u] >= 2 and u != out]
    # reachable cone of output
    cone = set(); st = [out]
    while st:
        u = st.pop()
        if u in cone: continue
        cone.add(u)
        if u >= n: st += [gates[u - n][1], gates[u - n][2]]
    # fan-out counted only inside cone
    fo = [0] * N
    for u in cone:
        if u >= n:
            fo[gates[u - n][1]] += 1; fo[gates[u - n][2]] += 1
    stems = [u for u in cone if fo[u] >= 2 and u != out]
    f = len(stems)
    for val in itertools.product((0, 1), repeat=f):
        fixed = dict(zip(stems, val)); ok = True
        memo = {}
        def poss(u, root):
            # set of achievable values of u in its tree; stems are leaves with fixed value
            if u in fixed and not root: return {fixed[u]}
            if u in memo: return memo[u]
            if u < n: r = {0, 1}
            else:
                tt, a, b = gates[u - n]
                r = {(tt >> (2 * p + q)) & 1 for p in poss(a, False) for q in poss(b, False)}
            memo[u] = r; return r
        roots = stems + [out]
        for u in roots:
            want = fixed.get(u, 1)
            if want not in poss(u, True): ok = False; break
        if ok: return True, f
    return False, f
bad = 0; cnt = 0; fs = []
for _ in range(600):
    n = random.randint(2, 6); s = random.randint(1, 9)
    g = rand_circ(n, s)
    r, f = branch(n, g); cnt += 1; fs.append(f)
    if r != brute(n, g): bad += 1
print(json.dumps({"trials": cnt, "mismatches": bad, "max_f": max(fs)}))
json.dump({"trials": cnt, "mismatches": bad, "max_f": max(fs)}, open("results/raw/claude_circuitsat_fanout_branch.json", "w"))
