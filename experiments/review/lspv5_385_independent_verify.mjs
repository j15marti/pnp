#!/usr/bin/env node
// Independent consumer for the REFEREE385 producer record.
import fs from "node:fs";
import crypto from "node:crypto";
const started = process.hrtime.bigint();

const path = process.argv[2];
if (!path) throw new Error("usage: verifier record.json");
const record = JSON.parse(fs.readFileSync(path, "utf8"));
let checks = 0;
const assert = (p, m) => { if (!p) throw new Error(m); checks++; };
const litTrue = (lit, a) => a.get(Math.abs(lit)) === (lit > 0);
const clauseTrue = (c, a) => c.some(l => litTrue(l, a));
const assignment = rows => new Map(rows.map(([v, b]) => [v, Boolean(b)]));

assert(record.run === "LSPV-5/REFEREE385", "run identity");
assert(record.seed === 385, "fixed seed");
assert(record.samples.length === 1, "one detailed sample");
const stable = JSON.stringify(record.samples).replace(/\s/g, "");
// Recreate Python's compact, sorted-key hash recursively.
const canonical = value => {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value && typeof value === "object")
    return `{${Object.keys(value).sort().map(k => `${JSON.stringify(k)}:${canonical(value[k])}`).join(",")}}`;
  return JSON.stringify(value);
};
const digest = crypto.createHash("sha256").update(canonical(record.samples)).digest("hex");
assert(digest === record.sample_sha256, "sample hash");

for (const sample of record.samples) {
  const c = sample.component, F = c.clauses, D = [];
  assert(F.length === 8 * c.k, "8k complete clauses");
  assert(c.core.length === 5 * c.k + 3, "5k+3 core sources");
  assert(new Set(c.core).size === c.core.length, "distinct core");
  for (const clause of F) {
    assert(clause.length === 3, "width three");
    assert(new Set(clause.map(Math.abs)).size === 3, "proper clause");
  }
  for (const [sidText, rows] of Object.entries(sample.witnesses)) {
    const sid = Number(sidText), a = assignment(rows);
    assert(!clauseTrue(F[sid], a), "omitted clause is false");
    assert(F.every((cl, i) => i === sid || clauseTrue(cl, a)), "full-source deletion model");
  }
  const get = ref => ref >= 0 ? F[ref] : D[-ref - 1];
  for (const node of sample.trace) {
    const A = get(node.left), B = get(node.right);
    assert(A && B, "antecedents exist");
    assert(A.includes(node.pivot), "positive oriented pivot");
    assert(B.includes(-node.pivot), "negative oriented pivot");
    const out = [];
    for (const lit of [...A, ...B])
      if (lit !== node.pivot && lit !== -node.pivot && !out.includes(lit)) out.push(lit);
    assert(!out.some(l => out.includes(-l)), "non-tautological resolvent");
    assert(JSON.stringify(out) === JSON.stringify(node.clause), "exact resolvent, no weakening");
    D.push(out);
  }
  assert(D.length === 5 * c.k + 2, "q-1 paid Resolution nodes");
  assert(D.at(-1).length === 0, "empty conclusion");

  const badPivot = structuredClone(sample.trace); badPivot[0].pivot += 999999;
  const truncated = sample.trace.slice(0, -1);
  const replay = trace => {
    const out = [];
    const fetch = r => r >= 0 ? F[r] : out[-r - 1];
    for (const n of trace) {
      const A = fetch(n.left), B = fetch(n.right);
      if (!A || !B || !A.includes(n.pivot) || !B.includes(-n.pivot)) return false;
      const C = [];
      for (const lit of [...A, ...B])
        if (lit !== n.pivot && lit !== -n.pivot && !C.includes(lit)) C.push(lit);
      if (JSON.stringify(C) !== JSON.stringify(n.clause)) return false;
      out.push(C);
    }
    return out.length > 0 && out.at(-1).length === 0;
  };
  assert(!replay(badPivot), "wrong-pivot corruption rejected");
  assert(!replay(truncated), "omitted-root corruption rejected");
}

assert(record.counters.cases === 523, "expected case count");
assert(record.counters.odd_cases === 269, "expected odd case count");
assert(record.counters.component_omission_products === 5382, "all omission products");
assert(record.counters.large_id_cases === 23, "large-id deletion cases");
console.log(JSON.stringify({pass:true, checks, sample_sha256:digest,
  elapsed_seconds:Number(process.hrtime.bigint()-started)/1e9,
  verifier_max_rss_kib:process.resourceUsage().maxRSS,
  producer_counters:record.counters, scope:"independent finite audit; historical /341 byte checker not run"}));
