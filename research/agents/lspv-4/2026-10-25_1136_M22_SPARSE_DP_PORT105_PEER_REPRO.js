/* M22-SPARSE-DP-PORT105 peer reproducer. Node >=16, stdlib only.
 * Width-tagged read-only logical source bit queries, not physical FLMV metrics.
 */
"use strict";
const fs=require("fs"),path=require("path");
const P=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]];
const Q=[[1,2,4],[1,3,6],[2,3,5],[4,5,6]];
const Y=[...P,...Q.map(c=>c.map(z=>-z))];
const H=[...P,...P.map(c=>c.map(z=>-z))];
function ck(x,s){if(!x)throw Error(s||"assertion");}
function grammar(F){
 const d=new Map(),keys=new Set();
 for(const c of F){
  ck(c.length===3&&new Set(c.map(Math.abs)).size===3,"proper");
  ck(c.every(z=>z>0)||c.every(z=>z<0),"monotone");
  const sig=c.slice().sort((a,b)=>a-b).join(",");
  ck(!keys.has(sig),"duplicate");keys.add(sig);
  for(const z of c){const k=Math.abs(z)+":"+(z>0);d.set(k,(d.get(k)||0)+1);}
 }
 for(const x of F.flat().map(Math.abs))ck(d.get(x+":true")===2&&d.get(x+":false")===2,"degree");
}
function sparse(F){
 const k=Math.max(...F.flat().map(Math.abs)),m=F.length;
 const w=Math.ceil(Math.log2(k+1)),h=Math.ceil(Math.log2(4*(m+50+k)+2));
 let deleted=new Set(),extra=[],history=[];
 for(const x of [1,2]){
  const pos=[],neg=[];
  function visit(type,i,c){
   if(c.includes(x))pos.push([type,i,c]);
   else if(c.includes(-x))neg.push([type,i,c]);
  }
  F.forEach((c,i)=>{if(!deleted.has(i))visit("B",i,c);});
  extra.forEach((c,i)=>visit("E",i,c));
  const removedE=new Set();
  for(const [type,i] of [...pos,...neg]){if(type==="B")deleted.add(i);else removedE.add(i);}
  extra=extra.filter((_,i)=>!removedE.has(i));
  const add=[];
  for(const [, ,a] of pos)for(const [, ,b] of neg){
   const c=[...new Set([...a.filter(z=>z!==x),...b.filter(z=>z!==-x)])];
   if(!c.some(z=>c.includes(-z)))add.push(c);
  }
  extra.push(...add);
  history.push({pivot:x,p:pos.length,q:neg.length,added:add.length});
 }
 const nbase=m-deleted.size;
 function nth(j){if(j>=nbase)return extra[j-nbase];
  let i=j;for(const d of [...deleted].sort((a,b)=>a-b))if(d<=i)i++;
  return F[i];}
 function cb(c){return c.length.toString(2).padStart(3,"0")+
   c.map(z=>(z<0?"1":"0")+Math.abs(z).toString(2).padStart(w,"0")).join("");}
 function hd(){return k.toString(2).padStart(h,"0")+
   (nbase+extra.length).toString(2).padStart(h,"0");}
 const baseLen=3+3*(w+1), size=2*h+nbase*baseLen+
   extra.reduce((n,c)=>n+3+c.length*(w+1),0);
 function bit(i){
  ck(i>=0&&i<size,"address");
  if(i<2*h)return hd()[i];i-=2*h;
  if(i<nbase*baseLen)return cb(nth(Math.floor(i/baseLen)))[i%baseLen];
  i-=nbase*baseLen;
  for(const c of extra){const z=3+c.length*(w+1);if(i<z)return cb(c)[i];i-=z;}
  throw Error("address overflow");
 }
 const output=Array.from({length:nbase+extra.length},(_,i)=>nth(i));
 const material=hd()+output.map(cb).join("");
 ck(material.length===size,"encoded length");
 for(let i=0;i<size;i++)ck(material[i]===bit(i),"indexed port");
 ck(extra.length<=20&&deleted.size<=12,"patch");
 ck(output.length<=m+8,"clause count");
 ck(output.every(c=>c.length<=6&&!c.some(z=>Math.abs(z)===1||Math.abs(z)===2)),"width/source name");
 return {output,history,sourceBits:2*h+m*baseLen,targetBits:size,
   checkedBits:size,clauses:output.length,deleted:deleted.size,extra:extra.length};
}
function holds(F,a){return F.every(c=>c.some(z=>a[Math.abs(z)]===(z>0)));}
function projection(F,G){
 const v=[...new Set(F.flat().map(Math.abs))].filter(z=>z!==1&&z!==2);
 let rows=0;
 for(let mask=0;mask<(1<<v.length);mask++){
  const a={};v.forEach((x,j)=>a[x]=!!(mask&(1<<j)));
  let expected=false;
  for(let t=0;t<4;t++)expected||=holds(F,{...a,1:!!(t&1),2:!!(t&2)});
  ck(holds(G,a)===expected,"full existential projection");rows++;
 }
 return rows;
}
function audit(F,label,enumerate){
 grammar(F);const r=sparse(F);
 return {label,k:Math.max(...F.flat().map(Math.abs)),m:F.length,
  sourceBits:r.sourceBits,targetBits:r.targetBits,clauses:r.clauses,
  deleted:r.deleted,extra:r.extra,bitChecks:r.checkedBits,
  projectionRows:enumerate?projection(F,r.output):null,history:r.history};
}
function run(U){
 const controls=[audit(Y,"Y SAT, Cstar",true),audit(H,"H paired SAT, outside Cstar",true)];
 if(U)controls.push(audit(U,"U Cstar UNSAT, label imported from Docker",false));
 return {experiment:"M22-SPARSE-DP-PORT105",controls,
  restrictions:"two original pivots (1,2), ordinary CNF only; no ARC exponent improvement"};
}
if(typeof require==="function"&&require.main===module){
 const f=path.join(process.cwd(),"research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt");
 const U=fs.existsSync(f)?JSON.parse(fs.readFileSync(f,"utf8").split("\n")
  .filter(s=>!s.trim().startsWith("#")).join("\n")):null;
 process.stdout.write(JSON.stringify(run(U),null,2)+"\n");
}
if(typeof module!=="undefined")module.exports={run,sparse,audit};