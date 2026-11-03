#!/usr/bin/env node
"use strict";
// LSPV-3 364: no-dependency independent verifier of generated certificates.
const fs=require("fs");
const data=JSON.parse(fs.readFileSync("lspv3_364_certificates.json","utf8"));
let tests=0,proofNodes=0,deletion=0,repairs=0,assignments=0,corrupt=0,malformed=0;
function ok(x,m){tests++;if(!x)throw Error(m||"failed assertion");}
function norm(c){
 if(!Array.isArray(c)||c.some(x=>!Number.isInteger(x)||!x))throw Error("bad literal");
 const a=Array.from(new Set(c)).sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
 if(a.some(x=>a.includes(-x)))throw Error("tautology");
 return a;
}
function same(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function sat(c,mask){return c.some(z=>((mask>>(Math.abs(z)-1))&1)===(z>0?1:0));}
function dimacs(s){
 if(typeof s!=="string"||!s.endsWith("\n"))throw Error("newline");
 const lines=s.trimEnd().split("\n");
 const hd=/^p cnf (\d+) (\d+)$/.exec(lines.shift());
 if(!hd)throw Error("header");
 const nv=Number(hd[1]),nc=Number(hd[2]);
 if(!Number.isSafeInteger(nv)||nc!==lines.length)throw Error("counts");
 const clauses=lines.map(l=>{
   const t=l.trim().split(/\s+/);
   if(t[t.length-1]!=="0"||t.some(x=>!/^[-]?[0-9]+$/.test(x)))throw Error("tokens");
   const c=t.slice(0,-1).map(Number);
   if(c.some(z=>Math.abs(z)>nv))throw Error("variable");
   if(!same(c,norm(c)))throw Error("canonical");
   return c;
 });
 return {nv,clauses};
}
for(const inst of data.instances){
 const n=inst.n,b=inst.b,paths=inst.paths,sources=inst.source,proof=inst.proof;
 const read=dimacs(inst.dimacs);
 ok(read.nv===n+b&&same(read.clauses,sources),"sources");
 ok(sources.length===(1<<b)*(n+1),"size");
 ok(Buffer.byteLength(inst.dimacs)*8===inst.dimacs_bits,"bytes");
 for(let leaf=0;leaf<(1<<b);leaf++){
  const p=paths[leaf],g=[];
  ok(new Set(p).size===n&&p.every(x=>x>=1&&x<=n),"path");
  for(let j=0;j<b;j++)g.push(((leaf>>(b-1-j))&1)?-(n+j+1):(n+j+1));
  const core=[[p[0]]];
  for(let j=0;j<n-1;j++)core.push([-p[j],p[j+1]]);
  core.push([-p[n-1]]);
  for(let j=0;j<=n;j++){
   const k=leaf*(n+1)+j;
   ok(same(sources[k],norm(g.concat(core[j]))),"clause");
   let mask=0;
   for(let i=0;i<j;i++)mask|=1<<(p[i]-1);
   for(let i=0;i<b;i++)if((leaf>>(b-1-i))&1)mask|=1<<(n+i);
   const wrong=[];
   for(let t=0;t<sources.length;t++)if(!sat(sources[t],mask))wrong.push(t);
   ok(same(wrong,[k]),"deletion witness");
   deletion++;
   for(let i=0;i<sources[k].length;i++){
    const repaired=sources[k].slice();repaired[i]=-repaired[i];
    ok(sat(repaired,mask),"flip witness");repairs++;
   }
  }
 }
 const lines=sources.map(c=>c.slice());
 function verifyStep(s){
  const {id,left,right,pivot,clause}=s;
  if(id!==lines.length||!Number.isInteger(left)||!Number.isInteger(right)||
     left<0||right<0||left>=id||right>=id)throw Error("references");
  const A=lines[left],B=lines[right];
  if(!A.includes(pivot)||!B.includes(-pivot))throw Error("pivot");
  const computed=norm(A.filter(x=>x!==pivot).concat(B.filter(x=>x!==-pivot)));
  if(!same(computed,clause))throw Error("resolvent");
  lines.push(clause.slice());
 }
 for(const s of proof){verifyStep(s);proofNodes++;tests++;}
 ok(inst.root===lines.length-1&&lines[inst.root].length===0,"root");
 for(let a=0;a<(1<<(n+b));a++){
  ok(!sources.every(c=>sat(c,a)),"unexpected SAT");assignments++;
 }
 const first=proof[0];let rejected=false;
 try{verifyStep({...first,id:lines.length,pivot:99999});}catch(e){rejected=true;}
 ok(rejected,"corrupt proof accepted");corrupt++;
 for(const bad of [
  inst.dimacs.replace(/^p cnf \d+ \d+/, "p cnf "+(n+b)+" "+(sources.length+1)),
  inst.dimacs.replace(/ 0\n/," 99\n"),
  inst.dimacs.slice(0,-1),
  inst.dimacs.replace(/^p cnf /,"p bad "),
  inst.dimacs.replace(/ 0\n/," BAD\n")
 ]){
  rejected=false;try{dimacs(bad);}catch(e){rejected=true;}
  ok(rejected,"malformed accepted");malformed++;
 }
}
function k4(charge){
 const E=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)E.push([a,b]);
 let models=0;
 for(let mask=0;mask<64;mask++){
  let good=true;
  for(let v=0;v<4;v++){
   let z=0;E.forEach((e,i)=>{if(e.includes(v))z^=(mask>>i)&1;});
   if(z!==charge[v])good=false;
  }
  if(good)models++;
 }
 return models;
}
ok(k4([1,0,0,0])===0,"odd K4");
ok(k4([0,0,0,0])===8,"even K4");
console.log(JSON.stringify({status:"PASS",tests,proofNodes,deletion,repairs,
 assignments,corrupt,malformed,K4_odd_even:[0,8]},null,2));
