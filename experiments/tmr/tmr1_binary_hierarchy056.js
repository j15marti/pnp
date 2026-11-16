'use strict';
// TMR-1/056. Deterministic finite exact tests for the binary-input witness lift.
// Run: node tmr1_binary_hierarchy056.js
const crypto = require('crypto');
const SEED = 20261115;
let state = SEED >>> 0;
function next() {state ^= state << 13; state ^= state >>> 17; state ^= state << 5; return state >>> 0;}
function assert(x,m) {stats.assertions++; if (!x) throw Error(m);}
const stats={revision:'tmr1-binary-hierarchy056.v1',seed:SEED,junta_cases:0,junta_truth_evaluations:0,junta_queries:0,source_instances:0,assignments:0,all_candidate_checks:0,checker_evaluations:0,violated_checker_count_checks:0,assertions:0,failures:0};
function bits(v,n){return Array.from({length:n},(_,j)=>(v>>>j)&1)}
function combMasks(n,k){let out=[];for(let m=0;m<(1<<n);m++){let x=m,c=0;while(x){c+=x&1;x>>>=1;}if(c<=k)out.push(m)}return out}
function recoverJunta(f,n,w){
  if(w>n || n>20)throw Error('invalid');
  const support=[];const sparse=combMasks(n,w-1);
  for(let j=0;j<n;j++){
    let relevant=false;
    for(const z of sparse){if((z&(1<<j))!==0)continue;
      const left=f(z),right=f(z|(1<<j));stats.junta_queries+=2;
      if(left!==right){relevant=true;break;}
    }
    if(relevant)support.push(j);
  }
  if(support.length>w)throw Error('not a w-junta');
  const table=[];
  for(let t=0;t<(1<<support.length);t++){
    let m=0;for(let j=0;j<support.length;j++)if(t&(1<<j))m|=1<<support[j];
    table.push(f(m));stats.junta_queries++;
  }
  return {support,table,eval:(v)=>{let t=0;for(let j=0;j<support.length;j++)if(v&(1<<support[j]))t|=1<<j;return table[t]}};
}
// Any Boolean w-junta is recoverable from the low-weight Hamming ball;
// exact source implementation is charged for each black-box gate evaluation.
for(let n=3;n<=11;n++)for(let z=0;z<55;z++){
  const w=1+(next()%Math.min(3,n));
  const order=Array.from({length:n},(_,i)=>i);
  for(let i=n-1;i>0;i--){const j=next()%(i+1);[order[i],order[j]]=[order[j],order[i]]}
  const selected=order.slice(0,w),table=Array.from({length:1<<w},()=>next()&1);
  const f=(m)=>{let a=0;for(let j=0;j<w;j++)if(m&(1<<selected[j]))a|=1<<j;return table[a]};
  const r=recoverJunta(f,n,w);stats.junta_cases++;
  for(let m=0;m<(1<<n);m++) {assert(f(m)===r.eval(m),'junta reconstruction');stats.junta_truth_evaluations++}
  assert(r.support.length<=w,'support size');
}
// Small authentic clause-index-to-violation toy. A real fixed x is part of the
// address family and NOT an uncharged unary 1^n instance.
const v=3,L=3;
const sat=(clauses,a)=>clauses.every(c=>c.some(l=>((a>>Math.abs(l)-1)&1)===(l>0?1:0)));
function clausesOf(x,n){
  const cs=(x&1) ? [[1],[-1],[2,3],[-3,2]] : [[1],[-1,2],[3,1],[-2,3]];
  if(n>3 && (x&2))cs[3]=[2,-3];
  return cs;
}
function encodeClause(clause){const width=3*(1+2+1),bitsOut=Array(width).fill(0);
 for(let j=0;j<Math.min(3,clause.length);j++){
    const lit=clause[j]; const code=Math.abs(lit);const off=j*4;
    bitsOut[off]=1; bitsOut[off+1]=code&1;bitsOut[off+2]=(code>>1)&1;bitsOut[off+3]=lit<0?1:0;
 }return bitsOut;
}
function decodeClause(b){let out=[];for(let j=0;j<3;j++){
  let off=j*4;if(!b[off])continue;let ix=b[off+1]+2*b[off+2];if(ix<1||ix>v)throw Error('bad slot');out.push(b[off+3]?-ix:ix);
}return out}
for(let n=3;n<=5;n++)for(let x=0;x<(1<<n);x++){
  const clauses=clausesOf(x,n); const raw=Array.from({length:1<<L},(_,j)=>encodeClause(clauses[j%clauses.length]));
  const dec=Array.from({length:12},(_,b)=>recoverJunta(i=>raw[i][b],L,L));
  const encodedAt=i=>dec.map(d=>d.eval(i));
  for(let i=0;i<(1<<L);i++)assert(JSON.stringify(encodedAt(i))===JSON.stringify(raw[i]),'clause decoder');
  const decoded=Array.from({length:1<<L},(_,j)=>decodeClause(encodedAt(j)));
  const satisfying=[];
  for(let a=0;a<(1<<v);a++)if(sat(clauses,a))satisfying.push(a);
  const lex=satisfying.length?satisfying[0]:0;
  const Wbit=(i)=> (lex>>i)&1; // binary x is present in source; fixing x specializes W(x,i).
  let zeros=0;
  for(let a=0;a<(1<<v);a++){
    let violating=0;
    for(let j=0;j<(1<<L);j++){
      const bad=!sat([decoded[j]],a);if(bad)violating++;
      stats.checker_evaluations++;assert(bad===!sat([clauses[j%4]],a),'decoder semantic');
    }
    assert((violating===0)===sat(clauses,a),'checker zero iff witness');
    stats.violated_checker_count_checks++;
    if(violating===0)zeros++;
    stats.all_candidate_checks++;
  }
  assert((zeros>0)===(satisfying.length>0),'exists candidate equivalence');
  if(satisfying.length)assert(Array.from({length:v},(_,j)=>Wbit(j)).every((b,j)=>b===((lex>>j)&1)),'witness specialization');
  stats.assignments+=1<<v;stats.source_instances++;
}
const canonical=JSON.stringify(stats,null,2)+'\n';
process.stdout.write(canonical);
