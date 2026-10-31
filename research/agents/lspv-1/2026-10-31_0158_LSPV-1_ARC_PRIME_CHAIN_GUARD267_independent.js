"use strict";
/* Independent full raw checker, Node 18+, no dependencies. */
function verify(A,B){
const rows=[...A.rows,...B.rows],eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),ok=(v,s)=>{if(!v)throw Error(s)};
const val=(c,m)=>c.reduce((z,l)=>z+((!!(m&(1<<(Math.abs(l)-1))))===(l>0)?1:0),0);
const resolve=(c,d,p)=>{ok(c.includes(p)&&d.includes(-p),"pivot");
const z=[...new Set(c.filter(l=>l!==p).concat(d.filter(l=>l!==-p)))].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
ok(z.every(l=>!z.includes(-l)),"tautology");return z;};
let modeChecks=0,models=0,proofSteps=0,projectionChecks=0;
for(const o of rows){
let {original_clauses:c,n,adversarial:a}=o;
ok(c.length===o.m&&a.indexed.length===c.length,"clause count");
for(let i=0;i<c.length;i++){
ok(c[i].length===3&&new Set(c[i].map(Math.abs)).size===3,"nonproper");
ok(eq(c[i],a.indexed[i].source),"source index");
for(let j=0;j<3;j++){let l=c[i][j],u=a.indexed[i].occ[j];
ok(u.literal===l&&u.S===(l>0?1:0)&&u.U===(l>0?0:1),"S/U");
ok(u.inverted_S===u.U&&u.inverted_U===u.S,"inversion");}}
for(const q of a.compat)for(const s of ["S","U"])for(const t of ["S","U"]){
let req=new Map(),valid=true;
for(const [idx,type] of [[q.i-1,s],[q.j-1,t]])for(const l of c[idx]){
let k=Math.abs(l),v=type==="S"?(l>0?1:0):(l>0?0:1);
if(req.has(k)&&req.get(k)!==v)valid=false;req.set(k,v);}
ok(q[s+t]===valid,"pair mode");modeChecks++;
}
let at0=c.map(z=>val(z,0)),at1=c.map(z=>val(z,(1<<n)-1));
ok(eq(at0,a.coherent_zero.truth_counts)&&eq(at1,a.coherent_one.truth_counts),"endpoints");
ok(at0.every((x,i)=>x+at1[i]===3),"complement");
for(let step of a.flips){let m=(1<<step.step)-1,ts=c.map(z=>val(z,m)),hist=[0,0,0,0];
for(let k of ts)hist[k]++;ok(eq(ts,step.truth_counts)&&eq(hist,step.histogram),"flip");}
if(n<=17){let total=0;for(let m=0;m<(1<<n);m++){if(c.every(z=>val(z,m)>0))total++;models++;}
ok(total===o.oracle_models&&((total>0)===(o.label==="SAT")),"SAT oracle");}
if(o.adaptive.proof){
let p=o.adaptive.proof,cur=c[0],steps=p.steps.filter(z=>z.kind==="chain");
ok(steps.length===p.R.length-3,"chain length");
for(let x of steps){ok(eq(x.left,cur)&&eq(x.right,c[x.original_parent_index-1]),"chain source");
cur=resolve(cur,x.right,x.pivot);ok(eq(cur,x.out),"chain resolution");proofSteps++;}
ok(eq(cur,p.R),"projection clause");
if(p.empty){
for(let x of p.steps.filter(z=>z.kind==="gadget")){
let q=x.source_indices.map(i=>c[i-1]),s=resolve(q[0],q[1],x.pivot1),t=resolve(q[2],q[3],x.pivot1),u=resolve(s,t,x.pivot2);
ok(eq(x.derived,[s,t,u]),"gadget");cur=resolve(cur,u,-u[0]);proofSteps+=4;
let r=p.steps.find(z=>z.kind==="refutation"&&z.pivot===-u[0]);
ok(!!r&&eq(r.out,cur),"empty derivation");}
ok(cur.length===0,"no global UNSAT proof");}}}
for(let g of A.projection){let h=g.h,c=[[h+3,1,2]];
for(let j=1;j<h-1;j++)c.push([-(h+2+j),h+3+j,j+2]);
c.push([-(2*h+1),h+1,h+2]);
for(let m=0;m<(1<<(h+2));m++){
let exists=false;for(let x=0;x<(1<<(h-1));x++){
projectionChecks++;if(c.every(z=>val(z,m|(x<<(h+2)))>0))exists=true;}
ok(exists===(m!==0),"projection");}
for(let j=0;j<h;j++){let found=false;
for(let x=0;x<(1<<(h-1));x++){if(c.filter((_,i)=>i!==j).every(z=>val(z,x<<(h+2))>0))found=true;}
ok(found,"indispensable leaf");}}
return {status:"PASS",formulas:rows.length,SAT:rows.filter(x=>x.label==="SAT").length,UNSAT:rows.filter(x=>x.label==="UNSAT").length,modeChecks,models,projectionChecks,proofSteps};
}
if(require.main===module){let fs=require("fs"),p=process.argv.slice(2);if(p.length!==2)throw Error("node independent.js rawA.json rawB.json");console.log(JSON.stringify(verify(...p.map(x=>JSON.parse(fs.readFileSync(x)))),null,2))}
module.exports={verify};