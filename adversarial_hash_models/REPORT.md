# Short-digest normalized-residual cache red team

Status: **COMPUTATIONAL**

This experiment tests whether 4, 6, or 8 hexadecimal digits of a normalized
residual hash can safely stand in for the residual itself. It does not prove an
asymptotic SAT statement.

## Source-checkable finite family

For 19 tag bits, the common parent has one control selector `p`, selectors
`x_j`, disjoint tag pairs `(y_j,z_j)`, and two gated XOR cores. Each tag gadget
is

```text
(x_j OR y_j OR z_j) AND (-x_j OR -y_j OR -z_j).
```

After assigning `x_j`, the normalized residual contains exactly one of
`(y_j OR z_j)` and `(-y_j OR -z_j)`. The control selector activates either a
satisfiable even XOR triangle or a contradictory odd XOR triangle. Therefore:

1. There are `2^20 = 1,048,576` syntactically distinct normalized residuals.
2. Exactly half are SAT and half are UNSAT.
3. Each residual has 25 clauses, 41 variables, and 20 connected components.
4. The direct residual generator was checked against restriction, unit
   propagation, and normalization on eight boundary histories.
5. The two three-variable cores were exhaustively checked: even is SAT and odd
   is UNSAT.

The hash is SHA-256 of the ASCII serialization of the normalized tuple,
truncated to the requested output width.

## Collision search

| Digest | Histories searched | Distinct digests | Collision insertions | Colliding buckets | SAT/UNSAT buckets | Largest bucket | Colliding pairs | Runtime |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 hex / 16 bit | 100,000 | 51,346 | 48,654 | 29,520 | 18,688 | 9 | 76,125 | 2.53 s |
| 6 hex / 24 bit | 250,000 | 248,192 | 1,808 | 1,796 | 846 | 3 | 1,820 | 5.09 s |
| 8 hex / 32 bit | 500,000 | 499,964 | 36 | 36 | 18 | 2 | 36 | 9.66 s |

The birthday-model expected pair counts were 76,293.18, 1,862.64, and 29.10,
respectively. This agreement is descriptive only. No random-oracle premise is
used in the correctness conclusions.

Concrete cross-answer witnesses include:

| Digest width | Digest | SAT history | UNSAT history |
|---:|---:|---:|---:|
| 4 hex | `4aed` | 12,560 | 29,291 |
| 6 hex | `059763` | 62,350 | 14,931 |
| 8 hex | `1c8a2dec` | 152,478 | 253,005 |

All saved collision witnesses were independently rehashed after the run.

## Cache-policy comparison

The adversarial replay workload uses up to 96 collision buckets, 256 singleton
keys, and four passes. It is intentionally collision-focused, not an estimate
of an average application workload. Storage is logical serialized payload. It
excludes Python object, dictionary, allocator, and process overhead, and charges
one byte per stored Boolean answer.

| Digest | Policy | Correct | Wrong replies | Leaf evaluations | Logical bytes | Equality comparisons | Equality token visits | Regenerations |
|---:|---|:---:|---:|---:|---:|---:|---:|---:|
| 4 | no cache | yes | 0 | 3,640 | 0 | 0 | 0 | 0 |
| 4 | hash only | **no** | 1,288 | 352 | 1,056 | 0 | 0 | 0 |
| 4 | hash + full-key verification | yes | 0 | 910 | 238,664 | 10,426 | 302,700 | 0 |
| 4 | full key | yes | 0 | 910 | 237,960 | 0 | 0 | 0 |
| 4 | hash + source replay | yes | 0 | 910 | 5,091 | 10,426 | 97,950 | 7,696 |
| 6 | no cache | yes | 0 | 1,836 | 0 | 0 | 0 | 0 |
| 6 | hash only | **no** | 404 | 352 | 1,408 | 0 | 0 | 0 |
| 6 | hash + full-key verification | yes | 0 | 459 | 120,040 | 1,849 | 107,252 | 0 |
| 6 | full key | yes | 0 | 459 | 118,984 | 0 | 0 | 0 |
| 6 | hash + source replay | yes | 0 | 459 | 3,639 | 1,849 | 3,977 | 472 |
| 8 | no cache | yes | 0 | 1,312 | 0 | 0 | 0 | 0 |
| 8 | hash only | **no** | 72 | 292 | 1,460 | 0 | 0 | 0 |
| 8 | hash + full-key verification | yes | 0 | 328 | 85,554 | 1,128 | 76,620 | 0 |
| 8 | full key | yes | 0 | 328 | 84,386 | 0 | 0 | 0 |
| 8 | hash + source replay | yes | 0 | 328 | 3,227 | 1,128 | 2,820 | 144 |

Hashing the residual is not free merely because the output is short. The 4,
6, and 8 digit cache workloads fed 948,200, 474,100, and 336,232 serialized
input bytes to the digest computation. Full-key verification then incurred the
additional equality work shown above.

The source-replay policy stores the 747-byte common parent once, plus a
three-byte history descriptor and one answer byte per residual, plus digest
buckets. It remains exact here because the fixed history-to-residual map is
syntactically injective. Its regeneration output was 584,896, 35,872, and
10,944 formula tokens for the three workloads. For a general wrapper, this
policy would require a uniform proof that the stored source record identifies
or regenerates the exact residual, with all parent, history, regeneration, and
comparison costs charged.

## Delayed-history separation

Hash collisions are not harmless when both residuals currently have the same
SAT answer. For any two histories that differ at tag bit `j`, assigning
`y_j = z_j = false` falsifies the positive tag clause and satisfies the negative
tag clause. Thus two currently SAT residuals can have different answers after
the same later restriction.

The saved collision buckets supplied 24 such SAT examples at 4 hex digits, 5
at 6 digits, and 10 at 8 digits among the bounded pairs recorded by the audit.
This rejects a cache contract based only on “same current SAT bit.” Such a
contract is weaker than interchangeable residual state.

## Pigeonhole comparison

The separate pigeonhole audit produced two useful controls.

1. In `PHP(9,8)`, 1,680 legal histories placing four pigeons produced 70 raw
   source-labelled residuals but one normalized residual. This is a genuine
   exact symmetry merge.
2. Among 1,024 arbitrary ten-variable prefixes of `PHP(5,4)`, there were only
   33 distinct normalized residuals. All are UNSAT because they restrict an
   UNSAT parent. No 4, 6, or 8 digit collision happened in that 33-residual
   set. More importantly, a current-answer-only audit would be unable to detect
   an erroneous identity merge there because every answer is UNSAT.

## Narrow conclusion

The finite countermodels establish the following for the tested cache design:

1. Truncated digest equality alone is not an exact residual-identity rule.
2. Full-key verification repairs correctness, but it retains the full residual
   and adds digest/index overhead. It is not a compression theorem.
3. Source replay can reduce retained payload on this structured family, but it
   moves the burden to source/history storage and verified regeneration. This
   is the only tested direction that could support compact exact keys, and its
   injectivity and total work are family-specific.
4. Syntactic normalization can merge strong symmetries, as the pigeonhole
   control shows, but the independent tag family prevents any general claim
   that normalization yields enough merges.

The remaining proof obligation is therefore not “find short hashes.” It is a
uniform, source-checkable residual identifier or replay rule whose exactness,
construction work, collision verification, retained state, and recursive use
all satisfy the claimed bounds on every input in scope.

## Exact limitations

1. These are bounded chosen-input searches, not asymptotic collision lower
   bounds and not a P versus NP argument.
2. The construction targets one syntactic normalization. It does not rule out a
   stronger semantic canonical form, though computing such a form must itself
   be charged.
3. Collision-focused replay exaggerates hash-only failure rates and cannot be
   read as an average-case rate.
4. The SAT labels are proved from the explicit family structure, not obtained
   from a general SAT solver.
5. Logical byte and token counters are implementation-independent proxies, not
   resident-memory or wall-time models.
6. A larger 8-digit multicollision was not found in the bounded search. The
   strongest 32-bit witnesses are pairs. The largest 16-bit and 24-bit buckets
   had 9 and 3 residuals, respectively.

## Reproduction

```bash
python red_hash_cache_models.py collision --hex-digits 4 --samples 100000 --output collision_4hex.json
python red_hash_cache_models.py collision --hex-digits 6 --samples 250000 --output collision_6hex.json
python red_hash_cache_models.py collision --hex-digits 8 --samples 500000 --output collision_8hex.json
python red_hash_cache_models.py pigeonhole --output pigeonhole_audit.json
```

Each recorded invocation completed below the program's 24-second wall-clock
alarm.
