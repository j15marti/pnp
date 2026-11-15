"""Finite controls for CLAUDE B3-REFLECTION-0001.
Checks the propositional rejection-soundness statement RS_{Q_A} on all CNFs
over a small clause universe for (a) a correct decider, (b) a buggy decider,
(c) a Goedel-style wrapper around a toy proof checker (consistent / forged).
Exhaustive, < 5 s. COMPUTATIONAL only: these are tautology checks by brute
force, not EF proofs and not evidence about asymptotic proof size."""
import itertools, json, sys

V = 3
LITS = [l for v in range(1, V + 1) for l in (v, -v)]
# clause universe: all nonempty clauses of width <=2 over 3 vars without complementary pairs
UNIV = []
for w in (1, 2):
    for c in itertools.combinations(LITS, w):
        if len({abs(l) for l in c}) == w:
            UNIV.append(c)
ASSIGN = list(itertools.product((0, 1), repeat=V))

def sat_by(F, a):
    return all(any((a[abs(l) - 1] == 1) == (l > 0) for l in c) for c in F)

def dpll(F, steps):
    steps[0] += 1
    if not F: return True
    if any(len(c) == 0 for c in F): return False
    l = F[0][0]
    for lit in (l, -l):
        G = [tuple(x for x in c if x != -lit) for c in F if lit not in c]
        if dpll(G, steps): return True
    return False

def A_correct(F):
    s = [0]; r = dpll(list(F), s); return ("SAT" if r else "UNSAT"), s[0]

def A_buggy(F):
    # rejects every formula with exactly 4 clauses: unsound on SAT inputs
    if len(F) == 4: return "UNSAT", 1
    return A_correct(F)

def check_RS(A, maxm):
    """RS_{Q_A}: for all F (|F|<=maxm) and all assignments a: not(A(F)=UNSAT and a |= F)."""
    checked = 0; viol = None
    for m in range(0, maxm + 1):
        for F in itertools.combinations(UNIV, m):
            out, _ = A(F)
            for a in ASSIGN:
                checked += 1
                if out == "UNSAT" and sat_by(F, a):
                    viol = viol or {"F": F, "a": a}
    return checked, viol

# toy theory T: proofs are bitstrings; Prf_T(p, 0=1) iff p in BAD (empty = consistent)
def make_wrapper(BAD):
    # A_T: inputs are pairs (F, p). If p is a T-proof of 0=1, output UNSAT on the
    # fixed SAT marker F0 = ((1,),). Otherwise run A_correct.
    def A(Fp):
        F, p = Fp
        if p in BAD and F == ((1,),): return "UNSAT", 1
        return A_correct(F)
    return A

def check_wrapper(BAD, plen=3):
    checked = 0; viol = None
    for p in ("".join(b) for b in itertools.product("01", repeat=plen)):
        for m in range(0, 3):
            for F in itertools.combinations(UNIV, m):
                out, _ = make_wrapper(BAD)((F, p))
                for a in ASSIGN:
                    checked += 1
                    if out == "UNSAT" and sat_by(F, a):
                        viol = viol or {"F": F, "p": p, "a": a}
    return checked, viol

res = {}
c, v = check_RS(A_correct, 4); res["RS_correct"] = {"checks": c, "violation": v}
c, v = check_RS(A_buggy, 4); res["RS_buggy"] = {"checks": c, "violation": v}
c, v = check_wrapper(set()); res["wrapper_consistent"] = {"checks": c, "violation": v}
c, v = check_wrapper({"101"}); res["wrapper_forged_contradiction"] = {"checks": c, "violation": v}
# malformed-input control: a clause with a zero literal must be rejected by the parser
def parse(cl):
    if any(l == 0 or abs(l) > V for l in cl): raise ValueError("malformed")
    return cl
mal = 0
for bad in [(0,), (4,), (1, 0), (-5, 2)]:
    try: parse(bad)
    except ValueError: mal += 1
res["malformed_rejected"] = mal
res["universe_size"] = len(UNIV)
assert res["RS_correct"]["violation"] is None
assert res["RS_buggy"]["violation"] is not None
assert res["wrapper_consistent"]["violation"] is None
assert res["wrapper_forged_contradiction"]["violation"] is not None
assert mal == 4
json.dump(res, sys.stdout, indent=1, default=list)
