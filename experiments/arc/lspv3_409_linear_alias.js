#!/usr/bin/env node
'use strict';
// LSPV-3/409. Construct/replay strict RES+paid XOR2 DEF alias certificates.
// CONDITIONAL: each paid DEF defining clause is addressable as a RES premise.
// This DOES NOT settle native R_mix341 LOCAL-CONVERT/export byte syntax.
// Every RES step has two parent clauses and an explicit complementary pivot.
(function() {
function check(x,m){if(!x)throw new Error(m)}
function cn(a){const s=[...new Set(a)];check(s.every(x=>Number.isInteger(x)&&x!==0&&!s.includes(-x)),'tautological clause');return s.sort((x,y)=>Math.abs(x)-Math.abs(y)||(y-x))}
function equal(a,b){return JSON.stringify(cn(a))===JSON.stringify(cn(b))}
function facets(x,y,z){const r=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++){if(c===(a^b))continue;r.push(cn([a?-x:x,b?-y:y,c?-z:z]))}return r}
function resolved(a,b,p){check(a.includes(p)&&b.includes(-p),'missing complementary pivot');const c=cn([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);return c}
function builder(m){
 check(Number.isInteger(m)&&m>0,'m positive');
 const gates=[],nodes=[],dedup=new Map(),steps=[];
 function def(x,y,z){check(x!==y&&y!==z&&x!==z,'distinct terminals');const gid=gates.length;gates.push({left:x,right:y,out:z,op:'XOR2',paid:1});return facets(x,y,z).map((clause,j)=>{const id=nodes.length;nodes.push({id,kind:'DEF_CLAUSE',gate:gid,facet:j,clause});return id})}
 function res(a,b,p){const aa=nodes[a].clause,bb=nodes[b].clause;let clause;
 try{clause=resolved(aa,bb,p)}catch(e){return null}
 const key=JSON.stringify(clause);if(dedup.has(key))return dedup.get(key);
 const id=nodes.length;nodes.push({id,kind:'RES',parents:[a,b],pivot:p,clause});dedup.set(key,id);return id}
 function elim(keep,p){const plus=keep.filter(i=>nodes[i].clause.includes(p)),minus=keep.filter(i=>nodes[i].clause.includes(-p));const out=keep.filter(i=>!nodes[i].clause.includes(p)&&!nodes[i].clause.includes(-p));for(const i of plus)for(const j of minus){const k=res(i,j,p);if(k!==null&&!out.includes(k))out.push(k)}return out}
 let p=1,forward=null,backward=null;
 for(let i=1;i<=m;i++){
   const t=3*i-1,a=3*i,q=3*i+1;
   const local=elim(elim([...def(p,t,a),...def(a,t,q)],a),t);
   const f=local.find(k=>equal(nodes[k].clause,[-p,q]));
   const b=local.find(k=>equal(nodes[k].clause,[p,-q]));
   check(f!==undefined&&b!==undefined,'local equalities absent');
   const nf=forward===null?f:res(forward,f,p);
   const nb=backward===null?b:res(b,backward,p);
   check(nf!==null&&nb!==null,'global pivot fail');
   steps.push({stage:i,from:p,to:q,step_forward:f,step_backward:b,forward:nf,backward:nb});
   forward=nf;backward=nb;p=q;
 }
 const r={schema:'LSPV3-409-cancel-chain-v1',m,original_port:1,final_port:p,gates,nodes,ends:[forward,backward],summary:steps};
 replay(r);return r;
}
function replay(r){
 check(r.schema==='LSPV3-409-cancel-chain-v1'&&r.gates.length===2*r.m,'schema/gates');
 const out=new Set();
 for(const g of r.gates){check(g.op==='XOR2'&&g.paid===1&&!out.has(g.out),'gate freshness');out.add(g.out)}
 for(let i=0;i<r.nodes.length;i++){
   const n=r.nodes[i];check(n.id===i&&equal(n.clause,n.clause),'record syntax');
   if(n.kind==='DEF_CLAUSE'){const g=r.gates[n.gate];check(g!==undefined&&equal(n.clause,facets(g.left,g.right,g.out)[n.facet]),'bad facet')}
   else if(n.kind==='RES'){const [a,b]=n.parents;check(a<i&&b<i&&a!==b&&equal(n.clause,resolved(r.nodes[a].clause,r.nodes[b].clause,n.pivot)),'bad RES')}
   else throw Error('unknown kind');
 }
 check(equal(r.nodes[r.ends[0]].clause,[-1,r.final_port]),'forward goal');
 check(equal(r.nodes[r.ends[1]].clause,[1,-r.final_port]),'backward goal');
 return true;
}
function run(){
 const rows=[];
 for(const m of [1,2,3,5,10,20]){
   const p=builder(m),defs=p.gates.length,resnodes=p.nodes.filter(x=>x.kind==='RES').length;
   check(defs===2*m&&resnodes===8*m-2,'closed counts');
   rows.push({m,paid_def:defs,paid_res:resnodes,total:defs+resnodes,clause_evidence:p.nodes.length});
 }
 const r=builder(5);
 for(const mutant of ['pivot','parents','facet','clause']){
   const b=JSON.parse(JSON.stringify(r));
   if(mutant==='pivot')b.nodes.find(x=>x.kind==='RES').pivot=999;
   if(mutant==='parents')b.nodes.find(x=>x.kind==='RES').parents=[999,0];
   if(mutant==='facet')b.nodes.find(x=>x.kind==='DEF_CLAUSE').facet=999;
   if(mutant==='clause')b.nodes.find(x=>x.kind==='RES').clause=[999];
   let rejected=false;try{replay(b)}catch(e){rejected=true}
   check(rejected,'corrupt certificate accepted');
 }
 return {status:'COMPUTATIONAL',model:'conditional addressable DEF facets; not full R_mix341',rows,corrupt_rejected:4,B3:'OPEN',PvsNP:'OPEN'};
}
globalThis.LSPV3_409_run=run;
if(typeof process!=='undefined' && typeof require!=='undefined' && require.main===module){
 console.log(JSON.stringify(run(),null,2));
}
})();