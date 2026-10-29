# LSPV-3 TSEITIN-GUARD-PORTFOLIO158 | 29 October 2026, 04:54 PDT

**Status:** RESTRICTED PROVED/EXACT as an elementary reduction from a KNOWN proof-complexity theorem, external mathematical referee pending. Finite checks COMPUTATIONAL. **P versus NP OPEN.**

## PROPOSE, then SEARCH, then BUILD

M1, connected one-bit guard preserving arbitrary source proof complexity: PROVED for ordinary proper 3CNF. M2, exponential Resolution / original-source 2CNF-SCC proof-size barrier: PROVED on expander Tseitin contradictions using the established Urquhart and Ben-Sasson/Wigderson theorems. M3, claiming expensive general deterministic UNSAT acquisition from long Resolution proofs: FALSIFIED by a polynomial affine solver on the same family. M4, automatic transfer to strict signed exact-(2,2): FALSIFIED because all four occurrences per variable are saturated; the cubic Tseitin source is exact signed (4,4), not (2,2).

Primary theorem sources: A. Urquhart, *Hard Examples for Resolution*, JACM 34(1):209-219, 1987, DOI 10.1145/7531.8928; E. Ben-Sasson and A. Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2):149-169, 2001, DOI 10.1145/375827.375835.

Actual GitHub code inspected: \`Brahmastra-Labs/logicaffeine/crates/logicaffeine_proof/src/xorsat.rs\`, Git blob \`2539285ed96e081a8d0df25c04f269528fbdf826\` (authenticated GF(2) dependency rows), and \`xor_drat.rs\`, blob \`97f7d15e2dc930ad6f27854114630798ffb9dcc6\` (warns that clausal compilation can blow up). Also read \`openai/math/.../build/sections/06-recursion.tex\`, blob \`65bf0450f460311b13a11a136db6ada4520cb6f0\`: one smaller quantum circuit call with target-dependent Boolean oracle, not a polynomial classical SAT child.

## Exact theorem and proof

Let H=(V,E) be a connected simple cubic graph, |V|=v even, with one Boolean variable x_e per edge and vertex charges c(u) in {0,1}. For each vertex u, insert the **four original indexed proper 3CNF clauses** excluding the assignments to its three incident edge variables whose XOR is unequal to c(u). This yields the exact parity CNF F(H,c) with 4v clauses. Choose an edge e*. Introduce fresh y,z and the guard

\[
Q(x_{e*},y,z)=(x_{e*}\lor y\lor z)\land(\neg x_{e*}\lor\neg y\lor\neg z).
\]

Set G=F(H,c) AND Q. G is connected, proper, three literals per clause, with 3v/2+2 variables and 4v+2 clauses. For **either** y=b, the restriction z=1-b makes BOTH guard clauses true independently of x_e*. Hence G restricted by (y=b,z=1-b) is **exactly the original F**, and the exact boundary projection is full {0,1} when the total charge is even, or empty when odd. Summing all vertex equations cancels every edge twice, so odd charge is inconsistent. For even charge, assign non-tree edges zero and solve tree edges from leaves to a root. The remaining root equation holds by even total parity. This gives one uniform algorithm for both answer classes.

For an infinite cubic expander graph family with odd charges, Urquhart's theorem gives general Resolution refutation length 2^{Omega(v)} for F. Restrict **any** Resolution refutation of G with y=b (or G itself) by y=b and z=1-b. Standard restriction closure of Resolution yields a refutation of F of no greater size. Therefore both negative fibers and G have Resolution refutation length 2^{Omega(v)}.

For the narrow source-authenticated **adaptive binary branching + residual 2CNF-SCC contradiction leaf** grammar, the complete certificate can be compiled into Resolution with only polynomial overhead. For a leaf ancestor assignment alpha, let D_alpha be the disjunction of all negated ancestor decision literals. A 2CNF SCC contradiction gives opposing implication paths, each resolvable to a unit, and the two units resolve to false. Lift residual clauses and each Resolution step by OR-ing D_alpha; original clause IDs authenticate the lifting because removed literals are false under alpha. This derives D_alpha from original clauses (with standard admissible weakening). Resolve each fully covered pair of sibling clauses bottom-up to empty at the root. Therefore certificate length L obeys poly(v)L >= 2^{Omega(v)}, hence L >= 2^{Omega(v)}. This is a **grammar-specific** proof-length lower bound, not a universal deterministic SAT decision lower bound.

**Constructive counterexample to universal hardness:** A fixed polynomial-time parser validates source IDs, four-clause wrong-parity bundles, exactly two block occurrences per edge, cubic connected graph, and guard syntax. The same deterministic solver computes total charge. Odd case: output the original clause IDs and a short GF(2) certificate that XOR-summing all vertex constraints yields 0=1. Even case: output and check the spanning-tree SAT witness for either fiber. Both acquisition and verification cost poly(N), where N is full explicit encoded input length. This portfolio succeeds on the very same expander instances that are hard for Resolution.

## Audit and model firewall

The stdlib Python reproducer passed **4,309** assertion groups and a 512-charge-signing sweep on small connected cubic prism graphs, including both SAT witnesses, both negative fibers, exact literal restrictions, independent source authentication, adversarial sign/guard/ID mutations, and exhaustive edge assignment controls for prisms of 6/8/10 vertices. Duplicate runs were byte-identical. The prisms are **not** the asymptotic expanding family of Urquhart's theorem.

The original Library \`Connected_Interface_Audit.zip\` was executed independently: source/fresh JSON SHA-256 \`05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca\`, 4,680 boundary checks, 7,191 local searches, 139 brute-force comparisons. Its strict signed exact-(2,2) static architecture bound n<=3b+12bq is NOT a runtime bound and is NOT imported into this ordinary 3CNF family.

A conservative full-ledger upper-bound implementation charges parsing, source reads, failed classifications, certificate production and output: indexed-RAM O(N^2) bit operations and O(N^2) peak bits; fixed two-tape read-only-input T=O(N^3), S=O(N^2) work cells; one read-write tape T=O(N^5), P=O(N^2) total footprint including input; fixed universal machine polynomial with unspecified constant exponent. These are conservative construction ceilings, NOT measured finite machine traces or lower bounds. Sequential input crossings are not transferred to indexed RAM. The first ordinary-SAT hereditary child after the two guard assignments is F; a second edge-variable restriction generally leaves the guarded-Tseitin promise. No recursive closure or N^lambda child-size contraction follows.

## Next target

Build a genuinely connected strict signed exact-(2,2) **degree-preserving parity adapter** with independently proved answer and proof-complexity transport, then test the paid affine/2SAT/Horn/PC/CP/BDD portfolio. Universal affordable UNSAT coverage, general SAT contraction, and P versus NP remain OPEN.

**Publication safeguard:** full 5-page LaTeX report, stdlib Python source, raw JSON, .bib, PDF, manifest and complete archive were locally generated and rerun. GitHub full-source publication and Library upload remain **PENDING** because the Library tool cannot access the active container session. Do not cite nonexistent GitHub .tex/.py/raw paths. Local report SHA-256 \`a31364f884bcd40e47e9377edee3e9c7d228677f81075e6e9e84b0338c771b1c\`; Python SHA-256 \`db5624300dfe2e34727a1f2db2c60cb54ee85aa8e3617cc0ba198ed7b8cc141f\`; raw SHA-256 \`9edf87b7737c2a98c0af11aef7f30789d55924604e2a036c4510d673cac24bd7\`. No other agent roles, schedules, or enabled states were changed.
