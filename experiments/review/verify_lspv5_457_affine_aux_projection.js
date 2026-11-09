#!/usr/bin/env node
"use strict";

// Independent finite verifier. This is not the historical R_mix341 checker.

function popParity(x) {
  let p = 0;
  while (x) { p ^= 1; x &= x - 1; }
  return p;
}

function word(labels, q) {
  let x = 0;
  labels.forEach((a, i) => { x |= 1 << (i * q + a); });
  return x;
}

function tuples(q, b) {
  const out = [];
  function rec(xs) {
    if (xs.length === b) { out.push(xs.slice()); return; }
    for (let a = 0; a < q; a++) { xs.push(a); rec(xs); xs.pop(); }
  }
  rec([]);
  return out;
}

function sets(q, b, eps, charge) {
  const U = tuples(q, b);
  const S = U.filter(xs => {
    let z = 0;
    xs.forEach((a, i) => { z += eps[i] * a; });
    return ((z - charge) % q + q) % q === 0;
  });
  return { S: S.map(xs => word(xs, q)), U: U.map(xs => word(xs, q)), labels: U };
}

function rank(rows) {
  const basis = new Map();
  for (let x of rows) {
    while (x !== 0) {
      const p = 31 - Math.clz32(x);
      if (basis.has(p)) x ^= basis.get(p);
      else { basis.set(p, x); break; }
    }
  }
  return basis.size;
}

function affdim(P) {
  const z = P[0];
  return rank(P.slice(1).map(x => x ^ z));
}

function main() {
  let checks = 0;
  const odd = [];
  for (const b of [3, 4, 5]) {
    const eps = Array.from({length: b}, (_, i) => i % 2 ? -1 : 1);
    const {S, U} = sets(3, b, eps, 1);
    const ds = affdim(S), du = affdim(U);
    if (ds !== 2 * b || du !== 2 * b) throw new Error(`rank q3 b${b}`);
    for (let mask = 1; mask < (1 << (3 * b)); mask++) {
      const c = popParity(mask & S[0]);
      if (S.every(x => popParity(mask & x) === c) &&
          U.some(x => popParity(mask & x) !== c)) throw new Error("separator");
      checks++;
    }
    odd.push({q: 3, b, valid: S.length, universe: U.length, dimension: ds});
  }

  const base = sets(3, 3, [1, -1, 1], 1);
  const containing = [];
  for (let mask = 0; mask < 512; mask++) for (const c of [0, 1]) {
    if (base.S.every(x => popParity(mask & x) === c)) containing.push([mask, c]);
  }
  let pairs = 0;
  for (let i = 0; i < containing.length; i++) {
    for (let j = i; j < containing.length; j++) {
      const [m1, c1] = containing[i], [m2, c2] = containing[j];
      if (base.U.some(x => popParity(m1 & x) !== c1 || popParity(m2 & x) !== c2)) {
        throw new Error("two-equation projected system excluded U");
      }
      pairs++; checks++;
    }
  }

  const hostile = [];
  for (const [q, b, eps, charge] of [[2,3,[1,1,1],1], [3,2,[1,-1],1]]) {
    const {S,U} = sets(q,b,eps,charge);
    let sep = null;
    for (let mask = 1; mask < (1 << (q*b)); mask++) {
      const c = popParity(mask & S[0]);
      if (S.every(x => popParity(mask & x) === c) && U.some(x => popParity(mask & x) !== c)) {
        sep = {mask, constant:c}; break;
      }
    }
    if (!sep) throw new Error("missing hostile separator");
    hostile.push({q,b,validDimension:affdim(S),universeDimension:affdim(U),...sep});
    checks++;
  }

  const eps = [1,-1,1,-1];
  let accepted = 0, rejected = 0;
  for (const xs of tuples(3,4)) {
    let state = 0;
    xs.forEach((a,i) => { state = ((state + eps[i]*a) % 3 + 3) % 3; });
    if (state === 1) accepted++; else rejected++;
    checks++;
  }
  if (accepted !== 27 || rejected !== 54) throw new Error("nonlinear control");

  console.log(JSON.stringify({
    status:"PASS",
    scope:"independent finite pure-affine projection controls; not R_mix341",
    odd,
    q3b3EquationsContainingS:containing.length,
    q3b3EquationPairsContainingS:pairs,
    hostile,
    nonlinearMod3Control:{accepted,rejected},
    checks,
    node:process.version
  }, null, 2));
}

main();
