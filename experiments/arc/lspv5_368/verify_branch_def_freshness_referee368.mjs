#!/usr/bin/env node
// Independent REFEREE368 replay.  No Python checker code is imported.

import fs from "node:fs";
import crypto from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../..");
let assertions = 0;
function ok(x, msg) { assertions++; if (!x) throw new Error(msg); }
function canon(xs) {
  const a = xs.map(Number);
  ok(!a.includes(0), "zero literal");
  ok(new Set(a).size === a.length, "duplicate literal");
  for (const x of a) ok(!a.includes(-x), "tautology");
  return a.sort((x, y) => Math.abs(x) - Math.abs(y) || Number(x < 0) - Number(y < 0));
}
function eq(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function parseDimacs(text) {
  const ls = text.split(/\r?\n/).map(x => x.trim()).filter(x => x && !x.startsWith("c"));
  const h = ls[0].split(/\s+/);
  ok(h.length === 4 && h[0] === "p" && h[1] === "cnf", "strict header");
  const n = Number(h[2]), m = Number(h[3]);
  const cs = ls.slice(1).map(line => {
    const xs = line.split(/\s+/).map(Number);
    ok(xs.at(-1) === 0 && !xs.slice(0, -1).includes(0), "terminator");
    const c = canon(xs.slice(0, -1));
    ok(c.every(x => Math.abs(x) <= n), "source range");
    return c;
  });
  ok(cs.length === m, "source count");
  return [n, cs];
}
function truth(c, a) { return c.some(l => a.get(Math.abs(l)) === (l > 0)); }
function models(n, cs) {
  let count = 0;
  for (let mask = 0; mask < 2 ** n; mask++) {
    const a = new Map(Array.from({length:n}, (_, i) => [i + 1, Boolean(mask & (1 << i))]));
    if (cs.every(c => truth(c, a))) count++;
  }
  return count;
}
function facetValid(out, ins, table, clause) {
  if (!/^[01]{4}$/.test(table)) return false;
  const vars = [...new Set([out, ...ins])].sort((a,b)=>a-b);
  for (let mask = 0; mask < 2 ** vars.length; mask++) {
    const a = new Map(vars.map((v,i)=>[v, Boolean(mask & (1<<i))]));
    const idx = 2 * Number(a.get(ins[0])) + Number(a.get(ins[1]));
    if (a.get(out) === (table[idx] === "1") && !truth(clause, a)) return false;
  }
  return true;
}
function resolve(a, b, p) {
  ok(a.includes(p) && b.includes(-p), "oriented pivot");
  return canon([...a.filter(x=>x!==p), ...b.filter(x=>x!==-p)]);
}
function verify(t, safe) {
  const [n, sources] = parseDimacs(t.source_dimacs);
  const rec = [], owners = new Set();
  for (let i = 0; i < t.nodes.length; i++) {
    const x = t.nodes[i], ctx = canon(x.ctx), clause = canon(x.clause);
    if (x.rule === "SRC") {
      ok(ctx.length === 0 && x.source >= 0 && x.source < sources.length, "source scope/index");
      ok(eq(clause, sources[x.source]), "source identity");
    } else if (x.rule === "ASSUME") {
      ok(clause.length === 1 && ctx.includes(clause[0]), "assumption");
    } else if (x.rule === "DEF") {
      const owner = safe ? String(x.output) : `${JSON.stringify(ctx)}:${x.output}`;
      if (safe) {
        ok(x.output > n, "fresh from source universe");
        ok(!x.inputs.includes(x.output) && !ctx.some(l=>Math.abs(l)===x.output), "fresh from inputs/context");
      }
      ok(!owners.has(owner), "unique owner"); owners.add(owner);
      ok(facetValid(x.output, x.inputs, x.table, clause), "facet semantics");
    } else if (x.rule === "RES") {
      ok(x.parents.every(p=>Number.isInteger(p) && p>=0 && p<i), "parent order");
      const [a,b] = x.parents.map(p=>rec[p]);
      ok(a.ctx.every(l=>ctx.includes(l)) && b.ctx.every(l=>ctx.includes(l)), "context inclusion");
      ok(eq(resolve(a.clause,b.clause,x.pivot), clause), "resolvent");
    } else if (x.rule === "MERGE") {
      ok(x.parents.every(p=>Number.isInteger(p) && p>=0 && p<i), "merge parent order");
      const [a,b] = x.parents.map(p=>rec[p]);
      ok(eq(a.clause,clause) && eq(b.clause,clause), "merge conclusion");
      const want = [canon([...ctx,x.pivot]), canon([...ctx,-x.pivot])].map(JSON.stringify).sort();
      const got = [a.ctx,b.ctx].map(JSON.stringify).sort();
      ok(eq(got,want), "both AND branches");
    } else throw new Error("unknown rule");
    rec.push({ctx,clause});
  }
  ok(eq(rec.at(-1), {ctx:[],clause:[]}), "unconditional contradiction");
  return {n, sources:sources.length, nodes:rec.length, models:models(n,sources)};
}
function reject(t, safe, label) {
  try { verify(t, safe); } catch (_) { return; }
  throw new Error(`unexpected accept: ${label}`);
}
function bytes(o) { return Buffer.from(JSON.stringify(o, Object.keys(o).sort())); }
function canonical(o) {
  if (Array.isArray(o)) return `[${o.map(canonical).join(",")}]`;
  if (o && typeof o === "object") return `{${Object.keys(o).sort().map(k=>`${JSON.stringify(k)}:${canonical(o[k])}`).join(",")}}`;
  return JSON.stringify(o);
}

const unsafe = JSON.parse(fs.readFileSync(path.join(here,"unsafe_branch_def_referee368.json"),"utf8"));
const safe = JSON.parse(fs.readFileSync(path.join(here,"safe_branch_def_referee368.json"),"utf8"));
const u = verify(unsafe, false), s = verify(safe, true);
ok(u.models === 4, "unsafe source must be SAT");
ok(s.models === 0, "safe source must be UNSAT");
reject(unsafe, true, "unsafe trace under safe discipline");
const c1 = structuredClone(safe); c1.nodes[5].output=1; c1.nodes[5].clause=[-1,2]; reject(c1,true,"source reuse");
const c2 = structuredClone(safe); c2.nodes[8].output=3; c2.nodes[8].clause=[-3,2]; reject(c2,true,"owner reuse");
const c3 = structuredClone(safe); c3.nodes[5].clause=[3,2]; reject(c3,true,"facet corruption");
const c4 = structuredClone(safe); c4.nodes[9].parents=[4,4]; reject(c4,true,"omitted branch");
const c5 = structuredClone(safe); c5.nodes[7].ctx=[]; reject(c5,true,"scope leak");
const c6 = structuredClone(safe); c6.source_dimacs=c6.source_dimacs.replace("p cnf 2 3","p cnf 2 4"); reject(c6,true,"malformed source");

const out = {
  artifact:"REFEREE368-independent",
  assertions,
  unsafe:u,
  safe:s,
  unsafe_sha256:crypto.createHash("sha256").update(canonical(unsafe)+"\n").digest("hex"),
  safe_sha256:crypto.createHash("sha256").update(canonical(safe)+"\n").digest("hex"),
  status:"PASS",
};
fs.writeFileSync(path.join(root,"results/raw/arc/2026-11-05_1148_LSPV5_REFEREE368_independent.json"), JSON.stringify(out,null,2)+"\n");
console.log(JSON.stringify(out,null,2));
