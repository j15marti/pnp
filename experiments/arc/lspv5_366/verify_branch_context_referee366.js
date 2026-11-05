#!/usr/bin/env node
"use strict";

// Independently structured replay.  This does not import the Python checker.
const fs = require("fs");
const crypto = require("crypto");
const path = require("path");

const root = path.resolve(__dirname, "../../..");
const tracePath = path.join(__dirname, "branch_shared_trace_referee366.json");
const rawPath = path.join(root, "results/raw/arc/2026-11-05_0948_LSPV5_REFEREE366_raw.json");
const outPath = path.join(root, "results/raw/arc/2026-11-05_0948_LSPV5_REFEREE366_independent.json");
let assertions = 0;
function ok(value, message) { assertions++; if (!value) throw new Error(message); }
function key(x) { return [Math.abs(x), x < 0 ? 1 : 0]; }
function cmp(a,b) { const x=key(a), y=key(b); return x[0]-y[0] || x[1]-y[1]; }
function canon(xs, taut=false) {
  ok(Array.isArray(xs) && xs.every(Number.isInteger) && xs.every(x=>x!==0), "bad literals");
  ok(new Set(xs).size===xs.length, "duplicate literal");
  if (!taut) ok(xs.every(x=>!xs.includes(-x)), "tautology/context conflict");
  ok(JSON.stringify(xs)===JSON.stringify([...xs].sort(cmp)), "noncanonical order");
  return xs;
}
function res(a,b,p) {
  const A=new Set(a), B=new Set(b); let C;
  if (A.has(p)&&B.has(-p)) C=[...A].filter(x=>x!==p).concat([...B].filter(x=>x!==-p));
  else if (A.has(-p)&&B.has(p)) C=[...A].filter(x=>x!==-p).concat([...B].filter(x=>x!==p));
  else throw new Error("bad pivot");
  C=[...new Set(C)].sort(cmp); ok(C.every(x=>!C.includes(-x)), "tautological resolvent"); return C;
}
function clauseTrue(c,m){return c.some(l=>Boolean(m&(1<<(Math.abs(l)-1)))===(l>0));}
function ctxTrue(c,m){return c.every(l=>Boolean(m&(1<<(Math.abs(l)-1)))===(l>0));}

const bytes=fs.readFileSync(tracePath); const t=JSON.parse(bytes.toString("utf8"));
const lines=t.source_raw.trimEnd().split("\n");
const head=lines[0].split(/\s+/); const n=+head[2], m=+head[3];
ok(head[0]==="p"&&head[1]==="cnf"&&lines.length===m+1,"header");
const source=lines.slice(1).map(line=>line.split(/\s+/).map(Number).slice(0,-1).sort(cmp));
ok(crypto.createHash("sha256").update(t.source_raw).digest("hex")===t.source_sha256,"source hash");
const nodes=[]; let paid=0, valuations=0, parentRefs=0;
t.nodes.forEach((r,i)=>{
  ok(r.id===i,"dense id"); canon(r.context); canon(r.clause);
  if(r.rule==="SRC") { ok(r.context.length===0&&JSON.stringify(r.clause)===JSON.stringify(source[r.source_index]),"source auth"); }
  else if(r.rule==="ASSUME") { paid++; ok(r.context.includes(r.literal)&&r.clause.length===1&&r.clause[0]===r.literal,"assume"); }
  else if(r.rule==="RES") { paid++; const L=nodes[r.left],R=nodes[r.right]; parentRefs+=2;
    ok(L.ctx.every(x=>r.context.includes(x))&&R.ctx.every(x=>r.context.includes(x)),"context subset");
    ok(JSON.stringify(res(L.clause,R.clause,r.pivot))===JSON.stringify(r.clause),"res");
  } else if(r.rule==="MERGE") { paid++; const L=nodes[r.left],R=nodes[r.right]; parentRefs+=2;
    const plus=[...r.context,r.split].sort(cmp),minus=[...r.context,-r.split].sort(cmp);
    ok((JSON.stringify(L.ctx)===JSON.stringify(plus)&&JSON.stringify(R.ctx)===JSON.stringify(minus))||
       (JSON.stringify(R.ctx)===JSON.stringify(plus)&&JSON.stringify(L.ctx)===JSON.stringify(minus)),"merge contexts");
    ok(JSON.stringify(L.clause)===JSON.stringify(r.clause)&&JSON.stringify(R.clause)===JSON.stringify(r.clause),"merge clauses");
  } else throw new Error("rule");
  nodes.push({ctx:r.context,clause:r.clause});
  for(let mask=0;mask<(1<<n);mask++){valuations++;if(source.every(c=>clauseTrue(c,mask))&&ctxTrue(r.context,mask))ok(clauseTrue(r.clause,mask),"semantic audit");}
});
ok(t.final===nodes.length-1&&nodes[t.final].ctx.length===0&&nodes[t.final].clause.length===0,"final");
const raw=JSON.parse(fs.readFileSync(rawPath,"utf8"));
ok(raw.accepted_trace.sha256===crypto.createHash("sha256").update(bytes).digest("hex"),"raw sha");
ok(raw.accepted_trace.bytes===bytes.length&&raw.accepted_trace.paid_nodes===paid,"raw counts");
ok(raw.controls.find(x=>x.label==="minimal_context_erasure_exploit").unsafe_accepts===true,"unsafe exploit");
const out={schema:"LSPV5_REFEREE366_INDEPENDENT_V1",trace_sha256:raw.accepted_trace.sha256,
  trace_bytes:bytes.length,source_clauses:m,nodes:nodes.length,paid_nodes:paid,parent_refs:parentRefs,
  semantic_valuations:valuations,assertions,status:"PASS",limitations:"independent declared checker; not authoritative R_mix341"};
fs.writeFileSync(outPath,JSON.stringify(out,null,2)+"\n"); console.log(JSON.stringify(out,null,2));
