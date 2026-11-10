"use strict";
// LSPV-3/549. TEST-ONLY CASE/LEAF/WEAKEN; NOT native R_mix341.
// This implementation materializes certificates; it does NOT measure FLMV space.
const big=(10n**65n);
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const plus=(a,v,z)=>[...a,[v,z]].sort((x,y)=>x[0]-y[0]);
const ident=x=>typeof x==="string"&&/^(0|[1-9][0-9]*)$/.test(x);
const srcok=f=>!!f&&Number.isSafeInteger(f.n)&&f.n>0&&Array.isArray(f.clauses)&&f.clauses.every(
 c=>Array.isArray(c)&&c.length===3&&c.every(x=>Number.isSafeInteger(x)&&x!==0&&Math.abs(x)<=f.n)&&new Set(c.map(Math.abs)).size===3);
const ctxt=(c,n)=>Array.isArray(c)&&c.every((p,i)=>Array.isArray(p)&&p.length===2&&Number.isSafeInteger(p[0])&&p[0]>=1&&p[0]<=n&&[0,1].includes(p[1])&&(!i||c[i-1][0]<p[0]));
function check(f,cert) {
 if(!srcok(f))return [false,"SOURCE"];
 if(!Array.isArray(cert)||!cert.length)return [false,"EMPTY"];
 const prev=new Map();let paid=0;
 for(const r of cert){
  if(!r||!ident(r.id)||prev.has(r.id))return [false,"ID"];
  if(!ctxt(r.ctx,f.n))return [false,"CTX"];
  if(r.tag==="LEAF"){
   if(!Number.isSafeInteger(r.source)||r.source<0||r.source>=f.clauses.length||r.weight!==0)return [false,"LEAF-REF"];
   const a=new Map(r.ctx);
   if(!f.clauses[r.source].every(l=>a.has(Math.abs(l))&&a.get(Math.abs(l))!==(l>0?1:0)))return [false,"LEAF-SEM"];
  } else if(r.tag==="WEAKEN"){
   const p=prev.get(r.parent),a=new Map(r.ctx);
   if(!p||r.weight!==0)return [false,"WEAKEN-REF"];
   if(!p.ctx.every(([v,b])=>a.has(v)&&a.get(v)===b))return [false,"WEAKEN-CTX"];
  } else if(r.tag==="CASE"){
   const x=prev.get(r.left),y=prev.get(r.right),v=r.pivot;
   if(!x||!y||x===y||!Number.isSafeInteger(v)||v<1||v>f.n||r.weight!==1)return [false,"CASE-REF"];
   if(r.ctx.some(a=>a[0]===v)||!eq(x.ctx,plus(r.ctx,v,0))||!eq(y.ctx,plus(r.ctx,v,1)))return [false,"CASE-CTX"];
   paid++;
  } else return [false,"TAG"];
  prev.set(r.id,r);
 }
 return cert.at(-1).ctx.length?[false,"GOAL"]:[true,paid];
}
function k4(charges){
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],clauses=[];
 for(let i=0;i<4;i++){
  const ids=edges.map((e,j)=>e.includes(i)?j+1:0).filter(Boolean);
  for(let mask=0;mask<8;mask++){
   const b=[0,1,2].map(j=>(mask>>j)&1);
   if((b[0]^b[1]^b[2])!==charges[i])clauses.push(ids.map((v,j)=>b[j]?-v:v));
  }
 }
 return {n:6,clauses};
}
function count(f){let n=0;for(let a=0;a<(1<<f.n);a++)if(f.clauses.every(c=>c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))n++;return n;}
function construct(f,limit,extra=false){
 let id=extra?10n**80n:big;const P=[];
 function add(tag,ctx,opt){
  const rec=Object.assign({id:String(id++),tag,ctx,weight:tag==="CASE"?1:0},opt);
  P.push(rec);return rec.id;
 }
 function rec(ctx){
  if(ctx.length===limit){
   const assign=new Map(ctx),idx=f.clauses.findIndex(c=>c.every(l=>assign.get(Math.abs(l))!==(l>0?1:0)));
   if(idx===-1)throw Error("SAT witness");
   return add("LEAF",ctx,{source:idx});
  }
  const v=Array.from({length:limit},(_,i)=>i+1).find(z=>!ctx.some(p=>p[0]===z));
  return add("CASE",ctx,{pivot:v,left:rec(plus(ctx,v,0)),right:rec(plus(ctx,v,1))});
 }
 const root=rec([]);
 if(extra){
  const l=add("WEAKEN",[[4,0]],{parent:root}),r=add("WEAKEN",[[4,1]],{parent:root});
  add("CASE",[],{pivot:4,left:l,right:r});
 }
 return {P,root};
}
function runTests(){
 const odd=k4([1,0,0,0]),even=k4([0,0,0,0]),p=construct(odd,6).P;
 if(count(odd)!==0||count(even)!==8||p.length!==127||!eq(check(odd,p),[true,63]))throw Error("K4");
 let satRejected=false;try{construct(even,6)}catch(e){satRejected=e.message==="SAT witness";}
 if(!satRejected)throw Error("SAT control");
 const sf={n:4,clauses:[]};
 for(let mask=0;mask<8;mask++)sf.clauses.push([1,2,3].map(v=>((mask>>(v-1))&1)?-v:v));
 const sh=construct(sf,3,true);
 if(!eq(check(sf,sh.P),[true,8])||sh.P.length!==18)throw Error("shared");
 const tests={
  forged_source:q=>q[0].source=99999,
  nonfalsifying_leaf:q=>q[0].ctx=Array.from({length:6},(_,i)=>[i+1,1]),
  missing_branch:q=>q.at(-1).right="9".repeat(95),
  incompatible_context:q=>q.at(-1).ctx=[[1,0]],
  duplicate_id:q=>q[1].id=q[0].id,
  leading_zero_id:q=>q[1].id="0"+q[1].id,
  forward_parent:q=>q.at(-1).left="9".repeat(95),
  invalid_rule:q=>q[0].tag="FAKE",
  unpaid_case:q=>q.at(-1).weight=0,
  illegal_weakening:q=>{q[1].tag="WEAKEN";q[1].parent=q[0].id;}
 };
 const rejected={};
 for(const [label,fn] of Object.entries(tests)){
  const q=JSON.parse(JSON.stringify(p));fn(q);
  const z=check(odd,q);if(z[0])throw Error("accepted "+label);
  rejected[label]=z[1];
 }
 const bads={
  repeated_variable:f=>f.clauses[0]=[1,1,2],
  zero_literal:f=>f.clauses[0]=[0,2,3],
  out_of_range:f=>f.clauses[0]=[7,2,3],
  short_clause:f=>f.clauses[0]=[1,2]
 },malformed={};
 for(const [label,fn] of Object.entries(bads)){
  const f=JSON.parse(JSON.stringify(odd));fn(f);
  const z=check(f,p);if(z[0])throw Error("accepted malformed "+label);
  malformed[label]=z[1];
 }
 return {run:"LSPV-3/549",sourceK4:{odd_models:count(odd),even_models:count(even),original_clauses:16,variables:6},
   full_tree:{records:p.length,paid_cases:check(odd,p)[1],id_digits:p[0].id.length},
   shared:{records:sh.P.length,paid_cases:check(sf,sh.P)[1],root_id:sh.root,root_ref_count:2},
   corrupt_controls:rejected,malformed_sources:malformed,beta_6_5:"23/45",gap:"1/90",
   exponent_ratios:Object.fromEntries([6,12,24,60].map(k=>[String(k),Number((10**(k/90)).toFixed(8))])),
   limitations:"TEST-ONLY proof grammar; full-memory JS/Python; no historical R_mix341 or native FLMV execution"};
}
if(typeof process!=="undefined"&&process.versions&&process.versions.node)
 console.log(JSON.stringify(runTests(),null,2));
