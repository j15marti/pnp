#!/usr/bin/env node
// Independent standard-Node reproducer of signed source family and delayed INDEX.
// Proof nodes have unit cost; no SAT oracle or hidden semantic inference.
const assert=require('assert').strict;
let checks=0;
const ok=(p)=>{assert(p);checks++};
function source(x){let u=[...x].map((b,i)=>[b==='1'?i+1:-(i+1)]);return [...u,u.map(a=>-a[0])]}
function holds(F,mask){return F.every(c=>c.some(v=>(((mask>>(Math.abs(v)-1))&1)===(v>0?1:0))))}
function count(F,L){let s=0;for(let a=0;a<(1<<L);a++)if(holds(F,a))s++;return s}
function replay(F){let c=[...F.at(-1)];for(let i=0;i<F.length-1;i++){ok(c.includes(-F[i][0]));c=c.filter(v=>v!==-F[i][0])}ok(c.length===0)}
const rows=[];
for(let L=1;L<=9;L++){
 let dels=0,flips=0;
 for(let mask=0;mask<(1<<L);mask++){
  let x=Array.from({length:L},(_,i)=>((mask>>i)&1)?'1':'0').join('');
  const F=source(x);ok(count(F,L)===0);replay(F);
  for(let j=0;j<=L;j++){
   let p=j===L?mask:mask^(1<<j);
   ok(holds(F.filter((_,i)=>i!==j),p));dels++;
  }
  for(let j=0;j<=L;j++)for(let t=0;t<F[j].length;t++){
   let G=F.map(c=>[...c]);G[j][t]*=-1;
   ok(holds(G,j===L?mask:mask^(1<<j)));flips++;
  }
 }
 // Every distinct source pair has a distinguishing delayed query.
 let pairs=0;
 for(let a=0;a<(1<<L);a++)for(let b=0;b<a;b++){
  let diff=a^b, i=Math.floor(Math.log2(diff&-diff));
  ok(((a>>i)&1)!==((b>>i)&1));pairs++;
 }
 rows.push({L,variants:1<<L,exact_minimum_mixed_nodes:L,
   distinct_one_pass_states:1<<L,source_deletion_SAT_demos:dels,
   occurrence_sign_flip_SAT_demos:flips,separated_pairs:pairs});
}
ok(rows.reduce((s,r)=>s+r.variants,0)===1022);
ok(rows.reduce((s,r)=>s+r.source_deletion_SAT_demos,0)===9216);
ok(rows.reduce((s,r)=>s+r.occurrence_sign_flip_SAT_demos,0)===16388);
// Strict delayed query syntax rejects malformed proof-sign claims.
function query(x,i,b){return /^[01]+$/.test(x)&&Number.isInteger(i)&&i>=0&&i<x.length&&(b===0||b===1)&&x[i]===String(b)}
for(let v of [['1a',0,1],['',0,0],['01',2,0],['01',-1,0],['01',0,3]])ok(!query(...v));
// Independent parity test of K4 Tseitin at charge 1 versus 0.
function k4(odd){const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],F=[];
 for(let v=0;v<4;v++){let ids=E.map((e,i)=>e.includes(v)?i+1:null).filter(z=>z);
  for(let a=0;a<8;a++){let parity=([0,1,2].reduce((s,j)=>s+((a>>j)&1),0))%2;
   if(parity!==(odd&&v===0?1:0))F.push(ids.map((j,k)=>((a>>k)&1)?-j:j));
  }
 }return F;
}
ok(count(k4(true),6)===0);ok(count(k4(false),6)===8);
const result={status:'PASS',assertions:checks,rows,scope:'INDEX lower bound applies ONLY to deterministic source-first exact late authentication, not SAT decision space'};
console.log(JSON.stringify({status:result.status,assertions:checks,variants:1022,low_space_warning:true},null,2));
if(process.argv[2])require('fs').writeFileSync(process.argv[2],JSON.stringify(result,null,2));
