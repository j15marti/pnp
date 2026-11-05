# LSPV-2/425: One-pass boundary-memory lower bound versus indexed reaccess

**2026-11-05 12:00 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | all-input FLMV contractor and P versus NP OPEN**

## IDEA, falsifiers, iteration

Test whether *arbitrary* shared-boundary survivor sets can be compressed below square-root input length in a **deterministic one-pass retained message**, not merely the explicit mask used in LSPV-2/421. Falsifiers: (F1) a valid 3-CNF suffix cannot distinguish two prefix sets; (F2) gates fail exact projection; (F3) prefix lengths vary by subset; (F4) indexed reread or an affine shortcut defeats promotion to arbitrary machines. F1-F3 were resolved by construction. **F4 succeeds** and is the central resource-model firewall.

## Theorem 425.1 (proved for exact one-way stream)

Fix $m\ge2$, $M=2^m$ and public bits $x_0,\ldots,x_{m-1}$. For each $a\in\{0,1\}^m$ define mismatch literals $\ell_{a,i}=x_i$ if $a_i=0$, else $\neg x_i$. The source block $F_S$ has a fresh switch $u_a$ fixed by a unit to $1$ precisely when $a\in S$. Encode $\ell_{a,0}\vee\cdots\vee\ell_{a,m-1}\vee u_a$ by a chain of $m$ OR2 gates, each output $z=p\lor q$ having three proper CNF clauses $(\neg p\vee z),(\neg q\vee z),(p\vee q\vee\neg z)$, and a final output unit. All gates are fresh, private and functional. Form $G_T$ analogously with disjoint private names.

Every assignment to public $x$ and forced selectors has a unique extension to the gates, so

$$
\exists\mathrm{priv}\, F_S(x)\iff x\in S,\qquad
\exists\mathrm{priv}\,G_T(x)\iff x\in T.
$$

The complete **3-CNF** is SAT iff $S\cap T\neq\varnothing$. Every encoded source at fixed $m$ has the same length since membership changes only fixed-width selector-sign bits.

Suppose a deterministic exact one-pass left-to-right machine reads the entire first block, then the second, without revisiting the prefix or using any external information, and retains $q$ configuration bits at the separator. Distinct $S\neq S'$ must give distinct states: choose $a$ in their symmetric difference and the identical singleton suffix $G_{\{a\}}$; final SAT labels must differ. There are $2^M$ possible first sets and at most $2^q$ states. Thus

$$
\boxed{q\ge M=2^m.}
$$

This is **representation-independent among retained deterministic one-way messages**, not independent of input access model. Complete input has $V=m+2M(m+1)$ named variables, $C=2M(3m+2)$ clauses and fixed-slot signed binary length $N=\Theta(m^2 2^m)$. Therefore one-pass memory is $\Omega(N/\log^2 N)$, eventually larger than $N^{1/2+o(1)}$.

## Theorem 425.2 (mandatory indexed escape)

On the **same promised source class** an indexed read-only input machine verifies the deterministic gate template and evaluates the $M$ *pairs of selector sign bits*, at fixed offsets. If any pair is positive-positive, output SAT; otherwise UNSAT. A binary counter, source/index-head and arithmetic require only $O(\log N)$ writable bits, and full source-template authentication takes at most $O(N\operatorname{polylog}N)$ operations. Nonmatching inputs yield OUT_OF_FAMILY rather than a false general SAT answer. Thus arbitrary indexed rereads destroy the one-way lower-bound implication. Read-only prefix bits are a lazy shared table, with each reaccess/index update charged.

This is not a general SAT algorithm. The actual Python and JavaScript producer/verifiers materialize $O(N)$ or more objects and are **not** native logspace/FLMV implementations.

## Known hard-family / model and short-circuit ledger

Compare with established odd-charge **cubic expander Tseitin 3-CNF**: $H$ vertices, $3H/2$ edge variables, four signed width-three wrong-parity clauses per vertex, $4H$ clauses, $N=\Theta(H\log H)$. Odd charge certifies UNSAT. Published Urquhart 1987 and Ben-Sasson/Wigderson 2001 lower bounds are $\exp(\Omega(H))$ for **ordinary shared-DAG Resolution on suitable expander sequences**, not arbitrary algorithms. Prior LSPV-2/341 gives short fixed-mixed AND3/GF(2) refutations with $4H-1$ paid nodes on bridgeless odd-charge sources, so this restricted Resolution hardness does not transfer to $R_{\mathrm{mix341}}$. LSPV-2/422-424 already cover explicit masks, cofactor mass, exact matching-cofactor memoization and affine quotient shortcuts. Our new gadget is a focused compression control, **not** a proposed hard SAT family. No new historical Rmix branching or discharge rule is assumed.

## SEARCH provenance and actual checks

Read original governing five-role handoff of November 2, issue #3 through LSPV-2/424 and LSPV-4/419, AGENTS.md, CODEX.md, pnp-research skill, actual GROKPROOF progress of November 5 (14:28 and 19:13 UTC), and actual Claude TPORT-0002 of October 28. Primary sources reviewed: FLMV JACM 2005 author PDF and Fortnow-van Melkebeek ECCC TR00-028, Urquhart JACM 1987, Ben-Sasson/Wigderson JACM 2001. Repositories actually inspected: konard/p-vs-np finite-one-tape complexity README (not FLMV); blkph0x/p-vs-np-proof-research METHOD_INDEX and bounded ADAPTIVE_FRAGMENT_SYNTHESIS_REPORT; cnfgen/families/tseitin.py; openai/math ExecCNFNodeSearchCosts.lean, specific driver only. The openai/math SATVariance.lean file visibly has a **sorry** in variance_main, not a complete formal proof. Direct Google search unavailable, indexed web and authenticated GitHub used instead.

Full separately preserved reproducer: Python producer 2,371 assertions; independent JavaScript verifier **795,237 checks**, 68 retained signed 3-CNF cases (55 SAT, 13 UNSAT), all original boundary assignments with unique gate extensions, 2,048 singleton-suffix tests at $m=3$, authentic bit-length and SHA256-source checks, actual indexed sign-bit retrieval and corrupted-control rejection. Seed 20261105. Python SHA256 d0036df2666dee8539c65f18cf4a089fcd991589283cf435c588e9a8b147f35e; JS SHA256 36c4be6e2dad3a088cc7f5013bc66306691084eb51d09a09d9123c9cf27b4b97; full raw SHA256 9d74a2563fa80d0ddfa9d26f16b00758d5172ec501d62cad891d7e311937189d. The SHA256 source digest is on an ASCII 0/1 rendering of the exact logical bitstream. Small compact in-repo replay and numeric summary accompany this report; complete original scripts/raw and full proof remain in the user-facing reproducibility archive.

## Missing Route A arrow

For **every** fixed uniform total correct polynomial SAT decider $A$, still need a recursively applicable all-input malformed-aware **same indexed-machine** transformation $A\mapsto\Phi(A)$ with

$$
t'\le\max\{11/10,\ 3/5+t/2\},\qquad s'\le\max\{1/2,\ s/2\}.
$$

No general small-child construction, parent-free exact joining or fully charged time/space simulator is established. For materialized children retain all-phase $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$, including source/index reads, parsing, failed policies, child writes, guests, output and live storage. Do not infer physical runtime or Rmix proof work from the restricted streaming state count. Root main.tex authenticated fetch returned SHA 1b8a7d9a1514b06c96501849a7902b7aa3dae2a1 with zero readable content, so **no mutation** was attempted. Peer review pending. P versus NP OPEN.
