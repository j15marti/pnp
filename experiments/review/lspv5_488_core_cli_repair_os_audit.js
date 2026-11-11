#!/usr/bin/env node
'use strict';

/* LSPV-5/488 independent OS replay and result validator for LSPV-4/542. */
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const {spawnSync} = require('node:child_process');

const root = path.resolve(__dirname, '../..');
const checker = path.join(root, 'experiments/arc/lspv2_386_independent_verify.js');
const peer = path.join(root, 'experiments/arc/lspv4_542_core_cli_repair.cjs');
const peer543 = path.join(root, 'experiments/arc/lspv4_543_native_inmemory_firewall.cjs');
const defaultOut = path.join(root, 'results/raw/arc/2026-11-11_0648_LSPV5_488_CORE_CLI_REPAIR_OS_RAW.json');
const expected = {
  checker: '338305c0ce101704205e57543756b8127074a986',
  peer: '4fbb1896cc9acda0249fd10536ce1522936ea6ae',
  peer543: '011ab55397245973328a19cedf2eb04dc98f9692',
  seeds: {
    'results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CORE28.json': 'c68eeaf67015416dae49a34ad5ce25432b839bee',
    'results/raw/arc/2026-11-11_0057_LSPV1_567_PIVOT999999_CORE_ONLY_PACKET.json': 'b2216a95f65d765028410ec3db9520dfcb104015',
    'results/raw/arc/2026-11-11_0057_LSPV1_567_NEGATIVE_PIVOT_CLI_ACCEPT_PACKET.json': '717970007a1988cda31b70ac5abce8fd81519f4c',
    'results/raw/arc/2026-11-11_0336_LSPV4_540_OWNER_FACET_CROSS_CONE_ACCEPTED.json': '25b5c1f95734f6eae36bdbb4a17c948c00753cff'
  }
};

function blobSha(file) {
  const b = fs.readFileSync(file);
  return crypto.createHash('sha1').update(Buffer.concat([
    Buffer.from(`blob ${b.length}\0`), b
  ])).digest('hex');
}
function sha256(b) { return crypto.createHash('sha256').update(b).digest('hex'); }
function bytes(file) { return fs.statSync(file).size; }

function main() {
  const t0 = process.hrtime.bigint();
  const checks = [];
  function check(ok, label) { assert.ok(ok, label); checks.push(label); }

  check(blobSha(checker) === expected.checker, 'pinned archived /386 checker blob');
  check(blobSha(peer) === expected.peer, 'pinned LSPV-4/542 runner blob');
  check(blobSha(peer543) === expected.peer543, 'pinned LSPV-4/543 runner blob');
  for (const [rel, sha] of Object.entries(expected.seeds))
    check(blobSha(path.join(root, rel)) === sha, `pinned seed ${rel}`);

  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lspv5-488-'));
  const peerRaw = path.join(tmp, 'peer-os.json');
  const runStart = process.hrtime.bigint();
  const run = spawnSync(process.execPath, [peer, peerRaw], {
    cwd: root, encoding: 'utf8', maxBuffer: 16 * 1024 * 1024
  });
  const runnerElapsedMs = Number(process.hrtime.bigint() - runStart) / 1e6;
  try {
    check(run.status === 0, `peer OS runner exited zero: ${run.stderr}`);
    check(fs.existsSync(peerRaw), 'peer raw result exists');
    const rawBytes = fs.readFileSync(peerRaw);
    const p = JSON.parse(rawBytes);
    check(p.originalCodeUnmodified === true, 'runner records original checker unmodified');
    check(p.checkerBlob === expected.checker, 'runner checker blob agrees');
    check(p.caseCount === 7 && p.observations.length === 7, 'seven theorem cases');
    check(p.hostileCount === 6 && p.hostiles.length === 6, 'six hostile cases');
    check(p.exactOriginalOSSubprocesses === 20, 'twenty exact OS checker subprocesses');
    check(p.observations.every(x => x.coreBefore.accepted && x.coreAfter.accepted), 'all before/after mathematical cores accept');
    check(p.observations.filter(x => x.original.accepted).length === 3, 'exactly three originals pass full CLI');
    check(p.observations.every(x => x.repaired.accepted), 'all seven repairs pass full CLI');
    check(p.hostiles.every(x => x.coreReject && x.originalCliReject), 'all hostiles rejected by core and CLI');

    const byName = Object.fromEntries(p.observations.map(x => [x.name, x]));
    check(byName.core28_no_gate_normal.coreAfter.paid === byName.core28_no_gate_normal.coreBefore.paid + 1,
      'zero-owner normal repair costs exactly one');
    check(byName.core28_no_gate_sentinel.coreAfter.paid === byName.core28_no_gate_sentinel.coreBefore.paid + 1,
      'zero-owner sentinel repair costs exactly one');
    check(p.observations.slice(2).every(x => x.coreAfter.paid === x.coreBefore.paid),
      'nonempty-owner repairs preserve paid cost');
    check(!byName.core28_no_gate_sentinel.original.accepted && byName.core28_no_gate_sentinel.repaired.accepted,
      'combined zero-owner/+999999 case repaired');
    check(!byName.core29_one_gate_sentinel.original.accepted && byName.core29_one_gate_sentinel.repaired.accepted,
      'positive sentinel repaired at zero extra cost when owner exists');
    check(byName.nested_56_paid_positive_sentinel.coreBefore.paid === 56 &&
      byName.nested_56_paid_positive_sentinel.repaired.paid === 56,
      'nested 56-paid sentinel repair preserves cost');
    check(p.hostiles.some(x => x.name === 'terminalPivotWithoutParentSwap'),
      'missing parent swap is an explicit reject');
    check(p.hostiles.some(x => x.name === 'invalidOwnerInput'),
      'invalid owner input is an explicit reject');

    const successes = p.observations.flatMap(x => [x.original, x.repaired]).filter(x => x.accepted);
    const assertionTotal = successes.reduce((s, x) => s + x.assertions, 0);
    const repairedNegativeTests = p.observations.reduce((s, x) => s + x.repaired.negativeTests, 0);
    check(assertionTotal === 39907, '39,907 successful-checker assertion groups');
    check(repairedNegativeTests === 77, '77 bundled hostile tests on repaired packets');

    const run543Start = process.hrtime.bigint();
    const run543 = spawnSync(process.execPath, [peer543], {
      cwd: root, encoding: 'utf8', maxBuffer: 16 * 1024 * 1024
    });
    const runner543ElapsedMs = Number(process.hrtime.bigint() - run543Start) / 1e6;
    check(run543.status === 0, `peer 543 OS runner exited zero: ${run543.stderr}`);
    const p543 = JSON.parse(run543.stdout);
    check(p543.all_passed === true && p543.rows.length === 5, '543 has five accepted OS cases');
    check(p543.bad.length === 5 && p543.bad.every(x => x.rejected), '543 has five rejected hostiles');
    check(p543.rows.every(x => x.positive_cli && x.paid === 31), '543 preserves W=31 across all k');
    check(p543.rows.reduce((s,x) => s + x.assertion_groups, 0) === 44540,
      '543 passes 44,540 original assertion groups');

    const timeLine = null;
    const output = {
      id: 'LSPV5-488',
      timestamp: '2026-11-11 06:48 PST',
      status: 'COMPUTATIONAL independent exact OS replay + restricted theorem validation',
      target: 'LSPV-4/542 archived /386 mathematical-core to full-CLI repair',
      provenance: {
        checkerBlob: expected.checker,
        peerRunnerBlob: expected.peer,
        peer543RunnerBlob: expected.peer543,
        seedBlobs: expected.seeds,
        node: process.version,
        platform: process.platform,
        arch: process.arch
      },
      execution: {
        peerExit: run.status,
        peerStdout: run.stdout.trim(),
        timeLine,
        exactOriginalOSSubprocesses: p.exactOriginalOSSubprocesses,
        successfulCheckerAssertionGroups: assertionTotal,
        repairedBundledNegativeTests: repairedNegativeTests,
        validatorAssertions: checks.length,
        runnerElapsedMs,
        runner543ElapsedMs,
        peer543Exit: run543.status,
        peer543StdoutSha256: sha256(Buffer.from(run543.stdout)),
        elapsedMs: Number(process.hrtime.bigint() - t0) / 1e6
      },
      inputLedger: {
        checkerBytes: bytes(checker),
        peerRunnerBytes: bytes(peer),
        peer543RunnerBytes: bytes(peer543),
        seedBytes: Object.fromEntries(Object.keys(expected.seeds).map(rel => [rel, bytes(path.join(root, rel))])),
        peerRawBytes: rawBytes.length,
        peerRawSha256: sha256(rawBytes)
      },
      result: {
        cases: p.caseCount,
        originalFullCliAccepts: p.observations.filter(x => x.original.accepted).length,
        repairedFullCliAccepts: p.observations.filter(x => x.repaired.accepted).length,
        hostilesRejectedByCoreAndCli: p.hostiles.filter(x => x.coreReject && x.originalCliReject).length,
        costDeltas: p.observations.map(x => ({name:x.name, before:x.coreBefore.paid, after:x.coreAfter.paid})),
        combinedCase: {
          name: 'core28_no_gate_sentinel',
          originalFullCliAccepted: byName.core28_no_gate_sentinel.original.accepted,
          repairedFullCliAccepted: byName.core28_no_gate_sentinel.repaired.accepted,
          paidBefore: byName.core28_no_gate_sentinel.coreBefore.paid,
          paidAfter: byName.core28_no_gate_sentinel.coreAfter.paid
        },
        latestPeer543: {
          acceptedCases: p543.rows.length,
          rejectedHostiles: p543.bad.length,
          paidValues: [...new Set(p543.rows.map(x => x.paid))],
          recordCounts: p543.rows.map(x => x.records),
          sourceCodeMinSimultaneousReferenceEntries: p543.rows.map(x => x.source_code_min_simultaneous_reference_entries),
          assertionGroups: p543.rows.reduce((s,x) => s + x.assertion_groups, 0)
        }
      },
      resourcePolarity: {
        logicalPaidNodes: 'exact from original checker summaries',
        evidenceBytes: 'exact serialized byte counts',
        elapsedAndRss: 'parent monotonic elapsed time recorded; child-process peak RSS unavailable in this container',
        proofDagWorkToMemory: 'not inferred',
        configurationCountToMemory: 'not inferred'
      },
      limitations: [
        'The archived /386 checker authenticates SOURCE, conservative paid AND2 owners, free DEF facets and strict RES only.',
        'This does not authenticate complete historical R_mix341, external source hashes, branching, contexts, discharge, joins, weakening, GF(2), AND3 or LOCAL-CONVERT.',
        'Finite OS replay is not a proof-complexity lower bound and does not close P2-D1, P2-C3, P2-B1, P2-B2 or B3.',
        'P versus NP remains OPEN.'
      ],
      checks
    };
    fs.mkdirSync(path.dirname(defaultOut), {recursive:true});
    fs.writeFileSync(process.argv[2] || defaultOut, JSON.stringify(output, null, 2) + '\n');
    console.log(JSON.stringify({ok:true, output:process.argv[2] || defaultOut, checks:checks.length,
      cases:p.caseCount, hostiles:p.hostileCount, assertions:assertionTotal,
      latestPeer543Cases:p543.rows.length, latestPeer543Hostiles:p543.bad.length,
      repairedNegativeTests, combinedCost:[28,29], timeLine}, null, 2));
  } finally {
    fs.rmSync(tmp, {recursive:true, force:true});
  }
}
main();
