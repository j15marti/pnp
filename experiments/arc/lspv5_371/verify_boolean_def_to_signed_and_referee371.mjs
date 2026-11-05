#!/usr/bin/env node
// Independent REFEREE371 replay; does not import the Python implementation.

import fs from "node:fs";
import path from "node:path";
import { performance } from "node:perf_hooks";
import { fileURLToPath } from "node:url";

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,"../../..");
const rawPath=path.join(root,"results/raw/arc/2026-11-05_1448_LSPV5_REFEREE371_raw.json");
const outPath=path.join(root,"results/raw/arc/2026-11-05_1448_LSPV5_REFEREE371_independent.json");
const started=performance.now(), ALL=15, A=12, B=10;
let assertions=0;
function ok(x,m){assertions++;if(!x)throw new Error(m);}
function lf(f,n){return n?(f^ALL):f;}
function stateKey(s){return [...s].sort((a,b)=>a-b).join(",");}
function synth(){
  const start=new Set([A,B]), queue=[start], pred=new Map([[stateKey(start),null]]), stateBy=new Map([[stateKey(start),start]]), found=new Map();
  for(let qi=0;qi<queue.length&&found.size<14;qi++){
    const s=queue[qi], fs=[...s].sort((a,b)=>a-b);
    for(const p of fs)for(const np of [false,true])for(const r of fs)for(const nr of [false,true]){
      const h=lf(p,np)&lf(r,nr);if(s.has(h))continue;const n=new Set(s);n.add(h);const k=stateKey(n);
      if(!pred.has(k)){pred.set(k,{parent:stateKey(s),step:[p,np,r,nr,h]});stateBy.set(k,n);queue.push(n);}
      if(!found.has(h))found.set(h,k);
    }
  }
  const t=new Map();
  for(let target=0;target<16;target++){
    if(target===A||target===B){t.set(target,[[target,false,target,false,target]]);continue;}
    let k=found.get(target), path=[];while(pred.get(k)!==null){const e=pred.get(k);path.push(e.step);k=e.parent;}t.set(target,path.reverse());
  }
  return {templates:t,states:pred.size};
}
function expected(t,a,b){return Boolean(t&(1<<(2*Number(a)+Number(b))));}
function evalTemplate(steps,a,b){const v=new Map([[A,a],[B,b]]);for(const [p,np,r,nr,h] of steps)v.set(h,(v.get(p)!==np)&&(v.get(r)!==nr));return v.get(steps.at(-1)[4]);}
function norm(c){const s=new Set(c);for(const x of s)if(s.has(-x))return null;return [...s].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);}
function ck(c){return c.join(",");}
function instantiate(steps){
  const rep=new Map([[A,1],[B,2]]);let next=3, facets=[], output;
  for(const [p,np,r,nr,h] of steps){const lp=(np?-1:1)*rep.get(p),lr=(nr?-1:1)*rep.get(r),z=next++;
    for(const c of [[-z,lp],[-z,lr],[z,-lp,-lr]]){const n=norm(c);if(n)facets.push(n);}
    rep.set(h,z);output=z;
  }return {facets,output};
}
function closure(seed){
  const cls=new Map(),parent=new Map();for(const c of seed){cls.set(ck(c),c);parent.set(ck(c),null);}
  let changed=true;while(changed){changed=false;const cur=[...cls.values()];
    for(let i=0;i<cur.length;i++)for(let j=i+1;j<cur.length;j++)for(const p of cur[i])if(cur[j].includes(-p)){
      const n=norm([...cur[i].filter(x=>x!==p),...cur[j].filter(x=>x!==-p)]);if(!n)continue;const k=ck(n);
      if(!cls.has(k)){cls.set(k,n);parent.set(k,[ck(cur[i]),ck(cur[j])]);changed=true;}
    }
  }return {cls,parent};
}
function anc(k,parent,seen=new Set()){if(seen.has(k)||parent.get(k)===null)return 0;seen.add(k);const [a,b]=parent.get(k);return 1+anc(a,parent,seen)+anc(b,parent,seen);}
function subset(c,t){return c.every(x=>t.includes(x));}
function clauseValue(c,assn){return c.some(x=>x>0?assn.get(x):!assn.get(-x));}
function projectedAudit(table,steps){
  const {facets,output}=instantiate(steps),{cls,parent}=closure(facets),atoms=[1,2,output];let implicates=0,maxNodes=0,proper=0;
  for(const s0 of [-1,0,1])for(const s1 of [-1,0,1])for(const s2 of [-1,0,1]){
    const ss=[s0,s1,s2],target=[];for(let i=0;i<3;i++)if(ss[i]!==-1)target.push(ss[i]===0?atoms[i]:-atoms[i]);if(!target.length)continue;
    let valid=true;for(const a of [false,true])for(const b of [false,true]){const as=new Map([[1,a],[2,b],[output,expected(table,a,b)]]);if(!clauseValue(target,as))valid=false;}
    if(!valid)continue;implicates++;const cand=[...cls.entries()].filter(([,c])=>subset(c,target));ok(cand.length>0,"projected facet derivable");
    cand.sort((x,y)=>x[1].length-y[1].length||anc(x[0],parent)-anc(y[0],parent));const [k,c]=cand[0];maxNodes=Math.max(maxNodes,anc(k,parent));if(c.length<target.length)proper++;
  }return {implicates,maxNodes,proper,closure:cls.size};
}
const {templates,states}=synth(),dist={1:0,2:0,3:0};let truthChecks=0;
let projected={projected_implicates:0,maximum_resolution_nodes:0,maximum_closure_clauses:0,proper_subclause_witnesses:0};
for(let t=0;t<16;t++){const s=templates.get(t);ok(s.length>=1&&s.length<=3,"three gate bound");dist[s.length]++;for(const a of [false,true])for(const b of [false,true]){ok(evalTemplate(s,a,b)===expected(t,a,b),"truth table");truthChecks++;}
  const p=projectedAudit(t,s);projected.projected_implicates+=p.implicates;projected.maximum_resolution_nodes=Math.max(projected.maximum_resolution_nodes,p.maxNodes);projected.maximum_closure_clauses=Math.max(projected.maximum_closure_clauses,p.closure);projected.proper_subclause_witnesses+=p.proper;}

// Independently exhaust semantic depth-two composition.  Signal values, not
// Python gate records, are used here.
let nested=0;
for(let f=0;f<16;f++)for(let g=0;g<16;g++)for(const s of ["a","~a","b","~b","z","~z"])for(const t of ["a","~a","b","~b","z","~z"]){
  for(const a of [false,true])for(const b of [false,true]){
    const z=expected(f,a,b);const val=x=>x==="a"?a:x==="~a"?!a:x==="b"?b:x==="~b"?!b:x==="z"?z:!z;
    const want=expected(g,val(s),val(t));
    // Substitute the two actual input values into g's independently synthesized template.
    ok(evalTemplate(templates.get(g),val(s),val(t))===want,"nested composition");nested++;
  }
}
const raw=JSON.parse(fs.readFileSync(rawPath,"utf8"));
ok(raw.status==="PASS","raw status");ok(raw.function_universe===16,"universe");ok(raw.reachable_function_sets_bfs===states,"BFS state count");
ok(raw.maximum_signed_and2_gates===3,"max three");ok(JSON.stringify(raw.gate_count_distribution)===JSON.stringify(dist),"distribution");
ok(raw.abstract_truth_table_checks===truthChecks,"truth count");ok(raw.nested_reconvergent_audit.valuation_checks===nested,"nested count");
for(const [k,v] of Object.entries(projected))ok(raw.projected_old_facet_resolution_audit[k]===v,`projected facet audit ${k}`);
ok(raw.source_controls.sat_a_or_b_projected_models===3,"SAT control");ok(raw.source_controls.unsat_a_and_not_a_projected_models===0,"UNSAT control");
for(const v of Object.values(raw.malformed_controls))ok(v==="REJECTED","malformed rejected");
const result={artifact:"REFEREE371-independent",status:"PASS",assertions,function_universe:16,reachable_function_sets_bfs:states,
  gate_count_distribution:dist,maximum_signed_and2_gates:3,abstract_truth_table_checks:truthChecks,nested_valuation_checks:nested,
  projected_old_facet_resolution_audit:projected,
  resource_ledger:{construction_search_seconds:Number(((performance.now()-started)/1000).toFixed(6)),rss_bytes:process.memoryUsage().rss,
    logical_xor_trace:"not used",offline_diagnostic:true}};
fs.writeFileSync(outPath,JSON.stringify(result,null,2)+"\n");console.log(JSON.stringify(result,null,2));
