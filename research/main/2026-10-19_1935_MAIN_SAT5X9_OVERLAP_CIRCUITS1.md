# SAT5X9-OVERLAP-CIRCUITS1

Date: 19 October 2026. Status: exact Boolean theorem, tested combinational Verilog implementations, raw-input global minimum OPEN. P versus NP OPEN.

## Exact 9-clause theorem

Let F consist of exactly 2^k+1 clauses of width k, each using k distinct variables, on n>=k Boolean variables. Let S_i denote the assignments falsifying clause i. Then

  UNSAT(F) iff W(F) = sum_{i<j} |S_i intersection S_j| = 2^(n-k).

Proof. Set r(x)=sum_i 1[x in S_i]. Each indicator is a multilinear real Boolean polynomial of degree k. Under UNSAT, e(x)=r(x)-1 is nonnegative integer-valued and has degree at most k. Its total mass is (2^k+1)2^(n-k)-2^n = 2^(n-k). By the polynomial minimum-support lemma, every nonzero real multilinear degree-at-most-k polynomial on the n-dimensional Boolean cube has at least 2^(n-k) nonzero evaluations. Hence e takes value 1 at exactly 2^(n-k) assignments and 0 at all others. Thus r(x) is either 1 or 2 and W=sum_x binomial(r(x),2)=2^(n-k). Conversely let U denote union size and D=(2^k+1)2^(n-k)-U. Since U<=2^n, D>=2^(n-k). Since binomial(r,2)>=r-1 for r>=1, W>=D. Thus W=2^(n-k) forces U=2^n and UNSAT.

The minimum-support lemma follows by induction from p=p_0+x_n q. If q=0, support doubles; otherwise wherever q is nonzero at least one of the two slices of p is nonzero. This is the classical type of minimum-weight bound underlying Reed-Muller codes; the real-field proof here is explicit.

For nine proper three-literal clauses on five variables, UNSAT iff W=4. The 36 clause pairs contribute weights 0,1,2,4 based on sign conflicts and shared-variable sets. For eight proper clauses, UNSAT instead requires pairwise disjoint falsification sets. This stronger eight-clause shortcut does not extend to nine.

## Independent minimally UNSAT nine-clause example

The five variables are a,b,c,d,e. The nine clauses, in order, are:
1. NOT a OR b OR c
2. a OR NOT b OR c
3. NOT a OR NOT b OR c
4. a OR b OR NOT e
5. NOT a OR b OR NOT e
6. a OR c OR e
7. NOT b OR NOT c OR d
8. NOT b OR NOT c OR NOT d
9. b OR NOT c OR e

Its seven-bit proper clause codes are 1,2,3,20,21,32,51,55,58. All 32 assignments fail, but deleting any one clause gives a satisfying assignment. The respective private witnesses, bit order a,b,c,d,e, are 10000,01001,11000,00001,10101,00000,01100,01110,00100. Only two pairs of clause-exclusion squares intersect, each in two assignments, so W=4.

## Actual emitted netlist inventory

Proper raw interface: 9 clauses times 7 bits, 63 bits total. Each clause specifies one of ten distinct-variable triples by four-bit index plus three polarity bits. General raw interface: 27 signed-literal slots, four bits each, 108 bits, including repeated literals and tautological clauses. Both reject invalid input codes. All output one SAT bit.

Primitive nominal static CMOS device proxies: INV 2, BUF2 4, NANDk/NORk 2k, AND2/OR2 6, XOR2 16. G is the functional gate count, P gate input-pin incidences, E=P+1 the logical connections including output, W=primary-input bits+G distinct driven nets, B separately emitted noninverting fanout-two buffers. Physical routing/delay, transistor-net topology, true switching and energy are unmeasured.

| Interface and architecture | Inputs | G | P | E | W | Depth | B | Core nominal MOS | With buffers MOS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Proper raw, cover using rails, fan-in <=16 | 63 | 1145 | 3367 | 3368 | 1208 | 15 | 1773 | 6734 | 13826 |
| Proper raw, shared-presence, fan-in <=16 | 63 | 1238 | 3421 | 3422 | 1301 | 12 | 1663 | 6842 | 13494 |
| Proper raw, fan-in <=4 | 63 | 1671 | 3425 | 3426 | 1734 | 23 | 1143 | 6850 | 11422 |
| Proper raw, naive weighted overlap, fan-in <=16 | 63 | 2885 | 6666 | 6667 | 2948 | 91 | 2569 | 18320 | 28596 |
| General raw, shared complements | 108 | 1548 | 5111 | 5112 | 1656 | 11 | 2592 | 10222 | 20590 |
| General raw, direct decoder | 108 | 1602 | 7001 | 7002 | 1710 | 10 | 4806 | 14002 | 33226 |
| Precomputed 80-bit presence | 80 | 38 | 357 | 358 | 118 | 5 | 160 | 714 | 1354 |
| Precomputed 90-bit literal rails | 90 | 646 | 2085 | 2086 | 736 | 8 | 1260 | 4170 | 9210 |
| Precomputed independent 288-bit table, two-input | 288 | 287 | 574 | 575 | 575 | 9 | 0 | 1720 | 1720 |
| Independent 288-bit table, high fan-in | 288 | 34 | 321 | 322 | 322 | 3 | 0 | 642 | 642 |

Among tested full proper raw circuits, 1145 gates and 6734 nominal unbuffered MOS are lowest; 11422 nominal buffered MOS on the fan-in-four version is lowest after abstract BUF2 completion. Among tested unrestricted general raw circuits, the 1548-gate version wins. The 288-bit independently supplied table has a PROVED minimum of 287 two-input gates because all 288 input bits are essential; the emitted netlist has 256 OR2, 30 AND2 and one NAND2. This minimum EXCLUDES raw-input-to-table conversion; no global raw-input gate or transistor minimum is proved. The 63 and 108 raw bits are all shown essential, yielding weak lower bounds of 62 and 107 two-input gates.

## Five-variable eight-to-nine clause comparison

Proper raw: 8 clauses = 56 input bits, 757 gates, 4024 core MOS, 7448 buffered MOS; 9 clauses = 63 bits, 1145 gates, 6734 core MOS, 11422 best buffered MOS. This is +388 gates, +2710 core devices, +3974 buffered devices for the chosen architectures. General raw: 8 clauses = 96 bits, 1381 gates, 9096 core MOS, 18312 buffered MOS; 9 clauses = 108 bits, 1548 gates, 10222 core MOS, 20590 buffered MOS. This is +167 gates, +1126 core devices, +2278 buffered devices. The values describe tested implementations, not asymptotic minima.

## Audit

18 independently parsed primitive gate-level Verilog modules (core and buffered); all gate types, gate-input pins, directed connections, driven nets, maximum fanout, logical depth, abstract buffers and MOS proxies reconciled. All 4380 Q5 eight-clause tilings with a ninth clause appended passed direct Verilog evaluation; the minimally UNSAT nine-clause core and each deletion were separately checked. 16384 independent falsification-table column controls; 720 proper and 660 arbitrary-literal random raw circuits; 12000 independently generated proper nine-clause random tests across n=3..8 comparing overlap criterion with direct full assignment enumeration; 300-row logical output-toggle ledgers. No detected mismatches. The computer experiments support the theorem, but its proof is symbolic. Main generator seed 2026101909, independent Verilog seed 6719102026, overlap seed 510902, switching seed 2026101919. Physical switching energy/routing remain NULL. Local complete code, component CSV/JSON, 18 .v netlists, checksums and tests are supplied in the originating conversation archive.

FINAL_VERIFICATION_SENTINEL::MAIN::SAT5X9_OVERLAP_CIRCUITS1::P_VS_NP_OPEN