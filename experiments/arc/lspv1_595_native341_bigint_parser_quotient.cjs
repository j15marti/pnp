'use strict';
// LSPV-1/595. Replays EXACT original archived /341 verifier through Node vm.
// No alterations to checker inference/acceptance code; only fs/argv/stdout adapters.
// Usage from j15marti/pnp root: node experiments/arc/lspv1_595_native341_bigint_parser_quotient.cjs [raw-output-path]
const fs=require('fs'),path=require('path'),crypto=require('crypto'),vm=require('vm'),assert=require('assert');
const root=process.cwd();
const checkerPath=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const packetPath=path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const checkerBytes=fs.readFileSync(checkerPath),packetBytes=fs.readFileSync(packetPath);
function gitBlob(b){return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex')}
assert.strictEqual(gitBlob(checkerBytes),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
assert.strictEqual(gitBlob(packetBytes),'fe27fe1011d0021e721ccaeb747ed58da65d7464');
const checker=checkerBytes.toString('utf8');
const original=JSON.parse(packetBytes.toString('utf8'));
function cp(x){return JSON.parse(JSON.stringify(x))}
function replay(packet){
  const lines=[],serialized=JSON.stringify(packet)+'\n';
  const adapters={
    require(name){if(name!=='fs')throw Error('unexpected require: '+name);return {readFileSync(){return serialized}}},
    process:{argv:['node','original-native341','packet.json']},
    console:{log(x){lines.push(String(x))}}
  };
  try{
    vm.runInNewContext(checker,adapters,{filename:'PINNED-original-341.js',timeout:20000});
    const answer=JSON.parse(lines.join(''));
    return {accepted:true,checks:answer.checks,fixtures:answer.cases.length};
  }catch(e){return {accepted:false,error:String(e).slice(0,150)}}
}
const first={fixtures:[cp(original.fixtures[0])],summary:[cp(original.summary[0])]};
assert(replay(first).accepted);
const rows=first.fixtures[0].proof.filter(r=>r.row);
const values=[
 null,false,true,0,1,7,25,30,42,52,[],[0],[7],[25],[30],[42],[52],
 [[0]],[[7]],[null],[false],'',' ','\t0','000','0x0','0b0','0o0','0',
 '7','25','30','42','52','0x7','0b111','0o7','7 ','0007',[0,0],{},['bad'],'0.0','-0',[[null]]
];
const tests=[];
for(let i=0;i<rows.length;i++)for(const value of values){
 const clone=cp(first);
 clone.fixtures[0].proof.filter(r=>r.row)[i].row.mask=value;
 let expected=false;
 try{expected=BigInt(value)===BigInt(rows[i].row.mask)}catch(_){}
 const observed=replay(clone);
 tests.push({row:i,id:rows[i].id,value,equalBigInt:expected,accepted:observed.accepted});
 assert.strictEqual(observed.accepted,expected,'single-field coercion mismatch at '+i+' '+JSON.stringify(value));
}
const allNested=cp(original);
let allRowCount=0;
for(const f of allNested.fixtures)for(const r of f.proof)if(r.row){
 r.row.mask=[[BigInt(r.row.mask).toString(10)]];
 allRowCount++;
}
const fullOriginalResult=replay(original),fullNestedResult=replay(allNested);
assert(fullOriginalResult.accepted&&fullNestedResult.accepted);
assert.strictEqual(fullNestedResult.checks,fullOriginalResult.checks);
const padded=cp(original);padded.fixtures[0].proof.at(-1).row.mask='0'.repeat(128);
const paddedResult=replay(padded);assert(paddedResult.accepted);
const pairedGhost=cp(first);
for(const k of [0,1])pairedGhost.fixtures[0].proof.filter(r=>r.row)[k].row.mask=(BigInt(rows[k].row.mask)^64n).toString(10);
const ghostResult=replay(pairedGhost);assert(ghostResult.accepted);
const mutants={};
for(const name of ['source','conjunction','parent','sink','rhs','badMask']){
 const m=cp(first);
 if(name==='source')m.fixtures[0].clauses[0].literals[0]=999;
 if(name==='conjunction')m.fixtures[0].proof[0].table^=1;
 if(name==='parent')m.fixtures[0].proof[0].parents[0]='unknown-source';
 if(name==='sink')m.fixtures[0].proof.at(-1).row.rhs=0;
 if(name==='rhs')m.fixtures[0].proof.filter(r=>r.row)[0].row.rhs=false;
 if(name==='badMask')m.fixtures[0].proof.at(-1).row.mask=['bad'];
 mutants[name]=replay(m);
 assert(!mutants[name].accepted,'hostile mutation accepted: '+name);
}
const result={
 run:'LSPV1-595-NATIVE341-BIGINT-QUOTIENT',
 status:'PROVED/RESTRICTED source-code factorization + COMPUTATIONAL original-checker Node-vm replay; not full R_mix341',
 checkerGitBlob:gitBlob(checkerBytes),fixtureGitBlob:gitBlob(packetBytes),
 scope:'source-bound in-band /341 SOURCE/AND3/XOR original fixture checker only',
 rootSourceUnchanged:true, paidNodesK4:first.fixtures[0].proof.length,
 singleFieldProbes:tests.length, singleFieldPredictedAccepted:tests.filter(t=>t.equalBigInt).length,
 singleFieldActuallyAccepted:tests.filter(t=>t.accepted).length,
 matched:tests.filter(t=>t.equalBigInt===t.accepted).length,
 allNestedMaskFields:allRowCount,fullOriginalResult,fullNestedResult,
 terminal128LeadingZeros:paddedResult,pairedHighGhostCountercontrol:ghostResult,
 hostileMutationResults:mutants,probeResults:tests,
 limitations:['fixed packet with single-field tests; not exhaustive JSON grammar','paired high ghost bits show same-BigInt equivalence is sufficient but not necessary for simultaneous edits','no historical R_mix341 RES/AND3/LOCAL-CONVERT cross-dispatcher authenticated']
};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:'PASS',probes:tests.length,accepted:result.singleFieldActuallyAccepted,nested:allRowCount,hostile:Object.keys(mutants).length}));
