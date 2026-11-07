'use strict';
// LSPV-3/474 original-source cubic Tseitin strict-3CNF quotient-PC GF(3)
// Separate calculus, NOT the accepted native historical R_mix341 checker.
const assert=require('node:assert/strict');
const f=x=>(x%3+3)%3;
function add(a,b,c=1){let r=new Map(a);for(let [m,v] of b){let t=f((r.get(m)||0)+c*v);if(t)r.set(m,t);else r.delete(m)}return r}
function mv(a,v){let r=new Map(),b=1<<v;for(let [m,c] of a){let n=m|b,t=f((r.get(n)||0)+c);if(t)r.set(n,t);else r.delete(n)}return r}
function C(lits){let p=new Map([[0,1]]);for(let l of lits){let t=mv(p,Math.abs(l)-1);p=l<0?t:add(p,t,-1)}return p}
function graphs(){return {K4:[...Array(4)].map((_,i)=>[0,1,2,3].filter(j=>j!==i)),K33:[...Array(6)].map((_,i)=>i<3?[3,4,5]:[0,1,2]),cube:[...Array(8)].map((_,i)=>[i^1,i^2,i^4])}}
let count=0,controls=0,rows=[];
for(let [name,g] of Object.entries(graphs()))for(let odd of [true,false]){
let e=[...new Set(g.flatMap((adj,i)=>adj.map(j=>[Math.min(i,j),Math.max(i,j)].join(','))))].sort().map(s=>s.split(',').map(Number)),n=e.length;
let clauses=[];for(let v=0;v<g.length;v++){let idx=e.map((ij,i)=>ij.includes(v)?i+1:0).filter(Boolean).sort((a,b)=>a-b);assert.equal(idx.length,3);for(let mask=0;mask<8;mask++)if((mask.toString(2).split('1').length-1)%2!==(odd&&v===0?1:0))clauses.push(idx.map((i,j)=>mask&(1<<j)?-i:i))}
let P=C(clauses[0]),paid=0,peak=P.size;for(let cl of clauses.slice(1)){let Q=P;for(let l of cl){let R=mv(Q,Math.abs(l)-1);paid++;if(l>0){Q=add(Q,R,-1);paid++}else Q=R;peak=Math.max(peak,Q.size)}let T=add(P,Q,-1);peak=Math.max(peak,T.size);P=add(T,C(cl));paid+=2;peak=Math.max(peak,P.size)}
let sat=0;for(let a=0;a<(1<<n);a++){let hasBad=clauses.some(c=>c.every(l=>Boolean(a&(1<<(Math.abs(l)-1)))!==(l>0)));if(!hasBad)sat++;let val=0;for(let [m,b] of P)if((a&m)===m)val=f(val+b);assert.equal(val,Number(hasBad));count++}
assert.equal(clauses.length,4*g.length);assert.equal(sat===0,odd);assert.equal(P.size===1&&P.get(0)===1,odd);rows.push({graph:name,odd,clauses:clauses.length,variables:n,paid,peak,models:sat});count+=4;
if(odd){let damaged=clauses.slice(1);let satWithoutFirst=0;for(let a=0;a<(1<<n);a++)if(damaged.every(c=>c.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0))))satWithoutFirst++;assert(satWithoutFirst>0);controls++;}
}
let U=new Map(),growth=[];for(let i=0;i<5;i++){let cl=[3*i+1,3*i+2,3*i+3],t=C(cl),prod=new Map();for(let [m,a] of U)for(let [n,b] of t){let s=m|n,c=f((prod.get(s)||0)+a*b);if(c)prod.set(s,c);else prod.delete(s)}U=add(add(U,t),prod,-1);growth.push(U.size);assert.equal(U.size,7**(i+1)+1);count++}
console.log(JSON.stringify({status:'PASS',checks:count,negative_controls:controls,prefix_terms:growth,rows}));
