"use strict";
/* LSPV-2/538: pins unmodified historical 341 producer/checker, V8 replay, original signed Petersen controls.
   Run from repository root: node experiments/arc/lspv2_538_support_string_native.cjs [raw.json].
   This is NOT the complete historical R_mix341 verifier. */
const PIN={p:"4081022e8a3841d79f751a3d3a7a10decbb026da",v:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"};
const copy=o=>JSON.parse(JSON.stringify(o));
function audit(ptext,vtext){
 let out=[];new Function("console",ptext)({log:x=>out.push(x)});
 const pack=JSON.parse(out[0]),orig=pack.fixtures.find(x=>x.graph.name==="PETERSEN");
 if(!orig||orig.graph.edges.length!==15||orig.proof.length!==39)throw Error("Original fixture drift");
 const wrap=f=>({fixtures:[f],summary:[null]});
 function hist(o){
  let out=[];
  try{
    new Function("require","process","console",vtext)(
      ()=>({readFileSync:()=>JSON.stringify(o)}),
      {argv:["node","pinned341","packet.json"]},{log:x=>out.push(x)});
    const z=JSON.parse(out[0]);return {accepted:true,checks:z.checks,fixtures:z.cases.length};
  }catch(e){return {accepted:false,error:String(e).slice(0,150)};}
 }
 const base=hist(wrap(orig));if(!base.accepted||base.checks!==4347)throw Error("baseline drift");
 const f=copy(orig),node=f.proof.find(x=>x.id==="d2");
 if(JSON.stringify(node.support)!=="[0,2,12]"||node.table!==150||node.row.mask!=="0x1005")throw Error("node drift");
 const factor=new Map();
 for(const c of f.clauses){
  const support=c.literals.map(x=>Math.abs(x)-1);let table=0;
  for(let a=0;a<8;a++)if(c.literals.some(l=>((a>>support.indexOf(Math.abs(l)-1))&1)===(l>0?1:0)))table|=1<<a;
  factor.set(c.id,{support,table});
 }
 for(const x of f.proof){if(x.id==="d2")break;factor.set(x.id,x);}
 const value=(p,b)=>{let a=0;for(let j=0;j<p.support.length;j++)a|=((b[p.support[j]]||0)<<j);return(p.table>>a)&1;};
 node.support="012";let table=0;
 for(let a=0;a<8;a++){
  const b=Array(15).fill(0);for(let j=0;j<3;j++)b[node.support[j]]=(a>>j)&1;
  if(node.parents.every(id=>value(factor.get(id),b)))table|=1<<a;
 }
 if(table!==90)throw Error("expected table 90");node.table=table;
 const mutant=hist(wrap(f));if(!mutant.accepted||mutant.checks!==4347)throw Error("native rejected forged factor");
 const controls=[{id:"original",...base},{id:"string_support_forged_table",...mutant}];
 function neg(id,fn){
   const q=copy(f);fn(q);let r=hist(wrap(q));if(r.accepted)throw Error(id+" unexpectedly accepted");
   controls.push({id,...r});
 }
 neg("string_old_table",q=>q.proof.find(x=>x.id==="d2").table=150);
 neg("array_wrong_table",q=>q.proof.find(x=>x.id==="d2").support=[0,2,12]);
 neg("incorrect_substring",q=>q.proof.find(x=>x.id==="d2").support="021");
 neg("bad_row",q=>q.proof.find(x=>x.id==="d2").row.mask="0x1004");
 neg("bad_parent",q=>q.proof.find(x=>x.id==="d2").parents[0]="NOT_A_PARENT");
 neg("bad_signed_source",q=>q.clauses[0].literals[0]*=-1);
 neg("bad_sink",q=>q.proof.at(-1).row.rhs=0);
 const bad=[],sourceClause=f.clauses.find(c=>c.id==="s3");
 for(let a=0;a<16;a++){
  const b=Array(15).fill(0);[0,1,2,12].forEach((e,j)=>b[e]=(a>>j)&1);
  const premise=!!value(factor.get("d1"),b) && sourceClause.literals.some(l=>b[Math.abs(l)-1]===(l>0?1:0));
  const claimed=!!((node.table>>(b[0]+2*b[1]+4*b[2]))&1);
  if(premise!==claimed)bad.push({x0:b[0],x1:b[1],x2:b[2],x12:b[12],premise,claimed});
 }
 if(bad.length!==8||!bad.some(x=>x.x0===0&&x.x1===0&&x.x2===0&&x.x12===1&&x.premise&&!x.claimed))
   throw Error("original-variable semantic witness failed");
 const seven=hist(pack);if(!seven.accepted||seven.checks!==30714)throw Error("historical full packet drift");
 if(!Array.isArray(orig.proof[2].support)||Array.isArray(node.support))throw Error("strict reference type guard failed");
 return {id:"LSPV2-538",status:"PROVED/RESTRICTED checker-specific type-inference mismatch; COMPUTATIONAL original V8",
  sourceBlobs:PIN,originalSource:"unchanged PETERSEN original signed 3CNF; 15 vars, 40 clauses",
  originalPaidNodes:39,originalRuleUnits:"declared AND3/XOR unit charges",
  base,mutant,sevenFixtureCheck:seven,
  changedNode:{id:"d2",parents:["d1","s3"],trueUnion:[0,2,12],forgedSupport:"012",oldTable:150,forgedTable:90,unchangedRow:{mask:"0x1005",rhs:1}},
  semanticMismatches:bad,strictTypedReference:"reject non-array AND3 support; native accepts",
  controls,acceptedPacketBytes:JSON.stringify(wrap(f)),
  semantics:"The string '012' passes includes(0), includes(2), includes(12), but enumerates character indices 0,1,2; edge 12 stays zero",
  sourceProvenance:"only embedded original clauses authenticated, no external independent DIMACS binder",
  absentNativeRules:"RES, LOCAL-CONVERT, DEF, fresh/owner facets, branching, discharge, joins and other declared rules remain UNKNOWN",
  costPolarity:"39 distinct paid nodes unchanged; raw evidence bits and checker runtime distinct"};
}
if(typeof module!=="undefined"&&typeof require==="function"&&require.main===module){
 const fs=require("fs"),crypto=require("crypto");
 const paths={p:"experiments/arc/lspv2_341_mixed_tseitin_min_dag.js",v:"experiments/arc/lspv2_341_independent_verify.js"};
 const txt={};
 for(const k of Object.keys(paths)){
  txt[k]=fs.readFileSync(paths[k],"utf8");
  const b=Buffer.from(txt[k],"utf8");
  const sha=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+b.length+"\0"),b])).digest("hex");
  if(sha!==PIN[k])throw Error("historical Git blob mismatch "+k);
 }
 const out=audit(txt.p,txt.v);
 out.acceptedPacketSHA256=crypto.createHash("sha256").update(out.acceptedPacketBytes).digest("hex");
 const raw=JSON.stringify(out,null,2)+"\n";
 if(process.argv[2])fs.writeFileSync(process.argv[2],raw);else process.stdout.write(raw);
}
