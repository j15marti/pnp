#!/usr/bin/env node
// LSPV-3/423: independent proof replay and exhaustive affine AND3 adapter audit.
// Usage: node experiments/arc/lspv3_423_independent.mjs results/raw/arc/2026-11-05_0624_LSPV3_AFFINE_PARENT_ADAPTER423_raw.json
const fs=require("fs"), assert=require("assert"), crypto=require("crypto");
const p=process.argv[2]||"results/raw/arc/2026-11-05_0624_LSPV3_AFFINE_PARENT_ADAPTER423_raw.json";
const data=JSON.parse(fs.readFileSync(p,"utf8"));
const input=Buffer.from(data.native.raw_source_b64,"base64");
const exact=Buffer.from("p cnf 3 5\n1 2 0\n1 -2 0\n-2 3 0\n-2 -3 0\n-1 2 0\n");
let checks=0;function ok(b,msg){checks++;assert(b,msg);}
ok(input.equals(exact),"raw original source changed");
ok(crypto.createHash("sha256").update(input).digest("hex")===data.source_sha256,"source digest");
ok(input.toString("base64")===data.native.raw_source_b64,"raw source encoding");
const clauses=input.toString("ascii").trimEnd().split("\n").slice(1).map(x=>{
 const a=x.split(" ").map(Number);ok(a.pop()===0,"bad DIMACS 0");return a;
});
function envs(ids){return Array.from({length:2**ids.length},(_,z)=>Object.fromEntries(ids.map((v,i)=>[v,(z>>i)&1])));}
function supp(x){if(x.type==="clause")return [...new Set(x.clause.map(Math.abs))];return x.type==="affine"?x.mask:x.support;}
function evalR(x,e){
 if(x.type==="clause")return Number(x.clause.some(l=>e[Math.abs(l)]===Number(l>0)));
 if(x.type==="affine")return Number(x.mask.reduce((a,v)=>a^e[v],0)===x.rhs);
 if(x.type==="factor")return x.truth[x.support.reduce((a,v,j)=>a+(e[v]<<j),0)];
 throw Error("untyped relation");
}
function replay(d,allowNativeAffine){
 ok(d.raw_source_b64===data.native.raw_source_b64,"external source bytes differ");
 ok(d.raw_sha256===data.source_sha256,"source hash");
 const view=new Map();
 clauses.forEach((c,i)=>view.set("s"+i,{type:"clause",clause:c}));
 function get(r,i){const key="src" in r?"s"+r.src:"n"+r.node+"/"+r.view;
  if("node" in r)ok(Number.isInteger(r.node)&&r.node<i,"forward dependency");
  ok(view.has(key),"unavailable reference "+key);return view.get(key);
 }
 for(let i=0;i<d.nodes.length;i++){
  const n=d.nodes[i];ok(n.id===i,"node id");
  if(n.rule==="AND3"){
   const a=get(n.left,i),b=get(n.right,i);
   if(!allowNativeAffine)ok(a.type!=="affine"&&b.type!=="affine","CANON2 excludes affine AND3 parent");
   const s=[...new Set([...supp(a),...supp(b)])].sort((a,b)=>a-b);
   ok(s.length<=3&&s.every(v=>v<=3),"AND3 out of local support");
   ok(JSON.stringify(s)===JSON.stringify(n.factor.support),"AND3 factor support");
   const t=envs(s).map(e=>evalR(a,e)&evalR(b,e));
   ok(JSON.stringify(t)===JSON.stringify(n.factor.truth),"AND3 truth");
   view.set("n"+i+"/factor",n.factor);
   if(n.affine){for(const e of envs(s))ok(evalR(n.affine,e)===evalR(n.factor,e),"false annotation");
    view.set("n"+i+"/affine",n.affine);}
  }else if(n.rule==="GF2"){
   const a=get(n.left,i),b=get(n.right,i);ok(a.type==="affine"&&b.type==="affine","GF2 parents");
   const m=[...new Set([...a.mask,...b.mask])].filter(v=>a.mask.includes(v)!==b.mask.includes(v)).sort((a,b)=>a-b);
   ok(JSON.stringify(m)===JSON.stringify(n.affine.mask)&&n.affine.rhs===(a.rhs^b.rhs),"GF2 sum");
   view.set("n"+i+"/affine",n.affine);
  }else if(n.rule==="LOCAL"){
   const a=get(n.parent,i),b=n.out;
   const s=[...new Set([...supp(a),...supp(b)])];
   ok(s.length<=3&&(b.type==="factor"||b.type==="clause"),"LOCAL support");
   for(const e of envs(s))ok(!evalR(a,e)||evalR(b,e),"LOCAL implication");
   view.set("n"+i+"/"+b.type,b);
  }else throw Error("unsupported rule "+n.rule);
 }
 const root=get(d.final,d.nodes.length);
 ok(root.type==="factor"&&root.truth.every(x=>x===0),"no contradiction");
}
replay(data.native,true);replay(data.compiled,false);
let rejected=false;
try{replay(data.native,false);}catch(e){rejected=String(e).includes("CANON2 excludes affine AND3 parent");}
ok(rejected,"CANON2 unexpectedly accepts affine-parent AND3");
const origAssignments=envs([1,2,3]);
ok(origAssignments.filter(e=>clauses.every(c=>evalR({type:"clause",clause:c},e))).length===0,"UNSAT");
ok(origAssignments.filter(e=>clauses.slice(0,-1).every(c=>evalR({type:"clause",clause:c},e))).length===2,"SAT deletion");
let comparisons=0;
for(let maskbits=0;maskbits<8;maskbits++)for(let rhs=0;rhs<2;rhs++){
 const mask=[1,2,3].filter((_,i)=>(maskbits>>i)&1);
 const row={type:"affine",mask,rhs};
 const factor={type:"factor",support:mask,truth:envs(mask).map(e=>evalR(row,e))};
 for(let table=0;table<256;table++){
  const other={type:"factor",support:[1,2,3],truth:Array.from({length:8},(_,i)=>(table>>i)&1)};
  for(const e of origAssignments){
   ok(evalR(row,e)===evalR(factor,e),"adapter mismatch");
   ok((evalR(row,e)&evalR(other,e))===(evalR(factor,e)&evalR(other,e)),"AND3 mismatch");
   comparisons+=2;
  }
 }
}
for(const [kind,change] of [
 ["source",d=>{d.raw_source_b64=Buffer.from("p cnf 3 5\n2 1 0\n1 -2 0\n-2 3 0\n-2 -3 0\n-1 2 0\n").toString("base64");}],
 ["GF2",d=>{d.nodes[2].affine.rhs^=1;}],
 ["factor",d=>{d.nodes[0].factor.truth[1]=0;}],
 ["LOCAL",d=>{d.nodes[4].out.truth[1]=0;}],
 ["port",d=>{d.nodes[5].left={node:4,view:"affine"};}]
]){
 const d=JSON.parse(JSON.stringify(data.compiled));change(d);let bad=false;
 try{replay(d,false);}catch(e){bad=true;}
 ok(bad,"accepted corruption "+kind);
}
ok(comparisons===65536,"wrong exhaustive scope");
console.log(JSON.stringify({status:"PASS",native_nodes:5,adapted_nodes:6,source_bytes:input.length,boolean_comparisons:comparisons,checks,corruptions_rejected:5}));
