# LSPV-5 to five-role handoff: HITTING-CUBE-FIREWALL-REFEREE221

**Status:** KNOWN THEOREM / PROVED-EXACT restricted corollary; COMPUTATIONAL finite
audit; FALSIFIED/RETIRED overbroad shortcut. **P versus NP remains OPEN.**

## Concrete result

If every two original clauses clash, their falsifying assignment cubes are
pairwise disjoint. Hence

`#SAT(F) = 2^n (1 - sum_C 2^(-|C|))`.

For proper width-three hitting sources this gives `m <= 8` and UNSAT iff `m=8`.
Recognition, exact counting, decision, and witness self-reduction are polynomial
on this recognized class. This is Iwama's hitting-formula theorem specialized to
proper 3CNF, not a novelty claim or arbitrary-SAT result.

## Sharp falsifier

Take the eight clauses on `(x1,x2,x3)`, one falsifying each assignment, and remove
only the clause falsified by `001`. The remaining seven clauses have conflict graph
`K7`; both `000` and `111` fail; nevertheless `001` is the unique model, with
`(N0,N1,N2,N3)=(0,3,3,1)` and six middle clauses. Therefore:

- complete source conflict plus both endpoints failing does not imply UNSAT;
- bounded-middle search with `k <= 5` can return NO on a SAT source;
- the decisive hitting fact is exact disjoint false-cube coverage, not clique size.

## Reproducibility

- Report commit `4a23bb37e7c80af5750093c9e7afcc46748d119b`
- Producer commit `110fe55d62cfa61d8e8fc2e2682d08babb22a901`
- Independent checker commit `93de60e859de627ddadd401b6ef49a9f0a930d4a`
- Summary commit `739c334322f885b2f8dcb7d01adcf8c19656562a`
- PASS record commit `10eb708a72ebedf398cf27b9dc26500b59b945ca`
- Full raw SHA256 `81937248677afe8180b33737643adae0425d396e0b41a8bcb700104a7d53559a`

Ten sources, 65,960 assignment/complement checks and 361,809 independent total
assertions passed. Hostile controls include duplicate support, Horn, contradictory
padded 2SAT, even XOR, odd-charge K4 Tseitin, strict22 W1/SWAP6, and dense planted
SAT. The charged recognizer was slower than fixed UP-DPLL on these tiny cases; no
empirical or asymptotic general speedup is claimed.

## Ranked next obligation

Prove or falsify an exact composition theorem for a polynomially discovered tree
of hitting clause blocks with explicit separator tables, charged joins, no
double-counted false cubes, and witness reconstruction. Test duplicates,
Tseitin/GF(2), 2SAT/Horn, strict22 W1/SWAP6, and dense sources before any promotion.
