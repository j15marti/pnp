# LSPV-5/468: exact count-once charging requires the paid-origin history

**2026-11-09 13:56 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

Affected proof-chain evidence: new **[P2-L5-468]**, refining [P2-C3],
[P2-L5-464], [P2-L5-467] and [P2-L1-544].  [P2-D1], [P2-C3],
[P2-B1] and [P2-B2] remain **OPEN**.  Historical R_mix341 grammar and weights
are unchanged.

## Actual advance

For $n$ independently reusable positive-weight paid origins, an exact
deterministic Markov abstraction of first-use/count-once charge must distinguish
all $2^n$ paid-origin histories.  This is a sharp abstract-state cardinality
lower bound.  A coarser MAY quotient remains cost-sound only by assigning each
abstract action at most the minimum concrete incremental charge over its
concretization; if a block mixes histories where origin $i$ is already paid and
not yet paid, that greatest safe uniform charge is zero.

Consequently, abstract-satisfaction transformers for deduction, propagation,
learning or quantification do not by themselves preserve proof cost.  A
cost-sound analysis needs a reduced product with a history component, or must
accept the stated undercharging.  This does **not** imply exponential physical
space: a paid-origin subset has an $n$-bit representation.  It also does not
imply a large proof minimum: the control goal using every origin has cost only
$\sum_i w_i$.

## IDEA and falsifiers

Hypothesis: an exact Markov abstraction cannot omit the already-paid-origin
set.

1. **Falsifier:** two different paid-origin subsets share one abstract state
   while all next-origin charges remain exact.  **Rejected** by the symmetric-
   difference proof below.
2. **Falsifier:** on a merged state, using the larger possible next charge is
   safe for negative-proof analysis.  **Rejected:** it overcharges a concrete
   zero-cost reuse and can falsely exclude a proof within budget.
3. **Falsifier:** reconvergent sharing defeats the argument.  **Rejected:** the
   correct concrete join is set union; next use is free exactly when the origin
   lies in that union.
4. **Falsifier:** the $2^n$ abstract-state result proves a superpolynomial
   historical mixed minimum or B3.  **Rejected:** the subsets are represented
   by $n$ bits and the control optimum is linear.

## SEARCH

### Governing repository evidence read

Fresh immutable preflight head:
`ae7a395136175781a1611d2450c5b28f446abae4`.  Both complete trackers were read:
`proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`
(18,553 characters) and `proof2.txt` blob
`117c9a87e616eb98b275d6329d64d703bfd5f1cc` (820,584 characters).  Also read
the complete November 9 abstraction refocus, AGENTS.md, CODEX.md, the repository
research skill, the governing November 2 handoff, and issue #3 through comment
`6752457051`.

Actual peer evidence read directly:

* [P2-L1-544], additive shared-obligation dual and its exact ceiling, report
  blob `90fe094212ea9b24719a47e44c230ec52d3f1108`;
* [P2-L2-527], cost-sound MUST/MAY RAT interval and exponentially branching
  spurious join, report blob `5fbb0898e52d98abf698c545de212cfe5570fa2a`;
* [P2-L3-541], DEF-facet polarity erased by extensional masks, report blob
  `4e264e6dee2c1a33bfc24bdc92940bce7cbad21e`;
* [P2-L5-467], sponsor-flow whole-DAG accounting, report blob
  `8b168fcae968a99d9e17f6ab9a5228293ce0aef3`;
* LSPV-4's shared-configuration cost-partition theorem and count-once branch
  falsifier, and the latest actual Grok report
  `GROKPROOF/2026-11-09_2015_PROGRESS.md` blob
  `5610d47e2a78ded4e4e57bc24fca3266e03f42ac`;
* actual Claude artifact
  `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob
  `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

The current historical-rule evidence still records specification nonuniqueness
for AND3 condition parents [P2-D1] and lacks a complete accepted-byte
LOCAL-CONVERT/DEF/GF(2)/RES/branch grammar.  No missing rule is assumed away.

### Primary literature

* Cousot and Cousot, *Abstract Interpretation* (POPL 1977),
  <https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml>, supplies the
  concrete/abstract fixed-point discipline; a negative result cannot omit a
  concrete behavior.
* D'Silva, Haller and Kroening, *Abstract Conflict Driven Learning* (POPL
  2013), <https://www.kroening.com/papers/popl2013.pdf>, combines over-
  approximated greatest fixed points with underapproximated least fixed points
  under lattice-theoretic hypotheses.  It does not establish proof-cost
  nonexpansion.
* D'Silva, Haller and Kroening, *Abstract Satisfaction* (POPL 2014),
  <https://www.kroening.com/papers/popl2014.pdf>, characterizes deduction,
  abduction, quantification and solver refinement by abstract transformers.
  The paper does not supply the history-dependent count-once resource product
  proved here.
* Rabin and Scott, *Finite Automata and Their Decision Problems* (IBM JRD
  1959), DOI 10.1147/RD.32.0114, is the classical finite-state distinguishability
  background.  The theorem below is proved directly and does not import an
  automata result as a proof-complexity lower bound.

No Google-branded search interface was available in this run; the available
primary web-search service was used, and actual papers/landing pages were
opened rather than relying on snippets.

### Required repository review

Pinned change-aware review found no active-gap closure:

| Repository | Head | Actual inspected evidence |
|---|---|---|
| `konard/p-vs-np` | `ecedd2b45f1c524d02734bbc8d0e705d057e1139` | README blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`; unchanged claim/method inventory |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` | `METHOD_INDEX.md` blob `18d693d07947d57723be912d0305890e81f366c0`; unchanged research index, not authority for a solution |
| `meelgroup/frat-xor` | `18cd6bc17af10a9891c10a846ce966166f9fe0dc` | `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; explicit XOR proof records, not historical R_mix341 bytes |
| `tanyongkiam/cake_lpr` | `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` | `README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; compiled checker/toolchain scope |
| `peitl/short-proof` | `2c524cfceecf68b56f51d23f6b63255b502856d3` | `README.md` blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`; shortest Resolution only |
| `marijnheule/drat-trim` | `2c67d5fb01ee4a9a290e237c2801c347ba78716a` | README blob `eb6ffcc4a85ff1c74a5995b6caae4372381dcd47`; DRAT checking is not a mixed lower bound |
| `msoos/cryptominisat` | `97c6efeae45d93c45d2ebc3e4e83c2014c79513d` | README blob `7636988713ee16802b84fb1cdf688ea8f87da70e`; 5.18 update/CI changes do not close the transformer gap |
| `openai/math` | `4eaee87548250b2682affda7d05d947c05554bae` | `README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`; no applicable theorem |
| `anthropics/formal-math` | `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` | `README.md` blob `1df53bfc14a022088d1b5757698f692bf79390b4`; no applicable theorem |

## ITERATE

### Concrete and abstract domains

Fix $n$ immutable paid origins $I=\{1,\ldots,n\}$ with $w_i>0$.  A concrete
history is $S\subseteq I$, the set already inserted and paid in the shared
DAG.  Action $\operatorname{use}(i)$ has transformer and incremental charge

$$
T_i(S)=S\cup\{i\},\qquad
\Delta_i(S)=\begin{cases}0&i\in S,\\w_i&i\notin S.\end{cases}
$$

This is the accounting fragment of a shared proof configuration, not a new
logical inference rule.  Reconvergence joins histories by union.

For a quotient map $a:2^I\to Q$, lift to the standard partition abstraction
between powersets:

$$
\alpha(X)=\{a(S):S\in X\},\qquad
\gamma(Y)=\{S:a(S)\in Y\}.
$$

Then $\alpha(X)\subseteq Y$ iff $X\subseteq\gamma(Y)$.  Reachability uses a
MAY overapproximation.  Resource polarity is lower: an abstract incremental
charge is safe for a lower bound only when it does not exceed the corresponding
concrete charge.

### Exact-history theorem

**Theorem 468.1 (PROVED/RESTRICTED).**  Suppose a deterministic Markov
abstraction assigns each abstract state $q$ and action $i$ a charge
$\widehat\Delta_i(q)$ satisfying

$$
\widehat\Delta_i(a(S))=\Delta_i(S)
$$

for every $S\subseteq I$ and $i\in I$.  Then $a$ is injective and
$|Q|\geq2^n$.  The same conclusion holds a fortiori when exact abstract
successors are also required.

**Proof.**  For distinct $S,T$, choose $i\in S\mathbin\triangle T$.  Without
loss of generality $i\in S$ and $i\notin T$.  Then
$\Delta_i(S)=0$ while $\Delta_i(T)=w_i>0$.  If $a(S)=a(T)$, the single value
$\widehat\Delta_i(a(S))$ would have to equal both, a contradiction.  Thus all
$2^n$ histories are distinct.  QED.

The bound is attained by $Q=2^I$ with the exact subset transformer, so it is
sharp within this interface.

### Greatest safe coarse charge

**Theorem 468.2 (PROVED/RESTRICTED).**  For abstract block
$B=\gamma(\{q\})$, the greatest uniform lower charge that is safe for every
concretization is

$$
\widehat\Delta_i(q)=\min_{S\in B}\Delta_i(S).
$$

If some $S,T\in B$ disagree on membership of $i$, this value is zero.

**Proof.**  Any safe uniform charge must be at most every concrete charge and
hence at most their minimum; the minimum itself satisfies all those
inequalities.  A mixed block contains one zero-charge reuse.  QED.

Choosing the larger value $w_i$ on such a block is not conservative: it can
raise an abstract path above budget even though its concrete image reuses an
already-paid node for zero charge.  Choosing zero preserves coverage and cost
nonexpansion but may create a cheap spurious path.  This is the resource
analogue of [P2-L2-527]'s logical MUST/MAY precision loss.

### Shared-DAG and sponsor-flow composition

At reconvergence the exact history is $S\cup T$.  A subsequent reference to
$i$ is free iff $i\in S\cup T$.  The theorem therefore covers count-once
sharing rather than a tree unfolding.  Combined with [P2-L5-467], the history
component decides which concrete origin capacities remain available, while a
sponsor-flow certificate prevents multiple abstract charges from overdrawing
one remaining capacity.  Neither theorem supplies missing logical transformer
semantics.

### Mandatory shortcut controls and non-implications

| Family/control | Established scope | Required legal shortcut | Consequence here |
|---|---|---|---|
| Haken PHP [P2-F1] | exponential ordinary DAG Resolution | Cook polynomial Extended Resolution | history theorem does not exclude ER |
| odd cubic Tseitin [P2-F2] | exponential ordinary Resolution on expanders | declared /341 AND3/GF(2) refutation has $4h-1$ paid nodes | parity action must remain in any MAY system |
| strict mod-3 one-hot [P2-L1-518], [P2-L1-519] | restricted opposite-characteristic proof bounds and explicit upper controls | nonlinear/extension/shared shortcuts remain possible | no historical mixed lower bound |
| RAT/DRAT [P2-L2-526], [P2-L2-527] | consequence-only abstraction is incomplete; interval join is imprecise | model-changing RAT and deletion | history product does not repair logical rule omission |

The exact abstract state count is not an evidence-bit lower bound, time lower
bound, or space lower bound.  An $n$-bit mask represents a state, sparse sets
can be smaller on some paths, and the ideal proof minimum excludes discovery
cost.  B3 is untouched.

## Independent computation and resources

Python checked 698,027 distinct history pairs for $n\leq10$, 669,924 exact
join/action triples for $n\leq8$, all 4,157 set partitions for $n\leq3$, and
99,484 pointwise MAY inequalities.  Exactly one partition at each $n=1,2,3$
preserved exact charges and exact deterministic successors: the discrete
partition.  Six malformed inputs were rejected.  Independent Node code
recomputed every count and partition result.

| Artifact | SHA-256 | Bytes / execution |
|---|---|---|
| Python producer | `16ea5061aa6e88a4b1aff5444968ff6703008fa87558b4fb538cd71b9cbe58ac` | 7,019 bytes; 0.331804 s; 9,856 KiB peak RSS |
| independent Node verifier | `97daf65cb670d5b133be601c8b77ed293d9339900b4cf0da53e60faee5a0290f` | 4,340 bytes; 0.057956 s; 53,880 KiB peak RSS |
| Python raw JSON | `fe6a9bf6175328e00bfc2c1a4e8d001f33afe4ad36f8345e44a6bbe26b2feea0` | 2,691 bytes |
| Node replay JSON | `2dfa29516b28937d6a0fbe63d67c7ac92710523aa38d3c2d2fe237bc9f632f5e` | 514 bytes |

Logical nodes, evidence bits, construction, search, parsing, tracker/head
reads, literature/repository retrieval, verification, output, publication and
readback remain separate phases.  No authoritative historical checker was
executed.

## Tracker assessment and remaining gap

This result materially refines the evidence/dependency description of
[P2-C3], so [P2-L5-468] is appended to `proof2.txt`.  `proof1.txt` has no
material change.

The precise remaining gap is a sound reduced product combining (i) complete
historical rule/context/provenance transformers, (ii) count-once history or a
proved safe undercharging quotient, and (iii) sponsor capacities, followed by
a nontrivial family invariant that survives GF(2), ER, RAT/deletion,
LOCAL-CONVERT, nonlinear and shared-DAG shortcuts.  [P2-D1], [P2-C3],
[P2-B1] and noncircular [P2-B2] remain **OPEN**.  P versus NP remains **OPEN**.

## Publication and readback

Published by lease-protected content commit
`f5db6d2f5bce52907d796858a0f4a513cd95527a` on refreshed parent
`ae7a395136175781a1611d2450c5b28f446abae4`.  All nine role-owned artifacts
read back byte-for-byte.  `proof1.txt` remained blob
`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; `proof2.txt` read back as blob
`24f942315c8558396499c336061fd514c6b669f4` with exactly one [P2-L5-468].
The contents endpoint returned only manuscript metadata, so full readback used
the blob endpoint: all 1,829,326 bytes of blob
`13e66d0bc721a26a389aa9b98042a6dd9d431ccf` matched, with one ownership-marker
pair, one REFEREE468 insertion and exact bytes outside the LSPV-5 region.
Issue #3 comment
<https://github.com/j15marti/pnp/issues/3#issuecomment-6752669395> read back with
the exact 1,150-byte body.  This receipt is committed separately after those
checks.
