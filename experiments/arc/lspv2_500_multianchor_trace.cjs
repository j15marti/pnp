'use strict';
// LSPV-2/500: executable finite control for two trusted guest-trace anchors.
// This guest classifies ONLY original K4 odd-charge prefixes; it is not a general SAT solver.
const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], H='10110101010000000011000000';
let checks=0; function ok(x,m){if(!x)throw Error(m);checks++}
function core(charge){let out='';for(let v=0;v<4;v++){
 const ids=E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
 for(let z=0;z<8;z++){let b=[z>>2&1,z>>1&1,z&1];if((b[0]^b[1]^b[2])!==(v===charge?1:0))for(let k=0;k<3;k++)out+=b[k]+ids[k].toString(2).padStart(4,'0');}}
 ok(out.length===240,'original proper 3-CNF K4 core');return out;}
const cores=[core(0),core(1)];
function guest(x){let reads=[];function read(i){reads.push(i);return x[i]}
 let prefix='';for(let i=0;i<26+240;i++)prefix+=read(i);
 let body=prefix.slice(26),label=cores.includes(body)?'UNSAT':'OUTSIDE';
 return {label,reads:[...new Set(reads)].sort((a,b)=>a-b)};}
function labelCache(cap){let anchors=[],executed=0,reused=0,compare=0,peak=0;
 function query(src){for(let a of anchors){if(a.len!==src.length)continue;
  let match=true;for(let [pos,bit] of a.trace){compare++;if(src[pos]!==bit){match=false;break}}
  if(match){reused++;return a.label;}}
 const r=guest(src);executed++;if(cap){anchors.unshift({len:src.length,label:r.label,trace:r.reads.map(i=>[i,src[i]])});anchors=anchors.slice(0,cap);
 const bits=anchors.reduce((s,a)=>s+a.trace.length*(Math.ceil(Math.log2(src.length+1))+1)+16,0);peak=Math.max(peak,bits);}
 return r.label;}
 return {query,stats:()=>({cap,executed,reused,compare,peak})};}
let stores=[labelCache(0),labelCache(1),labelCache(2)];
let rng=500;function next(){rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng&1}
for(let j=0;j<128;j++){
 let tail='';for(let k=0;k<2640;k++)tail+=next();
 let src=H+cores[j%2]+tail;ok(src.length===2906,'full child length');ok(parseInt(src.slice(8,14),2)===16&&parseInt(src.slice(14,26),2)===192,'header');
 for(let s of stores)ok(s.query(src)==='UNSAT','core UNSAT retained');}
const s=stores.map(c=>c.stats());ok(s[0].executed===128,'no cache');ok(s[1].executed===128,'one anchor no reuse');ok(s[2].executed===2 && s[2].reused===126,'two anchor reuse');
console.log(JSON.stringify({status:'PASS',checks,stats:s,scope:'finite trusted restricted guest; external records require complete replay; no general SAT/FLMV/R_mix341 claim'},null,2));
