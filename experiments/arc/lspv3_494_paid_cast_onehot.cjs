"use strict";
/* LSPV-3/494: PAID CAST3 type repair for original one-hot Tseitin sources.
 * DISTINCT proposed calculus R_cast494, not authenticated historical R_mix341.
 * Reuses /492 source producer and an independently run /492 semantic checker.
 * Run: node experiments/arc/lspv3_494_paid_cast_onehot.cjs
 */
const predecessor=require("./lspv3_492_onehot_declared_mixed_shortcut.cjs");
function insist(b,m){if(!b)throw Error("CAST494: "+m);}
function sup(c){return [...new Set(c.map(x=>Math.abs(x)))].sort((a,b)=>a-b);}
function table(c,s){let out=0;for(let mask=0;mask<1<<s.length;mask++)
 if(c.some(l=>{let bit=(mask>>s.indexOf(Math.abs(l)))&1;return l>0?bit:1-bit;}))out|=1<<mask;
 return out;
}
function insert(original){
 const old=new Map(original.nodes.map(p=>[p.id,p]));
 const needs=new Set(original.nodes.filter(p=>p.rule==="AND3").flatMap(p=>p.parents).filter(id=>old.get(id)?.rule==="RES"));
 const ren=new Map(original.src.map(p=>[p.id,p.id])),cast=new Map(),nodes=[];
 function add(rule,parents,fields){const id="d"+nodes.length;nodes.push({id,rule,parents,...fields});return id;}
 for(const p of original.nodes){
  const parents=p.parents.map(a=>p.rule==="AND3"&&cast.has(a)?cast.get(a):ren.get(a));
  insist(parents.every(x=>x!==undefined),"predecessor missing");
  const {id,rule,parents:omit,...fields}=p;
  const fresh=add(rule,parents,fields);ren.set(id,fresh);
  if(needs.has(id)){insist(rule==="RES"&&p.c.length===3,"cast target");
   const s=sup(p.c);cast.set(id,add("CAST3",[fresh],{s,t:table(p.c,s)}));}
 }
 return {name:original.name,edges:original.edges,charge:original.charge,src:original.src,nodes};
}
function check(packet){
 const map=new Map(packet.src.map(x=>[x.id,{kind:"CLAUSE",c:x.c,source:true,old:x.id}]));
 const oldNodes=[], oldToNew=new Map();let conversions=0,counts={RES:0,CAST3:0,AND3:0,XOR:0};
 const depths=new Map(packet.src.map(x=>[x.id,0]));
 for(let i=0;i<packet.nodes.length;i++){
  const p=packet.nodes[i];insist(p.id==="d"+i&&!map.has(p.id),"noncanonical ID");
  insist(p.parents.every(x=>map.has(x)),"non-topological reference");
  let parentEntries=p.parents.map(x=>map.get(x));let entry;
  if(p.rule==="CAST3"){
   insist(p.parents.length===1&&parentEntries[0].kind==="CLAUSE"&&!parentEntries[0].source,"CAST premise");
   const c=parentEntries[0].c,s=sup(c);
   insist(s.length<=3&&JSON.stringify(s)===JSON.stringify(p.s)&&table(c,s)===p.t,"CAST exact truth table");
   entry={kind:"FACTOR",s,t:p.t,old:parentEntries[0].old,cast:true};conversions++;
  }else{
   insist(["RES","AND3","XOR"].includes(p.rule)&&p.parents.length===2,"rule/arity");
   if(p.rule==="AND3")insist(parentEntries.every(q=>q.kind==="FACTOR"||(q.kind==="CLAUSE"&&q.source)),"unpaid RES-to-AND3");
   const oldId="d"+oldNodes.length;
   oldNodes.push({...p,id:oldId,parents:parentEntries.map(x=>x.old)});
   oldToNew.set(oldId,p.id);
   entry={kind:p.rule==="RES"?"CLAUSE":p.rule==="AND3"?"FACTOR":"AFFINE",
      c:p.c,s:p.s,t:p.t,row:p.row,old:oldId,source:false};
  }
  counts[p.rule]++;map.set(p.id,entry);
  depths.set(p.id,1+Math.max(...p.parents.map(x=>depths.get(x))));
 }
 const uncast={name:packet.name,edges:packet.edges,charge:packet.charge,src:packet.src,nodes:oldNodes};
 const prev=predecessor.check(uncast);
 const h=packet.charge.length,k=packet.charge.reduce((a,b)=>a+b,0);
 insist(counts.RES===6*h&&counts.CAST3===3*h+k&&counts.AND3===3*h&&counts.XOR===h-1,"count");
 insist(packet.nodes.length===13*h+k-1,"work");
 insist(packet.nodes.at(-1).rule==="XOR","sink");
 return {name:packet.name,h,k,originalVariables:prev.sourceVariables,
   sourceClauses:prev.sourceClauses,paid:packet.nodes.length,counts,
   span:depths.get(packet.nodes.at(-1).id),explicitBytes:JSON.stringify(packet).length,
   oddModels:prev.oddModels,evenModels:prev.evenModels};
}
function run(fixtures){
 const results=[];let rejected=0;
 for(const original of fixtures){const p=insert(original);results.push(check(p));
  const tests=[
   x=>x.nodes.find(t=>t.rule==="CAST3").t^=1,
   x=>x.nodes.find(t=>t.rule==="CAST3").s=[999],
   x=>{const j=x.nodes.findIndex(t=>t.rule==="CAST3");x.nodes[j].parents[0]="d9999";},
   x=>{const z=x.nodes.find(t=>t.rule==="CAST3"),y=x.nodes.find(t=>t.rule==="AND3"&&t.parents.includes(z.id));y.parents[y.parents.indexOf(z.id)]=z.parents[0];},
   x=>x.src[0].c[0]*=-1,
   x=>x.nodes.find(t=>t.rule==="RES").pivot=999,
   x=>{const y=x.nodes.find(t=>t.rule==="AND3"&&t.row);y.row.mask=String(1n<<BigInt(x.edges.length*2+1));}
  ];
  for(const mutate of tests){const copy=JSON.parse(JSON.stringify(p));mutate(copy);
   let denied=false;try{check(copy)}catch(e){denied=true;}insist(denied,"hostile accepted");rejected++;}
 }
 return {results,negativeControlsRejected:rejected,
  theorem:"q=13h+k-1 for odd charge with k ones; R_cast494 only; P versus NP OPEN."};
}
module.exports={insert,check,run};
if(require.main===module){const path=require("path"),fs=require("fs");
const raw=JSON.parse(fs.readFileSync(path.join(__dirname,"../../results/raw/arc/2026-11-07_2320_LSPV3_492_ONEHOT_MIXED_RAW.json"),"utf8"));
console.log(JSON.stringify(run(raw.fixtures),null,2));}
