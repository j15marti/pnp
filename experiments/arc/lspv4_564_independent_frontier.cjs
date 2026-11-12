'use strict';
/* LSPV-4/564: independently implemented Node.js recursive memoized order-ideal
   audit. This script is independent of the Python heap solver. The signed
   clauses/parent incidence are pinned to archived-/386 original W38 proof.
   Run from repository root: node experiments/arc/lspv4_564_independent_frontier.cjs
   This is a finite fixed-DAG theorem, not a full mixed-rule SAT lower bound.
*/
const assert=require('assert');
const parents=[[],[0],[1],[2],[3],[4],[0],[],[6],[],[5],[],[],[],[],[10],[11],[9],[13],[7],[8],[12],[14],[21,17],[20,18],[16,19],[15,22],[26],[23],[24],[25],[29,28],[27,30],[31,32],[33]];
const sizes=[13,13,14,13,13,13,13,12,14,14,16,14,14,14,14,15,13,14,14,12,15,15,14,12,12,10,12,9,9,10,8,7,6,4,2];
const N=parents.length,full=(1n<<BigInt(N))-1n;
const succ=Array.from({length:N},()=>new Set());
parents.forEach((ps,j)=>ps.forEach(p=>succ[p].add(j)));
const has=(mask,j)=>(mask&(1n<<BigInt(j)))!==0n;
function solve(limit) {
 const memo=new Map(),choice=new Map();let transitions=0;
 function dfs(mask) {
   if(mask===full)return [0,0];
   const k=mask.toString();
   if(memo.has(k))return memo.get(k);
   const live=[];
   for(let j=0;j<N;j++)if(has(mask,j)&&[...succ[j]].some(v=>!has(mask,v)))live.push(j);
   const bytes=live.reduce((s,i)=>s+sizes[i],0);
   let best=null;
   for(let j=0;j<N;j++){
     if(has(mask,j)||!parents[j].every(p=>has(mask,p)))continue;
     const overwrite=parents[j].some(p=>sizes[p]>=sizes[j]&&[...succ[p]].every(v=>has(mask,v)||v===j));
     const demand=bytes+(overwrite?0:sizes[j]);
     const registers=live.length+(overwrite?0:1);
     if(registers>4||demand>limit)continue;
     transitions++;
     const remaining=dfs(mask|(1n<<BigInt(j)));
     if(remaining===null)continue;
     const c=[bytes+remaining[0],live.length+remaining[1]];
     if(best===null||c[0]<best[0]||(c[0]===best[0]&&c[1]<best[1])){
       best=c;choice.set(k,j);
     }
   }
   memo.set(k,best);
   return best;
 }
 const optimum=dfs(0n);
 let order=[];
 if(optimum){
   let m=0n;
   while(m!==full){const j=choice.get(m.toString());assert(Number.isInteger(j));order.push(j);m|=1n<<BigInt(j)}
   assert.strictEqual(order.at(-1),34);
 }
 return {max_peak:limit,reachable:optimum!==null,visited_nonterminal:memo.size,transitions,
 post_byte_area:optimum?optimum[0]+2:null,post_slot_area:optimum?optimum[1]+1:null,order};
}
const results=[44,45,46,47,48,49,50,51,1000].map(solve);
assert.deepStrictEqual(results.map(x=>[x.max_peak,x.post_byte_area,x.post_slot_area]),
 [[44,null,null],[45,958,87],[46,958,87],[47,958,87],
  [48,958,87],[49,958,87],[50,927,87],[51,885,83],[1000,885,83]]);
console.log(JSON.stringify({result_type:'exact finite-state independent recursion',results},null,2));
