"""Exhaustive check of the restriction/literal-substitution step (Krajicek decency D1+D4)
for the clause-selector encoding sat_n(y,x,t) used in the reflection formula.
Variables: y[j,l] selects literal l in slot j; t[j,l] auxiliary; x[i] assignment.
sat clauses: OR_l t[j,l];  (-t[j,l] v y[j,l]);  (-t[j,l] v lit_l(x)).
Claims checked for every F (all m-slot formulas over n vars, each slot a nonempty set
of <=3 literals):
 (a) [tautological slots of F are deleted, as resolution ignores them]
     restriction y:=F, t[j,l]:=0 (unselected), t[j,l]:=lit_l (selected), followed by
     deletion of satisfied/tautological clauses, yields exactly the non-tautological clause set of F;
 (b) for every x: exists t with sat(F,x,t)=1  iff  x satisfies F.
Deterministic, no seed. Pure Python."""
import itertools, json, time, sys
n, m = int(sys.argv[1]) if len(sys.argv) > 1 else 3, int(sys.argv[2]) if len(sys.argv) > 2 else 2
lits = [(i, s) for i in range(n) for s in (1, -1)]           # literal = (var, sign)
slots = [frozenset(c) for k in (1, 2, 3) for c in itertools.combinations(lits, k)]
def sat_clauses():
    C = []
    for j in range(m):
        C.append([('t', j, l, 1) for l in lits])
        for l in lits:
            C.append([('t', j, l, -1), ('y', j, l, 1)])
            C.append([('t', j, l, -1), ('x', l[0], None, l[1])])
    return C
SAT = sat_clauses()
def restrict(F):
    out = set()
    for cl in SAT:
        new, done = set(), False
        for (kind, a, b, s) in cl:
            if kind == 'y':
                val = (b in F[a]); 
                if (val and s == 1) or (not val and s == -1): done = True; break
            elif kind == 't':
                if b in F[a]:  # t := literal b, sign s
                    new.add((b[0], b[1] * s))
                else:          # t := 0
                    if s == -1: done = True; break
            else:
                new.add((a, s))
        if done: continue
        if any((v, -sg) in new for (v, sg) in new): continue  # tautology
        out.add(frozenset(new))
    return out
t0 = time.time(); count = fails = syn_fail = sem_fail = 0; sem = 0
for F in itertools.product(slots, repeat=m):
    count += 1
    proper = {c for c in F if not any((v, -sg) in c for (v, sg) in c)}
    if restrict(F) != proper: fails += 1; syn_fail += 1
    for x in itertools.product((0, 1), repeat=n):
        satF = all(any((x[v] == 1) == (sg == 1) for (v, sg) in c) for c in F)
        # exists t: each slot needs some selected literal true (t=1 forces y=1 and lit true)
        ex = all(any(l in F[j] and ((x[l[0]] == 1) == (l[1] == 1)) for l in lits) for j in range(m))
        sem += 1
        if satF != ex: fails += 1; sem_fail += 1
res = dict(n=n, m=m, formulas=count, semantic_checks=sem, failures=fails, syntactic_failures=syn_fail, semantic_failures=sem_fail,
           seconds=round(time.time() - t0, 2), python=sys.version.split()[0])
print(json.dumps(res))
