'use strict';
// TMR-1/053, deterministic exact finite check of the restricted Boolean-gate
// to width<=3 CNF compiler, and numerical diagnostics for the loglog-tax theorem.
// Execute: node experiments/tmr/tmr1_loglog_density053.js
const seed=20261115; let state=seed>>>0;
function rng(){state^=state<<13;state^=state>>>17;state^=state<<5;return state>>>0;}
let assertions=0, assignmentChecks=0, circuits=0, tautologies=0, duplicateRemovals=0;
function check(ok,msg){assertions++;if(!ok)throw Error(msg);}
function mk(n,g){
  let gates=[];
  for(let i=0;i<g;i++){let r=n+i;gates.push({a:rng()%r,b:rng()%r,mask:rng()%16});}
  return {n,gates,out:n+g-1};
}
function cnf(C){
 const V=C.n+C.gates.length,clauses=[];
 function emit(lits){clauses.push(lits);}
 C.gates.forEach((G,j)=>{
   const z=C.n+j;
   for(let u=0;u<2;u++)for(let v=0;v<2;v++){
     const out=(G.mask>>((u<<1)|v))&1;
     emit([[G.a,u===0],[G.b,v===0],[z,out===1]]);
   }
 });
 emit([[C.out,true]]);
 const seen=new Set(clauses.flat().map(x=>x[0]));
 for(let i=0;i<V;i++)if(!seen.has(i)){emit([[i,true],[i,false],[i,true]]);tautologies++;}
 const uniq=[],keys=new Set();
 for(const c of clauses){let k=JSON.stringify(c);if(keys.has(k)){duplicateRemovals++;continue;}keys.add(k);uniq.push(c);}
 return {V,clauses:uniq};
}
function value(C,assignment){
 let w=new Array(C.n+C.gates.length).fill(false);
 for(let i=0;i<C.n;i++)w[i]=!!((assignment>>i)&1);
 C.gates.forEach((G,j)=>{let idx=(Number(w[G.a])<<1)|Number(w[G.b]);w[C.n+j]=!!((G.mask>>idx)&1);});
 return Number(w[C.out]);
}
function sat(form,assign){
 return form.clauses.every(c=>c.some(([id,pos])=>Boolean((assign>>id)&1)===pos));
}
function test(C){
 let F=cnf(C),V=F.V,all=new Set(F.clauses.flat().map(l=>l[0]));
 check(all.size===V,'all-occurs');
 check(F.clauses.every(c=>c.length>=1&&c.length<=3),'width');
 check(new Set(F.clauses.map(JSON.stringify)).size===F.clauses.length,'unique clauses');
 check(F.clauses.length<=5*V,'density m<=5V');
 for(let x=0;x<(1<<C.n);x++){
   let hits=0,expected=value(C,x);
   for(let y=0;y<(1<<C.gates.length);y++){
     let a=x|(y<<C.n);if(sat(F,a))hits++;assignmentChecks++;
   }
   check(hits===expected,'unique-extension positive-output count');
 }
 circuits++;return {n:C.n,g:C.gates.length,V,m:F.clauses.length,count:Array.from({length:1<<C.n},(_,x)=>value(C,x)).reduce((a,b)=>a+b,0)};
}
function run(){
 const special=[];
 for(let mask=0;mask<16;mask++)special.push(test({n:3,gates:[{a:0,b:1,mask}],out:3}));
 // All 16 two-input gate truth tables, including constants, XOR, and don't-care variables.
 const random=[];
 for(let i=0;i<96;i++){const n=2+(rng()%4),g=1+(rng()%5);let c=test(mk(n,g));if(i<8)random.push(c);}
 const Ls=[64,4096,1048576,2**34,2**48];
 const budgets=[];
 for(const beta of [0,1,2])for(const L of Ls){
   const A=1,eta=1/16,B=12,ell=Math.log2(L);
   const vRatio=3*eta*Math.sqrt(L)/(ell**beta)+B;
   const lv=L+Math.log2(vRatio);
   const exponentPerN=A*vRatio*Math.pow(Math.log2(lv),beta)/Math.sqrt(lv);
   const badV=3*eta*Math.sqrt(L)+B;
   const badLV=L+Math.log2(badV);
   const beta0SizeInBetaExponent=A*badV*Math.pow(Math.log2(badLV),beta)/Math.sqrt(badLV);
   check(Number.isFinite(exponentPerN)&&exponentPerN>0,'budget finite');
   budgets.push({beta,log2_n:L,V_over_n:vRatio,solver_exponent_over_n:exponentPerN,uncorrected_beta0_size_exponent_over_n:beta0SizeInBetaExponent});
 }
 check(3*2<16,'3A eta=3/16<1/2, symbolic A=1');
 return {revision:'TMR1_LOGLOG_DENSITY053_v1',seed,model:'arbitrary shared binary truth-table gates, each one functional 3-CNF extension; all variables occur; no repeated clause lists',status:'COMPUTATIONAL finite; theorem CONDITIONAL on specified #SAT runtime',checks:{assertions,assignmentChecks,circuits,tautologies,duplicateRemovals,failures:0},special,sampleRandom:random,asymptoticDiagnostics:budgets,limit_exponent_over_n:'3/16',notes:'Budget rows are numerical diagnostics in log-size L; no 2^L formulas were generated. Actual solver constant A is not claimed to equal 1.'};
}
if(typeof process!=='undefined'&&process.stdout)process.stdout.write(JSON.stringify(run(),null,2)+'\n');
