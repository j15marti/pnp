#!/usr/bin/env node
"use strict";

const fs = require("fs");
const file = "results/raw/arc/lspv5_341/evaluator_cost_reflection_referee341.json";
const data = JSON.parse(fs.readFileSync(file, "utf8"));
let checks = 0;
function ok(x, msg) { if (!x) throw new Error(msg); checks++; }
function ordered(c) { return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b); }
function key(c) { return ordered(c).join(","); }
function taut(c) { const s=new Set(c); return c.some(x=>s.has(-x)); }
function resolve(a,b,p) {
  const A=new Set(a), B=new Set(b); let x,y;
  if(A.has(p)&&B.has(-p)){x=p;y=-p;} else if(A.has(-p)&&B.has(p)){x=-p;y=p;}
  else throw new Error("bad pivot");
  A.delete(x); B.delete(y); const c=[...A,...B];
  if(taut(c)) throw new Error("tautological resolvent");
  return ordered(c);
}
function slots(g) {
  const [a,b]=g.inputs, o=g.out;
  if(g.op==="OR") return [[-a,o],[-b,o],[a,b,-o]];
  if(g.op==="AND") return [[-o,a],[-o,b],[o,-a,-b]];
  throw new Error("bad gate");
}

const rec=data.block2.record, env=new Map();
for(const s of rec.sources){ok(!env.has(s.id),"duplicate source");env.set(s.id,s.clause);}
for(const g of rec.defs){
  const want=slots(g);
  ok(g.slots.length===3,"slot count");
  g.slots.forEach((s,i)=>{ok(key(s.clause)===key(want[i]),"bad slot");env.set(s.id,s.clause);});
}
for(const r of rec.res){
  ok(env.has(r.left)&&env.has(r.right),"missing replay parent");
  ok(key(resolve(env.get(r.left),env.get(r.right),r.pivot))===key(r.clause),"bad replay step");
  env.set(r.id,r.clause);
}
ok(key(env.get(rec.root_ref))===String(rec.root_literal),"bad root unit");
for(const r of data.block2.downstream){
  ok(env.has(r.left)&&env.has(r.right),"missing downstream parent");
  ok(key(resolve(env.get(r.left),env.get(r.right),r.pivot))===key(r.clause),"bad downstream step");
  env.set(r.id,r.clause);
}
ok(env.get(data.block2.final_ref).length===0,"not contradiction");
ok(rec.defs.length===rec.literal_count-1,"gate formula");
ok(rec.res.length===2*(rec.literal_count-1),"replay formula");
ok(rec.paid===3*(rec.literal_count-1),"paid formula");
ok(data.block2.spliced_paid===rec.paid+data.block2.downstream_resolution_nodes,"splice sum");
ok(data.polarity_and_chain_records_checked===262,"coverage count");
ok(data.malformed_rejected===5,"malformed count");
console.log(JSON.stringify({checks,status:"PASS"}));
