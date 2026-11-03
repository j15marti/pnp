#!/usr/bin/env node
// Independently implemented LSPV-2 352 source/gate/resolution checker.
'use strict';
const fs=require('fs');
const fname=process.argv[2]||'results/raw/arc/2026-11-02_2312_LSPV2_PAID_WEAKENING352_compact_raw.json';
const data=JSON.parse(fs.readFileSync(fname,'utf8'));
let assertions=0;
const yes=(v,m)=>{assertions++;if(!v)throw Error(m||'failed')};
const norm=a=>{yes(Array.isArray(a),'clause list');let s=new Set(a);yes(s.size===a.length,'duplicate');for(let x of s){yes(Number.isInteger(x)&&x!==0,'signed int');yes(!s.has(-x),'tautology');}return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)};
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const literal=(x,v)=>x>0?v[x]:!v[-x];
function verify(d){
  let C=norm(d.C),B=norm(d.B);
  yes(C.length>0&&B.length>0&&!C.some(x=>B.includes(x)||B.includes(-x)),'bad source');
  yes(d.nodes[0].type==='source'&&equal(C,d.nodes[0].clause),'authentication');
  let active=new Set([JSON.stringify(C)]),slots=new Set();
  let high=Math.max(...C.concat(B).map(Math.abs)),def=0,res=0;
  for(let n of d.nodes.slice(1)){
    if(n.type==='DEF'){
      const [a,b]=n.inputs;
      yes(n.var>high,'DEF freshness');yes([a,b].every(x=>x!==0&&Math.abs(x)<=high),'DEF input');
      let expected=[[-n.var,a],[-n.var,b],[n.var,-a,-b]].map(norm);
      yes(equal(n.slots,expected),'gate clause slots');
      // Four input valuations check conservative truth functionality and all slots.
      for(let mask=0;mask<4;mask++){
        if(Math.abs(a)===Math.abs(b))continue;
        let v={};v[Math.abs(a)]=!!(mask&1);v[Math.abs(b)]=!!(mask&2);
        v[n.var]=literal(a,v)&&literal(b,v);
        for(let s of expected)yes(s.some(x=>literal(x,v)),'gate truth check');
      }
      expected.forEach(x=>slots.add(JSON.stringify(x)));
      high=n.var;def++;
    }else if(n.type==='RES'){
      const L=norm(n.left),R=norm(n.right),p=n.pivot;
      yes(active.has(JSON.stringify(L)),'missing left predecessor');
      yes(active.has(JSON.stringify(R))||slots.has(JSON.stringify(R)),'unpaid right predecessor');
      yes(L.includes(p)&&R.includes(-p),'invalid pivot');
      const result=norm([...new Set([...L.filter(x=>x!==p),...R.filter(x=>x!==-p)])]);
      yes(equal(result,n.clause),'bad resolvent');
      active.add(JSON.stringify(result));res++;
    }else throw Error('unknown node kind');
  }
  yes(equal(d.target,norm(C.concat(B))),'wrong target');
  yes(equal(d.nodes.at(-1).clause,d.target),'incomplete proof');
  yes(def===C.length+B.length-1,'DEF count');
  yes(res===2*C.length+B.length-1,'RES count');
  yes(def+res===d.logical_cost&&d.logical_cost===3*C.length+2*B.length-2,'cost');
}
let rejected=0;
for(let d of data.cases){
  verify(d);
  let broken=JSON.parse(JSON.stringify(d));
  broken.nodes.find(n=>n.type==='DEF').slots[0][0]*=-1;
  try{verify(broken);throw Error('accepted bad DEF')}catch(e){yes(!String(e).includes('accepted bad DEF'),'reject bad DEF');rejected++;}
  broken=JSON.parse(JSON.stringify(d));
  broken.nodes.find(n=>n.type==='RES').pivot*=-1;
  try{verify(broken);throw Error('accepted bad RES')}catch(e){yes(!String(e).includes('accepted bad RES'),'reject bad RES');rejected++;}
}
const countModels=(clauses,k)=>{let n=0;for(let bits=0;bits<(1<<k);bits++){let v={};for(let j=1;j<=k;j++)v[j]=!!(bits&(1<<(j-1)));if(clauses.every(c=>c.some(l=>literal(l,v))))n++;}return n};
for(let k=1;k<=5;k++){let C=Array.from({length:k},(_,i)=>i+1),u=C.map(x=>[-x]);
  yes(countModels([C,...u],k)===0,'UNSAT label');
  yes(countModels([C],k)>0,'SAT label');
  for(let i=0;i<k;i++)yes(countModels([C,...u.filter((_,j)=>i!==j)],k)===1,'SAT deletion');
}
for(let bad of [[1,-1],[1,1],[0],['x']]){try{norm(bad);throw Error('accepted bad source')}catch(e){yes(!String(e).includes('accepted bad source'),'reject malformed');}}
console.log(JSON.stringify({status:'PASS',cases:data.cases.length,assertions,corrupt_rejections:rejected,costs:data.cases.map(x=>x.logical_cost)}));
