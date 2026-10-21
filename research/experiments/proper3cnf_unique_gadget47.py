"""Parsimonious proper-3-CNF gate gadgets: every clause has exactly 3 distinct variables,
each gate has exactly one extension on its legal (inputs,output) pair. Runtime << 30s."""
import itertools

def clauses_excluding(vars3, bad):
    # clause over 3 distinct vars excluding exactly assignment `bad`: falsified only at bad
    return [(vars3, bad) for bad in bad]

def sat(cl, asg):
    return all(any(asg[v] != b[i] for i, v in enumerate(vs)) for vs, b in cl)

def gadget(kind):
    """returns (vars, legal-set predicate over vars, clauses). NOT/aux uses canonical aux w=0."""
    if kind in ("AND", "OR", "XOR"):
        f = {"AND": lambda a, b: a & b, "OR": lambda a, b: a | b, "XOR": lambda a, b: a ^ b}[kind]
        vs = ("a", "b", "z")
        bad = [t for t in itertools.product((0, 1), repeat=3) if t[2] != f(t[0], t[1])]
        return vs, [(vs, t) for t in bad]
    vs = ("a", "z", "w")  # NOT with one canonical aux bit w=0
    bad = [t for t in itertools.product((0, 1), repeat=3) if not (t[1] == 1 - t[0] and t[2] == 0)]
    return vs, [(vs, t) for t in bad]

for kind in ("AND", "OR", "XOR", "NOT"):
    vs, cl = gadget(kind)
    sols = [t for t in itertools.product((0, 1), repeat=3) if sat(cl, dict(zip(vs, t)))]
    inputs = 2 if kind != "NOT" else 1
    per_input = {}
    for t in sols:
        per_input[t[:inputs]] = per_input.get(t[:inputs], 0) + 1
    assert len(per_input) == 2 ** inputs and set(per_input.values()) == {1}, (kind, sols)
    print(kind, "clauses", len(cl), "all distinct-3-var; models", len(sols), "one per input: OK")

# whole-circuit check: shared DAG S_i=(S_{i-1}&y_i)|(S_{i-1}&~y_i); NOT gadgets on y_i; count models of full CNF
def full_count(d):
    names = ["x"] + [f"y{i}" for i in range(1, d + 1)]
    cls = []; nv = {}
    def new(n): nv[n] = len(nv); return n
    for n in names: new(n)
    prev = "x"
    for i in range(1, d + 1):
        y = f"y{i}"; ny, w, p, q, s = (new(f"{k}{i}") for k in ("ny", "w", "p", "q", "s"))
        for kind, mp in (("NOT", (y, ny, w)), ("AND", (prev, y, p)), ("AND", (prev, ny, q)), ("OR", (p, q, s))):
            vs, g = gadget(kind)
            m = dict(zip(vs, mp))
            cls += [(tuple(m[v] for v in cv), b) for cv, b in g]
        prev = s
    order = list(nv); n = len(order); inputs = len(names)
    cnt = 0
    for t in itertools.product((0, 1), repeat=n):
        a = dict(zip(order, t))
        if all(any(a[v] != b[i] for i, v in enumerate(vs)) for vs, b in cls): cnt += 1
    return cnt, 2 ** inputs
for d in (1, 2, 3):
    c, e = full_count(d)
    assert c == e, (d, c, e)
    print("shared DAG depth", d, "models", c, "== inputs", e, "OK")
print("PASS")
