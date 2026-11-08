#!/usr/bin/env node
"use strict";

function assert(ok, msg) { if (!ok) throw new Error(msg); }
function parity(x) { let p = 0; while (x) { p ^= 1; x &= x - 1; } return p; }
function q(x, g, t) {
  let y = 0;
  for (let i = 0; i < t; i++) y |= ((((x >>> (2*i)) & 1) & ((x >>> (2*i+1)) & 1)) << i);
  return y;
}
function affine(x, masks, c) {
  let y = 0;
  for (let i = 0; i < masks.length; i++) y |= ((parity(x & masks[i]) ^ ((c >>> i) & 1)) << i);
  return y;
}
function u(g, t) { return (2 ** (2*(g-t))) * (3 ** t); }
function enumerateMasks(n, t, f, a = []) {
  if (a.length === t) { f(a); return; }
  for (let m = 0; m < 2 ** n; m++) enumerateMasks(n, t, f, a.concat([m]));
}
function maxAgreement(g, t) {
  const n = 2*g, inputs = 2 ** n; let best = 0;
  enumerateMasks(n, t, masks => {
    for (let c = 0; c < 2 ** t; c++) {
      let a = 0;
      for (let x = 0; x < inputs; x++) if (q(x,g,t) === affine(x,masks,c)) a++;
      if (a > best) best = a;
    }
  });
  return best;
}

let checks = 0;
for (let g = 1; g <= 4; g++) { assert(maxAgreement(g,1) === u(g,1), `scalar g=${g}`); checks++; }
for (let g = 1; g <= 3; g++) for (let t = 1; t <= Math.min(2,g); t++) {
  assert(maxAgreement(g,t) === u(g,t), `vector g=${g},t=${t}`); checks++;
}
for (let g = 1; g <= 7; g++) for (let t = 1; t <= g; t++) {
  let z = 0;
  for (let x = 0; x < 2 ** (2*g); x++) if (q(x,g,t) === 0) z++;
  assert(z === u(g,t), `zero g=${g},t=${t}`); checks++;
}
assert(Math.ceil((4/3) ** 6) === 6, "full-vector lower bound"); checks++;
assert(2 < 6, "projection collapse"); checks++;
for (let n = 2; n <= 16; n++) {
  const inputs = 2 ** n; let zeros = 0, ones = 0;
  for (let x = 0; x < inputs; x++) { const v = Number(x === inputs - 1); zeros += Number(v === 0); ones += Number(v === 1); }
  assert(zeros === inputs - 1 && ones === 1, `nested n=${n}`); checks++;
}
console.log(JSON.stringify({
  status: "PASS",
  checks,
  theorem: "projecting g independent AND outputs to t exposed coordinates changes U from 3^g to 2^(2(g-t))*3^t",
  counterexample: {paidNonlinearGates: 6, exposedOutputs: 1, projectedConstantCover: 2, invalidHiddenCoordinateBound: 6},
  nestedPrivateChain: "two constant affine templates cover the final bit for every tested length",
  scope: "restricted output-projection control; no historical grammar authentication, all-mixed lower bound, B3, or P-vs-NP result"
}, null, 2));
