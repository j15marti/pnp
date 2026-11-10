"use strict";
const fs = require("fs");
const crypto = require("crypto");
const cp = require("child_process");

const baselinePath = process.argv[2] || "lspv5_477_baseline.json";
const verifierPath = process.argv[3] || "lspv5_477_historical_verifier.js";
const outPath = process.argv[4] || "lspv5_477_unsafe_integer_id_alias_raw.json";
const base = JSON.parse(fs.readFileSync(baselinePath, "utf8"));

function sha256(s) {
  return crypto.createHash("sha256").update(s).digest("hex");
}

function materialize(defToken, refToken, outFile) {
  const d = JSON.parse(JSON.stringify(base));
  const proof = d.fixtures[0].proof;
  const target = proof[0].id;
  proof[0].id = "__DEF_TOKEN__";
  let refs = 0;
  for (const rec of proof) {
    if (!Array.isArray(rec.parents)) continue;
    rec.parents = rec.parents.map(p => {
      if (p === target) {
        refs++;
        return "__REF_TOKEN__";
      }
      return p;
    });
  }
  if (refs < 1) throw new Error("chosen ID has no later reference");
  let raw = JSON.stringify(d, null, 2);
  raw = raw.replace('"__DEF_TOKEN__"', defToken);
  raw = raw.replaceAll('"__REF_TOKEN__"', refToken);
  fs.writeFileSync(outFile, raw + "\n");
  return {target, refs, raw, outFile};
}

function run(file) {
  const p = cp.spawnSync(process.execPath, [verifierPath, file], {
    encoding: "utf8",
    timeout: 30000,
    maxBuffer: 16 * 1024 * 1024
  });
  return {
    accepted: p.status === 0,
    status: p.status,
    signal: p.signal,
    stdout: p.stdout,
    stderr: p.stderr
  };
}

const baselineRun = run(baselinePath);
if (!baselineRun.accepted) throw new Error("baseline verifier replay failed");

const alias = materialize(
  "9007199254740993",
  "9007199254740992",
  "lspv5_477_alias_accepted.json"
);
const safeMismatch = materialize(
  "9007199254740991",
  "9007199254740990",
  "lspv5_477_safe_mismatch_rejected.json"
);
const stringMismatch = materialize(
  '"9007199254740993"',
  '"9007199254740992"',
  "lspv5_477_string_mismatch_rejected.json"
);

const aliasRun = run(alias.outFile);
const safeRun = run(safeMismatch.outFile);
const stringRun = run(stringMismatch.outFile);

if (!aliasRun.accepted) throw new Error("unsafe-integer alias was not accepted");
if (safeRun.accepted) throw new Error("safe-integer mismatch was unexpectedly accepted");
if (stringRun.accepted) throw new Error("string mismatch was unexpectedly accepted");

const parsedAlias = JSON.parse(alias.raw);
const baselineSummary = JSON.parse(baselineRun.stdout);
const aliasSummary = JSON.parse(aliasRun.stdout);
const parsedDef = parsedAlias.fixtures[0].proof[0].id;
const parsedParent = parsedAlias.fixtures[0].proof
  .flatMap(x => x.parents || [])
  .find(x => x === parsedDef);

const result = {
  run: "LSPV-5/477",
  status: "COMPUTATIONAL ACCEPTED-BYTE COUNTEREXAMPLE",
  verifier: {
    path: verifierPath,
    sha256: sha256(fs.readFileSync(verifierPath)),
    baseline_path: baselinePath,
    baseline_sha256: sha256(fs.readFileSync(baselinePath)),
    baseline_accepted: baselineRun.accepted,
    baseline_checks: baselineSummary.checks,
    fixture_count: baselineSummary.cases.length
  },
  attack: {
    original_target_id: alias.target,
    reference_count: alias.refs,
    definition_raw_token: "9007199254740993",
    parent_raw_token: "9007199254740992",
    definition_and_parent_bytes_differ: true,
    parsed_definition_value: parsedDef,
    parsed_parent_value: parsedParent,
    parsed_values_equal: parsedDef === parsedParent,
    accepted: aliasRun.accepted,
    accepted_checks: aliasSummary.checks,
    mutant_sha256: sha256(alias.raw + "\n")
  },
  controls: {
    safe_integer_mismatch_rejected: !safeRun.accepted,
    string_mismatch_rejected: !stringRun.accepted,
    baseline_stdout_sha256: sha256(baselineRun.stdout),
    alias_stdout_sha256: sha256(aliasRun.stdout),
    stdout_identical: baselineRun.stdout === aliasRun.stdout
  },
  conclusion: "The verifier authenticates parsed JavaScript Number identity, not raw identifier bytes. Distinct raw decimal tokens above 2^53 alias and an antecedent reference with different bytes is accepted.",
  scope: "This falsifies byte-level ID/provenance authentication for the pinned LSPV-2/341 verifier only. It is not a soundness failure of an independently specified canonical-string calculus, not a native full R_mix341 theorem, and not a P-versus-NP result."
};
fs.writeFileSync(outPath, JSON.stringify(result, null, 2) + "\n");
console.log(JSON.stringify(result, null, 2));
