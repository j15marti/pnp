/* LSPV-2/389 independent checker: no producer import, full Boolean truth replay. */
"use strict";
const fs=require("fs");
let tests=0;
function ok(cond,msg){tests++;if(!cond)throw Error(msg);}
function pc(x){let n=0;for(;x;x&=x-1)n++;return n;}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function rank(xs,n){
 const a=[...xs];let r=0;
 for(let col=0;col<n;col++){
  let pivot=-1;
  for(let j=r;j<a.length;j++)if((a[j]>>col)&1){pivot=j;break;}
  if(pivot<0)continue;
  [a[pivot],a[r]]=[a[r],a[pivot]];
  for(let j=0;j<a.length;j++)if(j!==r&&((a[j]>>col)&1))a[j]^=a[r];
  r++;
 }
 return r;
}
function clauseSat(c,v){return c.some(l=>(((v>>(Math.abs(l)-1))&1)===(l>0?1:0)));}
function models(cnf,n){
 const out=[];for(let a=0;a<2**n;a++)if(cnf.every(c=>clauseSat(c,a)))out.push(a);
 return out;
}
function authenticate(c){
 const {n,rows}=c;ok(n>=2&&n<=6&&rows.length>=3,"shape");
 const src=[],parts=[],mask=[];
 for(const row of rows){
  const vs=row.vars,b=row.b;
  ok(vs.length>=2&&vs.length<=3&&vs.every((v,i)=>v>=1&&v<=n&&(i===0||v>vs[i-1]))&&[0,1].includes(b),"row");
  let cl=[],vec=0;for(const v of vs)vec|=1<<(v-1);
  mask.push(vec);
  for(let a=0;a<2**vs.length;a++)if((pc(a)&1)!==b)cl.push(vs.map((v,i)=>a&(1<<i)?-v:v));
  const start=src.length;parts.push(cl.map((_,i)=>start+i));src.push(...cl);
 }
 ok(eq(src,c.sources)&&eq(parts,c.parts),"source and partitions");
 ok(eq(models(src,n),c.models),"models");
 const other=[],dims=[];
 for(let i=0;i<rows.length;i++){
  const rest=mask.filter((_,j)=>j!==i);other.push(rank(rest,n));
  let imgs=[];
  for(let v=0;v<2**n;v++)if(rest.every(m=>(pc(m&v)&1)===0)){
   let p=0;rows[i].vars.forEach((x,j)=>p|=((v>>(x-1))&1)<<j);
   imgs.push(p);
  }
  dims.push(rank(imgs,rows[i].vars.length));
 }
 ok(eq(other,c.rank_other)&&eq(dims,c.projection_dim),"projection ranks");
 const circuit=mask.reduce((a,b)=>a^b,0)===0&&rows.reduce((a,b)=>a^b.b,0)===1&&other.every(x=>x===rows.length-1);
 const full=dims.every((x,i)=>x===rows[i].vars.length-1);
 ok(circuit===c.circuit&&full===c.fullproj,"structural claim");
 for(let i=0;i<src.length;i++){
  let d=models(src.filter((_,j)=>i!==j),n);
  ok(c.delete[i]===(d.length?d[0]:null),"deletion");
  let flipped=src.map(r=>r.slice());flipped[i][0]*=-1;
  d=models(flipped,n);
  ok(c.flip[i]===(d.length?d[0]:null),"flip");
 }
 if(!c.compiled){ok(!(circuit&&full&&c.models.length===0),"missed compiler");return;}
 ok(circuit&&full&&c.models.length===0,"UNSAT preconditions");
 ok(c.proof.length===src.length-1&&c.paid===c.proof.length,"node count");
 const state={};
 for(let i=0;i<src.length;i++){
  const j=parts.findIndex(x=>x.includes(i)),scope=rows[j].vars;
  let truth=0;
  for(let t=0;t<2**scope.length;t++){
   const v=scope.reduce((a,x,k)=>a|(((t>>k)&1)<<(x-1)),0);
   if(clauseSat(src[i],v))truth|=1<<t;
  }
  state["s"+i]={scope,truth,eq:null};
 }
 c.proof.forEach((node,k)=>{
  ok(node.id==="d"+k&&node.parents.length===2,"record syntax");
  const l=state[node.parents[0]],r=state[node.parents[1]];
  ok(l&&r,"prior parents");
  if(node.rule==="AND3"){
   ok(eq(l.scope,node.scope)&&eq(r.scope,node.scope),"AND scope");
   const truth=l.truth&r.truth;ok(node.truth===truth,"AND truth");
   let equation=null;
   if(node.equation){
    const b=node.equation.b,vs=node.equation.vars;
    ok(eq(vs,node.scope)&&[0,1].includes(b),"annotation format");
    for(let v=0;v<2**vs.length;v++)ok(((truth>>v)&1)===(pc(v)%2===b?1:0),"false GF2 annotation");
    equation=[vs.reduce((a,x)=>a|(1<<(x-1)),0),b];
   }
   state[node.id]={scope:node.scope,truth,eq:equation};
  }else if(node.rule==="XOR"){
   ok(l.eq&&r.eq,"GF2 parents");
   const x=l.eq[0]^r.eq[0],b=l.eq[1]^r.eq[1];
   const vars=Array.from({length:n},(_,j)=>j+1).filter(v=>x&(1<<(v-1)));
   ok(eq(node.equation,{vars,b}),"GF2 row");
   state[node.id]={scope:null,truth:null,eq:[x,b]};
  }else throw Error("unknown rule");
 });
 ok(eq(state["d"+(c.proof.length-1)].eq,[0,1]),"not refuted");
 ok(c.delete.every(x=>x!==null)&&c.flip.every(x=>x!==null),"all-source indispensability");
}
function main(){
 const input=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
 ok(input.schema==="LSPV2-389-matroid-circuit-projection-v1"&&input.cases.length===5,"schema");
 input.cases.forEach(authenticate);
 const src=input.cases.find(x=>x.name==="five_var_hypergraph_circuit");
 const variants=[
 c=>c.proof[0].truth^=1,
 c=>c.proof[c.proof.length-1].equation.b^=1,
 c=>c.proof[0].parents[0]="bad",
 c=>c.sources[0][0]*=-1,
 c=>c.delete[0]=null,
 c=>c.projection_dim[0]-=1
 ];
 let rejects=0;
 for(const change of variants){
  const c=JSON.parse(JSON.stringify(src));change(c);
  try{authenticate(c);}catch(e){rejects++;continue;}
  throw Error("forgery accepted");
 }
 ok(rejects===variants.length,"forgery");
 console.log(JSON.stringify({status:"PASS",assertions:tests,fixtures:input.cases.length,paid:input.cases.filter(c=>c.compiled).map(c=>c.paid),corruptions_rejected:rejects}));
}
if(require.main===module)main();
