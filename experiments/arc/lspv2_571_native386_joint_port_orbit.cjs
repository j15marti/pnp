#!/usr/bin/env node
'use strict';
/* LSPV-2/571: original /386 signed-RES-port x AND2-input-port joint orbit.
 * REFERENCE generator and test driver; never the historical R_mix341 checker.
 * No external packages. Run with node from any working directory.
 * Optional argv[2] is a destination directory for committed byte artifacts.
 */
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const output=process.argv[2] ? path.resolve(process.argv[2]) : path.join(root,'results/raw/arc');
const sha256=x=>crypto.createHash('sha256').update(x).digest('hex');
const gitblob=x=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+x.length+'\0'),x])).digest('hex');
const checkerBytes=fs.readFileSync(checker),seedBytes=fs.readFileSync(seedPath);
assert.equal(gitblob(checkerBytes),'338305c0ce101704205e57543756b8127074a986');
assert.equal(gitblob(seedBytes),'318c52d99977ea4e91bc8554051138a700c1dc94');
const seed=JSON.parse(seedBytes);
const clone=x=>JSON.parse(JSON.stringify(x));
const canon=c=>[...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
function produce(k){
  assert(Number.isSafeInteger(k)&&k>=0&&k<=16);
  let packet=clone(seed);
  for(let j=1;j<=k;j++)packet.gate_defs.push([j,8+j,7+j,7+j]);
  const facets=[{kind:'DEF',c:canon([1,-8]),parents:[],gate:0}];
  for(let j=1;j<=k;j++)facets.push({kind:'DEF',c:canon([7+j,-(8+j)]),parents:[],gate:j});
  for(let j=1;j<=k;j++)facets.push({kind:'DEF',c:canon([8+j,-(7+j)]),parents:[],gate:j});
  facets.push({kind:'DEF',c:canon([8,-1,-4]),parents:[],gate:0});
  const rec=packet.records.slice(0,17).concat(facets);
  function add(ai,bi,pivot){
    const A=rec[ai].c,B=rec[bi].c;
    assert(A.includes(pivot)&&B.includes(-pivot),'RES orientation');
    const c=canon([...A.filter(x=>x!==pivot),...B.filter(x=>x!==-pivot)]);
    assert(!c.some(x=>c.includes(-x)),'tautological resolvent');
    rec.push({kind:'RES',c,parents:[ai,bi],pivot});
    return rec.length-1;
  }
  let tail=add(17,7,1);
  for(let j=1;j<=k;j++)tail=add(tail,17+j,-(7+j));
  for(let j=k;j>=1;j--)tail=add(tail,17+k+j,-(8+j));
  tail=add(tail,17+2*k+1,-8);
  assert.deepEqual(rec[tail].c,seed.records[7].c);
  const delta=4+4*k;
  for(let j=17;j<seed.records.length;j++){
    let r=clone(seed.records[j]);
    r.parents=r.parents.map(i=>i>=17?i+delta:i);
    if(j===20)r.parents=r.parents.map(i=>i===7?tail:i);
    rec.push(r);
  }
  packet.records=rec;
  const resolution=rec.filter(x=>x.kind==='RES').length;
  const def_views=rec.filter(x=>x.kind==='DEF').length;
  packet.summary={source:17,resolution,def_views,paid_gates:k+1,
     paid_total:resolution+k+1,live_records:rec.length};
  assert.equal(resolution,30+2*k);
  assert.equal(rec.length,49+4*k);
  const reachable=new Set(),stack=[rec.length-1];
  while(stack.length){let i=stack.pop();if(reachable.has(i))continue;
    reachable.add(i);stack.push(...rec[i].parents);}
  for(let i=17;i<17+delta;i++)assert(reachable.has(i),'gate facet/RES not live');
  return packet;
}
function flip(p,i){const r=p.records[i];assert.equal(r.kind,'RES');
  r.parents=[r.parents[1],r.parents[0]];r.pivot=-r.pivot;}
function transformed(base,ownerSwap,orient){let p=clone(base);
  if(ownerSwap){const g=p.gate_defs[0];assert.notEqual(g[2],g[3]);[g[2],g[3]]=[g[3],g[2]];}
  let ids=p.records.map((r,i)=>r.kind==='RES'?i:null).filter(i=>i!==null);
  if(orient==='first')flip(p,ids[0]);
  else if(orient==='last')flip(p,ids.at(-1));
  else if(orient==='all')ids.forEach(i=>flip(p,i));
  else if(orient==='alternating')ids.forEach((i,j)=>{if(j%2===0)flip(p,i)});
  else if(orient==='thirds')ids.forEach((i,j)=>{if(j%3===0)flip(p,i)});
  else assert.equal(orient,'none');
  return p;
}
function packetBytes(p){return Buffer.from(JSON.stringify(p)+'\n','utf8');}
function native(p,label,expect,tempDir){const b=packetBytes(p),f=path.join(tempDir,label+'.json');
  fs.writeFileSync(f,b);const t0=process.hrtime.bigint();
  const r=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8',timeout:15000});
  const nanos=process.hrtime.bigint()-t0;let got=r.status===0;
  const parsed=got?JSON.parse(r.stdout.trim().split('\n').at(-1)):null;
  if(got!==expect)throw Error(label+' unexpected native '+(got?'ACCEPT':'REJECT')+' '+r.stderr);
  return {id:label,positive:expect,accepted:got,bytes:b.length,sha256:sha256(b),
   work:p.summary.paid_total,res:p.summary.resolution,gateOwners:p.gate_defs.length,
   sourceCount:p.summary.source,defFacets:p.summary.def_views,records:p.records.length,
   assertionGroups:parsed?.assertions??null,negativeTests:parsed?.negativeTests??null,
   rejection:got?null:(r.stderr.match(/Error: [^\n]+/)||[])[0]||String(r.stderr).slice(0,250),
   elapsedMs:Number(nanos)/1e6};
}
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-571-native-'));
const positives=[],negatives=[];let p2,base2;
try{
  for(let k of [0,2]){
    const base=produce(k);
    if(k===2){base2=base;p2=transformed(base,true,'all');}
    for(const swap of [false,true])for(const orient of ['none','first','last','all','alternating','thirds']){
      let p=transformed(base,swap,orient);
      positives.push(native(p,'k'+k+'_'+(swap?'swap':'natural')+'_'+orient,true,temp));
    }
  }
  const controls={
    gate_operand_changed:p=>{p.gate_defs[0][3]=5;},
    wrong_signed_pivot:p=>{p.records.find(x=>x.kind==='RES').pivot*=-1;},
    wrong_parent_orientation:p=>{let r=p.records.find(x=>x.kind==='RES');r.parents.reverse();},
    forged_source:p=>{p.records[0].c[0]*=-1;},
    source_count_under:p=>{p.summary.source--;},
    undercharge:p=>{p.summary.paid_total--;},
    collision_gate_owner:p=>{p.gate_defs[1][0]=p.gate_defs[0][0];},
    bad_forward_dependency:p=>{let i=p.records.findIndex(x=>x.kind==='RES');p.records[i].parents[0]=p.records.length;},
    unsupported_local_convert:p=>{p.records[17].kind='LOCAL-CONVERT';}
  };
  for(let [name,mutate] of Object.entries(controls)){
    let p=clone(base2);mutate(p); negatives.push(native(p,'bad_'+name,false,temp));
  }
  fs.mkdirSync(output,{recursive:true});
  const sampleName='2026-11-12_0212_LSPV2_571_ACCEPTED_LIVE_JOINT_PORT_ORBIT.json';
  const example=packetBytes(p2);
  fs.writeFileSync(path.join(output,sampleName),example);
  const manifest={run:'LSPV-2/571',scope:'unchanged archived /386 CLI, not R_mix341 full history',
    status:'PROVED/RESTRICTED theorem plus COMPUTATIONAL original OS',
    originalCheckerGitBlob:gitblob(checkerBytes),seedGitBlob:gitblob(seedBytes),
    sourceSpecSha256:sha256(Buffer.from(JSON.stringify(seed.spec))),
    counts:{positive:positives.length,negative:negatives.length,pass:positives.length+negatives.length,
      positiveAssertions:positives.reduce((s,x)=>s+x.assertionGroups,0),
      positiveInternalNegatives:positives.reduce((s,x)=>s+x.negativeTests,0)},
    k0Orbit:'2^(30+1) distinct accepted presentations',
    k2Orbit:'2^(34+1) distinct accepted presentations',
    sample:{filename:sampleName,bytes:example.length,sha256:sha256(example),
      gitblob:gitblob(example),work:p2.summary.paid_total},
    positiveCases:positives,negativeCases:negatives,
    costs:'logical W first-use charged per RES record and gate owner; certificate bits/runtime/span/space distinct',
    missingNativeRules:'MAY; no historical LOCAL-CONVERT, AND3, GF2 or branch grammar authenticated',
    P_versus_NP:'OPEN'};
  const rawName='2026-11-12_0212_LSPV2_571_ORIGINAL_OS_JOINT_PORT_RAW.json';
  fs.writeFileSync(path.join(output,rawName),JSON.stringify(manifest,null,2)+'\n');
  console.log(JSON.stringify({run:manifest.run,checker:manifest.originalCheckerGitBlob,
    count:manifest.counts,byPaid:[...new Set(positives.map(x=>x.work))],sample:manifest.sample,
    negativeNames:negatives.map(x=>x.id),manifest:rawName},null,2));
}finally{fs.rmSync(temp,{recursive:true,force:true});}
