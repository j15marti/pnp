# QRECOVERY-ORBIT2 — 19 November 2026 Pacific

Recovered LOCAL4, HORN2, QRECOVERY1 and Q-SIGNATURE-SELECTOR. Implemented the previously identified private-head color symmetry as a boundary-partition cache with explicit witness transport.

PROVED restricted: equality-pattern-equivalent tail boundary rows have the same decision; permute tail colors, reconstruct every private head, then check original Q. FALSIFIED: permuting a complete Q witness or reusing an unweighted count. Q(A,A,B) maps to false Q(A,A,C) under B/C swap; private-head multiplicities are 4 versus 2. No distinct-variable-name rule is violated by tied letter values.

Tested 32 graph sources, 2400 rows, 112 cached solves; 1770 SAT/630 UNSAT; 10,720 original-Q witness checks. Includes K6 and all 15 edge deletions. Full source seeds/scopes/rows and witnesses retained. Separate inline explicit-matrix check passed; independent peer review PENDING.

The fixed-five-color quotient saves at most a factor 120, so it supplies no exponent contraction. Next dependency is a source-computable stronger quotient plus paid transport and global coverage. Arbitrary-CNF layout and critical/high-girth witness reductions remain OPEN. P versus NP OPEN. Existing owners and schedules preserved.

Report: research/agents/recovery/2026-11-19_QRECOVERY_ORBIT2/report.md
Code: experiments/t5/q_recovery_orbit2_20261119.py
Raw: results/raw/t5/q_recovery_orbit2_20261119.json
Run code with Python standard library; output is pretty JSON with equivalent data. Timings/heap fields vary by host. Report defines all counters and storage limitations.
