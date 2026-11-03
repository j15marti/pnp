// ANDTREE-MITER362: deterministic pure-Resolution certificate generator.
// Usage: node lspv2_362_andtree_miter_public.js 6
'use strict';
const canon=a=>{let x=[...new Set(a)].sort((u,v)=>Math.abs(u)-Math.abs(v)||u-v);if(x.some(v=>!Number.isInteger(v)||!v||x.includes(-v)))throw Error('invalid/tautological clause');return x;};
function tree(n,kind){let leaves=Array.from({length:n},(_,i)=>i+1);if(kind==='comb'){let z=leaves[0];for(let v of leaves.slice(1))z=[z,v];return z;}function bal(a){if(a.length===1)return a[0];let k=a.length>>1;return [bal(a.slice(0,k)),bal(a.slice(k))];}return bal(leaves.reverse());}
function produce(n){if(!Number.isInteger(n)||n<2||n>64)throw Error('n must be 2..64');
let id=n,source=[],proof=[],gates=[],imp=new Map(),def=new Map();
const pair=(a,b)=>a+':'+b;
function build(t,side){if(typeof t==='number')return t;const a=build(t[0],side),b=build(t[1],side),o=++id;gates.push({side,a,b,o});return o;}
const p=build(tree(n,'comb'),'A'),q=build(tree(n,'balanced'),'B');
function src(c){source.push(canon(c));return source.length-1;}
for(const g of gates){imp.set(pair(g.o,g.a),src([-g.o,g.a]));imp.set(pair(g.o,g.b),src([-g.o,g.b]));def.set(g.o,src([g.o,-g.a,-g.b]));}
const dis=src([p,q]),con=src([-p,-q]);
const cl=i=>i<source.length?source[i]:proof[i-source.length].cl;
function resolve(i,j,pivot){const a=cl(i),b=cl(j);if(!a.includes(pivot)||!b.includes(-pivot))throw Error('invalid pivot');const c=canon(a.filter(x=>x!==pivot).concat(b.filter(x=>x!==-pivot)));const z=source.length+proof.length;proof.push({cl:c,parents:[i,j],pivot});return z;}
function direction(start,inSide,outSide,end){const active=new Map();
function down(o){const g=gates.find(g=>g.side===inSide&&g.o===o);if(!g)return;
for(const v of [g.a,g.b]){const e=imp.get(pair(o,v));active.set(v,o===start?e:resolve(active.get(o),e,o));down(v);}}
down(start);
for(const g of gates.filter(g=>g.side===outSide)){const u=resolve(active.get(g.a),def.get(g.o),g.a);const v=resolve(active.get(g.b),u,g.b);active.set(g.o,v);}return active.get(end);}
const e1=direction(p,'A','B',q),e2=direction(q,'B','A',p);
const u=resolve(dis,e2,q),v=resolve(e1,con,q),empty=resolve(u,v,p);
if(cl(empty).length||proof.length!==8*n-9||source.length!==6*n-4)throw Error('count/error');
return {id:'ANDTREE_MITER362',n,variables:id,source,proof,empty,rootA:p,rootB:q,lower:6*n-5,upper:8*n-9};}
function replay(d){let all=d.source.map(canon),n=d.source.length;
for(let i=0;i<d.proof.length;i++){const z=d.proof[i],x=z.parents[0],y=z.parents[1];if(!Number.isInteger(x)||!Number.isInteger(y)||x<0||y<0||x>=n+i||y>=n+i)throw Error('invalid pointers');const a=all[x],b=all[y],p=z.pivot;if(!a.includes(p)||!b.includes(-p))throw Error('invalid source/pivot');const got=canon(a.filter(v=>v!==p).concat(b.filter(v=>v!==-p)));if(got.join()!=canon(z.cl).join())throw Error('incorrect resolvent');all.push(got);}
if(d.empty!==all.length-1||all[all.length-1].length)throw Error('no empty clause');return true;}
if(require.main===module){let n=Number(process.argv[2]||6),d=produce(n);replay(d);console.log(JSON.stringify({n:d.n,variables:d.variables,sources:d.source.length,paid:d.proof.length,lower:d.lower,upper:d.upper,checker:'strict pivot replay'},null,2));}
module.exports={produce,replay};
