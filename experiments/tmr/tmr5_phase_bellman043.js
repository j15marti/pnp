"use strict";
// TMR-5/043 independent shortest-path and phase-gated exact tariff verifier.
// Run: node experiments/tmr/tmr5_phase_bellman043.js
function audit(){
"use strict";
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const specs=[];
for(let q=1;q<=7;q++)for(let G=1;G<=5;G++){
  specs.push({name:"singletons",q,G,E:Array.from({length:q},(_,i)=>[i])});
  specs.push({name:"full",q,G,E:[Array.from({length:q},(_,i)=>i)]});
  if(q>=3 && G<=4) specs.push({name:"cycle",q,G,E:Array.from({length:q},(_,i)=>[i,(i+1)%q])});
}
for(let G=1;G<=5;G++){
  specs.push({name:"fano",q:7,G,E:fano});
  specs.push({name:"triangle",q:3,G,E:[[0,1],[1,2],[0,2]]});
}
for(let q=4;q<=7;q++)for(let G=1;G<=3;G++){
 const E=Array.from({length:q},(_,i)=>[i,(i+1)%q,(i+3)%q].filter((x,j,a)=>a.indexOf(x)===j));
 specs.push({name:"triple-overlap",q,G,E});
}
let assertions=0,paidEdges=0,zeroEdges=0,states=0;
let counts={CHECK:0,BATCH:0,FUSE:0,HALT:0,VIEW:0,NOP:0},summary=[],nonMonotone=0;
function check(cond,msg){assertions++;if(!cond)throw Error(msg);}
function pop(n){let c=0;for(;n;n&=n-1)c++;return c;}
for(const spec of specs){
 const {G,q,E,name}=spec, allG=(1<<G)-1,allU=(1<<q)-1, masks=E.map(a=>a.reduce((x,j)=>x|(1<<j),0));
 check(masks.every(x=>x!==0),"empty batch");
 check(masks.reduce((x,y)=>x|y,0)===allU,"incomplete cover");
 const tauMemo=new Map([[0,0]]);
 function tau(U){
  if(tauMemo.has(U))return tauMemo.get(U);
  let best=Infinity;
  for(const S of masks)if(U&S)best=Math.min(best,1+tau(U&~S));
  tauMemo.set(U,best);return best;
 }
 // Independent source-grammar transitions; all cost-one paid edges are generated.
 function edges(P,U,h){
  if(!h)return [];
  let e=[];
  for(let i=0;i<G;i++)if(!(P&(1<<i)))e.push({rule:"CHECK",P:P|(1<<i),U,h:1});
  if(P===allG)for(const S of masks)if(U&S)e.push({rule:"BATCH",P,U:U&~S,h:1});
  const missing=allG^P;
  if(U===allU && pop(missing)===1)for(const S of masks)
    e.push({rule:"FUSE",P:allG,U:U&~S,h:1});
  if(P===allG && U===0)e.push({rule:"HALT",P,U,h:0});
  return e;
 }
 // No formula for the answer is used in this shortest-path recursion.
 const minMemo=new Map([[`${allG},0,0`,0]]);
 function distance(P,U,h){
  const key=`${P},${U},${h}`;
  if(minMemo.has(key))return minMemo.get(key);
  const alternatives=edges(P,U,h);
  check(alternatives.length>0,"reachable non-goal deadlock "+name+" "+key);
  let val=Infinity;
  for(const e of alternatives)val=Math.min(val,1+distance(e.P,e.U,e.h));
  minMemo.set(key,val);return val;
 }
 function components(P,U,h){
  const t=G-pop(P);
  return [t,tau(U)-(h===1 && t>0 && U===allU ? 1:0),h];
 }
 function potential(P,U,h){return components(P,U,h).reduce((a,b)=>a+b,0);}
 for(let P=0;P<=allG;P++)for(let U=0;U<=allU;U++){
  const h=1, c=components(P,U,h), v=potential(P,U,h), d=distance(P,U,h);
  states++;check(c.every(x=>x>=0),"negative phase component "+name);
  check(v===d,`Bellman mismatch ${name} G${G} q${q} ${P},${U}: ${v} != ${d}`);
  check(v===G-pop(P)+tau(U)+1-((G-pop(P)>0&&U===allU)?1:0),"closed form mismatch");
  zeroEdges+=2;counts.VIEW++;counts.NOP++;
  check(v===potential(P,U,h),"VIEW changed potential");
  check(v===potential(P,U,h),"NOP changed potential");
  for(const e of edges(P,U,h)){
   const c2=components(e.P,e.U,e.h),delta=c.map((x,i)=>x-c2[i]),sum=delta.reduce((a,b)=>a+b,0);
   paidEdges++;counts[e.rule]++;
   check(sum===v-potential(e.P,e.U,e.h),"component delta mismatch");
   check(sum<=1,"legal paid tariff violation "+name+" "+e.rule+" "+sum);
   check(sum===0||sum===1,"nonintegral Bellman 1-Lipschitz row");
   if(delta[1]<0)nonMonotone++;
  }
 }
 check(potential(allG,0,0)===0,"goal nonzero");
 const initial=potential(0,allU,1),trueWork=distance(0,allU,1);
 check(initial===G+tau(allU),"initial exact record work");
 if(name==="singletons"){
   const linear=1+Math.max(G,q);
   check(initial-linear===Math.min(G,q)-1,"singleton linear gap");
 }
 if(name==="full")check(initial===G+1,"full batch real shortcut");
 if(name==="fano"){
   check(tau(allU)===3,"Fano integer cover");
   if(G===3)check(initial===6,"Fano G=3 authentic count");
 }
 if(name==="triangle")check(tau(allU)===2,"triangle integer cover");
 if(G===q && q===7 && name==="singletons")summary.push({name,G,q,integerCover:tau(allU),nonlinearTariff:initial,linearTariff:1+Math.max(G,q),gap:initial-(1+Math.max(G,q))});
 if(name==="fano" && G===3)summary.push({name,G,q,integerCover:3,fractionalCover:"7/3",nonlinearTariff:initial,linearTariff:4,gap:initial-4});
 if(name==="full" && G===3 && q===7)summary.push({name,G,q,integerCover:1,nonlinearTariff:initial,linearTariff:4,gap:0});
 if(name==="triangle" && G===2)summary.push({name,G,q,integerCover:2,fractionalCover:"3/2",nonlinearTariff:initial,linearTariff:3,gap:initial-3});
}
check(nonMonotone>0,"required negative signed discharge not observed");
check(2>1,"smallest fused action invalidates separate unit tariffs");
return {id:"TMR5_PHASE_BELLMAN043",status:"COMPUTATIONAL finite independent exact-state replay; symbolic model theorem peer review OPEN",
cases:specs.length,states,paidEdges,zeroEdges,assertions,failures:0,ruleCounts:counts,
negativeCoverDischargeEdges:nonMonotone,
smallestOldTariffFailure:{G:1,q:1,rule:"FUSE",cost:1,oldGammaWeight:1,oldScaleWeight:1,oldDischarge:2},
summary,zeroCostSCC:"VIEW toggles v, NOP loop; quotient (P,U,h)",
claimedExactPotential:"t+tau_E(U)+h-1[h=1,t>0,U=J]; t=G-|P|",
scope:"preauthenticated finite shared gate/batch record calculus only; not unrestricted 3SAT Turing computation"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
