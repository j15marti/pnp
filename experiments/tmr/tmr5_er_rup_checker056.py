#!/usr/bin/env python3
"""TMR-5/WR056 independent checker for extension+RUP refutations.

Revision: tmr5-er-rup-checker056.v1 (deterministic).

Independently of the producer it
  (1) regenerates BPHP^{n+1}_n from k with its own indexing code and
      requires the shipped formula to equal it as a clause multiset;
  (2) for every extension step requires the variable to be fresh (never
      seen in F or any earlier line), every clause to contain v or -v, and
      the definition to be CONSERVATIVE: for every assignment of the other
      variables occurring in the step there is a value of v satisfying all
      its clauses (brute force).  Conservative extension preserves
      satisfiability, so it is sound for refutations;
  (3) for every addition checks RUP (unit propagation of the negated clause
      against the current database reaches a conflict) and counts the
      propagations, an upper bound on the length of the trivial resolution
      derivation of that clause (Beame-Kautz-Sabharwal 2004);
  (4) for every deletion requires the clause to be present;
  (5) requires the empty clause to be the last added line.
"""
import json, sys, itertools, time
from collections import Counter, defaultdict

REV = "tmr5-er-rup-checker056.v1"


def regen(k):
    n = 2 ** k
    out = []
    for p1 in range(n + 1):
        for p2 in range(p1 + 1, n + 1):
            for hole in range(n):
                cl = []
                for bit in range(k):
                    val = (hole // 2 ** (k - 1 - bit)) % 2
                    for p in (p1, p2):
                        var = p * k + bit + 1
                        cl.append(-var if val else var)
                out.append(tuple(sorted(cl)))
    return out


class DB:
    def __init__(self):
        self.cl = {}
        self.occ = defaultdict(set)
        self.key = defaultdict(list)
        self.nid = 0
        self.short = set()

    def add(self, c):
        c = tuple(sorted(set(c)))
        cid = self.nid
        self.nid += 1
        self.cl[cid] = c
        for l in c:
            self.occ[l].add(cid)
        self.key[c].append(cid)
        if len(c) <= 1:
            self.short.add(cid)

    def delete(self, c):
        c = tuple(sorted(set(c)))
        ids = self.key.get(c)
        if not ids:
            return False
        cid = ids.pop()
        for l in self.cl[cid]:
            self.occ[l].discard(cid)
        del self.cl[cid]
        self.short.discard(cid)
        return True

    def rup(self, c):
        val = {}
        queue = []
        for l in c:
            if val.get(-l) is True:
                return True, 0  # tautology / complementary assumption
            val[-l] = True
            val[l] = False
            queue.append(-l)
        # conflict with an existing empty or all-false clause
        props = 0
        # initial pass over short clauses (empty and unit) only; every longer
        # clause is reached through the occurrence lists of assigned literals
        for cid in list(self.short):
            cc = self.cl[cid]
            st = self._status(cc, val)
            if st == "conflict":
                return True, props
            if isinstance(st, int):
                if val.get(st) is None:
                    val[st] = True
                    val[-st] = False
                    queue.append(st)
                    props += 1
        qi = 0
        while qi < len(queue):
            lit = queue[qi]
            qi += 1
            for cid in list(self.occ.get(-lit, ())):
                st = self._status(self.cl[cid], val)
                if st == "conflict":
                    return True, props
                if isinstance(st, int) and val.get(st) is None:
                    val[st] = True
                    val[-st] = False
                    queue.append(st)
                    props += 1
        return False, props

    @staticmethod
    def _status(cc, val):
        unassigned = None
        nun = 0
        for l in cc:
            v = val.get(l)
            if v is True:
                return "sat"
            if v is None:
                nun += 1
                unassigned = l
                if nun > 1:
                    return "open"
        if nun == 0:
            return "conflict"
        return unassigned


def conservative(v, cls):
    others = sorted({abs(l) for c in cls for l in c} - {v})
    for bits in itertools.product((False, True), repeat=len(others)):
        a = dict(zip(others, bits))
        ok_any = False
        for vv in (False, True):
            a[v] = vv
            if all(any(a[abs(l)] == (l > 0) for l in c) for c in cls):
                ok_any = True
                break
        if not ok_any:
            return False
    return True


def check(path):
    t0 = time.time()
    pr = json.load(open(path))
    k = pr["k"]
    res = {"k": k, "revision": REV, "file": path}
    F = [tuple(sorted(c)) for c in pr["F"]]
    res["formula_matches_independent_regeneration"] = Counter(F) == Counter(regen(k))
    seen = {abs(l) for c in F for l in c}
    db = DB()
    for c in F:
        db.add(c)
    nfail = 0
    nrup = next_ = nprop = maxprop = 0
    last_add = None
    for st in pr["steps"]:
        if st["t"] == "e":
            v = st["v"]
            ok = v not in seen and all((v in c) or (-v in c) for c in st["c"]) \
                and conservative(v, st["c"])
            if not ok:
                nfail += 1
            for c in st["c"]:
                seen |= {abs(l) for l in c}
                db.add(c)
            next_ += 1
        elif st["t"] == "a":
            c = st["c"]
            if any(abs(l) not in seen for l in c):
                nfail += 1
            ok, pp = db.rup(c)
            nprop += pp + 1
            maxprop = max(maxprop, pp)
            if not ok:
                nfail += 1
            db.add(c)
            nrup += 1
            last_add = c
        elif st["t"] == "d":
            if not db.delete(st["c"]):
                nfail += 1
        else:
            nfail += 1
    res.update({"extension_steps_checked": next_, "rup_steps_checked": nrup,
                "failures": nfail, "empty_clause_last": last_add == [],
                "trivial_resolution_steps_upper_bound": nprop,
                "max_propagations_one_lemma": maxprop,
                "PASS": nfail == 0 and last_add == [] and
                res["formula_matches_independent_regeneration"],
                "seconds": round(time.time() - t0, 3)})
    return res


def brute_unsat(k):
    F = regen(k)
    nv = (2 ** k + 1) * k
    for bits in itertools.product((False, True), repeat=nv):
        if all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in F):
            return False
    return True




def corruption_controls(path):
    """Each mutated proof must be REJECTED; returns {name: rejected?}."""
    import copy, os, tempfile
    base = json.load(open(path))
    muts = {}
    s = base["steps"]
    adds = [i for i, t in enumerate(s) if t["t"] == "a" and t["c"]]
    exts = [i for i, t in enumerate(s) if t["t"] == "e"]
    # 1. drop the first nonempty RUP lemma that is later needed (try several)
    m = copy.deepcopy(base); del m["steps"][adds[0]]; muts["drop_first_lemma"] = m
    # 2. remove the final empty clause
    m = copy.deepcopy(base); m["steps"] = [t for t in m["steps"] if not (t["t"] == "a" and t["c"] == [])]
    muts["no_empty_clause"] = m
    # 3. extension reusing an existing (non-fresh) variable
    m = copy.deepcopy(base); e = m["steps"][exts[0]]; old = e["v"]
    e["v"] = 1; e["c"] = [[(1 if l == old else -1 if l == -old else l) for l in c] for c in e["c"]]
    muts["nonfresh_extension"] = m
    # 4. non-conservative extension: add clause (v) and (-v)
    m = copy.deepcopy(base); m["steps"][exts[0]]["c"] += [[m["steps"][exts[0]]["v"]], [-m["steps"][exts[0]]["v"]]]
    muts["nonconservative_extension"] = m
    # 5. drop one source clause of F
    m = copy.deepcopy(base); m["F"] = m["F"][1:]; muts["drop_source_clause"] = m
    # 6. replace a hole lemma by a stronger unit clause
    m = copy.deepcopy(base); m["steps"][adds[-2]]["c"] = m["steps"][adds[-2]]["c"][:1]; muts["strengthen_lemma"] = m
    out = {}
    d = tempfile.mkdtemp()
    for name, mm in muts.items():
        fp = os.path.join(d, name + ".json")
        json.dump(mm, open(fp, "w"))
        r = check(fp)
        out[name] = {"rejected": not r["PASS"], "failures": r["failures"],
                     "formula_match": r["formula_matches_independent_regeneration"]}
    return out


if __name__ == "__main__":
    out = {"checks": [check(p) for p in sys.argv[1:]],
           "brute_force_unsat": {"k1": brute_unsat(1), "k2": brute_unsat(2)},
           "corruption_controls_on_smallest_k_file": corruption_controls(
               min(sys.argv[1:], key=lambda f: json.load(open(f))["k"]))}
    print(json.dumps(out, indent=1))
