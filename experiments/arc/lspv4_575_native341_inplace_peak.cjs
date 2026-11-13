#!/usr/bin/env node
"use strict";
/*
 LSPV-4/575: pinned original-/341 two-register atomic in-place payload peak.
 Usage (from repository root):
   node experiments/arc/lspv4_575_native341_inplace_peak.cjs
   node experiments/arc/lspv4_575_native341_inplace_peak.cjs --out /tmp/lspv4_575.json
 Native OS CLI is invoked on baseline, all optimal reordered, and corrupted packets.
 This is a declared semantic-value payload machine, NOT physical Node.js heap.
 */
const fs=require("fs"),os=require("os"),path=require("path"),crypto=require("crypto"),cp=require("child_process");
const repo=path.resolve(__dirname,"../..");
const orig=path.join(repo,"results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json");
const originalChecker=path.join(repo,"experiments/arc/lspv2_341_independent_verify.js");
const expectedPacket="fe27fe1011d0021e721ccaeb747ed58da65d7464";
const expectedChecker="fcb7d4ced8f922de14c0bda16263a8cc7853e8e0";
function blobId(buf){return crypto.createHash("sha1").update(Buffer.from("blob "+buf.length+"\0")).update(buf).digest("hex");}
for(const [p,expect] of [[orig,expectedPacket],[originalChecker,expectedChecker]]){
 const got=blobId(fs.readFileSync(p)); if(got!==expect)throw Error("SOURCE SHA MISMATCH "+p+": "+got);
}
const packet=JSON.parse(fs.readFileSync(orig,"utf8"));
const bit=i=>1n<<BigInt(i);
function solve(f){
 const n=f.proof.length,V=f.graph.n,E=f.graph.edges.length;
 const F=Math.ceil((9+3*Math.ceil(Math.log2(E)))/8), R=Math.ceil((E+2)/8);
 const expectedW=4*V-1;
 if(n!==expectedW)throw Error("wrong original paid count "+f.graph.name);
 const idix=new Map(f.proof.map((p,i)=>[p.id,i]));
 if(idix.size!==n)throw Error("duplicate paid IDs");
 const deps=f.proof.map(p=>p.parents.map(x=>idix.get(x)).filter(x=>x!==undefined));
 const kids=Array.from({length:n},()=>[]);
 deps.forEach((p,j)=>p.forEach(i=>kids[i].push(j)));
 const wt=f.proof.map(p=>(p.rule==="XOR"||p.row)?R:F);
 const bits=Array.from({length:n},(_,i)=>bit(i)),full=(1n<<BigInt(n))-1n;
 // At a paid inference, one dead parent register may be written in place. No
 // third output value is allocated. Source/packet bytes and scratch are OUTSIDE
 // this value-payload metric. Goal is retained through the terminal step.
 const states=new Map([["0",{peak:0,area:0,order:[]}]]);
 let layer=[0n],transitions=0,overCap=0,invalidOverwrite=0;
 function live(s,terminal=false){
  const a=[];
  for(let i=0;i<n;i++)if((s&bits[i])&&(kids[i].some(k=>(s&bits[k])===0n)||(terminal&&i===n-1)))a.push(i);
  return a;
 }
 for(let d=0;d<n;d++){
  const next=[];
  for(const s of layer){
   const prev=states.get(s.toString()),pre=live(s),preBytes=pre.reduce((q,i)=>q+wt[i],0);
   for(let j=0;j<n;j++){
    if(s&bits[j])continue;
    if(deps[j].some(i=>(s&bits[i])===0n))continue;
    const t=s|bits[j],post=live(t,true);
    if(post.length>2){overCap++;continue;}
    // Replacing a full register requires one now-dead paid parent. If a
    // register is free, the result occupies that free register.
    const free=2-pre.length;
    const dead=pre.filter(i=>deps[j].includes(i)&&!post.includes(i));
    if(free===0&&dead.length===0){invalidOverwrite++;continue;}
    const postBytes=post.reduce((q,i)=>q+wt[i],0);
    const peak=Math.max(prev.peak,preBytes,postBytes),area=prev.area+postBytes;
    const key=t.toString(),old=states.get(key);
    if(!old){states.set(key,{peak,area,order:[...prev.order,j]});next.push(t);}
    else if(peak<old.peak||(peak===old.peak&&area<old.area))
       states.set(key,{peak,area,order:[...prev.order,j]});
    transitions++;
   }
  }
  layer=next;
 }
 const answer=states.get(full.toString());
 if(!answer)throw Error("no completed two-register proof "+f.graph.name);
 const theoremPeak=Math.max(F+R,2*R);
 const theoremArea=2*F*V+(5*V-4)*R-Math.max(0,2*R-3*F);
 const freshPeak=Math.max(R+2*F,F+2*R,3*R);
 if(answer.peak!==theoremPeak||answer.area!==theoremArea)
   throw Error("formula/DP mismatch "+f.graph.name);
 // Validate the precise same-inference, same-source, same-goal chronological
 // execution and its occupied-payload register schedule.
 const computed=new Set(),register=new Set();let area=0,peak=0,overwrite=0;
 for(const j of answer.order){
  const p=f.proof[j]; for(const parent of deps[j])
   if(!computed.has(parent))throw Error("missing paid parent "+p.id);
  const existing=[...register],dead=existing.filter(i=>deps[j].includes(i)&&kids[i].every(k=>computed.has(k)||k===j));
  if(register.size===2&&!dead.length)throw Error("illegal overwrite "+p.id);
  let pre=[...register].reduce((s,i)=>s+wt[i],0);
  for(const i of dead)register.delete(i);
  if(dead.length)overwrite++;
  computed.add(j); register.add(j);
  if(j!==n-1&&kids[j].length===0)throw Error("orphan paid result");
  if(register.size>2)throw Error("register cap exceeded");
  const post=[...register].reduce((s,i)=>s+wt[i],0);
  area+=post;peak=Math.max(peak,pre,post);
 }
 if(computed.size!==n||register.size!==1||!register.has(n-1)||area!==answer.area||peak!==answer.peak)
   throw Error("witness replay mismatch "+f.graph.name);
 return {
  fixture:f.graph.name,V,E,paid:n,parent_applications:2*n,F,R,
  in_place_peak:answer.peak,allocate_before_release_peak:freshPeak,
  percent_peak_reduction:Number((100*(freshPeak-answer.peak)/freshPeak).toFixed(4)),
  optimal_value_area:answer.area,retention_area_574:theoremArea,
  reachable_states:states.size,accepted_transitions:transitions,
  rejected_over_cap:overCap,rejected_overwrite:invalidOverwrite,
  actual_overwrites:overwrite,ordered_paid_ids:answer.order.map(i=>f.proof[i].id)
 };
}
const rows=packet.fixtures.map(solve);
const mapped=JSON.parse(JSON.stringify(packet));
rows.forEach((r,i)=>{const m=new Map(mapped.fixtures[i].proof.map(p=>[p.id,p]));
 mapped.fixtures[i].proof=r.ordered_paid_ids.map(id=>m.get(id));});
const dir=fs.mkdtempSync(path.join(os.tmpdir(),"lspv4-575-"));
function invoke(data,name){
 const f=path.join(dir,name+".json");fs.writeFileSync(f,JSON.stringify(data)+"\n");
 const run=cp.spawnSync(process.execPath,[originalChecker,f],{encoding:"utf8",timeout:25000,maxBuffer:4*1024*1024});
 if(run.error)throw run.error;
 return {accepted:run.status===0,exit_status:run.status,
    assertions:run.status===0?JSON.parse(run.stdout).checks:null,
    stderr:run.stderr.slice(0,260)};
}
let cli;
try{
 const baseline=invoke(packet,"baseline"),reordered=invoke(mapped,"reordered");
 const hostile=JSON.parse(JSON.stringify(mapped)); hostile.fixtures[0].proof.at(-1).row.rhs^=1;
 const corruptSink=invoke(hostile,"corrupt-sink");
 const corruptParent=JSON.parse(JSON.stringify(mapped)); corruptParent.fixtures[0].proof[0].parents[0]="not-a-source";
 const corruptSource=invoke(corruptParent,"corrupt-parent");
 cli={baseline,reordered,corruptSink,corruptSource};
 if(!baseline.accepted||!reordered.accepted||corruptSink.accepted||corruptSource.accepted)
   throw Error("original native CLI unexpected acceptance or rejection");
}finally{fs.rmSync(dir,{recursive:true,force:true});}
const result={
 tag:"LSPV-4/575",status:"PROVED/RESTRICTED atomic in-place payload theorem; COMPUTATIONAL independent exact DP and authentic original OS checker",
 original_packet_git_blob:expectedPacket,original_checker_git_blob:expectedChecker,
 theorem:"P_inplace^*=max(F+R,2R); A_payload^*=2FV+(5V-4)R-max(0,2R-3F) for V>=3 and fixed two-register original proof tree",
 scope:"Atomic in-place resize/read-then-write semantic payload only, with last-use release. Does not count scratch, JSON, parser, source, references or physical heap.",
 total_paid:rows.reduce((s,x)=>s+x.paid,0),
 total_parent_applications:rows.reduce((s,x)=>s+x.parent_applications,0),
 cli,fixtures:rows
};
const json=JSON.stringify(result,null,2)+"\n";
const oi=process.argv.indexOf("--out");if(oi>=0){if(!process.argv[oi+1])throw Error("need --out path");fs.writeFileSync(process.argv[oi+1],json);}
process.stdout.write(json);
