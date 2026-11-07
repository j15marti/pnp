#!/usr/bin/env node
'use strict';
// Restricted finite self-check; no historical R_mix341 execution.
function main() {
let checks=0,peelable=0,nonpeelable=0,fullspan=0,unsat=0,corruptRejected=0;
const ok=(v,msg)=>{if(!v)throw Error(msg);checks++};
function combos(n,k){let out=[];function rec(i,a){if(a.length===k){out.push([...a]);return}for(;i<=n-k+a.length;i++){a.push(i);rec(i+1,a);a.pop()}}rec(0,[]);return out}
function clauses(n){let out=[];for(let t of combos(n,3))for(let b=0;b<8;b++)out.push(t.map((v,j)=>(b>>j&1)?-(v+1):v+1));return out}
function peel(F,n){let live=new Set(F.map((_,i)=>i)),steps=0;while(live.size){let degree=Array(n).fill(0),owner=Array(n).fill(-1);for(let j of live)for(let l of F[j]){let v=Math.abs(l)-1;degree[v]++;owner[v]=j}let j=-1;for(let v=0;v<n;v++)if(degree[v]===1){j=owner[v];break}if(j<0)break;live.delete(j);steps++}return {yes:!live.size,steps,core:live.size}}
function sat(F,a){return F.every(c=>c.some(l=>l>0?((a>>(l-1))&1):!((a>>(-l-1))&1)))}
function span(M,n){if(!M.length)return -1;let basis=Array(n).fill(0),r=0;for(let x of M){let y=x^M[0];while(y){let b=31-Math.clz32(y);if(basis[b])y^=basis[b];else{basis[b]=y;r++;break}}}return r}
function audit(F,n){let p=peel(F,n),M=[];for(let a=0;a<2**n;a++)if(sat(F,a))M.push(a);let r=span(M,n);if(p.yes){peelable++;ok(M.length>0,'SAT');ok(r===n,'affine span')}else nonpeelable++;if(r===n)fullspan++;if(!M.length)unsat++;return {peel:p,models:M.length,rank:r}}
for(let n of [4,5]){let cs=clauses(n),max=n===4?4:3;for(let k=0;k<=max;k++)if(!k)audit([],n);else for(let ix of combos(cs.length,k))audit(ix.map(j=>cs[j]),n)}
let seed=0x5eeda1f;function draw(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
for(let [n,t] of [[6,2400],[8,1800]]){let cs=clauses(n);for(let i=0;i<t;i++){let k=1+draw(n===6?11:14),I=new Set();while(I.size<k)I.add(draw(cs.length));audit([...I].map(j=>cs[j]),n)}}
let parity=audit([[1,2,3],[1,2,-3],[-1,-2,4],[-1,-2,-4]],4);ok(!parity.peel.yes&&parity.rank===3,'parity witness');
let unsat3=audit(clauses(3),3);ok(!unsat3.models&&!unsat3.peel.yes,'8 clause unsat');
function valid(F,n){return Array.isArray(F)&&F.every(c=>Array.isArray(c)&&c.length===3&&c.every(l=>Number.isInteger(l)&&l!==0&&Math.abs(l)<=n)&&new Set(c.map(Math.abs)).size===3)}
for(let F of [[[0,1,2]],[[1,1,2]],[[1,-1,3]],[[1,2,5]],[[1,2]],[[1,2,3.5]]]){ok(!valid(F,4),'malformed');corruptRejected++}
return {schema:'LSPV1_473_PeelAffine/v1',seed:'0x5eeda1f',status:'COMPUTATIONAL',checks,peelable,nonpeelable,fullspan,unsat,corruptRejected,parity,unsat3,scope:'exhaustive n4 <=4 clauses, n5 <=3 clauses; deterministic n6,n8 controls; not R_mix341'};
}
console.log(JSON.stringify(main()));
