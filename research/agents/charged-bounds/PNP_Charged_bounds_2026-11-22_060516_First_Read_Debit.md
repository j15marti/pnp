# Compulsory first reads, with preprocessing debited exactly

22 November 2026, 06:05:16 PST. PNP Lower Bound Connections.
DYNAMIC-FIRST-READ-DEBIT1 within DYNAMIC-COMPATIBILITY-OBLIGATION1.

**PROVED/EXACT restricted lemma:** every fixed correct deterministic solver must acquire each of q disjoint decision-sensitive regions on the explicit packed-cycle family below. At an observable checkpoint, precisely the still-unread regions give this certificate of fresh work. **COMPUTATIONAL:** encoding and decoder fibers checked. Independent adversarial review pending. The first-read bound is proved for the stated packed encoding of length L. Its transfer to the project's adjacent-witness encoding of length N is **OPEN** pending a physical support audit. No lower bound for that encoding is inferred merely from decision equivalence. P versus NP remains **OPEN**.

This advances the earliest compulsory-decoder premise, rather than another optional copied-output execution. Discovery's new NP-complete cycle family supplies the construction. Accounting correctly distinguishes disjoint physical reads from aliases of one cached read; the present lemma derives disjoint first reads from correctness, but also proves why they cannot be demanded anew after acquisition.

## Fixed model, target and falsifiers

Fix a uniform deterministic machine A, correct on every valid packed-cycle input, before choosing q or the sample. It has one finite-alphabet writable tape, one head with unit motion, binary initial input, input-independent initial control, and terminated Boolean output at the origin. A transition reads before writing its scanned cell. All input, working copies, addresses, caches and output occupy the same tape. No input oracle, externally initialized cache or uncharged input-dependent advice is allowed. Preprocessing, relocation, algebra, and arbitrary subsequent representations are unrestricted and paid.

For every q>=1 and every b in {0,1}^q, let G_q(b) be the packed input below. The assertion is

    for every correct fixed A, every q,b, and every observable stopping
    checkpoint tau <= T_A(G_q(b)):
    T_A(G_q(b)) - tau >= q - R_tau(b),

where R_tau counts the distinct sensitive regions first read by tau. This is a lower bound on the same actual run, not on virtual queries or a prescribed search DAG. The corresponding entropy statement uses uniform b for a fixed q.

Four falsifiers are (1) a one-coordinate change preserves the answer, (2) its physical changes overlap another coordinate's changes or leak into common metadata, (3) selection of the recorded read requires hidden advice, and (4) preprocessing has already read the supposedly fresh coordinate. Sections below exclude the first three on the packed family and explicitly debit the fourth. The compiled-input version of falsifier (2) remains untested.

## A parity-controlled subfamily of the new cycle construction

Let E(a,b,c) mean that exactly one of its three Boolean occurrences is 1, with repeated names counted with multiplicity. Use distinct names z,o,x_0,...,x_q,w_1,...,w_q. Start with

    E(z,z,o), E(x_0,x_0,o), E(x_q,x_q,o).

For j=1,...,q append

    E(x_(j-1),w_j,z),
    E(x_j,w_j,z)                 if b_j=0,
    E(x_j,x_(j-1),z)             if b_j=1.

The first row forces z=0,o=1. The next two pin x_0=x_q=0. The first row of each pair forces w_j=1-x_(j-1). Its second row forces x_j=x_(j-1) for b_j=0 and x_j=1-x_(j-1) for b_j=1. Consequently a satisfying assignment exists exactly when XOR_j b_j=0. The recurrence also constructs the unique source assignment when the parity is even. Thus every coordinate is decision-sensitive at every b, and both labels occur equally often. This is an affine control expressed inside the mixed family, not a purported hard instance generator.

Give z,o IDs 0,1, x_i ID 2+i and w_j ID q+2+j. There are v=2q+3 names and m=2q+3 triples. Apply Discovery's pinned reduction [1]. A variable block has two AA edges, a clause block three, and every block is followed by CC,AC,CC. The separator forces block endpoints 1 and 0. Variable interiors are their source values. A clause path 1,B,C,0 has successive XOR differences (1 XOR B,B XOR C,C), exactly one of which is 1. The three occurrence equations equate those differences with the indicated variable interiors. Distinct physical columns prevent cancellation when a source name repeats. The cyclic seam has the same separator. These observations prove both directions independently at the projected-cycle level.

The cycle has t=5v+6m=22q+33 columns and r=3m=6q+9 homogeneous ternary rows. Its ordinary proper source CNF has d=8t=176q+264 names and c=26t+4r=596q+894 clauses. These source counts are not the final physical length.

Define the explicit packed encoding used in the lower-bound proof as

    gamma(t) | top[t] | bottom[t] | gamma(r+1) | rows[3r*w],
    w=ceil(log2(t)), A=0, C=1,
    L=(2 floor(log2(t))+1)+2t+(2 floor(log2(r+1))+1)+3rw.

Addresses are zero-based fixed-width binary, with value <t; invalid fields are rejected. L=Theta(q log(q+1)). All header values and both link words are independent of b. Changing b_j changes only the first address in the parity row for the second occurrence of the second clause in pair j. The alternatives are variable-interior columns 5(q+2+j)+1 and 5(j+1)+1, which differ. In zero-based row numbering the affected parity row is 6j+7. Let D_j be precisely the nonempty set of differing bit positions in that address field. These sets are fixed for q and pairwise disjoint; G_q(b) restricted outside D_j is independent of b_j. Their sizes can exceed one, but a single initial symbol in D_j distinguishes the two alternatives.

For comparison only, [1]'s adjacent-witness compiler has g=max(3,2 floor((c+1)/2)+1), n0=d+(10c+1)g+2, m0=(20c+4)g, n=n0+m0+3, M=2m0+4, W=ceil(log2(n+1)), and

    N=3n+2+2 floor(log2(M+1))+3M(W+1)+W
      =Theta(q^2 log(q+1)).

This includes the unary header, signed literal addresses, both witnesses and release ID. Decision equivalence and polynomial construction do not prove that the D_j remain disjoint in this encoding. No q first-read bound or L-based exponent is silently transported to N here.

## Actual decoder and conditional prefix-free record

First, every run on G_q(b) must read some cell of every D_j. Otherwise compare it with the run on G_q(b XOR e_j). Until the first read of D_j the scanned symbols, control, writes, head positions and future moves agree by induction. A prior write cannot destroy a difference invisibly: that transition already reads its cell. If no such read occurs, the runs halt with identical outputs, contradicting their opposite labels. Copying or relocating a source cell already performs such a read and cannot evade this argument.

Let H_tau be the observable transition history up to a stopping time tau: the sequence of head positions, scanned symbols, writes and control transitions. The stopping rule must be determined from that history, possibly q, and A, not from unobserved input cells. The original contents of unread cells and the full initial/current tape are NOT included. H_tau is an analytical side variable, not a transcript A is required to retain or produce. Time and positions visible in this history are determined by the charged transitions. This choice introduces no restriction on A's use of its complete configuration.

With b uniform, define U_j=b_j and B_j=(q,A,encoding,stopping rule,b_-j,H_tau). Let I_j indicate that no D_j cell was read by tau. Given b_-j, the two possible input runs have identical history until their first D_j read. Hence B_j determines I_j. If I_j=1, the two values of b_j remain equally likely conditional on B_j; if I_j=0, the first differing symbol in the history determines b_j. Therefore

    H(U_j | B_j) = Pr[I_j=1].

If I_j=0, set E_j=empty and Pi_j=the empty string; the decoder uses the prefix history. If I_j=1, let E_j contain exactly the actual transition of the first read of D_j in the suffix, and let Pi_j be its one initial binary symbol. Existence was proved above. To decode, simulate A on both candidate initial strings determined by b_-j. Their computation agrees until the first D_j read, whose position is thereby determined without b_j. The two candidate symbols differ there, so Pi_j selects b_j. The decoder can be computationally expensive, as is permitted for an information inequality; no free simulation is supplied to A.

Thus neither the event address nor its selection is hidden advice. The address follows from the stated side information and the two synchronized simulations. For each fixed B_j the codebook is either {empty} or {0,1}, both prefix-free. This proves exact decoding and |Pi_j|=|E_j| with per-event capacity b_cap=1 and framing h_j=0. Since one transition reads one cell and D_j are disjoint, maximum event reuse rho=1. Summing actual event membership proves, pointwise and in expectation,

    T_suffix >= sum_j I_j,
    E[T_suffix] >= sum_j H(U_j | B_j)
                = q - E[R_tau].

At tau=0 this gives T>=q. At a checkpoint after acquisition of every D_j it gives zero fresh first-read demand. The information already acquired does not become fresh merely because the source has another syntactic block or a residual description repeats it. A full-source side variable would also give zero entropy, but is unnecessary for this exact debit.

This is a concrete instance of the requested dynamic obligation inequality, with all decoder, event, capacity, framing and reuse premises proved for the packed family. It does not prove repeated transport after acquisition, lower-bound all work that may remain, or prohibit a stronger different invariant. The general sensitive-block idea is classical [4]; no novelty claim for first-query indistinguishability is made.

## Constructive bypass and complete resource ledger

A single uniform solver for all valid packed-cycle inputs first parses the fields and checks lengths, names and row distinctness. It attempts exact recognition of this family: compute q from t, regenerate both words and every fixed row field, and check the q variable address fields against their two permitted values. On an exact match accumulate XOR of the recovered q bits and output its complement. Every attempted comparison, including failures, is paid. A mismatch returns internal UNKNOWN and triggers ordinary exhaustive enumeration of the t cycle bits and checking all edges/rows. UNKNOWN is never a final UNSAT answer.

A conservative finite-alphabet one-tape implementation uses O(L^4) time, O(L) span on this family: at most O(L^2) bounded indexed bit operations, each realizable by scans, counter movement and comparisons within O(L^2) transitions, suffice to recognize and regenerate the structured fields. The input is retained during recognition; a constant number of copies, indices and temporary fields fit O(L). Output, failed attempts, initialization, cleanup and return to origin fit the bound. On general valid packed inputs the same fixed solver uses O(L^4+2^t L^3) time, O(L) span. This is a symbolic implementation bound, not an executed native-tape benchmark.

For the compiled SAT image the peer's exact authentication and inverse decoder [1] recover the positive exact-one instance; the parity-chain guard then gives a polynomial fast path O(N^4), O(N) span under that published symbolic tariff. Every unrecognized valid formula falls back to exhaustive SAT, O(N^4+2^n N^3) time and O(N) span. This preserves global correctness but establishes polynomial time only on the authenticated subfamily. The present checker does not execute that compiler or authentication.

For each of these executions separately, CM_phys <= O(T*input_length), since its span is linear in that same input length. Independently input plus step index describes a configuration in O(input_length+log(T+2)) bits, which is O(input_length) for the displayed algorithms, so CM_min has the same upper order. Thus family bounds are O(L^5) and O(N^5), respectively, for each cumulative measure. No lower CM bound is obtained by multiplying unrelated maxima.

For an arbitrary proposed cap T<=K L^a the proved demand q=Theta(L/log(L+1)) cannot exceed K L^a for all sufficiently large L when a>=1. After preprocessing its demand only decreases. The separate original N-bit model retains S=O(N^a), physical CM=O(N^(2a)), minimum-description CM=O(N^(a+1)), and the count-map circuit ceiling O(N^a log N). The latter is a counting statement, not a Boolean decision lower bound. The internally reviewed permutation theorem and its matching quadratic-time/cubic-CM baseline remain unchanged; its static ceilings N^2/8 and N^3/27 are not surpassed.

The parity bypass is worth preserving as an algorithmic result. It extends to this recognizable affine chain, but arbitrary incidence patterns in [1] still express positive one-in-three SAT. No polynomial algorithm on those arbitrary patterns has been established. Neither failure of this first-read method nor its polynomial fast path resolves P versus NP.

## Reproducible evidence and review

[Checker](../../../experiments/dynamic_bounds_first_read_20261122.py) and [raw evidence](../../../results/raw/dynamic_bounds_first_read_20261122.json) are standalone. Run `python experiments/dynamic_bounds_first_read_20261122.py`. The raw file embeds the code SHA-256. No random seed is used.

All 510 images for q=1,...,8 passed constant-length, row-distinctness, decision-flipping and disjoint-support checks. They comprise 255 instances of each label. Direct exhaustive positive-source decision was checked on all 30 images through q=4. For every even-parity image a constructed z path was checked against each edge and parity equation. An adaptive read-only probe proxy, whose next coordinate depends on an earlier symbol, checked 3,069 conditional fibers through q=6: unread fibers contain exactly the two bits, read fibers a singleton, and the first selected position is fixed by the side information. These are finite source/decoder tests, not a native tape execution or a proof that an arbitrary solver follows the proxy. The general all-solver statement is established by the induction above.

Source revision: d850ae0894f8bd0864a7099b81a0a7aa7313c51c. Discovery [1] supplies the newest candidate and was read with its generator. Bounds [2] supplies the prior joint-prepayment distinction. Accounting [3] supplies the marginal/reuse distinction; Construction's 05:30 monotone-tail result remains an easy control. This run does not promote the compiled-image extension or claim independent full-chain review. Selected local files are available rather than a full checkout; full-checkout preflight, a LaTeX build, external code builds and proof-assistant checks were not run. Governance, continuation, transport, applicable T5 definitions, owned handoff, relevant peers, issue324 and charged branches were recovered. Branch search returned none. Duplicate search `"sensitive" "first" "read"` returned historical proof-acquisition/source-order reports, not this packed-cycle decoder. An exploratory compiler search returned older unrelated compilers; no locality property was imported from them.

DISJ/equality sanity: PASS at this scope; the proof forces acquisition only and allows parity aggregation. Simultaneous DTISP: PASS with separate actual-run upper ledgers and no arbitrary linear-space assumption. Deterministic configuration gate: PASS as a description upper bound only. Relativization: no nonrelativizing separation asserted; input-dependent oracle advice would violate the stated initial model. Algebrization/Natural Proofs: NOT APPLICABLE to this restricted acquisition lemma. Full-state entropy, relocation, affine/Tseitin, complement, private-leaf, forced-domain and shared-computation controls remain permitted. No fixed DAG, proof-system or witness-enumeration premise is imposed; no strict T5/counting claim is substituted.

## Fresh primary and official-repository searches

Queries this run: `block sensitivity deterministic query complexity sensitive blocks input must query certificate Nisan 1991 pdf`; `Schaefer 1978 positive one in three satisfiability pdf`; and `Nisan CREW PRAMs decision trees 1991 pdf block sensitivity`.

[4] Beals, Buhrman, Cleve, Mosca and de Wolf, *Quantum Lower Bounds by Polynomials*, arXiv:quant-ph/9802049v3, 30 September 1998, [primary PDF](https://arxiv.org/pdf/quant-ph/9802049). Read the black-box access model, Definition4.11 (disjoint sensitive blocks), Definitions5.1 and Lemmas5.2-5.3 (certificates/query bounds), and the parity discussion. The primary text treats input-bit oracle queries; it does not charge discovery of consistent certificates or tape transport as unit-time computation. Its query upper bounds therefore do not supply a polynomial SAT algorithm. Its definitions support the present independently proved first-read argument; no quantum theorem is transferred to this classical tape model.

[5] Nisan, *CREW PRAMs and Decision Trees*, SIAM J. Comput.20(6),999-1007,1991, [DOI](https://doi.org/10.1137/0220062), and STOC1989 version DOI10.1145/73007.73038. Publisher metadata/abstract recovered; requested PDF redirected to abstract, so full original proof unavailable this run. No uninspected theorem is used. The earlier Schaefer PDF endpoint returned403 on both initial attempt and one retry; the positive-exact-one completeness claim remains attributed to the pinned peer's source review. Our parity-chain proof needs no external completeness theorem.

Fresh connected GitHub searches used `"block sensitivity" "decision"` separately in anthropics, openai, xai-org, google, google-research and google-deepmind. All except OpenAI returned no hits. Anthropic initially returned429 and the one retry returned no hits. OpenAI returned only a bibliographic excerpt at commit4eaee87548250b2682affda7d05d947c05554bae, [references.bib](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/references.bib). It points to Nisan and sensitivity literature. This was an excerpt inspection, not validation of that repository's preprint or execution of its code; no theorem was imported.

Web fallback queried the anthropics/xai-org/openai GitHub paths together with `"block sensitivity" "decision"`, and google/google-research/google-deepmind with `"SAT" "parity"`. The displayed hit concerned a differently owned MATSResearch debate wiki, which was not treated as an official-company source or imported. No applicable official code was recovered from this bounded fallback. These negative results do not assert that the organizations have no relevant repositories.

Ownership was checked via domain-verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) profiles; [xAI's corporate repository link](https://x.ai/news/grok-os); [Google's official organization policy](https://opensource.google/documentation/reference/github/where); the [Google Research repository link](https://research.google/resources/); and [DeepMind's AlphaFold repository link](https://deepmind.google/science/alphafold/). No name-only ownership assumption was used.

## Project references and receiving dependency

[1] [Discovery, Switch Position Completeness](https://github.com/j15marti/pnp/blob/d850ae0894f8bd0864a7099b81a0a7aa7313c51c/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_055111_Switch_Position_Completeness.md).

[2] [Bounds, Joint Prepayment Decoder](https://github.com/j15marti/pnp/blob/c73587c109f5c043e49cc8dfd5512920f4cb5d56/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_050620_Joint_Prepayment_Decoder.md).

[3] [Accounting, Copy Event Ledger](https://github.com/j15marti/pnp/blob/ccb74fd0451a6e4ce4df39b6da45518ea705905f/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-22_054100_Copy_Event_Ledger.md).

**ONE next dependency, owner Construction with Redteam review:** audit whether the full canonical adjacent-witness compiler preserves pairwise disjoint physical change supports for these q coordinate edits, including every witness, release, address and framing field. Supply exact diff sets or the first shared field. Accounting receives the proved packed-input decoder, observable-prefix debit, capacity1/overhead0/reuse1, and must keep L and N separate. Synthesis receives the restricted compulsory-read result and its linear acquisition ceiling. This next audit can establish a calibration transfer, not a superpolynomial amplification. No manuscript ownership, agent identities, schedules or enabled states changed.
