# PROOF-TRANSPORT RAND-SEEDFIREWALL1
Date: 2026-10-16 12:37 KST

Status: mathematical seed-fixing lemma and counterexample, not a P versus NP proof.

## Pre-search proposals
P1: Exact public-coin seed fixing for same-realization triangle transport.
P2: Fully charged verification and amplification of indexed 3-CNF falsified-clause outputs.
P3: Counterexample to per-input randomized success implying one globally successful seed.
P4: Check that no arbitrary SAT decider must emit a search protocol or proof.

## Core lemma
For a finite total relation R on X times Y, a randomized public-output protocol of worst-case communication c and per-input error epsilon admits a fixed globally correct public random seed if |X| |Y| epsilon < 1. Proof: The expected number of input pairs on which the fixed-seed protocol errs is less than one, so some seed has zero errors. Its deterministic transcript tree is a triangle DAG of depth at most c and size at most 2^(c+1)-1.

For indexed search, |X| |Y| = b^nu 2^(b nu). Full-domain seed fixing requires error less than b^(-nu) 2^(-b nu).

## Concrete counterexample
The public-coin equality protocol over n-bit strings sends two independent random parity hashes from Alice to Bob, followed by Bob's one-bit public verdict. It communicates three bits and has error exactly one quarter for each unequal input pair, zero on equal inputs. For every fixed seed and n>=3, the two-by-n hash matrix has nonzero kernel, so some unequal pair is falsely declared equal. Per-input correctness does not imply a globally correct seed.

## Indexed 3-CNF amplification cost
A proposed false source clause can be verified publicly using at most 3(ceil(log2 b)+1) communication bits: Alice sends up to three pointers, Bob sends the corresponding data bits. Repeating an error-at-most-one-third protocol k times with independent coins reduces error to 3^(-k). The full-domain union bound requires k > (b nu + nu log2 b)/log2 3, hence the generic unrolled protocol-tree size bound cannot certify the ROUNDINGSQUEEZE5 small-size requirement, although more efficient DAG compression could exist.

## Full proof-system audit
Compiler counts: specialized Tseitin 24n variables / 32n clauses; general selector compiler 72m / 96m; compiled OR shield for q=m_A+m_B has 144q / 192q, encoded bits Theta(q log q). Integer syntactic Cutting Planes transport is guarded and depth-sensitive, not semantic CP. PC/PCR projection preserves expanded monomial size and degree over each field; all-field graph-colouring source is distinct from characteristic-two-easy Tseitin. Real SoS substitution, strict Resolution projection, and same-realization triangle lifting remain separate resource models.

## Decider firewall
An arbitrary polynomial-time SAT decider returns only SAT/UNSAT. For the fixed contradictory formula (z) AND (NOT z), the SAT answer is constant but indexed false-clause search still requires communicating the indexed bit. There is no automatic decider-to-Resolution, Cutting Planes, PC/PCR, SoS or triangle-DAG extractor. TRACEFRONT1 and the TQBF oracle objection continue to apply. P versus NP remains open.

## Computational audit
Exhaustive parity tests: 294132 seed/difference pairs across dimensions 1 through 6, with all n>=3 seeds having a collision. Twenty-four rational-arithmetic amplification checks passed. For n=5, 1024/1024 seeds have collisions. For b=4,nu=4, union-bound k=16, verification cost 9 bits and amplified worst-case communication 160 bits at base c=1, versus maximal RS5 log2 size cap 8 bits.

Script SHA256: a0631a3075418da79fb2599de2ae26905a2d3ca2fd948b85137cda33c50c631b
Results SHA256: 3d0320ce0a4a68eca43e8237e39f3e436388470d9fa4f0a827a2b39de061e489

## Handoff
Closed: randomized full-domain correctness condition, verification cost, no-global-seed counterexample and amplification budget diagnosis.
Open: a nonrelativizing arbitrary-decider-to-same-realization lower-bound-covered structure. Next: robust distributional triangle lifting with explicit error measure and quantifier order.

## Literature
Cook and Reckhow (1979): https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf
de Rezende et al. (STOC 2025): https://arxiv.org/abs/2411.14267
Conneryd et al. (2025): https://arxiv.org/abs/2503.17022
