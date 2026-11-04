#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = process.argv[2] || "results/raw/arc/lspv5_337/growing_support_dominance_referee337.json";
const raw = JSON.parse(fs.readFileSync(path, "utf8"));
let checks = 0;
function check(c, m) { checks++; if (!c) throw new Error(m); }
function parity(row) { return row.reduce((a, b) => a ^ b, 0); }
function rows(m) {
  const out = [];
  for (let x = 0; x < 2 ** m; x++) out.push(Array.from({length:m}, (_,i)=>(x >> (m-1-i)) & 1));
  return out;
}

check(raw.artifact === "GROWING-SUPPORT-DOMINANCE-REFEREE337", "artifact");
check(raw.status.B1 === "OPEN" && raw.status.B2 === "OPEN" && raw.status.B3 === "OPEN", "bridges");
check(raw.status.P_vs_NP === "OPEN", "P vs NP");
for (const c of raw.chain_controls) {
  const m = c.m;
  check(c.clauses === 4*m-6 && c.target_nodes === 4*m-7, `chain ${m}`);
  check(c.models === 2**(m-1), `models ${m}`);
  check(c.ancestral_hard_q_nodes === 5*m-5, `ancestral ${m}`);
  check(c.dominance_bypass_nodes === 5*m-6, `bypass ${m}`);
  const beta = [1, ...Array(m-1).fill(0)];
  for (const r of rows(m)) {
    const p = parity(r) === 0;
    const blocker = r.some((v,i)=>v !== beta[i]);
    check(!p || blocker, `P=>C beta ${m}`);
  }
}
for (const q of raw.finite_q_controls) {
  check(q.family_size === 2 ** (2 ** (q.m-1) - 1), `family ${q.m}`);
  check(parity(q.beta) === 1, `odd beta ${q.m}`);
}
for (const c of raw.counting_controls) {
  const m = c.m, D = 2*m+6;
  const s = Math.max(0, Math.floor((2**(m-1)-2*m-4)/D));
  check(c.D_m === D && c.certified_min_gates === s+1, `count fields ${m}`);
  check(c.family_log2 === 2**(m-1)-1, `family log ${m}`);
  if (s > 0) {
    const logCount = Math.log2(s+1)+Math.log2(m+s+2)+s*(4+2*Math.log2(m+s+2));
    check(logCount < c.family_log2, `count separation ${m}`);
  }
}
check(raw.strict_fixed_k_rejection === true && raw.malformed_rejections === 5, "grammar controls");
console.log(JSON.stringify({artifact: raw.artifact, independent_checks: checks, status: "PASS"}, null, 2));
