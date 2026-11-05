#!/usr/bin/env node
// Independent REFEREE369 replay. No Python checker code is imported.

import fs from "node:fs";
import crypto from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../..");
let assertions = 0;
function ok(v, msg) { assertions++; if (!v) throw new Error(msg); }
function eq(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function parseLit(lit) {
  ok(typeof lit === "string", "literal string");
  const m = lit.match(/^(~)?([xd])([1-9][0-9]*)$/);
  ok(m !== null, "qualified literal");
  return { neg: Boolean(m[1]), kind: m[2], id: Number(m[3]) };
}
function opposite(lit) { return lit.startsWith("~") ? lit.slice(1) : `~${lit}`; }
function canonClause(xs) {
  const a = xs.map(String);
  a.forEach(parseLit);
  ok(new Set(a).size === a.length, "duplicate literal");
  for (const x of a) ok(!a.includes(opposite(x)), "tautology");
  return a.sort((x, y) => {
    const a = parseLit(x), b = parseLit(y);
    return a.kind.localeCompare(b.kind) || a.id - b.id || Number(a.neg) - Number(b.neg);
  });
}
function canonCtx(xs) {
  const a = xs.map(Number);
  ok(!a.includes(0) && new Set(a).size === a.length, "context duplicate/zero");
  for (const x of a) ok(!a.includes(-x), "context contradiction");
  return a.sort((x, y) => Math.abs(x) - Math.abs(y) || Number(x < 0) - Number(y < 0));
}
function parseDimacs(text) {
  const ls = text.split(/\r?\n/).map(x => x.trim()).filter(x => x && !x.startsWith("c"));
  ok(ls.length > 0, "source nonempty");
  const h = ls[0].split(/\s+/);
  ok(h.length === 4 && h[0] === "p" && h[1] === "cnf", "strict header");
  const n = Number(h[2]), m = Number(h[3]);
  const cs = ls.slice(1).map(line => {
    const vals = line.split(/\s+/).map(Number);
    ok(vals.at(-1) === 0 && !vals.slice(0, -1).includes(0), "terminator");
    ok(vals.slice(0, -1).every(v => Math.abs(v) <= n), "source range");
    return canonClause(vals.slice(0, -1).map(v => `${v < 0 ? "~" : ""}x${Math.abs(v)}`));
  });
  ok(cs.length === m, "source count");
  return { n, cs };
}
function subset(a, b) { return a.every(x => b.includes(x)); }
function clauseTrue(c, assignment) {
  return c.some(l => { const x = parseLit(l); return assignment.get(`${x.kind}${x.id}`) !== x.neg; });
}
function models(n, cs) {
  let out = 0;
  for (let mask = 0; mask < 2 ** n; mask++) {
    const a = new Map(Array.from({length:n}, (_,i)=>[`x${i+1}`, Boolean(mask & (1<<i))]));
    if (cs.every(c => clauseTrue(c, a))) out++;
  }
  return out;
}
function visible(clause, ctx, records, idx, self=false) {
  for (const lit of clause) {
    const x = parseLit(lit);
    if (x.kind !== "d") continue;
    ok(x.id < idx || (self && x.id === idx), "owner precedes use");
    if (x.id === idx) continue;
    ok(records[x.id]?.rule === "DEF", "owner is DEF");
    ok(subset(records[x.id].ctx, ctx), "owner context visible");
  }
}
function exactDef(owner, inputs, table, facets) {
  ok(/^[01]{4}$/.test(table), "truth table");
  const atoms = [...new Set([...inputs.map(l => { const x=parseLit(l); return `${x.kind}${x.id}`; }), `d${owner}`])];
  for (let mask = 0; mask < 2 ** atoms.length; mask++) {
    const a = new Map(atoms.map((v,i)=>[v, Boolean(mask & (1<<i))]));
    const i0=parseLit(inputs[0]), i1=parseLit(inputs[1]);
    const b0=a.get(`${i0.kind}${i0.id}`), b1=a.get(`${i1.kind}${i1.id}`);
    const relation = a.get(`d${owner}`) === (table[2*Number(b0)+Number(b1)] === "1");
    const cnf = facets.every(f => clauseTrue(f,a));
    ok(relation === cnf, "exact definition relation");
  }
}
function resolve(a,b,p) {
  parseLit(p);
  ok(a.includes(p) && b.includes(opposite(p)), "oriented pivot");
  return canonClause([...a.filter(x=>x!==p), ...b.filter(x=>x!==opposite(p))]);
}
function parent(ref, idx, records) {
  let node, facet;
  if (Number.isInteger(ref)) { node=ref; facet=null; }
  else { ok(ref && Object.keys(ref).sort().join(",") === "facet,node", "parent ref shape"); node=Number(ref.node); facet=Number(ref.facet); }
  ok(Number.isInteger(node) && node >= 0 && node < idx, "acyclic parent");
  const r=records[node];
  if (facet === null) { ok(r.rule !== "DEF", "DEF needs facet"); return {ctx:r.ctx, clause:r.clause, node}; }
  ok(r.rule === "DEF" && Number.isInteger(facet) && facet >= 0 && facet < r.facets.length, "facet ref");
  return {ctx:r.ctx, clause:r.facets[facet], node};
}
function verify(t) {
  ok(t.format === "REFEREE369-scoped-owner-v1", "format");
  const {n,cs}=parseDimacs(t.source_dimacs), records=[], spans=[];
  const aliases=new Map();
  for (let i=0;i<t.nodes.length;i++) {
    const x=t.nodes[i], ctx=canonCtx(x.ctx), r={rule:x.rule,ctx};
    let span;
    if (x.rule === "SRC") {
      const c=canonClause(x.clause); visible(c,ctx,records,i);
      ok(ctx.length===0 && x.source>=0 && x.source<cs.length && eq(c,cs[x.source]), "source auth");
      r.clause=c; span=0;
    } else if (x.rule === "ASSUME") {
      const c=canonClause(x.clause); ok(c.length===1,"unit assumption");
      const l=parseLit(c[0]); ok(l.kind==="x" && l.id<=n,"original assumption");
      ok(ctx.includes(l.neg ? -l.id : l.id),"assumption context"); r.clause=c; span=1;
    } else if (x.rule === "DEF") {
      ok(typeof x.alias==="string" && x.alias && !x.alias.startsWith("x") && !x.alias.startsWith("d"),"cosmetic alias namespace");
      aliases.set(x.alias,[...(aliases.get(x.alias)||[]),i]);
      const ins=x.inputs.map(String); ins.forEach(parseLit); visible(ins,ctx,records,i);
      const fs=x.facets.map(canonClause); fs.forEach(f=>{visible(f,ctx,records,i,true); ok(f.some(l=>{const z=parseLit(l); return z.kind==="d"&&z.id===i;}),"owned output in facet");});
      exactDef(i,ins,x.table,fs); Object.assign(r,{inputs:ins,facets:fs,alias:x.alias}); span=1;
    } else if (x.rule === "RES") {
      const c=canonClause(x.clause); visible(c,ctx,records,i);
      const a=parent(x.parents[0],i,records), b=parent(x.parents[1],i,records);
      ok(subset(a.ctx,ctx)&&subset(b.ctx,ctx),"parent contexts"); ok(eq(resolve(a.clause,b.clause,x.pivot),c),"resolvent");
      r.clause=c; span=1+Math.max(spans[a.node],spans[b.node]);
    } else if (x.rule === "MERGE") {
      const c=canonClause(x.clause); visible(c,ctx,records,i); ok(x.parents.length===2,"two merge parents");
      const a=parent(x.parents[0],i,records), b=parent(x.parents[1],i,records);
      ok(eq(a.clause,c)&&eq(b.clause,c),"merge clauses");
      const want=[canonCtx([...ctx,x.pivot]),canonCtx([...ctx,-x.pivot])].map(JSON.stringify).sort();
      const got=[a.ctx,b.ctx].map(JSON.stringify).sort(); ok(eq(got,want),"both branches");
      r.clause=c; span=1+Math.max(spans[a.node],spans[b.node]);
    } else throw new Error("unknown rule");
    records.push(r); spans.push(span);
  }
  ok(eq(records.at(-1).ctx,[])&&eq(records.at(-1).clause,[]),"final contradiction");
  return {n,cs,records,aliases:Object.fromEntries(aliases),paid:records.filter(r=>r.rule!=="SRC").length,span:spans.at(-1)};
}
function alphaExpected(t) {
  const v=verify(t), owners=v.records.map((r,i)=>r.rule==="DEF"?i:null).filter(i=>i!==null);
  const map=new Map(owners.map((o,i)=>[o,v.n+i+1]));
  function tr(l) { const x=parseLit(l), id=x.kind==="x"?x.id:map.get(x.id); return `${x.neg?"~":""}x${id}`; }
  const c=structuredClone(t); c.format="REFEREE369-global-alpha-v1";
  c.alpha_map=Object.fromEntries(owners.map(o=>[`d${o}`,`x${map.get(o)}`]));
  for (const n of c.nodes) {
    if (n.clause) n.clause=canonClause(n.clause.map(tr));
    if (n.inputs) n.inputs=n.inputs.map(tr);
    if (n.facets) n.facets=n.facets.map(f=>canonClause(f.map(tr)));
    if (n.rule === "RES") n.pivot=tr(String(n.pivot));
  }
  for (let i=0;i<c.nodes.length;i++) {
    if (c.nodes[i].rule === "DEF") {
      c.nodes[i].global_output=map.get(i);
      c.nodes[i].alias=`g${map.get(i)}`;
    }
  }
  return {compiled:c, owners, targets:[...map.values()], paid:v.paid, span:v.span};
}
function reject(t,label) { try { verify(t); } catch (_) { return; } throw new Error(`unexpected accept: ${label}`); }
function canonical(o) {
  if (Array.isArray(o)) return `[${o.map(canonical).join(",")}]`;
  if (o && typeof o === "object") return `{${Object.keys(o).sort().map(k=>`${JSON.stringify(k)}:${canonical(o[k])}`).join(",")}}`;
  return JSON.stringify(o);
}

const trace=JSON.parse(fs.readFileSync(path.join(here,"scoped_alias_trace_referee369.json"),"utf8"));
const compiled=JSON.parse(fs.readFileSync(path.join(here,"global_alpha_trace_referee369.json"),"utf8"));
const v=verify(trace), a=alphaExpected(trace);
ok(models(v.n,v.cs)===0,"source UNSAT"); ok(eq(v.aliases.z,[5,10]),"same alias in siblings");
ok(canonical(compiled)===canonical(a.compiled),"canonical alpha bytes"); ok(a.targets.every(x=>x>v.n)&&new Set(a.targets).size===a.targets.length,"fresh targets");
ok(a.paid===v.paid&&a.span===v.span,"work/span preserved");
let b=structuredClone(trace); b.nodes[11].parents[1]={node:5,facet:1}; reject(b,"sibling capture");
b=structuredClone(trace); b.nodes[6].clause=["z"]; reject(b,"unqualified alias");
b=structuredClone(trace); b.nodes.splice(14,0,{rule:"MERGE",ctx:[],parents:[6,11],pivot:1,clause:["d5"]}); reject(b,"escape");
b=structuredClone(trace); b.nodes[13].parents=[7,7]; reject(b,"omitted branch");
b=structuredClone(trace); b.nodes[5].facets[0]=["d5","x2"]; reject(b,"corrupt facet");
b=structuredClone(trace); b.nodes[10].alias="x1"; reject(b,"semantic namespace alias");
b=structuredClone(trace); b.source_dimacs=b.source_dimacs.replace("p cnf 2 3","p cnf 2 4"); reject(b,"malformed source");
b=structuredClone(trace); b.source_dimacs=b.source_dimacs.replace("p cnf 2 3","p cnf 2 4"); reject(b,"malformed source");

const out={artifact:"REFEREE369-independent",status:"PASS",assertions,source_models:models(v.n,v.cs),paid_nodes:v.paid,span:v.span,
  alias_owners:v.aliases.z,alpha_targets:a.targets,
  trace_sha256:crypto.createHash("sha256").update(canonical(trace)+"\n").digest("hex"),
  compiled_sha256:crypto.createHash("sha256").update(canonical(compiled)+"\n").digest("hex")};
fs.writeFileSync(path.join(root,"results/raw/arc/2026-11-05_1248_LSPV5_REFEREE369_independent.json"),JSON.stringify(out,null,2)+"\n");
console.log(JSON.stringify(out,null,2));
