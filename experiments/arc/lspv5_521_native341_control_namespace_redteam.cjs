#!/usr/bin/env node
'use strict';
/*
 LSPV-5/521 independent red-team of LSPV-1/612's reachable support namespaces.
 Scope: unchanged archived /341 SOURCE/AND3/XOR checker only. This is not the
 missing historical all-rule R_mix341 dispatcher.

 Run from repository root:
   node experiments/arc/lspv5_521_native341_control_namespace_redteam.cjs \
     --out /tmp/lspv5_521_raw.json --packet /tmp/lspv5_521_nul_packet.json
*/
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const cp=require('node:child_process');
const crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const basePath=path.join(root,'results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json');
const support612Path=path.join(root,'experiments/arc/lspv1_612_native341_support_namespace.cjs');
const checkerBytes=fs.readFileSync(checkerPath);
const baseBytes=fs.readFileSync(basePath);
const checker=checkerBytes.toString('utf8');
const base=JSON.parse(baseBytes.toString('utf8'));
const support612=require(support612Path);
const gitBlob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(gitBlob(checkerBytes),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
assert.equal(gitBlob(baseBytes),'8d6d9bc7f2940a77edf2a07fcb72af111ba5b928');

function ns(s){
  if(Array.isArray(s)&&s.length===3&&new Set(s).size===3&&
     s.every(x=>Number.isInteger(x)&&x>=0))return 'N';
  if(typeof s==='string'&&s.length===3&&new Set(s).size===3)return 'C-string';
  if(Array.isArray(s)&&s.length===3&&new Set(s).size===3&&
     s.every(x=>typeof x==='string'&&x.length===1))return 'C-array';
  return 'OTHER';
}
function gate(a,b,out){
  try{
    const sup=[...new Set([...a,...b])];
    return sup.length<=3&&out.length===sup.length&&
      new Set(out).size===sup.length&&sup.every(x=>out.includes(x));
  }catch(_){return false;}
}
function nativeRun(packet,label){
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5_521_'));
  const p=path.join(dir,'packet.json');
  try{
    const bytes=Buffer.from(JSON.stringify(packet,null,2)+'\n','utf8');
    fs.writeFileSync(p,bytes);
    const r=cp.spawnSync(process.execPath,[checkerPath,p],{encoding:'utf8',timeout:25000});
    return {label,accepted:r.status===0,status:r.status,signal:r.signal,
      stdout:r.stdout.trim(),stderr:r.stderr.trim(),packetBytes:bytes.length,
      packetSha256:sha256(bytes),packetGitBlob:gitBlob(bytes),bytes};
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
}

// The finite carrier corpus includes every reachable namespace shape needed by
// the induction plus deliberately unreachable lexical/property-key attacks.
const N=[[0,1,2],[0,1,10],[1,0,10]];
const C=['012','10A','A10','102','10\u0000','10\n','10\t','10\uffff','10\ud800',
  ['0','1','2'],['1','0','A'],['1','0','\u0000'],['A','0','\ud800']];
const hostile=['length','__proto__','-0A','10\ud835\udfd8','100','01A','1\u00000',
  [1,'0','A'],['length','0','A'],[null,'0','A'],{0:'1',1:'0',2:'A',length:3}];
const parents=N.concat(C);
const outputs=N.concat(C,hostile);
let gatedTriples=0,transformerChecks=0,mixedGates=0,outsideGates=0;
const tables=[0,1,0x33,0x55,0xaa,0xff];
for(const a of parents)for(const b of parents)for(const out of outputs){
  if(!gate(a,b,out))continue;
  gatedTriples++;
  const na=ns(a),nb=ns(b),no=ns(out);
  if((na==='N')!==(nb==='N'))mixedGates++;
  const allowed=na==='N'&&nb==='N'?(no==='N'||no.startsWith('C')):
    na.startsWith('C')&&nb.startsWith('C')?no.startsWith('C'):false;
  if(!allowed)outsideGates++;
  assert(allowed,'accepted carrier escaped N/C closure');
  for(const ta of tables)for(const tb of tables){
    const aa={support:a,table:ta},bb={support:b,table:tb};
    assert.equal(support612.originalLocalTable(aa,bb,out,18),
      support612.specTable(aa,bb,out),'native/key transformer disagreement');
    transformerChecks++;
  }
}
assert.equal(mixedGates,0);
assert.equal(outsideGates,0);

const reachableSamples=N.concat(C.filter(x=>ns(x)!=='OTHER'));
let keyInjectivityChecks=0;
for(const s of reachableSamples){
  const keys=Array.from({length:s.length},(_,i)=>String(s[i]));
  assert.equal(new Set(keys).size,3,'reachable ToPropertyKey collision');
  assert(!keys.includes('length')&&!keys.includes('__proto__'),'special Array key reachable');
  keyInjectivityChecks++;
}

const accepted=[];
let nulPacket=null;
for(const carrier of ['10\u0000','10\n','10\t','10\uffff','10l']){
  const made=support612.balanced(base,carrier);
  const hosted=support612.originalCheck(checker,made.packet);
  assert(hosted.accepted);
  const native=nativeRun(made.packet,JSON.stringify(carrier));
  assert(native.accepted,native.stderr);
  const body=JSON.parse(native.stdout);
  assert.equal(body.checks,5155);
  assert.deepEqual(made.three.map(x=>x.table),[153,255,153]);
  accepted.push({carrierJson:JSON.stringify(carrier),namespace:ns(carrier),
    tables:made.three.map(x=>x.table),checks:body.checks,
    packetBytes:native.packetBytes,packetSha256:native.packetSha256,
    packetGitBlob:native.packetGitBlob});
  if(carrier==='10\u0000')nulPacket=made.packet;
}

const rejected=[];
for(const [label,carrier,expected] of [
  ['astral-math-zero','10\ud835\udfd8','build'],
  ['duplicate-zero','100','build'],
  ['character-array-from-numeric',['1','0','A'],'build'],
  ['numeric-array-terminal-alias',[1,0,10],'native']
]){
  try{
    const made=support612.balanced(base,carrier);
    const native=nativeRun(made.packet,label);
    assert.equal(expected,'native');
    assert(!native.accepted,'hostile packet unexpectedly accepted');
    rejected.push({label,stage:'native',error:
      native.stderr.split('\n').find(x=>x.includes('Error: Verifier:'))||native.stderr.split('\n').at(-1)});
  }catch(e){
    assert.equal(expected,'build');
    rejected.push({label,stage:'construction',error:String(e)});
  }
}

assert(nulPacket);
const nulBytes=Buffer.from(JSON.stringify(nulPacket,null,2)+'\n','utf8');
const result={
  report:'LSPV-5/521',
  date:'2026-11-13 00:52 PST',
  status:'PASS',
  scope:'unchanged archived /341 SOURCE/AND3/XOR checker only; full historical R_mix341 unavailable',
  checker:{gitBlob:gitBlob(checkerBytes),sha256:sha256(checkerBytes)},
  baseline:{gitBlob:gitBlob(baseBytes),sha256:sha256(baseBytes)},
  finiteClosureAudit:{parentSupports:parents.length,outputCandidates:outputs.length,
    gatedTriples,transformerChecks,mixedGates,outsideGates,keyInjectivityChecks},
  accepted,rejected,
  nulPacket:{bytes:nulBytes.length,sha256:sha256(nulBytes),gitBlob:gitBlob(nulBytes)},
  repairedLemma:'On every reachable N or C support, ToPropertyKey is injective; no reachable key is length or __proto__. The /612 last-write transformer therefore reduces to a unique-coordinate transformer. Control characters widen syntax but do not cross the one-way N/C membrane.',
  consequence:{P2_D1:'OPEN: NUL and other control-character carriers are accepted by /341 but the all-rule historical checker is absent',P2_C3:'OPEN: restricted transformer validated only for /341',P2_B1:'OPEN',P2_B2_B3:'separate and unsupported'},
  pVsNP:'OPEN'
};
const arg=n=>{const i=process.argv.indexOf(n);return i<0?null:process.argv[i+1];};
const out=arg('--out'),packetOut=arg('--packet');
if(out)fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n','utf8');
if(packetOut)fs.writeFileSync(packetOut,nulBytes);
process.stdout.write(JSON.stringify(result,null,2)+'\n');
