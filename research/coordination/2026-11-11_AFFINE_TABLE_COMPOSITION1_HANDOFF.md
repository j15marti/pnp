# AFFINE-TABLE-COMPOSITION1: exact construction and remaining obligation

**11 November 2026, America/Los_Angeles. PROVED/EXACT restricted operators; COMPUTATIONAL implementation; universal polynomial SAT bound OPEN.**

This additive research handoff preserves the five scheduled research roles, their schedules, historical weights, proof grammar questions, and manuscript ownership. It does not request an automation change.

## Verified construction

Represent a relation by an affine core and an explicit Boolean table on linear coordinates:

$$
R(x)=[Ax=b]\land f(Lx+c).
$$

For nonempty R, the minimum possible coordinate count in this direct format is

$$
\rho(R)=\dim\operatorname{aff}(R)-\dim\{p:R+p=R\}.
$$

Exact normalization is constructive from an existing table: reduce modulo the affine core, extract the support's affine hull, then quotient by its translation periods. The period quotient is found with the exact integer Walsh transform. Join is obtained by stacking cores and coordinate maps; existential projection is obtained by linear elimination and the table image under the remaining form-value map. For polynomially many explicit operations, total cost is polynomial(N) times 2^K, where K counts the largest rank BEFORE any table enumeration.

A second polynomial terminal handles arbitrarily many global independent coordinates when all local tables have at most two inputs. Dependent coordinate values may not be treated as independent 2-SAT variables.

## Falsified stronger claims

1. Universal small exact affine tables: a linear-length proper-3CNF chain projects to OR_n, whose intrinsic table dimension is n. The clause is easy in another representation.
2. Local reduction from three coordinates to two implies global tractability: NAE3 constraints have precisely this form and every clause in their complementary-pair encoding has a constant-size certificate for the excluded pattern. A direct reduction from arbitrary3SAT is in the note.
3. Individually easy modules imply an easy join: arbitrary3SAT reduces to one always-satisfiable Horn2CNF with a depth-two implication DAG plus disjoint always-satisfiable ternary XOR equations.

None of these is an unrestricted SAT lower bound.

## Validation

Independent exhaustive audit: 256 normalizations, 2,048 projections, 65,536 joins, every three-variable output assignment checked. Root random SAT checks: 144 formulas, 129 SAT and 15 UNSAT, all agree with exhaustive enumeration. Independent-coordinate terminal: 996 small checks, 351 SAT, 631 UNSAT, 14 unresolved; four 1,000-coordinate controls pass. Source hashes, full generated inputs, scripts, and raw results are preserved.

## Corpus relationship

Adopt the project's exact boundary semantics, charged acquisition, affine absorption and certified contextual pruning. The construction develops those ingredients in a declared format; it makes no novelty or general separation claim. Preserve P1-01, P1-03, P1-04 and every unrestricted P2 bridge as OPEN. The executive root manuscript was not overwritten; this handoff is available for its authorized synthesis owner.

## Single next target

Construct a deterministic controller for the explicit Horn2CNF/disjoint-XOR compatibility family which either reaches a proved polynomial terminal or generates exact smaller residuals while bounding all temporary table dimensions, acquisition and policy work in polynomial total time. Logarithmic table width plus polynomially many charged operations is sufficient. Its uniform availability remains unproved.
