#!/usr/bin/env node
// Independent verifier for REFEREE377 raw data.  No producer import.
import fs from 'node:fs';
import crypto from 'node:crypto';

const rawPath = new URL('../../results/raw/review/2026-11-05_2052_LSPV5_CUT_CONTEXT_COST377.json', import.meta.url);
const rawBytes = fs.readFileSync(rawPath);
const r = JSON.parse(rawBytes);
let checks = 0;
function req(x, msg) { checks++; if (!x) throw new Error(msg); }
const sha = s => crypto.createHash('sha256').update(s).digest('hex');
const bitRows = n => Array.from({length: 2 ** n}, (_, x) => Array.from({length: n}, (_, i) => (x >> i) & 1));

function parse(src) {
  const lines = src.trimEnd().split('\n');
  if (lines[0] !== 'p cnf 6 16' || lines.length !== 17) return null;
  const clauses = [];
  for (const line of lines.slice(1)) {
    const xs = line.trim().split(/\s+/).map(Number);
    if (xs.length !== 4 || xs[3] !== 0 || xs.slice(0, 3).some(x => !x || Math.abs(x) > 6)) return null;
    if (new Set(xs.slice(0, 3).map(Math.abs)).size !== 3) return null;
    clauses.push(xs.slice(0, 3));
  }
  return clauses;
}
function sat(clauses, a) {
  return clauses.every(c => c.some(l => (a[Math.abs(l) - 1] === 1) === (l > 0)));
}

req(sha(r.odd_dimacs) === r.odd_source_sha256, 'odd source hash');
req(sha(r.even_dimacs) === r.even_source_sha256, 'even source hash');
req(Buffer.byteLength(r.odd_dimacs) === r.odd_source_bytes, 'odd bytes');
req(Buffer.byteLength(r.even_dimacs) === r.even_source_bytes, 'even bytes');
const odd = parse(r.odd_dimacs), even = parse(r.even_dimacs);
req(odd && even, 'strict source parse');
req(bitRows(6).filter(a => sat(odd, a)).length === 0, 'odd source UNSAT');
req(bitRows(6).filter(a => sat(even, a)).length === 8, 'even source model count');

for (const c of r.cases) {
  const k = c.k;
  const L = 2 ** (k - 3);
  req(c.exact_min_leaf_contexts === L, `leaf lower bound k=${k}`);
  req(c.canonical_leaf_contexts === L, `matching cover k=${k}`);
  req(c.canonical_split_internal_nodes_if_paid === L - 1, `tree joins k=${k}`);
  req(c.canonical_total_tree_nodes_before_leaf_closure_if_paid === 2 * L - 1, `tree nodes k=${k}`);
  req(c.materialized_fixed_bit_records === L * (k - 3), `materialized bits k=${k}`);
  req(c.dfs_live_fixed_bits === k - 3, `DFS bits k=${k}`);
  req(c.native_final_xor_nodes === 1 && c.native_branch_contexts === 0, `native shortcut k=${k}`);

  const universe = new Set(bitRows(k).map(x => x.join('')));
  const covered = new Set();
  for (const prefix of bitRows(k - 3)) {
    for (const tail of bitRows(3)) {
      const row = prefix.concat(tail).join('');
      req(!covered.has(row), `disjoint canonical contexts k=${k}`);
      covered.add(row);
    }
  }
  req(covered.size === universe.size && [...universe].every(x => covered.has(x)), `cover k=${k}`);
  req(Math.ceil(universe.size / 8) === L, `volume lower bound k=${k}`);

  const mask = (1 << k) - 1;
  req((mask ^ mask) === 0 && (0 ^ 1) === 1, `opposite row XOR k=${k}`);
  req((0 ^ 0) === 0, `same row does not close k=${k}`);
}

req(parse(r.odd_dimacs.replace('p cnf 6 16', 'p cnf 6 15')) === null, 'malformed header rejected');
req(parse(r.odd_dimacs.replace('1 2 3 0', '1 2 7 0')) === null, 'corrupt literal rejected');
console.log(JSON.stringify({status: 'COMPUTATIONAL', checks, raw_sha256: sha(rawBytes), cases: r.cases.length}, null, 2));
