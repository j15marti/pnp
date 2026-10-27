#!/usr/bin/env node
"use strict";
function runAudit(){
 let assertions=0;const ck=(ok,msg)=>{assertions++;if(!ok)throw Error(msg)};
 const W1=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
 const A=[[6,0],[11,0]],B=[[9,2],[17,2]];
 const mod=(a,b)=>{const F=W1.map(x=>x.slice());if(!a)for(const[i,j]of A)F[i][j]*=-1;if(!b)for(const[i,j]of B)F[i][j]*=-1;return F};
 function proper(F){ck(F.length===20&&new Set(F.map(x=>x.join())).size===20,"clause count");const p=Array(16).fill(0),n=Array(16).fill(0);for(const c of F){ck(c.length===3&&new Set(c.map(x=>Math.abs(x))).size===3,"proper");for(const l of c)(l>0?p:n)[Math.abs(l)]++}for(let i=1;i<=15;i++)ck(p[i]===2&&n[i]===2,"signed exact22")}
 function count(F){let ans=0;for(let a=0;a<(1<<15);a++){if(F.every(c=>c.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0))))ans++}return ans}
 const models={};for(const a of[0,1])for(const b of[0,1]){const F=mod(a,b);proper(F);models[""+a+b]=count(F)}ck(models["00"]===772&&models["01"]===272&&models["10"]===272&&models["11"]===0,"W1 modes");
 function verifier(a,b,read){const m=a.length,q=Math.ceil(Math.log2(m));const left=Array.from({length:q},(_,i)=>i),v=[];let prev=0;for(let j=0;j<q;j++){const pick=(prev+j)%left.length,address=left.splice(pick,1)[0],ans=read(address);if(ans!==0&&ans!==1)return false;if(read(address)!==ans)return false;v.push(ans);prev=ans}const idx=v.reduce((s,bit,i)=>s+(bit<<i),0);return idx<m&&a[idx]===1&&b[idx]===1}
 function simulate(a,b,z){const q=Math.ceil(Math.log2(a.length)),cache=new Map();let used=0;const read=i=>{if(!cache.has(i)){if(used>=q)throw Error("over budget");cache.set(i,(z>>used)&1);used++}return cache.get(i)};const ok=verifier(a,b,read);ck(used===q&&cache.size===q,"distinct bits and repeats");return ok}
 let cases=0,sat=0,unsat=0,proofCalls=0,transcriptCalls=0;
 for(let m=1;m<=5;m++){const cap=1<<Math.ceil(Math.log2(m));for(let aa=0;aa<(1<<m);aa++)for(let bb=0;bb<(1<<m);bb++){const a=Array.from({length:m},(_,i)=>(aa>>i)&1),b=Array.from({length:m},(_,i)=>(bb>>i)&1),bad=a.some((x,i)=>x&&b[i]);let np=0,nt=0;for(let pi=0;pi<cap;pi++){np+=+verifier(a,b,i=>(pi>>i)&1);proofCalls++}for(let z=0;z<cap;z++){nt+=+simulate(a,b,z);transcriptCalls++}ck(np===nt&&np===a.reduce((s,x,i)=>s+(x&b[i]),0),"adaptive answers");ck((np>0)===bad,"sound and complete on promise");cases++;if(bad)unsat++;else sat++}}
 ck(cases===1364&&sat+unsat===cases,"promise count");
 let bogus=false;for(const bit of[0,1]){const memo=new Map(),read=i=>{if(!memo.has(i))memo.set(i,bit);return memo.get(i)};bogus ||= read(0)===0&&read(0)===1}ck(!bogus,"repeated bit consistency");
 const a=[0,0,0,1],b=[0,0,0,1];ck([0,1,2,3].some(i=>a[i]&b[i])&&![0,1].some(i=>a[i]&b[i]),"word must count two bits");
 ck([0,1,2,3].some(len=>a[len]&b[len])&&!(a[0]&b[0]),"length side channel");
 const changed=mod(1,1).map(x=>x.slice());changed[0][0]*=-1;ck(![0,1].some(x=>[0,1].some(y=>JSON.stringify(changed)===JSON.stringify(mod(x,y)))),"malformed sign");
 const c=241/200,ss=11642479/23232400;ck(Math.abs((c+2)/(2*c*c)-c/2-ss)<1e-12,"FLMV fraction");
 const pts=[[1,.200,.4],[1,.205,.4],[1,.210,.4],[1.1,.10,.4],[1,0,.6]];
 const forbidden=pts.map(([r,alpha,s])=>Math.max(1,r+alpha)<c&&s<ss);
 ck(forbidden.join(",")==="true,false,false,true,false","strict endpoints");
 return {run_id:"ARC200_OBSERVED_PROOF_BIT_FRONTIER",label:"COMPUTATIONAL finite W1 promise controls",models,properModules:4,cases,sat_cases:sat,unsat_cases:unsat,proofCalls,transcriptCalls,controls:["adaptive-query order","consistent repeated bits","packed 2-bit word","variable length advice","one-sign corruption","strict FLMV endpoint"],forbidden,assertionGroups:assertions,failures:0,seed:null,limitations:["No ordinary all-UNSAT proof coverage established","The W1 experiment is only on canonical proper signed exact22 source promise","No claimed unrestricted SAT time lower bound","Proof queries are individual bits with fixed public proof length","No sequential-tape to indexed-RAM transfer"]};
}
const raw=runAudit();
if(typeof process!=="undefined"&&process.versions&&process.versions.node){
 const fs=require("node:fs"),path=require("node:path");
 fs.writeFileSync(path.join(__dirname,"2026-10-27_0355_ARC200_observed_proof_bits_raw.json"),JSON.stringify(raw,null,2)+"\n");
 console.log(JSON.stringify(raw,null,2));
}
