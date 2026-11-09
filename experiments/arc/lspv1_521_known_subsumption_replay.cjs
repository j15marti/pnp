'use strict';
const assert=require('node:assert/strict');
const source=[[1,2],[-1,2],[-2,3],[-2,-3]];
const rows=[
 {kind:'source',source:0,clause:source[0]},
 {kind:'source',source:1,clause:source[1]},
 {kind:'source',source:2,clause:source[2]},
 {kind:'source',source:3,clause:source[3]},
 {kind:'res',parents:[0,1],pivot:1,clause:[2]},
 {kind:'res',parents:[4,2],pivot:2,clause:[3]},
 {kind:'res',parents:[4,3],pivot:2,clause:[-3]},
 {kind:'res',parents:[5,6],pivot:3,clause:[]}
];
let checks=0;
function ck(x,msg){assert.ok(x,msg);checks++}
function norm(xs){let s=[...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);ck(!s.some(x=>s.includes(-x)),'tautology');return s}
function subset(a,b){return a.every(x=>b.includes(x))}
function eq(a,b){return JSON.stringify(norm(a))===JSON.stringify(norm(b))}
function resolvent(a,b,p){if(!a.includes(p)||!b.includes(-p))throw new Error('oriented pivot absent');return norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)])}
function replay(axioms){const out=[],map=[],modes={RES:0,BYPASS:0}; for(let j=0;j<rows.length;j++){let r=rows[j];if(r.kind==='source'){map[j]=out.length;out.push({kind:'source',source:r.source,clause:norm(axioms[r.source])});continue} let ia=map[r.parents[0]],ib=map[r.parents[1]],a=out[ia].clause,b=out[ib].clause;
 if(a.includes(r.pivot)&&b.includes(-r.pivot)){let c=resolvent(a,b,r.pivot);map[j]=out.length;out.push({kind:'res',parents:[ia,ib],pivot:r.pivot,clause:c});modes.RES++}else{map[j]=!a.includes(r.pivot)?ia:ib;modes.BYPASS++}ck(subset(out[map[j]].clause,r.clause),'old output subsumption')}
 ck(out[map[7]].clause.length===0,'empty retained');let seen=new Set(),todo=[map[7]];while(todo.length){let i=todo.pop();if(seen.has(i))continue;seen.add(i);let r=out[i];if(r.kind==='res'){let a=out[r.parents[0]],b=out[r.parents[1]];ck(eq(resolvent(a.clause,b.clause,r.pivot),r.clause));todo.push(...r.parents)}else{ck(eq(r.clause,axioms[r.source]),'source binding')}}
 let work=[...seen].filter(i=>out[i].kind==='res').length;ck(work<=4,'work monotonicity');return {work,modes,reachable:seen.size}}
function variants(xs){let ans=[];for(let mask=0;mask<(1<<xs.length);mask++)ans.push(xs.filter((_,i)=>mask&(1<<i)));return ans}
const vv=source.map(variants);let cases=0,min=10,max=-1,distribution={},modeCounts={};
for(let a of vv[0])for(let b of vv[1])for(let c of vv[2])for(let d of vv[3]){let v=replay([a,b,c,d]);cases++;min=Math.min(min,v.work);max=Math.max(max,v.work);distribution[v.work]=(distribution[v.work]||0)+1;modeCounts[v.modes.BYPASS]=(modeCounts[v.modes.BYPASS]||0)+1}
ck(cases===256);ck(max===4);ck(min===0);
try{resolvent([1],[-2],1);throw new Error('bad pivot accepted')}catch(e){ck(e.message==='oriented pivot absent')}
ck(source.every(c=>c.length===2));
const out={status:'COMPUTATIONAL independent replay of KNOWN standard lemma',family:'four-clause UNSAT 2SAT sharing one derived unit into two branches',cases,subclause_choices:4,minimum_paid:min,maximum_paid:max,original_paid:4,distribution,modeCounts,assertions:checks,scope:'ordinary oriented Resolution only; no mixed-rule native authentication',id_links:['P2-L1-442','P2-L1-520','P2-D1','P2-C3','P2-B1','P2-B2']};
console.log(JSON.stringify(out,null,2));
