# TMR-5/100: paid SAT witness routing, intrinsic T5 easy controls, and selector-profile firewall

**Status:** PROVED for restricted structural and conditional machine-model claims; OPEN for unrestricted SAT-witness lower bounds. Date 2026-11-18 America/Los_Angeles. Independent TMR-5 red-team result, keeping other agents and their files unchanged.

## 1. New decision-to-witness cost audit

Under an **authenticated, explicitly covered** layout with (R\le n^{.195+o(1)}) rows, (B\le n^{.65+o(1)}) blocks **per row**, and encoded child size (b\le n^{.35+o(1)}), with disjoint private variables conditional on each shared assignment (z), a per-block deterministic **decision** seed of runtime (D(b)=b^{t+o(1)}) gives the specified sequential scanning *upper bound* (n^{.845+.35t+o(1)}), in addition to charged parsing, materialization, verification and row generation. For the target exponent 1.33 this accounting requires (t\le97/70\approx1.385714). An unspecified polynomial seed does not establish the bound.

Crucially, an ordinary decision-only seed does **not** return the private witnesses (y_i). The standard black-box SAT self-reduction can ask up to (b) adaptive seed questions per block, giving worst-case upper bound (n^{1.195+.35t+o(1)}) for this specific method, already (n^{1.545+o(1)}) at (t=1). This is not an unrestricted lower bound: a witness-producing seed or source-aware extraction may do better. The nominal live-space condition (n^{.35s}\le n^{.5}) gives (s\le10/7), subject to all ancillary buffers, replay and verification also fitting.

## 2. Quantifiers, polarities and source soundness

For (F(z,y)=\bigwedge_i F_i(z,y_i)),
[
\operatorname{SAT}(F)\iff\exists z\,\forall i\,\exists y_i F_i(z,y_i),\qquad
\operatorname{UNSAT}(F)\iff\forall z\,\exists i\,\forall y_i\,\neg F_i(z,y_i).
]
A SAT output must include an independently verified shared row plus all child witnesses. An UNSAT output must cover every relevant (z) and source-certify each chosen negative child. A bare bad-block index is not a refutation. Free answer polarity or a favorable existential path is not a uniform sound specialist. Polynomially long, polynomial-time checkable UNSAT certificates for **all** CNFs would imply NP=coNP, a currently open collapse.

For any uniform (V(F,p)\in\{\mathsf{SAT},\mathsf{UNSAT},\mathsf{UNKNOWN}\}) with *all* decisive paths sound, at least one decisive path on every input, and every path bounded by charged time (T), space (S), and (k) supplied bits, complete deterministic enumeration costs (O(2^k(T+n+k))) time and (O(S+k+\log n)) workspace. Buss-Williams (2015), Fig. 8.2, rules out total deterministic general SAT in (\operatorname{DTISP}(n^{1.34070},n^{.5})) in its random-access model. Thus (T=n^{1.33+o(1)},S=n^{.5+o(1)}) and (k\le(.01060-\delta)\log_2 n) on every input cannot coexist under these hypotheses. This does not constrain an unchecked one-bit oracle polarity, ordinary nondeterministic SAT witness verification, or an uncharged alternating strategy.

At time exponent 1.33, the FLMV 2005 deterministic time-space cutoff is about .279104 and its **co-nondeterministic** cutoff about .089300, neither excluding space exponent .5. The latter does not apply to nondeterministic SAT witnesses. Transfer to T5 or critical-deletion promise instances requires a source-preserving efficient reduction.

## 3. New constructive T5 theorem: oriented pseudoforests

Every oriented graph whose underlying undirected simple graph is a pseudoforest has a T5-homomorphism constructible in (O(n+m)) time and (O(n+m)) space. For a traversed cycle edge let (\epsilon\in\{0,1\}) mark whether its direction is backward; a valid color increment is (1+\epsilon+2t\pmod5), (t\in\{0,1\}). A length-\(\ell\) cycle with (q) backward arcs closes if (\ell+q+2\sum t_i=0\pmod5). For \(\ell\ge4\), the first four bits cover all five residues; for \(\ell=3\), every \(q\in\{0,1,2,3\}\) has a closing choice. Extend the resulting cycle coloring into the attached trees using forward +1 / backward -1, or color trees directly.

The bound on undirected cycle rank is sharp for the *existence of UNSAT examples*: a native five-vertex six-arc oriented \(K_{2,3}\) has cycle rank two, is UNSAT, and becomes SAT after deleting any arc. This does not establish that larger-cycle-rank instances are computationally hard.

## 4. New connected exponential-profile false positive

Join \(m\) copies of that six-arc \(K_{2,3}\) obstruction at a single common terminal; retain all other vertices distinct. This creates a **connected** UNSAT native T5 graph with \(4m+1\) vertices, \(6m\) arcs. Each module has two private blocks. For shared endpoint difference \(d\) mod 5, the failing-block sets are \(\{0,1\}\) at \(d=0\), \(\{0\}\) at \(d=1,3,4\), and \(\{1\}\) at \(d=2\). Thus there are \(5^m\) relative-boundary orbits and exactly **\(3^m\)** different failure-mask profiles. Nevertheless a source-aware procedure parses the promised construction in \(O(m)\) time and certifies UNSAT from its first constant-sized obstruction. No expensive profile enumeration is necessary. For \(m>1\), these graphs are **not edge-minimal UNSAT** and are expressly **not** proposed as intrinsically critical-hard families.

## 5. Independent reproduction and dependency verdict

The full standard-library verifier executed 24,654 checks, zero assertion failures: all \(5^m\) relative-boundary rows for \(1\le m\le6\); 4,088 complete orientations of cycles of lengths 3-11; 504 randomly generated oriented pseudoforests with explicit color witnesses and source validation; the five native interface residues and six edge-deletion controls; and exact exponent arithmetic. Largest joined control: 25 vertices, 36 arcs, 15,625 boundary orbits, 729 failure profiles. Full executed evidence and reproducibility package: TMR5_100_machine_witness_evidence.zip (conversation attachment). Raw results SHA256: `abf2ea368963dc4bfce54174b3d37af84e292a32d9b8b6523e8fc1e330a112b0`.

**PROVED:** structural T5 pseudoforest witness theorem; joined-family profile counts and easy refutation; quantified soundness, conditional path-enumeration bound.

**FALSIFIED:** large selector-profile information implies necessary T5 decision work; a naive decision-only SAT self-reduction automatically meets the proposed 1.33 time accounting; an unverified free correct-polarity bit is a deterministic algorithm.

**OPEN:** a hereditary source-authenticated arbitrary-CNF splitter with checked coverage of all z, complete negative-child proofs, and a time/space-charged witness extractor; unrestricted time lower bounds; P versus NP.

**Next blocker:** source-preserving arbitrary-CNF splitters must pay for both polarities and all adaptive children, while demonstrating witness extraction rather than decision-only calls.

**Primary sources:** Buss and Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, *Computational Complexity* 24 (2015), 533-600, DOI [10.1007/s00037-015-0104-9](https://doi.org/10.1007/s00037-015-0104-9), Fig. 8.2. Fortnow, Lipton, van Melkebeek, Viglas, *Time-space lower bounds for satisfiability*, *JACM* 52 (2005), DOI [10.1145/1101821.1101822](https://doi.org/10.1145/1101821.1101822), Thms 5.7 and 6.4.
