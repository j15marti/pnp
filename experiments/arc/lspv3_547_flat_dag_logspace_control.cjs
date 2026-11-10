"use strict";
/* LSPV-3/547 finite semantic control; not an actual FLMV logspace run or historical R_mix341 checker. */
const ok=(b,m)=>{if(!b)throw Error(m)};
const copy=x=>JSON.parse(JSON.stringify(x));
const canon=(a,n)=>{ok(Array.isArray(a),'array');let old=0;for(let x of a){ok(Number.isSafeInteger(x)&&x!==0&&Math.abs(x)<=n&&Math.abs(x)>old,'noncanonical literal');old=Math.abs(x)}};
const ext=(a,p)=>[...a,p].sort((x,y)=>Math.abs(x)-Math.abs(y));
const eq=(a,b)=>a.length===b.length&&a.every((x,j)=>x===b[j]);
function audit(F,P){
 ok(F&&Number.isSafeInteger(F.n)&&F.n>0&&Array.isArray(F.clauses)&&F.clauses.length>0,'source');
 for(let c of F.clauses){ok(c.length<=3,'width');canon(c,F.n)}
 ok(Array.isArray(P)&&P.length>0,'proof');let paid=0;
 P.forEach((node,i)=>{ok(node&&Array.isArray(node.ctx),'node');canon(node.ctx,F.n);
 let parent=j=>{ok(Number.isSafeInteger(j)&&0<=j&&j<i,'parent');return P[j].ctx};
 if(node.op==='LEAF'){
 ok(Number.isSafeInteger(node.src)&&0<=node.src&&node.src<F.clauses.length,'source ID');
 ok(F.clauses[node.src].every(x=>node.ctx.includes(-x)),'leaf not false')
 }else if(node.op==='CASE'){
 paid++;ok(Number.isSafeInteger(node.var)&&node.var>0&&node.var<=F.n&&!node.ctx.some(x=>Math.abs(x)===node.var),'pivot');
 ok(node.yes!==node.no,'AND both children');
 ok(eq(parent(node.yes),ext(node.ctx,node.var))&&eq(parent(node.no),ext(node.ctx,-node.var)),'scopes')
 }else if(node.op==='WEAKEN'){
 ok(parent(node.parent).every(x=>node.ctx.includes(x)),'leaked assumption')
 }else throw Error('unsupported rule')});
 ok(P[P.length-1].ctx.length===0,'not globally closed');return {nodes:P.length,paid_cases:paid};
}
function k4(q){
 let edges=[];for(let v=0;v<4;v++)for(let w=v+1;w<4;w++)edges.push([v,w]);
 let clauses=[];for(let v=0;v<4;v++){
 let vars=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
 for(let j=0;j<8;j++)if(((j&1)^((j>>1)&1)^((j>>2)&1))!==q[v])
 clauses.push(vars.map((x,i)=>(j&(1<<i))?-x:x))
 }return {n:6,clauses}
}
function models(F){let m=0;for(let a=0;a<2**F.n;a++)
 if(F.clauses.every(C=>C.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0))))m++;
 return m}
function tree(F){
 let P=[];function rec(ctx,d){
 if(d===F.n){
 let src=F.clauses.findIndex(C=>C.every(l=>ctx.includes(-l)));
 ok(src>=0,'SAT branch cannot close');P.push({op:'LEAF',ctx,src});return P.length-1
 }
 let v=d+1,no=rec(ext(ctx,-v),d+1),yes=rec(ext(ctx,v),d+1);
 P.push({op:'CASE',ctx,var:v,yes,no});return P.length-1
 }rec([],0);return P;
}
const S={n:2,clauses:[[1],[-1]]};
const P=[{op:'LEAF',ctx:[-1],src:0},{op:'LEAF',ctx:[1],src:1},
{op:'CASE',ctx:[],var:1,yes:1,no:0},{op:'WEAKEN',ctx:[2],parent:2},
{op:'WEAKEN',ctx:[-2],parent:2},{op:'CASE',ctx:[],var:2,yes:3,no:4}];
function test(){
 const F=k4([1,0,0,0]),E=k4([0,0,0,0]);
 ok(models(F)===0&&models(E)===8,'Tseitin models');
 let A=audit(F,tree(F)),B=audit(S,P);
 ok(A.nodes===127&&A.paid_cases===63&&B.nodes===6&&B.paid_cases===2,'counts');
 let refused=false;try{tree(E)}catch(e){refused=true};ok(refused,'SAT not refused');
 let rejects=0;
 const reject=(f,p)=>{let failed=false;try{audit(f,p)}catch(e){failed=true};ok(failed,'bad certificate accepted');rejects++};
 const mutate=(idx,change)=>{let pp=copy(P);change(pp[idx]);reject(S,pp)};
 mutate(0,x=>x.src=1);mutate(5,x=>x.yes=x.no);mutate(2,x=>x.var=2);
 mutate(3,x=>x.ctx=[-2]);mutate(3,x=>x.parent=5);mutate(5,x=>x.ctx=[1]);
 mutate(5,x=>x.yes=10**30);mutate(5,x=>x.no=0.5);
 reject({n:2,clauses:[[0]]},P);reject({n:2,clauses:[[1,-1]]},P);
 return {odd_k4_models:0,odd_k4:A,even_k4_models:8,sat_refused:refused,shared:B,hostile_rejections:rejects,
 note:'Full-memory semantic tests; not native R_mix341 or measured native FLMV space.'}
}
const result=test();
if(typeof process!=='undefined')process.stdout.write(JSON.stringify(result,null,2)+'\n');
result;