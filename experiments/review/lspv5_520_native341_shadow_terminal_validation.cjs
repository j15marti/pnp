#!/usr/bin/env node
'use strict';
/* LSPV-5/520: independent terminal-packet validation of the LSPV-1/611
 * Array/String shadow-coordinate semantics in the unchanged recovered /341
 * checker.  This is not a complete historical R_mix341 authentication.
 */
const fs=require('fs'),os=require('os'),path=require('path'),cp=require('child_process'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const packetPath=path.join(root,'results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json');
const pins={
  checker_sha256:'0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae',
  packet_sha256:'b1cd6c51b34502801319c47f9c1617cdb53f265c49b09867e3176d262bb8a3a2',
  checker_git_blob:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
  packet_git_blob:'8d6d9bc7f2940a77edf2a07fcb72af111ba5b928'
};
function sha(p){return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');}
function need(x,m){if(!x)throw Error(m);}
function clone(x){return JSON.parse(JSON.stringify(x));}
need(sha(checkerPath)===pins.checker_sha256,'checker hash mismatch');
need(sha(packetPath)===pins.packet_sha256,'packet hash mismatch');

/* Source clause s23 is (e0 OR not-e1 OR not-e10), hence only local mask 6
 * falsifies it in support order [0,1,10]. */
const parentA={support:[0,1,10],table:217};
const parentB={support:[0,1,10],table:191};
function shadowBit(s,m,e){
  if(Array.isArray(s)){const j=s.indexOf(e);return j<0?0:(m>>j)&1;}
  if(typeof s==='string'&&e<=9){
    for(let j=0;j<s.length;j++)if(s.charCodeAt(j)===48+e)return (m>>j)&1;
  }
  return 0;
}
function evalParent(p,s,m){
  let q=0;for(let j=0;j<p.support.length;j++)q|=shadowBit(s,m,p.support[j])<<j;
  return (p.table>>q)&1;
}
function shadowTable(s){
  let t=0;for(let m=0;m<(1<<s.length);m++)if(evalParent(parentA,s,m)&&evalParent(parentB,s,m))t|=1<<m;
  return t;
}
function localGate(s){
  try{return s.length===3&&new Set(s).size===3&&[0,1,10].every(e=>s.includes(e));}
  catch{return false;}
}
function runPacket(packet,name,tmp){
  const p=path.join(tmp,name+'.json');fs.writeFileSync(p,JSON.stringify(packet,null,2)+'\n');
  const r=cp.spawnSync(process.execPath,[checkerPath,p],{encoding:'utf8',timeout:20000});
  const accepted=r.status===0;
  const m=accepted?r.stdout.match(/"checks"\s*:\s*(\d+)/):null;
  return {name,accepted,checks:m?Number(m[1]):null,exit:r.status,rejection:accepted?null:(r.stderr+r.stdout).split('\n').find(x=>x.includes('Verifier:'))||'rejected'};
}
function cover(sets,weights){
  const universe=[...new Set(sets.flat())],n=sets.length;let optimum=Infinity;
  for(let mask=0;mask<(1<<n);mask++){
    if(!universe.every(u=>sets.some((s,j)=>(mask&(1<<j))&&s.includes(u))))continue;
    let c=0;for(let j=0;j<n;j++)if(mask&(1<<j))c+=weights[j];optimum=Math.min(optimum,c);
  }
  const tree=universe.reduce((z,u)=>z+Math.min(...sets.map((s,j)=>s.includes(u)?weights[j]:Infinity)),0);
  return {optimum,tree};
}

const base=JSON.parse(fs.readFileSync(packetPath,'utf8'));
const d17=base.fixtures[0].proof.find(p=>p.id==='d17');
need(d17&&d17.parents.join(',')==='d16,s23','d17 anchor');
need(d17.table===153&&d17.support==='102','baseline anchor');
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-520-'));
try{
  const cases=[];
  for(const [name,s] of [
    ['front_uppercase','10A'],
    ['back_uppercase','A10'],
    ['front_lone_surrogate','10'+String.fromCharCode(0xD800)]
  ]){
    need(localGate(s),name+' gate');
    const table=shadowTable(s),q=clone(base),p=q.fixtures[0].proof.find(x=>x.id==='d17');
    p.support=s;p.table=table;
    const r=runPacket(q,name,tmp);need(r.accepted&&r.checks===5155,name+' terminal packet');
    cases.push({...r,support_json:JSON.stringify(s),utf16_length:s.length,codepoint_set_size:new Set(s).size,derived_table:table,coordinate10_shadow:[0,1,2,3,4,5,6,7].map(m=>shadowBit(s,m,10))});
  }
  const negative=[];
  for(const [name,s] of [['object_support',{0:1,1:0,2:'A',length:3}],['number_support',102],['surrogate_pair','😀0']]){
    const q=clone(base),p=q.fixtures[0].proof.find(x=>x.id==='d17');p.support=s;
    const r=runPacket(q,name,tmp);need(!r.accepted,name+' unexpectedly accepted');negative.push({...r,local_gate:localGate(s)});
  }
  const arrays=[];
  for(const s of [[0,1,10],[10,1,0],[1,10,0]]){
    need(localGate(s),'array gate');
    const q=clone(base),p=q.fixtures[0].proof.find(x=>x.id==='d17');p.support=s;p.table=shadowTable(s);
    const r=runPacket(q,'array_'+s.join('_'),tmp);
    arrays.push({...r,support:s,derived_table:p.table,note:'Local Array transformer control only; downstream row bytes were intentionally not repaired.'});
  }
  const star=cover([[0,1,2],[0],[1],[2]],[1,1,1,1]);
  const triangle=cover([[0,1],[0,2],[1,2]],[1,1,1]);
  need(star.optimum===1&&star.tree===3,'cover star');need(triangle.optimum===2&&triangle.tree===3,'cover triangle');
  const out={
    schema:'LSPV5-520-NATIVE341-SHADOW-TERMINAL/v1',timestamp_pst:'2026-11-12T23:48:00-08:00',
    status:'COMPUTATIONAL original-checker OS validation + PROVED/RESTRICTED shadow calculation; full R_mix341 OPEN',
    pins,target:'Falsify LSPV-1/611 exact Array/String local transformer by complete terminal replay.',
    falsifiers:['non-Array/non-String JSON carrier accepted','String writes coordinate 10','surrogate-pair length/code-point mismatch accepted','predicted terminal acceptance disagrees with checker'],
    result:'No falsifier found. Three predicted String packets are accepted by the unchanged checker; three hostile carriers are rejected. Array permutations validate the local transformer only because unrepaired downstream row bytes need not remain terminal-accepted.',
    parent_reconstruction:{d16:parentA,s23:parentB,explanation:'s23 table 191 because only local mask 6 falsifies literals [1,-2,-11]'},
    string_cases:cases,array_cases:arrays,negative_controls:negative,
    peer592_independent_restricted_cover:{star,triangle,conclusion:'paid-once sharing makes independent min-plus overcharge; this is not historical-calculus authentication'},
    peer592_repository_reproducer_blocker:['native_W29.json absent','native_W32.json absent','native_W32_repeat128_raw.json absent','native_checker_pinned.js absent'],
    cegar:'Every cheap String path tested here was concretely replayed. Accepted paths remain genuine checker paths; none is refined away.',
    affected:['P2-D1 remains OPEN','P2-C3 remains OPEN','P2-B1 remains OPEN','P2-B2/B3 remain separate OPEN'],
    nonClaims:['not the historical mixed dispatcher','not an UNSAT-soundness theorem for String supports','not an all-rule shared-DAG abstraction','not a lower bound','P versus NP remains OPEN']
  };
  const raw=JSON.stringify(out,null,2)+'\n';if(process.argv[2])fs.writeFileSync(process.argv[2],raw);process.stdout.write(raw);
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
