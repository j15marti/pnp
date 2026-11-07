#!/usr/bin/env node
// Independent raw-byte replay for LSPV-5/417.
import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../..");
const packetPath = path.join(root, "replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json");
const checker = path.join(root, "replay/413/lspv2_341_independent_verify.js");
const base = JSON.parse(fs.readFileSync(packetPath, "utf8"));
const compact = x => JSON.stringify(x);
const hash = s => crypto.createHash("sha256").update(s).digest("hex");

function duplicate(pathParts, first, second) {
  const obj = structuredClone(base);
  let cur = obj.fixtures[0];
  for (const step of pathParts.slice(0, -1)) cur = cur[step];
  const key = pathParts.at(-1), sentinel = "__LSPV5_417_NODE__";
  cur[key] = sentinel;
  const raw = compact(obj), old = `${compact(key)}:${compact(sentinel)}`;
  assert.equal(raw.split(old).length - 1, 1);
  return raw.replace(old, `${compact(key)}:${compact(first)},${compact(key)}:${compact(second)}`);
}

function strictUnique(raw) {
  let i = 0;
  const ws = () => { while (/\s/.test(raw[i] ?? "")) i++; };
  const str = () => {
    const start = i++;
    while (i < raw.length) {
      if (raw[i] === "\\") { i += 2; continue; }
      if (raw[i++] === '"') return JSON.parse(raw.slice(start, i));
    }
    throw Error("unterminated string");
  };
  const value = () => {
    ws();
    if (raw[i] === '"') { str(); return; }
    if (raw[i] === "{") {
      i++; ws(); const seen = new Set();
      if (raw[i] === "}") { i++; return; }
      for (;;) {
        ws(); const key = str();
        if (seen.has(key)) throw Error(`duplicate member: ${key}`);
        seen.add(key); ws(); assert.equal(raw[i++], ":"); value(); ws();
        if (raw[i] === "}") { i++; return; }
        assert.equal(raw[i++], ",");
      }
    }
    if (raw[i] === "[") {
      i++; ws(); if (raw[i] === "]") { i++; return; }
      for (;;) { value(); ws(); if (raw[i] === "]") { i++; return; } assert.equal(raw[i++], ","); }
    }
    const m = raw.slice(i).match(/^(?:-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null)/);
    if (!m) throw Error(`bad scalar at ${i}`);
    i += m[0].length;
  };
  value(); ws(); if (i !== raw.length) throw Error("trailing bytes");
  return true;
}

function check(raw) {
  const tmp = path.join(os.tmpdir(), `lspv5-417-${process.pid}-${crypto.randomUUID()}.json`);
  fs.writeFileSync(tmp, raw);
  try {
    const cp = spawnSync(process.execPath, [checker, tmp], { encoding: "utf8" });
    return { accepted: cp.status === 0, stdoutHash: hash(cp.stdout), stderr: cp.stderr.split("\n")[0] };
  } finally { fs.unlinkSync(tmp); }
}

const f = base.fixtures[0];
const ai = f.proof.findIndex(p => p.kind === "affine");
const cases = [
  ["source id", ["clauses",0,"id"], "forged-source", f.clauses[0].id],
  ["derived id", ["proof",0,"id"], "forged-derived", f.proof[0].id],
  ["parents", ["proof",0,"parents"], ["forged-a","forged-b"], f.proof[0].parents],
  ["source literals", ["clauses",0,"literals"], [999], f.clauses[0].literals],
  ["kind", ["proof",0,"kind"], "affine", f.proof[0].kind],
  ["affine mask", ["proof",ai,"row","mask"], "not-a-bigint", f.proof[ai].row.mask],
];

const baseline = check(compact(base));
assert.equal(baseline.accepted, true);
let checks = 1;
for (const [name, p, forged, canonical] of cases) {
  const acceptedRaw = duplicate(p, forged, canonical);
  const rejectedRaw = duplicate(p, canonical, forged);
  assert.throws(() => strictUnique(acceptedRaw), /duplicate member/); checks++;
  assert.throws(() => strictUnique(rejectedRaw), /duplicate member/); checks++;
  const a = check(acceptedRaw), b = check(rejectedRaw);
  assert.equal(a.accepted, true, name); checks++;
  assert.equal(a.stdoutHash, baseline.stdoutHash, name); checks++;
  assert.equal(b.accepted, false, name); checks++;
}
console.log(JSON.stringify({status:"PASS",checks,cases:cases.length*2,accepted:cases.length,rejected:cases.length,baselineStdoutSha256:baseline.stdoutHash}));
