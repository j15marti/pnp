#!/usr/bin/env node
// Independent arithmetic/status audit of REFEREE365's emitted ledger.
import fs from "node:fs";

const path = "results/raw/arc/2026-11-05_0848_LSPV5_REFEREE365_raw.json";
const x = JSON.parse(fs.readFileSync(path, "utf8"));
let checks = 0;
const ok = (b, m) => { if (!b) throw new Error(m); checks++; };

ok(x.format === "LSPV5-EF-EQUIVALENCE-AUDIT-REFEREE365-1", "format");
ok(x.randomness === "none", "randomness");
ok(x.status.bare_b3.startsWith("OPEN"), "B3 status");
ok(x.status.p_vs_np === "OPEN", "P/NP status");
ok(x.status.historical_rmix341_reverse_simulation.startsWith("OPEN"), "historical status");
ok(x.ledgers.length === 3, "ledger count");

for (const l of x.ledgers) {
  ok(l.paid_nodes > 0, `${l.label}: nodes`);
  ok(l.source_bytes > 0 && l.certificate_bytes > l.source_bytes, `${l.label}: bytes`);
  ok(l.ef_total_symbol_budget === l.relation_symbols + l.ef_macro_symbols, `${l.label}: sum`);
  ok(l.ef_total_symbol_budget <= l.polynomial_cap, `${l.label}: cap`);
  ok(l.certificate_bytes <= l.polynomial_cap, `${l.label}: cert cap`);
  ok(Object.values(l.rules).reduce((a,b) => a+b, 0) === l.paid_nodes, `${l.label}: rules`);
  ok(l.checker_stats.accepted === true, `${l.label}: accepted`);
}

ok(x.er_embedding.tables.length === 16, "all binary truth tables");
ok(x.er_embedding.valuation_checks === 128, "16 tables x 8 valuations");
for (const row of x.er_embedding.tables) ok(row.facet_count === 4, `facets ${row.table}`);
for (const key of ["wrong_gf2", "hidden_payload", "forward_def_input", "sat_same_sign"])
  ok(typeof x.hostile_controls[key] === "string" && x.hostile_controls[key].length > 0, key);

const out = {
  format: "LSPV5-EF-EQUIVALENCE-INDEPENDENT-REFEREE365-1",
  checks,
  ledgers: x.ledgers.map(l => ({label:l.label, paid_nodes:l.paid_nodes, ef:l.ef_total_symbol_budget, cap:l.polynomial_cap})),
  status: "PASS",
  limitation: "Independent replay checks the emitted arithmetic and status firewall, not an authoritative EF byte proof."
};
fs.writeFileSync("results/raw/arc/2026-11-05_0848_LSPV5_REFEREE365_independent.json", JSON.stringify(out, null, 2)+"\n");
console.log(JSON.stringify(out, null, 2));
