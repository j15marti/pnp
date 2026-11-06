# LSPV-5/REFEREE389 five-role handoff | 2026-11-06 08:48 PST

**Route B LSPV-5 primary; exactly two Route A and three Route B roles remain unchanged. P versus NP OPEN.**

## New result

**PROVED/RESTRICTED:** For a minimally unsatisfiable split CNF $L(X,b)\wedge R(Y,b)$ with disjoint private variables, both sides satisfiable, any strict pure-Resolution source-once refutation normalizes into full-source side derivations $L\vdash b$, $R\vdash\neg b$, and one final RES. Minimality forbids the wrong bridge polarity, restriction by a model of the opposite side preserves every local source, and lifting restores only one bridge polarity.

**FALSIFIED/REPAIRED:** Without MUS, the theorem is false. The five-source 2-CNF

$$
(b\lor\neg x),(b\lor x),(\neg y),(\neg b),(\neg b\lor y)
$$

has a four-step interleaved source-once refutation but no full-source right-unit derivation. Its deletion model counts $(1,1,0,0,0)$ expose the missing hypothesis.

## Bridge consequence

The authenticated 36-clause bridge core is MUS; its 18/18 sides share only $x_{15}$, are satisfiable, and force opposite bridge units with the correct one-sided polarity. REFEREE388 excludes both full-source side-unit trees. Therefore **every pure-Resolution 35-node bridge tree is impossible, including interleaved trees**, and the restricted bound is

$$
W_{\mathrm{RES}}(F_{\mathrm{bridge}})\ge36.
$$

The full mixed interval remains $35\le W_{R_{\mathrm{mix341}}}(F_{\mathrm{bridge}})\le37$ because a 35-node AND3/XOR/RES tree is not excluded.

## Verification

- bridge core: 0 models; every deletion 16 or 32 models;
- sides: 1,024 models each; exact shared variable 15; forced opposite signs;
- imported REFEREE388 raw and independent verifier authenticated by exact SHA-256;
- independent new replay: 119 grouped checks; five hostile mutations rejected;
- finite controls: 77 small minimal-entailment width-three sets and 36 non-ROR MUS gadget pairs, no counterexample; non-load-bearing because the symbolic theorem is complete;
- no authoritative historical byte checker executed.

## Role handoff

**LSPV-1:** use the new pure-RES exclusion only at its stated restricted scope; do not promote it to mixed or asymptotic hardness. Attack mixed 35-node tree grammars and noncircular B3 independently.

**LSPV-3:** test whether any exact assumption-safe AND3/XOR consequence can fit a source-once 35-node tree without LOCAL; source implication is not exact annotation.

**LSPV-2/4:** Route A may use the bridge only as a finite proof-structure control. It supplies no same-machine contraction or FLMV bound.

## Remaining gap

Construct or exclude a legal 35-node mixed AND3/XOR/RES tree, then analyze the three 36-node topology classes. Full mixed superpolynomial $\overline W_R$, B1/B2/B3 and P versus NP remain **OPEN**.

Report: `research/main/2026-11-06_0848_MAIN_MUS_CUT_NORMALIZATION_REFEREE389.md`.
