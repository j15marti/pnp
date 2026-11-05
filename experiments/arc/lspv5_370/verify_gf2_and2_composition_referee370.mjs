#!/usr/bin/env node
// Independent REFEREE370 replay; no Python implementation is imported.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { performance } from "node:perf_hooks";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../..");
const rawPath = path.join(root, "results/raw/arc/2026-11-05_1348_LSPV5_REFEREE370_raw.json");
const outPath = path.join(root, "results/raw/arc/2026-11-05_1348_LSPV5_REFEREE370_independent.json");
const started = performance.now();
let assertions = 0;
function ok(x, m) { assertions++; if (!x) throw new Error(m); }
function stable(x) {
  if (Array.isArray(x)) return `[${x.map(stable).join(",")}]`;
  if (x && typeof x === "object") return `{${Object.keys(x).sort().map(k=>`${JSON.stringify(k)}:${stable(x[k])}`).join(",")}}`;
  return JSON.stringify(x);
}
function canon(xs) {
  const s = new Set([...xs].map(Number));
  ok(!s.has(0), "zero literal");
  for (const x of s) if (s.has(-x)) return null;
  return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b) || Number(a<0)-Number(b<0));
}
function key(c) { return JSON.stringify(c); }
function resolve(a,b,p) {
  ok(a.includes(p) && b.includes(-p), "oriented pivot");
  const x=new Set(a.filter(q=>q!==p)), y=new Set(b.filter(q=>q!==-p));
  for (const q of x) ok(!y.has(-q), "nonpivot complement");
  return canon([...x,...y]);
}
function vars(mask) { return [1,2,3,4,5].filter(v=>mask&(1<<(v-1))); }
function assignments(vs) {
  const out=[];
  for (let m=0;m<2**vs.length;m++) out.push(new Map(vs.map((v,i)=>[v,Number(Boolean(m&(1<<i)))])));
  return out;
}
function violation(mask,rhs,a) { let p=0; for(const v of vars(mask)) p^=a.get(v); return p!==rhs; }
function blocker(vs,a) { return canon(vs.map(v=>a.get(v)===0?v:-v)); }

let pairs=0, blockers=0, stepsTotal=0, maxSteps=0, exact=0, proper=0;
for(let ma=0;ma<32;ma++) for(let ra=0;ra<2;ra++) for(let mb=0;mb<32;mb++) for(let rb=0;rb<2;rb++) {
  pairs++;
  const sa=new Set(vars(ma)), sb=new Set(vars(mb));
  const inter=[...sa].filter(v=>sb.has(v)).sort(), diff=[...new Set([...sa,...sb])].filter(v=>!(sa.has(v)&&sb.has(v))).sort();
  for(const tau of assignments(diff)) {
    if(!violation(ma^mb,ra^rb,tau)) continue;
    blockers++;
    let level=new Map();
    for(const u of assignments(inter)) {
      const full=new Map([...tau,...u]);
      const af=violation(ma,ra,full), bf=violation(mb,rb,full);
      ok(af!==bf,"exactly one parent violated");
      const c=blocker(vars(af?ma:mb),full);
      level.set(inter.map(v=>u.get(v)).join(""),c);
    }
    let active=[...inter], steps=0;
    while(active.length) {
      const p=active.at(-1), next=new Map(), prefixes=new Set([...level.keys()].map(k=>k.slice(0,-1)));
      for(const pre of prefixes) { next.set(pre,resolve(level.get(pre+"0"),level.get(pre+"1"),p)); steps++; }
      level=next; active.pop();
    }
    const final=level.get(""), target=blocker(diff,tau);
    ok(final.every(x=>target.includes(x)),"final subclause");
    ok(steps<=2**inter.length-1,"tree bound");
    stepsTotal+=steps; maxSteps=Math.max(maxSteps,steps);
    if(key(final)===key(target)) exact++; else proper++;
  }
}

function clauses(vs) {
  const out=[];
  for(let m=0;m<3**vs.length;m++) { let q=m, lits=[]; for(const v of vs){const d=q%3;q=Math.floor(q/3);if(d===1)lits.push(-v);if(d===2)lits.push(v);} out.push(canon(lits)); }
  return out;
}
function subst(c,a,b,z=3) {
  if(c===null)return [];
  ok(Math.abs(a)!==z&&Math.abs(b)!==z,"self input");
  let cs;
  if(c.includes(z)){const r=c.filter(x=>x!==z);cs=[canon([...r,a]),canon([...r,b])];}
  else if(c.includes(-z)){const r=c.filter(x=>x!==-z);cs=[canon([...r,-a,-b])];}
  else cs=[c];
  return [...new Map(cs.filter(x=>x!==null).map(x=>[key(x),x])).values()];
}
function closure(initial) {
  const d=new Map(initial.map(c=>[key(c),{c,d:0}])); let changed=true;
  while(changed){changed=false;const now=[...d.values()];for(const L of now)for(const R of now)for(const p of [1,2,4]){
    if(!L.c.includes(p)||!R.c.includes(-p))continue;let o;try{o=resolve(L.c,R.c,p);}catch{continue;}const k=key(o),nd=1+Math.max(L.d,R.d);
    if(!d.has(k)||nd<d.get(k).d){d.set(k,{c:o,d:nd});changed=true;}
  }} return [...d.values()];
}
const cs=clauses([1,2,3,4]), inf=[];
for(const p of [1,2,3,4])for(const l of cs)if(l.includes(p))for(const r of cs)if(r.includes(-p)){try{inf.push([l,r,p,resolve(l,r,p)]);}catch{}}
const count={identical:0,complementary:0,distinct:0}, obligations={identical:0,complementary:0,distinct:0}, maxDepth={identical:0,complementary:0,distinct:0};
let facetChecks=0;
for(const a of [1,-1,2,-2])for(const b of [1,-1,2,-2]){
  const cl=a===b?"identical":a===-b?"complementary":"distinct";
  count[cl]++;
  for(const f of [[-3,a],[-3,b],[3,-a,-b]]){facetChecks++;ok(subst(canon(f),a,b).length===0,"facet tautology");}
  for(const [l,r,p,o] of inf){const init=[...new Map([...subst(l,a,b),...subst(r,a,b)].map(c=>[key(c),c])).values()],clo=closure(init);
    for(const g of subst(o,a,b)){obligations[cl]++;const ds=clo.filter(x=>x.c.every(q=>g.includes(q))).map(x=>x.d);ok(ds.length>0,"reachable target");maxDepth[cl]=Math.max(maxDepth[cl],Math.min(...ds));}
  }
}

const raw=JSON.parse(fs.readFileSync(rawPath,"utf8"));
ok(raw.status==="PASS","raw pass"); ok(raw.gf2.ordered_pairs===pairs,"pair count");
ok(raw.gf2.output_blockers===blockers,"blocker count"); ok(raw.gf2.strict_resolution_steps_constructed===stepsTotal,"step count");
ok(raw.gf2.maximum_steps_for_one_blocker===maxSteps,"max steps"); ok(raw.gf2.exact_output_blockers===exact,"exact count"); ok(raw.gf2.proper_subclause_outputs===proper,"proper count");
ok(raw.and2_elimination.original_strict_inferences===inf.length,"inference count"); ok(stable(raw.and2_elimination.pair_classes)===stable(count),"pair classes");
ok(stable(raw.and2_elimination.target_clause_obligations)===stable(obligations),"obligations"); ok(stable(raw.and2_elimination.maximum_local_resolution_depth)===stable(maxDepth),"depths");
ok(raw.and2_elimination.definition_facets_eliminated_as_tautologies===facetChecks,"facet checks");
const result={artifact:"REFEREE370-independent",status:"PASS",assertions,ordered_pairs:pairs,output_blockers:blockers,
  strict_resolution_steps_constructed:stepsTotal,maximum_steps_for_one_blocker:maxSteps,original_strict_inferences:inf.length,
  pair_classes:count,target_clause_obligations:obligations,maximum_local_resolution_depth:maxDepth,definition_facets_checked:facetChecks,
  resource_ledger:{construction_search_seconds:Number(((performance.now()-started)/1000).toFixed(6)),rss_bytes:process.memoryUsage().rss,
    logical_xor_trace:"not used",offline_diagnostic:true}};
fs.writeFileSync(outPath,JSON.stringify(result,null,2)+"\n"); console.log(JSON.stringify(result,null,2));
