#!/usr/bin/env node
// Independent replay of the three explicit controls in the Python artifact.
import fs from "node:fs";

const path = process.argv[2];
if (!path) throw new Error("usage: node verify...mjs RAW.json");
const raw = JSON.parse(fs.readFileSync(path, "utf8"));
const c = raw.explicit_controls;
const checks = {
  python_pass: raw.status === "PASS",
  private_collision_undercount:
    c.private_collision.analysis.naive_cost < c.private_collision.analysis.true_cost,
  shared_origin_split: c.shared_split.analysis.split === true,
  blind_shared_overcount:
    c.blind_duplicate.analysis.blind_cost > c.blind_duplicate.analysis.true_cost,
  provenance_exact_all_pairs:
    raw.counts.provenance_cost_failures === 0 &&
    raw.counts.provenance_identity_failures === 0,
};
const pass = Object.values(checks).every(Boolean);
console.log(JSON.stringify({pass, checks, n: raw.n, pairs: raw.counts.pairs}));
if (!pass) process.exit(1);
