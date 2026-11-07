#!/usr/bin/env node
// Independent raw-token replay for LSPV-5/418.
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
const sentinel = "__LSPV5_418_NODE__";

function valueToken(pathParts, rawToken) {
  const obj = structuredClone(base); let cur = obj.fixtures[0];
  for (const step of pathParts.slice(0, -1)) cur = cur[step];
  cur[pathParts.at(-1)] = sentinel;
  const raw = compact(obj), old = compact(sentinel);
  assert.equal(raw.split(old).length - 1, 1);
  return raw.replace(old, rawToken);
}

function keyToken(pathParts, key, rawToken) {
  const obj = structuredClone(base); let cur = obj.fixtures[0];
  for (const step of pathParts) cur = cur[step];
  const value = cur[key]; delete cur[key]; cur[sentinel] = value;
  const raw = compact(obj), old = compact(sentinel);
  assert.equal(raw.split(old).length - 1, 1);
  return raw.replace(old, rawToken);
}

function canonicalStrings(raw) {
  JSON.parse(raw);
  const tokens = raw.match(/"(?:\\["\\/bfnrt]|\\u[0-9a-fA-F]{4}|[^"\\\u0000-\u001f])*"/g) ?? [];
  let bad = 0;
  for (const token of tokens) if (JSON.stringify(JSON.parse(token)) !== token) bad++;
  if (bad) throw Error(`noncanonical strings: ${bad}`);
  return true;
}

function check(raw) {
  const tmp = path.join(os.tmpdir(), `lspv5-418-${process.pid}-${crypto.randomUUID()}.json`);
  fs.writeFileSync(tmp, raw);
  try {
    const cp = spawnSync(process.execPath, [checker, tmp], { encoding: "utf8" });
    return { accepted: cp.status === 0, stdoutHash: hash(cp.stdout), stderr: cp.stderr.split("\n")[0] };
  } finally { fs.unlinkSync(tmp); }
}

const specs = [
  ["source definition same", "value", ["clauses",0,"id"], '"\\u0073\\u0030"', true],
  ["source reference same", "value", ["proof",0,"parents",0], '"\\u0073\\u0030"', true],
  ["derived definition same", "value", ["proof",0,"id"], '"\\u0064\\u0030"', true],
  ["derived reference same", "value", ["proof",1,"parents",0], '"\\u0064\\u0030"', true],
  ["source definition different", "value", ["clauses",0,"id"], '"\\u0078\\u0030"', false],
  ["source reference different", "value", ["proof",0,"parents",0], '"\\u0078\\u0030"', false],
  ["derived definition different", "value", ["proof",0,"id"], '"\\u0078\\u0030"', false],
  ["derived reference different", "value", ["proof",1,"parents",0], '"\\u0078\\u0030"', false],
  ["id key same", "key-id", ["clauses",0], '"\\u0069\\u0064"', true],
  ["id key different", "key-id", ["clauses",0], '"\\u006a\\u0064"', false],
  ["parents key same", "key-parents", ["proof",0], '"\\u0070\\u0061\\u0072\\u0065\\u006e\\u0074\\u0073"', true],
  ["parents key different", "key-parents", ["proof",0], '"\\u0071\\u0061\\u0072\\u0065\\u006e\\u0074\\u0073"', false],
  ["malformed escape", "value", ["clauses",0,"id"], '"\\uZZZZ"', false],
];

const baselineRaw = compact(base), baseline = check(baselineRaw);
assert.equal(baseline.accepted, true); assert.equal(canonicalStrings(baselineRaw), true);
let checks = 2, accepted = 0, rejected = 0;
for (const [name, mode, p, token, expected] of specs) {
  const raw = mode === "value" ? valueToken(p, token) : keyToken(p, mode === "key-id" ? "id" : "parents", token);
  assert.throws(() => canonicalStrings(raw)); checks++;
  const result = check(raw);
  assert.equal(result.accepted, expected, name); checks++;
  if (expected) { assert.equal(result.stdoutHash, baseline.stdoutHash, name); checks++; accepted++; }
  else rejected++;
}
console.log(JSON.stringify({status:"PASS",checks,cases:specs.length,accepted,rejected,baselineStdoutSha256:baseline.stdoutHash}));
