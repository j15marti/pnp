"use strict";
// LSPV-3/387: exact finite controls for guarded affine projection.
function parity(x){let p=0;while(x){p^=x&1;x>>>=1;}return p;}
function makeGates(n,mask,b){
 if(!Number.isInteger(n)||n<1||n>20||!Number.isInteger(mask)||mask<1||mask>=(1<<n)||(b!==0&&b!==1))throw Error("malformed source");
 let gates=[],fresh=n+1;
 const lit=(wire,neg=false)=>({wire,neg});
 const inv=l=>({wire:l.wire,neg:!l.neg});
 const add=(u,v)=>{let id=fresh++;gates.push({id,u,v});return lit(id);};
 const inputs=[];for(let i=0;i<n;i++)if((mask>>i)&1)inputs.push(lit(i+1));
 let cur=inputs[0];
 for(let i=1;i<inputs.length;i++){
  const next=inputs[i],p=add(cur,inv(next)),q=add(inv(cur),next);
  cur=inv(add(inv(p),inv(q)));
 }
 const violation=b?inv(cur):cur;
 const out=add(lit(0),violation); // gate zero is the t input
 return {n,mask,b,gates,out:out.wire};
}
function evaluate(network,t,x){
 const values=new Map([[0,Boolean(t)]]);
 for(let i=0;i<network.n;i++)values.set(i+1,Boolean((x>>i)&1));
 const lval=l=>values.get(l.wire)!==l.neg;
 for(const g of network.gates)values.set(g.id,lval(g.u)&&lval(g.v));
 return !values.get(network.out); // asserted unit NOT(out)
}
function target(n,mask,b,t,x){return (!t)||(parity(x&mask)===b);}
function runAudit(){
 const out={run:"LSPV3-387",model:"projected affine equations versus guarded parity",range_n:[1,6],
 tested_relations:0,assignments:0,three_point_witnesses:0,gate_count_sum:0,
 max_gate_count:0,positive_controls:0,negative_controls:0,degenerate_controls:0,corrupted_rejections:0,malformed_rejections:0};
 const assert=(c,msg)=>{if(!c)throw Error(msg);};
 for(let n=1;n<=6;n++)for(let mask=1;mask<(1<<n);mask++)for(let b=0;b<=1;b++){
  const c=makeGates(n,mask,b);
  const expectedGateCount=3*(parityPop(mask)-1)+1;
  assert(c.gates.length===expectedGateCount,"gate count mismatch");
  out.tested_relations++;out.gate_count_sum+=c.gates.length;
  out.max_gate_count=Math.max(out.max_gate_count,c.gates.length);
  let satcount=0;
  for(let t=0;t<2;t++)for(let x=0;x<(1<<n);x++){
   const a=evaluate(c,t,x),v=target(n,mask,b,t,x);
   assert(a===v,"gate/target mismatch n="+n+" mask="+mask+" b="+b);
   out.assignments++;if(a)satcount++;
   if(t===0){assert(a,"t=0 SAT");out.positive_controls++;}
   else if(!v){out.negative_controls++;}
  }
  assert(satcount===3*(1<<(n-1)),"relation cardinality");
  const bit=Math.floor(Math.log2(mask&-mask));
  const x0=b?(1<<bit):0;
  const x1=x0^(1<<bit);
  assert(target(n,mask,b,0,x0)&&target(n,mask,b,0,x1)&&target(n,mask,b,1,x0)&&!target(n,mask,b,1,x1),"3-pt closure fail");
  out.three_point_witnesses++;
  assert(evaluate(c,1,x1)===false,"corruption control");
  out.corrupted_rejections++;
 }
 for(let n=1;n<=6;n++)for(let b=0;b<2;b++){
   let count=0;for(let t=0;t<2;t++)for(let x=0;x<(1<<n);x++)count+=Number(target(n,0,b,t,x));
   assert(count===(b===0?2*(1<<n):(1<<n)),"degenerate count");
   out.degenerate_controls++;
 }
 const bad=[[0,1,0],[1,0,0],[1,2,0],[1,1,2],[2,4,0],[1,1,-1],[1,-1,1]];
 for(const [n,mask,b] of bad){try{makeGates(n,mask,b);throw Error("accepted malformed");}catch(e){assert(e.message!=="accepted malformed","accepted invalid record");out.malformed_rejections++;}}
 return out;
}
function parityPop(x){let n=0;while(x){n+=x&1;x>>>=1;}return n;}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(runAudit(),null,2));
