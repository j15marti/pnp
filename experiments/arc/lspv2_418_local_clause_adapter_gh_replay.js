#!/usr/bin/env node
// LSPV-2/418 restricted CANON2R replay. Run: node experiments/arc/lspv2_418_local_clause_adapter_gh_replay.js
// Independent from the Python proof producer. Does NOT implement all R_mix341 rules.
"use strict";
const fs=require("fs"),crypto=require("crypto");
const raw=JSON.parse(fs.readFileSync("results/raw/arc/2026-11-05_0712_LSPV2_LOCAL_CLAUSE_PARENT418_raw.json","utf8"));
const assert=(v,m)=>{if(!v)throw Error(m)};
const stable=x=>Array.isArray(x)?"["+x.map(stable).join(",")+"]":x&&typeof x==="object"?"{"+Object.keys(x).sort().map(k=>JSON.stringify(k)+":"+stable(x[k])).join(",")+"}":JSON.stringify(x);
const hash=x=>crypto.createHash("sha256").update(x).digest("hex");
const evalRel=(r,v)=>r.kind==="clause"?+r.clause.some(l=>v[Math.abs(l)]===(l>0?1:0)):r.truth[r.support.reduce((a,b,i)=>a+(v[b]<<i),0)];
const support=r=>r.kind==="clause"?r.clause.map(Math.abs):r.support;
let checks=0;
function verify(d,strict){
  assert(hash(stable(d.source))===d.source_sha256,"source hash"); checks++;
  assert(d.format==="Rmix341-CANON2","format"); checks++;
  let table=new Map(d.source.clauses.map((c,i)=>["s"+i,{kind:"clause",clause:c}]));
  function get(ref,i){let k="src" in ref?"s"+ref.src:"n"+ref.node;if("node" in ref)assert(Number.isInteger(ref.node)&&ref.node<i,"acyclic");assert(table.has(k),"ref");checks++;return table.get(k);}
  let rows=0;
  for(let i=0;i<d.nodes.length;i++){
    let n=d.nodes[i], parents=[],out;assert(n.id===i,"node order");
    if(n.rule==="AND3"){parents=[get(n.left,i),get(n.right,i)];out={kind:"factor",...n.factor};
      const s=[...new Set(parents.flatMap(support))].sort((a,b)=>a-b);
      assert(JSON.stringify(s)===JSON.stringify(out.support),"factor support");
    }else if(n.rule==="LOCAL"){parents=[get(n.parent,i)];if(strict)assert(parents[0].kind!=="clause","strict LOCAL parent");out={kind:"factor",...n.out.factor};}
    else throw Error("unexpected rule");
    const s=[...new Set([...parents.flatMap(support),...support(out)])].sort((a,b)=>a-b);
    assert(s.length<=3&&s.every(x=>x>=1&&x<=d.source.nvars),"original support");
    assert(out.truth.length===(1<<out.support.length),"factor length");
    for(let z=0;z<(1<<s.length);z++){
      const v={};s.forEach((x,j)=>v[x]=z>>j&1);
      const target=evalRel(out,v), prem=n.rule==="AND3"?evalRel(parents[0],v)&evalRel(parents[1],v):evalRel(parents[0],v);
      assert(n.rule==="AND3"?target===prem:(!prem||target===1),"semantic rule");
      rows++; checks++;
    }
    table.set("n"+i,out);
  }
  const f=get(d.final,d.nodes.length);assert(f.kind==="factor"&&f.truth.every(x=>x===0),"contradiction");
  return {nodes:d.nodes.length,truth_rows:rows,bytes:Buffer.byteLength(stable(d))};
}
assert(hash(raw.raw_external_source)===raw.raw_external_sha256,"external raw SHA");
let strictReject=false;try{verify(raw.permissive,true)}catch(e){strictReject=String(e).includes("strict LOCAL parent")}
assert(strictReject,"permissive proof must violate strict LOCAL typing");
const p=verify(raw.permissive,false),s=verify(raw.repaired,true);
assert(p.nodes===3&&s.nodes===4&&p.truth_rows===10&&s.truth_rows===12,"verified counts");
assert(p.bytes===598&&s.bytes===728,"canonical evidence lengths");
assert(stable(raw.repaired.nodes[0].left)===stable(raw.repaired.nodes[0].right),"paid self-conjunction");
let srcModels=0,satControl=0;
for(let x=0;x<2;x++)for(let y=0;y<2;y++){
  const v={1:x,2:y},holds=cs=>cs.every(c=>evalRel({kind:"clause",clause:c},v));
  if(holds(raw.repaired.source.clauses))srcModels++;
  if(holds([[1],[-1,2],[2]]))satControl++;
}
assert(srcModels===0&&satControl===1,"both-label control");
for(const edit of [d=>d.nodes[0].factor.truth=[1,1],d=>d.nodes[1].out.factor.truth=[0,0],d=>d.nodes[2].factor.truth=[0,0,1,1],d=>d.nodes[3].factor.truth=[0,0,0,1],d=>d.nodes[1].parent={node:1,view:"factor"}]){
 const d=JSON.parse(JSON.stringify(raw.repaired));edit(d);let fails=false;
 try{verify(d,true)}catch(e){fails=true}assert(fails,"corrupt proof accepted");
}
console.log(JSON.stringify({status:"PASS",permissive:p,strict:s,source_unsat_models:srcModels,sat_control_models:satControl,mutations_rejected:5,assertion_groups:checks,B3:"OPEN"}));
