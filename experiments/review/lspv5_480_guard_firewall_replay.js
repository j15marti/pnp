"use strict";

const fs = require("fs");
const crypto = require("crypto");
const cp = require("child_process");

const checkerPath = process.argv[2] || "lspv5_477_historical_verifier.js";
const baselinePath = process.argv[3] || "lspv5_477_baseline.json";
const negativeZeroPath = process.argv[4] || "lspv5_479_negative_zero_alias_accepted.json";
const satPacketPath = process.argv[5] || "lspv3_557_packet.json";
const externalSourcePath = process.argv[6] || "peer_lspv2_542_raw.json";
const outPath = process.argv[7] || "lspv5_480_guard_firewall_raw.json";
const started = process.hrtime.bigint();

function sha256(s) {
  return crypto.createHash("sha256").update(s).digest("hex");
}

function runChecker(raw, tag) {
  const temp = `.lspv5_480_${tag}.json`;
  fs.writeFileSync(temp, raw);
  const start = process.hrtime.bigint();
  const p = cp.spawnSync(process.execPath, [checkerPath, temp], {
    encoding: "utf8",
    timeout: 30000,
    maxBuffer: 16 * 1024 * 1024
  });
  fs.unlinkSync(temp);
  return {
    accepted: p.status === 0,
    status: p.status,
    wallMilliseconds: Number(process.hrtime.bigint() - start) / 1e6,
    stdout: p.stdout,
    stderr: p.stderr,
    checks: p.status === 0 ? JSON.parse(p.stdout).checks : null
  };
}

function guard(f, external) {
  const E = f.graph.edges.length;
  if (!Array.isArray(f.charges) ||
      !f.charges.every(x => typeof x === "number" && (x === 0 || x === 1))) {
    return "CHARGE_NOT_BINARY_NUMBER";
  }
  if (!Array.isArray(external) || external.length !== f.clauses.length) {
    return "SOURCE_NOT_BOUND";
  }
  for (let i = 0; i < external.length; i++) {
    const a = f.clauses[i].literals;
    const b = external[i];
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length ||
        !a.every((x, j) => typeof x === "number" && Number.isSafeInteger(x) &&
                           x !== 0 && x === b[j])) {
      return "SOURCE_NOT_BOUND_OR_TYPED";
    }
  }
  for (const p of f.proof) {
    if (p.rule !== "AND3") continue;
    if (!Array.isArray(p.support)) return "AND3_SUPPORT_NOT_ARRAY";
    if (p.row) {
      let m;
      try { m = BigInt(p.row.mask); }
      catch (_) { return "AFFINE_MASK_INVALID"; }
      if (m < 0n || (m >> BigInt(E)) !== 0n) return "AFFINE_MASK_OUT_OF_RANGE";
    }
  }
  return "SOURCE_BOUND_SEMANTICALLY_SOUND_FRAGMENT";
}

function parseDimacs(text) {
  const lines = text.split(/\r?\n/).map(x => x.trim()).filter(x => x && !x.startsWith("c"));
  const header = lines.shift().split(/\s+/);
  if (header[0] !== "p" || header[1] !== "cnf") throw new Error("bad DIMACS header");
  const clauses = lines.map(line => {
    const row = line.split(/\s+/).map(Number);
    if (row.pop() !== 0 || row.length !== 3) throw new Error("bad strict clause");
    return row;
  });
  if (clauses.length !== Number(header[3])) throw new Error("DIMACS clause count");
  return clauses;
}

function modelCount(f) {
  const E = f.graph.edges.length;
  if (E > 20) throw new Error("finite control too large");
  let count = 0;
  let first = null;
  for (let a = 0; a < (1 << E); a++) {
    const sat = f.clauses.every(c => c.literals.some(l => {
      const bit = (a >> (Math.abs(l) - 1)) & 1;
      return bit === (l > 0 ? 1 : 0);
    }));
    if (sat) {
      count++;
      if (first === null) first = a;
    }
  }
  return {count, first};
}

const baselineRaw = fs.readFileSync(baselinePath, "utf8");
const negativeZeroRaw = fs.readFileSync(negativeZeroPath, "utf8");
const satRaw = fs.readFileSync(satPacketPath, "utf8");
const externalRaw = JSON.parse(fs.readFileSync(externalSourcePath, "utf8"));
const externalK4 = parseDimacs(externalRaw.rawK4CanonicalSource);
const baseline = JSON.parse(baselineRaw);
const negativeZero = JSON.parse(negativeZeroRaw);
const satPacket = JSON.parse(satRaw);

const baselineRun = runChecker(baselineRaw, "baseline");
const zeroRun = runChecker(negativeZeroRaw, "negative_zero");
const satRun = runChecker(satRaw, "single_sat");
if (!baselineRun.accepted || baselineRun.checks !== 30714) throw new Error("baseline replay failed");
if (!zeroRun.accepted || zeroRun.checks !== 30714) throw new Error("negative-zero replay failed");
if (!satRun.accepted || satRun.checks !== 3273) throw new Error("single SAT replay failed");

const baselineFixture = baseline.fixtures[0];
const zeroFixture = negativeZero.fixtures[0];
const satFixture = satPacket.fixtures[0];
const baselineGuard = guard(baselineFixture, externalK4);
const zeroGuard = guard(zeroFixture, externalK4);
const satExternal = satFixture.clauses.map(c => c.literals.slice());
const satGuard = guard(satFixture, satExternal);
if (baselineGuard !== "SOURCE_BOUND_SEMANTICALLY_SOUND_FRAGMENT") throw new Error(baselineGuard);
if (zeroGuard !== "SOURCE_BOUND_SEMANTICALLY_SOUND_FRAGMENT") throw new Error(zeroGuard);
if (satGuard !== "CHARGE_NOT_BINARY_NUMBER") throw new Error(`unexpected SAT guard ${satGuard}`);

const baselineModels = modelCount(baselineFixture);
const zeroModels = modelCount(zeroFixture);
const satModels = modelCount(satFixture);
if (baselineModels.count !== 0 || zeroModels.count !== 0 || satModels.count < 1) {
  throw new Error("independent model count mismatch");
}

const parsedDef = zeroFixture.proof[0].id;
const parsedRef = zeroFixture.proof[1].parents[0];
if (!Object.is(parsedDef, -0) || !Object.is(parsedRef, 0) || Object.is(parsedDef, parsedRef)) {
  throw new Error("raw signed-zero setup lost");
}
const parsedMap = new Map([[parsedDef, "node"]]);
if (parsedMap.get(parsedRef) !== "node") throw new Error("Map did not merge signed zero");

const normalizedSAT = JSON.parse(satRaw);
normalizedSAT.fixtures[0].charges = normalizedSAT.fixtures[0].charges.map(Number);
const supportRepairs = [];
for (let i = 0; i < normalizedSAT.fixtures[0].proof.length; i++) {
  const p = normalizedSAT.fixtures[0].proof[i];
  if (p.rule === "AND3" && !Array.isArray(p.support)) {
    supportRepairs.push(i);
    p.support = [...p.support].map(Number);
  }
}
const normalizedSATRaw = JSON.stringify(normalizedSAT);
const normalizedRun = runChecker(normalizedSATRaw, "typed_sat_repair");
if (normalizedRun.accepted) throw new Error("typed SAT repair unexpectedly accepted");

const result = {
  run: "LSPV-5/480",
  datePacific: "2026-11-10 17:48 PST",
  status: "PROVED_RESTRICTED_VALIDATION_PLUS_COMPUTATIONAL_REPLAY",
  checker: {path: checkerPath, sha256: sha256(fs.readFileSync(checkerPath))},
  cases: {
    authenticK4: {
      accepted: baselineRun.accepted,
      checks: baselineRun.checks,
      guard: baselineGuard,
      externalSourceSHA256: sha256(externalRaw.rawK4CanonicalSource),
      models: baselineModels.count
    },
    negativeZeroAlias: {
      accepted: zeroRun.accepted,
      checks: zeroRun.checks,
      guard: zeroGuard,
      models: zeroModels.count,
      rawDefinitionToken: "-0",
      rawParentToken: "0",
      objectIsDistinct: !Object.is(parsedDef, parsedRef),
      mapIdentityMerged: parsedMap.has(parsedRef),
      semanticEffect: "none in this packet; it remains an UNSAT K4 refutation",
      provenanceEffect: "G1-G4 do not authenticate an injective raw-token identifier encoding"
    },
    singleFixtureSATForgery557: {
      accepted: satRun.accepted,
      checks: satRun.checks,
      guard: satGuard,
      models: satModels.count,
      firstModelInteger: satModels.first,
      typedChargeAndSupportRepairAccepted: normalizedRun.accepted,
      repairedSupportRecordIndices: supportRepairs
    }
  },
  theoremAssessment: {
    semanticFirewall559SurvivesTheseFalsifiers: true,
    rawByteIdentityAuthenticationEstablished: false,
    completeConcreteStepCoverageEstablished: false,
    lowerBoundMAYAbstractionEstablished: false,
    reason: "The SAT forgery is rejected by G2 and the typed repair is rejected by the concrete checker. The signed-zero packet passes G1-G4 but is genuinely UNSAT; it falsifies only any stronger claim of raw-token identifier injectivity or complete accepted-language coverage."
  },
  resources: {
    baselineWallMilliseconds: baselineRun.wallMilliseconds,
    negativeZeroWallMilliseconds: zeroRun.wallMilliseconds,
    satForgeryWallMilliseconds: satRun.wallMilliseconds,
    typedRepairWallMilliseconds: normalizedRun.wallMilliseconds,
    totalWallMillisecondsBeforeWrite: Number(process.hrtime.bigint() - started) / 1e6,
    orchestratorMaxRSSKiB: process.resourceUsage().maxRSS,
    note: "Child verifier wall time is measured; child RSS/CPU, retrieval, publication, and physical indexed-machine peak work space are not measured."
  },
  trackerDecision: "TRACKERS REVIEWED; NO MATERIAL CHANGE",
  open: ["P2-D1", "P2-C3", "P2-B1", "P2-B2/B3", "P versus NP"]
};

fs.writeFileSync(outPath, JSON.stringify(result, null, 2) + "\n");
console.log(JSON.stringify(result, null, 2));
