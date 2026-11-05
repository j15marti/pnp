#!/usr/bin/env node
'use strict';
// LSPV-4/398 independent, dependency-free 2SAT -> authenticated Resolution DAG.
// Tested separately against 1280 exhaustive-assignment truth labels.
const assert=require('assert');
function key(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function check(F){if(!Array.isArray(F))throw Error('bad formula');for(const c of F){if(!Array.isArray(c)||!c.length||c.length>2||c.some(x=>!Number.isSafeInteger(x)||!x)||new Set(c).size!==c.length||c.some(x=>c.includes(-x)))throw Error('bad clause')}return F.map(key)}
function edges(F){let A=new Map();function add(u,v,i){if(!A.has(u))A.set(u,[]);A.get(u).push([v,i])};F.forEach((c,i)=>{if(c.length===1)add(-c[0],c[0],i);else{add(-c[0],c[1],i);add(-c[1],c[0],i)}});return A}
function path(A,s,t){let Q=[s],pos=0,P=new Map([[s,null]]);while(pos<Q.length){let u=Q[pos++];if(u===t)break;for(let [v,id] of A.get(u)||[]){if(!P.has(v)){P.set(v,[u,id]);Q.push(v)}}}if(!P.has(t))return null;let out=[];for(let u=t;u!==s;){let [prev,id]=P.get(u);out.push([prev,u,id]);u=prev}return out.reverse()}
function res(a,b,v){if(!a.includes(v)||!b.includes(-v))throw Error('pivot');let o=key([...a.filter(x=>x!==v),...b.filter(x=>x!==-v)]);if(o.some(x=>o.includes(-x)))throw Error('taut');return o}
function refute(input){let F=check(input),A=edges(F),names=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b);
 for(let x of names){let P=path(A,x,-x),Q=path(A,-x,x);if(!P||!Q)continue;let steps=[];
 function emit(edges,s){let c=F[edges[0][2]],idx=edges[0][2];for(let [u,v,id] of edges.slice(1)){c=res(c,F[id],u);steps.push({a:idx,b:id,p:u,c});idx=F.length+steps.length-1;if(c.length===1&&c[0]===-s)break}assert.deepStrictEqual(c,[-s]);return idx}
 let a=emit(P,x),b=emit(Q,-x),nodes=[...F,...steps.map(s=>s.c)];steps.push({a,b,p:-x,c:res(nodes[a],nodes[b],-x)});assert(!steps.at(-1).c.length);assert(steps.length<=4*names.length-3);return {source:F,steps,bound:4*names.length-3}}
 return null}
function verify(pr){let nodes=check(pr.source);for(let s of pr.steps){if(!Number.isInteger(s.a)||!Number.isInteger(s.b)||s.a<0||s.b<0||s.a>=nodes.length||s.b>=nodes.length)throw Error('bad source address');let q=res(nodes[s.a],nodes[s.b],s.p);assert.deepStrictEqual(q,s.c);nodes.push(q)}assert(!nodes.at(-1).length);return true}
function models(F){let names=[...new Set(F.flat().map(Math.abs))],n=names.length,k=0;for(let m=0;m<(1<<n);m++)if(F.every(c=>c.some(x=>Boolean((m>>names.indexOf(Math.abs(x)))&1)===(x>0))))k++;return k}
let checks=0,sat=0,unsat=0;let states=20261104;function rand(){states=(Math.imul(states,1664525)+1013904223)>>>0;return states}
for(let n=1;n<=8;n++){let lits=[];for(let i=1;i<=n;i++)lits.push([i],[-i]);for(let i=1;i<=n;i++)for(let j=i+1;j<=n;j++)for(let a of [-1,1])for(let b of [-1,1])lits.push(key([a*i,b*j]));
for(let t=0;t<160;t++){let clauses=lits.slice(),m=rand()%(Math.min(lits.length,3*n)+1);for(let i=0;i<m;i++){let j=i+rand()%(clauses.length-i);[clauses[j],clauses[i]]=[clauses[i],clauses[j]]}let F=clauses.slice(0,m),p=refute(F),cnt=models(F);assert.equal(Boolean(p),cnt===0);checks++;if(p){verify(p);checks++;unsat++}else sat++}}
let bad=0;for(let F of [[[0]],[[1,1]],[[1,-1]],[[1,2,3]],[[true]],[[1.4]],[[1],[]],'garbage']){try{refute(F)}catch(e){bad++;continue}throw Error('accepted malformed')}
console.log(JSON.stringify({status:'PASS',seed:20261104,cases:1280,sat,unsat,checks,malformed_rejected:bad,bound:'4n-3',optimum_claim:false},null,2));
