'use strict';
/** LSPV-4/583: exact same-realization minimum-pair obstruction for accepted /341 source-order aliases.
 * Run in the j15marti/pnp repository root:
 * node experiments/arc/lspv4_583_joint_attainability.cjs --out results/raw/arc/2026-11-13_0347_LSPV4_583_JOINT_ATTAINABILITY_RAW.json
 * It requires the immutable original packet and checker in their original repository locations.
 */
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const cp = require('node:child_process');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..', '..');
const checkerPath = path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const packetPath = path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const pins = { checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
  packet:'fe27fe1011d0021e721ccaeb747ed58da65d7464' };
const blob = b => crypto.createHash('sha1').update(`blob ${b.length}\0`).update(b).digest('hex');
function fixturePermutations(a){return [
 [a[0],a[1],a[2]], [a[0],a[2],a[1]], [a[1],a[0],a[2]],
 [a[1],a[2],a[0]], [a[2],a[0],a[1]], [a[2],a[1],a[0]] ];}
function literalProbes(lits,assignment){let q=0;
 for(const lit of lits){q++;
  const b=assignment[Math.abs(lit)-1];
  if(lit>0 ? b==='1' : b==='0')break;
 }return q;
}
function insertionComparisons(lits){const a=lits.map(l=>Math.abs(l));let q=0;
 for(let i=1;i<a.length;i++){
  const value=a[i];let j=i-1;
  while(j>=0){q++;if(a[j]<=value)break;a[j+1]=a[j];j--;}
  a[j+1]=value;
 }return q;
}
function allEquivalent(a,b){return a.length===b.length &&
  [...a].sort((x,y)=>x-y).every((x,i)=>x===[...b].sort((u,v)=>u-v)[i]);}
function chooseMin(options,score){return options.reduce((best,x)=>
 score(x)<score(best)?x:best,options[0]);}
function verifyNative(packet,name,expectSuccess){
 const temp=path.join(os.tmpdir(),`lspv4_583_${process.pid}_${name}.json`);
 fs.writeFileSync(temp,Buffer.from(JSON.stringify(packet,null,2)+'\n'));
 let r;try{r=cp.spawnSync(process.execPath,[checkerPath,temp],{encoding:'utf8',maxBuffer:16*1024*1024});}
 finally{fs.unlinkSync(temp);}
 if(expectSuccess){assert.equal(r.status,0,`${name}: ${r.stderr?.slice(0,300)}`);
  const v=JSON.parse(r.stdout);assert.equal(v.checks,30714,`${name}: checker group count`);
  return {accepted:true,assertion_groups:v.checks};
 }
 assert.notEqual(r.status,0,`${name}: malformed packet unexpectedly accepted`);
 return {accepted:false,exit_code:r.status,reason:(r.stderr||'').slice(0,160)};
}
const packetBytes=fs.readFileSync(packetPath),checkerBytes=fs.readFileSync(checkerPath);
assert.equal(blob(packetBytes),pins.packet);assert.equal(blob(checkerBytes),pins.checker);
const original=JSON.parse(packetBytes);const clone=x=>JSON.parse(JSON.stringify(x));
const witnessMin=clone(original),sortMin=clone(original),jointMin=clone(original);
let all={clauses:0,witnesses:0,paid:0,applications:0,
 minQ:0,minS:0,minJ:0,delta:0,compatibleClauses:0,gapClauses:0};
const fixtures=[];
for(let fi=0;fi<original.fixtures.length;fi++){
 const f=original.fixtures[fi];const ws=f.deleted.filter(d=>d.assignment!==null).map(d=>d.assignment);
 const local={name:f.graph.name,clauses:f.clauses.length,witnesses:ws.length,
  minQ:0,minS:0,minJ:0,delta:0,compatibleClauses:0,gapClauses:0};
 for(let ci=0;ci<f.clauses.length;ci++){
  const c=f.clauses[ci];assert.equal(c.literals.length,3);
  const options=fixturePermutations(c.literals).map(lits=>({lits,q:ws.reduce((s,w)=>s+literalProbes(lits,w),0),
   s:insertionComparisons(lits)}));
  assert(options.every(o=>allEquivalent(o.lits,c.literals)));
  const q=chooseMin(options,o=>o.q), s=chooseMin(options,o=>o.s),j=chooseMin(options,o=>o.q+o.s);
  const minQ=q.q,minS=s.s,minJ=j.q+j.s;
  const d=minJ-minQ-minS;
  assert(d===0||d===1,`unexpected local gap ${d}`);
  const coexist=options.some(o=>o.q===minQ && o.s===minS);
  assert.equal(coexist,d===0);
  for(const target of [local,all]){
   target.minQ+=minQ;target.minS+=minS;target.minJ+=minJ;target.delta+=d;
   target.compatibleClauses+=Number(coexist);target.gapClauses+=Number(!coexist);
  }
  witnessMin.fixtures[fi].clauses[ci].literals=q.lits;
  sortMin.fixtures[fi].clauses[ci].literals=s.lits;
  jointMin.fixtures[fi].clauses[ci].literals=j.lits;
  all.clauses++;
 }
 all.witnesses+=ws.length;all.paid+=f.proof.length;
 all.applications+=f.proof.reduce((s,p)=>s+p.parents.length,0);
 fixtures.push(local);
}
assert.deepEqual([all.clauses,all.witnesses,all.paid,all.applications],[328,324,321,642]);
assert.deepEqual([all.minQ,all.minS,all.minJ,all.delta,
 all.compatibleClauses,all.gapClauses],[29238,656,30061,167,161,167]);
assert.equal(all.minJ,all.minQ+all.minS+all.delta);
const serialized=x=>Buffer.from(JSON.stringify(x,null,2)+'\n');
for(const pkt of [witnessMin,sortMin,jointMin])assert.equal(serialized(pkt).length,packetBytes.length);
const native={};
if(!process.argv.includes('--skip-native')){
 native.original=verifyNative(original,'original',true);
 native.witnessMin=verifyNative(witnessMin,'qmin',true);
 native.sortMin=verifyNative(sortMin,'smin',true);
 native.jointMin=verifyNative(jointMin,'jmin',true);
 const hostile=clone(jointMin);
 hostile.fixtures[0].proof[0].parents[0]='definitely-not-a-source';
 native.corruptParent=verifyNative(hostile,'corrupt-parent',false);
}
const result={schema:'LSPV4_583_JOINT_ATTAINABILITY/v1',
 date:'2026-11-13 03:47 PST',model:'Insertion-sort comparison events (explicit algorithm), original /341 short-circuit witness scans; 328 independently permutable signed ternary SOURCE occurrences; identical 197514-byte pretty JSON packet',
 authority:{checker:checkerPath.replace(root+'/',''),checker_blob:pins.checker,
  packet:packetPath.replace(root+'/',''),packet_blob:pins.packet,packet_bytes:packetBytes.length},
 result:all,per_fixture:fixtures,
 certificate_hashes:{witness_min_blob:blob(serialized(witnessMin)),sort_min_blob:blob(serialized(sortMin)),joint_min_blob:blob(serialized(jointMin))},
 native,conclusions:['The coordinatewise minimum pair (29238,656) is not realized by any signed SOURCE-order alias in the declared model.',
 'The exact least realizable Q+S is 30061, exceeding the sum of the separate minima 29894 by 167.',
 'The 167 is the sum of 167 strictly positive local one-event conflicts, one at each incompatible clause.',
 'Coordinatewise minima remain valid nonnegative lower bounds; the conflict concerns simultaneous attainability, not abstract-cost overcharge.',
 'The insertion-sort comparison event is a separately declared concrete algorithm, not the historical /341 V8 sort cost or the fixed R_mix341 inference tariff.',
 'Any native acceptance does not prove source UNSAT in general because the checker has independently documented semantic holes.',
 'This restricted alias-class finding does not authenticate Resolution, DEF, LOCAL-CONVERT, branches, joins, or all-rule P2-C3 closure.']};
const oi=process.argv.indexOf('--out');if(oi>=0){const dest=process.argv[oi+1];assert(dest);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,JSON.stringify(result,null,2)+'\n');}
process.stdout.write(JSON.stringify(result,null,2)+'\n');