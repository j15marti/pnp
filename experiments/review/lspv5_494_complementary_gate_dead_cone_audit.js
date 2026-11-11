#!/usr/bin/env node
'use strict';

// LSPV-5/494 independent red-team audit.
// Tests the original archived /386 checker, not a reimplementation.
// Usage:
//   node experiments/review/lspv5_494_complementary_gate_dead_cone_audit.js \
//     [raw-output.json] [accepted-k8-packet.json]

const assert = require('node:assert/strict');
const cp = require('node:child_process');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '../..');
const CHECKER = path.join(ROOT, 'experiments/arc/lspv2_386_independent_verify.js');
const SEED = path.join(ROOT, 'results/raw/arc/2026-11-11_0224_LSPV3_566_K4x3_CLI_ACCEPTED_PACKET.json');
const CHECKER_BLOB = '338305c0ce101704205e57543756b8127074a986';
const SEED_BLOB = '4656b801feba72b84133bacad5ae18692a83fe03';

function gitBlob(buf) {
  return crypto.createHash('sha1').update(Buffer.concat([
    Buffer.from(`blob ${buf.length}\0`), buf
  ])).digest('hex');
}
function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }
function clone(x) { return JSON.parse(JSON.stringify(x)); }
function canon(c) {
  return [...new Set(c)].sort((x, y) => Math.abs(x) - Math.abs(y) || x - y);
}

const checkerBytes = fs.readFileSync(CHECKER);
const seedBytes = fs.readFileSync(SEED);
assert.equal(gitBlob(checkerBytes), CHECKER_BLOB, 'authoritative checker bytes changed');
assert.equal(gitBlob(seedBytes), SEED_BLOB, 'seed bytes changed');
const seed = JSON.parse(seedBytes);

function produce(k) {
  assert(Number.isSafeInteger(k) && k >= 0 && k <= 4096);
  const p = clone(seed);
  const terminal = p.records.pop();
  const added = [];
  for (let j = 1; j <= k; j++) {
    const z = 20 + j;
    p.gate_defs.push([j, z, 1, -1]);
    const left = p.records.length + added.length;
    added.push({kind: 'DEF', c: canon([1, -z]), parents: [], gate: j});
    const right = p.records.length + added.length;
    added.push({kind: 'DEF', c: canon([-1, -z]), parents: [], gate: j});
    added.push({kind: 'RES', c: [-z], parents: [left, right], pivot: 1});
  }
  p.records.push(...added, terminal);
  p.summary.def_views += 2 * k;
  p.summary.resolution += k;
  p.summary.paid_gates += k;
  p.summary.paid_total += 2 * k;
  p.summary.live_records += 3 * k;
  return {packet: p, addedStart: p.records.length - 1 - 3 * k, addedCount: 3 * k};
}

function terminalAncestry(records) {
  const seen = new Set();
  const stack = [records.length - 1];
  while (stack.length) {
    const i = stack.pop();
    if (seen.has(i)) continue;
    seen.add(i);
    stack.push(...records[i].parents);
  }
  return seen;
}

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-494-'));
function native(label, packet, expected) {
  const raw = Buffer.from(JSON.stringify(packet) + '\n');
  const file = path.join(tmp, label + '.json');
  fs.writeFileSync(file, raw);
  const r = cp.spawnSync(process.execPath, [CHECKER, file], {
    encoding: 'utf8', timeout: 30000, maxBuffer: 4 << 20
  });
  if (r.error) throw r.error;
  const accepted = r.status === 0;
  assert.equal(accepted, expected, `${label}: ${(r.stderr || r.stdout).slice(0, 500)}`);
  let checkerResult = {};
  if (accepted) {
    const parsed = JSON.parse(r.stdout.trim().split('\n').at(-1));
    delete parsed.file; // ephemeral temp path is not part of the evidence
    checkerResult = parsed;
  } else {
    checkerResult = {error: (r.stderr || r.stdout).trim().slice(0, 300)};
  }
  return {
    label, accepted, bytes: raw.length, sha256: sha256(raw), git_blob: gitBlob(raw),
    ...checkerResult
  };
}

function polarityAudit(packet, addedStart, addedCount) {
  const ancestry = terminalAncestry(packet.records);
  const addedIndices = Array.from({length: addedCount}, (_, j) => addedStart + j);
  const addedVars = new Set(packet.gate_defs.slice(1).map(g => g[1]));
  const sourceHasAddedVar = packet.records.some(r => r.kind === 'SOURCE' &&
    r.c.some(x => addedVars.has(Math.abs(x))));
  const positiveOccurrences = packet.records.flatMap((r, i) =>
    r.c.filter(x => addedVars.has(x)).map(x => ({record: i, literal: x})));
  const negativeOccurrences = packet.records.flatMap((r, i) =>
    r.c.filter(x => x < 0 && addedVars.has(-x)).map(x => ({record: i, literal: x})));
  return {
    terminal_ancestry_size: ancestry.size,
    all_added_records_dead: addedIndices.every(i => !ancestry.has(i)),
    added_records_in_terminal_ancestry: addedIndices.filter(i => ancestry.has(i)),
    source_has_added_variable: sourceHasAddedVar,
    positive_added_wire_occurrences: positiveOccurrences,
    negative_added_wire_occurrence_count: negativeOccurrences.length,
    empty_clause_contains_added_wire: packet.records.at(-1).c.some(x => addedVars.has(Math.abs(x)))
  };
}

try {
  const positives = [];
  let witness = null;
  for (const k of [0, 1, 2, 8, 64]) {
    const made = produce(k);
    const replay = native('k' + k, made.packet, true);
    const polarity = polarityAudit(made.packet, made.addedStart, made.addedCount);
    assert.equal(replay.paid, 29 + 2 * k);
    assert.equal(replay.def, 1 + k);
    assert.equal(replay.res, 28 + k);
    assert.equal(polarity.all_added_records_dead, true);
    assert.equal(polarity.source_has_added_variable, false);
    assert.deepEqual(polarity.positive_added_wire_occurrences, []);
    positives.push({k, ...replay, polarity});
    if (k === 8) witness = made.packet;
  }

  const hostile = {};
  const edits = {
    forged_positive_facet(p) { p.records[p.records.length - 4].c = [21]; },
    forged_positive_unit(p) { p.records[p.records.length - 2].c = [21]; },
    wrong_resolvent(p) { p.records[p.records.length - 2].c = [-21, 1]; },
    future_parent(p) { p.records[p.records.length - 2].parents[0] = p.records.length + 3; },
    undercharge(p) { p.summary.paid_total--; },
    forged_source(p) { p.records[0].c[0] = -p.records[0].c[0]; }
  };
  for (const [label, edit] of Object.entries(edits)) {
    const p = produce(1).packet;
    edit(p);
    hostile[label] = native(label, p, false);
  }

  const result = {
    run: 'LSPV-5/494',
    timestamp: '2026-11-11 12:48 PST',
    status: 'PROVED/RESTRICTED syntactic polarity lemma + COMPUTATIONAL original-checker replay',
    checker: {path: path.relative(ROOT, CHECKER), git_blob: CHECKER_BLOB, sha256: sha256(checkerBytes)},
    seed: {path: path.relative(ROOT, SEED), git_blob: SEED_BLOB, sha256: sha256(seedBytes)},
    exact_scope: 'archived /386 SOURCE/paid-AND2/free-DEF/strict-Resolution complete CLI; not full historical R_mix341',
    symbolic_lemma: {
      premise: 'fresh complementary owner z = a AND (-a); checker drops tautological positive-z view',
      admitted_views: ['[-z,a]', '[-z,-a]'],
      consequence: 'SOURCE omits z and strict Resolution cannot invent +z; every descendant of a gate facet retains -z; no such descendant is the empty clause',
      terminal_liveness: false
    },
    positives,
    hostile_rejections: hostile,
    accepted_k8_packet_sha256: sha256(Buffer.from(JSON.stringify(witness) + '\n')),
    resource_firewall: 'paid W inflation is dead certificate work, not minimum refutation work, live proof space, physical memory, or SAT time',
    tracker_status: 'TRACKERS REVIEWED; NO MATERIAL CHANGE',
    open: ['P2-D1', 'P2-C3', 'P2-B1', 'P2-B2', 'P2-B3', 'P versus NP']
  };
  if (process.argv[2]) fs.writeFileSync(process.argv[2], JSON.stringify(result, null, 2) + '\n');
  if (process.argv[3]) fs.writeFileSync(process.argv[3], JSON.stringify(witness) + '\n');
  console.log(JSON.stringify(result, null, 2));
} finally {
  fs.rmSync(tmp, {recursive: true, force: true});
}
