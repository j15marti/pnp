"use strict";
// Dependency-free Node.js 18+; no randomness. Full original occurrence S/U, pair modes, exact enumeration,
// source witnesses, UP-DPLL work, and partial-state cardinality controls.
function reproduce(){
const ok=(x,m)=>{if(!x)throw Error(m)};
const W="-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14".split(";").map(x=>x.trim().split(/\s+/).map(Number));
const V=W.map(x=>x.slice());ok(V[7][0]===1&&V[19][0]===-1,"verified source");V[7][0]=-1;V[19][0]=1;
const H=[[1,3,5],[1,-3,6],[-1,4,5],[-1,-4,6],[2,3,-5],[2,-3,-6],[-2,4,-5],[-2,-4,-6]],X=[[1,2,3],[1,-2,-3],[-1,2,-3],[-1,-2,3]],Y=[[-1,-2,-3],[-1,2,3],[1,-2,3],[1,2,-3]];
const inputs=[["W1_UNSAT",15,W,0],["W1_SWAP_SAT",15,V,168],["H1_SAT",6,H,4],["XOR3_SAT",3,X,4],["XOR3_UNSAT",3,X.concat(Y),0],["HORN_SAT",3,[[-1,2],[-2,3],[1]],1],["HORN_UNSAT",2,[[1],[-1,2],[-2]],0],["KROM_SAT",2,[[1,2],[-1,2]],2],["KROM_UNSAT",2,[[1],[2],[-1,-2]],0]];
const lit=(l,a)=>((a>>>(Math.abs(l)-1))&1)===(l>0?1:0);
const hist=(C,a)=>{let N=[0,0,0,0],t=[];for(const cl of C){let q=cl.filter(l=>lit(l,a)).length;N[q]++;t.push(q);}return {N,t,sat:t.map(v=>v>0)}};
function solve(C,n){
 let S={nodes:0,leaves:0,work:0,branches:0,depth:0,witness:null};
 function rec(A,d){
  S.nodes++;S.depth=Math.max(S.depth,d);let change=true;
  while(change){
   change=false;let all=true;
   for(const cl of C){
    let u=0,last=0,sat=false;
    for(const l of cl){S.work++;let z=A[Math.abs(l)-1];if(z<0){u++;last=l;}else if(z===(l>0?1:0)){sat=true;break;}}
    if(sat)continue;all=false;
    if(u===0){S.leaves++;return false;}
    if(u===1){let v=Math.abs(last)-1,bit=last>0?1:0;if(A[v]>=0&&A[v]!==bit){S.leaves++;return false;}if(A[v]<0){A[v]=bit;S.work++;change=true;}}
   }
   if(all&&!change){S.witness=A.map(x=>x<0?0:x);return true;}
  }
  let v=0;while(v<n&&A[v]>=0){v++;S.work++;}
  if(v===n){S.witness=A.slice();return true;}
  for(const b of [0,1]){let B=A.slice();S.work+=n;B[v]=b;S.branches++;if(rec(B,d+1))return true;}return false;
 }
 S.sat=rec(Array(n).fill(-1),0);
 if(S.sat){ok(C.every(c=>c.some(l=>S.witness[Math.abs(l)-1]===(l>0?1:0))),"original witness");S.work+=C.reduce((a,c)=>a+c.length,0);}
 return S;
}
function matrix(C){
 let rows=[],checks=0,exception=0,both=0;
 for(let j=0;j<C.length;j++)for(let k=j+1;k<C.length;k++){
  let same=false,opp=false;
  for(const l of C[j])for(const r of C[k])if(Math.abs(l)===Math.abs(r)){if(l*r>0)same=true;else opp=true;}
  let row={j,k,SS:!opp,SU:!same,US:!same,UU:!opp,same,opp};
  if(same||opp)exception++;if(same&&opp)both++;
  let v=[...new Set(C[j].concat(C[k]).map(Math.abs))];
  for(const mode of ["SS","SU","US","UU"]){
   let found=false;
   for(let b=0;b<(1<<v.length);b++){
    let feas=true;
    for(let side=0;side<2&&feas;side++)for(const l of (side===0?C[j]:C[k])){
     if(((b>>v.indexOf(Math.abs(l)))&1)!==((l>0?1:0)^(mode[side]==="U"?1:0))){feas=false;break;}
    }
    checks++;if(feas){found=true;break;}
   }
   ok(found===row[mode],"pair source mode");
  }
  rows.push(row);
 }
 return {rows,exception,both,checks};
}
function triples(C,limit){
 let count=0,modes=0;
 for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++)for(let k=j+1;k<C.length;k++){
  if(count>=limit)return {count,modes,exhaustive:false};
  const cs=[C[i],C[j],C[k]],v=[...new Set(cs.flat().map(Math.abs))];
  for(let mode=0;mode<8;mode++){
   let a=new Map(),possible=true;
   for(let z=0;z<3;z++)for(const l of cs[z]){let x=Math.abs(l),b=(l>0?1:0)^((mode>>z)&1);if(a.has(x)&&a.get(x)!==b)possible=false;a.set(x,b);}
   let brute=false;
   for(let bits=0;bits<(1<<v.length);bits++){
    let good=true;for(let z=0;z<3&&good;z++)for(const l of cs[z])if(((bits>>v.indexOf(Math.abs(l)))&1)!==((l>0?1:0)^((mode>>z)&1))){good=false;break;}
    if(good){brute=true;break;}
   }
   ok(possible===brute,"triple");modes++;
  }count++;
 }
 return {count,modes,exhaustive:true};
}
let results=[],complement_checks=0,pair_checks=0,triple_checks=0;
for(let [name,n,C,expect] of inputs){
 let E=C.map((cl,j)=>({j,occurrences:cl.map((l,k)=>({j,k,variable:Math.abs(l),literal:l,S:+(l>0),S_inverted:+(l<0),U:+(l<0),U_inverted:+(l>0)}))}));
 let P=matrix(C),T=triples(C,C.length<=8?100000:18),models=0;
 for(let a=0;a<(1<<n);a++){let h=hist(C,a),z=hist(C,((1<<n)-1)^a);for(let j=0;j<C.length;j++){ok(h.t[j]+z.t[j]===C[j].length,"complement length");complement_checks++;}if(!h.N[0])models++;}
 ok(models===expect,"expected models "+name);
 let B=solve(C,n);ok(B.sat===(models>0),"both labels "+name);
 let flips=[...new Set([0,1,3,7,(1<<n)-1].filter(x=>x<(1<<n)))].map(mask=>({mask,...hist(C,mask)}));
 let prepass=4*C.reduce((s,c)=>s+c.length,0)+9*C.length*(C.length-1)/2+P.checks+T.modes*(1<<Math.min(n,9))+flips.length*C.reduce((s,c)=>s+c.length,0);
 if(name.startsWith("W1"))ok(P.exception<=6*n,"strict22 sparse edges");
 pair_checks+=4*P.rows.length;triple_checks+=T.modes;
 results.push({name,n,m:C.length,models,per_original_occurrence_S_U: E,clause_pair_SS_SU_US_UU:P.rows,pair_exception_edges:P.exception,pair_both:P.both,triple_modes:T,global_zero_one_and_flip_trail:flips,baseline_UP_DPLL:B,paid_extreme_diagnostic_plus_same_DPLL:{nodes:B.nodes,extra_selected_operations:prepass,total_selected_operations:B.work+prepass}});
}
const binom=(n,k)=>{let a=1;for(let j=1;j<=k;j++)a=Math.round(a*(n-j+1)/j);return a;};
function states(n,t){
 let M=binom(n,t)*2**t,bits=Math.ceil(Math.log2(M)),count=0,seen=new Set(),lowmap=new Map(),collision=null;
 for(let mask=0;mask<(1<<n);mask++){
  let v=[];for(let i=0;i<n;i++)if(mask&(1<<i))v.push(i);
  if(v.length!==t)continue;
  for(let z=0;z<(1<<t);z++){
   let a=Array(n).fill(0);for(let j=0;j<t;j++)a[v[j]]=1+((z>>j)&1);
   let code=0;for(let i=n-1;i>=0;i--)code=code*3+a[i];
   ok(!seen.has(code),"injective digits");seen.add(code);count++;
   if(!collision){let key=code%2**(bits-1);if(lowmap.has(key)&&lowmap.get(key)!==code){let old=lowmap.get(key);collision={bits_truncated:bits-1,old_code:old,new_code:code,distinguishing_variable:Array.from({length:n},(_,i)=>i+1).find(i=>Math.floor(old/3**(i-1))%3!==Math.floor(code/3**(i-1))%3)}}else lowmap.set(key,code);}
  }
 }
 ok(count===M&&collision,"state pigeonhole");
 return {n,pins:t,distinct_partial_states:M,minimum_bits:bits,exhaustively_enumerated:count,collision};
}
let state_controls=[states(6,3),states(12,6),states(15,5)];
for(let a=0;a<64;a++)if([1,5,6].every(l=>!lit(l,a)))ok(!H.every(c=>c.some(l=>lit(l,a))),"resolution cube");
return {id:"LSPV4_ARC_ASSIGNMENT_STATE_FIREWALL259",result:"PASS",seed:null,scope:"Exact state-query-interface information bound and finite source controls. No unrestricted SAT hardness.",counts:{sources:results.length,complement_original_occurrence_checks:complement_checks,pair_mode_checks:pair_checks,triple_mode_checks:triple_checks},state_controls,source_certified_cube:{parent_indices:[0,1],pivot:3,resolvent:[1,5,6],falsifying_pins:{1:0,5:0,6:0}},benchmarks:results};
}
process.stdout.write(JSON.stringify(reproduce(),null,2)+"\n");
