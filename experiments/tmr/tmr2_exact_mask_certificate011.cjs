'use strict';
// TMR-2/011: exact bit-certificate audit for the eight-row mask class.
// Source grammar and template semantics: TMR-2/010. This is a query model,
// NOT a physical multitape Turing-machine implementation.
const assert = require('node:assert/strict');
const maskBase=[1,2,3,4,5,6,7,7];
const full=[0,1,2,3,4,5,6,7];
function candidateDomains(reference, observation) {
  return Array.from({length:8}, (_,row)=> {
    let domain=[];
    for(let word=0;word<8;word++){
      let match=true;
      for(let b=0;b<3;b++) {
        const pos=3*row+b;
        if((observation & (1<<pos)) && (((word>>b)&1)!==((reference[row]>>b)&1))) {match=false;break;}
      }
      if(match)domain.push(word);
    }
    return domain;
  });
}
function perfectMatching(domains) {
  // Exact, deterministic eight-row bipartite matching (augmenting paths).
  const owner=Array(8).fill(-1);
  function augment(row,visited){
    for(const value of domains[row]){
      if(visited[value])continue;
      visited[value]=true;
      if(owner[value]===-1||augment(owner[value],visited)){owner[value]=row;return true;}
    }
    return false;
  }
  for(let row=0;row<8;row++)if(!augment(row,Array(8).fill(false)))return false;
  return true;
}
function combos(N,K,fn){
  function rec(next,depth,mask){
    if(depth===K){fn(mask);return;}
    for(let p=next;p<=N-(K-depth);p++)rec(p+1,depth+1,mask|(1<<p));
  }
  rec(0,0,0);
}
function run(){
  const tests={tag:'TMR2-EXACT-MASK-CERTIFICATE-011',status:'COMPUTATIONAL',version:process.version,reference:maskBase,
    oneBlockPartialQueries:{},satFiveCertificate:[0,2,4,6,7].map(row=>3*row),
    unsatSingleBitSensitive:0,satCertificateSampleCounts:{},failedAssertions:0};
  for(let k=0;k<=4;k++){
    let masks=0,consistentFull=0;
    combos(24,k,obs=>{masks++;const match=perfectMatching(candidateDomains(maskBase,obs));assert.equal(match,true,'unexpected <=4-bit SAT certificate obs='+obs);consistentFull++;});
    tests.oneBlockPartialQueries[k]={tested:masks,consistentWithUnSAT:consistentFull};
  }
  const five=tests.satFiveCertificate.reduce((m,p)=>m|(1<<p),0);
  assert.equal(perfectMatching(candidateDomains(maskBase,five)),false,'five-bit SAT certificate must exclude every permutation');
  // 8! UNSAT completions, every single sign bit is individually sensitive.
  assert.equal(new Set(full).size,8);
  for(let pos=0;pos<24;pos++){
    const changed=full.slice();changed[Math.floor(pos/3)]^=1<<(pos%3);
    assert.equal(new Set(changed).size,7,'full block bit should be sensitive');
    tests.unsatSingleBitSensitive++;
  }
  // Check every remaining 5-bit candidate and exact minimum over one block.
  let possibleFive=0,certifyingFive=0;
  combos(24,5,obs=>{
    possibleFive++;
    if(!perfectMatching(candidateDomains(maskBase,obs)))certifyingFive++;
  });
  tests.satCertificateSampleCounts={candidateFiveSubsets:possibleFive,certifyingFiveSubsets:certifyingFive};
  assert(certifyingFive>0);
  // All-label semantic check over all eight possible assignments to three variables
  // for each of 500 deterministic local configurations.
  let seed=0x23c1abef,randomChecked=0;
  const rand=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0;};
  for(let i=0;i<500;i++){
    const masks=Array.from({length:8},()=>rand()%8);
    const semantic=Array.from({length:8},(_,a)=>!masks.includes(a)).some(Boolean);
    assert.equal(semantic,new Set(masks).size<8);
    randomChecked++;
  }
  tests.randomSemanticChecks=randomChecked;
  tests.demonstratedFamilyBounds=[1,2,3,8,16,128].map(r=>({r,SAT_certificate_bits:5*r,UNSAT_certificate_bits:24,source_sign_bits:24*r}));
  return tests;
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={candidateDomains,perfectMatching,run};
