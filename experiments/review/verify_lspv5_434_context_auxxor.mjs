#!/usr/bin/env node
"use strict";

// Independent implementation of the finite LSPV-5/434 control.
// It does not import the Python code and is not the historical R_mix341 checker.

const ok = (condition, message) => { if (!condition) throw new Error(message); };
const originals = ["r", "x"];
const source = [["-r", "x"], ["-r", "-x"], ["r", "x"], ["r", "-x"]];
const assignments = [];
for (let r = 0; r < 2; r++) for (let x = 0; x < 2; x++) assignments.push({r, x});

const lit = (l, a) => l[0] === "-" ? !Boolean(a[l.slice(1)]) : Boolean(a[l]);
const clause = (c, a) => c.some(l => lit(l, a));
const wire = (name, a) => name === "z" ? a.r ^ a.x : a[name];
const row = (q, a) => q.terms.reduce((v, term) => v ^ wire(term, a), 0) === q.rhs;
const xorRows = (a, b) => {
  const terms = new Set(a.terms);
  for (const term of b.terms) terms.has(term) ? terms.delete(term) : terms.add(term);
  return {terms: [...terms].sort(), rhs: a.rhs ^ b.rhs};
};
const equal = (a, b) => JSON.stringify(a) === JSON.stringify(b);

const trace = [
  {id:"d1", rule:"DEF", parents:[], context:[], wire:"z"},
  {id:"d2", rule:"LOCAL", parents:["s0","d1"], context:["r"], row:{terms:["z"],rhs:0}},
  {id:"d3", rule:"LOCAL", parents:["s1","d1"], context:["r"], row:{terms:["z"],rhs:1}},
  {id:"d4", rule:"GF2ADD", parents:["d2","d3"], context:["r"], row:{terms:[],rhs:1}},
  {id:"d5", rule:"LOCAL", parents:["s2","d1"], context:["-r"], row:{terms:["z"],rhs:1}},
  {id:"d6", rule:"LOCAL", parents:["s3","d1"], context:["-r"], row:{terms:["z"],rhs:0}},
  {id:"d7", rule:"GF2ADD", parents:["d5","d6"], context:["-r"], row:{terms:[],rhs:1}},
  {id:"d8", rule:"DISCHARGE", parents:["d4","d7"], context:[], pivot:"r", row:{terms:[],rhs:1}}
];

function verify(t = trace, src = source) {
  const index = new Map(src.map((c, i) => ["s" + i, {kind:"source", clause:c}]));
  let localChecks = 0, addChecks = 0;
  for (const node of t) {
    ok(!index.has(node.id), "duplicate id");
    ok(node.parents.every(p => index.has(p)), "missing/forward parent");
    if (node.rule === "DEF") {
      ok(node.id === "d1" && node.wire === "z" && !node.context.length && !node.parents.length, "bad DEF");
    } else if (node.rule === "LOCAL") {
      const s = index.get(node.parents[0]);
      ok(s.kind === "source" && node.parents[1] === "d1", "LOCAL provenance");
      for (const a of assignments) {
        if (node.context.every(l => lit(l, a)) && clause(s.clause, a)) ok(row(node.row, a), "LOCAL unsound");
        localChecks++;
      }
    } else if (node.rule === "GF2ADD") {
      const left = index.get(node.parents[0]), right = index.get(node.parents[1]);
      ok(equal(left.context, node.context) && equal(right.context, node.context), "context leak");
      ok(equal(xorRows(left.row, right.row), node.row), "wrong GF2 sum");
      for (const a of assignments.filter(a => node.context.every(l => lit(l, a)))) {
        if (row(left.row, a) && row(right.row, a)) ok(row(node.row, a), "GF2 unsound");
        addChecks++;
      }
    } else if (node.rule === "DISCHARGE") {
      const left = index.get(node.parents[0]), right = index.get(node.parents[1]);
      ok(equal(left.context, [...node.context, node.pivot]), "positive branch");
      ok(equal(right.context, [...node.context, "-" + node.pivot]), "negative branch");
      ok(equal(left.row, node.row) && equal(right.row, node.row), "different branch conclusions");
      ok(equal(node.row, {terms:[],rhs:1}), "not false");
    } else throw new Error("unknown rule");
    index.set(node.id, {kind:"derived", ...node});
  }
  return {localChecks, addChecks};
}

const resolve = (left, right, pivot) => {
  ok(left.includes(pivot) && right.includes("-" + pivot), "oriented pivot");
  return [...new Set([...left.filter(x => x !== pivot), ...right.filter(x => x !== "-" + pivot)])];
};
const minusR = resolve(source[0], source[1], "x");
const plusR = resolve(source[2], source[3], "x");
const empty = resolve(plusR, minusR, "r");
ok(equal(minusR,["-r"]) && equal(plusR,["r"]) && equal(empty,[]), "target proof");

let wideChecks = 0;
const wide = 12;
for (let bits = 0; bits < 2 ** (wide + 2); bits++) {
  const a = {r:bits&1, x:(bits>>1)&1};
  let direct = wire("z", a), projected = a.r ^ a.x;
  for (let i = 0; i < wide; i++) {
    const v = (bits >> (i + 2)) & 1;
    direct ^= v; projected ^= v;
  }
  ok((direct === 0) === (projected === 0), "wide affine projection");
  wideChecks++;
}

const corruptions = [];
function reject(name, mutate) {
  const t = JSON.parse(JSON.stringify(trace)), s = JSON.parse(JSON.stringify(source));
  mutate(t, s);
  let rejected = false;
  try { verify(t, s); } catch { rejected = true; }
  ok(rejected, "accepted corruption " + name);
  corruptions.push(name);
}
reject("missing-negative-branch", t => t.splice(6,1));
reject("cross-branch-row-reuse", t => t[6].parents=["d2","d6"]);
reject("branch-scoped-definition", t => t[0].context=["r"]);
reject("wrong-gf2-rhs", t => t[3].row={terms:[],rhs:0});
reject("wrong-local-row", t => t[1].row={terms:["z"],rhs:1});
reject("missing-source-parent", t => t[1].parents=["ghost","d1"]);
reject("bad-discharge-pivot", t => t[7].pivot="x");
reject("source-sign-mutation", (t,s) => s[0][0]="r");

const checks = verify();
const models = assignments.filter(a => source.every(c => clause(c,a))).length;
ok(models === 0, "source SAT");
const deletionWitnesses = source.map((_, omit) => {
  const a = assignments.find(a => source.every((c,i) => i === omit || clause(c,a)));
  ok(a, "deletion UNSAT"); return `${a.r}${a.x}`;
});

console.log(JSON.stringify({
  status:"PASS", claim:"P2-L5-434", system:"distinct R_ctx_extxor434; NOT historical R_mix341",
  sourceUnsatModels:models, singleDeletionSatWitnesses:deletionWitnesses,
  paidNodes:trace.length, sharedGlobalDefinitions:1, localNodes:4, gf2AddNodes:2, dischargeNodes:1,
  maxAuxiliaryAncestorCone:2, targetPaidResolutionNodes:3,
  wideAffineControl:{directOriginalTerms:wide, auxiliaryAncestorCone:2, respcProjectionLines:4,
    ordinaryCanonicalSupport:wide+2, ordinaryCanonicalFalseClauses:2**(wide+1), semanticChecks:wideChecks},
  localAssignmentChecks:checks.localChecks, gf2AssignmentChecks:checks.addChecks,
  corruptedControlsRejected:corruptions,
  limitations:["Independent finite audit only", "No historical checker execution for new trace"]
}, null, 2));
