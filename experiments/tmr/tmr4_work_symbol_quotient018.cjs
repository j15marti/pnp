"use strict";
// TMR-4/018: exhaustive work-symbol cost-congruence and source-bound MAY audit.
const audit=function audit(){
 const assert=(c,m)=>{if(!c)throw Error(m||"failed assertion")};
 const syms=["L","0","1","R"], parts=["","0","1","00","01","10","11"], end=["H_SAT","H_UNSAT","H_MALFORMED"];
 const states=["S","R","D","E",...Array.from({length:256},(_,m)=>parts.map(p=>"A|"+m+"|"+p)).flat(),...end];
 const isEnd=q=>q.startsWith("H_");
 const mk=(next,move,write)=>({next,move,write,cost:1,workMove:0});
 function delta(q,r,s,gated){
  if(isEnd(q))return null;
  if(q==="S")return mk(r==="R"?"R":"S",r==="R"?-1:1,r==="1"?(s^1):s);
  if(q==="R")return mk(r==="L"?(gated&&s===1?"D":"A|0|"):"R",r==="L"?1:-1,s);
  if(q==="D")return mk(r==="R"?"E":"D",r==="R"?-1:1,s);
  if(q==="E")return mk(r==="L"?"A|0|":"E",r==="L"?1:-1,s);
  assert(q.startsWith("A|"),"unknown control");
  const sep=q.indexOf("|",2),mask=Number(q.slice(2,sep)),part=q.slice(sep+1);
  if(r==="L")return mk(q,1,s);
  if(r==="R")return mk(part.length?"H_MALFORMED":(mask===255?"H_UNSAT":"H_SAT"),0,s);
  if(part.length<2)return mk("A|"+mask+"|"+part+r,1,s);
  return mk("A|"+(mask|(1<<parseInt(part+r,2)))+"|",1,s);
 }
 function projection(t){return t?JSON.stringify([t.next,t.move,t.cost,t.workMove,"*"]):"HALT"}
 let inertChecks=0,gatedChecks=0,gatedFailures=[];
 for(const q of states)for(const r of syms){
  const u=delta(q,r,0,false),v=delta(q,r,1,false);
  assert(projection(u)===projection(v),"inert symbol congruence fails "+q+" "+r);
  inertChecks++;
  const a=delta(q,r,0,true),b=delta(q,r,1,true);
  gatedChecks++;
  if(projection(a)!==projection(b))gatedFailures.push({q,r,zero:a?.next,one:b?.next});
 }
 assert(gatedFailures.length===1&&gatedFailures[0].q==="R"&&gatedFailures[0].r==="L","unexpected gated failures");
 const sourceSymbol=(x,p)=>p===0?"L":p===x.length+1?"R":x[p-1];
 const parity=x=>[...x].reduce((s,c)=>s^(c==="1"?1:0),0);
 const expected=x=>x.length%3?"H_MALFORMED":(new Set(x.match(/.{3}/g)||[]).size===8?"H_UNSAT":"H_SAT");
 function phi(q,p,n){
  if(isEnd(q))return 0;
  if(q==="S"||q==="D")return 3*n-p+1;
  if(q==="R"||q==="E")return p+n+1;
  if(q.startsWith("A|"))return n-p+1;
  throw Error("bad phase");
 }
 function run(x,gated){
  let q="S",p=0,s=0,t=0,gate=-1,bellman=0;
  const n=x.length+1;
  while(!isEnd(q)){
   assert(t<=10*n+20,"nontermination");
   const r=sourceSymbol(x,p);
   if(q==="R"&&p===0)gate=s;
   const a=delta(q,r,s,gated),np=p+a.move;
   assert(np>=0&&np<=n,"illegal source move "+q+":"+p+"->"+np);
   assert(phi(q,p,n)<=a.cost+phi(a.next,np,n),"bad concrete bellman");
   q=a.next;p=np;s=a.write;t+=a.cost;bellman++;
  }
  assert(q===expected(x),"wrong SAT/UNSAT/MALFORMED label");
  assert(gate===parity(x),"incorrect source parity at gate");
  assert(t===3*n+1+(gated?2*n*parity(x):0),"wrong physical time");
  return {t,gate,bellman,label:q,space:1};
 }
 function abstractAudit(x,gated){
  const n=x.length+1,queue=[{q:"S",p:0,d:0}],seen=new Set(["S#0"]);
  let shortest=Infinity,edges=0,bellman=0,spurious=false;
  for(let i=0;i<queue.length;i++){
   const a=queue[i];
   if(isEnd(a.q)){shortest=Math.min(shortest,a.d);continue}
   const r=sourceSymbol(x,a.p);
   for(const s of [0,1]){
    const z=delta(a.q,r,s,gated),p=a.p+z.move;
    assert(p>=0&&p<=n,"illegal abstract move");
    assert(phi(a.q,a.p,n)<=z.cost+phi(z.next,p,n),"bad abstract Bellman edge");
    edges++;bellman++;
    if(gated&&a.q==="R"&&a.p===0&&parity(x)===1&&s===0&&z.next==="A|0|")spurious=true;
    const key=z.next+"#"+p;
    if(!seen.has(key)){seen.add(key);queue.push({q:z.next,p,d:a.d+z.cost})}
   }
  }
  assert(shortest===3*n+1,"abstract shortest incorrect");
  if(gated&&parity(x)===1)assert(spurious,"missing replay-spurious odd gate");
  return {shortest,edges,bellman,states:seen.size,spurious};
 }
 const inputs=[];
 for(let L=0;L<=10;L++)for(let k=0;k<(1<<L);k++)inputs.push(L===0?"":k.toString(2).padStart(L,"0"));
 const eight=Array.from({length:8},(_,i)=>i.toString(2).padStart(3,"0")).join("");
 inputs.push(eight,eight+"001",eight+"000",eight+"1","000".repeat(30),"111".repeat(30),"010".repeat(32)+"1","101".repeat(32),"001".repeat(16));
 let sat=0,unsat=0,malformed=0,odd=0,traceTransitions=0,abstractEdges=0,inertExact=0,gatedShortcuts=0,spurious=0,visited=0;
 for(const x of inputs){
  const a=run(x,false),b=run(x,true),ca=abstractAudit(x,false),cb=abstractAudit(x,true);
  const n=x.length+1,p=parity(x);
  assert(a.t===ca.shortest,"inert exact quotient mismatch");
  assert(b.t-cb.shortest===2*n*p,"gated false shortcut mismatch");
  assert(a.label===b.label,"labels disagree");
  sat+=a.label==="H_SAT";unsat+=a.label==="H_UNSAT";malformed+=a.label==="H_MALFORMED";
  odd+=p;traceTransitions+=a.t+b.t;abstractEdges+=ca.edges+cb.edges;
  inertExact++;gatedShortcuts+=b.t-cb.shortest;spurious+=Number(cb.spurious);visited+=ca.states+cb.states;
 }
 assert(spurious===odd,"odd source spurious count mismatch");
 return {claim:"work-symbol quotient strong cost congruence and parity gate falsifier",model:"one input head; one visited writable scratch cell; fixed 3-variable sign-stream CNF controller",machineStates:states.length,inertUniversalLocalTransitionPairs:inertChecks,gatedUniversalLocalTransitionPairs:gatedChecks,gatedCertificateFailures:gatedFailures,fixtures:inputs.length,sat,unsat,malformed,oddParity:odd,concreteChargedTransitions:traceTransitions,abstractGraphEdgesAndBellmanChecks:abstractEdges,reachableAbstractStates:visited,costExactInertFixtures:inertExact,replaySpuriousGatedFixtures:spurious,omittedTrueTransitions:gatedShortcuts,failedAssertions:0,status:"COMPUTATIONAL finite test; mathematical claim CANDIDATE/RESTRICTED; P vs NP OPEN"};
};
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
module.exports={audit};
