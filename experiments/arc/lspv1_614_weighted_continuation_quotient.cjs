#!/usr/bin/env node
'use strict';
/* LSPV-1/614: weighted continuation right-congruence controls.
 * Pure finite transition automata, NOT historical R_mix341.
 * Exhaustive all two-state (2-symbol, weights 0/1) partial deterministic machines,
 * plus seeded 3..5-state controls. Every concrete action's unit or zero
 * marginal cost is paid once in the toy history-specific model.
 */
const assert = require('node:assert/strict');
const alphabet = ['a','b'];
let seed = 0x6145a7;
function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
function machine(n, goal, cells){
  return {n,goal,step: Array.from({length:n},(_,i)=>cells.slice(2*i,2*i+2))};
}
function wordTrace(M,start,word){
  let s=start,cost=0;
  for (const a of word){const k=alphabet.indexOf(a),e=M.step[s][k];if(e===null)return {valid:false};cost+=e.w;s=e.to;}
  return {valid:true,cost,goal:M.goal[s]};
}
function signaturePartitions(M){
  let cls=M.goal.map(x=>x?1:0),rounds=0;
  while(true){
    const keys=M.goal.map((g,i)=>JSON.stringify([Number(g),...M.step[i].map(e=>e===null?null:[e.w,cls[e.to]])]));
    const d=new Map();const next=keys.map(k=>{if(!d.has(k))d.set(k,d.size);return d.get(k);});
    rounds++;
    if(next.every((v,i)=>v===cls[i]))return {cls,rounds,classes:new Set(cls).size};
    // Comparing literal numbers is unnecessary for equivalence; classes
    // assigned by first occurrence may be relabelled between passes.
    const eq=(a,b)=>a.every((x,i)=>a.every((y,j)=>(x===y)===(b[i]===b[j])));
    if(eq(next,cls))return {cls:next,rounds,classes:new Set(next).size};
    cls=next;
    assert(rounds<=M.n+2,'nonconvergent partition');
  }
}
function allWords(max){let words=[[]],layer=[[]];for(let k=1;k<=max;k++){layer=layer.flatMap(w=>alphabet.map(a=>[...w,a]));words.push(...layer);}return words;}
function exactSuffixEquivalent(M,i,j,words){
  for (const w of words){const x=wordTrace(M,i,w),y=wordTrace(M,j,w);
    if(x.valid!==y.valid)return false;
    if(x.valid&&(x.cost!==y.cost||x.goal!==y.goal))return false;
  }return true;
}
let automata=0,pairs=0,assertions=0,maxRounds=0,classHistogram={};
function audit(M){
  const q=signaturePartitions(M),words=allWords(M.n-1);maxRounds=Math.max(maxRounds,q.rounds);
  for(let i=0;i<M.n;i++)for(let j=i;j<M.n;j++){
    const ex=exactSuffixEquivalent(M,i,j,words),pt=q.cls[i]===q.cls[j];
    assert.equal(pt,ex,`quotient versus all suffixes n=${M.n} ${i},${j}`);assertions++;pairs++;
  }
  for(let i=0;i<M.n;i++)for(let a=0;a<2;a++)for(let j=0;j<M.n;j++)if(q.cls[i]===q.cls[j]){
    const x=M.step[i][a],y=M.step[j][a];
    assert.equal(x===null,y===null);assertions++;
    if(x){assert.equal(x.w,y.w);assert.equal(q.cls[x.to],q.cls[y.to]);assertions+=2;}
  }
  automata++;classHistogram[q.classes]=(classHistogram[q.classes]||0)+1;
}
// 5 choices per transition: absent, or one of 2 targets x 2 weights.
const options2=[null,...[0,1].flatMap(to=>[0,1].map(w=>({to,w})))];
for(let flags=0;flags<4;flags++)for(let code=0;code<625;code++){
  let v=code,cells=[];for(let k=0;k<4;k++){cells.push(options2[v%5]);v=Math.floor(v/5);}
  audit(machine(2,[Boolean(flags&1),Boolean(flags&2)],cells));
}
for(let n=3;n<=5;n++)for(let run=0;run<500;run++){
  const cells=Array.from({length:2*n},()=>{
    const z=rnd()%(1+3*n);return z===0?null:{to:rnd()%n,w:rnd()%3};
  });
  audit(machine(n,Array.from({length:n},()=>Boolean(rnd()&1)),cells));
}
// Native-calculus-relevant toy witnesses: paid history, branch scope, source.
const toy = {
  n:7,
  goal:[false,false,true,false,false,false,false],
  step:[
    [{to:2,w:1},null], // s0: owner not previously paid
    [{to:2,w:0},null], // s1: owner already paid
    [null,null],        // completed goal
    [null,{to:2,w:0}], // s3: properly discharged branch
    [null,null],        // s4: unresolved assumption
    [{to:2,w:0},null], // s5: source-compatible closure
    [null,null]         // s6: same raw proof line, different external source
  ]
};
const toyQ=signaturePartitions(toy);
assert.notEqual(toyQ.cls[0],toyQ.cls[1]);assertions++;
assert.notEqual(toyQ.cls[3],toyQ.cls[4]);assertions++;
assert.notEqual(toyQ.cls[5],toyQ.cls[6]);assertions++;
assert.deepEqual(wordTrace(toy,0,['a']),{valid:true,cost:1,goal:true});assertions++;
assert.deepEqual(wordTrace(toy,1,['a']),{valid:true,cost:0,goal:true});assertions++;
assert.deepEqual(wordTrace(toy,4,['b']),{valid:false});assertions++;
const MAYmergedMin=Math.min(toy.step[0][0].w,toy.step[1][0].w);
assert.equal(MAYmergedMin,0);assertions++;
// A sound MAY quotient has its goal distance <= both concrete distances, but is not exact on s0.
assert(MAYmergedMin<=wordTrace(toy,0,['a']).cost);assertions++;
const output={report:'LSPV-1/614',status:'PROVED/RESTRICTED symbolic theorem + COMPUTATIONAL',
 source:'self-contained deterministic weighted prefix machines; not historical R_mix341',
 seed:'0x6145a7',alphabet, exhaustive_two_state:2500,random_per_size:500,
 automata,pairs,assertions,maxRounds,classHistogram,
 toy: {paid_first:wordTrace(toy,0,['a']),paid_cached:wordTrace(toy,1,['a']),
       scope_discharge:wordTrace(toy,3,['b']),scope_unresolved:wordTrace(toy,4,['b']),
       source_bound:wordTrace(toy,5,['a']),source_unbound:wordTrace(toy,6,['a']),
       quotient_classes:toyQ.cls,merged_min_cost:MAYmergedMin},
 historical_checker_executed:false, p2_d1:'OPEN',p2_c3:'OPEN',p2_b1:'OPEN',p2_b2_b3:'OPEN',p_vs_np:'OPEN'};
console.log(JSON.stringify(output,null,2));
