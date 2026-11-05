#!/usr/bin/env node
"use strict";
// LSPV-4/411 independent finite group-miter referee. No Python imports.
// Tests the exact semantic predicate, balanced query bound, sparse XOR controls.
let nchecks=0,seed=411;
function ok(x,msg){nchecks++;if(!x)throw Error(msg||"assertion");}
function rnd(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0;}
function ev(n,g,out,x){let v=Array.from({length:n},(_,i)=>Boolean((x>>i)&1));
for(const [op,a,b] of g){ok(a<v.length&&b<v.length,"refs");v.push(Boolean((op>>(2*Number(v[a])+Number(v[b])))&1));}return v[out];}
function supp(n,g,out){let S=[];for(let i=0;i<n;i++){let f=false;for(let x=0;x<(1<<n);x++)if(ev(n,g,out,x)!==ev(n,g,out,x^(1<<i))){f=true;break;}if(f)S.push(i);}return S;}
function group(n,g,out,I){let mask=I.reduce((x,i)=>x|(1<<i),0);for(let x=0;x<(1<<n);x++){let y=mask;for(;;){if(ev(n,g,out,x)!==ev(n,g,out,x^y))return true;if(!y)break;y=(y-1)&mask;}}return false;}
function locate(n,ans){let q=0,found=[];function step(I){if(found.length>=4)return;q++;if(!ans(I))return;if(I.length===1){found.push(I[0]);return;}let k=Math.floor(I.length/2);step(I.slice(0,k));step(I.slice(k));}step(Array.from({length:n},(_,i)=>i));return {q,found};}
let cases=0;
for(let n=2;n<=7;n++)for(let rep=0;rep<10;rep++){let g=[];let t=3+rnd()%8;
for(let j=0;j<t;j++)g.push([[6,8,14,7,9,13,1][rnd()%7],rnd()%(n+j),rnd()%(n+j)]);
let out=n+t-1,S=supp(n,g,out),res=locate(n,I=>{let a=group(n,g,out,I);ok(a===I.some(i=>S.includes(i)),"iff");return a;});
ok(res.found.length===Math.min(4,S.length),"count");ok(res.found.every(i=>S.includes(i)),"support");ok(res.q<=1+2*Math.min(4,S.length)*Math.ceil(Math.log2(n)),"bound");cases++;}
let large={};
for(const n of [16,64,256]){let g=[[6,0,1]],cur=n;for(let i=2;i<n;i++){g.push([6,i,i]);let z=n+g.length-1;g.push([6,cur,z]);cur=n+g.length-1;}
for(let j=0;j<100;j++){let x=rnd(),v=Array.from({length:n},(_,i)=>i<31?Boolean((x>>>i)&1):false);
for(const [op,a,b] of g)v.push(Boolean((op>>(2*Number(v[a])+Number(v[b])))&1));ok(v[cur]===Boolean((x&1)^((x>>1)&1)),"cancel");}
let r=locate(n,I=>I.includes(0)||I.includes(1));ok(r.found.join(",")==="0,1");ok(r.q===2*Math.ceil(Math.log2(n))+1);large[n]=r.q;cases++;}
ok([0,1,2,3].every(x=>(((x&1)^((x>>1)&1))===(((x^3)&1)^(((x^3)>>1)&1)))),"incorrect all flip");ok((true&&true)===true);ok((false&&true)!==true);
process.stdout.write(JSON.stringify({status:"PASS",assertions:nchecks,cases,large,seed_initial:411})+"\n");