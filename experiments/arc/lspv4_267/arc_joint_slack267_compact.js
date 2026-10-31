#!/usr/bin/env node
"use strict";
/* LSPV-4 ARC-JOINT-SLACK267. Independent compact exact-arithmetic and
   original-source SAT/UNSAT verifier. No native FLMV TM timing is claimed. */
const assert = require("assert");
function gcd(a,b){while(b){const t=a%b;a=b;b=t;}return a<0n?-a:a;}
class Q {
 constructor(a,b=1n){a=BigInt(a);b=BigInt(b);assert(b!==0n);if(b<0n){a=-a;b=-b;}const g=gcd(a,b);this.a=a/g;this.b=b/g;}
 add(v){v=q(v);return new Q(this.a*v.b+v.a*this.b,this.b*v.b);}
 mul(v){v=q(v);return new Q(this.a*v.a,this.b*v.b);}
 div(v){v=q(v);return new Q(this.a*v.b,this.b*v.a);}
 sub(v){return this.add(q(v).mul(new Q(-1n)));}
 lt(v){v=q(v);return this.a*v.b<v.a*this.b;}
 eq(v){v=q(v);return this.a===v.a&&this.b===v.b;}
 pow(k){assert(Number.isInteger(k)&&k>=0);return new Q(this.a**BigInt(k),this.b**BigInt(k));}
 toString(){return this.b===1n?String(this.a):this.a+"/"+this.b;}
}
function q(v){if(v instanceof Q)return v;if(typeof v==="string"&&v.includes("/")){const [a,b]=v.split("/");return new Q(a,b);}return new Q(v);}
function max(...xs){return xs.reduce((a,b)=>a.lt(b)?b:a);}
function min(a,b){return a.lt(b)?a:b;}
function envelope(c){
 c=q(c);let f=q(1),best=q(-1),win=0,checked=[];
 for(let k=1;k<80;k++){
  f=c.mul(f).div(q(1).add(f));
  const d=min(q(1).div(f).sub(c).div(k),q(1).div(c.pow(k)));
  checked.push([k,d.toString()]);if(best.lt(d)){best=d;win=k;}
  const future=q(1).div(c.pow(k+1));
  if(future.lt(best))return {boundary:best.toString(),winning_k:win,checked,
      excluded_from:k+1,tail_upper:future.toString()};
 }
 throw Error("tail not certified");
}
const sources={
 W1_UNSAT:[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]],
 S15_SAT:[[-1,-3,14],[2,8,-9],[-10,13,14],[3,-7,-13],[-4,9,-11],[-5,-8,-14],[4,-8,11],[1,7,-13],[1,-7,10],[-5,-6,15],[-2,6,-12],[4,9,-10],[-2,5,-12],[3,6,-15],[-6,7,11],[2,-9,-11],[-4,8,10],[-3,12,15],[5,12,-15],[-1,13,-14]],
 H8_UNSAT:[[1,2,3],[-1,2,3],[1,-2,3],[1,2,-3],[-1,-2,3],[-1,2,-3],[1,-2,-3],[-1,-2,-3]],
 HORN_SAT:[[-1,-2,3],[-1,2,3]],
 XOR3_SAT:[[1,2,-3],[1,-2,3],[-1,2,3],[-1,-2,-3]],
 XOR3_UNSAT:[[1,2,-3],[1,-2,3],[-1,2,3],[-1,-2,-3],[1,2,3],[1,-2,-3],[-1,2,-3],[-1,-2,3]]
};
function count(c,a){return c.reduce((r,x)=>r+(((a>>(Math.abs(x)-1)&1)===(x>0?1:0))?1:0),0);}
function audit(name,clauses){
 const n=Math.max(...clauses.flat().map(Math.abs));
 const modes=[];for(let j=0;j<clauses.length;j++)for(let k=j+1;k<clauses.length;k++){
  const a=clauses[j],b=clauses[k],same=a.some(x=>b.includes(x)),
      opposite=a.some(x=>b.includes(-x));
  modes.push({j,k,expected:(!opposite?9:0)|(!same?6:0),seen:0});
 }
 let models=0,complementChecks=0;
 const full=(1<<n)-1;
 for(let a=0;a<=full;a++){
  const t=clauses.map(c=>count(c,a));if(t.every(x=>x>0))models++;
  if(a<=(full^a))for(let j=0;j<t.length;j++){
   assert.strictEqual(t[j]+count(clauses[j],full^a),3);complementChecks++;
  }
  for(const p of modes){
   if(t[p.j]===3&&t[p.k]===3)p.seen|=1;
   if(t[p.j]===3&&t[p.k]===0)p.seen|=2;
   if(t[p.j]===0&&t[p.k]===3)p.seen|=4;
   if(t[p.j]===0&&t[p.k]===0)p.seen|=8;
  }
 }
 for(const p of modes)assert.strictEqual(p.seen,p.expected,name+" "+p.j+","+p.k);
 for(const c of clauses)for(const l of c){
  const S=+(l>0),U=+(l<0);assert.strictEqual(1-S,U);assert.strictEqual(1-U,S);
 }
 return {n,m:clauses.length,models,SAT:models>0,source_pairs:modes.length,
  pair_modes_verified:modes.length*4,complement_checks:complementChecks,
  endpoints:{allzero:clauses.map(c=>count(c,0)),allone:clauses.map(c=>count(c,full))}};
}
function budget(theta,beta,xi,rho){
 theta=q(theta);beta=q(beta);xi=q(xi);rho=q(rho);
 const c=q("241/200"),d=q("11642479/23232400"),lam=q("1/2");
 const k=max(q("11/10"),q("3/5").add(theta).add(rho),
     q("3/5").add(theta).add(beta).div(q(1).sub(lam).sub(xi)));
 const ell=max(q("1/2"),lam.add(xi));
 return {theta:theta.toString(),beta:beta.toString(),xi:xi.toString(),
  rho:rho.toString(),Kstar:k.toString(),Lstar:ell.toString(),
  joint:theta.add(beta).add(c.mul(xi)).toString(),
  time_eligible:k.lt(c),space_eligible:ell.lt(d),both_eligible:k.lt(c)&&ell.lt(d)};
}
function main(){
 const flmv={};for(const c of ["6/5","241/200","7/5","3/2","8/5"])flmv[c]=envelope(c);
 assert.strictEqual(flmv["6/5"].boundary,"23/45");
 assert.strictEqual(flmv["241/200"].boundary,"11642479/23232400");
 const budgets={
  zero:budget(0,0,0,"1/2"),
  jointly_small:budget("1/2000","1/2000","1/2000","1001/2000"),
  separately_small_but_fail:budget("1/600","1/600",0,"1/2"),
  space_only_fail:budget(0,0,"1/800","401/800"),
  full_parent_rescan:budget(0,0,0,1),
  strict_boundary:budget(0,"1/400",0,"1/2")
 };
 assert(!budgets.separately_small_but_fail.time_eligible);
 assert(budgets.space_only_fail.time_eligible&&!budgets.space_only_fail.space_eligible);
 assert(!budgets.full_parent_rescan.time_eligible);
 const controls={};for(const [name,clauses] of Object.entries(sources))controls[name]=audit(name,clauses);
 assert(controls.W1_UNSAT.models===0&&controls.S15_SAT.models===861);
 assert(controls.H8_UNSAT.models===0&&controls.XOR3_UNSAT.models===0);
 const result={run:"ARC-JOINT-SLACK267",status:"CONDITIONAL/COMPUTATIONAL; ARC OPEN",
       flmv,budgets,controls,note:"No arbitrary-A child constructor, no native TM transitions."};
 console.log(JSON.stringify(result,null,2));return result;
}
if(require.main===module)main();
module.exports={main,audit,envelope,budget};
