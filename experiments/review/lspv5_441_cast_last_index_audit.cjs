#!/usr/bin/env node
"use strict";

/* Independent adversarial replay of LSPV-3/507's published generator.
   Scope: the separately declared R_CAST507(w), never historical R_mix341. */

const fs = require("fs");
const path = require("path");
const started = process.hrtime.bigint();
const published = require(path.resolve("replay/441/lspv3_507_paid_cast_exact.cjs"));
const repaired = require(path.resolve("replay/441/lspv3_507_paid_cast_exact_repaired.cjs"));

function clone(x) { return JSON.parse(JSON.stringify(x)); }

function audit(mod, label) {
  const rows = [];
  let accepted = 0, rejected = 0, corruptRejected = 0;
  for (const graph of ["K4", "K33", "cube"]) {
    const count = mod.make(graph, 0, true).origin.length;
    for (let replace = 0; replace < count; replace++) {
      for (const w of [1, 2, 4]) {
        const d = mod.make(graph, replace, true);
        try {
          const pr = mod.proof(d, w);
          const checked = mod.check(d, pr, w);
          accepted++;
          const bad = clone(pr);
          const k = bad.nodes.findIndex(n => n.kind === "CAST");
          bad.nodes[k].clause = [1];
          let rejectedBad = false;
          try { mod.check(d, bad, w); }
          catch (_) { rejectedBad = true; corruptRejected++; }
          if (!rejectedBad) throw Error("corrupted CAST accepted");
          rows.push({label, graph, replace, w, outcome:"ACCEPT", weight:checked.weight});
        } catch (e) {
          rejected++;
          rows.push({label, graph, replace, w, outcome:"REJECT", error:String(e.message)});
        }
      }
    }
  }
  return {label, accepted, rejected, corruptRejected, rows};
}

const upstreamRun = published.run();
if (upstreamRun.proofs.length !== 27 || upstreamRun.corrupt_rejected !== 27)
  throw Error("published controls did not replay");

const original = audit(published, "published");
const fixed = audit(repaired, "one_line_repair");
const originalFailures = original.rows.filter(x => x.outcome === "REJECT");

if (original.accepted !== 207 || original.rejected !== 9)
  throw Error(`unexpected published totals ${original.accepted}/${original.rejected}`);
if (!originalFailures.every(x =>
  (x.graph === "K4" && x.replace === 15) ||
  (x.graph === "K33" && x.replace === 23) ||
  (x.graph === "cube" && x.replace === 31)))
  throw Error("failure not isolated to final clause index");
if (fixed.accepted !== 216 || fixed.rejected !== 0 || fixed.corruptRejected !== 216)
  throw Error("repair did not cover all indices and corruption controls");

const result = {
  date_pst: "2026-11-08 10:48 PST",
  status: "COMPUTATIONAL_COUNTEREXAMPLE_TO_PUBLISHED_GENERATOR_COVERAGE",
  model: "R_CAST507(w), distinct from historical R_mix341",
  upstream_controls: {proofs: upstreamRun.proofs.length, corrupt_rejected: upstreamRun.corrupt_rejected},
  published_exhaustive: {accepted: original.accepted, rejected: original.rejected,
    corrupt_rejected: original.corruptRejected, failures: originalFailures},
  one_line_repair_exhaustive: {accepted: fixed.accepted, rejected: fixed.rejected,
    corrupt_rejected: fixed.corruptRejected},
  diagnosis: "The j===sourceIndex.length-1 arm precedes the replaced-clause test, so a final-index replacement feeds source A instead of the paid CAST into its vertex factor chain.",
  theorem_status: "NOT_REFUTED; mathematical construction is repaired by selecting CAST whenever j is the replaced origin index",
  wall_seconds: Number(process.hrtime.bigint() - started) / 1e9,
  max_rss_kib: process.resourceUsage().maxRSS,
  historical_checker_executed: false,
  p_vs_np: "OPEN"
};

fs.mkdirSync("experiments/review/raw", {recursive:true});
fs.writeFileSync("experiments/review/raw/lspv5_441_cast_last_index_audit.json",
  JSON.stringify(result, null, 2) + "\n");
process.stdout.write(JSON.stringify(result, null, 2) + "\n");
