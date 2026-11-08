#!/usr/bin/env node
'use strict';
// LSPV-1/513: independent native syntactic Res(PC_1/F_2) gate audit.
// Original source axioms only; no native R_mix341 byte grammar asserted.
(function(){
const ok=(b,m)=>{if(!b)throw Error(m||'failed')};
const e=(m,r)=>m+','+(r&1), dec=x=>x.split(',').map(Number);
const l=(...a)=>[...new Set(a)].sort();
const not=x=>{let [m,r]=dec(x);return e(m,r^1)};
const add=(x,y)=>{let a=dec(x),b=dec(y);return e(a[0]^b[0],a[1]^b[1])};
const same=(x,y)=>JSON.stringify(x)===JSON.stringify(y);
const source=ls=>l(...ls.map(x=>e(1<<(Math.abs(x)-1),x>0?1:0)));
class Proof{
constructor(n,s){this.n=n;this.s=s;this.nodes=[];this.count={};this.ids=s.map(x=>this.put('source',x))}
put(kind,x,par=[],sel=[]){
 let q=l(...x);
 if(kind==='source')ok(this.s.some(z=>same(q,z)),'source');
 else if(kind==='bool')ok(Array.from({length:this.n},(_,i)=>i).some(i=>same(q,l(e(1<<i,0),e(1<<i,1)))),'bool');
 else if(kind==='true')ok(same(q,l(e(0,0))),'true');
 else if(kind==='weak')ok(par.length===1&&this.nodes[par[0]].q.every(t=>q.includes(t)),'weak');
 else if(kind==='sum'){
   ok(par.length===2,'parents');let a=this.nodes[par[0]].q,b=this.nodes[par[1]].q;
   ok(a.includes(sel[0])&&b.includes(sel[1]),'selected');
   ok(same(q,l(...a.filter(t=>t!==sel[0]),...b.filter(t=>t!==sel[1]),add(...sel))),'sum');
 }else if(kind==='del'){
   ok(par.length===1&&this.nodes[par[0]].q.includes(e(0,1)),'false');
   ok(same(q,this.nodes[par[0]].q.filter(t=>t!==e(0,1))),'delete');
 }else throw Error('unknown rule');
 ok(par.every(i=>Number.isInteger(i)&&i>=0&&i<this.nodes.length),'parent');
 let id=this.nodes.length;this.nodes.push({kind,q,par,sel});this.count[kind]=(this.count[kind]||0)+1;return id;
}
ax(i){return this.put('bool',l(e(1<<(i-1),0),e(1<<(i-1),1)))}
sum(p,q,a,b){return this.put('sum',l(...this.nodes[p].q.filter(t=>t!==a),...this.nodes[q].q.filter(t=>t!==b),add(a,b)),[p,q],[a,b])}
cut(p,q,a){ok(this.nodes[p].q.includes(a)&&this.nodes[q].q.includes(not(a)),'pivot');
let t=this.sum(p,q,a,not(a));return this.put('del',this.nodes[t].q.filter(x=>x!==e(0,1)),[t])}
}
const n=16,S=[source([1]),source([-1]),...Array.from({length:n-1},(_,i)=>source([i+2]))];
const P=new Proof(n,S),B={};for(let i=1;i<=n;i++)B[i]=P.ax(i);
let u=1,pre=B[1],plus=P.ids[0],minus=P.ids[1],max=1;
for(let v=2;v<=n;v++){
 let vm=1<<(v-1),z=u^vm,f={};
 for(let a=0;a<2;a++)for(let b=0;b<2;b++)
   f[a+','+b]=P.sum(pre,B[v],e(u,a),e(vm,b));
 let p0=P.cut(f['0,0'],f['1,0'],e(u,1));
 let p1=P.cut(f['0,1'],f['1,1'],e(u,1));
 let next=P.cut(p0,p1,e(vm,1));
 ok(same(P.nodes[next].q,l(e(z,0),e(z,1))),'Bz');
 function step(id){
  let a=dec(P.nodes[id].q[0])[1];
  let t=P.cut(f[a+',1'],id,e(u,1-a));
  t=P.cut(t,P.ids[v],e(vm,0));
  ok(same(P.nodes[t].q,l(e(z,a^1))),'carry');
  return t;
 }
 plus=step(plus);minus=step(minus);u=z;pre=next;
 max=Math.max(max,u.toString(2).replace(/0/g,'').length);
}
let root=P.cut(plus,minus,P.nodes[plus].q[0]);
ok(P.nodes[root].q.length===0,'empty');
let attacks=0;
for(let a of ['source','true','parent','sum']){
 try{
 if(a==='source')P.put('source',source([1,2,3]));
 else if(a==='true')P.put('true',[e(0,1)]);
 else if(a==='parent')P.put('del',[],[P.nodes.length+5]);
 else P.sum(P.ids[0],P.ids[1],e(1,1),e(1,1));
 }catch(err){attacks++;continue}
 throw Error('hostile accepted');
}
const edges=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);
const cube=()=>Array.from({length:64},(_,i)=>i);
const holds=(x,a)=>{let [m,r]=dec(x),p=0;while(m){let bit=m&(-m);p^=((a&bit)?1:0);m-=bit}return p===r};
function tseitin(charge){
 let C=[];for(let v=0;v<4;v++){
  let inc=edges.map((ab,i)=>ab.includes(v)?i+1:0).filter(Boolean);
  for(let a=0;a<8;a++){let bits=[a&1,(a>>1)&1,(a>>2)&1];
    if((bits[0]^bits[1]^bits[2])!==charge[v])
      C.push(source(inc.map((x,j)=>bits[j]?-x:x)));
  }
 }return C;
}
const models=F=>cube().filter(a=>F.every(C=>C.some(x=>holds(x,a)))).length;
let odd=tseitin([1,0,0,0]),even=tseitin([0,0,0,0]);
ok(odd.length===16&&even.length===16&&models(odd)===0&&models(even)===8,'K4 models');
let result={status:'PASS',source_count:S.length,affine_gates:15,full_original_support:max,
native_target_proof_nodes:P.nodes.length,root_empty:true,hostile_rejections:attacks,
odd_K4_clauses:odd.length,odd_K4_models:0,even_K4_models:8,
target_rules:Object.keys(P.count),historical_Rmix341_checker_executed:false};
if(typeof console!=='undefined')console.log(JSON.stringify(result));return result;
})();
