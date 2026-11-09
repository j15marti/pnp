#!/usr/bin/env node
// LSPV-1/523: independent from Python modulo-three global-charge audit.
// Exhaustive all 2^18 Boolean masks for strict proper K4 one-hot source.
'use strict';
const assert = require('node:assert/strict');
function build(sigma) {
  assert(sigma===0 || sigma===1 || sigma===2);
  const edges=[]; for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);
  const incidence=Array.from({length:4},()=>[]);
  edges.forEach(([a,b],i)=>{incidence[a].push([i,1]); incidence[b].push([i,-1]);});
  const charges=[sigma,0,0,0],clauses=[],ids=[];
  for(let e=0;e<edges.length;e++){
    clauses.push([3*e,3*e+1,3*e+2].map(i=>({i,pos:true})));ids.push({kind:'ALO',edge:e});
  }
  for(let v=0;v<4;v++)for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++){
    if((a+b+c)%3===charges[v])continue;
    const triple=[a,b,c];
    clauses.push(triple.map((val,j)=>{
      const [e,sign]=incidence[v][j];
      return {i:3*e+((sign*val)%3+3)%3,pos:false};
    }));ids.push({kind:'D',v,triple});
  }
  assert.equal(clauses.length,78);
  for(const clause of clauses)assert.equal(new Set(clause.map(x=>x.i)).size,3);
  return {clauses,ids,charges};
}
function falseClause(clause,assignment){
  return clause.every(({i,pos})=>pos ? ((assignment >>> i)&1)===0 : ((assignment >>> i)&1)===1);
}
function audit(sigma){
  const {clauses,ids,charges}=build(sigma),counter=new Array(78).fill(0);
  let exactOne=0,allGood=0;
  for(let bits=0;bits<(1<<18);bits++){
    let failed=-1;
    for(let i=0;i<78;i++)if(falseClause(clauses[i],bits)){
      if(failed!==-1){failed=-2;break;} failed=i;
    }
    if(failed===-1)allGood++;
    else if(failed>=0){counter[failed]++;exactOne++;}
  }
  const expected=ids.map(x=>x.kind==='ALO' || ((x.triple[0]+x.triple[1]+x.triple[2]-charges[x.v]+6)%3)===(3-sigma)%3);
  for(let i=0;i<78;i++)assert.equal(counter[i]>0,expected[i],`sigma=${sigma} clause=${i}`);
  if(sigma) {
    assert.equal(allGood,0);assert.equal(expected.filter(Boolean).length,42);
    assert.equal(expected.slice(6).filter(Boolean).length,36);
  } else assert(allGood>0);
  return {sigma,assignments:1<<18,exactOne,allGood,essential:sigma?expected.filter(Boolean).length:null,predicted_singletons:expected.filter(Boolean).length,essential_ids:sigma?expected.map((b,i)=>b?i:null).filter(x=>x!==null):null,nonessential_ids:sigma?expected.map((b,i)=>!b?i:null).filter(x=>x!==null):null};
}
const r=[audit(1),audit(2),audit(0)];
// A deliberately corrupted original source must not pass an authenticated clause comparison.
const F=build(1);const k=F.ids.findIndex(x=>x.kind==='D');
const corrupt=F.clauses.map(c=>c.map(l=>({...l})));
corrupt[k][0].pos=true;
assert.notDeepEqual(corrupt[k],F.clauses[k]);
let changeDetected=false;
for(let bits=0;bits<(1<<18);bits++)if(falseClause(corrupt[k],bits)!==falseClause(F.clauses[k],bits)){changeDetected=true;break;}
assert(changeDetected);
const result={status:'COMPUTATIONAL finite exhaustive, not unrestricted proof-system lower bound',r,corruption_detected:changeDetected};
console.log(JSON.stringify(result));
