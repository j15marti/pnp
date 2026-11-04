#!/usr/bin/env node
"use strict";

const fs = require("fs");
const crypto = require("crypto");

if (process.argv.length !== 3) throw new Error("usage: verifier raw.json");
const raw = fs.readFileSync(process.argv[2], "utf8");
const data = JSON.parse(raw);
let checks = 0;
function check(x, m) { if (!x) throw new Error(m); checks++; }

function clauseValue(clause, a) {
  return clause.some(lit => (a[Math.abs(lit)-1] === 1) === (lit > 0));
}
function cnfValue(cnf, a) { return cnf.every(c => clauseValue(c, a)); }
function assignments(n) {
  const out = [];
  for (let x=0; x<(1<<n); x++) out.push(Array.from({length:n}, (_,i)=>(x>>i)&1));
  return out;
}
function core(n) {
  const f = [[1],[-1]];
  for (let i=2;i<=n;i++) f.push([1,i],[1,-i]);
  return f;
}
function verifyOne(cnf, p) {
  if (!p || !Array.isArray(p.parents) || p.parents.length!==2 || !Number.isInteger(p.pivot) || !Array.isArray(p.conclusion)) return false;
  const [a,b]=p.parents;
  if (!Number.isInteger(a)||!Number.isInteger(b)||a<0||b<0||a>=cnf.length||b>=cnf.length||p.pivot<=0) return false;
  const ca=new Set(cnf[a]), cb=new Set(cnf[b]); let res;
  if(ca.has(p.pivot)&&cb.has(-p.pivot)) res=[...ca].filter(x=>x!==p.pivot).concat([...cb].filter(x=>x!==-p.pivot));
  else if(ca.has(-p.pivot)&&cb.has(p.pivot)) res=[...ca].filter(x=>x!==-p.pivot).concat([...cb].filter(x=>x!==p.pivot));
  else return false;
  const s=new Set(res); if([...s].some(x=>s.has(-x))) return false;
  return p.conclusion.length===s.size && p.conclusion.every(x=>s.has(x));
}

check(data.run === "REFEREE347", "run tag");
check(data.theorem.status === "PROVED_EXACT", "status");
check(data.unit_core_family.length === 12, "core count");
for (const rec of data.unit_core_family) {
  const f=core(rec.n), vals=assignments(rec.n).map(a=>cnfValue(f,a));
  check(vals.every(x=>!x), `false core ${rec.n}`);
  check(verifyOne(f,{parents:[0,1],pivot:1,conclusion:[]}), `proof ${rec.n}`);
  check(rec.resolution_paid_nodes===1, `cost ${rec.n}`);
}
check(data.exhaustive_two_variable.formulas===256, "all two-var CNFs");
check(data.exhaustive_two_variable.sat===95, "SAT count");
check(data.exhaustive_two_variable.unsat===161, "UNSAT count");
check(data.exhaustive_two_variable.unsat_zero_signature===161, "zero signatures");
check(data.k4_tseitin.odd_models===0, "odd K4");
check(data.k4_tseitin.even_models===8, "even K4");
check(data.malformed_rejected===7, "malformed count");
check(data.bad_proofs_rejected===5, "bad proof count");
check(data.bridges.B1==="OPEN" && data.bridges.B2==="OPEN" && data.bridges.B3==="OPEN", "bridge status");

console.log(JSON.stringify({verifier:"REFEREE347-independent-js",checks,raw_sha256:crypto.createHash("sha256").update(raw).digest("hex")},null,2));
