#!/usr/bin/env node
// Self-contained exact theorem regression, no SAT oracle. Node 18+.
"use strict";
const assert=require("assert");let checks=0;
const check=(b,s)=>{assert.ok(b,s);checks++};
function val(g,r,u=0,v=0,w=0){let a=[];for(let i=0;i<g.length;i++){let p=g[i],z;check(p.id===i);switch(p.op){
case "K":check(p.bit===0||p.bit===1);z=p.bit;break;
case "U":z=u;break;case "V":z=v;break;case "W":z=w;break;
case "A":case "O":check(p.a<i&&p.b<i&&p.a>=0&&p.b>=0);z=p.op==="A"?a[p.a]&a[p.b]:a[p.a]|a[p.b];break;
case "N":check(p.a>=0&&p.a<i);z=1-a[p.a];break;
default:throw Error("malformed gate");
}a.push(z)}check(r<a.length&&r>=0);return a[r]}
function wrap(n,t){let g=[{id:0,op:"K",bit:0},{id:1,op:"K",bit:1}],r=t?1:0;let add=(op,o={})=>{let id=g.length;g.push({id,op,...o});return id};
for(let i=0;i<n;i++){let op=i%2?"O":"A",b=op==="A"?1:0;r=add(op,{a:r,b})}
let u=add("U"),v=add("V"),w=add("W");
function xor(a,b){let or=add("O",{a,b}),an=add("A",{a,b}),not=add("N",{a:an});return add("A",{a:or,b:not})}
let p=xor(xor(u,v),add("A",{a:r,b:w}));return [g,p]}
function table(g,p){let mask=0;for(let j=0;j<8;j++)mask|=val(g,p,j&1,(j>>1)&1,(j>>2)&1)<<j;return mask}
function k4(c){let es=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)es.push([a,b]);let out=0;
for(let m=0;m<64;m++){let good=true;for(let v=0;v<4;v++){let x=0;for(let e=0;e<6;e++)if(es[e].includes(v))x^=(m>>e)&1;if(x!==(v===0?c:0))good=false}if(good)out++}return out}
let cases=0,broken=0;for(let size of [1,2,4,8,16,32,64,128])for(let t of [0,1])for(let i=0;i<5;i++){
let [g,p]=wrap(size,t),mask=table(g,p);check(mask===(t?150:102));
check(val(g,p,0,0,1)===t);check((mask>>4&1)===t);cases++;
if(i===0){let bad=g.map(o=>({...o}));bad[p].a=g.length+1;
try{val(bad,p,0,0,1);throw Error("bad reference accepted")}catch(e){check(String(e).includes("AssertionError")||String(e).includes("Assertion"));broken++}}
}
check(k4(1)===0);check(k4(0)===8);
const out={status:"COMPUTATIONAL, fixed-typed CUT3 only; P versus NP OPEN",cases,checks,malformed_rejected:broken,masks:[102,150],K4:[0,8]};
process.stdout.write(JSON.stringify(out,null,2)+"\n");
