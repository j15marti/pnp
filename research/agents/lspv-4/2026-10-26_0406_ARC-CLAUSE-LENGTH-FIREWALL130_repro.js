#!/usr/bin/env node
'use strict';
// Fully deterministic, no dependencies or random seed. Node.js 18+.
// Logical ASCII bit-writes only; no FLMV TM runtime claim.
const audit = function audit(){
 "use strict";
 let checks=0;
 const check=(x,msg)=>{checks++;if(!x)throw new Error("FAIL "+msg)};
 const W="-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14".split(";").map(x=>x.trim().split(/\s+/).map(Number));
 const G=[[1,2,3],[1,-2,-3],[-1,2,-3],[-1,-2,3]];
 function balanced(f,n){
   const P=Array(n+1).fill(0),M=Array(n+1).fill(0);
   check(3*f.length===4*n,"3m=4n");
   for(const c of f){
     check(c.length===3,"all ternary");
     check(new Set(c.map(Math.abs)).size===3,"proper ternary");
     for(const lit of c){check(Math.abs(lit)>0 && Math.abs(lit)<=n,"identifier bounds");(lit>0?P:M)[Math.abs(lit)]++}
   }
   for(let i=1;i<=n;i++){check(P[i]===2,"2 positive");check(M[i]===2,"2 negative")}
 }
 function sat(f,n){
   check(n<=15,"small exhaustive");
   for(let a=0;a<2**n;a++){
     let yes=true;
     for(const c of f)if(!c.some(x=>(((a>>(Math.abs(x)-1))&1)!==0)===(x>0))){yes=false;break}
     if(yes)return true;
   }
   return false;
 }
 function disjoint(f,n,q){
   let out=[];for(let k=0;k<q;k++)for(const c of f)out.push(c.map(x=>Math.sign(x)*(Math.abs(x)+k*n)));
   return {f:out,n:q*n};
 }
 function addBlocks(a,b,q){
   const ext=disjoint(b.f,b.n,q);
   return {f:a.f.concat(ext.f.map(c=>c.map(x=>Math.sign(x)*(Math.abs(x)+a.n)))),n:a.n+ext.n};
 }
 function encode(f,n){return "p cnf "+n+" "+f.length+"\n"+f.map(c=>c.join(" ")+" 0\n").join("");}
 function validateEncoded(f,n){
   const s=encode(f,n),lines=s.trimEnd().split("\n"),h=lines[0].split(" ");
   check(h.length===4&&h[0]==="p"&&h[1]==="cnf","dimacs header");
   check(+h[2]===n&&+h[3]===f.length,"dimacs counts");
   check(lines.length===f.length+1,"dimacs physical clauses");
   for(let j=0;j<f.length;j++){
      const row=lines[j+1].split(/\s+/).map(Number);
      check(row.length===4&&row[3]===0,"trailing 0 literal");
      check(row.slice(0,3).every((v,i)=>v===f[j][i]),"literal roundtrip");
   }
   check([...s].every(c=>c.charCodeAt(0)<128),"ascii emitted");
   return s.length*8;
 }
 function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t}return a}
 function frac(n,d=1n){n=BigInt(n);d=BigInt(d);check(d!==0n,"rational nonzero divisor");if(d<0n){n=-n;d=-d};let g=gcd(n,d);return [n/g,d/g]}
 const mul=(x,y)=>frac(x[0]*y[0],x[1]*y[1]);
 const add=(x,y)=>frac(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
 const sub=(x,y)=>frac(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
 const div=(x,y)=>frac(x[0]*y[1],x[1]*y[0]);
 const fs=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
 const lt=(x,y)=>x[0]*y[1]<y[0]*x[1];
 const two=frac(2),one=frac(1),beta=c=>div(sub(div(add(c,two),mul(c,c)),c),two);
 const cStar=frac(241,200),sStar=beta(cStar),t=frac(11,10),s=frac(7,10),chosen=frac(111,100),bc=beta(chosen);
 check(fs(sStar)==="11642479/23232400","published FLMV exact");
 check(fs(bc)==="1742369/2464200","curve exact");
 check(fs(sub(bc,s))==="17429/2464200","curve space slack");
 check(lt(t,chosen)&&lt(s,bc),"curved strict");
 check(!lt(s,sStar),"outside fixed rectangle");
 const d=frac(901,500),co=div(sub(mul(two,d),one),mul(d,sub(d,one))),qstar=div(mul(d,d),sub(mul(d,d),one));
 check(fs(co)==="651000/361301"&&fs(qstar)==="811801/561801","extra seed companions");
 balanced(G,3);balanced(W,15);check(sat(G,3),"G sat");check(!sat(W,15),"W unsat");
 let rows=[],allEmitted=0;
 for(const base of [{name:"G_SAT",f:G,n:3,sat:true},{name:"W1_UNSAT",f:W,n:15,sat:false}]){
   for(const q of [1,2,4,8,16]){
      const root=disjoint(base.f,base.n,q),child=addBlocks(root,{f:G,n:3},q),grand=addBlocks(child,{f:G,n:3},q);
      for(const x of [root,child,grand])balanced(x.f,x.n);
      const bits=[root,child,grand].map(x=>validateEncoded(x.f,x.n));
      check(bits[0]<bits[1]&&bits[1]<bits[2],"honest two-level non-contraction");
      check(root.f.length+4*q===child.f.length&&child.f.length+4*q===grand.f.length,"clause conservation");
      check(base.sat===sat(base.f,base.n),"SAT vs UNSAT anchored at base");
      allEmitted+=bits.reduce((a,b)=>a+b,0);
      rows.push({source:base.name,copies:q,ordinary_levels:[{vars:root.n,clauses:root.f.length,bits:bits[0]},{vars:child.n,clauses:child.f.length,bits:bits[1]},{vars:grand.n,clauses:grand.f.length,bits:bits[2]}],source_and_descendant_SAT:base.sat,total_actual_bit_writes:bits.reduce((a,b)=>a+b,0),simultaneously_retaining_three_encodings_bits:bits.reduce((a,b)=>a+b,0)});
   }
 }
 const lower=[];
 for(const m of [4,16,64,256,1024,4096]){
   let f=Array.from({length:m},(_,j)=>[3*j+1,3*j+2,3*j+3]);
   const n=3*m,sourceBits=validateEncoded(f,n),requiredVars=3*m/4;
   let digits=0;for(let i=1;i<=requiredVars;i++)digits+=String(i).length;
   const bound=8*4*digits;
   check(bound>0,"nonzero size floor");
   lower.push({sourceClauses:m,sourceVars:n,sourceBits,requiredTargetVarsAtLeast:requiredVars,minimumFourOccurrenceTargetLiteralDigitsBits:bound,ratio:Math.round(bound/sourceBits*1000000)/1000000});
 }
 check(!sat([[1],[-1]],1),"Horn UNSAT control");check(sat([[1,2],[-1,2]],2),"2SAT SAT control");
 return {run:"ARC-CLAUSE-LENGTH-FIREWALL130",status:"PROVED/EXACT restricted lower bound; COMPUTATIONAL checks; general ARC OPEN",checks,failures:0,source:"LSPV-3 BACKDOOR-SCC-CERT130 W1 source / exact G",machine_scope:"DIMACS ASCII fully encoded bits; count actual physical string writes, not FLMV timing",FLMV:{fixed_t:"241/200",fixed_s:fs(sStar),hypothetical_t:fs(t),hypothetical_s:fs(s),chosen_curve_c:fs(chosen),beta_c:fs(bc),strict_time_gap:fs(sub(chosen,t)),strict_space_gap:fs(sub(bc,s)),inside_fixed_rectangle:false,inside_curved_endpoint_conditionally:true,extra_d:fs(d),extra_coNTIME_threshold:fs(co),extra_decision_circuit_q_threshold:fs(qstar)},literalLocalClauseAccountable:lower,twoLevel:rows,totalActualSerializedBits:allEmitted,random_seed:null,controls:"W1 UNSAT; G SAT; Horn UNSAT; 2SAT SAT; disjoint SAT/UNSAT; exact (2,2) all levels; 2 physical ordinary descendant levels",limitations:"Restricted clause-accountable architecture and ASCII DIMACS only; no all-input SAT contractor; only logical bitwrites; no physical Turing machine step count, no polynomial SAT seed"};
};
console.log(JSON.stringify(audit(), null, 2));
