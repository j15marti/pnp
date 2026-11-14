#!/usr/bin/env node
'use strict';
// TMR-3/021 independent finite controls. No arbitrary-TM compiler is claimed.
const assert = require('node:assert/strict');
function parity(x){let v=0; for(const z of x) v^=(z==='1')?1:0; return v;}
function profile(x,kind){
  const p=parity(x);
  if(kind==='index') return x;
  if(kind==='parity') return String(p).repeat(x.length);
  if(kind==='parity-index') return [...x].map(b=>String(Number(b)^p)).join('');
  throw Error('kind');
}
function rank(L,kind){const S=new Set();for(let n=0;n<2**L;n++){const x=n.toString(2).padStart(L,'0');S.add(profile(x,kind));}return S.size;}
function satE3(x){assert(x.length%3===0);let mask=0;for(let j=0;j<x.length;j+=3)mask|=1<<parseInt(x.slice(j,j+3),2);return mask!==255;}
function signFlip(x,j){return x.slice(0,j)+(x[j]==='1'?'0':'1')+x.slice(j+1);}
function signProfile(x){return Array.from({length:x.length},(_,i)=>satE3(signFlip(x,i))?'1':'0').join('');}
function uniqueProfileRank(words,kind){return new Set(words.map(x=>profile(x,kind))).size;}
const rows=[];let assertions=0;
for(let L=1;L<=10;L++){
 const I=rank(L,'index'),P=rank(L,'parity'),X=rank(L,'parity-index');
 assert.equal(I,2**L);assertions++;
 assert.equal(P,2);assertions++;
 assert.equal(X,2**(L-(L%2)));assertions++;
 rows.push({L,INDEX:I,PARITY:P,XOR_PARITY_INDEX:X});
}
// A full-response-profile method can encode all L bits (INDEX) or only one (PARITY).
const e3Rows=[];
for(let r=1;r<=4;r++){
 const U=Array.from({length:8},(_,i)=>i.toString(2).padStart(3,'0').repeat(r)).join('');
 assert.equal(U.length,24*r);assertions++;
 assert.equal(satE3(U),false);assertions++;
 const pro=signProfile(U),expect=(r===1?'1':'0').repeat(24*r);
 assert.equal(pro,expect);assertions++;
 e3Rows.push({r,L:U.length,one_bit_flip_SAT_count:[...pro].filter(x=>x==='1').length});
}
// The footprint of a standard TM is not a readable symbol: visited-then-blank
// and never-visited have the same actual alphabet symbols at query time.
const tapeA={head:0, cells:new Map(), visited:new Set([0])};
const tapeB={head:0, cells:new Map(), visited:new Set([0,1])};
function read(t,i){return t.cells.get(i)??0;}
for(let i=-2;i<=2;i++){assert.equal(read(tapeA,i),read(tapeB,i));assertions++;}
assert.equal(tapeA.head,tapeB.head);assertions++;
assert.notEqual(tapeA.visited.size,tapeB.visited.size);assertions++;
// A deterministic adaptive query controller must replay identically on equal
// current physical symbols. Its legal actions are scans, writes and +/-1 moves.
function replay(tape,commands){const t={head:tape.head,cells:new Map(tape.cells)};let out='';for(const a of commands){
 if(a==='R') t.head++;
 else if(a==='L') t.head--;
 else if(a==='0'||a==='1') t.cells.set(t.head,Number(a));
 else if(a==='?') out+=read(t,t.head);
 else throw Error(a);
}return out;}
const programs=['?','R?','R1?L0?','L1R?R0?','RR?LL?','R1R1L?L0?'];
for(const pr of programs){assert.equal(replay(tapeA,pr),replay(tapeB,pr));assertions++;}
// The ordinary source tape INDEX port has a fully charged unary query:
// one move per index increment and one query read/return transition.
let unaryRuns=0,unarySteps=0,parityRuns=0;
for(let L=1;L<=8;L++) for(let n=0;n<2**L;n++){
  const x=n.toString(2).padStart(L,'0');
  for(let p=0;p<L;p++){
   let sourceHead=0,queryHead=0,steps=0,unary='1'.repeat(p)+'0';
   while(unary[queryHead]==='1'){sourceHead++;queryHead++;steps++;}
   assert.equal(x[sourceHead],x[p]);assertions++;
   assert.equal(steps+1,p+1);assertions++;
   unaryRuns++;unarySteps+=p+1;
   assert.equal(parity(x),Number(profile(x,'parity')[p]));assertions++;parityRuns++;
  }
}
// Exact proper-3CNF realization of the delayed INDEX response profile.
// A unit literal ell is forced by its four sign-completion clauses.
function unit3(v,positive){let ell={v,positive};const out=[];for(const su of [false,true])for(const sv of [false,true])out.push([ell,{v:0,positive:su},{v:1,positive:sv}]);return out;}
function evalLit(l,mask){const b=((mask>>l.v)&1)===1;return l.positive?b:!b;}
function sat3(clauses,nvars){for(let a=0;a<(1<<nvars);a++)if(clauses.every(c=>c.some(l=>evalLit(l,a))))return true;return false;}
let gadgetQueries=0,gadgetTests=0,gadgetDistinctChecks=0;
const gadgetRows=[];
for(let L=1;L<=6;L++){
 let profiles=new Set();
 for(let n=0;n<(1<<L);n++){
  const x=n.toString(2).padStart(L,'0');
  const base=[];
  for(let i=0;i<L;i++)base.push(...unit3(i+2,x[i]==='1'));
  assert.equal(base.length,4*L); assertions++;
  assert.equal(sat3(base,L+2),true); assertions++;gadgetTests++;
  let response='';
  for(let p=0;p<L;p++){
   const clauses=base.concat(unit3(p+2,true));
   assert.equal(clauses.length,4*(L+1));assertions++;
   for(const cl of clauses){assert.equal(new Set(cl.map(l=>l.v)).size,3);assertions++;gadgetDistinctChecks++;}
   const got=sat3(clauses,L+2);
   assert.equal(got,x[p]==='1');assertions++;gadgetTests++;gadgetQueries++;
   response+=got?'1':'0';
  }
  assert.equal(response,x);assertions++;
  profiles.add(response);
 }
 assert.equal(profiles.size,1<<L); assertions++;
 gadgetRows.push({L,formula_family_size:1<<L,distinct_sat_query_profiles:profiles.size});
}
const raw={status:'COMPUTATIONAL',model:'separate nonsensing local heads; finite control; full tape alphabet includes blank; query tape x-independent',rows,e3Rows,gadgetRows,gadgetQueries,gadgetTests,gadgetDistinctChecks,blankVisitedTest:{samePhysicalSymbols:true,differentVisitedFootprints:true,programs:programs.length},unaryRuns,unarySteps,parityRuns,assertions,failures:0};
console.log(JSON.stringify(raw,null,2));
