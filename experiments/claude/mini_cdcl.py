"""Minimal CDCL SAT solver (2-watched literals, 1UIP learning, VSIDS-like activity,
restarts) that emits a DRUP-style list of learned clauses, plus an independent
naive RUP checker.  Standard library only.  Literals: nonzero ints."""
import heapq


def solve(nvars, clauses, max_conflicts=2_000_000):
    """Return (model_or_None, learned_list, stats). model: list of bool, index 1..n."""
    assign = [0] * (nvars + 1)      # 0 unassigned, 1 true, -1 false
    level = [0] * (nvars + 1)
    reason = [None] * (nvars + 1)
    trail, lim = [], []
    watches = {}
    cls = []
    learned = []
    act = [0.0] * (nvars + 1)
    inc = 1.0
    phase = [-1] * (nvars + 1)

    def val(l):
        a = assign[abs(l)]
        return a if l > 0 else -a

    def enqueue(l, r):
        v = abs(l)
        assign[v] = 1 if l > 0 else -1
        level[v] = len(lim)
        reason[v] = r
        trail.append(l)

    def add_clause(c):
        idx = len(cls)
        cls.append(c)
        if len(c) >= 2:
            watches.setdefault(-c[0], []).append(idx)
            watches.setdefault(-c[1], []).append(idx)
        return idx

    units = []
    for c in clauses:
        c = list(dict.fromkeys(c))
        if len(c) == 0:
            return None, [], {'trivial': True}
        if len(c) == 1:
            units.append(c[0])
        add_clause(c)
    for u in units:
        if val(u) == -1:
            return None, [[]], {'conflicts': 0}
        if val(u) == 0:
            enqueue(u, None)

    qhead = 0

    def propagate():
        nonlocal qhead
        while qhead < len(trail):
            p = trail[qhead]; qhead += 1
            wl = watches.get(p, [])
            i = j = 0
            n = len(wl)
            while i < n:
                ci = wl[i]; i += 1
                c = cls[ci]
                if c[0] == -p:
                    c[0], c[1] = c[1], c[0]
                if val(c[0]) == 1:
                    wl[j] = ci; j += 1
                    continue
                found = False
                for k in range(2, len(c)):
                    if val(c[k]) != -1:
                        c[1], c[k] = c[k], c[1]
                        watches.setdefault(-c[1], []).append(ci)
                        found = True
                        break
                if found:
                    continue
                wl[j] = ci; j += 1
                if val(c[0]) == -1:
                    while i < n:
                        wl[j] = wl[i]; j += 1; i += 1
                    del wl[j:]
                    return ci
                enqueue(c[0], ci)
            del wl[j:]
        return None

    heap = [(0.0, v) for v in range(1, nvars + 1)]
    heapq.heapify(heap)

    def pick():
        while heap:
            a, v = heapq.heappop(heap)
            if assign[v] == 0:
                return v
        return 0

    conflicts = 0
    restart_at = 100
    since = 0
    while True:
        confl = propagate()
        if confl is not None:
            conflicts += 1; since += 1
            if not lim:
                learned.append([])
                return None, learned, {'conflicts': conflicts}
            # 1UIP analysis
            seen = set()
            out = []
            cnt = 0
            p = None
            c = cls[confl]
            idx = len(trail) - 1
            dl = len(lim)
            while True:
                for q in c:
                    if p is not None and q == p:
                        continue
                    v = abs(q)
                    if v not in seen and level[v] > 0:
                        seen.add(v)
                        act[v] += inc
                        if level[v] == dl:
                            cnt += 1
                        else:
                            out.append(q)
                while abs(trail[idx]) not in seen:
                    idx -= 1
                p = trail[idx]
                idx -= 1
                cnt -= 1
                if cnt == 0:
                    break
                c = cls[reason[abs(p)]]
            lc = [-p] + out
            inc *= 1.05
            if inc > 1e100:
                for v in range(1, nvars + 1):
                    act[v] *= 1e-100
                inc *= 1e-100
            bt = max((level[abs(q)] for q in out), default=0)
            # backjump
            while len(lim) > bt:
                start = lim.pop()
                for l in trail[start:]:
                    v = abs(l)
                    phase[v] = assign[v]
                    assign[v] = 0; reason[v] = None
                    heapq.heappush(heap, (-act[v], v))
                del trail[start:]
            qhead = len(trail)
            learned.append(list(lc))
            if len(lc) == 1:
                enqueue(lc[0], None)
            else:
                # put highest-level literal second for watching
                k = max(range(1, len(lc)), key=lambda t: level[abs(lc[t])])
                lc[1], lc[k] = lc[k], lc[1]
                ci = add_clause(lc)
                enqueue(lc[0], ci)
            if conflicts > max_conflicts:
                raise RuntimeError('conflict budget exceeded')
        else:
            if since >= restart_at and lim:
                since = 0
                restart_at = int(restart_at * 1.5)
                start = lim[0]
                for l in trail[start:]:
                    v = abs(l)
                    phase[v] = assign[v]
                    assign[v] = 0; reason[v] = None
                    heapq.heappush(heap, (-act[v], v))
                del trail[start:]
                lim.clear()
                qhead = len(trail)
                # refresh heap priorities
                heap[:] = [(-act[v], v) for v in range(1, nvars + 1) if assign[v] == 0]
                heapq.heapify(heap)
                continue
            v = pick()
            if v == 0:
                return [None] + [assign[i] == 1 for i in range(1, nvars + 1)], learned, {'conflicts': conflicts}
            lim.append(len(trail))
            enqueue(v if phase[v] == 1 else -v, None)


def rup_check(nvars, clauses, lemmas):
    """Independent naive RUP checker: every lemma must follow from formula+previous
    lemmas by unit propagation on its negation; final lemma must be empty.
    Uses simple counter-free repeated scanning with occurrence lists."""
    db = [list(dict.fromkeys(c)) for c in clauses]
    occ = {}
    for i, c in enumerate(db):
        for l in c:
            occ.setdefault(-l, []).append(i)

    def up_conflict(assumps):
        a = {}
        stack = []
        for l in assumps:
            if a.get(abs(l)) == -(1 if l > 0 else -1):
                return True
            a[abs(l)] = 1 if l > 0 else -1
            stack.append(l)
        # also all units of the db
        for c in db:
            if len(c) == 1:
                l = c[0]
                s = a.get(abs(l))
                want = 1 if l > 0 else -1
                if s == -want:
                    return True
                if s is None:
                    a[abs(l)] = want; stack.append(l)
        while stack:
            p = stack.pop()
            for ci in occ.get(p, ()):
                c = db[ci]
                unk = None; sat = False; nunk = 0
                for q in c:
                    s = a.get(abs(q))
                    if s is None:
                        nunk += 1; unk = q
                        if nunk > 1:
                            break
                    elif s == (1 if q > 0 else -1):
                        sat = True; break
                if sat or nunk > 1:
                    continue
                if nunk == 0:
                    return True
                a[abs(unk)] = 1 if unk > 0 else -1
                stack.append(unk)
        return False

    for lem in lemmas:
        if not up_conflict([-l for l in lem]):
            return False, lem
        i = len(db)
        db.append(list(lem))
        for l in lem:
            occ.setdefault(-l, []).append(i)
    return (len(lemmas) > 0 and lemmas[-1] == []), None
