#!/usr/bin/env node
// Independent finite verifier for LSPV-3/380. No import from the producer.
// node experiments/arc/lspv3_380_independent_verify.js results/raw/arc/2026-11-03_1820_LSPV3_CENTROID_XOR_ROW_MASS380_raw.json
'use strict';
const fs=require('fs'), assert=require('assert');
let checks=0;
function ok(b,label){checks++;assert(b,label)}
function test(c){
  const {h,edges,proof,graph}=c,n=edges.length,full=(1<<h)-1;
  ok(2*n===3*h,'cubic edge count');
  const degree=Array(h).fill(0);
  for(const [u,v] of edges){ok(u>=0&&v>=0&&u<h&&v<h&&u!==v,'edge');degree[u]++;degree[v]++}
  for(let i=0;i<h;i++)ok(degree[i]===3,'cubic vertex');
  function cut(s){let a=0;for(const [u,v] of edges)a+=(((s>>u)&1)!==((s>>v)&1));return a}
  const memo=new Map;
  function optimum(s){
    if((s&(s-1))===0)return 0;
    if(memo.has(s))return memo.get(s);
    const first=s&-s;let best=Infinity;
    for(let a=(s-1)&s;a>0;a=(a-1)&s)
      if(a&first)best=Math.min(best,optimum(a)+optimum(s^a)+cut(s));
    memo.set(s,best);return best;
  }
  ok(optimum(full)===c.exact_min_aggregate_derived_width,'global subset-split minimum');
  const known=new Map;
  for(let v=0;v<h;v++){
    let mask=0;for(let j=0;j<n;j++)if(edges[j].includes(v))mask|=(1<<j);
    known.set('s'+v,{mask,rhs:Number(v===0),support:1<<v});
  }
  let sum=0;
  for(let i=0;i<proof.length;i++){
    const z=proof[i];
    ok(z.ref==='d'+i,'sequential distinct inference');
    const a=known.get(z.parents[0]),b=known.get(z.parents[1]);
    ok(!!a&&!!b,'parents exist');
    ok((a.support&b.support)===0,'true tree disjoint support');
    const mask=a.mask^b.mask,rhs=a.rhs^b.rhs,support=a.support|b.support;
    ok(z.mask===mask&&z.rhs===rhs&&z.support_vertices===support,'signed XOR');
    ok(z.width===cut(support),'incidence boundary row');
    sum+=z.width;known.set(z.ref,{mask,rhs,support});
  }
  ok(sum===c.exact_min_aggregate_derived_width&&proof.length===h-1,'aggregate and node count');
  const root=known.get('d'+(proof.length-1));
  ok(root.mask===0&&root.rhs===1&&root.support===full,'authentic contradiction');
  function satisfies(bits,odd){
    for(let v=0;v<h;v++){
      const values=[];
      for(let j=0;j<n;j++)if(edges[j].includes(v))values.push((bits>>j)&1);
      ok(values.length===3,'source local arity');
      const local=(values[0]^(values[1])^(values[2]));
      if(local!==Number(odd&&v===0))return false;
    }
    return true;
  }
  let odd=0,even=0;
  for(let bits=0;bits<(1<<n);bits++){
    if(satisfies(bits,true))odd++;
    if(satisfies(bits,false))even++;
  }
  ok(odd===0&&even===(1<<(n-h+1)),'parity model counts');
  ok(odd===c.odd_models&&even===c.even_models,'recorded opposite labels');
  return {graph,exact_min:sum,odd_models:odd,even_models:even};
}
function main(){
  const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
  ok(data.id==='LSPV3-380'&&data.cases.length===4,'format/case count');
  const good=data.cases.map(test);
  let bad=0;
  const corrupt=[
    ...data.cases.map(c=>({...c,proof:[...c.proof.slice(0,-1),{...c.proof.at(-1),rhs:0}]})),
    {...data.cases[0],edges:[[0,0],...data.cases[0].edges.slice(1)]},
    {...data.cases[0],exact_min_aggregate_derived_width:-1}
  ];
  for(const c of corrupt){try{test(c)}catch(e){bad++}}
  ok(bad===corrupt.length,'corrupted records rejected');
  let malformed=0;
  for(const s of ['{','[]','false','{"id":12}']){
    try{const v=JSON.parse(s);ok(v.cases.length===4,'valid record')}catch(e){malformed++}
  }
  ok(malformed===4,'malformed inputs rejected');
  console.log(JSON.stringify({id:'LSPV3-380-independent',assertions:checks,cases:good,corrupted_rejected:bad,malformed_rejected:malformed,
    scope:'finite h-1-XOR-tree optimum and parity controls; not full Rmix341'}));
}
main();
