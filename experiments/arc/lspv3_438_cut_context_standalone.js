#!/usr/bin/env node
/* LSPV-3/438 compact, independent theorem-control reproducer.
 * Rebuilds actual signed cubic Tseitin 3-CNF clauses and verifies cut projections.
 * Full source-attached AND3/XOR DAG and independent checker are in reproducibility ZIP.
 * NOT the historical R_mix341 accepted-byte parser.
 */
'use strict';
let checks=0;
function req(b,s){checks++;if(!b)throw Error(s||'verification failed')}
function bits(n){return Array.from({length:2**n},(_,k)=>Array.from({length:n},(_,i)=>(k>>i)&1))}
function graph(n){if(n==='K4')return [4,Array.from({length:4},(_,i)=>Array.from({length:4-i-1},(_,j)=>[i,i+j+1])).flat()];
 if(n==='Cube')return [8,Array.from({length:8},(_,i)=>[1,2,4].filter(b=>i<(i^b)).map(b=>[i,i^b])).flat()];
 if(n==='Petersen')return [10,[...Array(5)].flatMap((_,i)=>[[i,(i+1)%5],[i,i+5],[i+5,5+(i+2)%5]])];
 if(n==='Prism6')return [12,[...Array(6)].flatMap((_,i)=>[[i,(i+1)%6],[i+6,6+(i+1)%6],[i,i+6]])];throw Error(n)}
function build(name,k){const [h,edges]=graph(name),near=Array.from({length:h},()=>[]);
 edges.forEach(([a,b],i)=>{near[a].push(i+1);near[b].push(i+1)});req(near.every(x=>x.length===3),'cubic');
 const order=[0],seen=new Set(order);for(const v of order)for(const [a,b] of edges){const w=a===v?b:b===v?a:-1;if(w>=0&&!seen.has(w)){seen.add(w);order.push(w)}}
 const S=new Set(order.slice(0,k)),charge=Array(h).fill(0);charge[0]=1;
 const clauseSet=near.map((ed,v)=>bits(3).filter(x=>x.reduce((a,b)=>a^b,0)!==charge[v]).map(x=>ed.map((e,i)=>x[i]?-e:e)));
 req(clauseSet.every(x=>x.length===4),'four signed clauses per vertex');
 const boundary=[],inner=[];edges.forEach(([a,b],i)=>{if(S.has(a)!==S.has(b))boundary.push(i+1);if(S.has(a)&&S.has(b))inner.push(i+1)});req(boundary.length>=4,'high cut');
 const target=[...S].reduce((acc,v)=>acc^charge[v],0);
 function sat(a){return [...S].every(v=>clauseSet[v].every(cl=>cl.some(l=>l>0?a[l]===1:a[-l]===0)))}
 const allowed=new Set();for(const row of bits(boundary.length)){
  let yes=false;for(const col of bits(inner.length)){const a={};boundary.forEach((x,i)=>a[x]=row[i]);inner.forEach((x,i)=>a[x]=col[i]);if(sat(a)){yes=true;break}}
  req(yes===(row.reduce((a,b)=>a^b,0)===target),'exact original-source projection');if(yes)allowed.add(row.join(''));
 }
 for(let fixed=0;fixed<boundary.length;fixed++)for(const prefix of bits(fixed)){
  const good=[...allowed].filter(x=>x.slice(0,fixed)===prefix.join('')).map(x=>x.slice(fixed));
  req(good.length===2**(boundary.length-fixed-1),'context models');
  const free=boundary.length-fixed;let local=false;
  for(let mask=1;mask<(1<<free);mask++){if(mask.toString(2).replace(/0/g,'').length>3)continue;
   const positions=[...Array(free).keys()].filter(j=>(mask>>j)&1);
   for(const b of bits(positions.length))if(!good.some(s=>positions.every((j,i)=>+s[j]===b[i])))local=true;
  }
  req(local===(free<=3),'context-locality iff remaining <=3');
 }
 return {name,S:[...S].sort((a,b)=>a-b),cut_width:boundary.length,min_branch_leaves:2**(boundary.length-3),min_boundary_cnf:2**(boundary.length-1),original_source_clauses:4*h,mixed_semantic_upper_nodes:4*h-1};
}
const specs=[['K4',[2]],['Cube',[2,3,5]],['Petersen',[2,3,4]],['Prism6',[2,3,4,5]]];
const cases=[];for(const [g,ks] of specs)for(const k of ks)cases.push(build(g,k));
req(cases.length===11,'eleven cases');
console.log(JSON.stringify({status:'COMPUTATIONAL',checks,cases},null,2));
