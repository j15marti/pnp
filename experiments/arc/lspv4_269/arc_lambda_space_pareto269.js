"use strict";
// LSPV-4: ARC-LAMBDA-SPACE-PARETO269. node arc_lambda_space_pareto269.js
// Exact Fractions, exhaustive SAT/UNSAT, original-clause S/U, paid work proxies.
function run(){
 let checks=0;function check(b,s){checks++;if(!b)throw Error(s)}
 const W1="-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14";
 const w=W1.split(";").map(x=>x.split(" ").map(Number));
 const swap=w.map(x=>x.slice());swap[7][0]=-1;swap[19][0]=1;
 const h8=Array.from({length:8},(_,k)=>[1,2,3].map(i=>(k>>(i-1)&1)?i:-i));
 const perm=F=>F.map(c=>c.map(l=>(l>0?1:-1)*(Math.abs(l)===1?-1:1)*[0,2,3,1][Math.abs(l)]));
 const tests=[["W1 strict22 UNSAT",w,false],["W1 sign-swap strict22 SAT",swap,true],
  ["H8 cube UNSAT",h8,false],["H7 cube SAT",h8.slice(0,7),true],
  ["H8 signed-renamed UNSAT",perm(h8),false],["H7 signed-renamed SAT",perm(h8.slice(0,7)),true]];
 const nVars=F=>Math.max(0,...F.flat().map(Math.abs));
 const truth=(l,a)=>a[Math.abs(l)-1]===Number(l>0);
 const sat=(F,a)=>F.every(c=>c.some(l=>truth(l,a)));
 const counts=(F,a)=>F.map(c=>c.reduce((z,l)=>z+Number(truth(l,a)),0));
 const textCNF=(F,n)=>"p cnf "+n+" "+F.length+"\n"+F.map(c=>c.join(" ")+" 0\n").join("");
 function dpll(F,n){
  let nodes=0,tests=0;
  function visit(a){
   nodes++;a=a.slice();
   while(true){
    let all=true,changed=false;
    for(const c of F){
     let good=false,unset=0,last=0;
     for(const l of c){tests++;const v=a[Math.abs(l)-1];if(v<0){unset++;last=l}else if((v===1)===(l>0)){good=true;break}}
     if(good)continue;
     all=false;
     if(!unset)return null;
     if(unset===1){let i=Math.abs(last)-1,v=last>0?1:0;if(a[i]>=0&&a[i]!==v)return null;if(a[i]<0){a[i]=v;changed=true}}
    }
    if(all)return a.map(z=>z<0?0:z);
    if(!changed)break;
   }
   const i=a.indexOf(-1);if(i<0)return null;
   for(const v of [0,1]){const b=a.slice();b[i]=v;const r=visit(b);if(r)return r}
   return null;
  }
  const witness=visit(Array(n).fill(-1));
  return {sat:!!witness,nodes,literal_tests:tests,witness};
 }
 const residual=(F,v)=>F.filter(c=>!c.some(l=>Math.abs(l)===1&&Number(l>0)===v)).map(c=>c.filter(l=>Math.abs(l)!==1));
 const expectedLocal=(clause,mode)=>clause.map(l=>({var:Math.abs(l),value:mode?Number(l>0):Number(l<0)}));
 function pairCompatible(C,D,mode1,mode2){
  const map=new Map();
  for(const t of expectedLocal(C,mode1).concat(expectedLocal(D,mode2))){
   if(map.has(t.var)&&map.get(t.var)!==t.value)return false;
   map.set(t.var,t.value);
  }
  return true;
 }
 function verifyLocal(F){
  const extremes=F.map((C,j)=>({j:j+1,literals:C,
   S:expectedLocal(C,1),invert_S:expectedLocal(C,0),
   U:expectedLocal(C,0),invert_U:expectedLocal(C,1),
   occurrences:C.map((l,k)=>({source_index:j+1,occurrence:k+1,literal:l,
    S_value:Number(l>0),inverted_S:Number(l<0),U_value:Number(l<0),inverted_U:Number(l>0)}))}));
  const pairs=[];
  for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++){
   const C=F[i],D=F[j],shared=C.flatMap(a=>D.filter(b=>Math.abs(a)===Math.abs(b)).map(b=>Math.sign(a)===Math.sign(b)));
   const same=shared.includes(true),opp=shared.includes(false);
   const modes={SS:!opp,SU:!same,US:!same,UU:!opp};
   const variables=[...new Set([...C,...D].map(Math.abs))];
   for(const [key,a,b] of [["SS",1,1],["SU",1,0],["US",0,1],["UU",0,0]]){
    let brute=false;
    for(let z=0;z<(1<<variables.length);z++){
     const vals=new Map(variables.map((v,t)=>[v,(z>>t)&1]));
     const modeTrue=(cl,m)=>cl.every(l=>((vals.get(Math.abs(l))===Number(l>0))===Boolean(m)));
     if(modeTrue(C,a)&&modeTrue(D,b)){brute=true;break}
    }
    check(brute===modes[key],"pair four-mode compatibility");
    check(brute===pairCompatible(C,D,a,b),"pair local assignment collision");
   }
   pairs.push({i:i+1,j:j+1,modes,same_shared:same,opposite_shared:opp});
  }
  let triple_checks=0;
  for(let i=0;i<Math.min(8,F.length);i++)for(let j=i+1;j<Math.min(8,F.length);j++)
  for(let k=j+1;k<Math.min(8,F.length);k++){
   const C=[F[i],F[j],F[k]],variables=[...new Set(C.flat().map(Math.abs))];
   for(let mode=0;mode<8;mode++){
    const mem=new Map();let compatible=true;
    for(let t=0;t<3;t++)for(const z of expectedLocal(C[t],(mode>>t)&1)){
     if(mem.has(z.var)&&mem.get(z.var)!==z.value)compatible=false;
     mem.set(z.var,z.value);
    }
    let brute=false;
    for(let z=0;z<(1<<variables.length);z++){
     const vals=new Map(variables.map((v,t)=>[v,(z>>t)&1]));
     if(C.every((cl,t)=>cl.every(l=>((vals.get(Math.abs(l))===Number(l>0))===Boolean((mode>>t)&1))))){brute=true;break}
    }
    check(brute===compatible,"multi-clause S/U compatibility");triple_checks++;
   }
  }
  return {extremes,pairs,triple_checks};
 }
 function derivedRule(F){
  for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++)
  for(const l of F[i])if(F[j].includes(-l)){
   const r=[...new Set([...F[i].filter(v=>v!==l),...F[j].filter(v=>v!==-l)])];
   if(r.some(v=>r.includes(-v)))continue;
   return {source_clauses:[i+1,j+1],pivot:l,resolvent:r,
    forbidden_cube:r.map(v=>({variable:Math.abs(v),value:Number(v<0)}))};
  }
  return null;
 }
 const instances=[];
 for(const [name,F,expectedSAT] of tests){
  const n=nVars(F),N=8*textCNF(F,n).length,local=verifyLocal(F),zero=Array(n).fill(0),one=Array(n).fill(1);
  let models=0,witness=null;
  for(let z=0;z<(1<<n);z++){
   const a=Array.from({length:n},(_,i)=>(z>>i)&1),b=a.map(x=>1-x);
   const t=counts(F,a),u=counts(F,b);
   for(let j=0;j<F.length;j++)check(t[j]+u[j]===3,"original 3CNF complement counts");
   const accepted=t.every(x=>x>0);check(accepted===sat(F,a),"coherent assignment SAT");
   if(accepted){models++;if(!witness)witness=a}
  }
  check((models>0)===expectedSAT,"expected original label "+name);
  const flips=[];let prev=zero,prevCnt=counts(F,zero);
  for(let i=0;i<Math.min(32,(1<<n));i++){
   const g=i^(i>>1),a=Array.from({length:n},(_,k)=>(g>>k)&1),curr=counts(F,a);
   const changed=[];for(let k=0;k<n;k++)if(a[k]!==prev[k])changed.push(k);
   for(let j=0;j<F.length;j++){
    let delta=0;for(const k of changed)for(const l of F[j])
     if(Math.abs(l)===k+1)delta+=Number(truth(l,a))-Number(truth(l,prev));
    check(prevCnt[j]+delta===curr[j],"exact intermediate flip");
   }
   flips.push({step:i,flipped_variables:changed.map(k=>k+1),
    count_categories:[0,1,2,3].map(v=>curr.filter(x=>x===v).length)});
   prev=a;prevCnt=curr;
  }
  const r=derivedRule(F);
  if(r){for(let z=0;z<(1<<n);z++){
   const a=Array.from({length:n},(_,i)=>(z>>i)&1);
   if(sat(F,a))check(r.resolvent.some(l=>truth(l,a)),"resolution-derived forbidden cube");
  }}
  const baseline=dpll(F,n);
  check(baseline.sat===expectedSAT,"DPLL label correct");
  if(baseline.witness)check(sat(F,baseline.witness),"DPLL witness original");
  const children=[];let childBits=0,childWork=0;
  for(const v of [0,1]){
   const child=residual(F,v),R=dpll(child,n),bits=8*textCNF(child,n).length;
   let brute=false;
   for(let z=0;z<(1<<n);z++){
    const a=Array.from({length:n},(_,i)=>(z>>i)&1);if(a[0]!==v)continue;
    check(sat(F,a)===sat(child,a),"cofactor same-source projected both labels");
    if(sat(child,a))brute=true;
   }
   check(R.sat===brute,"cofactor independent label");
   children.push({x1:v,clauses:child.length,physical_bits:bits,dpll_nodes:R.nodes,
    literal_tests:R.literal_tests,sat:R.sat});
   childBits+=bits;childWork+=R.literal_tests;
  }
  check(children.some(c=>c.sat)===expectedSAT,"OR of cofactors preserves both labels");
  instances.push({name,n,original_clauses:F,models,witness,source_bits:N,
   original_clause_local_extremes:local.extremes,pairs:local.pairs,triple_checks:local.triple_checks,
   all_zero_counts:counts(F,zero),all_one_counts:counts(F,one),
   flips,derived_forbidden_cube:r,baseline,children,
   selected_events_baseline:N+baseline.literal_tests,
   selected_events_controller:N+F.length+2*n+childBits+childWork,
   note:"Selected source/child bit output and literal test events; NOT native FLMV machine transitions."});
 }
 const gcd=(a,b)=>b?gcd(b,a%b):a<0n?-a:a;
 const Q=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b}let g=gcd(a,b);return [a/g,b/g]};
 const add=(x,y)=>Q(x[0]*y[1]+x[1]*y[0],x[1]*y[1]);
 const sub=(x,y)=>Q(x[0]*y[1]-x[1]*y[0],x[1]*y[1]);
 const mul=(x,y)=>Q(x[0]*y[0],x[1]*y[1]);
 const div=(x,y)=>Q(x[0]*y[1],x[1]*y[0]);
 const lt=(x,y)=>x[0]*y[1]<y[0]*x[1];
 const str=x=>x[0]+"/"+x[1];
 const pw=(x,n)=>{let y=Q(1);for(let i=0;i<n;i++)y=mul(y,x);return y};
 function envelope(c){
  let f=Q(1),best=Q(-1),winner=[],steps=[];
  for(let k=1;k<=120;k++){
   f=div(mul(c,f),add(Q(1),f));
   const a=div(sub(div(Q(1),f),c),Q(k)),b=div(Q(1),pw(c,k)),d=lt(a,b)?a:b;
   if(lt(best,d)){best=d;winner=[k]}else if(!lt(d,best)&&!lt(best,d))winner.push(k);
   steps.push({k,value:str(d)});
   if(lt(div(b,c),best))return {c:str(c),d:str(best),maximizers:winner,tail_excluded_from_k:k+1,checked:steps};
  }
  throw Error("full FLMV tail not excluded");
 }
 const envelope_controls=[envelope(Q(6,5)),envelope(Q(241,200)),envelope(Q(301,250)),envelope(Q(603,500)),envelope(Q(6023,5000))];
 check(envelope_controls[0].d==="23/45"&&envelope_controls[0].maximizers.join()==="2","FLMV 6/5");
 check(envelope_controls[1].d==="11642479/23232400"&&envelope_controls[1].maximizers.join()==="2","FLMV 241/200");
 const gates=[
  ["baseline",Q(0),Q(0),Q(0),Q(0),Q(1,2),Q(241,200),true],
  ["child exponent 0.5015 global-c rescue",Q(3,2000),Q(0),Q(0),Q(0),Q(1,2),Q(301,250),true],
  ["child exponent 0.5015 fixed c fails",Q(3,2000),Q(0),Q(0),Q(0),Q(1,2),Q(241,200),false],
  ["child exponent 0.5019 razor thin",Q(19,10000),Q(0),Q(0),Q(0),Q(1,2),Q(6023,5000),true],
  ["child exponent 0.502 fails",Q(1,500),Q(0),Q(0),Q(0),Q(1,2),Q(6023,5000),false],
  ["two individually small selector tariffs",Q(0),Q(0),Q(1,600),Q(1,600),Q(1,2),Q(241,200),false],
  ["full parent read per child",Q(0),Q(0),Q(0),Q(0),Q(1),Q(241,200),false],
  ["FLMV boundary equality in space",Q(0),Q(26279,23232400),Q(0),Q(0),Q(1,2),Q(241,200),false]
 ];
 const exact_gates=[];
 for(const [name,xi,eta,theta,beta,rho,c,expected] of gates){
  const lam=add(Q(1,2),xi),g=add(Q(3,5),theta),kt=div(add(g,beta),sub(Q(1),lam));
  const K=[Q(11,10),add(g,rho),kt].reduce((a,b)=>lt(a,b)?b:a);
  const S=[add(Q(1,2),eta),lam].reduce((a,b)=>lt(a,b)?b:a);
  const e=envelope(c),d=Q(...e.d.split("/").map(BigInt));
  const ok=lt(K,c)&&lt(S,d);
  check(ok===expected,"exact fraction ARC gate "+name);
  exact_gates.push({name,xi:str(xi),eta:str(eta),theta:str(theta),beta:str(beta),rho:str(rho),
   lambda:str(lam),Kstar:str(K),Lstar:str(S),c:str(c),d_FLVM:str(d),strict:ok});
 }
 return {run:"ARC-LAMBDA-SPACE-PARETO269",timestamp:"2026-10-31 03:36 America/Los_Angeles",
  status:"CONDITIONAL recurrence; PROVED/EXACT conditional algebra; COMPUTATIONAL SAT/UNSAT controls; P versus NP OPEN",
  seed:null,verification:"deterministic exact Fractions plus complete assignment enumeration",
  checks,instances,exact_gates,envelope_controls,
  limitations:"The ARC recurrence is hypothetical. No all-input compiler, hereditary child constructor or native FLMV transition/space measurement."};
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
