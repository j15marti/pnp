'use strict';
// LSPV-5/496 independent audit of LSPV-3/578.
// Replays the unchanged peer program in a temporary exact-byte repository,
// then exhaustively checks both source semantics and a source-digest join firewall.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const cp = require('node:child_process');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '../..');
const rel = Object.freeze({
  peer: 'experiments/arc/lspv3_578_dual_native_sat_unsat_polyglot.cjs',
  peer581: 'experiments/arc/lspv1_581_two_fresh_signed_weakening.cjs',
  seed579: 'results/raw/arc/2026-11-11_1200_LSPV1_579_BRIDGE_DP_W61.json',
  witness581: 'results/raw/arc/2026-11-11_1400_LSPV1_581_TWO_FRESH_WEAKENING_ACCEPTED.json',
  peer565: 'experiments/arc/lspv2_565_native386_step_alpha.cjs',
  seed562: 'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json',
  source559: 'results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf',
  peer551: 'experiments/arc/lspv4_551_independent_byte_area.cjs',
  base549: 'results/raw/arc/2026-11-11_1236_LSPV4_549_BRIDGE_W61_BYTE_SAFE_FIVE_SLOT.json',
  old550: 'results/raw/arc/2026-11-11_1331_LSPV4_550_W61_MINAREA_FIVE_SLOT_ACCEPTED.json',
  byte551: 'results/raw/arc/2026-11-11_1436_LSPV4_551_W61_MIN_BYTE_AREA_FIVE_SLOT_ACCEPTED.json',
  slot551: 'results/raw/arc/2026-11-11_1436_LSPV4_551_W61_MIN_SLOT_THEN_BYTE_AREA_ACCEPTED.json',
  checker341: 'experiments/arc/lspv2_341_independent_verify.js',
  checker386: 'experiments/arc/lspv2_386_independent_verify.js',
  sat341: 'results/raw/arc/2026-11-11_0424_LSPV3_568_NUMERIC_WRAP32_SAT_ACCEPTED_PACKET.json',
  unsat386: 'results/raw/arc/2026-11-11_1324_LSPV3_577_LIVE_COMPLEMENTARY_NATIVE386_PACKET.json',
  dual: 'results/raw/arc/2026-11-11_1424_LSPV3_578_DUAL_CHECKER_SAT_UNSAT_PACKET.json'
});
const pinned = Object.freeze({
  peer: 'afdb72b6745e5cb4a603af618afba8a259e73cbe',
  peer581: '9a986410cc43812c1e145b0cdecee30421e7505d',
  seed579: '807aaf7b7cf5e4a4feb29c2599f9e582ea140e30',
  witness581: '31e9fcc0215d93f3abc087043a8bd410a62aba7d',
  peer565: 'f154ff2645601283a028eb28497140a29972f87e',
  seed562: '318c52d99977ea4e91bc8554051138a700c1dc94',
  source559: 'e8bc4300f1f4518cb447edaf3f699bcee4839803',
  peer551: 'c7831e31d7519aa03512597a3e2c6cb2027b0151',
  base549: 'd12f02d2b665c172f806f09e23770d9b76980172',
  old550: 'cbc7044e84bac8e4e1683a2f1637c98f632bdb14',
  byte551: 'a975b7ec8a095421f78bf2567f442b587b5d2596',
  slot551: 'fb5556522e5b476345a6dc30bad14d628e23cebf',
  checker341: 'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
  checker386: '338305c0ce101704205e57543756b8127074a986',
  sat341: 'adb4864906029ecf7b1cd1cf7a4bf513218a13a8',
  unsat386: '5edeac8fbbe39764cfd3d075acd3c6ce7b5c87fe',
  dual: '1c3b400857ab2cfb7d78f37b2723945e6521a83a'
});
function gitBlob(bytes) {
  return crypto.createHash('sha1')
    .update(Buffer.concat([Buffer.from('blob ' + bytes.length + '\0'), bytes]))
    .digest('hex');
}
function exactBytes(key) {
  const bytes = fs.readFileSync(path.join(root, rel[key]));
  if (gitBlob(bytes) === pinned[key]) return bytes;
  // apply_patch materializes a final LF for JSON blobs that had none upstream.
  if (bytes.length && bytes.at(-1) === 10) {
    const stripped = bytes.subarray(0, bytes.length - 1);
    if (gitBlob(stripped) === pinned[key]) return stripped;
  }
  assert.fail('unrecoverable source drift: ' + key + ' got ' + gitBlob(bytes));
}
const exact = Object.fromEntries(Object.keys(rel).map(k => [k, exactBytes(k)]));
function runExactPeer(programKey, dependencyKeys, args = []) {
  const tree = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-496-peer-'));
  try {
    for (const key of [programKey, ...dependencyKeys]) {
      const target = path.join(tree, rel[key]);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, exact[key]);
    }
    const rr = cp.spawnSync(process.execPath, [path.join(tree, rel[programKey]), ...args], {
      cwd: tree, encoding: 'utf8', maxBuffer: 32_000_000, timeout: 30_000
    });
    if (rr.error) throw rr.error;
    assert.equal(rr.status, 0, rr.stderr);
    return JSON.parse(rr.stdout.trim());
  } finally {
    fs.rmSync(tree, { recursive: true, force: true });
  }
}
const peer581 = runExactPeer('peer581',
  ['checker386', 'seed579', 'witness581']);
assert.equal(peer581.cases.length, 12);
assert.equal(peer581.cases.filter(x => x.accepted === x.expected).length, 12);
assert.equal(peer581.cases.find(x => x.name === 'two_fresh_owners').paid, 67);
const peer565 = runExactPeer('peer565',
  ['checker386', 'seed562', 'source559']);
assert.deepEqual(peer565, { count: 10, accepted: 5, rejected: 5, assertions: 17878 });
const peer551 = runExactPeer('peer551',
  ['checker386', 'base549', 'old550', 'byte551', 'slot551'], ['--native-check']);
assert.deepEqual(peer551.by.cost, [1925, 157]);
assert.deepEqual(peer551.sl.cost, [156, 1930]);
assert.equal(peer551.by.states, 1129302);
assert.equal(peer551.sl.states, 1129302);
assert.equal(peer551.native.performed, true);
const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-496-'));
function place(key) {
  const target = path.join(scratch, rel[key]);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, exact[key]);
}
for (const key of Object.keys(rel)) place(key);
let peer;
try {
  const rr = cp.spawnSync(process.execPath, [path.join(scratch, rel.peer)], {
    cwd: scratch, encoding: 'utf8', maxBuffer: 32_000_000, timeout: 30_000
  });
  if (rr.error) throw rr.error;
  assert.equal(rr.status, 0, rr.stderr);
  peer = JSON.parse(rr.stdout);
  assert.equal(peer.all_pass, true);
  assert.equal(peer.cases.length, 10);
  assert.equal(peer.packet_bytes, 14032);
  assert.equal(peer.cases[0].original341.accepted, true);
  assert.equal(peer.cases[0].original386.accepted, true);
} finally {
  fs.rmSync(scratch, { recursive: true, force: true });
}

const packet = JSON.parse(exact.dual);
const fixture = packet.fixtures[0];
const assignment = peer.source341.assignment;
const satClause = clause => clause.literals.some(lit =>
  assignment[Math.abs(lit) - 1] === (lit > 0 ? '1' : '0'));
const satCount = fixture.clauses.filter(satClause).length;
assert.equal(satCount, fixture.clauses.length);

const sourceRecords = packet.records.filter(r => r.kind === 'SOURCE');
assert.equal(sourceRecords.length, 49);
function clauseTrue(c, mask) {
  for (const lit of c) {
    const v = Math.abs(lit);
    const bit = v === 19 ? true : Boolean(mask & (1 << (v - 1)));
    if ((lit > 0) === bit) return true;
  }
  return false;
}
let models386 = 0;
let firstModel386 = null;
for (let mask = 0; mask < (1 << 18); mask++) {
  if (sourceRecords.every(r => clauseTrue(r.c, mask))) {
    models386++;
    if (firstModel386 === null) firstModel386 = mask;
  }
}
assert.equal(models386, 0);

function stable(value) {
  if (Array.isArray(value)) return '[' + value.map(stable).join(',') + ']';
  if (value && typeof value === 'object') {
    return '{' + Object.keys(value).sort().map(k =>
      JSON.stringify(k) + ':' + stable(value[k])).join(',') + '}';
  }
  return JSON.stringify(value);
}
function sha256(value) {
  return crypto.createHash('sha256').update(
    Buffer.isBuffer(value) ? value : Buffer.from(stable(value), 'utf8')
  ).digest('hex');
}
const source341 = {
  calculus: 'archived-341',
  graph: fixture.graph,
  charges: fixture.charges,
  clauses: fixture.clauses
};
const source386 = {
  calculus: 'archived-386',
  spec: packet.spec,
  source_records: sourceRecords.map(r => ({ c: r.c, source: r.source }))
};
const canonical341 = stable(source341);
const canonical386 = stable(source386);
const digest341 = sha256(source341);
const digest386 = sha256(source386);
assert.notEqual(digest341, digest386);
assert.notEqual(canonical341, canonical386);

function joinedFirewall(label, declaredBytes) {
  const accepts341 = declaredBytes === canonical341;
  const accepts386 = declaredBytes === canonical386;
  return { label, telemetry_sha256: sha256(Buffer.from(declaredBytes, 'utf8')),
    accepts341, accepts386, joined: accepts341 && accepts386 };
}
const hostileJoinCases = [
  joinedFirewall('declared-source-341', canonical341),
  joinedFirewall('declared-source-386', canonical386),
  joinedFirewall('declared-empty-source', '')
];
assert.ok(hostileJoinCases.every(x => !x.joined));

const result = {
  id: 'LSPV-5/496',
  run_time_zone: '2026-11-11 14:48 PST',
  target: 'P2-D1 single-source authentication before any cross-checker join',
  exact_git_blobs: pinned,
  execution: {
    peer_lspv1_581: {
      unchanged_program_os_subprocess: true,
      cases: peer581.cases.length,
      decisions_matched: peer581.cases.filter(x => x.accepted === x.expected).length,
      accepted_work: peer581.cases.find(x => x.name === 'two_fresh_owners').paid
    },
    peer_lspv2_565: {
      unchanged_program_os_subprocess: true,
      ...peer565
    },
    peer_lspv4_551: {
      unchanged_program_os_subprocess: true,
      byte_first_cost: peer551.by.cost,
      slot_first_cost: peer551.sl.cost,
      states_each: peer551.by.states,
      native_checker_replays: Object.keys(peer551.native.results).length,
      historical_R_mix341_authenticated: peer551.historical_R_mix341_authenticated
    },
    peer_program_unchanged: true,
    peer_program_os_subprocess: true,
    archived_checkers_unchanged: true,
    differential_cases: peer.cases.length,
    differential_cases_passed: peer.cases.filter(x => x.pass).length,
    dual_packet_bytes: exact.dual.length,
    dual_packet_sha256: sha256(exact.dual),
    checker341_baseline: peer.cases[0].original341,
    checker386_baseline: peer.cases[0].original386
  },
  independent_semantics: {
    source341: {
      variables: assignment.length,
      assignment,
      clauses_satisfied: satCount,
      clauses_total: fixture.clauses.length,
      satisfiable: true
    },
    source386: {
      enumerated_assignments: 1 << 18,
      guard_fixed_true: true,
      source_clauses: sourceRecords.length,
      satisfying_assignments: models386,
      first_model: firstModel386,
      unsatisfiable: true
    }
  },
  source_join_firewall: {
    canonicalization: 'recursive sorted-key UTF-8 JSON with explicit calculus tag',
    authority: 'exact canonical byte equality; SHA-256 values are telemetry only',
    digest341,
    digest386,
    telemetry_digests_equal: digest341 === digest386,
    exact_canonical_bytes_equal: canonical341 === canonical386,
    hostile_declared_digest_cases: hostileJoinCases,
    dual_acceptance_without_common_source: true,
    repaired_rule: 'accept a joined derivation only if every component checker verifies the same externally supplied canonical source bytes'
  },
  classification: {
    family_failure: false,
    P2_D1: 'FALSIFIED for naive acceptance intersection; repaired exact-source join validated on this witness',
    P2_C3: 'OPEN',
    P2_B1: 'OPEN',
    P2_B2_B3_transfer: 'UNSUPPORTED'
  },
  limitations: [
    'The firewall is a repaired interface lemma, not authentication of historical R_mix341.',
    'SHA-256 is reporting telemetry only; the proof-level firewall uses exact canonical byte equality.',
    'The two archived checkers remain sibling languages, not one mixed-calculus checker.',
    'Finite exhaustive semantics does not prove a proof-size lower bound.'
  ],
  p_vs_np: 'OPEN'
};
console.log(JSON.stringify(result, null, 2));

