'use strict';
// Independent finite control for the strictly proper ternary projection theorem.
// Deliberately does not import Python's algorithm or generated results.
const assert = require('node:assert/strict');
function mkOR(pins, counter){
  let n=pins.length;
  if(n===1){let u=++counter[0],v=++counter[0];return [[pins[0],u,v],[pins[0],u,-v],[pins[0],-u,v],[pins[0],-u,-v]];}
  if(n===2){let u=++counter[0];return [[pins[0],pins[1],u],[pins[0],pins[1],-u]];}
  if(n===3)return [pins.slice()];
  let y=[];for(let i=0;i<n-3;i++)y.push(++counter[0]);
  let out=[[pins[0],pins[1],y[0]]];
  for(let j=1;j<y.length;j++)out.push([-y[j-1],pins[j+1],y[j]]);
  out.push([-y.at(-1),pins[n-2],pins[n-1]]);
  return out;
}
function source(w,allowed){
  let counter=[w], clauses=[];
  for(let id=0;id<(1<<w);id++)if(!allowed.has(id)){
    let lits=Array.from({length:w},(_,j)=> ((id>>j)&1)?-(j+1):(j+1));
    clauses.push(...mkOR(lits,counter));
  }
  if(clauses.length===0){clauses=[[++counter[0],++counter[0],++counter[0]]];}
  return clauses;
}
function projection(clauses,w,frontier){
  const vars=[...new Set(clauses.flat().map(x=>Math.abs(x)).filter(v=>v>w))].sort((a,b)=>a-b);
  assert.ok(vars.length<=14);
  for(let bits=0;bits<2**vars.length;bits++){
    let a={};for(let i=1;i<=w;i++)a[i]=(frontier>>(i-1))&1;
    vars.forEach((v,i)=>{a[v]=(bits>>i)&1;});
    if(clauses.every(c=>c.some(x=>(x>0?Boolean(a[x]):!Boolean(a[-x])))))return true;
  }
  return false;
}
let assertions=0,cases=0;
for(let w=1;w<=3;w++){
  let values=1<<w;
  for(let mask=0;mask<(1<<values);mask++){
    let S=new Set(Array.from({length:values},(_,i)=>i).filter(i=>(mask>>i)&1));
    let formula=source(w,S);
    assert.ok(formula.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3)); assertions++;
    for(let a=0;a<values;a++){
      assert.equal(projection(formula,w,a),S.has(a));assertions++;
    }
    cases++;
  }
}
for(let w=1;w<=4;w++)for(let target=0;target<(1<<w);target++){
  const counter=[w];let formula=[];
  for(let i=0;i<w;i++)formula.push(...mkOR([(target>>i)&1?i+1:-(i+1)],counter));
  for(let a=0;a<(1<<w);a++){
    assert.equal(projection(formula,w,a),a===target);assertions++;
  }
}
for(let w=1;w<=6;w++)for(let banned=0;banned<(1<<w);banned++){
  let literals=Array.from({length:w},(_,i)=>(banned>>i)&1?-(i+1):i+1);
  let g=mkOR(literals,[w]);
  assert.ok(g.every(c=>new Set(c.map(Math.abs)).size===3));assertions++;
  for(let a=0;a<(1<<w);a++){
    assert.equal(projection(g,w,a),a!==banned);assertions++;
  }
}
const out={checker:'independent JS',strict_3cnf_projected_subsets:cases,assertions,pass:true};
console.log(JSON.stringify(out,null,2));
