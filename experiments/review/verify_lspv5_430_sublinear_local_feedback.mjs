#!/usr/bin/env node
// Independent finite replay for LSPV-5/430. This is not R_mix341.

function g(n) { return Math.floor(Math.sqrt(n)); }
function K(b) { return 8n * BigInt(b + 1) * (1n << BigInt(b)); }

let totalPairs = 0;
let validPairs = 0;
const pairRows = [];
for (let b = 1; b <= 3; b++) {
  const a = 1 << b;
  const f = 1 << a;
  let valid = 0;
  for (let p = 0; p < f; p++) {
    for (let q = 0; q < f; q++) {
      if ((p & ~q) === 0) valid++;
    }
  }
  if (valid !== 3 ** a) throw new Error(`pair count mismatch at b=${b}`);
  pairRows.push({b, ordered_factor_pairs: f * f, valid_implications: valid});
  totalPairs += f * f;
  validPairs += valid;
}

const b = 3;
const assignments = 1 << b;
const functions = 1 << assignments;
let validTriples = 0;
for (let p = 0; p < functions; p++) {
  for (let q = 0; q < functions; q++) {
    const intersection = p & q;
    let pop = 0;
    for (let x = intersection; x; x &= x - 1) pop++;
    validTriples += 2 ** (assignments - pop);
  }
}

let projectionCases = 0;
let projectedClauses = 0;
for (let u = 0; u <= 3; u++) {
  for (let s = 0; s <= u; s++) {
    const f = 1 << (1 << s);
    for (let table = 0; table < f; table++) {
      let trueRows = 0;
      for (let x = table; x; x &= x - 1) trueRows++;
      const falseRows = (1 << s) - trueRows;
      const full = falseRows * (1 << (u - s));
      if (full !== falseRows * (1 << (u - s))) throw new Error("projection mismatch");
      projectionCases++;
      projectedClauses += falseRows;
    }
  }
}

const asymptotic = [16,64,256,1024,4096,16384,65536].map(n => {
  const width = g(n);
  const bound = K(width);
  return {n, g_sqrt_n: width, compiler_bound_decimal: bound.toString(), compiler_bound_bit_length: bound.toString(2).length};
});

console.log(JSON.stringify({
  claim_id: "P2-L5-430",
  historical_r_mix341_checker: false,
  exhaustive: true,
  pair_rows: pairRows,
  ordered_factor_pairs: totalPairs,
  valid_implications: validPairs,
  b3_valid_two_parent_implications: validTriples,
  projection_cases: projectionCases,
  projected_output_clauses: projectedClauses,
  asymptotic,
  limitations: ["finite controls only", "no Pang replay", "no historical checker execution"]
}, null, 2));
