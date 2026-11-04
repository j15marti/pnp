#!/usr/bin/env node
// Independent finite verifier for REFEREE336.  No imports.

const fs = require("fs");
const path = "results/raw/arc/lspv5_336/er2_rmix_equivalence_referee336.json";
const raw = JSON.parse(fs.readFileSync(path, "utf8"));
let checks = 0;
function ok(condition, message) {
  if (!condition) throw new Error(message);
  checks += 1;
}
function lit(l, a) {
  const v = a[Math.abs(l)];
  return l > 0 ? v : !v;
}
function clause(c, a) { return c.some(x => lit(x, a)); }

let gateCases = 0;
for (const s1 of [1, -1]) for (const s2 of [1, -1]) {
  const l1 = s1, l2 = 2 * s2, u = 4;
  const slots = [[u, l1, l2], [-u, -l1], [-u, -l2]];
  for (const x1 of [false, true]) for (const x2 of [false, true]) for (const uv of [false, true]) {
    const a = {1:x1, 2:x2, 4:uv};
    const expected = (!lit(l1, a)) && (!lit(l2, a));
    ok(slots.every(c => clause(c, a)) === (uv === expected), "bad signed OR-to-AND translation");
    gateCases += 1;
  }
}

let numeric = 0;
for (let n = 0; n <= 64; n++) for (let wr = 0; wr <= 64; wr++) {
  const upper = Math.pow(n + wr + 3, 4);
  for (const we of [wr, Math.min(upper, wr + n + 1), upper]) {
    ok(wr <= we && we <= upper, "reversed polynomial comparison");
    numeric += 1;
  }
}

ok(raw.status === "PASS", "producer did not pass");
ok(raw.or_def_assignment_cases === gateCases, "gate case mismatch");
ok(raw.numeric_comparison_cases === numeric, "numeric case mismatch");
ok(raw.malformed_extension_records_rejected === 7, "malformed count mismatch");
ok(raw.both_label_controls === 2, "both-label count mismatch");
ok(Array.isArray(raw.not_claimed) && raw.not_claimed.includes("B3") && raw.not_claimed.includes("P!=NP"), "scope firewall missing");

console.log(JSON.stringify({status:"PASS", checks, gateCases, numericCases:numeric, producerAssertions:raw.assertions}, null, 2));
