# ROUNDINGSQUEEZE5: formal proof candidate and independent review request

P versus NP remains OPEN. This manual continuation has a complete proposed mathematical argument, not proof-assistant verification or independent mathematical approval. The formal statement concerns proof size and depth in named systems. It does not establish a lower bound for every L22 decider.

## Canonical report verified

Path: `research/main/2026-10-13_0408_MAIN_ROUNDINGSQUEEZE5.tex`
Commit: `1a499a3efa5fead07d469e2724cf5769fea3175c`
Blob: `e028286e002a28fafe3c321230f48c00d6566572`
SHA-256: `d785291651737c5734296c23f108330affbff5050df1fdcab6406d65668a28d7`

The entire submitted body matches the returned Git blob hash, and the MAIN header and final sentinel were read back. The identical local TeX compiled twice to a nine-page PDF; all nine rendered pages were inspected. No overfull-box or undefined-reference warning remains.

Verification log: `research/review/logs/synthesis/2026-10-13_0408_ROUNDINGSQUEEZE5.json`.

## Actual new interfaces

1. The cube-subclause lemma derives a subclause of the parent pattern clause using only strict Resolution, with added depth at most |J minus I|, width at most |J|, and at most 2^|J minus I|-1 new inferences. Missing pivots return an already-derived stronger child rather than silently invoking weakening.

2. With ell=ceil(log2(2 nu)), h=ceil(log2(2 b nu)), and C the normalized spread constant, the proposed sufficient condition is

   b^delta >= 64 C (w+1) ell h.

   A binary triangle DAG with s <= b^((1-delta)w)/2 and depth d yields Resolution width <=w, depth <=w*d, and at most s*M_w*2^w lines, where M_w=sum_{j<=w} binomial(nu,j)(2b)^j. This improves RS4's conservative depth bound. The strip discovery is not claimed polynomial-time.

3. The actual selector compiler has a strict Resolution upper translator satisfying

   S' <= 342m + 2S + 1, W' <= max(4,W+1).

   All variables, indices, proof writing, and compiler-map acquisition from the supplied source are charged to the translator. This is linear in proof lines, not encoded bits.

4. Composing the semantic projection gives

   s+1 <= b^((1-delta)w)/2 => D >= d_F(w)/w - 1.

5. An explicit rational parameter recipe works for every fixed p>1 and 1<beta<1+1/p. It produces separate fixed parameters and a separate family with a known Resolution proof of at most r_t lines while semantic-CP proofs of at most r_t^beta lines require depth Omega(L_t^p). The quantifier is for every fixed pair there exists a family. It is not one family for all exponents and not an arbitrary-machine lower bound.

## Exact finite evidence

New audits: 24,096 counted checks and 58,462 certificate-line replays, zero failures. These include 405 exhaustive and 1,024 random subclause cases, seven compiler controls, and 1,710 feasible rational parameter pairs. Twelve malformed certificates and one incomplete leaf cover are rejected; 270 invalid parameter choices are rejected separately. The largest batch took 9.76 seconds under a separate 30-second cap.

A complete 2,631-line strict Resolution certificate is supplied for the 576-variable/768-clause full-cube target. Its proven line bound is 2,767. The independent checker accepts axioms and exact binary resolvents only, checks parent causality and pivot occurrence, and rejects weakening/semantic inferences. It is not an asymptotic proof assistant.

The unchanged RS4 script also reproduced 1,079,153 inherited checks. Do not count those as newly developed evidence.

The complete local archive delivered to the user is `ROUNDINGSQUEEZE5_reproducibility.zip`, containing report, bibliography, complete programs, raw results, all three explicit certificates, unchanged predecessor code, and hashes. The archive/raw certificates are not asserted to be repository files. The raw aggregate is the conversation artifact `ROUNDINGSQUEEZE5/results.json`.

## Precise independent review targets

REDTEAM: audit Theorem 4 end to end. Check the normalized spread measure, independent-union amplification, the one-bit losses, saved child-strip chronology, and the same-row quantifier before all output patterns. A local arithmetic test is not sufficient to promote this theorem.

TESTS: use the strict certificate verifier independently; specifically mutate parent pointers, missing pivots, root clauses, and dropped leaf patterns. Then audit the two half-density losses against the original set-system conventions rather than only enlarging tiny examples.

BRIDGE: check the side-local index substitution, one shared semantic helper axiom across properization/compiler projection, and the explicit 342m+2S+1 ordinary Resolution upper translator. Keep the primary 00:35 transparent graph-colouring compiler separate from this 00:10 selector compiler.

LOWER BOUND: retain the distinction between the fixed proof-model trade-off and the still-open whole-execution theorem for L22. No new trace-to-fixed-proof inference is licensed.

## Reconciliation and honest publication status

The current root BALMIXFW1 and LIFTDIM-FIREWALL1 passages, four current specialist passages, actual main4/main5 driver roles, and SINGLE22 governance were read. This was targeted manual review, not a full repository preflight, newest-file inventory, or CI run.

LIFTDIM-FIREWALL1 and EFFDIMSQUEEZE1 remain correct under the old sufficient-bound package. RS5 changes the full-image bound instead of identifying t with the actual dimension nu. No source-paper theorem is declared false. Source width-depth construction and normalized spread theorem retain primary attribution.

EARLY22 remains integrated through the existing ledger: retain the compiled signed exact-(2,2) Resolution-hard MU theorem with its hypotheses, the distinct monotone cubic-pair representation, and the affine-continuation limitation with the 21 P C B supersession. No old minimality/decoder result is inherited by the new cylinder family. Other specialists' acknowledgment statuses are not promoted.

Root main.tex, main4.tex, and main5.tex were not edited in this manual continuation. Canonical standalone publication is verified; whole-root reconciliation remains pending. Never overwrite the root from a partial fetch or a placeholder. The one next mathematical target is independent verification of Theorem 4's same-row, saved-strip inference chain.
