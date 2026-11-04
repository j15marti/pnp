"use strict";
let checks=0;function ok(c,m){checks++;if(!c)throw Error(m||"assert")}
const E=(m,b)=>[m,b],val=(e,a)=>{let v=0;for(let i=0;i<3;i++)if((e[0]>>i)&1)v^=(a>>i)&1;return v===e[1]},
  sat=(c,a)=>c.some(e=>val(e,a)),implies=(c,d)=>Array.from({length:8},(_,a)=>!sat(c,a)||sat(d,a)).every(Boolean),
  K=c=>c.map(e=>e.join(':')).sort().join('|');
function resolve(c,d,p){const n=E(p[0],1-p[1]);ok(c.some(x=>K([x])===K([p]))&&d.some(x=>K([x])===K([n])),"invalid pivot");
  const z=Array.from(new Map([...c.filter(x=>K([x])!==K([p])),...d.filter(x=>K([x])!==K([n]))].map(x=>[K([x]),x])).values());
  for(let a=0;a<8;a++)ok(!(sat(c,a)&&sat(d,a))||sat(z,a),"unsound resolution");return z;}
function main(){
const X=1,W=2,Y=4, x=[E(X,1)], w=[E(W,1)], C=[E(X,0),E(W,0)],
  d1=[E(Y,0),E(X,1)],d2=[E(Y,0),E(W,1)],d3=[E(Y,1),E(X,0),E(W,0)];
const r1=resolve(C,d1,E(X,0)),r2=resolve(r1,d2,E(W,0)),
 r3=resolve(x,d3,E(X,1)),r4=resolve(r3,w,E(W,0)),r5=resolve(r4,r2,E(Y,1));
ok(r5.length===0,"mixed proof root");
for(let a=0;a<4;a++){const y=((a&1)&&(a&2))?1:0;for(let d of [d1,d2,d3])ok(sat(d,a|(y<<2)),"DEF facet");}
const g1=[E(X,0),E(W,1)],g2=[E(X,0),E(W,0)];ok(implies(w,g1)&&implies(C,g2),"guard lift");
const z=resolve(g1,g2,E(W,1));ok(K(z)===K([E(X,0)]),"guarded branch");
ok(resolve(x,z,E(X,1)).length===0,"authentic source proof");
let binary_gate_cases=0,nested_cases=0;
for(let tab=0;tab<16;tab++)for(let a=0;a<2;a++){const f0=(tab>>(2*a))&1,f1=(tab>>(2*a+1))&1;
 for(let b=0;b<2;b++){ok(((tab>>(2*a+b))&1)===(f0===f1?f0:(f0===0?b:1-b)),"binary gate cofactor");binary_gate_cases++;}}
for(let p=0;p<16;p++)for(let q=0;q<16;q++)for(let a=0;a<2;a++)for(let b=0;b<2;b++){
 const y=(p>>(2*a+b))&1;ok(((q>>(2*y+a))&1)===((q>>(2*((p>>(2*a+b))&1)+a))&1),"nested gate");nested_cases++;}
let affine_pairs=0,degenerate_pairs=0;
for(let m1=0;m1<8;m1++)for(let b1=0;b1<2;b1++)for(let m2=0;m2<8;m2++)for(let b2=0;b2<2;b2++){
 const v1=E(m1,b1),v2=E(m2,b2),sum=E(m1^m2,b1^b2),weak=[sum,E(m2,1-b2)];
 ok(implies([v1],weak),"affine sum weakening");affine_pairs++;
 if(m1!==0&&m2!==0){const r=resolve(weak,[v2],E(m2,1-b2));ok(K(r)===K([sum]),"affine cut");}
 else{degenerate_pairs++;for(let a=0;a<8;a++)ok(!(val(v1,a)&&val(v2,a))||val(sum,a),"degenerate XOR");}}
const bad=[[[7,2]],[[8,0]],[["x",0]],[[1,-1]]];for(let c of bad)
 ok(!c.every(e=>Array.isArray(e)&&e.length===2&&Number.isInteger(e[0])&&e[0]>=0&&e[0]<8&&(e[1]===0||e[1]===1)),"malformed");
let caught=false;try{resolve([E(X,1)],[E(X,1)],E(X,1));}catch(e){caught=true;}ok(caught,"forged pivot");
return {id:"LSPV-1-397",status:"COMPUTATIONAL finite controls",checks,binary_gate_cases,nested_cases,affine_pairs,degenerate_pairs,
  source:{x:"(x)",w:"(w)",third:"(not x OR not w)",UNSAT:true,sat_sibling:"(x) AND (w)"},
  original_mixed_witness:{DEF:1,RES:5},translated_same_source_witness:{DEF:0,RES:2},
  cautions:"not all-rule Rmix341 or arbitrary-machine hardness"};}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(main(),null,2));