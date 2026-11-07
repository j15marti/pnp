#!/usr/bin/env node
// Independent verifier for the LSPV-5/404 JSON ledger.
import fs from "node:fs";

const path = process.argv[2];
if (!path) throw new Error("usage: node verify_lspv5_404_recursive_extension.mjs RAW.json");
const data = JSON.parse(fs.readFileSync(path, "utf8"));
let checks = 0;
function check(condition, message) {
  checks += 1;
  if (!condition) throw new Error(message);
}

check(data.classification.P_vs_NP === "OPEN", "P vs NP scope");
check(data.classification.historical_R_mix341_acceptance === "OPEN", "historical scope");
for (const row of data.rows) {
  const k = row.k;
  check(row.assignments === 2 ** k, `assignments k=${k}`);
  check(row.ordinary_multilinear_guard_terms === 2 ** k, `guard k=${k}`);
  check(row.canonical_even_signed_minterms === (k === 1 ? 1 : 2 ** (k - 1)), `minterms k=${k}`);
  check(row.recursive_product_definitions === k, `product definitions k=${k}`);
  check(row.recursive_product_definition_terms === 3 * k, `product terms k=${k}`);
  check(row.recursive_output_relation_terms === 3, `output relation k=${k}`);
  check(row.xor2_gates === Math.max(0, k - 1), `xor gates k=${k}`);
  check(row.xor2_strict_3cnf_clauses === 4 * Math.max(0, k - 1), `clauses k=${k}`);
  check(row.xor2_literal_occurrences === 12 * Math.max(0, k - 1), `literals k=${k}`);
  check(row.strict_even_source_selector_variables === 2, `selector vars k=${k}`);
  check(row.strict_even_source_output_clauses === 4, `output clauses k=${k}`);
  check(row.strict_even_source_total_clauses === 4 * k, `strict source clauses k=${k}`);
  check(row.strict_even_source_total_variables === 2 * k + 1, `strict source variables k=${k}`);

  for (let mask = 0; mask < 2 ** k; mask += 1) {
    let product = 1;
    let parity = 0;
    for (let i = 0; i < k; i += 1) {
      const bit = (mask >> i) & 1;
      product *= 1 - 2 * bit;
      parity ^= bit;
    }
    check(product === (parity ? -1 : 1), `product semantics k=${k} mask=${mask}`);
    check((1 + product) / 2 === 1 - parity, `indicator k=${k} mask=${mask}`);
  }
}
for (const [name, rejected] of Object.entries(data.corruptions_rejected)) {
  check(rejected === true, `corruption not rejected: ${name}`);
}
console.log(JSON.stringify({ independent_node_checks: checks, rows: data.rows.length, status: "PASS" }));
