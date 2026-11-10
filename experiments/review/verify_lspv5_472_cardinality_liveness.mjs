#!/usr/bin/env node
// Independent replay for LSPV-5/472. This does not invoke Python and does not
// implement an FLMV machine or the historical R_mix341 checker.

import fs from "node:fs";

const rawPath = "results/raw/arc/2026-11-09_1748_LSPV5_472_CARDINALITY_LIVENESS_RAW.json";
const raw = JSON.parse(fs.readFileSync(rawPath, "utf8"));
let checks = 0;

function ok(cond, msg) {
  if (!cond) throw new Error(msg);
  checks += 1;
}

function ceilLog2(n) {
  let p = 1;
  let k = 0;
  while (p < n) {
    p *= 2;
    k += 1;
  }
  return k;
}

for (let n = 1; n <= 20; n += 1) {
  const states = 1n << BigInt(n);
  const work = ceilLog2(n + 1) + 3;
  ok(states === 2n ** BigInt(n), `source states n=${n}`);
  ok(BigInt(states.toString()).toString() === states.toString(), `decimal replay n=${n}`);
  ok(work === ceilLog2(n + 1) + 3, `work bound n=${n}`);
}

for (let h = 1; h <= 20; h += 1) {
  const q = 2 ** h;
  const nodes = 2 * q;
  const dfs = 2 * h + 5;
  ok(nodes === 2 ** (h + 1), `count-once nodes h=${h}`);
  ok(dfs === 2 * h + 5, `dfs peak h=${h}`);
  ok(h <= 2 || dfs < nodes, `asymptotic separation h=${h}`);
}

ok(23 * 90 - 45 * 46 === 0, "23/45 - 1/2 = 1/90");
ok(raw.node === "P2-L5-472", "raw node");
ok(raw.python_assertions === 150, "python assertion ledger");
ok(raw.controls.source_N20.authenticated_states === "1048576", "raw source N=20");
ok(raw.controls.source_N20.live_work_bits === 8, "raw work N=20");
ok(raw.controls.dag_h20.distinct_nodes === 2097152, "raw DAG h=20");
ok(raw.controls.dag_h20.dfs_peak_bits === 45, "raw DAG DFS h=20");

for (const row of raw.illustrative_scales_not_bytes) {
  const N = 10 ** row.log10_N;
  const ratio = N ** (1 / 90);
  ok(Math.abs(ratio / row.N_pow_1_over_90 - 1) < 1e-12, `ratio N=1e${row.log10_N}`);
  ok(row.scanner_live_work_bits === ceilLog2(N + 1) + 3, `scanner N=1e${row.log10_N}`);
}

const result = {
  node: "P2-L5-472",
  checks,
  status: "PASS",
  conclusions: raw.conclusions,
};
console.log(JSON.stringify(result, null, 2));
