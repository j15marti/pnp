#!/usr/bin/env node
'use strict';
// Signed expander camouflage 347: self-contained source producer and independent RES replay.
// Run: node lspv3_347_signed_cube_referee.js
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const norm=a=>{if(a.some(x=>!Number.isInteger(x)||x===0)||new Set(a).size!==a.length||a.some(x=>a.includes(-x)))throw Error('invalid clause');return a.slice().sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x)};
function res(A,B,p){if(!(A.includes(p)&&B.includes(-p))){if(!(B.includes(p)&&A.includes(-p)))throw Error('bad pivot');[A,B]=[B,A]}return norm([...new Set([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)])])}
function graph(k){if(k===4)return [4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]];
if(k===8){let E=[];for(let a=0;a<8;a++)for(let b=a+1;b<8;b++){let x=a^b;if(!(x&(x-1)))E.push([a,b])}return [8,E]}
let p=k/2,E=[];for(let a=0;a<p;a++){E.push([a,(a+1)%p],[a+p,(a+1)%p+p],[a,a+p])}
return [k,E.map(e=>e.sort((a,b)=>a-b)).sort((a,b)=>a[0]-b[0]||a[1]-b[1])]}
function build(h){let [v,E]=graph(h),t=E.length,src=[],tag=[],guard=[],gates=[],proof=[];
const add=(a,kind)=>{src.push(norm(a));tag.push(kind);return src.length-1};
for(let e=0;e<t;e++){let [u,w]=E[e],L=[];for(let j=0;j<8;j++){let b=[j>>2&1,j>>1&1,j&1],xs=[u+1,w+1,v+e+1],y=v+t+e+1;L.push(add([y,...xs.map((x,i)=>b[i]?-x:x)],['cube',e,b]))}guard.push(L)}
let Q=E.map((_,e)=>v+t+e+1);while(Q.length>1){let [a,b]=Q.splice(0,2),z=v+2*t+gates.length+1,i=add([-a,-b,z],['gate']);gates.push([a,b,z,i]);Q.push(z)}
let root=Q[0],last=add([-root],['root']);
let get=i=>i<src.length?src[i]:proof[i-src.length].clause;
let infer=(a,b,p)=>{let clause=res(get(a),get(b),p);proof.push({a,b,p,clause});return src.length+proof.length-1};
let units=new Map();for(let e=0;e<t;e++){let [u,w]=E[e],vars=[v+e+1,w+1,u+1],cur=guard[e];for(let p of vars){let nx=[];for(let j=0;j<cur.length;j+=2)nx.push(infer(cur[j],cur[j+1],p));cur=nx}if(!eq(get(cur[0]),[v+t+e+1]))throw Error('cube failure');units.set(v+t+e+1,cur[0])}
for(let [a,b,z,i]of gates){let j=infer(i,units.get(a),a);units.set(z,infer(j,units.get(b),b))}infer(last,units.get(root),root);
return {v,E,t,src,tag,gates,root,proof,variables:v+3*t-1}}
function model(D,omit){let {v,t,E,gates,tag}=D,A=Array(D.variables+1).fill(false);for(let e=0;e<t;e++)A[v+t+e+1]=true;
if(omit!==null&&tag[omit][0]==='cube'){let [,e,b]=tag[omit],[u,w]=E[e];A[v+t+e+1]=false;[u+1,w+1,v+e+1].forEach((x,i)=>A[x]=Boolean(b[i]))}
for(let [a,b,z,i]of gates){A[z]=A[a]&&A[b];if(omit===i)A[z]=false}return A}
const sat=(c,A)=>c.some(l=>A[Math.abs(l)]===(l>0));
function dimacs(D){return 'p cnf '+D.variables+' '+D.src.length+'\n'+D.src.map(c=>c.join(' ')+' 0\n').join('')}
function parse(s){let a=s.trimEnd().split('\n'),h=/^p cnf ([1-9]\d*) ([1-9]\d*)$/.exec(a[0]);if(!h||a.length!==Number(h[2])+1)throw Error('header');
let cs=[];for(let l of a.slice(1)){if(!/^-?[1-9]\d*( -?[1-9]\d*)* 0$/.test(l))throw Error('line');let c=l.split(' ').map(Number);c.pop();if(c.some(x=>Math.abs(x)>Number(h[1])))throw Error('range');cs.push(norm(c))}return cs}
function check(D){let {v,E,t,src,tag,gates,proof,variables}=D,a=0;const ok=(b,msg)=>{a++;if(!b)throw Error(msg)};
ok(src.length===9*t&&proof.length===9*t-1,'size');ok(variables===v+3*t-1,'variable count');
let txt=dimacs(D);ok(eq(parse(txt),src),'DIMACS');
let header='p cnf '+variables+' '+src.length;
let bad=[txt.replace(header,'p cnf '+variables+' '+(src.length+1)),txt.replace(header,'p cnf '+(variables-1)+' '+src.length),txt.replace(' 0\n','\n'),txt.replace(' 0\n',' 1 0\n'),txt.replace('p cnf','q cnf'),txt.replace(' 0\n',' 1 -1 0\n'),txt.replace(' 0\n',' 999999 0\n'),txt+'extra\n'];
for(let z of bad){let failed=false;try{parse(z)}catch{failed=true}ok(failed,'bad syntax accepted')}
for(let e=0;e<t;e++){let [u,w]=E[e];for(let j=0;j<8;j++){let b=[j>>2&1,j>>1&1,j&1],xs=[u+1,w+1,v+e+1];ok(eq(src[8*e+j],norm([v+t+e+1,...xs.map((x,i)=>b[i]?-x:x)])),'signed source')}}
let lines=src.map(x=>x.slice());for(let z of proof){ok(z.a>=0&&z.b>=0&&z.a<lines.length&&z.b<lines.length,'acyclic');ok(eq(res(lines[z.a],lines[z.b],z.p),z.clause),'RES replay');lines.push(z.clause)}
ok(lines.at(-1).length===0,'no empty clause');
let used=new Set(),stack=[lines.length-1];while(stack.length){let i=stack.pop();if(used.has(i))continue;used.add(i);if(i>=src.length)stack.push(proof[i-src.length].a,proof[i-src.length].b)}ok(src.every((_,i)=>used.has(i)),'missing source');
let flips=0;for(let i=0;i<src.length;i++){let A=model(D,i);ok(src.every((c,j)=>j===i||sat(c,A)),'deletion witness');ok(!sat(src[i],A),'deleted false');
for(let j=0;j<src[i].length;j++){let c=src[i].slice();c[j]=-c[j];ok(src.every((d,k)=>sat(k===i?c:d,A)),'signed flip');flips++}}
let A=model(D,null);ok(src.every((c,i)=>sat(i===src.length-1?[-c[0]]:c,A)),'matched SAT');
for(let i of [0,Math.floor(proof.length/2),proof.length-1]){let z=proof[i],failed=false;try{res(lines[z.a],lines[z.b],variables+500)}catch{failed=true}ok(failed,'bad pivot accepted')}
for(let c of [[1,1],[1,-1],[0],[1,0]]){let failed=false;try{norm(c)}catch{failed=true}ok(failed,'bad clause accepted')}
let mincut=Infinity;for(let mask=1;mask<(1<<v)-1;mask++){let k=0;for(let i=0;i<v;i++)k+=mask>>i&1;if(k<Math.ceil(v/3)||k>Math.floor(v/2))continue;let z=E.filter(([u,w])=>Boolean(mask&(1<<u))!==Boolean(mask&(1<<w))).length;mincut=Math.min(z,mincut)}
return {vertices:v,edges:t,variables,clauses:src.length,derived:proof.length,source_deletion_witnesses:src.length,sign_flip_witnesses:flips,min_terminal_cut:mincut,assertions:a}}
const results=[4,6,8,10].map(h=>check(build(h)));
console.log(JSON.stringify({id:'LSPV3_SIGNED_EXPANDER_CAMOUFLAGE347',status:'FINITE COMPUTATIONAL controls; mathematical exact theorem in companion report',results},null,2));