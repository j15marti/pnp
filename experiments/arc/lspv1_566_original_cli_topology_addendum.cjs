'use strict';
// LSPV-1/566 CLI addendum: exercise the ORIGINAL archived /386 full CLI
// validation and its bundled eleven negative tests on topo-permuted packets.
// All original checker mathematics is unchanged. Only fs/file and
// output SHA adapters are simulated. Run:
// node experiments/arc/lspv1_566_original_cli_topology_addendum.cjs [out.json]
const fs=require('fs'),path=require('path'),assert=require('assert'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const vf='experiments/arc/lspv2_386_independent_verify.js';
const pf='results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json';
const source=fs.readFileSync(path.join(root,vf),'utf8');
const P=JSON.parse(fs.readFileSync(path.join(root,pf),'utf8'));
const cp=x=>JSON.parse(JSON.stringify(x));
function permutation(d,indices){
  const pos=new Map(indices.map((old,i)=>[old,i]));
  return {...cp(d),records:indices.map(i=>({...cp(d.records[i]),parents:d.records[i].parents.map(j=>pos.get(j))}))};
}
function topo(seed){
  let n=seed>>>0,seen=new Set(),order=[],last=P.records.length-1;
  for(let t=0;t<P.records.length;t++){
    const ready=P.records.map((_,i)=>i).filter(i=>!seen.has(i)&&(i!==last||t===last)&&P.records[i].parents.every(p=>seen.has(p)));
    assert(ready.length>0);
    n=(Math.imul(n,1664525)+1013904223)>>>0;
    const id=ready[n%ready.length];seen.add(id);order.push(id);
  }
  return permutation(P,order);
}
function run(packet){
  const logs=[];
  const fakeFs={readFileSync:()=>JSON.stringify(packet)};
  const fakeCrypto={createHash:()=>({update(){return this;},digest(){return 'output-only-synthetic-hash';}})};
  const fakeRequire=n=>n==='fs'?fakeFs:n==='crypto'?fakeCrypto:require(n);
  const count=new Function('require','process','console','structuredClone',
    source+'\nreturn tests;')(
      fakeRequire,{argv:['node','original-checker','packet.json']},
      {log:v=>logs.push(v)},cp);
  assert.strictEqual(logs.length,1);
  return count;
}
const before=run(P);
const def=P.records.map((r,i)=>r.kind==='DEF'?i:-1).filter(i=>i>=0);
const src=P.records.map((r,i)=>r.kind==='SOURCE'?i:-1).filter(i=>i>=0);
const res=P.records.map((r,i)=>r.kind==='RES'?i:-1).filter(i=>i>=0);
const facetBeforeAllSource=run(permutation(P,[...def,...src,...res]));
let accepted=0,total=0;const perSeed=[];
for(let seed=1;seed<=128;seed++){
  const assertions=run(topo(seed));
  accepted++;total+=assertions;
  if(seed<=3)perSeed.push({seed,assertions});
}
assert.strictEqual(accepted,128);
const output={
  status:'COMPUTATIONAL original archived /386 complete CLI wrapper replay',
  originalChecker: vf,
  originalCheckerGitBlob:'338305c0ce101704205e57543756b8127074a986',
  originalPacket:pf,
  originalPacketGitBlob:'08aa169b5db49b2ddd1cb5a9b6890fcc3b790916',
  baseCLIAssertions:before,facetBeforeAllSourceCLIAssertions:facetBeforeAllSource,
  randomTopologicalOrdersAccepted:accepted,randomCLISumAssertions:total,perSeed,
  bundledHostileMutationsPerAcceptedPacket:11,
  caveats:['Unchanged original math and CLI negative tests, fake fs and output-only SHA only.',
    'Hosted V8 replay previously executed; this standalone Node script syntax parsed, not OS-executed.',
    'Only the archived /386 sibling, not the missing full R_mix341 dispatcher.']
};
const txt=JSON.stringify(output,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(process.argv[2],txt);
process.stdout.write(txt);
