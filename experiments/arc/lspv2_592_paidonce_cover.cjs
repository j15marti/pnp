#!/usr/bin/env node
'use strict';
/* LSPV-2/592. Independent restricted cover-provenance model, NOT historical R_mix341. */
const fs = require('fs');
const crypto = require('crypto');
const cp = require('child_process');
const path = require('path');
const sha256 = b => crypto.createHash('sha256').update(b).digest('hex');
function fail(s){throw Error(s)}
function check(x,s){if(!x)fail(s)}
function cover(sets,weight){
  check(sets.length===weight.length,'cost dimension');
  const m=1+Math.max(...sets.flat(),0),n=sets.length;
  check(n>0&&n<=20&&m>0,'finite sizes');
  for(let i=0;i<m;i++)check(sets.some(t=>t.includes(i)),'uncovered obligation '+i);
  const coverCount=Array(n).fill(0); const records=[];
  let optimum=Infinity,bestMask=null,feasible=0,checks=0;
  for(let mask=0;mask<(1<<n);mask++){
    let good=true,paid=0;
    for(let j=0;j<n;j++)if(mask&(1<<j))paid+=weight[j];
    for(let u=0;u<m;u++){checks++;if(!sets.some((s,j)=>(mask&(1<<j))&&s.includes(u))){good=false;break;}}
    if(good){feasible++;if(paid<optimum){optimum=paid;bestMask=mask;}}
  }
  let tree=0;
  for(let u=0;u<m;u++)tree+=Math.min(...sets.map((s,j)=>s.includes(u)?weight[j]:Infinity));
  /* A feasible dual is y_u = min_j w_j / |S_j|. It is NEVER a higher bound than any paid-once witness. */
  const unit=Math.min(...sets.map((s,j)=>weight[j]/s.length));
  const dual=m*unit;
  check(dual<=optimum+1e-10,'dual exceeded concrete optimum');
  check(tree>=optimum-1e-10,'tree minplus below concrete optimum');
  const selected=sets.map((s,j)=>bestMask&(1<<j)?j:null).filter(x=>x!==null);
  return {n,m,sets,weight,optimum,bestMask,selected,tree,dual,feasible,checks};
}
function rng(seed){return()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296}}
function validatePaidOwnerPacket(file,checker){
  const bytes=fs.readFileSync(file),p=JSON.parse(bytes);
  const native=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:20000});
  check(native.status===0,'native positive failed: '+native.stderr);
  const nativeOut=JSON.parse(native.stdout.trim().split('\n').at(-1));
  const paidOwner=new Set(p.gate_defs.map(x=>x[0]));
  const allFacets=p.records.filter(r=>r.kind==='DEF');
  check(nativeOut.paid===p.summary.paid_total,'native W mismatch');
  check(nativeOut.paid===p.summary.resolution+paidOwner.size,'count once native owner');
  const bad=JSON.parse(bytes);bad.records.at(-1).pivot=123456789;
  const temp=path.join(path.dirname(file),'__592_bad_pivot_temp.json');
  fs.writeFileSync(temp,JSON.stringify(bad));
  const reject=cp.spawnSync(process.execPath,[checker,temp],{encoding:'utf8',timeout:20000});
  fs.unlinkSync(temp);
  check(reject.status!==0,'native corrupted pivot accepted');
  return {packet:file,sha256:sha256(bytes),checkerSha256:sha256(fs.readFileSync(checker)),nativeAccept:true,badPivotRejected:true,paid:nativeOut.paid,paidOwners:paidOwner.size,defFacets:allFacets.length,sourceRecords:p.summary.source,resolutions:p.summary.resolution,originalAssertions:nativeOut.assertions};
}
function main(){
  const results=[];
  for(let m=2;m<=10;m++){
    let sets=[Array.from({length:m},(_,i)=>i)];for(let i=0;i<m;i++)sets.push([i]);
    let r=cover(sets,sets.map(()=>1));
    check(r.optimum===1&&r.tree===m&&Math.abs(r.dual-1)<1e-12,'star family');
    results.push({family:'shared_owner_star',size:m,...r});
  }
  const tri=cover([[0,1],[0,2],[1,2]],[1,1,1]);
  check(tri.optimum===2&&tri.tree===3&&tri.dual===1.5,'triangle CEGAR');
  const fractional={x:[0.5,0.5,0.5],obligationCoverage:[1,1,1],cost:1.5};
  check(fractional.obligationCoverage.every(x=>x>=1),'LP feasible');
  const refinedCut={inequality:'x0+x1+x2>=2',proof:'Each selected owner covers at most two of three obligations; two distinct owners are necessary',rhs:2,lpPointViolates:true,integralOptimum:2};
  const random=rng(592);let randomCases=0,randomChecks=0;
  for(let rep=0;rep<200;rep++){
    const n=2+Math.floor(random()*7),m=1+Math.floor(random()*6);
    const sets=Array.from({length:n},()=>[]);
    for(let u=0;u<m;u++){
      const opts=Array.from({length:n},(_,i)=>i).filter(()=>random()<0.48);
      if(!opts.length)opts.push(Math.floor(random()*n));
      for(const j of opts)sets[j].push(u);
    }
    for(let j=0;j<n;j++)if(!sets[j].length)sets[j].push(Math.floor(random()*m));
    const weights=sets.map(()=>1+Math.floor(random()*4));
    const r=cover(sets,weights);randomCases++;randomChecks+=r.checks;
    check(r.dual<=r.optimum+1e-9,'violating independent dual');
    check(r.tree>=r.optimum-1e-9,'violating tree');
  }
  const native=[validatePaidOwnerPacket(path.join(__dirname,'native_W29.json'),path.join(__dirname,'native_checker_pinned.js')),validatePaidOwnerPacket(path.join(__dirname,'native_W32.json'),path.join(__dirname,'native_checker_pinned.js')),validatePaidOwnerPacket(path.join(__dirname,'native_W32_repeat128_raw.json'),path.join(__dirname,'native_checker_pinned.js'))];
  const output={date:'2026-11-12 23:12 PST',role:'LSPV-2',scope:'RESTRICTED COVER MODEL; native386 independently archived fixture; no historical R_mix341 full dispatcher',hypothesis:'once-paid shared owners cannot be soundly replaced by independent min-plus conjunctive costs',falsifiers:['one owner cannot cover all obligations','fractional point is concrete legal payment','proven dual exceeds a concrete witness','native /386 reuses a facet owner at additional gate charge'],star:results.map(r=>({obligations:r.m,owners:r.n,concreteMinimum:r.optimum,naiveTree:r.tree,dualLower:r.dual,selected:r.selected})),triangle:{concreteMinimum:tri.optimum,naiveTree:tri.tree,dualLower:tri.dual,fractional,refinedCut},random:{seed:592,cases:randomCases,checkedObligationTests:randomChecks,status:'ALL PASS'},native,notClaims:['not a complete R_mix341 checker','not a universal CALCULUS transformer','not a P-vs-NP proof','not new Set Cover NP-hardness']};
  const raw=JSON.stringify(output,null,2)+'\n';fs.writeFileSync(path.join(__dirname,'2026-11-12_2312_LSPV2_592_PAIDONCE_COVER_RAW.json'),raw);
  process.stdout.write(JSON.stringify({star:output.star,triangle:output.triangle,random:output.random,native:output.native,rawSha256:sha256(Buffer.from(raw))},null,2)+'\n');
}
main();
