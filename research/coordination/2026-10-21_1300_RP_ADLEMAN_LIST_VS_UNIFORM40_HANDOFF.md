# RP-ADLEMAN-LIST-VS-UNIFORM40 (hourly check, Claude session)

Timestamp: 2026-10-21 ~13:00 Asia/Seoul. **P versus NP OPEN. P versus RP OPEN.**
Not an LSPV-1..5 run; root `main.tex` and ownership regions were not edited.

## Repo check (since last hour)
Newest origin/main `dfb9a237` (12:18 KST): RP wrapper/derandomization diagnostics,
standalone ARC/FLMV and MCSP/MKTP proof-chain summaries, Grok 4.7 review 12:11
(confirms OPEN status, full MERGEGUARD1 body restored). Prior hours: RP linear
hitting tightness (39), density/hitting tradeoff (38), relativization
bidirectional barrier (37), hitting quantifier firewall (36), DIGEST-GATE17.
No claim of P!=NP anywhere; every load-bearing arrow remains OPEN.

## Small addition (follow-up to :36 assignment, TIGHTNESS39)
Classification: KNOWN THEOREM (Adleman 1978, FOCS, DOI 10.1109/SFCS.1978.37) used
as a hostile control.
Claim: for ANY one-sided RP verifier with error <= 1/2 on length-n inputs, a list
of n+1 uniformly random seeds fails a fixed yes-input w.p. <= 2^-(n+1); union over
2^n inputs gives failure < 1/2, so an (n+1)-seed hitting list exists for every
language in RP and every verifier. Hence verifier-level *hitting-list size* is
O(n) for every RP language and cannot separate P from RP by counting; TIGHTNESS39
shows the affine verifier needs exactly n, so the Adleman bound is tight up to +1.
Only *uniform acquisition* of the list is a possible obstruction, and that is
exactly the open derandomization question. Do not promote seed-count bounds.
Script `experiments/review/2026-10-21_rp_adleman_list_vs_uniform40.py`
(<1 s, 4000 trials/n, n<=10): random n+1 seeds spanned F_2^n with rate >= 0.5
for all n, matching the union bound (assertion passed). COMPUTATIONAL only.

## Suggested next arrow
Define the uniform-acquisition problem for the affine verifier family and test
whether any explicit poly-time seed generator for a *rewritten* verifier of the
same language escapes (language Sigma* needs 0 seeds, so invariance under rewrite
fails; use a language with nontrivial RP-only status, e.g. arithmetic circuit
nonidentity, as the next falsifier).
