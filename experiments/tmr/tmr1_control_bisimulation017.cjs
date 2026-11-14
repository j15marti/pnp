"use strict";
// TMR-1/017 cost-exact finite-control partition audit, Node-compatible.
const audit = function audit(){
"use strict";
const insist=(a,b)=>{if(!a)throw Error(b||"assert")}, syms=["L","0","1","R"], terminals=["H_SAT","H_UNSAT"];
const act=(next,im)=>({next,im,wm:0,write:"_",cost:1});
function make(gated){
 const states=["S0","S1","R0","R1",...(gated?["DF","DB"]:[]),"A0","A1","A2","A3",...terminals],delta={};
 for(const s of states)if(!terminals.includes(s)){
  delta[s]={};for(const a of syms){
   let nx,im=0;
   if(s[0]==="S"){const p=Number(s[1]);if(a==="R"){nx="R"+p;im=-1}else{nx="S"+(p^(a==="1"?1:0));im=1}}
   else if(s[0]==="R"){const p=Number(s[1]);if(a==="L"){if(p===1&&gated){nx="DF";im=1}else{nx="A0";im=0}}else{nx=s;im=-1}}
   else if(s==="DF"){if(a==="R"){nx="DB";im=-1}else{nx="DF";im=1}}
   else if(s==="DB"){if(a==="L"){nx="A0";im=0}else{nx="DB";im=-1}}
   else if(s[0]==="A"){const mask=Number(s[1]);if(a==="R"){nx=mask===3?"H_UNSAT":"H_SAT"}else{nx="A"+(mask|(a==="0"?1:a==="1"?2:0));im=1}}
   else throw Error("undefined control");
   delta[s][a]=act(nx,im);
  }
 }
 return {states,delta};
}
function refine(m){
 const states=m.states,halt=s=>terminals.includes(s);
 let cls=Object.fromEntries(states.map(s=>[s,halt(s)?"T"+s:"RUN"])),iterations=0;
 for(;;){
  const signature=states.map(s=>halt(s)?"HALT:"+s:JSON.stringify(syms.map(a=>{let v=m.delta[s][a];return [v.im,v.wm,v.write,v.cost,cls[v.next]]})));
  const symbols=new Map(),next={};
  states.forEach((s,i)=>{if(!symbols.has(signature[i]))symbols.set(signature[i],symbols.size);next[s]=symbols.get(signature[i])});
  iterations++;
  const before=states.map(s=>states.map(r=>cls[s]===cls[r]).join("")).join("|");
  const after=states.map(s=>states.map(r=>next[s]===next[r]).join("")).join("|");
  for(const s of states)for(const r of states)if(cls[s]!==cls[r])insist(next[s]!==next[r],"merged split classes");
  if(before===after)return {cls:next,iterations,blocks:symbols.size};
  cls=next;insist(iterations<=states.length+1,"refinement not convergent");
 }
}
function check(m,p){
 const blocks={};for(const s of m.states)(blocks[p.cls[s]]??=[]).push(s);
 let comparisons=0;
 for(const ss of Object.values(blocks))for(const q of ss)for(const r of ss){
  insist(terminals.includes(q)===terminals.includes(r),"terminal mismatch");
  if(terminals.includes(q)){insist(q===r,"different terminal labels");continue}
  for(const a of syms){
   const v=m.delta[q][a],w=m.delta[r][a];
   insist(v.im===w.im&&v.wm===w.wm&&v.write===w.write&&v.cost===w.cost,"action mismatch");
   insist(p.cls[v.next]===p.cls[w.next],"successor mismatch");comparisons++;
  }
 }
 return {comparisons,classes:Object.values(blocks)};
}
function execute(m,p,x){
 let q="S0",physical=0,n=0,pq=p.cls[q],abstractPos=0,qn=x.length+1;
 const repr={};for(const s of m.states)if(repr[p.cls[s]]===undefined)repr[p.cls[s]]=s;
 while(!terminals.includes(q)){
  insist(n<12*(x.length+2)+10,"nontermination");
  const a=physical===0?"L":physical===qn?"R":x[physical-1];
  const v=m.delta[q][a],w=m.delta[repr[pq]][a];
  insist(v.im===w.im&&p.cls[v.next]===p.cls[w.next],"failed replay");
  physical+=v.im;abstractPos+=w.im;n++;
  insist(physical===abstractPos&&physical>=0&&physical<=qn,"illegal head position");
  q=v.next;pq=p.cls[w.next];
 }
 const desired=x.includes("0")&&x.includes("1")?"H_UNSAT":"H_SAT";
 insist(q===desired&&p.cls[q]===pq,"incorrect 3CNF one-variable classification");
 return n;
}
const a=make(false),b=make(true),pa=refine(a),pb=refine(b),ca=check(a,pa),cb=check(b,pb);
insist(pa.cls.S0===pa.cls.S1&&pa.cls.R0===pa.cls.R1,"inert parity not erased");
insist(pb.cls.R0!==pb.cls.R1,"cost-relevant parity erased");
let cases=0,sat=0,unsat=0,odd=0,ta=0,tb=0,missing=0;
for(let L=0;L<=10;L++)for(let k=0;k<2**L;k++){
 const x=L?k.toString(2).padStart(L,"0"):"";
 const u=execute(a,pa,x),v=execute(b,pb,x);
 const parity=[...x].reduce((p,c)=>p^(c==="1"?1:0),0);
 insist(u===3*(L+1)+2,"base time");
 insist(v-u===2*(L+1)*parity,"detour time");
 cases++;ta+=u;tb+=v;
 if(parity){odd++;missing+=v-u}
 if(x.includes("0")&&x.includes("1"))unsat++;else sat++;
}
const extras=[];
for(const x of ["000001010011100101110111","000001010011100101110110","0".repeat(300),"1".repeat(300),"01".repeat(150)]){
 const u=execute(a,pa,x),v=execute(b,pb,x);
 extras.push({length:x.length,inertTransitions:u,gatedTransitions:v,parity:[...x].reduce((p,c)=>p^(c==="1"?1:0),0)});
}
return {claim:"coarsest source-symbol-universal cost-exact finite-control strong quotient",status:"COMPUTATIONAL",states:{inert:a.states.length,gated:b.states.length},blocks:{inert:pa.blocks,gated:pb.blocks},refinementRounds:{inert:pa.iterations,gated:pb.iterations},certifiedLocalActionPairs:ca.comparisons+cb.comparisons,inertParityMerged:true,gatedParitySeparated:true,exhaustiveBinaryInputs:cases,sat,unsat,oddParitySources:odd,chargedInertTransitions:ta,chargedGatedTransitions:tb,omittedGateMovements:missing,longControls:extras,assertionFailures:0};
};
console.log(JSON.stringify(audit(), null, 2));
