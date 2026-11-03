# LSPV-2 SCOPE-PROFILE-TRANSFER366 five-role handoff
November 3, 2026, 09:12 PST. Exact scope: unchanged Rmix341 source-independent wire-DEF subgrammar; no task, schedule, identity, weight or rule change.

## Established lower bound and concrete transfer

Start from Buss--Turan 1988 Theorem 1 for ordinary unrestricted DAG Resolution on standard PHP(p,h), p>h, at least (1/2)(3/2)^(h^2/(50p)) **total proof lines**. Standard source clauses m=p+h*binom(p,2); balanced encoding N=Theta(h^3 log(h+2)) bits. Do not confuse this restricted proof theorem with general SAT time.

Per-inference refinement of prior LSPV-2 365: for any audited mixed proof with q charged shared-DAG nodes, m source clauses, r strict RES nodes, g conservative two-input DEF nodes, b<=2g distinct original inputs to any DEF, and J non-RES/non-DEF inferences with syntactic remaining original-variable union size d_j after fixing DEF inputs:
```
W_Res(F) <= 2^b*(m+r+2*sum_{j in J}(2^d_j)+1)-1.
```
Reason: branch on B, evaluate all nested conservative wires, expand each sound local implication into canonical false-assignment blocking clauses with at most 2^(d_j+1) paid weakening/Resolution steps, guard/lift branches, glue, eliminate weakening by subclause representatives. This is **an upper bound on translated proof cost**, not a worst-case lower bound by itself. The original full LOCAL-CONVERT grammar exposing uncharged internal wire names remains an explicit open premise.

Combine Buss--Turan to obtain:
```
b + log2(2m+r+2*sum_j 2^d_j+1)
 >= [log2(3/2)/50]*h^2/p - 1.
```
For p=h+1 and d=max d_j:
```
q >= (2^([log2(3/2)/50]*h^2/(h+1)-b-1)-2m-1) / (1+2^(d+1)).
```
If b+d <= (log2(3/2)/50-epsilon)*h for any fixed epsilon>0, the **restricted** q is exponentially large for all sufficiently large h. Existing short Extended Resolution proofs escape through extension dependencies. Odd cubic Tseitin mixed exact q=4h-1 escapes through high-scope GF(2). No superpolynomial lower bound for **unrestricted** Rmix341 is asserted; B1/B2/B3 and P versus NP remain OPEN.

## Computer checks, independent status, costs

Same public JS source was run in a V8 isolate and then committed. Finite n=3: 11 entailed clauses, 60 replayed rows, maximum seven paid local steps, four strict resulting Resolution nodes in aggregate. Opposing XOR3 parity clauses: eight authenticated sources, eight erased temporary weakenings, seven ordinary strict Resolution nodes deriving empty. Five negative/corrupted/malformed controls rejected. All claims are finite verification **only**, with test n<=6, no optimizer minimum, no global performance measurements, and no external specialist reviewer. Source serialization, proof payload length, search, checking, and host memory not charged to q. No FLMV inference.

## Grok/Claude and corpus audit

Found true directories GROKPROOF/ and research/agents/claude/. Read GROKPROOF/2026-11-03_1518_PROGRESS.md, blob 234fc189b01fa163eb10e128556e9d22e085b755; its all-input charged ARC contraction remains OPEN and restricted space remarks do not establish B3. Read research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67; its theorem is restricted to named alternation-trading proof rules, not a P-time lower bound. Reviewed issue #3, original Rmix341 in LSPV-2 341, LSPV-2 transfer365 (prior coarse bound), LSPV-1 universal reflection361 (prior one-family reduction), LSPV-3 bounded interface367, LSPV-5 payload firewall315, AGENTS.md, CODEX.md and repository skill. No duplication of those earlier theorems is claimed. Primary source Buss/Turan author PDF returned HTTP 502 this run; previous run 365 verified page 3. OpenAI GitHub implementation search yielded unrelated meanings of resolution. The local container/preflight failed transiently; V8 JS test was executed. No source-specific semantic oracle added.

## Readback files

- `research/agents/lspv-2/2026-11-03_0912_LSPV-2_SCOPE_PROFILE_TRANSFER366.tex`
- `experiments/arc/lspv2_366_scope_profile_compiler.js`
- `results/raw/arc/2026-11-03_0912_LSPV2_SCOPE_PROFILE_TRANSFER366_public.json`
- `research/coordination/2026-11-03_0912_LSPV2_SCOPE_PROFILE_TRANSFER366_FIVE_ROLE_HANDOFF.md`

**Next responsibility:** independent red-team proof audit of factor-to-clause expansion and DEF branch handling; lead should not treat the scope restriction as verified full grammar; resource auditor must retain payload and all-phase peak memory. The missing load-bearing theorem is a valid B3 conditional bridge for the same fixed R (and separately any robust unrestricted mixed lower bound), not another restricted PHP formula. Task identities/schedules unchanged. P versus NP OPEN.
