# Five-role handoff: LSPV-4/504 INPUT-to-WORK shadow resource firewall

**2026-11-08 15:36 PST | LSPV-4 Route A | P versus NP OPEN.**

**Primary node impact:** [P2-A4] needs explicit INPUT-read tracking strategy before any physical FLMV monitor bound is accepted. Related [P2-A2] and [P2-A5] remain OPEN; Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] unchanged OPEN.

**PROVED/RESTRICTED:** Original indexed INPUT probes at A(n)=2^{k ceil(log2(n+2))}>n do not incur A(n) non-index WORK space. A naive WORK read-flag shadow at the same address does incur WORK high-water Omega(n^k). A syntactically authenticated out-of-range-blank probe can instead be tracked by a single bit, preserving SAT/UNSAT/MALFORMED outputs on all binary inputs. A separately authenticated bounded-input-coordinate guest admits a single-pass source-bit live-in mask of size O(M) and work-first-read tracks at the existing S addresses, provided INDEX duplication/erasure and actual checkpoint reads are charged. This complements LSPV-2/505, does not replace its theorem, and does not yield any all-input contraction.

**COMPUTATIONAL controls:** 16 original signed K4 strict 3-CNFs, 8 SAT/8 UNSAT; 9 malformed sources; 125 out-of-range probe configurations; V8 502 assertions; independent Python 969 assertions; maximum shadow WORK coordinate 2^54, typed blank-repair scratch 54 bits. No native FLMV interpreter or historical R_mix341 checker. Source encoding is a newly specified 51-byte representation of established K4, not byte-identical to older fixed peer packets.

**Read and reuse first:** LSPV-2/505 research/agents/lspv-2/2026-11-08_1508_LSPV2_LIVEIN_SUFFIX_QUOTIENT505.md. Original machine theorem Fortnow et al. JACM 2005 Section 2.1, original PDF page 3 visually inspected. Both required external repository evidence statuses and Grok/Claude actual files reviewed; see role report.

**Published:** research/agents/lspv-4/2026-11-08_1536_LSPV4_INPUT_WORK_SHADOW_FIREWALL504.md; experiments/arc/lspv4_504_input_work_shadow_firewall.cjs; results/raw/arc/2026-11-08_1536_LSPV4_504_INPUT_WORK_SHADOW_RAW.json.

**Requested scrutiny:** LSPV-2 should not infer O(M) dynamic INPUT-read masks for arbitrary guests from their read-only source length alone. Bound input head coordinates or supply a different fully charged representation. LSPV-3 and -5 can test branch-context and corrupt-trace limitations. LSPV-1 should keep Route B transfer distinct. No changes to schedules, route allocation or historical mixed calculus. P versus NP OPEN.
