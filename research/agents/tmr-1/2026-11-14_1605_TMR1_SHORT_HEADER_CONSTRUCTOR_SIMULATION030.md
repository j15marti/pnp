# TMR-1/030: A charged short-header constructor simulation for one-work-tape MCSP networks

**Pacific timestamp:** 2026-11-14 16:05 PST. **Owner:** TMR-1 Machine Model Lead. **Scientific status:** SHORTHEAD41 is a self-contained **PROVED/RESTRICTED symbolic simulation lemma, awaiting independent TMR-3/TMR-5 review**. The finite physical-head interpreter is **COMPUTATIONAL**. The CHMY low-threshold magnification premise and P versus NP remain **OPEN**.

## 1. New finding relative to existing project work

TMR-3/030 gave a lower-bound frontier for a length-uniform network computing *large-threshold* MCSP, using an additive constructor cost \(C\). TMR-5/027 correctly found an open interface: a constructor that reads binary \(n\) on an **additional independent input head** is not automatically a physical **one-work-tape** constructor. Its safe universal rescanning simulation costs \(O(C(C+\log N))\), making a \(C=\Theta(N)\) constructor exceed the \(N^{1.99}\) theorem budget.

**SHORTHEAD41 repairs this precisely scoped interface:** a fixed deterministic constructor with **one guest work head** and one separate **short** read-only \(h\)-bit input head can be simulated on **one physical work tape** with \(O(C(h+1)^2)\) transitions, *provided the entire header is first legitimately stored on that tape*. An additional spooling-and-arity-discovery step shows how, for **length-only** network constructors, this header can be obtained from an ordinary header-free **one-way** MCSP truth-table stream, without using a second live input head. The repair is restricted to the exact constructor/output/network normal form below, and it does **not** transform a high-\(\mu\) theorem into the low-\(\mu\) magnification premise.

This is a constructive repair of TMR-5's legitimate model objection, not a generic optimization claim for arbitrary multihead constructors.

## 2. Precise model and all quantities

- **Source MCSP input:** a complete table \(x\in\{0,1\}^N\), \(N=2^n\), on the one-way read-only source tape; no advance arity, rewinding, or source random access. Malformed non-power-of-two lengths are rejected. \(n\) is the Boolean arity, **not** encoded SAT input length \(L\).
- **Length-only constructor \(G\):** one fixed finite-alphabet deterministic machine with one two-way read/write **guest work tape**, one separate two-way read-only input tape containing a fixed binary encoding \(u=\mathrm{bin}(n)\) of \(h=\Theta(\log(n+2))\) symbols, one head per tape, fixed finite control and halting output. It does **not** inspect the \(N\) source bits. Its actual guest transition count is \(C(N)\), visited guest work cells at most \(C+O(1)\); a description of length \(B(N)\le C+O(1)\) is present in the **first \(B\) consecutive guest work cells at halt**, with a finitely identifiable delimiter. There is **no additional live output tape or second guest writable head**. Its output program/description and all preprocessing are charged.
- **Network \(K_n\):** the description encodes \(p(N)\) finite-alphabet single-tape processors with total charged count \(E(N)\) of constant-symbol local steps, bounded-symbol message and routing events, source accesses, and scheduling actions. A long message costs one event per symbol; no unit-cost unbounded word or free source reread. The network uses no length-dependent advice beyond what the constructor wrote. Uniform correctness and a bounded two-sided-error random choice model, if randomization is used, are part of the hypotheses.
- **Simulator:** one *fixed*, deterministic or correspondingly randomized machine with the original one-way input and **one** two-way writable work tape. The head is physical; auxiliary marks reside on tracks of this same tape. A bounded-state controller may not cache the variable \(u\) for free.

Let \(h=|\mathrm{bin}(n)|\) with the harmless \(n=0\) case encoded by one symbol. Define a symbolic active network record budget

\[
M=O\left(N+B(h+1)+(E+p+1)\log(N+B+E+p+2)\right).
\]

The block replication construction provides the following **restricted upper bound**, with constants dependent only on the fixed constructor and network record interpreter:

\[
\boxed{T_{\rm sim}(N)=O\!\left(N\log(N+2)+C(N)(h+1)^2+(E(N)+1)M\right).}
\]

The same physical run has peak visited writable cells at most

\[
O\!\left(N+C(h+1)+B(h+1)+(E+p+1)\log(N+B+E+p+2)\right).
\]

The constructor's potentially wasteful peak workspace is therefore **not** erased from the space ledger. For the network phase, the active prefix may exclude stale constructor scratch cells beyond the delimiter, with initialization tags preventing stale content from being accepted as a fresh network record.

## 3. Fully charged proof of the short-header lemma

Suppose \(u\) has already been copied legitimately to the one physical work tape. Represent each visited guest work-tape cell \(j\) by a block of \(O(h+1)\) **physical** cells. Every block contains its guest work symbol, a complete immutable copy of all \(h\) header symbols, and a unary one-hot marker giving the guest read-only input head's current position, including endmarkers. Block separators and initialized/uninitialized tags use a fixed finite alphabet. The *only* distinguished physical block is that of the current guest work head.

At each guest step, scan the current block once to discover the guest work symbol and the header symbol under its marked virtual read-only head, and apply the guest's finite transition table. Update the work symbol and the virtual input-head marker within the current block. For a guest work-head move to an adjacent cell, copy all \(O(h+1)\) header/marker symbols into the adjacent block. A single physical head can copy any one of these symbols by traveling between the two adjacent blocks, costing \(O(h+1)\) charged steps. Thus a complete block copy costs at most \(O((h+1)^2)\); if the destination was previously visited, preserve its guest work symbol, but overwrite its stale local input-head marker. An uninitialized block has guest symbol blank. On an unchanged guest work-head position, no copy is needed. This proves **every** guest transition is represented by a finite physical path of no more than \(K_G(h+1)^2\) steps. It uses no unbounded-word instruction, nonuniform input-specific transition table or extra physical head.

The original stored header permits initialization of the first block in \(O((h+1)^2)\). For \(C\ge1\), the entire \(C\)-step guest trace, including reversal, recomputation, output writes and final head return, costs \(O((C+1)(h+1)^2)\). Each guest work cell occupies \(O(h+1)\) physical cells. A separate guest read-only head has therefore been eliminated without the \(O(C^2)\) full-tape scan of TMR-5/027.

**Scope:** This proof is for *one* guest writable head plus the short header head. An arbitrary constructor with many independent writable heads, source-data access, random-access unit-cost writes or a separate live output tape is not covered. Encoding the full \(N\)-bit MCSP source as the replicated header would give \(h=N\) and no useful bound.

## 4. Obtaining the header without an MCSP input-length oracle

A header-free one-way-input simulator first copies all \(N\) source bits to its work tape, with both physical heads advancing together. This costs \(O(N)\). At EOF, keep the source bits intact but mark a second *track*. Repeated complete left-to-right sweeps of the copied \(N\)-cell segment remove every second currently active marker. A finite-state parity toggle detects whether the current number of active markers is even, and a finite-state zero/one/many flag detects termination. If an odd number greater than one remains, reject the malformed length. At each successful halving, increment a separate counter for \(n\). No assignment to the original source-bit track changes.

For \(N=2^n\), exactly \(n\) halvings leave one active marker. Each round makes \(O(N)\) physical moves; the counter has \(O(\log(n+2))\) binary digits and can instead be built in unary \(n\) units, then converted to binary in \(\mathrm{poly}(n)\) work, well within \(O(N\log(N+2))\). The \(N\) original source bits remain available on the **same work tape** for subsequent simulation. Move to the adjacent scratch region, initialize the first short-header block and execute \(G\). Its separate original input head is now represented *solely* in the block headers, as above.

At halting, the \(B\)-bit network description is already in the first \(B\) consecutive guest blocks, of footprint \(O(B(h+1))\). Returning from the guest's last visited location costs \(O(C(h+1))\), already charged. Interpret only the compact description prefix and the source data; ignore and lazily overwrite any old scratch beyond the current active delimiter. No quadratic compaction of \(C\) abandoned guest cells is assumed.

Finally, serialize the stipulated network events using the standard single-work-tape **active-record scan** of TMR-3/030. Each bounded-symbol event reads or updates \(O(1)\) logical records in at most \(O(M)\) movements, including access to the previously **spooled** input and virtual processor heads. \(E\) events cost \(O((E+1)M)\), with scheduling and messages counted. Initializing \(p\) processor states and the \(B\) description cells is covered by the \(M\) scan. All source rereads are accesses to the charged spool, not free rewinding of the original source tape. The resulting fixed physical machine has **exactly one one-way input head and one work head**.

This proof gives an upper-bound **simulation**; no lower bound follows without independently invoking a theorem whose target model exactly matches it. It also requires scrutiny of TMR-3/030's per-event active-record normal form.

## 5. Exact theorem transfer and exponent frontier

| Original theorem | Input, promise, model, threshold, result |
| --- | --- |
| Cheraghchi, Hirahara, Myrisiotis and Yoshida, STACS 2021, Theorem 1, printed p.23:3 [1] | **Ordinary exact decision** MCSP on a full \(N=2^n\)-bit truth table, \(s=2^{\mu_1 n}=N^{\mu_1}\) for some unspecified **sufficiently small** fixed \(\mu_1>0\). Deterministic one-way read-only input plus one two-way work tape. **Conditional:** a lower bound excluding \(O(N^{1.01})\) implies \(P\ne NP\). This premise is **OPEN**. |
| Same, Theorem 2, printed p.23:3 [1] | **Ordinary exact decision** MCSP, a **different larger** constant \(\mu_2\) close to 1, same one-way source and one-work-tape interface, even two-sided-error randomized computation. **KNOWN THEOREM:** excludes \(O(N^{1.99})\), with bounded error convention at least \(2/3\). Not a magnification proof at \(\mu_1\). |
| McKay, Murray and Williams, STOC 2019, Theorems 1.2-1.3, p.2, author accepted manuscript [2] | **Search**-\(MCSP^A[s(n)]\), oracle gates \(A\), \(N=2^n\), time-constructible \(s(n)\ge n\). One-pass \(\Sigma_3SAT^A\)-oracle streaming upper bound with \(\widetilde O(s)\) space and \(\widetilde O(s^2)\) update time; a specified absent deterministic \(\mathrm{poly}(s)\)-space/update streamer for some \(A\in PH\) **conditionally** implies \(P\ne NP\). Does not identify that search task with ordinary decision MCSP. |
| Oliveira and Santhanam, FOCS 2018, original ECCC TR18-139 [3] | Distinct MCSP *approximation/average-case formula* magnification, with its own promises, input measure and nonuniform conclusions. Not imported into this simulation. |
| Chen, Jin and Williams, FOCS 2019 [4] | Hardness magnification in sparse NP languages and related locality constraints. No locality barrier is assumed to imply a one-work-tape time lower bound here. |

For \(C=O(N^c)\), \(B=O(N^b)\), \(p=O(N^a)\), \(E=O(N^e)\), put \(d=\max(1,a,b,e)\). Since \(h=\Theta(\log\log N)\) and \(\log(N+B+E+p)=O(\log N)\) for fixed polynomial exponents, SHORTHEAD41 yields \(T_{\rm sim}=N^{\max(1,c,e+d)+o(1)}\). The published **large-threshold** Theorem 2 therefore excludes simultaneous performance with

\[
\boxed{c<1.99,\qquad e+\max(1,a,b,e)<1.99}
\]

under the precisely declared constructor/network model. The constructor condition is **not** the weaker \(2c<1.99\) condition forced by TMR-5's generic fallback. At \(C=\Theta(N)\), \(B,p=O(N)\), \(E=O(N^{0.8})\), the repaired physical construction runs in \(N^{1.8+o(1)}\), whereas the generic quadratic constructor fallback only establishes \(N^{2+o(1)}\).

**Crucial separation firewall:** This conclusion applies only at \(\mu_2\), with a restricted length-only, compact-output, bounded-event network architecture. It does not exclude all \(N^{O(1)}\) algorithms, transfer from arbitrary SAT programs or prove the \(\mu_1\) antecedent. For arbitrary correct uniform 3-SAT deciders \(A\), the unsolved quantifier remains

\[
\forall A\,\forall k\ge1\,\forall C_0>0\,\forall L_0\;\exists F:
|F|\ge L_0\;\land\;
T_A(F)>C_0(|F|+1)^k.
\]

No ETH, SETH, natural-proofs assumption, uncharged oracle, nonuniform hardcoded constructor, or assumption of MCSP NP-completeness was used.

## 6. Reproducible finite controls and adversarial inputs

**Native OS Node.js** executed \`experiments/tmr/tmr1_short_header_bridge041.js\` with seed family \`h*65537+seed\` for \(h=1,\ldots,12\), seeds \(1,\ldots,18\), 90 adaptive guest steps per case. The single-head proxy charges every read, write and physical move, and explicitly copies the header and input-position vector between neighboring blocks. It compares read symbols and input-head positions against a second direct guest interpreter after every step and checks all touched work symbols. **216 configurations, 19,440 guest steps, 9,978,085 charged physical operations, 257 exact source-length halving controls and 89,177 rational-grid exponent tests, 397,331 assertions, zero failures.** The observed maximum step cost was \(29.5(h+1)^2\). The code implements an indexed-block *testing proxy*, not a compiler of a finite-control machine, and the symbolic block-delimiter proof is independent of its finite observations.

Native source SHA256: \`0e295ceb5ecfe6c98a8e3831c97adc9bfed37cdf7ddb721a04cedc9618a4e6b9\`; raw JSON SHA256: \`16072681f2441e8b38a433fd862ff24b6af83c79a82c90dddc46023ecdfb8d38\`. Compare the committed Git blobs with local \`git hash-object\`: \`a1c10185fc67086825e4522fde0420be4550fcc2\`, \`9bf44a2349def43241204bb2907ba56378e6b232\`.

All upper/lower conclusions are separately scoped: finite controls are **COMPUTATIONAL**, block-copy lemma is **PROVED/RESTRICTED pending peer review**, network lower-bound corollary is **CONDITIONAL** on the restricted network model and the published high-\(\mu_2\) theorem, unrestricted SAT and low-\(\mu_1\) conclusions remain **OPEN**.

## 7. Prior-work ledger, reconciliation and peer request

Preflight read **first** the 2026-11-14 MCSP directive (Git blob \`1e11aa64a0b0d635a65cea58500b09f2b0fe010a\`), then the Nov13 TMR replacement, both root proof trackers (proof2 recovered as full 1,051,196-character Git blob), the complete 2,545,859-character main.tex Git blob, AGENTS.md, CODEX.md, pnp-research skill, issue #3 through TMR-5/027 and all current TMR handoffs. Read the original TMR-3/030 and TMR-5/027 reports rather than relying on chat, plus TMR-1/029, TMR-2/030, TMR-4/031 and relevant original one-tape/TPORT/direct-product Claude notes, Grok status, Walsh/moment and mixed-checker controls. Their representation-specific and restricted-model results are not promoted. The original accepted-counterexample evidence remains intact.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to either proof1.txt or proof2.txt; the constructor bridge does not close an unrestricted load-bearing arrow. Root main.tex is TMR-5 synthesis-owned and remains unchanged. No tasks, agent count or schedule modified.

**Single next target:** TMR-3 independently formalize and replay the one-physical-head short-header block copying and spool/halving stages, especially the compact-prefix output convention and network-event \(O(M)\) scan. TMR-5 red-team stale scratch records and source-independent-constructor scope. If either refutes an edge, preserve the exact minimal counterexample and replace the claimed frontier with the strictly weaker validated one. The ultimate low-\(\mu_1\) MCSP \(N^{1.01}\) lower bound is still **OPEN**.

## Numbered original references

[1] Cheraghchi, Hirahara, Myrisiotis and Yoshida. *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*. STACS 2021, Theorems 1-2, printed p.23:3. https://doi.org/10.4230/LIPIcs.STACS.2021.23

[2] McKay, Murray and Williams. *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*. STOC 2019, Theorems 1.2-1.3, p.2. https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf

[3] Oliveira and Santhanam. *Hardness Magnification for Natural Problems*. FOCS 2018, original ECCC TR18-139, https://eccc.weizmann.ac.il/report/2018/139/

[4] Chen, Jin and Williams. *Hardness Magnification for all Sparse NP Languages*. FOCS 2019, https://dspace.mit.edu/entities/publication/d86a1c74-972d-42f9-a3c7-a083d1bc1398
