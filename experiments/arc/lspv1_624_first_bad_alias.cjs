'use strict';
// LSPV-1/624 exact /341 first-false-affine-row forensic control.
// From repository root: node experiments/arc/lspv1_624_first_bad_alias.cjs
// To independently OS-replay the historical checker, pass --native.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),cp=require('child_process'),assert=require('assert/strict');
const root=path.resolve(__dirname,'../..');
const packetPath=path.join(root,'results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json');
const checkerPath=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const blobPins={packet:'706947c767361e7c979b8208677eb983d33838f4',checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0'};
const E=[[0,2],[0,3],[1,2],[1,3],[2,3],[1,4],[8,9],[5,8],[6,7],[9,10],[6,9],[7,5],[0,4],[10,8],[7,10],[5,11],[6,11],[4,11]];
const patterns=Array.from({length:12},(_,v)=>v===0?[0,4,3,7]:[1,2,4,7]);
const inc=v=>E.map(([a,b],i)=>a===v||b===v?i:-1).filter(i=>i>=0);
const cs=[];for(let v=0;v<12;v++)for(const p of patterns[v]){
 const ie=inc(v); assert.equal(ie.length,3);
 cs.push({id:'s'+cs.length,vertex:v,pattern:p,literals:ie.map((e,j)=>((p>>j)&1? -1:1)*(e+1))});
}
const nativeIds=Array.from({length:12},(_,v)=>'d'+(3*v+2));
const masks=Array.from({length:12},(_,v)=>inc(v).reduce((a,e)=>a^(1<<e),0));
assert.equal(masks[0],0x1003);
const gitsha=buf=>crypto.createHash('sha1').update('blob '+buf.length+'\0').update(buf).digest('hex');
let packetVerified=false;
if(fs.existsSync(packetPath)){
 const bytes=fs.readFileSync(packetPath); assert.equal(gitsha(bytes),blobPins.packet);
 const fixture=JSON.parse(bytes).fixtures[1];
 assert.deepEqual(fixture.graph.edges,E); assert.deepEqual(fixture.clauses,cs);
 assert.equal(fixture.charges[0],'1'); assert.deepEqual(fixture.charges.slice(1),Array(11).fill(0));
 const rows=fixture.proof.filter(p=>p.rule==='AND3'&&p.row);
 assert.equal(rows.length,12);assert.deepEqual(rows.map(x=>x.id),nativeIds);
 assert.deepEqual(rows.map(x=>Number(BigInt(x.row.mask))),masks);
 assert.deepEqual(rows.map(x=>x.row.rhs),[1,...Array(11).fill(0)]);
 assert.equal(rows[0].support,'012');
 assert.deepEqual(fixture.proof.at(-1).row,{mask:'0x0',rhs:1});
 packetVerified=true;
}
// SOURCE has 48 signed width-three clauses; compute falsifying bit pattern per clause.
const forbidden=cs.map(c=>({mask:c.literals.reduce((a,l)=>a|(1<<(Math.abs(l)-1)),0),
 val:c.literals.filter(l=>l<0).reduce((a,l)=>a|(1<<(-l-1)),0)}));
const sourceSAT=a=>forbidden.every(({mask,val})=>(a&mask)!==val);
const parity=a=>(a.toString(2).replaceAll('0','').length&1);
const rowViolated=(a,i)=>parity(a&masks[i])!==(i===0?1:0);
let count=0,bad=Array(12).fill(0),firstExample=null,sourceModelX13_0=0;
for(let a=0;a<(1<<18);a++)if(sourceSAT(a)){
 count++;if(firstExample===null)firstExample=Array.from({length:18},(_,i)=>(a>>i)&1).join('');
 if(((a>>12)&1)===0)sourceModelX13_0++;
 for(let v=0;v<12;v++)if(rowViolated(a,v))bad[v]++;
}
assert.equal(count,64);assert.deepEqual(bad,[64,...Array(11).fill(0)]);
const witness='101001000000100000',value=[...witness].reduce((a,b,i)=>a|(Number(b)<<i),0);
assert(sourceSAT(value));assert(rowViolated(value,0));
assert.equal(sourceModelX13_0,0);
function gf2rank(rows){const piv=new Map();for(let x of rows){while(x){const k=31-Math.clz32(x);if(piv.has(k))x^=piv.get(k);else{piv.set(k,x);break;}}}return piv.size;}
const otherMasks=masks.slice(1),v0Source=(1<<0)|(1<<1);
assert.equal(gf2rank(otherMasks),11);assert.equal(gf2rank([...otherMasks,v0Source]),12);
assert.equal(otherMasks.reduce((a,b)=>a^b,0),masks[0]);
// Original checker accepts a bad string support because substring(12) matches "12".
assert.equal('012'.includes(12),true);assert.equal(1!=='1',true);assert.equal('1'^0,1);
let nativeReplay='NOT_RUN',checks=null;
if(process.argv.includes('--native')){
 assert(fs.existsSync(packetPath),'missing pinned original packet');assert(fs.existsSync(checkerPath),'missing pinned original checker');
 assert.equal(gitsha(fs.readFileSync(checkerPath)),blobPins.checker);
 const proc=cp.spawnSync(process.execPath,[checkerPath,packetPath],{encoding:'utf8',maxBuffer:1<<22});
 if(proc.status!==0)throw Error('original checker rejected: '+proc.stderr+' '+proc.stdout);
 const verdict=JSON.parse(proc.stdout);nativeReplay='ACCEPT';checks=verdict.checks;
}
const out={id:'LSPV-1/624',date:'2026-11-13 America/Los_Angeles',source:'exact published /341 BRIDGE_K4x2 fixture',
 original_packet_git_blob:blobPins.packet,original_checker_git_blob:blobPins.checker,
 exact_packet_verified:packetVerified,source_variables:18,source_clauses:48,
 exhaustive_assignments:1<<18,satisfying_assignments:count,witness,
 other_11_native_aliases_false_on:bad.slice(1),first_native_alias_d2_false_on:bad[0],
 independent_source_GF2_rank:12,remaining_vertex_rank:11,
 sum_of_other_11_masks:'0x'+otherMasks.reduce((a,b)=>a^b,0).toString(16),
 d2_mask:'0x'+masks[0].toString(16),d2_rhs:1,
 special_vertex_source_relation:'x1 XOR x2 = 1',forced_x13:1,
 native_original_checker_replay:nativeReplay,native_original_checker_checks:checks,
 conclusion:'All 64 SAT models satisfy the 11 authentic local parity rows and falsify d2. The sole bad base row feeds the final false XOR contradiction.',
 scope:'Pinned /341 SOURCE/AND3/XOR only, not authenticated full R_mix341.'};
console.log(JSON.stringify(out,null,2));
