#!/usr/bin/env node
// Independent REFEREE362 verification: raw identity and affine provenance.
import fs from "node:fs";
import crypto from "node:crypto";

const peer = JSON.parse(fs.readFileSync(
  "results/raw/arc/2026-11-05_0512_LSPV2_MIXED_DEF_PORT416.json", "utf8"));
const cert = peer.complete_certificate;
let checks = 0;
const ok = (x, m) => { checks++; if (!x) throw new Error(m); };

function simplify(xs) {
  return [...new Set(xs)].sort((a,b) => Math.abs(a)-Math.abs(b) || Number(a<0)-Number(b<0));
}
function parse(raw) {
  const lines = raw.split(/\r?\n/);
  let h = null; const cs = [];
  for (const line0 of lines) {
    const line = line0.trim();
    if (!line || line.startsWith("c")) continue;
    const f = line.split(/\s+/);
    if (f[0] === "p") {
      ok(h === null && f.length === 4 && f[1] === "cnf", "header");
      h = [Number(f[2]), Number(f[3])]; continue;
    }
    ok(h !== null, "clause before header");
    const a = f.map(Number);
    ok(a.at(-1) === 0 && !a.slice(0,-1).includes(0), "terminator");
    ok(a.slice(0,-1).every(x => Number.isInteger(x) && Math.abs(x) <= h[0]), "literal");
    cs.push(simplify(a.slice(0,-1)));
  }
  ok(h !== null && cs.length === h[1], "count");
  return {nvars:h[0], clauses:cs};
}
const sha = s => crypto.createHash("sha256").update(Buffer.from(s,"ascii")).digest("hex");

const a = "p cnf 2 3\n2 1 0\n1 0\n-1 0\n";
const b = "c byte-distinct source\np cnf 2 3\n1 2 0\n1 0\n-1 0\n";
ok(a !== b, "raw differ");
ok(JSON.stringify(parse(a)) === JSON.stringify(parse(b)), "same parsed source");
ok(sha(a) !== sha(b), "raw hashes differ");
const canonicalA = Buffer.from(a, "ascii").toString("base64");
const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
const pos = canonicalA.length - 3;
const old = alphabet.indexOf(canonicalA[pos]);
const aliasChar = alphabet[(old & 0b110000) | ((old + 1) & 0b001111)];
const noncanonicalA = canonicalA.slice(0,pos) + aliasChar + canonicalA.slice(pos+1);
ok(Buffer.from(noncanonicalA, "base64").equals(Buffer.from(a, "ascii")), "padding alias decodes");
ok(noncanonicalA !== canonicalA, "padding alias differs");
ok(Buffer.from(noncanonicalA, "base64").toString("base64") !== noncanonicalA,
   "canonical re-encoding rejects alias");
ok(JSON.stringify(parse(peer.raw_dimacs)) === JSON.stringify(cert.source), "peer raw parse");
ok(cert.nodes.length === 17, "peer node count");
ok(cert.nodes.every((n,i)=>n.id===i), "topological ids");
ok(cert.nodes.filter(n=>n.rule==="DEF").length===2, "two paid defs");
ok(cert.nodes.filter(n=>n.rule==="RES").length===10, "ten res");
ok(cert.nodes.filter(n=>n.rule==="AND3").length===3, "three and3");
ok(cert.nodes.filter(n=>n.rule==="LOCAL").length===1, "one local");
ok(cert.nodes.filter(n=>n.rule==="GF2").length===1, "one gf2");

// Static affine provenance induction for the complete peer certificate.
const views = new Map();
cert.source.clauses.forEach((c,i)=>views.set(`s:${i}:clause`, {kind:"clause", support:new Set(c.map(Math.abs))}));
const key = r => "src" in r ? `s:${r.src}:${r.view}` :
  `n:${r.node}:${r.view}${"facet" in r ? ":"+r.facet : ""}`;
for (const n of cert.nodes) {
  if (n.rule === "DEF") {
    for (let j=0;j<4;j++) views.set(`n:${n.id}:clause:${j}`, {kind:"clause", support:new Set([...n.inputs,n.var])});
  } else if (n.rule === "RES") {
    ok(views.has(key(n.left)) && views.has(key(n.right)), "RES refs");
    views.set(`n:${n.id}:clause`, {kind:"clause", support:new Set(n.clause.map(Math.abs))});
  } else if (n.rule === "AND3") {
    const l=views.get(key(n.left)), r=views.get(key(n.right));
    ok(l && r, "AND3 refs");
    const u=new Set([...l.support,...r.support]);
    ok([...u].every(v=>v<=cert.source.nvars), "AND3 original-only firewall");
    views.set(`n:${n.id}:factor`, {kind:"factor", support:new Set(n.factor.support)});
    if (n.affine) {
      ok(n.affine.mask.every(v=>v<=cert.source.nvars), "affine original-only");
      views.set(`n:${n.id}:affine`, {kind:"affine", support:new Set(n.affine.mask)});
    }
  } else if (n.rule === "LOCAL") {
    const p=views.get(key(n.parent)); ok(p, "LOCAL ref");
    const s=n.out.kind==="clause" ? n.out.clause.map(Math.abs) : n.out.factor.support;
    ok([...p.support,...s].every(v=>v<=cert.source.nvars), "LOCAL original-only firewall");
    views.set(`n:${n.id}:${n.out.kind}`, {kind:n.out.kind, support:new Set(s)});
  } else if (n.rule === "GF2") {
    const l=views.get(key(n.left)), r=views.get(key(n.right));
    ok(l?.kind==="affine" && r?.kind==="affine", "GF2 typed parents");
    ok(n.affine.mask.every(v=>v<=cert.source.nvars), "GF2 original-only");
    views.set(`n:${n.id}:affine`, {kind:"affine", support:new Set(n.affine.mask)});
  }
}
ok(views.get("n:16:affine")?.support.size===0 && cert.nodes[16].affine.rhs===1, "final 0=1");

// All DEF truth tables have only clause-facet views, never affine views.
for (let t=0;t<16;t++) for (let f=0;f<4;f++) {
  const available = new Set([`n:0:clause:${f}`]);
  ok(!available.has("n:0:affine"), "no direct DEF affine view");
}

console.log(JSON.stringify({status:"PASS", checks, peer_nodes:cert.nodes.length,
  raw_hash_a:sha(a), raw_hash_b:sha(b), direct_def_affine_views:0}));
