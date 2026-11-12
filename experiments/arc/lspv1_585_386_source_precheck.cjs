'use strict';
// LSPV-1/585, exact independent graph-rank enumeration; Node >=18.
// Archived checker: experiments/arc/lspv2_386_independent_verify.js
function ok(b,m){if(!b)throw Error(m)}
function inspect(name,n,edges){
 ok(edges.length*2===3*n,'not cubic');
 const deg=Array(n).fill(0),adj=Array.from({length:n},()=>[]),seen=new Set();
 for(const [u,v] of edges){
  ok(Number.isInteger(u)&&Number.isInteger(v)&&u>=0&&v<n&&u<v,'edge order');
  const k=u+':'+v;ok(!seen.has(k),'duplicate edge');seen.add(k);
  deg[u]++;deg[v]++;adj[u].push(v);adj[v].push(u);
 }
 ok(deg.every(x=>x===3),'degree');
 let comp=Array(n).fill(-1),c=0;
 for(let root=0;root<n;root++)if(comp[root]<0){
  comp[root]=c;const q=[root];
  for(let i=0;i<q.length;i++)for(const v of adj[q[i]])if(comp[v]<0){comp[v]=c;q.push(v)}
  c++;
 }
 const m=edges.length;
 let tested=0,passes=0,rejects=0,modelChecks=0,evenFeasible=0,evenInfeasible=0;
 let witness=null;
 for(let mask=0;mask<2**n;mask++){
  let odd=0;for(let v=0;v<n;v++)odd^=(mask>>v)&1;
  if(!odd)continue;
  tested++;
  const evenMask=mask&~1;
  let parity=Array(c).fill(0);
  for(let v=0;v<n;v++)parity[comp[v]]^=(evenMask>>v)&1;
  const predicted=parity.some(Boolean)?0:2**(m-n+c);
  let evenModels=0,oddModels=0;
  for(let a=0;a<2**m;a++){
   const synd=Array(n).fill(0);
   edges.forEach(([u,v],e)=>{if((a>>e)&1){synd[u]^=1;synd[v]^=1}});
   let eok=true,ook=true;
   for(let v=0;v<n;v++){
    if(synd[v]!==((evenMask>>v)&1))eok=false;
    if(synd[v]!==((mask>>v)&1))ook=false;
   }
   evenModels+=Number(eok);oddModels+=Number(ook);
  }
  ok(oddModels===0,'odd source SAT');
  ok(evenModels===predicted,'component-rank count mismatch '+name+':'+mask);
  const pass=evenModels===2**(m-n+1);
  ok(pass===Boolean((mask&1)&&c===1),'native CLI parity control mismatch');
  if(pass)passes++;else rejects++;
  if(predicted>0)evenFeasible++;else evenInfeasible++;
  modelChecks+=2**m;
  if(!witness&&!pass)witness={odd_charge_mask:mask,component_parities_after_setting_b0_zero:parity,actual_even_models:evenModels,checker_expected:2**(m-n+1)};
 }
 return {name,n,m,c,odd_charge_vectors:tested,parity_test_accept:passes,parity_test_reject:rejects,even_rhs_feasible:evenFeasible,even_rhs_infeasible:evenInfeasible,exhaustive_assignments:modelChecks,first_rejection:witness};
}
const k4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const prism=[[0,1],[0,2],[1,2],[3,4],[3,5],[4,5],[0,3],[1,4],[2,5]];
const k33=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)k33.push([i,j]);
const cube=[];for(let i=0;i<8;i++)for(const x of [1,2,4])if(i<(i^x))cube.push([i,i^x]);
const cases=[inspect('K4',4,k4),inspect('prism6',6,prism),inspect('K3,3',6,k33),inspect('cube8',8,cube),inspect('K4+K4',8,[...k4,...k4.map(([a,b])=>[a+4,b+4])])];
const result={theorem:'For cubic graph with m<=12 and globally odd b, archived /386 even-charge self-test accepts exactly when graph is connected and b_0=1.',
component_equation:'rank(B)=n-c; even-charge solution count equals 0 if any component parity odd, else 2^(m-n+c)',
original_checker_blob:'338305c0ce101704205e57543756b8127074a986',
total_odd_sources:cases.reduce((x,y)=>x+y.odd_charge_vectors,0),
total_pass:cases.reduce((x,y)=>x+y.parity_test_accept,0),
total_fail:cases.reduce((x,y)=>x+y.parity_test_reject,0),
assignment_exhaustions:cases.reduce((x,y)=>x+y.exhaustive_assignments,0),cases,
limitations:['Only original /386 parity self-test, not full R_mix341','A passing self-test does not guarantee a checker-accepted proof','For m>12 original checker skips this test','No SAT time lower bound']};
console.log(JSON.stringify(result,null,2));
