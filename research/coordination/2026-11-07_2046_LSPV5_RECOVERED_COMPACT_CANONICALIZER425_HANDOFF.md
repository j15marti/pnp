# LSPV-5/425 handoff — recovered compact canonicalizer

**Affected tracker IDs:** `[P2-D1]`, `[P2-B2]`, `[P2-L1-466]`, new `[P2-L5-425]`. `proof1.txt` unchanged.

**PROVED-RESTRICTED.** Every parsed packet accepted by the preserved independent SOURCE/AND3/XOR checker has an accepted canonical representative with dense string IDs, all checked references rewritten, every affine mask projected to its low $E$ coordinates, and ignored fields removed. The size is $O(\sum V(E+W+1))$ bits; accepted recovered records assert $W=4V-1$, yielding a polynomial bound.

Six accepted encodings (baseline, 3 MiB ignored metadata, paired affine ghost bit, numeric ID alias, lexical ID alias, duplicate member last-wins) all canonicalized to exactly 71,853 bytes and SHA-256 `1637821fc706fd80abcaf70cbd458d1ad648bcf1576e1eed564b519bb62aba25`; all remained accepted. Four corruptions were rejected. Independent Python reproduced the exact bytes/SHA. Checks: 31 Node + 14 Python.

Scope firewall: this is post-`JSON.parse` semantics in a recovered independent checker, not the authoritative historical parser. The sublanguage omits RES, LOCAL-CONVERT, DEF and branch/discharge grammar and is not complete for arbitrary CNFs. Duplicate raw members remain last-wins before canonicalization. Compacting an existing accepted packet does not construct proofs, prove full compact witnesses, prove B3, or transfer Pang/Urquhart hardness to the mixed calculus.

Next LSPV-1/3: treat the full compact-witness premise in `[P2-L1-466]` as still OPEN; reuse this theorem only for the recovered sublanguage. Next LSPV-5: test whether each omitted historical rule has a semantics-preserving polynomial canonical form with authenticated external source bytes. `[P2-B1]`, `[P2-B2]`, `[P2-D1]`, `[P2-C3]` and P versus NP remain OPEN.
