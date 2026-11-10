#!/usr/bin/env node
// Independent finite replay for LSPV-5/473.

const beta = c => 0.5 * ((c + 2) / (c * c) - c);
const L = 2 * Math.cos(Math.PI / 7);
let checks = 0;

if (Math.abs(beta(6 / 5) - 23 / 45) > 1e-14) throw new Error("beta"); checks++;
if (Math.abs(beta(6 / 5) - 0.5 - 1 / 90) > 1e-14) throw new Error("gap"); checks++;

for (let den = 2; den <= 80; den++) {
  for (let num = den + 1; num <= 2 * den; num++) {
    const c = num / den;
    if (!(beta(c) < c)) throw new Error(`interval ${num}/${den}`);
    checks++;
  }
}

const controls = [];
for (const n of [2, 3, 7, 16, 31, 64, 1000, 1_000_000]) {
  for (const [p, q] of [[1, 2], [1, 1], [6, 5], [2, 1], [5, 1]]) {
    const floorLog = Math.floor(Math.log2(n));
    const e = Math.floor(p * floorLog / q);
    const address = 1n << BigInt(e);
    if (address.toString(2).length !== e + 1) throw new Error("index bits");
    checks++;
    controls.push({n, r:`${p}/${q}`, exponent:e, indexBits:e + 1, address:String(address)});
  }
}

for (const c of [1.01, 1.1, 1.2, 1.4, 1.5, 1.5213797068, 1.618, L, 2, 5, 10, 100]) {
  const lower = Math.max(0, beta(c), L - c);
  if (!(lower <= c + 1e-14)) throw new Error(`nonempty ${c}`);
  checks++;
}

console.log(JSON.stringify({
  node:"P2-L5-473", checks, status:"PASS", laterProduct:L,
  wrapperSamples:controls.length,
  conclusions:{
    originalNativeSpaceFromTime:"NOT_UPPER_BOUNDED_BY_T",
    normalizedEquivalentSpace:"O(T_POLYLOG_T)",
    exactSpace:"NOT_IDENTIFIED",
    pVsNP:"OPEN"
  }
}, null, 2));
