"use strict";

const fs = require("fs");
const crypto = require("crypto");
const cp = require("child_process");
const ref539 = require("./peer_lspv2_539_reference.cjs");
const transport542 = require("./peer_lspv2_542.cjs");

const baselinePath = process.argv[2] || "lspv5_477_baseline.json";
const verifierPath = process.argv[3] || "lspv5_477_historical_verifier.js";
const peerRawPath = process.argv[4] || "peer_lspv2_542_raw.json";
const outPath = process.argv[5] || "lspv5_479_negative_zero_id_alias_raw.json";
const acceptedPath = process.argv[6] || "lspv5_479_negative_zero_alias_accepted.json";
const auditStart = process.hrtime.bigint();
const auditStartUsage = process.resourceUsage();

function sha256(s) {
  return crypto.createHash("sha256").update(s).digest("hex");
}

function runVerifier(raw, tag) {
  const path = `.lspv5_479_${tag}.json`;
  fs.writeFileSync(path, raw);
  const start = process.hrtime.bigint();
  const p = cp.spawnSync(process.execPath, [verifierPath, path], {
    encoding: "utf8",
    timeout: 30000,
    maxBuffer: 16 * 1024 * 1024
  });
  fs.unlinkSync(path);
  return {
    accepted: p.status === 0,
    status: p.status,
    signal: p.signal,
    stdout: p.stdout,
    stderr: p.stderr,
    wallMilliseconds: Number(process.hrtime.bigint() - start) / 1e6
  };
}

function mutantRaw(definitionToken, referenceToken, oneFixture) {
  const base = JSON.parse(fs.readFileSync(baselinePath, "utf8"));
  if (oneFixture) {
    base.fixtures = [base.fixtures[0]];
    base.summary = [base.summary[0]];
  }
  const proof = base.fixtures[0].proof;
  if (proof[0].id !== "d0") throw new Error("unexpected target paid ID");
  proof[0].id = "__DEF_TOKEN__";
  let references = 0;
  for (const node of proof) {
    if (!Array.isArray(node.parents)) continue;
    node.parents = node.parents.map(parent => {
      if (parent === "d0") {
        references++;
        return "__REF_TOKEN__";
      }
      return parent;
    });
  }
  if (references !== 1) throw new Error(`expected one d0 reference, got ${references}`);
  let raw = JSON.stringify(base, null, 2) + "\n";
  raw = raw.replace('"__DEF_TOKEN__"', definitionToken);
  raw = raw.replace('"__REF_TOKEN__"', referenceToken);
  return {raw, references};
}

const baselineRaw = fs.readFileSync(baselinePath, "utf8");
const baselineRun = runVerifier(baselineRaw, "baseline");
if (!baselineRun.accepted) throw new Error("baseline rejected");

const hostile = mutantRaw("-0", "0", false);
const hostileRun = runVerifier(hostile.raw, "negative_zero");
if (!hostileRun.accepted) throw new Error("negative-zero alias was not accepted");
fs.writeFileSync(acceptedPath, hostile.raw);

const stringMismatch = mutantRaw('"-0"', '"0"', false);
const stringMismatchRun = runVerifier(stringMismatch.raw, "string_mismatch");
if (stringMismatchRun.accepted) throw new Error("distinct strings unexpectedly accepted");

const unboundNumeric = mutantRaw("-0", "1", false);
const unboundNumericRun = runVerifier(unboundNumeric.raw, "unbound_numeric");
if (unboundNumericRun.accepted) throw new Error("unbound numeric reference unexpectedly accepted");

const single = mutantRaw("-0", "0", true);
const peerRaw = JSON.parse(fs.readFileSync(peerRawPath, "utf8"));
const refResult = ref539.tryAudit(peerRaw.rawK4CanonicalSource, single.raw);
const transportResult = transport542.transport(peerRaw.rawK4CanonicalSource, single.raw);
if (refResult.accepted) throw new Error("strict typed reference accepted numeric paid ID");
if (transportResult.status !== "REFERENCE_REJECT") {
  throw new Error(`source-occurrence transporter returned ${transportResult.status}`);
}

const parsed = JSON.parse(hostile.raw);
const parsedDefinition = parsed.fixtures[0].proof[0].id;
const parsedReference = parsed.fixtures[0].proof[1].parents[0];
if (!Object.is(parsedDefinition, -0)) throw new Error("definition token did not parse as -0");
if (!Object.is(parsedReference, 0)) throw new Error("reference token did not parse as +0");
if (Object.is(parsedDefinition, parsedReference)) throw new Error("Object.is should distinguish signed zero");
if (parsedDefinition !== parsedReference) throw new Error("strict equality should merge signed zero");

const map = new Map([[parsedDefinition, "paid-node"]]);
if (map.get(parsedReference) !== "paid-node") throw new Error("Map SameValueZero alias failed");

const baselineSummary = JSON.parse(baselineRun.stdout);
const hostileSummary = JSON.parse(hostileRun.stdout);
const result = {
  run: "LSPV-5/479",
  datePacific: "2026-11-10 17:20 PST",
  status: "COMPUTATIONAL ACCEPTED-BYTE COUNTEREXAMPLE + PROVED ECMASCRIPT SEMANTIC FACT",
  target: "LSPV-2/542 occurrence transport is sufficient for all original-checker-accepted byte representations",
  verifier: {
    path: verifierPath,
    sha256: sha256(fs.readFileSync(verifierPath)),
    baselinePath,
    baselineSha256: sha256(baselineRaw),
    baselineAccepted: true,
    baselineChecks: baselineSummary.checks
  },
  attack: {
    definitionRawToken: "-0",
    parentRawToken: "0",
    rawTokensDiffer: true,
    parsedDefinitionObjectIsNegativeZero: Object.is(parsedDefinition, -0),
    parsedParentObjectIsPositiveZero: Object.is(parsedReference, 0),
    objectIsDistinguishes: !Object.is(parsedDefinition, parsedReference),
    strictEqualityMerges: parsedDefinition === parsedReference,
    mapSameValueZeroMerges: map.has(parsedReference),
    originalCheckerAccepted: hostileRun.accepted,
    acceptedChecks: hostileSummary.checks,
    originalCheckerStdoutIdenticalToBaseline: hostileRun.stdout === baselineRun.stdout,
    acceptedPacketBytes: Buffer.byteLength(hostile.raw),
    acceptedPacketSHA256: sha256(hostile.raw)
  },
  independentControls: {
    distinctStringTokensRejectedByOriginalChecker: !stringMismatchRun.accepted,
    unboundNumericParentRejectedByOriginalChecker: !unboundNumericRun.accepted,
    strictTypedReferenceAccepted: refResult.accepted,
    strictTypedReferenceDiagnostic: refResult.diagnostic,
    sourceOccurrenceTransportStatus: transportResult.status,
    sourceOccurrenceTransportReason: transportResult.reason
  },
  resourceLedger: {
    parserAndBaselineVerifierWallMilliseconds: baselineRun.wallMilliseconds,
    hostileVerifierWallMilliseconds: hostileRun.wallMilliseconds,
    stringControlVerifierWallMilliseconds: stringMismatchRun.wallMilliseconds,
    unboundControlVerifierWallMilliseconds: unboundNumericRun.wallMilliseconds,
    totalOrchestratorWallMillisecondsBeforeFinalWrite: Number(process.hrtime.bigint() - auditStart) / 1e6,
    orchestratorMaxRSSKiB: process.resourceUsage().maxRSS,
    orchestratorUserCPUSeconds: (process.resourceUsage().userCPUTime - auditStartUsage.userCPUTime) / 1e6,
    orchestratorSystemCPUSeconds: (process.resourceUsage().systemCPUTime - auditStartUsage.systemCPUTime) / 1e6,
    physicalScope: "Node process.resourceUsage covers the audit orchestrator; child verifier wall time is measured per invocation, but child RSS/CPU and GitHub retrieval/publication are not included. Logical paid work remains 15 for the attacked K4 fixture and 622 across the unchanged seven-fixture corpus."
  },
  provedInterpretation: "ECMAScript JSON.parse preserves -0 as a Number distinguishable from +0 by Object.is, while strict equality and Map key matching use zero-merging semantics; JSON.stringify(-0) emits 0.",
  concreteConclusion: "The pinned recovered /341 fixture checker accepts different raw paid-node definition/reference tokens -0 and 0 as one Map identity. The strict 539 typed reference and 542 occurrence transporter reject the same packet, so 542 is a sound repair for its declared typed fragment but is not complete for the recovered checker accepted-byte language.",
  scope: "This refines the known unsafe/native identifier-alias obstruction. It is not semantic refutation unsoundness, not authentication of full historical R_mix341, not a minimum-proof lower bound, and not a P-versus-NP result."
};

fs.writeFileSync(outPath, JSON.stringify(result, null, 2) + "\n");
console.log(JSON.stringify(result, null, 2));
