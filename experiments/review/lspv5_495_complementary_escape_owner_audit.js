#!/usr/bin/env node
'use strict';

// LSPV-5/495 independent OS audit of LSPV-3/577.
// Restricted to the unchanged archived /386 SOURCE/AND2-facet/RES checker.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const cp = require('node:child_process');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '../..');
const checkerPath = path.join(root, 'experiments/arc/lspv2_386_independent_verify.js');
const livePath = path.join(root, 'results/raw/arc/2026-11-11_1324_LSPV3_577_LIVE_COMPLEMENTARY_NATIVE386_PACKET.json');
const seedPath = path.join(root, 'results/raw/arc/2026-11-11_0224_LSPV3_566_K4x3_CLI_ACCEPTED_PACKET.json');
const outputPath = process.argv[2] || path.join(root, 'results/raw/arc/2026-11-11_1348_LSPV5_495_COMPLEMENTARY_ESCAPE_OWNER_RAW.json');

const exact = p => fs.readFileSync(p, 'utf8');
const clone = x => JSON.parse(JSON.stringify(x));
const sha256 = s => crypto.createHash('sha256').update(s).digest('hex');
const gitBlob = s => crypto.createHash('sha1')
  .update(Buffer.concat([Buffer.from('blob ' + Buffer.byteLength(s) + '\0'), Buffer.from(s)]))
  .digest('hex');

const checkerText = exact(checkerPath);
const liveText = exact(livePath).trimEnd();
const seedText = exact(seedPath);
assert.equal(gitBlob(checkerText), '338305c0ce101704205e57543756b8127074a986');
assert.equal(gitBlob(liveText), '5edeac8fbbe39764cfd3d075acd3c6ce7b5c87fe');
assert.equal(gitBlob(seedText), '4656b801feba72b84133bacad5ae18692a83fe03');
assert.equal(Buffer.byteLength(liveText), 5455);

const live = JSON.parse(liveText);
const seed = JSON.parse(seedText);
const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'pnp495-'));

function terminalAncestry(p) {
  const seen = new Set();
  const stack = [p.records.length - 1];
  while (stack.length) {
    const i = stack.pop();
    if (seen.has(i)) continue;
    const r = p.records[i];
    if (!r) throw new Error('invalid ancestry record ' + i);
    seen.add(i);
    for (const j of r.parents) stack.push(j);
  }
  return seen;
}

function run(label, packet, expected) {
  const serialized = JSON.stringify(packet);
  const input = path.join(temp, label + '.json');
  fs.writeFileSync(input, serialized);
  const proc = cp.spawnSync(process.execPath, [checkerPath, input], {
    encoding: 'utf8', timeout: 30000, maxBuffer: 1 << 22
  });
  if (proc.error) throw proc.error;
  const accepted = proc.status === 0;
  assert.equal(accepted, expected, label + ': ' + String(proc.stderr || proc.stdout).slice(0, 300));
  const row = {
    label, accepted, raw_bytes: Buffer.byteLength(serialized), sha256: sha256(serialized),
    exit_status: proc.status
  };
  if (accepted) {
    row.verifier = JSON.parse(proc.stdout.trim());
    row.terminal_ancestors = terminalAncestry(packet).size;
  } else {
    row.error = String(proc.stderr || proc.stdout).trim().split('\n').slice(0, 3).join(' | ');
  }
  return row;
}

try {
  const tests = [];
  tests.push(run('exact_5455_byte_live_packet', live, true));
  tests.push(run('exact_seed_baseline', seed, true));

  const underpaid = clone(live);
  underpaid.summary.paid_total--;
  tests.push(run('underpaid_second_owner', underpaid, false));

  const missingOwner = clone(live);
  missingOwner.gate_defs.splice(2, 1);
  missingOwner.summary.paid_gates--;
  missingOwner.summary.paid_total--;
  tests.push(run('deleted_second_owner_but_kept_facets', missingOwner, false));

  const collision = clone(live);
  collision.gate_defs[2][1] = 21;
  tests.push(run('second_owner_output_collides_with_false_wire', collision, false));

  const noPositiveZFacet = clone(live);
  noPositiveZFacet.records[20].c = [-1, -21, 22];
  tests.push(run('remove_first_positive_z_facet', noPositiveZFacet, false));

  const dead = clone(live);
  for (let i = 25; i < dead.records.length; i++) {
    if (dead.records[i].kind === 'RES') {
      dead.records[i].parents = dead.records[i].parents.map(j => j === 24 ? 0 : j);
    }
  }
  tests.push(run('accepted_unrewired_dead_control', dead, true));
  assert.equal(terminalAncestry(dead).has(17), false);
  assert.equal(terminalAncestry(live).has(17), true);

  // Syntactic provenance audit: Resolution can only remove pivot literals and
  // union the rest, so it cannot be the first primitive source of +z.
  const z = 21;
  const primitivePositiveZ = [];
  const firstPositiveZ = [];
  for (let i = 0; i < live.records.length; i++) {
    const r = live.records[i];
    if (r.c.includes(z)) {
      firstPositiveZ.push(i);
      if (r.kind !== 'RES') primitivePositiveZ.push(i);
    }
    if (r.kind === 'RES') {
      const [a, b] = r.parents.map(j => live.records[j].c);
      for (const lit of r.c) assert(a.includes(lit) || b.includes(lit));
    }
  }
  assert.deepEqual(primitivePositiveZ, [20]);
  assert.equal(live.records[20].kind, 'DEF');
  assert.equal(live.records[20].gate, 2);
  assert.deepEqual(live.gate_defs[2], [2, 22, -21, 1]);
  assert.equal(terminalAncestry(live).has(20), true);

  // Reproduce the published OS wrapper's deterministic post-rejection defect:
  // after the checker rejects its future-parent hostile, the wrapper calls
  // ancestry(p) unconditionally and dereferences an out-of-range record.
  const futureParent = clone(live);
  futureParent.records[22].parents[1] = futureParent.records.length;
  tests.push(run('future_parent_checker_rejects', futureParent, false));
  let postRejectAncestryError = null;
  try {
    terminalAncestry(futureParent);
  } catch (e) {
    postRejectAncestryError = String(e.message);
  }
  assert.match(postRejectAncestryError, /invalid ancestry record/);

  const result = {
    run: 'LSPV-5/495',
    timestamp: '2026-11-11 13:48 PST',
    target: 'LSPV-3/577 terminal-live complementary gate and escape-owner cut',
    scope: 'unchanged archived /386 SOURCE/paid-AND2-facet/strict-RES checker only',
    authority: {
      checker_git_blob: gitBlob(checkerText),
      seed_git_blob: gitBlob(seedText),
      live_packet_git_blob: gitBlob(liveText),
      live_packet_bytes: Buffer.byteLength(liveText),
      live_packet_sha256: sha256(liveText),
      node: process.version,
      platform: process.platform
    },
    result: {
      exact_live_packet_accepted: true,
      exact_live_paid_total: live.summary.paid_total,
      seed_paid_total: seed.summary.paid_total,
      exact_delta: live.summary.paid_total - seed.summary.paid_total,
      live_terminal_ancestors: terminalAncestry(live).size,
      dead_control_terminal_ancestors: terminalAncestry(dead).size,
      inserted_live_indices: Array.from({length: 8}, (_, i) => 17 + i)
        .filter(i => terminalAncestry(live).has(i)),
      primitive_positive_z_records: primitivePositiveZ,
      first_positive_z_record: firstPositiveZ[0],
      first_positive_z_owner: live.gate_defs[2],
      post_rejection_wrapper_defect: postRejectAncestryError
    },
    tests,
    theorem_scope: 'For this restricted grammar, original SOURCE clauses contain no auxiliary z; a complementary owner z=(ell AND NOT ell) exposes only negative-z non-tautological facets; strict Resolution introduces no fresh literal. Therefore a terminal-live route through a z-bearing clause to the empty clause must cross a later authenticated primitive clause containing positive z. In the /577 witness that unique primitive escape is record 20, a facet of the second globally paid owner [2,22,-21,1].',
    limits: 'This is not a minimum-cost theorem, not a full mixed R_mix341 checker, and not a P2-D1/P2-C3/P2-B1 closure. P2-B2/B3 remain separate. P versus NP remains OPEN.'
  };
  fs.mkdirSync(path.dirname(outputPath), {recursive: true});
  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify(result, null, 2));
} finally {
  fs.rmSync(temp, {recursive: true, force: true});
}
