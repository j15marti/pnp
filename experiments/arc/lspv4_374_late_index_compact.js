"use strict";
// LSPV-4/374. Finite source-check controls, no claim about FLMV space.
const assert=require("node:assert/strict");
function count(a,j){
 let m=0;for(let z=0;z<(1<<a.length);z++){
   if(a.every((v,i)=>((z>>i)&1)===v)&&((z>>(j-1))&1)===0)m++;
 }return m;
}
function mk(a,j){return "p cnf "+a.length+" "+(a.length+1)+"\n"+
 a.map((v,i)=>(v?" ":"-")+(i+1)+" 0\n").join("")+"-"+j+" 0\n";}
function parse(s){let lines=s.split("\n");assert.equal(lines.at(-1),"");lines.pop();
 const h=/^p cnf ([1-9]\d*) ([1-9]\d*)$/.exec(lines[0]);
 if(!h||+h[2]!==+h[1]+1||lines.length!==+h[2]+1)throw Error("grammar");
 let n=+h[1],a=[];for(let i=1;i<=n;i++){let m=/^([ -])([1-9]\d*) 0$/.exec(lines[i]);
 if(!m||+m[2]!==i)throw Error("unit");a.push(m[1]===" "?1:0);}
 let tail=/^-([1-9]\d*) 0$/.exec(lines[n+1]);if(!tail||+tail[1]>n)throw Error("selector");
 return {a,j:+tail[1]};}
let tests=0,sat=0,unsat=0,models=0;
for(let k=1;k<=8;k++)for(let mask=0;mask<(1<<k);mask++){
 let a=Array.from({length:k},(_,i)=>(mask>>i)&1);
 for(let j=1;j<=k;j++){let p=parse(mk(a,j)),b=a[j-1]===0;
 assert.deepEqual(p,{a,j});tests++;
 if(b)sat++;else unsat++;
 if(k<=6){assert.equal(count(a,j),b?1:0);models++;}}
}
let bad=["p cnf 2 3\n 1 0\n-2 0\n-3 0\n","p cnf 2 3\n 1 0\n-2 0\n--1 0\n","p cnf 2 3\n 1 0\n-2 0\n 2 0\n"];
for(let s of bad)assert.throws(()=>parse(s));
let edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function parity(c){let out=0;for(let mask=0;mask<64;mask++){
 let ok=c.every((v,i)=>edges.reduce((z,e,j)=>z^(e.includes(i)?((mask>>j)&1):0),0)===v);
 if(ok)out++;}return out;}
assert.equal(parity([0,0,0,0]),8);assert.equal(parity([1,0,0,0]),0);
const result={test_cases:tests,sat,unsat,brute_models:models,malformed_rejected:bad.length,odd_K4:0,even_K4:8,scope:"one-pass late-index unit-CNF controls only; no unrestricted lower bound"};
assert.equal(tests,3586);assert.equal(sat,1793);assert.equal(unsat,1793);
console.log(JSON.stringify(result,null,2));