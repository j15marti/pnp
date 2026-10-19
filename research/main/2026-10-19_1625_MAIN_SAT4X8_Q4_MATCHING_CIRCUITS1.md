# SAT4X8-Q4-MATCHING-CIRCUITS1 | 19 October 2026

**Status:** Exact Q4 combinatorial characterization and explicitly emitted, independently checked combinational Verilog implementations. The literal-input designs are **UPPER BOUNDS**, not proven minimum gates/transistors. P versus NP **OPEN**.

## Mathematical reduction

For exactly eight proper three-variable clauses over four named Boolean variables, each clause fixes three variables' falsifying values and leaves one free. The two falsified assignments are the endpoints of a hypercube Q4 edge. Exactly eight clauses contribute 16 falsification occurrences, so all 16 assignments are excluded iff the eight edges are pairwise vertex-disjoint, equivalently a perfect matching of Q4. Q4 has exactly 272 perfect matchings by the finite least-vertex matching recurrence. Hence **272 × 8! = 10,967,040** ordered UNSAT inputs out of **32^8 = 1,099,511,627,776** proper eight-clause lists.

## Declared hardware interfaces and exact emitted netlist counts

All listed functions output one SAT decision bit. Nominal library: static complementary CMOS INV=2, BUF2=4, NAND/NOR with fan-in k=2k MOS transistors; un-sized high-input-stack cells are not characterized. `P_in` denotes gate input-pin incidences; `E` counts directed driver-to-sink logic connections plus the one output connection, `W` counts distinct driven logic nets including primary inputs.

| Input interface and candidate | Bits | Gates | P_in | E | W | Max fanout | Depth | Core MOS | Additional BUF2 | MOS with BUF2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 32-bit edge presence, wide NOR16 | 32 | 18 | 81 | 82 | 50 | 2 | 3 | 162 | 0 | 162 |
| 32-bit edge presence, max fan-in 4 | 32 | 21 | 84 | 85 | 53 | 2 | 3 | 168 | 0 | 168 |
| 40-bit proper raw, factored | 40 | 445 | 1148 | 1149 | 485 | 8 | 7 | 2296 | 456 | **4120** |
| 40-bit proper raw, NAND5 direct | 40 | 349 | 1660 | 1661 | 389 | 17 | 6 | 3320 | 1160 | 7960 |
| 72-bit any signed literal raw, bipolar | 72 | 745 | 2016 | 2017 | 817 | 7 | 7 | 4032 | 744 | **7008** |
| 72-bit any signed literal raw, direct | 72 | 793 | 2712 | 2713 | 865 | 8 | 6 | 5424 | 1512 | 11472 |
| 128-bit independent clause-falsification table, NOR16 | 128 | 18 | 145 | 146 | 146 | 1 | 3 | 290 | 0 | 290 |
| 128-bit table, only two-input NAND/NOR | 128 | **127** | 254 | 255 | 255 | 1 | 7 | **508** | 0 | 508 |

32-bit and 128-bit interfaces **exclude** preprocessing from clauses. The 40-bit raw input contains eight 5-bit proper-clause codes: three low sign bits, two high missing-variable bits. The **72-bit raw input handles every** three-slot clause over four variables using eight possible signed-literal types per slot, allowing repeated variables, repeated clauses and tautologies.

### Primitive inventories

- Presence32 wide: NOR4=16, NOR16=1, INV=1 (162 MOS).
- Presence32 max fan-in 4: NOR4=20, NAND4=1 (168 MOS).
- Proper40 factored: INV=40, NAND2=256, NOR2=32, NOR3=64, NAND8=32, NOR4=20, NAND4=1 (2296 MOS).
- Proper40 direct: INV=40, NAND5=256, NAND8=32, NOR4=20, NAND4=1 (3320 MOS).
- General72 bipolar: INV=240, NAND3=320, NAND4=168, NAND8=16, NAND16=1 (4032 MOS).
- General72 direct: INV=72, NAND3=320, NAND4=384, NAND8=16, NAND16=1 (5424 MOS).
- Table128 binary: NOR2=90, NAND2=37 (508 MOS); Table128 wide: NOR8=16, NOR16=1, INV=1 (290 MOS).

**Provable restricted optimum:** Since each of 128 independently supplied table inputs is essential and two-input gates merge at most two formerly disconnected dependency components, at least 127 binary gates are necessary. The 127-gate, 508-MOS NAND2/NOR2 implementation attains this bound. No global minimum is claimed for the 40-bit or 72-bit raw-input circuits; every raw bit is essential, yielding only 39- and 71-binary-gate general lower bounds respectively.

**Actual buffer circuits** use explicit fanout-two noninverting BUF2 trees, not unmeasured physical routing. 40-bit factored BUF2: 901 total cells, 941 logical nets, 1605 logical connections, 4120 nominal MOS. 72-bit bipolar BUF2: 1489 total cells, 1561 nets, 2761 connections, 7008 nominal MOS. Physical wirelength, placement area, device sizing, power, transistor nets, energy and delay are all **NULL/unmeasured**, not zero.

### Independently checked evidence and availability

The reproducible local research package `3SAT_8clauses_4variables_verified_circuits.zip` (attached to the originating conversation, **not** uploaded to GitHub) includes the full dependency-free generator, primitive-level Verilog netlists for all twelve named core and buffered circuits, an independently written Verilog interpreter, raw JSON and CSV censuses, directed-cube schematic SVG, finite tests, logical gate-output toggle counts and SHA-256 manifest. Independently parsed 12 Verilog modules. All 272 Q4 perfect matching families, 10,240 single-clause replacements, random 40/72-bit formulas, 4096 table-column controls and every edge-vertex incidence passed with no mismatch. The **10,967,040** ordered UNSAT count is mathematical enumeration, **not** 10,967,040 full circuit simulations.

Dynamic output-toggle count under specified 300-row stimulus: proper40 factored core 24,133; with BUF2 74,425 (50,292 buffer toggles). General72 bipolar core 82,639; with BUF2 160,713 (78,074 buffer toggles). Gate-output toggles are not transistor switching events or measured physical energy.

### Scientific limit

Fixed four-variable circuits give no asymptotic SAT lower bound. Logic counts, cube matching, proof-system hardness and hardware-device counts do not establish P != NP for growing input families. P versus NP remains **OPEN**.

<!-- FINAL_VERIFICATION_SENTINEL::MAIN::SAT4X8-Q4-MATCHING-CIRCUITS1::P_VS_NP_OPEN -->