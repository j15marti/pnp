"use strict";
/* ARC-HEAD-HORIZON-REPLAY255, LSPV-1, reproducible Node 18+
   Scope: read-only input-head + explicitly charged binary-address jump stream.
   All counted costs are abstract logical events, not native FLMV TM steps. */
let assertions=0;
function ck(x,s){assertions++;if(!x)throw Error(s)}
const size=x=>x?Math.floor(Math.log2(x))+1:1;
const J=x=>({jump:x});
function tape(F,n){
 const w=Math.max(1,Math.ceil(Math.log2(n+1)));
 return "1".repeat(n+1)+"0"+F.map(c=>c.map(l=>(l<0?"1":"0")+Math.abs(l).toString(2).padStart(w,"0")).join("")).join("0")+"1";
}
function clause(c,a){return c.reduce((s,l)=>s+(((a>>(Math.abs(l)-1)&1)===(l>0?1:0))?1:0),0)}
function hist(F,a){let h=[0,0,0,0];F.forEach(c=>h[clause(c,a)]++);return h}
function modelCount(F,n){let v=0;for(let a=0;a<(1<<n);a++)if(F.every(c=>clause(c,a)>0))v++;return v}
function dpll(F,n){
 let s={nodes:0,source_reads:0,literal_reads:0};
 function visit(b){
  s.nodes++;let a=b.slice();
  while(true){
   let force=0,all=true;
   for(let c of F){
    s.source_reads++;let sat=false,unknown=[];
    for(let l of c){s.literal_reads++;let v=a[Math.abs(l)];
     if(v===-1)unknown.push(l);else if(v===(l>0?1:0)){sat=true;break;}}
    if(sat)continue;
    all=false;if(!unknown.length)return false;
    if(unknown.length===1){force=unknown[0];break;}
   }
   if(all)return true;
   if(!force)break;
   a[Math.abs(force)]=force>0?1:0;
  }
  let v=a.findIndex((x,i)=>i>0&&x===-1);
  if(v<0)return false;
  for(let k of [0,1]){let aa=a.slice();aa[v]=k;if(visit(aa))return true}
  return false;
 }
 s.SAT=visit(Array(n+1).fill(-1));return s;
}
function extreme(F){
 return F.map((c,j)=>({clause:j+1,source:c,
 occurrences:c.map((l,k)=>({i:Math.abs(l),j:j+1,position:k+1,sign:l>0?"+":"-",
   S:l>0?1:0,inverted_S:l>0?0:1,U:l>0?0:1,inverted_U:l>0?1:0}))}));
}
function compat(F){
 let checked=0,blocked=0,examples=[];
 for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++){
  let a=F[i],b=F[j],same=a.some(l=>b.includes(l)),opp=a.some(l=>b.includes(-l)),
  flags={SS:!opp,SU:!same,US:!same,UU:!opp},vars=[...new Set(a.concat(b).map(Math.abs))];
  for(let m of ["SS","SU","US","UU"]){
   let possible=false;
   for(let z=0;z<(1<<vars.length);z++){
    let v=new Map(vars.map((x,k)=>[x,z>>k&1]));
    let good=(c,mode)=>c.every(l=>v.get(Math.abs(l))===((l>0)===(mode==="S")?1:0));
    if(good(a,m[0])&&good(b,m[1])){possible=true;break;}
   }
   ck(possible===flags[m],"compatibility");
   checked++;if(!possible)blocked++;
  }
  if(examples.length<5)examples.push({clauses:[i+1,j+1],same,opposite:opp,...flags});
 }
 return {checked,blocked,examples};
}
function flips(F,n){
 let seq=[0,1,Math.min(3,(1<<n)-1),(1<<n)-1,0],prev=0,out=[];
 for(let a of seq){
  F.forEach(c=>{let d=c.reduce((s,l)=>((prev^a)>>(Math.abs(l)-1)&1)?
      s+(((prev>>(Math.abs(l)-1)&1)===(l>0?1:0))?-1:1):s,0);
    ck(clause(c,a)-clause(c,prev)===d,"flip identity")});
  let h=hist(F,a);out.push({mask:a,N:h,SAT:h[0]===0,complement_SAT:F.every(c=>clause(c,a)<c.length)});prev=a;
 }
 return out;
}
function execute(y,program,B,mode){
 let p=0,far=false,reads=[],charge={steps:0,address_bits:0,child_reads:0,blank_reads:0,head_bit_updates:0};
 const cap=y.length+B;
 for(let t=0;t<Math.min(B,program.length);t++){
  let cmd=program[t];charge.steps++;
  if(typeof cmd==="object"){
   let digits=cmd.jump.toString(2);charge.address_bits+=digits.length;
   if(mode==="physical"){p=cmd.jump;far=false}
   else if(mode==="sticky"){p=cmd.jump;far=p>=y.length}
   else {let v=0;for(let d of digits)v=Math.min(cap+1,2*v+(d==="1"?1:0));p=v;far=v>cap}
  }else if(cmd==="L"||cmd==="R"){
   if(!far){p=cmd==="L"?Math.max(0,p-1):p+1;
    if(mode==="clip"&&p>cap){p=cap+1;far=true}}
   charge.head_bit_updates+=size(p)+1;
  }else if(cmd==="READ"){
   let x=far||p>=y.length?"_":y[p];
   reads.push(x);if(x==="_")charge.blank_reads++;else charge.child_reads++;
  }else if(cmd!=="HALT")throw Error("invalid");
 }
 return {reads,charge,halted:B>=program.length};
}
function replay(y,P){
 let B=1,acc={epochs:0,steps:0,address_bits:0,head_bit_updates:0,child_reads:0,blank_reads:0},last;
 for(let k=0;k<24;k++){
  last=execute(y,P,B,"clip");acc.epochs++;
  for(let f of ["steps","address_bits","head_bit_updates","child_reads","blank_reads"])acc[f]+=last.charge[f];
  if(last.halted)break;B*=2;
 }
 ck(last.halted,"termination");ck(acc.steps<4*P.length+1,"replay step bound");
 return {reads:last.reads,acc,cap_budget:B,head_bits:Math.ceil(Math.log2(y.length+B+2))};
}
function audit(name,F,n,seed0){
 let z=dpll(F,n),models=modelCount(F,n);ck(z.SAT===(models>0),"DPLL vs enumeration");
 let e=extreme(F);for(let row of e)for(let v of row.occurrences)
  ck(v.S===v.inverted_U&&v.U===v.inverted_S,"occurrence invert");
 let p=compat(F),zero=hist(F,0),one=hist(F,(1<<n)-1);
 if(F.every(c=>c.length===3))ck(zero.join(",")===one.slice().reverse().join(","),"width3 complement");
 else F.forEach(c=>ck(clause(c,0)+clause(c,(1<<n)-1)===c.length,"width-sensitive complement"));
 let trail=flips(F,n),y=tape(F,n),m=y.length;
 let guard=[J(m+1),"L","L","READ",J(m-1),"READ","HALT"];
 let a=execute(y,guard,guard.length,"physical"),b=replay(y,guard),bad=execute(y,guard,guard.length,"sticky");
 ck(a.reads.join("")===b.reads.join(""),"guarded replay");
 ck(a.reads.join("")==="11"&&bad.reads.join("")==="_1","sticky false");
 let label=models?1:0;
 ck((label^(b.reads[0]!==b.reads[1]?1:0))===label,"sound labels");
 ck((label^(bad.reads[0]!==bad.reads[1]?1:0))!==label,"sticky reverses both labels");
 let seed=seed0>>>0;const rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};
 let random={seed:seed0,traces:0,reads:0,epochs:0};
 for(let j=0;j<70;j++){
  let q=8+rng()%35,P=[];
  for(let k=0;k<q;k++){
   let t=rng()%7;
   if(t<2){let choices=[0,1,m-1,m,m+1,m+8,m+99,2**35,2**40];P.push(J(choices[rng()%choices.length]));}
   else P.push(["L","R","READ","R","READ"][t-2]);
  }
  let exact=execute(y,P,q,"physical"),clip=execute(y,P,q,"clip"),r=replay(y,P);
  ck(exact.reads.join("")===clip.reads.join(""),"horizon complete");
  ck(exact.reads.join("")===r.reads.join(""),"geometric complete");
  random.traces++;random.reads+=exact.reads.length;random.epochs+=r.acc.epochs;
 }
 let original_work=z.source_reads+z.literal_reads,
  wrapper_work=original_work+2*y.length+b.acc.steps+b.acc.address_bits+
                b.acc.head_bit_updates+guard.length;
 return {name,n,source:F,models,label:label?"SAT":"UNSAT",
  original_targets:e,compatibility:p,endpoints:{zero,one},flip_trail:trail,
  solver:{...z,original_work,wrapper_work},head:{physical:a.reads,clipped:b.reads,
     sticky:bad.reads,replay:b.acc,head_bits:b.head_bits},random};
}
function xor3(p){let r=[];for(let a=0;a<8;a++)if(((a&1)^((a>>1)&1)^((a>>2)&1))!==p)
  r.push([1,2,3].map(v=>(a>>(v-1)&1)?-v:v));return r}
function runAudit(){
 assertions=0;let pattern=[];for(let a=0;a<8;a++)
  pattern.push([1,2,3].map(v=>(a>>(v-1)&1)?-v:v));
 const W="-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14";
 const W1=W.split(";").map(c=>c.trim().split(/\s+/).map(Number));
 const H=[[1,3,5],[1,-3,6],[-1,4,5],[-1,-4,6],[2,3,-5],[2,-3,-6],[-2,4,-5],[-2,-4,-6]];
 let inputs=[["3CNF_7of8_SAT",pattern.slice(1),3],
 ["3CNF_8of8_UNSAT",pattern,3],["strict22_H_SAT",H,6],
 ["strict22_W1_UNSAT",W1,15],["XOR3_SAT",xor3(1),3],
 ["XOR3_both_UNSAT",xor3(0).concat(xor3(1)),3],
 ["Horn_SAT",[[-1,-2,3],[-3,-2,1]],3],
 ["Krom_UNSAT",[[1,2],[-1,2],[1,-2],[-1,-2]],2]];
 let cases=inputs.map(([name,F,n],i)=>audit(name,F,n,20261030+107*i));
 for(let i=0;i<cases.length;i+=2){ck(cases[i].models>0,"SAT control");ck(cases[i+1].models===0,"UNSAT control")}
 for(let j=0;j<1200;j++){let y="1".repeat(37),h=(j*99371+41)%(2**40);
  let P=[J(h),"L","R","READ"];
  ck(execute(y,P,64,"physical").reads.join("")===execute(y,P,64,"clip").reads.join(""),"huge jump");}
 return {id:"ARC-HEAD-HORIZON-REPLAY255",local_date:"2026-10-30 14:58 PDT",
  assertions,cases,status:"PROVED/EXACT restricted head model, independent review pending",
  compiler:"OPEN",P_vs_NP:"OPEN",limit:"Not a full same-machine virtual-child or all-input ARC contraction."};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)
 console.log(JSON.stringify(runAudit(),null,2));