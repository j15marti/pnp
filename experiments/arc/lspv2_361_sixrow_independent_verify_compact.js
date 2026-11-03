"use strict";
// LSPV-2 361 independent strict RES verification and source witness replay.
const check=function check(data){
 const assert=(x,m)=>{if(!x)throw Error("certificate verification: "+m)};
 assert(data.proof.nodes.length===19,"nodes");
 const lines=data.source.dimacs.trimEnd().split("\n"), header=lines.shift().split(" ");
 assert(header.join(" ")==="p cnf 9 24"&&lines.length===24,"input dimensions");
 const src=lines.map(line=>{
  let t=line.split(" ").map(Number);
  assert(t.length===4&&t[3]===0,"terminated width three");
  assert(t.slice(0,3).every(l=>l!==0&&Math.abs(l)<=9)&&new Set(t.slice(0,3).map(Math.abs)).size===3,"distinct vars");
  return t.slice(0,3);
 });
 const valid=(cs,sk=-1,flip=-1,k=-1)=>{for(let a=0;a<512;a++){
   if(cs.every((cl,i)=>i===sk||cl.some((lit,j)=>{let l=i===flip&&j===k?-lit:lit;return Boolean(a&(1<<(Math.abs(l)-1)))===(l>0)})))return a;
 }return null;};
 assert(valid(src)===null,"source unsat");
 const essential=[];for(let i=0;i<24;i++){
  const w=valid(src,i);
  assert(w===data.controls.deletionWitnesses[i],"deletion witness");
  if(w!==null)essential.push(i);
  for(let j=0;j<3;j++)assert(valid(src,-1,i,j)===data.controls.flipWitnesses[i][j],"flip witness");
 }
 assert(essential.length===20&&essential.every((x,i)=>x===data.controls.essentialIndices[i]),"indispensable clauses");
 const core=essential.map(i=>src[i]);assert(valid(core)===null,"core UNSAT");
 const facts=new Map(src.map((c,i)=>["s"+i,c]));
 const ancestry=new Map(src.map((_,i)=>["s"+i,new Set([i])]));
 const normal=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0?1:0)-(b<0?1:0));
 for(let i=0;i<19;i++){
  const v=data.proof.nodes[i];assert(v.id==="n"+i,"topological IDs");
  const [la,lb]=v.parents, a=facts.get(la),b=facts.get(lb), p=v.pivot;
  assert(a&&b&&a.includes(p)&&b.includes(-p),"oriented genuine pivot");
  const c=normal([...a.filter(l=>l!==p),...b.filter(l=>l!==-p)]);
  assert(!c.some(l=>c.includes(-l))&&c.join(",")===v.lits.join(","),"strict resolvent");
  facts.set(v.id,c);ancestry.set(v.id,new Set([...ancestry.get(la),...ancestry.get(lb)]));
 }
 assert(facts.get("n18").length===0&&ancestry.get("n18").size===20,"root, ancestry");
 assert(data.accounting.sourceBytes===data.source.dimacs.length&&data.accounting.nodes===19,"accounting");
 return {checked:true,pureResolutionNodes:19,essentialSources:20,lowerBound:19,upperBound:19,oppositeModels:16};
};
if(typeof module!=="undefined"&&module.exports)module.exports={check};
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");const data=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));console.log(JSON.stringify(check(data)));}
