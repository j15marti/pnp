# AMPLIFY-FIX-SELECTOR4 handoff | 2026-10-20 02:48 Asia/Seoul

## New exact result

For a finite slice `X_n`, independent repetition followed by majority voting gives per-input error `epsilon_r`. If `|X_n| epsilon_r<1`, a union bound proves one seed tuple works for every input in the slice. This repairs REDTEAM20's `forall x exists-good-seed` counterexample only as nonuniform advice. It does not find the tuple uniformly, preserve a target promise automatically, or produce ordinary total MKTP.

Exact audit: all 512 three-input/three-seed matrices; six REDTEAM20 counterexamples; each repaired by majority tuple `(0,1,2)`. Exact rational minimal odd repetitions for domains of size `2^n`, `n<=64`; largest is `r=701` at `n=64`; 646 assertions, zero failures.

## Mandatory next falsifiers

- **:00:** amplify the actual Ilango oracle event or prove why it cannot yield a source-checkable ordinary total target. No concrete-hash substitution.
- **:12:** build the `exists Z forall x Good(x,Z)` search with exact input scale and unknown exponent; identify every call to SAT/target verification and peak live state. A certified fastest portfolio does not bound the exponent.
- **:24:** charge selector construction plus target materialization in the same random-access machine as the proposed ARC successor; test both outputs and delayed deciders.
- **:36:** attack independence, promise validity, advice uniformity, and any retained `M`-bit source. Also keep `exists W forall i` separate from `forall i exists W_i`.
- **:48:** retain as CONDITIONAL/nonuniform until a fully uniform total `R_k` exists.

Compact History remains a diagnostic, not a third route. Root `main.tex` remains unsafe and untouched. **P versus NP OPEN.**

END_OF_VERIFIED_HANDOFF::AMPLIFY_FIX_SELECTOR4
