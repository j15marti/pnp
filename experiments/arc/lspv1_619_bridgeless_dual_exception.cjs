"use strict";
/*
 LSPV-1/619: bridgeless two-exception checker-accepted SAT source.
 EXACT ORIGINAL CHECKER REQUIRED at experiments/arc/lspv2_341_independent_verify.js
 Pin: Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0.
 This fixture is NOT a mathematically valid refutation and NOT historical full R_mix341.
 Run: node experiments/arc/lspv1_619_bridgeless_dual_exception.cjs [raw-results.json]
*/
function makePacket() {
 const edges=[
 [0,1],[5,0],[8,9],[9,10],[1,2],[2,3],[3,4],[4,5],
 [6,7],[7,8],[0,6],[10,11],[3,9],[11,6],[1,7],[2,8],[4,10],[5,11]
 ];
 const V=12,E=edges.length,t=0,u=9, q=Array(V).fill(0);
 q[1]=1;
 const inc=Array.from({length:V},()=>[]);
 edges.forEach(([a,b],e)=>{inc[a].push(e);inc[b].push(e)});
 if(inc[t].join()!=[0,1,10].join()||inc[u].join()!=[2,3,12].join())throw Error("string-support edge indexing invalid");
 const charges=q.slice();charges[t]="0";charges[u]="0";
 const clauses=[];
 for(let v=0;v<V;v++)for(let m=0;m<8;m++) {
  const b=[m&1,(m>>1)&1,(m>>2)&1];
  const parity=(v===t||v===u)?b[0]^b[1]:b[0]^b[1]^b[2];
  if(parity!==q[v])clauses.push({id:"s"+clauses.length,vertex:v,literals:inc[v].map((e,j)=>b[j]?-(e+1):e+1)});
 }
 if(clauses.length!==4*V)throw Error("source length");
 const clauseSat=(c,bits)=>c.literals.some(x=>x>0?bits[x-1]===1:bits[-x-1]===0);
 const factors=new Map();
 for(const c of clauses){
  const sup=inc[c.vertex];let tab=0;
  for(let m=0;m<8;m++){
   const bits=Array(E).fill(0);sup.forEach((e,j)=>bits[e]=(m>>j)&1);
   if(clauseSat(c,bits))tab|=1<<m;
  }
  factors.set(c.id,{kind:"factor",support:sup,table:tab});
 }
 const evalFactor=(f,bits)=>{
  let index=0;for(let j=0;j<f.support.length;j++)index|=Number(bits[f.support[j]])<<j;
  return (f.table>>index)&1;
 };
 const proof=[],rows=[];
 for(let v=0;v<V;v++){
  let left="s"+4*v;
  for(let j=1;j<=3;j++){
   const right="s"+(4*v+j),a=factors.get(left),b=factors.get(right);
   const support=(j===3&&v===t)?"102":(j===3&&v===u)?"123":inc[v].slice();
   let table=0;
   for(let m=0;m<8;m++){
    const bits=Array(E).fill(0);
    for(let i=0;i<support.length;i++)bits[support[i]]=(m>>i)&1;
    if(evalFactor(a,bits)&&evalFactor(b,bits))table|=1<<m;
   }
   const p={id:"d"+proof.length,kind:"factor",rule:"AND3",parents:[left,right],support,table};
   if(j===3){
    let mask=0n;for(const e of inc[v])mask|=1n<<BigInt(e);
    p.row={mask:"0x"+mask.toString(16),rhs:q[v]};
    rows.push(p.id);
   }
   proof.push(p);factors.set(p.id,p);left=p.id;
  }
 }
 let prev=rows[0],mask=BigInt(factors.get(prev).row.mask),rhs=factors.get(prev).row.rhs;
 for(let v=1;v<V;v++){
  const id="d"+proof.length,right=rows[v],r=factors.get(right).row;
  mask^=BigInt(r.mask);rhs^=r.rhs;
  proof.push({id,kind:"affine",rule:"XOR",parents:[prev,right],row:{mask:"0x"+mask.toString(16),rhs}});
  prev=id;
 }
 if(proof.length!==4*V-1||mask!==0n||rhs!==1)throw Error("terminal");
 const deleted=clauses.map(c=>({sourceId:c.id,assignment:null}));
 let satCount=0,satWitness=null,oneViolationCounts=Array(clauses.length).fill(0);
 for(let value=0;value<(1<<E);value++){
  const bits=Array.from({length:E},(_,e)=>(value>>e)&1);
  let bad=-1,nBad=0;
  for(let i=0;i<clauses.length;i++)if(!clauseSat(clauses[i],bits)){nBad++;bad=i;if(nBad>1)break;}
  if(nBad===0){satCount++;if(satWitness===null)satWitness=bits.join("");}
  else if(nBad===1){oneViolationCounts[bad]++;if(deleted[bad].assignment===null)deleted[bad].assignment=bits.join("");}
 }
 const essential=deleted.filter(d=>d.assignment!==null).length;
 if(satCount!==64||essential!==48||oneViolationCounts.some(c=>c!==16))throw Error("SAT/essentiality spectrum mismatch");
 const packet={version:"LSPV1-619-BRIDGELESS-DUAL-DEFECT",fixtures:[{
   graph:{name:"BRIDGELESS_PRISM12_DUAL_EXCEPTION",n:V,edges},
   charges,clauses,proof,deleted,evenWitness:"0".repeat(E),properties:{essential}
 }],summary:[{}]};
 return {packet,meta:{V,E,sourceClauses:clauses.length,paidNodes:proof.length,
  satCount,satWitness,essential,oneViolationMin:Math.min(...oneViolationCounts),
  oneViolationMax:Math.max(...oneViolationCounts),
  stringSupports:proof.filter(p=>typeof p.support==="string").map(p=>({id:p.id,support:p.support})),
  sourceChargeTypes:charges.map((c,v)=>({v,type:typeof c,value:c})).filter(x=>x.type!=="number")}};
}
function adversaries(packet){
 const cp=()=>JSON.parse(JSON.stringify(packet));
 const tests=[];
 let p=cp();p.fixtures[0].charges[0]=0;tests.push(["repair_charge_t",p,false]);
 p=cp();p.fixtures[0].charges[9]=0;tests.push(["repair_charge_u",p,false]);
 p=cp();p.fixtures[0].proof[2].support=[0,1,10];tests.push(["repair_support_t",p,false]);
 p=cp();p.fixtures[0].proof[29].support=[2,3,12];tests.push(["repair_support_u",p,false]);
 p=cp();p.fixtures[0].proof[2].parents[0]="missing";tests.push(["bad_parent",p,false]);
 p=cp();p.fixtures[0].proof.at(-1).row.rhs=0;tests.push(["bad_terminal",p,false]);
 p=cp();p.fixtures[0].deleted[0].assignment="0".repeat(18);tests.push(["bad_deletion_witness",p,false]);
 p=cp();p.fixtures[0].clauses[0].literals[0]=9999;tests.push(["bad_source_literal",p,false]);
 p=cp();p.fixtures[0].evenWitness="1".repeat(18);tests.push(["bad_even_witness",p,false]);
 return tests;
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs"),os=require("node:os"),path=require("node:path"),
  crypto=require("node:crypto"),cp=require("node:child_process"),assert=require("node:assert/strict");
 const checker=path.resolve(__dirname,"lspv2_341_independent_verify.js");
 const src=fs.readFileSync(checker);
 const blob=crypto.createHash("sha1").update("blob "+src.length+"\0").update(src).digest("hex");
 assert.equal(blob,"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0","original checker changed");
 const {packet,meta}=makePacket(),dir=fs.mkdtempSync(path.join(os.tmpdir(),"lspv1-619-"));
 const tests=[["bridgeless_sat_false_acceptance",packet,true],...adversaries(packet)],results=[];
 try{
  for(const [name,input,want] of tests){
   const file=path.join(dir,name+".json");fs.writeFileSync(file,JSON.stringify(input));
   const r=cp.spawnSync(process.execPath,[checker,file],{encoding:"utf8",timeout:30000,maxBuffer:5_000_000});
   const accepted=r.status===0;
   assert.equal(accepted,want,name+" unexpected native verifier verdict: "+r.stderr);
   results.push({name,accepted,checks:accepted?JSON.parse(r.stdout).checks:null,
      rejection:accepted?null:(r.stderr.match(/Error: [^\r\n]*/)||[])[0]||"REJECT"});
  }
  const output={run:"LSPV-1/619",model:"archived /341 SOURCE/AND3/XOR fixture, not historical R_mix341",
    checkerBlob:blob,nativeOS:true,exhaustiveEdgeAssignments:1<<18,meta,
    packetSHA256:crypto.createHash("sha256").update(JSON.stringify(packet)).digest("hex"),
    packetBytes:Buffer.byteLength(JSON.stringify(packet)),tests:results};
  if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(output,null,2)+"\n");
  process.stdout.write(JSON.stringify(output,null,2)+"\n");
 }finally{fs.rmSync(dir,{recursive:true,force:true})}
}
if(typeof module!=="undefined")module.exports={makePacket,adversaries};
