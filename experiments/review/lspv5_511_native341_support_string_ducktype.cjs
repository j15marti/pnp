#!/usr/bin/env node
'use strict';

/* LSPV-5/511: original-/341 AND3 support duck-typing audit. */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const cp = require('child_process');

const root = path.resolve(__dirname, '../..');
const checker = path.join(root, 'experiments/arc/lspv2_341_independent_verify.js');
const seed = path.join(root, 'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const outPath = path.join(root, 'results/raw/review/2026-11-12_1348_LSPV5_511_NATIVE341_SUPPORT_STRING_RAW.json');
const acceptedPath = path.join(root, 'results/raw/review/2026-11-12_1348_LSPV5_511_SUPPORT_STRING_ACCEPTED.json');

function sha256(b) { return crypto.createHash('sha256').update(b).digest('hex'); }
function gitBlob(b) {
  return crypto.createHash('sha1').update(Buffer.from(`blob ${b.length}\0`)).update(b).digest('hex');
}
function clone(x) { return JSON.parse(JSON.stringify(x)); }

const checkerBytes = fs.readFileSync(checker);
const seedBytes = fs.readFileSync(seed);
if (gitBlob(checkerBytes) !== 'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0') throw Error('checker blob drift');
if (gitBlob(seedBytes) !== 'fe27fe1011d0021e721ccaeb747ed58da65d7464') throw Error('seed blob drift');
const seedObj = JSON.parse(seedBytes);

function run(name, obj, expected) {
  const dir = fs.mkdtempSync('/tmp/lspv5-511-');
  const file = path.join(dir, `${name}.json`);
  const bytes = Buffer.from(JSON.stringify(obj) + '\n');
  fs.writeFileSync(file, bytes);
  const p = cp.spawnSync(process.execPath, [checker, file], { encoding: 'utf8' });
  fs.rmSync(dir, { recursive: true, force: true });
  const accepted = p.status === 0;
  let checks = null;
  if (accepted) checks = JSON.parse(p.stdout).checks;
  const rejectionLines = (p.stderr || p.stdout).trim().split('\n').filter(Boolean);
  const rejection = accepted ? null : (
    rejectionLines.find(line => line.startsWith('Error: Verifier:')) ||
    rejectionLines.find(line => line.startsWith('TypeError:')) ||
    rejectionLines.find(line => line.startsWith('Error:')) ||
    rejectionLines.at(-1) || `exit ${p.status}`
  );
  if (accepted !== expected) throw Error(`${name}: expected ${expected}, got ${accepted}: ${rejection}`);
  return { name, accepted, expected, bytes: bytes.length, sha256: sha256(bytes), checks, rejection };
}

function mutateSupport(index, value) {
  const o = clone(seedObj);
  o.fixtures[0].proof[index].support = value;
  return o;
}

const cases = [];
cases.push(run('baseline', clone(seedObj), true));
cases.push(run('single_terminal_string', mutateSupport(2, '012'), true));

const allTerminal = clone(seedObj);
for (const i of [2, 5, 8, 11]) allTerminal.fixtures[0].proof[i].support = allTerminal.fixtures[0].proof[i].support.join('');
cases.push(run('all_four_terminal_strings', allTerminal, true));
fs.writeFileSync(acceptedPath, JSON.stringify(allTerminal) + '\n');

cases.push(run('array_of_string_digits', mutateSupport(2, ['0', '1', '2']), false));
cases.push(run('internal_string', mutateSupport(0, '012'), false));
cases.push(run('duplicate_digit_string', mutateSupport(2, '001'), false));
cases.push(run('short_string', mutateSupport(2, '01'), false));
cases.push(run('wrong_digit_string', mutateSupport(2, '013'), false));
for (const s of ['012','021','102','120','201','210'])
  cases.push(run(`terminal_string_permutation_${s}`, mutateSupport(2, s), true));
cases.push(run('object_with_length', mutateSupport(2, {0:0,1:1,2:2,length:3}), false));

const result = {
  id: 'LSPV-5/511',
  date_local: '2026-11-12 13:48 PST',
  status: 'COMPUTATIONAL accepted-byte counterexample plus PROVED/RESTRICTED checker lemma; P versus NP OPEN',
  target_claim: 'Every accepted /341 AND3 support is an array of distinct integer coordinates.',
  falsifiers_declared_before_search: [
    'one original-CLI acceptance with string-valued AND3 support',
    'stable fresh-process acceptance after replacing every terminal row-producing AND3 support by a string',
    'unchanged source, proof length, sink and cost-relevant structure under the type substitution',
    'hostile nearby strings rejected, showing a genuine narrow checker path rather than bypassed checking'
  ],
  authority: {
    checker: path.relative(root, checker), checker_git_blob: gitBlob(checkerBytes), checker_sha256: sha256(checkerBytes),
    seed: path.relative(root, seed), seed_git_blob: gitBlob(seedBytes), seed_sha256: sha256(seedBytes),
    runtime: process.version, execution: 'fresh OS Node subprocess per verdict'
  },
  mechanism: 'String.prototype.includes coerces each numeric coordinate to a string; string indexing supplies digit characters that coerce back to array indices. Terminal row-producing AND3 nodes feed XOR, so their string support is never spread into a later AND3 union.',
  cases,
  counts: {
    cli_runs: cases.length,
    accepted: cases.filter(x => x.accepted).length,
    rejected: cases.filter(x => !x.accepted).length,
    accepted_assertion_groups: cases.filter(x => x.accepted).reduce((s,x) => s + x.checks, 0)
  },
  accepted_witness: {
    path: path.relative(root, acceptedPath),
    bytes: fs.statSync(acceptedPath).size,
    sha256: sha256(fs.readFileSync(acceptedPath)),
    changed_nodes: [2,5,8,11],
    original_supports: [[0,1,2],[0,3,4],[1,3,5],[2,4,5]],
    accepted_supports: ['012','034','135','245']
  },
  repaired_lemma: 'For the pinned K4 /341 checker, an AND3 support may be either the expected integer array or, at a terminal row-producing AND3 whose coordinates are distinct single decimal digits and which has no AND3 child, any permutation of the corresponding digit string. This relies on the symmetric affine parity table and is not a general grammar theorem.',
  cegar: 'The all-terminal-string packet is genuinely accepted and must remain in any MAY abstraction. Type refinement may reject only concretely rejected preimages.',
  scope: [
    'pinned archived /341 K4 SOURCE/AND3/XOR checker only',
    'no historical mixed dispatcher or Resolution/LOCAL-CONVERT/paid-DEF/branching transfer',
    'no cheaper proof and no proof-size lower bound',
    'P2-D1 type authentication failure; P2-C3 requires a union sort; P2-B1 remains OPEN; P2-B2/B3 separate'
  ]
};
fs.writeFileSync(outPath, JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result, null, 2));
