#!/usr/bin/env node
"use strict";
/* LSPV-4/522. Run from j15marti/pnp repository root:
   node experiments/arc/lspv4_522_native_evidence_streaming_audit.cjs [out.json]
   Requires Node >=18. Exercises the original pinned /341 producer/verifier
   via V8 with only the readFileSync/argv/console interface shimmed.
   The separate streaming recognizer handles only a FIXED K4 literal-token slice.
*/
const fs=require("fs"),crypto=require("crypto");
const P="experiments/arc/lspv2_341_mixed_tseitin_min_dag.js";
const V="experiments/arc/lspv2_341_independent_verify.js";
const PIN={P:"4081022e8a3841d79f751a3d3a7a10decbb026da",
 V:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"};
function gitBlob(s){const b=Buffer.from(s,"utf8");return crypto.createHash("sha1")
 .update(Buffer.concat([Buffer.from("blob "+b.length+"\0"),b])).digest("hex");}
function audit(producerText,checkerText){
 let assertions=0,calls=0;const requireTrue=(x,msg)=>{assertions++;if(!x)throw Error("FAIL "+msg)};
 const logs=[];new Function("console",producerText)({log:x=>logs.push(x)});
 const original=JSON.parse(logs[0]),f=original.fixtures[0],clone=x=>JSON.parse(JSON.stringify(x));
 const base={version:original.version,definition:original.definition,
  fixtures:[f],summary:[original.summary[0]]};
 function runNative(o){
  const payload=JSON.stringify(o),out=[];calls++;
  try{new Function("require","process","console",checkerText)(
   mod=>{if(mod!=="fs")throw Error("unexpected require");return {readFileSync:()=>payload}},
   {argv:["node","original_native_checker","packet.json"]},{log:s=>out.push(s)});
   return {accept:true,checks:JSON.parse(out[0]).checks,bytes:payload.length};
  }catch(e){return {accept:false,bytes:payload.length,diagnostic:String(e.message).slice(0,120)}}
 }
 const first=runNative(base),paid=f.proof.filter(p=>p.rule==="AND3"||p.rule==="XOR");
 requireTrue(first.accept&&first.checks===1401&&paid.length===15&&f.clauses.length===16,"baseline native K4");
 requireTrue(new Set(paid.map(x=>x.id)).size===15,"paid node identities unique");
 // Stable byte-template with precisely ONE semantically active numeric literal token variable.
 const s0=clone(base);s0.fixtures[0].clauses[0].literals[0]="1";
 const full=JSON.stringify(s0),j=full.indexOf('"literals":["1"');
 requireTrue(j>=0,"first literal is positive 1");
 const t=full.indexOf('"1"',j),prefix=full.slice(0,t+1),suffix=full.slice(t+2);
 function streamingMatch(s){
  let i=0,reads=0;
  for(let j=0;j<prefix.length;j++){reads++;if(s[i++]!==prefix[j])return {ok:false,reads}}
  while(i<s.length&&s[i]==="0"){reads++;i++}
  reads++;if(s[i++]!=="1")return {ok:false,reads};
  for(let j=0;j<suffix.length;j++){reads++;if(s[i++]!==suffix[j])return {ok:false,reads}}
  return {ok:i===s.length,reads}
 }
 const rows=[];let sensitive=0;
 for(const k of [0,1,2,7,31,127,1023,4095]){
  const item=clone(base);item.fixtures[0].clauses[0].literals[0]="0".repeat(k)+"1";
  const v=runNative(item),s=JSON.stringify(item),r=streamingMatch(s);
  requireTrue(v.accept&&v.checks===first.checks,"original accepts "+k);
  requireTrue(r.ok&&r.reads===s.length,"single scan "+k);
  requireTrue(s===prefix+"0".repeat(k)+"1"+suffix,"fixed template "+k);
  const positions=k<=127?Array.from({length:k},(_,i)=>i):[0,Math.floor(k/2),k-1];
  for(const pos of positions){
   const bad=clone(item),x=bad.fixtures[0].clauses[0].literals[0];
   bad.fixtures[0].clauses[0].literals[0]=x.slice(0,pos)+"2"+x.slice(pos+1);
   requireTrue(!runNative(bad).accept&&!streamingMatch(JSON.stringify(bad)).ok,
      "0->2 corruption "+k+"/"+pos);sensitive++;
  }
  rows.push({k,bytes:s.length,deltaBytes:s.length-first.bytes,
    checkerAssertions:v.checks,streamedReads:r.reads,
    sensitivePositionsTested:positions.length,logicalPaid:paid.length});
 }
 // Separate mathematical DAG ownership/cost-partition test. No native CASE opcode claimed.
 const paidSeen=new Set(),part=[0,0],depth=new Map(f.clauses.map(c=>[c.id,0]));
 for(const p of paid){
  requireTrue(!paidSeen.has(p.id),"fresh paid ID");
  paidSeen.add(p.id);part[Number(p.id.slice(1))%2]++;
  depth.set(p.id,1+Math.max(...p.parents.map(id=>{
   requireTrue(depth.has(id),"topological source/parent");
   return depth.get(id)})));
 }
 requireTrue(paidSeen.size===15&&part[0]+part[1]===15,"split charge exactly once");
 const compatible=(local,consumer)=>Object.entries(local).every(([k,v])=>consumer[k]===v);
 requireTrue(compatible({}, {x:0})&&compatible({x:1},{x:1,y:0})
    &&!compatible({x:1},{x:0}),"compatible / incompatible scopes");
 const controls=[];
 for(const [name,change] of [
   ["AND3_FALSE_TABLE",o=>o.fixtures[0].proof[0].table^=1],
   ["XOR_FALSE_ROW",o=>o.fixtures[0].proof.find(p=>p.rule==="XOR").row.mask="0xFFFF"],
   ["BAD_PARENT",o=>o.fixtures[0].proof[0].parents[0]="no_source"],
   ["BAD_SOURCE",o=>o.fixtures[0].clauses[0].literals[0]=2]
 ]){const o=clone(base);change(o);const v=runNative(o);
    requireTrue(!v.accept,name);controls.push({name,diagnostic:v.diagnostic})}
 const extra=clone(base),duplicate=clone(extra.fixtures[0].proof[0]);
 duplicate.id="paid_duplicate_522";extra.fixtures[0].proof.splice(1,0,duplicate);
 const dupCheck=runNative(extra);requireTrue(!dupCheck.accept,"fixture q-length guard");
 return {experiment:"LSPV4/522 native-341 evidence-read vs native-work-space and DAG cost partition",
  statuses:["PROVED/RESTRICTED","COMPUTATIONAL"],
  scope:"Pinned original 341 SOURCE/AND3/XOR FIXTURE checker only, not the historical complete R_mix341",
  exactOriginalGitBlobSHAs:PIN,
  nativeExecution:"Original unchanged JavaScript bodies in V8, only Node CLI I/O shimmed",
  fixture:{name:f.graph.name,sourceClauses:16,chargedNodes:15,bytes:first.bytes,
    originalCheckerAssertions:first.checks,weightedSpan:depth.get(paid.at(-1).id)},
  streamingFiber:{regex:"FIXED_PREFIX (0*) 1 FIXED_SUFFIX",
    prefixBytes:prefix.length,suffixBytes:suffix.length,rows,sensitivePositions:sensitive,
    nativeTime:"Theta(B) on fixed regular slice, B=input bytes",
    nativeSpace:"O(1) finite-state scratch; O(log B) if INPUT head coordinate is charged",
    oracleQueryLower:"Every accepted 0^k1 packet has at least k sensitive byte positions"},
  ownership:{distinctPaid:paidSeen.size,partitionEvenOdd:part,referenceViews:2,
    correctSharedTotal:15,wrongPerViewSum:30,scopeControls:3,
    caution:"Two references illustrate sharing only, not historical accepted CASE/WEAKEN grammar"},
  corruptions:controls,padding:{accepted:dupCheck.accept,diagnostic:dupCheck.diagnostic},
  verifierCalls:calls,auditAssertions:assertions,
  limitations:["No authentic historical full-rule parser or external original DIMACS API",
    "No standalone SAT solver or all-input native FLMV interpreter",
    "Independent scope/cost abstract controls are not native syntax",
    "Actual host parse memory is not a universal native working-space lower bound",
    "P versus NP remains OPEN"]};
}
const pt=fs.readFileSync(P,"utf8"),vt=fs.readFileSync(V,"utf8");
if(gitBlob(pt)!==PIN.P||gitBlob(vt)!==PIN.V)throw Error("Historical blob SHA mismatch");
const res=audit(pt,vt),raw=JSON.stringify(res,null,2)+"\n";
if(process.argv[2])fs.writeFileSync(process.argv[2],raw,"utf8");else process.stdout.write(raw);
