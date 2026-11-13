"use strict";
// LSPV-1/609. Produces an accepted SAT-source packet for UNCHANGED
// archived /341 fixture checker. This is NOT a legal R_mix341 refutation.
// Run: node experiments/arc/lspv1_609_bridge_slice_forge.cjs [raw-ledger.json]
function construct(){
 const n=12,t=5,charges=Array.from({length:n},(_,i)=>+(i===0));
 let ed=[];
 for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)if(u!==0||v!==1)ed.push([u,v]);
 ed.push([0,4],[1,4]);
 for(let u=5;u<=7;u++)for(let v=8;v<=10;v++)if(u!==5||v!==8)ed.push([u,v]);
 ed.push([5,11],[8,11],[4,11]);
 function take(pair){let i=ed.findIndex(x=>x[0]===pair[0]&&x[1]===pair[1]);if(i<0)throw Error("edge");return ed.splice(i,1)[0];}
 const a=take([5,9]),b=take([5,10]),c=take([5,11]);
 ed=[a,b,...ed.splice(0,8),c,...ed];
 const E=ed.length,inc=Array.from({length:n},()=>[]);
 ed.forEach(([u,v],e)=>{inc[u].push(e);inc[v].push(e);});
 if(E!==18||inc[t].join(",")!=="0,1,10"||inc.some(x=>x.length!==3))throw Error("graph");
 const clauses=[];
 for(let v=0;v<n;v++)for(let m=0;m<8;m++){
  const b=[m&1,(m>>1)&1,(m>>2)&1];
  if(v===t?b[0]!==b[1]:(b[0]^b[1]^b[2])!==charges[v])
   clauses.push({id:"s"+clauses.length,vertex:v,pattern:m,literals:inc[v].map((e,j)=>b[j]?-(e+1):e+1)});
 }
 if(clauses.length!==48)throw Error("source length");
 const sat=(c,b)=>c.literals.some(l=>l>0?b[l-1]===1:b[-l-1]===0);
 const factors=new Map();
 for(let c of clauses){
  const sup=inc[c.vertex];let table=0;
  for(let m=0;m<8;m++){let bits=Array(E).fill(0);sup.forEach((e,j)=>bits[e]=(m>>j)&1);if(sat(c,bits))table|=1<<m;}
  factors.set(c.id,{support:sup,table,kind:"factor"});
 }
 const ev=(p,b)=>{let x=0;for(let j=0;j<p.support.length;j++)x|=(b[p.support[j]]??0)<<j;return(p.table>>x)&1;};
 const proof=[],rows=[];
 for(let v=0;v<n;v++){
  let left="s"+(4*v);
  for(let j=1;j<=3;j++){
   const right="s"+(4*v+j),A=factors.get(left),B=factors.get(right),sup=(v===t&&j===3)?"102":inc[v].slice();
   let table=0;
   for(let m=0;m<8;m++){let bits=Array(E).fill(0);for(let k=0;k<sup.length;k++)bits[sup[k]]=(m>>k)&1;
    if(ev(A,bits)&&ev(B,bits))table|=1<<m;}
   const id="d"+proof.length,p={id,kind:"factor",rule:"AND3",parents:[left,right],support:sup,table};
   if(j===3){const mask=inc[v].reduce((a,e)=>a|(1n<<BigInt(e)),0n);
    p.row={mask:"0x"+mask.toString(16),rhs:charges[v]};rows.push(id);}
   proof.push(p);factors.set(id,p);left=id;
  }
 }
 let prev=rows[0],mask=BigInt(factors.get(prev).row.mask),rhs=factors.get(prev).row.rhs;
 for(let v=1;v<n;v++){
  const right=rows[v],id="d"+proof.length,row=factors.get(right).row;
  mask^=BigInt(row.mask);rhs^=row.rhs;
  const p={id,kind:"affine",rule:"XOR",parents:[prev,right],row:{mask:"0x"+mask.toString(16),rhs}};
  proof.push(p);prev=id;
 }
 if(proof.length!==47||mask!==0n||rhs!==1)throw Error("sink");
 const deleted=clauses.map(c=>({sourceId:c.id,assignment:null}));
 let essential=0,models=0,witness=null;
 for(let x=0;x<(1<<E);x++){
  const bits=Array.from({length:E},(_,e)=>(x>>e)&1);let count=0,last=-1;
  for(let i=0;i<clauses.length;i++)if(!sat(clauses[i],bits)){count++;last=i;if(count>1)break;}
  if(count===0){models++;if(witness===null)witness=bits.join("");}
  if(count===1&&deleted[last].assignment===null){deleted[last].assignment=bits.join("");essential++;}
 }
 if(models!==64||essential!==39)throw Error("regression source");
 const packet={version:"LSPV1-609-SAT-FORGE",
   definition:"Archived /341 fixture parser, not the declared full R_mix341",
   fixtures:[{graph:{name:"BRIDGE_SUBDIV_K4_K33",n,edges:ed},
    charges:charges.map((x,i)=>i===t?String(x):x),clauses,proof,deleted,
    evenWitness:"0".repeat(E),properties:{variables:E,sourceClauses:48,inferences:47,
     essential,oddUnsat:false,evenSat:true,predictedMinimum:null}}],summary:[{}]};
 return {packet,models,witness,essential};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("node:fs"),os=require("node:os"),path=require("node:path"),
  cp=require("node:child_process"),assert=require("node:assert/strict"),
  crypto=require("node:crypto");
 const root=path.resolve(__dirname,"../.."),checker=path.join(root,"experiments/arc/lspv2_341_independent_verify.js");
 const cb=fs.readFileSync(checker),blob=b=>crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex");
 assert.equal(blob(cb),"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0");
 const made=construct(),clone=()=>JSON.parse(JSON.stringify(made.packet));
 const q=clone(),tests=[["accepted_sat",q,true]];
 const arr=clone();arr.fixtures[0].proof[17].support=[0,1,10];tests.push(["fixed_array_support",arr,false]);
 const num=clone();num.fixtures[0].charges[5]=0;tests.push(["fixed_numeric_charge",num,false]);
 const par=clone();par.fixtures[0].proof[17].parents[0]="MISSING";tests.push(["bad_parent",par,false]);
 const sink=clone();sink.fixtures[0].proof.at(-1).row.rhs=0;tests.push(["bad_sink",sink,false]);
 const src=clone();src.fixtures[0].clauses[20].literals[0]*=-1;tests.push(["bad_source",src,false]);
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"lspv1-609-")),runs=[];
 try{
  for(let [name,pkt,expected]of tests){
   const f=path.join(tmp,name+".json");fs.writeFileSync(f,JSON.stringify(pkt));
   const r=cp.spawnSync(process.execPath,[checker,f],{encoding:"utf8",timeout:30000,maxBuffer:2000000});
   assert.equal(r.status===0,expected,name+" "+r.stderr);
   runs.push({name,accepted:r.status===0,checks:r.status===0?JSON.parse(r.stdout).checks:null,
    error:r.status===0?null:(r.stderr.match(/Error: [^\r\n]*/)||[])[0]||"REJECT"});
  }
  const out={checker_blob:blob(cb),scope:"recovered /341 fixture checker only",native_os:true,
   model_count:made.models,witness:made.witness,essential:made.essential,
   signed_original_clauses:48,paid_nodes:47,runs};
  const json=JSON.stringify(out,null,2)+"\n";
  if(process.argv[2])fs.writeFileSync(process.argv[2],json);
  process.stdout.write(json);
 }finally{fs.rmSync(tmp,{recursive:true,force:true});}
}
