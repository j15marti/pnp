// Reproduce a density-scope error using the exact original /055 source.
// Node >=18. No random inputs in the new regression; baseline seed is 20261115.
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const sourcePath = process.argv[2] || path.join(__dirname, 'tmr1_totalizer_e2e055.js');
const source = fs.readFileSync(sourcePath);
const expected = 'b3e4e6f2c1b9280e45cc4c523b3b6c45fd063536';
const sourceBlob = crypto.createHash('sha1').update(Buffer.from(`blob ${source.length}\0`)).update(source).digest('hex');
if (sourceBlob !== expected) throw Error('Wrong /055 source revision');
const baselineLogs = [];
const context = {console: {log: s => baselineLogs.push(JSON.parse(s))}};
vm.runInNewContext(source.toString('utf8'), context, {timeout: 10000, filename: sourcePath});
let checks = 0;
const check = (condition, label) => {checks++; if (!condition) throw Error(label);};
const lit = (i, positive) => [i, positive];
const literals = [lit(0, true), lit(0, false), lit(1, true), lit(1, false)];
const clauses = [[lit(0, true)], [lit(1, true)]];
for (const a of literals) for (const b of literals)
  if (a[1] || b[1]) clauses.push([a, b]);
clauses.push(
  [literals[0], literals[0], literals[0]],
  [literals[0], literals[0], literals[1]],
  [literals[0], literals[0], literals[2]],
  [literals[0], literals[0], literals[3]],
  [literals[0], literals[1], literals[0]],
  [literals[0], literals[1], literals[1]]);
const input = {n: 5, cs: clauses};
const output = context.norm(input);
const count = h => {
  let result = 0;
  for (let z = 0; z < 2 ** h.n; z++) {
    const assignment = Array.from({length: h.n}, (_, i) => Boolean((z >> i) & 1));
    if (h.cs.every(c => c.some(([i, positive]) => assignment[i] === positive))) result++;
  }
  return result;
};
check(clauses.length === 20, 'twenty source clauses');
check(new Set(clauses.map(JSON.stringify)).size === 20, 'outer Nodup');
check(clauses.every(c => c.length <= 3), 'width <=3');
check(clauses.length <= 4 * input.n, 'claimed density premise');
check(output.n === 6 && output.cs.length === 25, 'actual original normalizer');
check(output.cs.length > 4 * output.n, 'old universal density conclusion falsified');
check(count(input) === 8 && count(output) === 8, 'count preservation survives');
check(new Set(output.cs.flatMap(c => c.map(l => l[0]))).size === 6, 'AllOccur survives');
check(new Set(output.cs.map(JSON.stringify)).size === output.cs.length, 'NoDup survives');
check(context.enc(output).length === 311, 'actual encoded bit length');
let assignmentsChecked = 0;
for (let z = 0; z < 32; z++) {
  const old = Array.from({length: 5}, (_, i) => Boolean((z >> i) & 1));
  const evaluate = (cs, a) => cs.every(c => c.some(([i, positive]) => a[i] === positive));
  let extensions = 0;
  for (const t of [false, true]) extensions += Number(evaluate(output.cs, old.concat(t)));
  check(extensions === Number(evaluate(input.cs, old)), 'unique-extension semantics');
  assignmentsChecked++;
}
// The circuit compiler's AllOccur precondition protects its actual use of the lemma.
const circuitInput = context.toCNF({q: 5, gs: [], out: 0});
const circuitOutput = context.norm(circuitInput);
check(new Set(circuitInput.cs.flatMap(c => c.map(l => l[0]))).size === 5, 'compiler AllOccur');
check(circuitOutput.cs.length <= 4 * circuitOutput.n, 'restricted pipeline density survives');
check(count(circuitInput) === 16 && count(circuitOutput) === 16, 'circuit control count');
// Exact integer checks of the corrected general and restricted inequalities.
let parameterCases = 0;
for (let n = 0; n <= 20; n++) for (let u = 0; u <= n; u++) for (let m0 = 0; m0 <= 4*n; m0++) {
  const d = Math.max(1, 4-n), np = n+d, mp = m0+u+d+1;
  check(mp <= 5*np, 'general 5-density bound');
  if (u === 0) check(mp <= 4*np, 'AllOccur 4-density bound');
  parameterCases++;
}
console.log(JSON.stringify({revision:'tmr1-totalizer-density060.v2',
  status:'COMPUTATIONAL_COUNTEREXAMPLE_WITH_SYMBOLIC_SCOPE_CORRECTION',
  originalSourceBlob:sourceBlob, originalBaseline:baselineLogs[0],
  counterexample:{input,output,inputCount:count(input),outputCount:count(output),
    n:5,m:20,u:3,d:1,nPrime:6,mPrime:25,claimedCap:24,formalInputBits:311},
  correctedFormula:'mPrime = mDistinct + unused + d + 1',
  correctedGeneralBound:'m <= 4n implies mPrime <= 5nPrime',
  correctedRestrictedBound:'AllOccur and m <= 4n imply mPrime <= 4nPrime',
  assignmentsChecked,parameterCases,regressionAssertions:checks,failures:0,
  leanKernelExecuted:false}));
