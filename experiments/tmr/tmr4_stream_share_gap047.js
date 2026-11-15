"use strict";
// TMR-4/033: exact small-circuit count and paid source traversal controls.
// This is a FINITE test, not a Turing-machine compiler or lower-bound proof.
const assert = require("assert");
let assertions = 0;
function check(p, msg) { assertions++; assert.ok(p, msg); }
function oneGateMasks(n) {
  const N = 2 ** n, all = 2 ** N - 1;
  const inputs = [0, all];
  for (let j = 0; j < n; j++) {
    let m = 0;
    for (let i = 0; i < N; i++) if ((i >> j) & 1) m |= 2 ** i;
    inputs.push(m);
  }
  const yes = new Set(inputs);
  for (const a of inputs) yes.add(all ^ a); // NOT
  for (const a of inputs) for (const b of inputs) {
    yes.add(a & b); yes.add(a | b); // AND / OR
  }
  return yes;
}
function word(mask, N) { return Array.from({length: N}, (_, i) => String((mask >> i) & 1)).join(""); }
function streamCopy(src) {
  let out = "", moves = 0;
  for (let i = 0; i < src.length; i++) { out += src[i]; moves++; }
  return { out, moves, eof: 1 }; // one endmarker transition
}
function indexScan(src, target) {
  let moves = 0, answer = null;
  for (let i = 0; i <= target; i++) {
    moves++;
    if (i === target) answer = src[i];
  }
  return { answer, moves }; // paid source reads; index decode adds nonnegative work
}
const rows = [];
for (const n of [2, 3, 4]) {
  const N = 2 ** n, yes = oneGateMasks(n), total = 2 ** N;
  let no = -1, yesCount = 0;
  for (let mask = 0; mask < total; mask++) {
    const isYes = yes.has(mask);
    if (isYes) yesCount++;
    else if (no < 0) no = mask;
  }
  check(no >= 0, "NO exists for n=" + n);
  check(yesCount === yes.size, "all <=1 gate masks enumerated for n=" + n);
  const sources = [word(no, N), word(0, N), word(2 ** N - 1, N)];
  for (let m = 0; m < Math.min(total, 200); m++) sources.push(word(m, N));
  let pairedTotal = 0;
  for (const src of sources) {
    const g = streamCopy(src);
    check(g.out === src && g.moves + g.eof === N + 1, "copy is exact with paid input and EOF");
    for (let i = 0; i < N; i++) {
      const e = indexScan(src, i);
      check(e.answer === g.out[i], "independent-index and full streaming output agree");
      check(e.moves === i + 1, "index scan advances count");
      pairedTotal += e.moves;
    }
  }
  const independentReads = N * (N + 1) / 2;
  const streamedReads = N;
  check(independentReads > streamedReads, "amortized read gap");
  rows.push({n, truth_table_length_N: N, gate_threshold_s: 1, exact_yes_count: yesCount,
    exact_no_count: total - yesCount, first_no_truth_table: word(no, N),
    full_stream_source_reads: streamedReads, independent_index_source_reads: independentReads,
    ratio: independentReads / streamedReads, tested_sources: sources.length,
    paired_source_reads: pairedTotal});
}
console.log(JSON.stringify({experiment: "TMR4/033 STREAMSHARE047", status: "COMPUTATIONAL",
  model: "explicit truth table F as the source; fixed sequential input and output head; indexed scan rereads source from origin",
  assertions, failed: 0, rows, qualification: "no SAT-to-MCSP reduction, no superlinear MCSP decision lower bound"}, null, 2));
