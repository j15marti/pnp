#!/usr/bin/env node
// LSPV-3/430 self-contained graph-PHP matching versus exhaustive-CNF audit.
// Usage: node lspv3_430_graphphp_essential.js
const assert = require('assert');
function source(ms){
  const edges=[];for(let p=0;p<4;p++)for(let h=0;h<3;h++)if(ms[p]&(1<<h))edges.push([p,h]);
  const id=new Map(edges.map(([p,h],i)=>[`${p}:${h}`,i+1]));
  const cls=[];const meta=[];
  for(let p=0;p<4;p++){cls.push([...Array(3).keys()].filter(h=>id.has(`${p}:${h}`)).map(h=>id.get(`${p}:${h}`)));meta.push(['row',p]);}
  for(let h=0;h<3;h++)for(let p=0;p<4;p++)for(let q=p+1;q<4;q++)
    if(id.has(`${p}:${h}`)&&id.has(`${q}:${h}`)){cls.push([-id.get(`${p}:${h}`),-id.get(`${q}:${h}`)]);meta.push(['col',p,q,h]);}
  return {edges,cls,meta};
}
function match(ms,exceptP,exceptH){
  const remaining=[0,1,2,3].filter(p=>!exceptP.includes(p));
  function dfs(i,used){if(i===remaining.length)return true;
    const p=remaining[i];for(let h=0;h<3;h++)if((ms[p]&(1<<h))&&!(used&(1<<h))&&h!==exceptH&&dfs(i+1,used|(1<<h)))return true;
    return false;}
  return dfs(0,0);
}
function brute(cls,n){
  const hit=new Uint8Array(cls.length);
  for(let a=0;a<(1<<n);a++){
    let only=-1;
    for(let ci=0;ci<cls.length;ci++)if(!cls[ci].some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0))){if(only>=0){only=-2;break;}only=ci;}
    assert.notStrictEqual(only,-1,'graph PHP must be UNSAT');
    if(only>=0)hit[only]=1;
  }
  return [...hit].map(x=>String(x)).join('');
}
const total={graphs:0,assignment_tests:0,clause_tests:0,essential_clauses:0,redundant_clauses:0,graphs_all_essential:0,graphs_some_redundant:0,graphs_zero_essential:0,max_clauses:0,max_essential:0};
for(let a=1;a<=7;a++)for(let b=1;b<=7;b++)for(let c=1;c<=7;c++)for(let d=1;d<=7;d++){
 const ms=[a,b,c,d],{edges,cls,meta}=source(ms);
 const flags=meta.map(x=>x[0]==='row'?match(ms,[x[1]],-1):match(ms,[x[1],x[2]],x[3])?'1':'0').map(x=>typeof x==='boolean'?(x?'1':'0'):x).join('');
 assert.strictEqual(flags,brute(cls,edges.length),`matching mismatch graph ${ms}`);
 const e=flags.split('').filter(x=>x==='1').length;
 total.graphs++;total.assignment_tests+=(1<<edges.length);total.clause_tests+=cls.length;
 total.essential_clauses+=e;total.redundant_clauses+=cls.length-e;
 total.graphs_all_essential+=(e===cls.length);total.graphs_some_redundant+=(e<cls.length);
 total.graphs_zero_essential+=(e===0);total.max_clauses=Math.max(total.max_clauses,cls.length);total.max_essential=Math.max(total.max_essential,e);
}
assert.deepStrictEqual(total,{graphs:2401,assignment_tests:456976,clause_tests:23716,essential_clauses:14980,redundant_clauses:8736,graphs_all_essential:241,graphs_some_redundant:2160,graphs_zero_essential:264,max_clauses:22,max_essential:22});
console.log(JSON.stringify({status:'PASS matching against all original-CNF assignments',...total},null,2));
