#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = process.argv[2] || "results/raw/arc/lspv5_338/recognizer_conditioned_recoding_referee338.json";
const raw = JSON.parse(fs.readFileSync(path, "utf8"));
let checks = 0;
function check(ok, msg) { checks++; if (!ok) throw new Error(msg); }

function emit(n, clauses) {
  return Buffer.from(`p cnf ${n} ${clauses.length}\n` + clauses.map(c => c.join(" ") + (c.length ? " " : "") + "0\n").join(""));
}
function parse(buf) {
  const ls = buf.toString("ascii").trimEnd().split("\n"), h = ls[0].split(/\s+/);
  const n = Number(h[2]), m = Number(h[3]);
  check(h[0] === "p" && h[1] === "cnf" && ls.length === m + 1, "JS DIMACS parse");
  return {n, clauses: ls.slice(1).map(s => s.trim().split(/\s+/).map(Number).slice(0, -1))};
}
function encodeUnitSource(src) {
  const bits = [...src].flatMap(b => [...Array(8)].map((_, i) => (b >> (7-i)) & 1));
  const tags = bits.flatMap((b, i) => [[(b ? 1 : -1) * (4*i+1)], [(b ? 1 : -1) * (4*i+3)]]);
  return emit(4*bits.length-1, [[2], ...tags]);
}
function decodeTags(enc) {
  const tags = new Map();
  for (const c of parse(enc).clauses) if (c.length === 1 && Math.abs(c[0]) % 2 === 1)
    tags.set((Math.abs(c[0])-1)/2, Number(c[0] > 0));
  check(tags.size % 16 === 0, "JS tag cardinality");
  const bits=[];
  for(let i=0;i<tags.size/2;i++) { check(tags.get(2*i) === tags.get(2*i+1), "JS tag pair"); bits.push(tags.get(2*i)); }
  return Buffer.from([...Array(bits.length/8)].map((_,i)=>bits.slice(8*i,8*i+8).reduce((a,b)=>2*a+b,0)));
}

check(raw.artifact === "RECOGNIZER-CONDITIONED-RECODING-REFEREE338", "artifact");
check(raw.active_source_retained_all_valid === true, "active retention");
check(raw.roundtrip_all_byte_strings_tested === true, "roundtrip");
const f = raw.left_inverse_is_not_image_authentication;
check(f.source_models === 1 && f.honest_encoded_sat === true && f.forged_unsat_by_empty_source === true, "forged semantics");
check(f.decoder_recovers_source_from_forge === true, "left inverse accepts forge");
check(f.full_image_verifier_rejects_forge === true, "image verifier rejects forge");
check(raw.recognized_php === 4, "PHP count includes 2VAR PHP1 duplicate");
check(raw.recognized_odd_prism === 3, "odd prism count");
check(raw.status.fixed_rmix_prism_original === "published exact 4h-1", "rmix original");
check(raw.status.fixed_rmix_encoded === "zero paid nodes via empty source", "rmix encoded");
check(raw.status.ordinary_resolution_php_original === "published exponential", "Haken scope");
check(raw.status.ordinary_resolution_encoded === "zero paid nodes", "Resolution encoded");
check(raw.status.B1 === "OPEN for R_mix341" && raw.status.B2 === "OPEN" && raw.status.B3 === "OPEN", "bridges");
check(raw.status.P_vs_NP === "OPEN", "P versus NP");
check(raw.status.decoder === "left inverse only; not semantic/image verifier", "decoder status");
check(raw.status.repair.includes("E(D(G))"), "authentication repair");

// Independent reconstruction of the decisive forged-target counterexample.
const jsSource = Buffer.from("p cnf 1 1\n1 0\n"), jsHonest = encodeUnitSource(jsSource);
const hp = parse(jsHonest), jsForged = emit(hp.n, [[], ...hp.clauses.slice(1)]);
check(decodeTags(jsHonest).equals(jsSource), "JS honest roundtrip");
check(decodeTags(jsForged).equals(jsSource), "JS decoder accepts forged active formula");
check(!jsForged.equals(encodeUnitSource(decodeTags(jsForged))), "JS image equality rejects forge");
check(parse(jsHonest).clauses.every(c => c.length > 0), "JS honest source satisfiable by construction");
check(parse(jsForged).clauses.some(c => c.length === 0), "JS forged source contradiction");

for (const r of raw.special_records) {
  check(r.valid === true, `special valid ${r.name}`);
  check(r.has_empty_source === true, `empty source ${r.name}`);
  check(r.active_clauses > 0, `active clauses retained ${r.name}`);
  check(r.tag_clauses === 16 * r.input_bytes, `tag count ${r.name}`);
  check(r.output_bytes > r.input_bytes, `charged output ${r.name}`);
  if (r.name.startsWith("PHP_") || r.name === "2VAR_133") check(r.family === "PHP", `PHP family ${r.name}`);
  if (r.name.includes("PRISM")) check(r.family === "ODD_PRISM_TSEITIN", `prism family ${r.name}`);
}
const names = new Set(raw.selected_controls.map(x => x.name));
for (const name of ["2VAR_000", "2VAR_003", "2VAR_255", "PRISM_3_EVEN", "MALFORMED_1"])
  check(names.has(name), `selected ${name}`);
const even = raw.selected_controls.find(x => x.name === "PRISM_3_EVEN");
check(even.valid && even.family === null && !even.has_empty_source, "even prism no shortcut");
const malformed = raw.selected_controls.find(x => x.name === "MALFORMED_1");
check(!malformed.valid && malformed.family === null && malformed.active_clauses === 0, "malformed control");

console.log(JSON.stringify({artifact: raw.artifact, independent_checks: checks, status: "PASS"}, null, 2));
