#!/usr/bin/env node
// LSPV-3/379 finite signed gate and RES countercontrol. NOT a full Rmix341 checker.
'use strict';
const assert=require('assert'), fs=require('fs');
let checks=0,rejections=0;
function yes(x,msg){assert(x,msg);checks++}
const gates=[
 {out:7,input:[1,2],slots:[[-7,1],[-7,2],[7,-1,-2]]},
 {out:8,input:[7,3],slots:[[-8,7],[-8,3],[8,-7,-3]]},
 {out:9,input:[8,4],slots:[[-9,8],[-9,4],[9,-8,-4]]}
];
const P=[9,5,6],Q=[-9,5,6],R=[5,6];
function lit(l,a){return l>0?!!a[Math.abs(l)]:!a[Math.abs(l)]}
function clause(c,a){return c.some(l=>lit(l,a))}
function resolve(c,d,p){
 if(!c.includes(p)||!d.includes(-p))throw Error('pivot missing');
 let o=new Set([...c.filter(x=>x!==p),...d.filter(x=>x!==-p)]);
 if([...o].some(x=>o.has(-x)))throw Error('tautological');
 return [...o].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
}
for(let bits=0;bits<512;bits++){
 let a={};for(let i=1;i<=9;i++)a[i]=(bits>>(i-1))&1;
 for(const g of gates)yes(g.slots.every(s=>clause(s,a))===(a[g.out]===(a[g.input[0]]&a[g.input[1]])),'signed AND gate equivalence');
}
for(let bits=0;bits<64;bits++){
 let a={};for(let i=1;i<=6;i++)a[i]=(bits>>(i-1))&1;
 for(const g of gates)a[g.out]=a[g.input[0]]&a[g.input[1]];
 yes(gates.every(g=>g.slots.every(s=>clause(s,a))),'conservative gate values');
 yes(!(clause(P,a)&&clause(Q,a))||clause(R,a),'sound RES');
 yes((clause(P,a)&&clause(Q,a))===Boolean(a[5]||a[6]),'non-tautological factor equality');
}
yes(JSON.stringify(resolve(P,Q,9))===JSON.stringify(R),'strict signed RES');
const source={};for(let i=1;i<=6;i++)source[i]=[i];
for(const g of gates)source[g.out]=[...new Set(g.input.flatMap(i=>source[i]))].sort((a,b)=>a-b);
const lexical=[5,6,9],base=[...new Set(lexical.flatMap(i=>source[i]))].sort((a,b)=>a-b);
yes(base.length===6&&lexical.length===3,'typed guard mismatch');
yes(clause(P,{9:1,5:0,6:0})&&!clause(R,{9:1,5:0,6:0}),'missing premise counterexample');
for(const wrongPivot of [4,5,-9]){
 try{resolve(P,Q,wrongPivot);throw Error('accepted')}catch(e){yes(e.message==='pivot missing','corrupted pivot rejection');rejections++}
}
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function k4(charges){let count=0;for(let bits=0;bits<64;bits++){
 let ok=true;for(let v=0;v<4;v++){let p=0;for(let e=0;e<6;e++)if(edges[e].includes(v))p^=(bits>>e)&1;if(p!==charges[v])ok=false;}if(ok)count++;
}return count;}
yes(k4([1,0,0,0])===0,'odd charge UNSAT');
yes(k4([0,0,0,0])===8,'even charge SAT');
function parse(s){
 const lines=s.trim().split(/\n/),m=/^p cnf (\d+) (\d+)$/.exec(lines[0]);
 if(!m)throw Error('header');
 const cs=lines.slice(1).map(s=>{if(!/^(-?\d+\s+)*0$/.test(s.trim()))throw Error('syntax');return s.trim().split(/\s+/).map(Number).slice(0,-1)});
 if(cs.length!==+m[2]||cs.some(c=>c.some(x=>x===0||Math.abs(x)>+m[1])))throw Error('range');
 return cs;
}
for(const bad of ['p cnf 1 1\n2 0','p cnf 1 2\n1 0','p cnf a 1\n1 0','p cnf 1 1\n1 0 0','p cnf 1 1\n1','p cnf 1 1\n-2 0']){
 try{parse(bad);throw Error('accepted')}catch(e){yes(e.message!=='accepted','malformed rejected');rejections++}
}
yes(parse('p cnf 2 2\n1 -2 0\n-1 2 0').length===2,'valid parse');
const out={id:'LSPV3-379',scope:'finite local signed-AND2 gate and strict RES; NOT full Rmix341 verifier',gates,premises:[P,Q],pivot:9,resolvent:R,lexicalSupport:lexical,baseSupport:base,checks,corruptedOrMalformedRejected:rejections,oddK4Models:0,evenK4Models:8};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out,null,2)+'\n');else console.log(JSON.stringify(out,null,2));
