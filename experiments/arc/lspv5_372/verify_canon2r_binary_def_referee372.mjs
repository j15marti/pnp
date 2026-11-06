#!/usr/bin/env node
// Independent REFEREE372 replay. Imports no Python producer/checker code.
import fs from "node:fs";
import crypto from "node:crypto";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {performance} from "node:perf_hooks";

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"../../..");
const raw=JSON.parse(fs.readFileSync(path.join(root,"results/raw/arc/2026-11-05_1548_LSPV5_REFEREE372_raw.json"),"utf8"));
const certs=JSON.parse(fs.readFileSync(path.join(root,"results/raw/arc/2026-11-05_1548_LSPV5_REFEREE372_certificates.json"),"utf8"));
const outPath=path.join(root,"results/raw/arc/2026-11-05_1548_LSPV5_REFEREE372_independent.json");
const started=performance.now();let checks=0;
function ok(x,m){checks++;if(!x)throw new Error(m);}
const sortClause=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||+(x<0)-+(y<0));
const key=c=>JSON.stringify(c);
const sat=(c,e)=>c.some(l=>e.get(Math.abs(l))===Number(l>0));
function facets(a,b,z,t){const out=[];for(const av of [0,1])for(const bv of [0,1]){const zv=1-t[av|(bv<<1)];out.push(sortClause([av?-a:a,bv?-b:b,zv?-z:z]));}return out;}
function oriented(a,b,p){const ans=[];if(a.includes(p)&&b.includes(-p))ans.push(sortClause([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]));if(a.includes(-p)&&b.includes(p))ans.push(sortClause([...a.filter(x=>x!==-p),...b.filter(x=>x!==p)]));return ans;}
function canon(x){if(Array.isArray(x))return `[${x.map(canon).join(",")}]`;if(x&&typeof x==="object")return `{${Object.keys(x).sort().map(k=>JSON.stringify(k)+":"+canon(x[k])).join(",")}}`;return JSON.stringify(x);}
const sha=s=>crypto.createHash("sha256").update(s).digest("hex");
function refKey(r){return "src" in r?`s:${r.src}:clause`:`n:${r.node}:${r.view}${"facet" in r?":"+r.facet:""}`;}
function checkProof(doc){
  ok(doc.format==="Rmix341-CANON2","format");ok(doc.source_sha256===sha(canon(doc.source)),"source hash");
  const views=new Map();doc.source.clauses.forEach((c,i)=>views.set(`s:${i}:clause`,c));let next=doc.source.nvars+1,maxvar=doc.source.nvars;
  for(let i=0;i<doc.nodes.length;i++){const n=doc.nodes[i];ok(n.id===i,"id");
    if(n.rule==="DEF"){ok(n.var===next++&&n.inputs.length===2,"fresh DEF");ok(n.inputs.every(x=>x>=1&&x<n.var),"DEF inputs");ok(n.truth.length===4&&n.truth.every(x=>x===0||x===1),"truth");maxvar=n.var;facets(n.inputs[0],n.inputs[1],n.var,n.truth).forEach((c,j)=>views.set(`n:${i}:clause:${j}`,c));}
    else if(n.rule==="RES"){const a=views.get(refKey(n.left)),b=views.get(refKey(n.right));ok(a!==undefined&&b!==undefined,"refs");ok(n.pivot>=1&&n.pivot<=maxvar,"pivot");ok(oriented(a,b,n.pivot).some(c=>key(c)===key(n.clause)),"resolvent");views.set(`n:${i}:clause`,n.clause);}
    else throw new Error("unexpected rule in local certificate");
  }
  const fin=views.get(refKey(doc.final));ok(Array.isArray(fin)&&fin.length===0,"empty final");return views;
}

const proofs=certs.normalized_and_only_proofs,wrappers=certs.normalized_and_only_wrappers;
ok(raw.status==="PASS","raw pass");ok(proofs.length===16&&wrappers.length===16,"sixteen normalized docs");ok(certs.old_arbitrary_gate_proofs.length===16,"sixteen old docs");let facetChecks=0,maxDefs=0,maxPaid=0,exactFacets=0;
for(let table=0;table<16;table++){
  const proof=proofs[table],wrapper=wrappers[table],summary=raw.summaries[table],views=checkProof(proof);checkProof(certs.old_arbitrary_gate_proofs[table]);
  ok(summary.table===table.toString(2).padStart(4,"0"),"table label");
  const bytes=Buffer.from(wrapper.source_raw_b64,"base64");ok(bytes.toString("base64")===wrapper.source_raw_b64,"canonical base64");ok(sha(bytes)===wrapper.source_raw_sha256,"raw hash");ok(canon(wrapper.proof)===canon(proof),"wrapped proof");
  // Replay the compiled network as a function on all four inputs.
  const defs=proof.nodes.filter(n=>n.rule==="DEF");maxDefs=Math.max(maxDefs,defs.length);maxPaid=Math.max(maxPaid,proof.nodes.length);
  for(const a of [0,1])for(const b of [0,1]){const e=new Map([[1,a],[2,b]]);for(const n of defs)e.set(n.var,n.truth[e.get(n.inputs[0])|(e.get(n.inputs[1])<<1)]);const output=defs.at(-1).var;const want=(table>>(2*a+b))&1;ok(e.get(output)===want,"compiled truth");}
  const oldTruth=[];for(const b of [0,1])for(const a of [0,1])oldTruth.push((table>>(2*a+b))&1);ok(key(oldTruth)===key(summary.old_truth),"row permutation");
  const output=defs.at(-1).var,oldFacets=facets(1,2,output,oldTruth);ok(summary.projected_old_facets.length===4,"four facets");
  for(const m of summary.projected_old_facets){const rep=views.get(refKey(m.reference));ok(key(oldFacets[m.old_facet])===key(m.target),"target facet");ok(key(rep)===key(m.representative),"representative ref");ok(rep.every(l=>m.target.includes(l)),"subclause");if(m.exact_target_in_strict_resolution_closure)exactFacets++;facetChecks++;}
}
ok(facetChecks===64&&raw.all_four_old_facets_checked===64,"facet total");ok(exactFacets===raw.exact_old_facets_in_strict_resolution_closure&&64-exactFacets===raw.subclause_only_old_facets,"exact/subclause split");ok(maxDefs===3&&raw.maximum_compiled_definitions===3,"max defs");ok(maxPaid===raw.validation_trace_paid_nodes_range[1],"max paid");for(const v of Object.values(raw.hostile_controls))ok(v.startsWith("REJECTED:"),"hostile rejected");
const result={artifact:"REFEREE372-independent",status:"PASS",checks,function_tables:16,projected_facets:facetChecks,exact_facets:exactFacets,subclause_only_facets:64-exactFacets,maximum_compiled_definitions:maxDefs,maximum_validation_paid_nodes:maxPaid,resource_ledger:{replay_seconds:Number(((performance.now()-started)/1000).toFixed(6)),rss_bytes:process.memoryUsage().rss,logical_xor_trace:"not used"}};
fs.writeFileSync(outPath,JSON.stringify(result,null,2)+"\n");console.log(JSON.stringify(result,null,2));
