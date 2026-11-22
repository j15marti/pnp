# Additional forbidden regions for T5 and compact T_q

22 November 2026, America/Los_Angeles.

Status: published-theorem transfers and a deterministic streaming consequence of the verified pin gadgets. These are fixed polynomial or interface-restricted exclusions. P versus NP remains open. No historical novelty or independent formal verification is claimed.

## 1. Target and conventions

Q is the compact regular-tournament language already defined in the project: the input contains a binary B and a circuit describing canonical edges of a B-vertex base tournament; a fixed interpreter completes it to a regular tournament on q=2B+1 vertices. The question is whether some x satisfies R(x,0,1) AND R(2B,x,B). N is the full compact encoded length.

Transfers from SAT use the previously established locally computable reduction: quasilinear output length, polylogarithmic time per requested output bit, logarithmic workspace, and no full-output materialization. Mere polynomial-time NP-completeness would not suffice. This note relies on that reduction and does not claim a new independent audit of its local Cook-Levin source encoding.

For auxiliary cumulative memory C, use the preceding note's small-initial-workspace, bounded-growth model, compatible with deterministic random-access Turing machines up to polylogarithmic time and peak-space overhead. Charge at least one bit per elapsed step, include all preprocessing, and allow at most polylog(N) additional usable workspace bits per charged step. Then

$$
T\le C,\qquad S_{\max}\le\widetilde O(1+\sqrt C).
$$

The second bound comes from the area required to build a memory peak. It is not C>=T*S. Input initially supplied as free writable auxiliary storage violates the small-initial-workspace premise. Read-only input is excluded from auxiliary C and S.

## 2. A stronger standalone auxiliary-CM exclusion

Williams's corrected author manuscript, Table I on manuscript page A:18 (PDF page 18), lists a simultaneous SAT exclusion at time n^1.24 and workspace n^0.666 [1]. Use strict exponent slack for every transfer. The table is a published lower-bound result, not a numerical conjecture in this note.

General transfer: if a compatible SAT/Q problem excludes simultaneous exponents (a_0,b_0), the above peak lemma excludes a CM upper exponent

$$
\gamma<\min(a_0,2b_0).
$$

Indeed C<=N^{gamma+o(1)} implies T<=N^{gamma+o(1)} and S<=N^{gamma/2+o(1)}. Strict inequalities absorb both machine-simulation and local-reduction overheads.

With (a_0,b_0)=(1.24,0.666), min(a_0,2b_0)=1.24. Thus

$$
\boxed{\text{For every fixed }\gamma<1.24,\quad
C_Q(N)\le N^{\gamma+o(1)}\text{ is impossible.}}
$$

For example, C=O(N^1.23) would give T<=N^{1.23+o(1)} and S<=N^{0.615+o(1)}, strictly inside the excluded rectangle. This improves the earlier standalone 1.165373... threshold obtained using only our selected FLMV branch. It does not assert the sharpest possible CM frontier or exclude the boundary gamma=1.24.

The same table supplies additional time-CM rectangles. For example its excluded time n^1.14 / space n^0.75 pair excludes the simultaneous target bounds T<=N^{a+o(1)}, C<=N^{gamma+o(1)} whenever a<1.14 and gamma<1.50. All these statements require the model assumptions above.

## 3. A stronger small-workspace time region

The established SAT time exclusion for subpolynomial workspace extends to every fixed

$$
a<2\cos(\pi/7)=1.8019377358\ldots.
$$

Accordingly, the local Q reduction transfers the exclusion

$$
\boxed{T_Q(N)\le N^{a+o(1)},\quad S_Q(N)=N^{o(1)},\quad a<1.8019377358\ldots.}
$$

This goes beyond the golden-ratio endpoint used in the original FLMV-only region. It concerns deterministic algorithms, excludes input from workspace, and does not give an unrestricted time lower bound without the workspace condition [1,2].

The known alternation-trading framework has a proved limitation at this endpoint in the subpolynomial-workspace setting [2]. Merely repeating those proof rules does not exclude every polynomial exponent.

## 4. A product region for worst-case time and peak workspace

Williams's Theorem 4.11 supplies a conservative published product bound for polynomially bounded time and workspace [1]. In exponent form, after the same local transfer,

$$
\boxed{T_Q(N)\le N^{a+o(1)},\quad S_Q(N)\le N^{b+o(1)},\quad a+b<\varphi}
$$

is forbidden, where phi=(1+sqrt(5))/2. The statement is a simultaneous exclusion for one correct uniform solver's worst-case resource bounds. It is not a product of resource minima achieved by different solvers, and it cannot be substituted directly for a CM bound.

Source correction: an older version claimed a general product exponent near 1.801. The corrected manuscript explicitly withdraws that assertion in footnote 9. This note uses its proved golden-ratio product bound and its stated individual time-space pairs, not the withdrawn stronger product claim. The separate subpolynomial-space time exponent 1.801937... remains valid.

## 5. Passes times retained memory: allowing a limited number of rereads

The previous INDEX construction was defeated by a second pass. Replace it by equality on two k-bit strings u,v.

Use the verified T5 anchors and pin gadgets. With C(a,b,c)=R(a,b,c) AND R(b,a,c), the anchor frame A has ten assignments; P_0(X)=C(a_1,a_4,X) and P_1(X)=C(a_2,a_4,X) pin X to distinct frame-relative values. Construct

$$
G_{u,v}=A\land\bigwedge_{j=1}^kP_{u_j}(X_j)
\land\bigwedge_{j=1}^kP_{v_j}(X_j).
$$

The input places the entire u-block before the v-block. It has N=Theta(k log(k+2)) bits and is satisfiable exactly when u=v. When satisfiable it has ten assignments.

Suppose an exact deterministic p-pass forward streaming solver has at most 2^S complete persistent states, including all continuation-relevant registers and metadata. A pass reads forward; between passes the input cursor resets to the start. No extra input head or uncharged store is available. Use fixed-width messages and pad halted runs with a halt marker when needed.

Alice, given u, simulates each first block. Bob, given v, simulates each second block. Transfer the complete state whenever simulation switches owners: at most 2p-1 messages, each S+O(1) bits.

Every accepting deterministic communication transcript must correspond to a rectangle. No such transcript can accept two distinct diagonals (u,u) and (v,v): it would then accept the off-diagonal (u,v), contradicting correctness. There are 2^k diagonals, so at least 2^k accepting transcripts are necessary. Thus

$$
(2p-1)(S+O(1))\ge k.
$$

In particular,

$$
\boxed{p(S+1)=o(k)\text{ is forbidden},}
$$

or p(S+1)=o(N/log N) on this encoded family. For bounded p, this requires linear-in-k retained state. With S=O(log k), it requires p=Omega(k/log k).

The same equality test embeds into the compact Q language using the circuit E_{u,v}=AND_j[u_j=v_j] as a predicate independent of its two assignment inputs. Put k u-constant records before k v-constant records and keep all topology fixed. The standard wrapper with B=6, q=13 has a witness exactly when E=1. This yields the same compact-description streaming bound, even at fixed q=13. It is a data-access theorem, not growing-alphabet SAT hardness.

Scope exclusions matter: bounded-error equality admits fingerprints, so this exact deterministic proof does not establish the same randomized bound. Random-access comparison solves these equality instances efficiently. Arbitrary interleaving/reordering of the input blocks is outside the protocol simulation. The pS lower bound alone also does not establish a p-dependent CM lower bound; a residence proof would be needed.

## 6. Preprocessing and online computation must share the budget

Suppose a compiler preprocesses each input in P(N) time, then a consumer decides it in E(N) time. Include the generated representation, retained parent state, conversion and output in the same-run memory ledger. The combined time is P+E, and every previous simultaneous exclusion applies to that composition if its machine model matches.

For example, total P+E<=N^{1.23+o(1)} and total peak auxiliary workspace <=N^{0.65+o(1)} are forbidden for Q by the published (1.24,0.666) pair. A fast query alone is not forbidden if preprocessing has already paid greater time or workspace. No information-theoretic claim can hide expensive answer computation in an uncharged preprocessor.

## 7. What these regions do not establish

These exclusions eliminate low-resource corners, not the entire polynomial quadrant. A solver with time N^3 and workspace N remains compatible with all listed unrestricted time-space bounds and their CM consequences. The streaming theorem removes low-pass/low-memory combinations but does not constrain arbitrary random access.

For a P versus NP separation, one still needs either a lower bound that defeats every fixed polynomial-time cap, or a proved solver-dependent transformation that forces any hypothetical polynomial solver into an already forbidden region. The recently proposed CM contraction contract states one sufficient transformation, but its universal implementation remains open [5].

## Validation and provenance

Primary sources [1,2] were opened, their relevant theorem/table and limitation statements inspected, and the corrected versus withdrawn product claim distinguished. The exponent arithmetic 1.23<1.24, 1.23/2=0.615<0.666, and 2*0.666=1.332>1.24 is elementary. No new software experiments were needed or run. The equality consequence is a symbolic communication proof using the anchor/pin semantics already verified in [4]. No independent review or formal-kernel verification is claimed.

## References

1. Ryan Williams. Alternation-Trading Proofs, Linear Programming, and Lower Bounds. Corrected author manuscript, Table I and Theorem 4.11, page A:18; correction in footnote 9, page A:17. https://people.csail.mit.edu/rrw/automated-lbs.pdf
2. Samuel R. Buss and Ryan Williams. Limits on Alternation-Trading Proofs for Time-Space Lower Bounds. CCC 2012 conference manuscript. https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/samCCC-cr.pdf
3. Project. T_q FLMV and CM Forbidden Regions, 2026-11-22. https://chatgpt.com/library?file_id=libfile_12e7c9e98f948191a775423cc98dcfc8&account_id=personal
4. Project. T5 and T_q Entropy Lower Bounds, 2026-11-22. https://chatgpt.com/library?file_id=libfile_8b0ae7ec0de48191916c56fe72c5cec4&account_id=personal
5. Project. PNP CM Contraction Proof Attempt, 2026-11-22. https://chatgpt.com/library?file_id=libfile_59805510f01c819198d654d42c495e23&account_id=personal
