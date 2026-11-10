"use strict";
// LSPV-1/557: alternate prism-family reproduction of prior LSPV-3/551-553.
// Run in j15marti/pnp root with Node >=18. NOT the full historical checker.
const fs=require("fs"),path=require("path"),vm=require("vm"),cp=require("child_process"),os=require("os"),crypto=require("crypto");
const root=path.resolve(__dirname,"../..");
const files=["experiments/arc/lspv2_341_mixed_tseitin_min_dag.js","experiments/arc/lspv2_341_independent_verify.js","results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json"];
const pins=["4081022e8a3841d79f751a3d3a7a10decbb026da","fcb7d4ced8f922de14c0bda16263a8cc7853e8e0","706947c767361e7c979b8208677eb983d33838f4"];
const bodies=files.map(x=>fs.readFileSync(path.join(root,x),"utf8"));
function sha(s){return crypto.createHash("sha1").update("blob "+Buffer.byteLength(s)+"\0").update(s).digest("hex");}
bodies.forEach((s,i)=>{if(sha(s)!==pins[i])throw Error("wrong blob "+files[i]);});
const seed=JSON.parse(bodies[2]);
function graph(k){
 if(!Number.isSafeInteger(k)||k<3||k>10000)throw Error("k range");
 const e=[[0,2],[0,3],[1,2],[1,3],[2,3],[1,4]],t=5,b=5+k,s=5+2*k;
 for(let i=0;i<k;i++){if(i)e.push([t+i,t+(i+1)%k]);e.push([b+i,b+(i+1)%k],[t+i,b+i]);}
 e.push([t,s],[t+1,s],[4,s]);
 return {name:"PRISM_ALTERNATE_"+k,n:2*k+6,edges:[...e.slice(0,12),[0,4],...e.slice(12)]};
}
function forge(k){
 const key="const fixtures=graphs().map(fixture);";
 if(!bodies[0].includes(key))throw Error("producer entry changed");
 const ctx={__G:[graph(k)],console:{log(){}}};
 vm.runInNewContext(bodies[0].replace(key,"const fixtures=__G.map(fixture);")+"\nglobalThis.out=data;",ctx,{timeout:60000});
 const f=JSON.parse(JSON.stringify(ctx.out.fixtures[0]));
 const lit=[[1,2,13],[1,2,-13],[-1,-2,13],[-1,-2,-13]],pattern=[0,4,3,7];
 for(let j=0;j<4;j++){f.clauses[j].literals=lit[j];f.clauses[j].pattern=pattern[j];}
 f.charges[0]="1";f.proof[0].table=238;f.proof[1].table=230;
 f.proof[2].support="012";f.proof[2].table=102;
 for(const d of f.deleted)d.assignment=null;
 f.properties.essential=0;return f;
}
function packet(f){
 return {version:seed.version,definition:seed.definition,fixtures:[seed.fixtures[0],f],
 summary:[seed.summary[0],{name:f.graph.name,vertices:f.graph.n,variables:f.properties.variables,clauses:f.properties.sourceClauses,essential:0,inferences:f.proof.length,predictedMinimum:null,allEssential:false}]};
}
function sat(cl,a){return cl.literals.some(l=>l>0?a[Math.abs(l)-1]===1:a[Math.abs(l)-1]===0);}
function witness(f){
 const a=Array(f.graph.edges.length).fill(0);for(const e of [0,2,5,12])a[e]=1;
 if(!f.clauses.every(c=>sat(c,a)))throw Error("SAT witness failed");return a.join("");
}
function countSmall(f){
 const E=f.graph.edges.length;if(E!==18)throw Error("only 18-bit brute force");
 let count=0;
 for(let v=0;v<(1<<E);v++){
  let okay=true;
  for(const c of f.clauses){
   let valid=false;
   for(const l of c.literals){let b=(v>>(Math.abs(l)-1))&1;if(l>0?b===1:b===0){valid=true;break;}}
   if(!valid){okay=false;break;}
  }
  if(okay)count++;
 }
 return count;
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"lspv1-557-"));
function run(pkt){
 const dest=path.join(tmp,"packet.json");
 fs.writeFileSync(dest,JSON.stringify(pkt));
 const r=cp.spawnSync(process.execPath,[path.join(root,files[1]),dest],{encoding:"utf8",timeout:120000,maxBuffer:30000000});
 if(r.error)throw r.error;
 if(r.status===0)return {accept:true,checks:JSON.parse(r.stdout).checks};
 return {accept:false,error:(r.stderr||r.stdout).trim().split("\n").slice(-1)[0]};
}
const results=[];
try {
 for(const k of [3,4,5,8,12]){
  const f=forge(k),a=witness(f),p=packet(f),positive=run(p);
  if(!positive.accept)throw Error("native rejection k="+k);
  const changes=[
   ["numeric_charge",x=>x.fixtures[1].charges[0]=1],
   ["typed_support",x=>x.fixtures[1].proof[2].support=[0,1,12]],
   ["bad_table",x=>x.fixtures[1].proof[2].table=103],
   ["bad_sink",x=>x.fixtures[1].proof.at(-1).row.rhs=0]
  ];
  const controls=changes.map(([name,change])=>{let x=JSON.parse(JSON.stringify(p));change(x);return {name,...run(x)};});
  if(controls.some(x=>x.accept))throw Error("hostile control accepted k="+k);
  results.push({k,V:f.graph.n,E:f.graph.edges.length,m:f.clauses.length,q:f.proof.length,SATWitness:a,checker:positive,controls});
 }
 const models=countSmall(forge(3));if(models!==64)throw Error("model count "+models);
 const output={id:"LSPV1/557",scope:"independent alternative family reproducing prior LSPV-3/551-553; incomplete original fixture checker only",sourceBlobs:files.map((x,i)=>({path:x,sha:pins[i]})),tests:results,exhaustiveK3Models:models,modelCountFormula:"2^(k+3)",P2_D1:"OPEN",P2_C3:"OPEN",P2_B1:"OPEN",P2_B2:"OPEN",P_vs_NP:"OPEN"};
 if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(output,null,2)+"\n");
 console.log(JSON.stringify(output,null,2));
} finally {fs.rmSync(tmp,{recursive:true,force:true});}
