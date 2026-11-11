#!/usr/bin/env node
"use strict";

// LSPV-5/492: independent audit of LSPV-1/576 and LSPV-4/547.
// This does not modify either peer artifact. It records the exact /576
// reproducer failure, independently reconstructs its finite theorem, and
// separately replays the /547 fixed-DAG slot recurrence.

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const cp = require("node:child_process");
const crypto = require("node:crypto");
const os = require("node:os");

const root = path.resolve(__dirname, "../..");
const rel = {
  peer576: "experiments/arc/lspv1_576_bridge_exact_core_lower.cjs",
  peer547: "experiments/arc/lspv4_547_exact_bridge_fresh_slot.cjs",
  peer561: "experiments/arc/lspv2_561_native386_paid_fanout_congruence.cjs",
  seed560: "results/raw/arc/2026-11-11_0912_LSPV2_560_ACCEPTED_TRIMMED_NATIVE386_K4.json",
  peer574: "experiments/arc/lspv3_574_arbitrary_topology_source_gauge.cjs",
  seed563: "results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json",
  packet575: "results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json",
  checker386: "experiments/arc/lspv2_386_independent_verify.js",
  raw576: "results/raw/arc/2026-11-11_0957_LSPV1_576_BRIDGE_EXACT_CORE_LOWER_RAW.json",
  out: "results/raw/arc/2026-11-11_1048_LSPV5_492_BRIDGE_LOWER_SLOT_POLARITY_RAW.json"
};
const abs = key => path.join(root, rel[key]);
const bytes = key => fs.readFileSync(abs(key));
const read = key => JSON.parse(bytes(key).toString("utf8"));
const sha256 = b => crypto.createHash("sha256").update(b).digest("hex");
const gitBlob = b => crypto.createHash("sha1")
  .update(Buffer.concat([Buffer.from("blob " + b.length + "\0"), b])).digest("hex");

const pins = {
  peer576: "9c2564971d6d69568f1c6aad23e800e14409ed6c",
  peer547: "b26b40f5d80f0bc6dec6d773ce91792c0df91089",
  peer561: "40b5ad61194b327844ebd3c8de38a23148a75aee",
  seed560: "3843187f0ccccf8f04cc049e25a8de1df91ce194",
  peer574: "b1968992a77c1561b3d7a85df1864bf69a73170c",
  packet575: "d5de0f477cd736ec5fd7b01be18350f9cb594fd2",
  checker386: "338305c0ce101704205e57543756b8127074a986",
  raw576: "4567f1002fe5b58b60d713f07eac266e443ed01c"
};
for (const [k, v] of Object.entries(pins)) {
  assert.equal(gitBlob(bytes(k)), v, k + " blob mismatch");
}

const EDGES = [[0,3],[0,4],[1,2],[1,3],[1,4],[2,3],[2,4],
  [5,8],[5,9],[6,7],[6,8],[6,9],[7,8],[7,9],[0,5]];
const CHARGE = [1,0,0,0,0,0,0,0,0,0];
const GUARD = 16;
const occ = Array.from({length:10}, () => []);
for (let e = 0; e < EDGES.length; e++) for (const v of EDGES[e]) occ[v].push(e + 1);
assert(occ.every(x => x.length === 3));
const canonical = c => [...new Set(c)].sort((a,b) => Math.abs(a)-Math.abs(b) || a-b);
const rows = [];
for (let v = 0; v < 10; v++) for (let bits = 0; bits < 8; bits++) {
  const parity = ((bits&1)+((bits>>1)&1)+((bits>>2)&1)) & 1;
  if (parity === CHARGE[v]) continue;
  rows.push({vertex:v, pattern:bits,
    c:canonical([...occ[v].map((e,i) => ((bits>>i)&1) ? -e : e), -GUARD])});
}
assert.equal(rows.length, 40);
const source = [...rows.map(r => r.c), [GUARD]];
const sat = (c, mask, guard=true) => c.some(l => {
  const bit = Math.abs(l) === GUARD ? Number(guard) : ((mask >> (Math.abs(l)-1)) & 1);
  return (l > 0) === Boolean(bit);
});

const singleton = {};
const histogram = {};
for (let mask = 0; mask < (1<<15); mask++) {
  const violated = [];
  for (let i = 0; i < 40; i++) if (!sat(rows[i].c, mask)) violated.push(i);
  histogram[violated.length] = (histogram[violated.length] || 0) + 1;
  if (violated.length === 1 && singleton[violated[0]] === undefined) singleton[violated[0]] = mask;
}
const essential = Object.keys(singleton).map(Number).sort((a,b)=>a-b);
const dispensable = Array.from({length:40}, (_,i)=>i).filter(i => singleton[i] === undefined);
assert.equal(essential.length, 36);
assert.deepEqual(dispensable, [2,3,20,21]);
let coreModels = 0;
for (let mask = 0; mask < (1<<15); mask++) {
  if (essential.every(i => sat(rows[i].c, mask))) coreModels++;
}
assert.equal(coreModels, 0);
for (const i of essential) {
  const m = singleton[i];
  assert(!sat(rows[i].c, m));
  assert(rows.every((r,j) => j === i || sat(r.c, m)));
}

// Compare the independently reconstructed theorem with the published raw
// schema, which intentionally differs from the peer script's internal schema.
const published = read("raw576");
assert.equal(published.assignments_tested, 32768);
assert.equal(published.core_models, 0);
assert.equal(published.unique_minimum_unsat_core_size_including_guard, 37);
assert.equal(published.proved_native_core_res_lower, 36);
assert.equal(published.proved_native_full_cli_work_lower, 37);
assert.deepEqual(published.globally_indispensable_source_ordinals, essential);
assert.deepEqual(published.globally_dispensable_source_ordinals, dispensable);

const packet = read("packet575");
const keyClause = c => JSON.stringify(c);
const nativeSources = packet.records
  .map((r,i) => ({...r, index:i})).filter(r => r.kind === "SOURCE");
assert.deepEqual(nativeSources.map(r => keyClause(r.c)).sort(),
  source.map(keyClause).sort());
const seen = new Set(), todo = [packet.records.length - 1];
while (todo.length) {
  const i = todo.pop();
  if (seen.has(i)) continue;
  seen.add(i);
  for (const p of packet.records[i].parents || []) todo.push(p);
}
const dead = nativeSources.filter(r => !seen.has(r.index));
assert.equal(dead.length, 4);
assert.deepEqual(dead.map(r => keyClause(r.c)).sort(),
  dispensable.map(i => keyClause(rows[i].c)).sort());

const checker = cp.spawnSync(process.execPath, [abs("checker386"), abs("packet575")],
  {encoding:"utf8", timeout:30000, maxBuffer:4<<20});
assert.equal(checker.status, 0, checker.stderr);
const checkerOut = JSON.parse(checker.stdout.trim().split(/\n/).at(-1));
assert.equal(checkerOut.paid, 63);
assert.equal(checkerOut.res, 62);
assert.equal(checkerOut.sources, 41);
assert.equal(checkerOut.negativeTests, 11);

const peer576Text = bytes("peer576").toString("utf8");
assert(peer576Text.includes("const key=r=>JSON.stringify(r.c);"));
assert(peer576Text.includes("source.map(key).sort()"));
const peer576Run = cp.spawnSync(process.execPath, [abs("peer576")],
  {encoding:"utf8", timeout:30000, maxBuffer:4<<20});
assert.notEqual(peer576Run.status, 0);
assert(peer576Run.stderr.includes("native source multiset changed"));
assert(peer576Run.stderr.includes("undefined"));

const peer547Run = cp.spawnSync(process.execPath, [abs("peer547")],
  {encoding:"utf8", timeout:30000, maxBuffer:16<<20});
assert.equal(peer547Run.status, 0, peer547Run.stderr);
const slot = JSON.parse(peer547Run.stdout);

// LSPV-2/561: the peer CLI runner does execute all eleven checker cases but
// then aborts while asking depth() to accept the deliberately forward-parent
// negative case. Independently replay the checker outcomes without that
// post-rejection metric.
const peer561Run = cp.spawnSync(process.execPath, [abs("peer561")],
  {encoding:"utf8", timeout:30000, maxBuffer:16<<20});
assert.notEqual(peer561Run.status, 0);
assert(peer561Run.stderr.includes("assert.ok(j<i)"));
const mod561 = require(abs("peer561"));
const cases561 = mod561.buildCases(read("seed560")).rows;
const temp561 = fs.mkdtempSync(path.join(os.tmpdir(), "lspv5-492-561-"));
const replay561 = [];
try {
  for (const [name,p,expect] of cases561) {
    const f = path.join(temp561, name + ".json");
    fs.writeFileSync(f, JSON.stringify(p) + "\n");
    const q = cp.spawnSync(process.execPath, [abs("checker386"), f],
      {encoding:"utf8", timeout:30000, maxBuffer:4<<20});
    const accepted = q.status === 0;
    assert.equal(accepted, expect, name);
    replay561.push({name, expected:expect, accepted});
  }
} finally { fs.rmSync(temp561, {recursive:true, force:true}); }
assert.equal(replay561.filter(x=>x.accepted).length, 3);
assert.equal(replay561.filter(x=>!x.accepted).length, 8);

// LSPV-3/574: the connector's line-oriented materialization adds a final LF
// to the remotely no-final-LF seed. Reconstruct the exact pinned 4,421 bytes
// in an isolated temporary repository, then execute the peer OS runner there.
const temp574 = fs.mkdtempSync(path.join(os.tmpdir(), "lspv5-492-574-"));
let replay574;
try {
  for (const d of ["experiments/arc", "results/raw/arc"])
    fs.mkdirSync(path.join(temp574,d), {recursive:true});
  fs.writeFileSync(path.join(temp574, rel.peer574), bytes("peer574"));
  fs.writeFileSync(path.join(temp574, rel.checker386), bytes("checker386"));
  const exactSeed563 = Buffer.from(bytes("seed563").toString("utf8").replace(/\n$/, ""));
  assert.equal(gitBlob(exactSeed563), "08aa169b5db49b2ddd1cb5a9b6890fcc3b790916");
  fs.writeFileSync(path.join(temp574, rel.seed563), exactSeed563);
  const q = cp.spawnSync(process.execPath, [path.join(temp574, rel.peer574)],
    {cwd:temp574, encoding:"utf8", timeout:30000, maxBuffer:16<<20});
  assert.equal(q.status, 0, q.stderr);
  replay574 = JSON.parse(q.stdout);
} finally { fs.rmSync(temp574, {recursive:true, force:true}); }
assert.equal(slot.nodeCount, 62);
assert.equal(slot.area546.freshPeak, 7);
assert.equal(slot.area546.afterOnlyPeak, 6);
assert.equal(slot.completeNo6.reached, false);
assert.equal(slot.completeNo6.visited, 770940);
assert.equal(slot.completeNo6.legalTransitionTraversals, 1911021);
assert.equal(slot.independentNo6.visited, 185340);

// Separate the resource statements explicitly. The source theorem lower-bounds
// paid RES nodes over this restricted calculus. The slot theorem minimizes peak
// live paid results only for one fixed DAG and one fresh-before-release model.
assert(36 <= 62);
assert(7 <= 62);
const result = {
  id: "LSPV-5/492",
  status: "PROVED/RESTRICTED plus COMPUTATIONAL",
  peer_blobs: pins,
  independent_source_audit: {
    assignments_tested: 1<<15,
    core_models: coreModels,
    indispensable_vertex_clauses: essential.length,
    dispensable_vertex_ordinals: dispensable,
    unique_minimum_unsat_source_size_including_guard: 37,
    restricted_binary_RES_lower_bound: 36,
    native_packet_dead_SOURCE_indices: dead.map(r => r.index),
    checker: {
      status: "ACCEPT", paid:checkerOut.paid, res:checkerOut.res,
      sources:checkerOut.sources, assertions:checkerOut.assertions,
      negativeTests:checkerOut.negativeTests
    }
  },
  peer576_reproducer_failure: {
    exit_status: peer576Run.status,
    exact_cause: "source.map(key) passes clause arrays to key(r)=JSON.stringify(r.c), yielding undefined",
    assertion: "native source multiset changed",
    theorem_effect: "No theorem-level falsification: independent reconstruction and published raw values agree"
  },
  independent_lspv2_561_replay: {
    checker_cases: replay561.length,
    accepted: replay561.filter(x=>x.accepted).length,
    rejected: replay561.filter(x=>!x.accepted).length,
    peer_runner_exit_status: peer561Run.status,
    peer_runner_failure: "depth() is applied after a deliberately rejected future-parent case and asserts j<i",
    theorem_effect: "No transformer-level falsification: all 3 expected accepts and 8 expected rejects independently match"
  },
  independent_lspv3_574_OS_replay: {
    accepted: replay574.positiveOriginalCheckerExecutions,
    rejected: replay574.negativeOriginalCheckerExecutions,
    accepted_cycle_masks: replay574.acceptedNativeMasks,
    kernel_composition_checks: replay574.kernelCompositionChecks,
    paid_work: replay574.work.total
  },
  independent_slot_replay: {
    fixed_DAG_nodes: slot.nodeCount,
    accepted_fresh_peak: slot.area546.freshPeak,
    after_release_peak: slot.area546.afterOnlyPeak,
    cap6_reached: slot.completeNo6.reached,
    cap6_BFS_states: slot.completeNo6.visited,
    cap6_ready_transitions: slot.completeNo6.legalTransitionTraversals,
    cap6_DFS_states: slot.independentNo6.visited
  },
  polarity: {
    source_work: "36 <= restricted fixed-source /386 binary-RES work <= 62",
    full_CLI_work: "37 <= restricted full-CLI paid work <= 63",
    fixed_DAG_live_slots: "exactly 7 only under fresh-before-release/no-recompute scheduling",
    forbidden_transfers: [
      "fixed-DAG live slots to alternative-proof or full-R_mix341 memory",
      "proof-node count to physical RAM bytes",
      "finite fixed-instance work to asymptotic SAT-machine lower bounds",
      "archived /386 sibling grammar to missing mixed-rule dispatcher"
    ]
  }
};
const output = JSON.stringify(result, null, 2) + "\n";
if (process.argv.includes("--write-raw")) {
  fs.mkdirSync(path.dirname(abs("out")), {recursive:true});
  fs.writeFileSync(abs("out"), output);
}
process.stdout.write(output);
