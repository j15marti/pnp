"use strict";
// TMR-4/016 exact finite-control simulator; 3-bit sign clauses x0,x1,x2.
function check(z,msg){if(!z)throw Error(msg);}
function labelBrute(x){
 if(x.length%3)return "MALFORMED";
 let cl=[];for(let i=0;i<x.length;i+=3)cl.push(parseInt(x.slice(i,i+3),2));
 for(let a=0;a<8;a++)if(cl.every(v=>v!==a))return "SAT";
 return "UNSAT";
}
function initial(){return {phase:"F",p:0,par:0,last:0,part:0,mod:0,mask:0,label:null};}
function step(s,x,gated){
 let n={...s},L=x.length;
 if(s.phase==="F"){
   if(s.p<L){
     let v=x.charCodeAt(s.p)-48;n.par^=v;n.last=v;
     n.part=((n.part<<1)|v)&7;n.mod=(n.mod+1)%3;
     if(n.mod===0)n.mask|=(1<<n.part);
   }
   n.p++;if(n.p===L+1)n.phase="R";
 }else if(s.phase==="R"){
   check(s.p>0,"bad return");n.p--;
   if(n.p===0)n.phase=(gated&&n.par===1)?"DO":"O";
 }else if(s.phase==="DO"){
   n.p++;if(n.p===L+1)n.phase="DB";
 }else if(s.phase==="DB"){
   check(n.p>0,"bad detour");n.p--;
   if(n.p===0)n.phase="O";
 }else if(s.phase==="O"){
   n.label=n.mod!==0?"MALFORMED":n.mask===255?"UNSAT":"SAT";
   n.phase="H";
 }else throw Error("step on HALT");
 return n;
}
function project(s){return JSON.stringify([s.phase,s.p,s.part,s.mod,s.mask,s.label]);}
function phi(s,L){
 if(s.phase==="F")return (L+1-s.p)+(L+1)+1;
 if(s.phase==="R")return s.p+1;
 if(s.phase==="DO")return (L+1-s.p)+(L+1)+1;
 if(s.phase==="DB")return s.p+1;
 if(s.phase==="O")return 1;
 if(s.phase==="H")return 0;
 throw Error("unknown phase");
}
function trace(x,gate){
 let states=[initial()];while(states.at(-1).phase!=="H"){
   check(states.length<10*(x.length+3),"nontermination");
   states.push(step(states.at(-1),x,gate));
 }
 return states;
}
function run(){
 let st={cases:0,even:0,odd:0,sat:0,unsat:0,malformed:0,
   concreteEdges:0,inertBisimEdges:0,gateBisimEdges:0,
   gatedBranchFailures:0,maySpurious:0,refinedParityChecks:0,
   bellmanEdges:0,allCosts:0,assertionFailures:0};
 let fixtures=[];
 for(let L=0;L<=11;L++)for(let a=0;a<2**L;a++)fixtures.push(L===0?"":a.toString(2).padStart(L,"0"));
 let rng=123456789;for(let j=0;j<256;j++){
   rng=(Math.imul(rng,1664525)+1013904223)>>>0;
   fixtures.push((rng&16777215).toString(2).padStart(24,"0"));
 }
 fixtures.push(Array.from({length:8},(_,i)=>i.toString(2).padStart(3,"0")).join(""));
 fixtures.push("111".repeat(8));
 fixtures.push("000".repeat(8));
 for(const x of fixtures){
   let L=x.length, par=[...x].reduce((p,b)=>p^(b==="1"),0)?1:0;
   let a=trace(x,false),b=trace(x,true),truth=labelBrute(x);
   check(a.at(-1).label===truth && b.at(-1).label===truth,"terminal label");
   check(a.length-1===2*(L+1)+1,"inert cost");
   check(b.length-1===2*(L+1)*(1+par)+1,"gated cost");
   check(a.every(s=>s.phase!=="DO"&&s.phase!=="DB"),"inert detour");
   check(a[0].phase==="F" && b[0].phase==="F","initial binding");
   st.cases++;st[par?"odd":"even"]++;st[truth.toLowerCase()]++;
   st.allCosts+=(a.length+b.length-2);
   for(const [g,t] of [[false,a],[true,b]]){
     for(let i=0;i<t.length-1;i++){
       let s=t[i],u=t[i+1],n=step(s,x,g);
       check(JSON.stringify(n)===JSON.stringify(u),"concrete transition");
       check(phi(s,L)<=1+phi(u,L),"Bellman all edge");
       st.concreteEdges++;st.bellmanEdges++;
       let flipped={...s,par:s.par^1,last:s.last^1};
       let alt=step(flipped,x,g);
       if(!g){
         check(project(alt)===project(u),"inert quotient is not bisimulation");
         st.inertBisimEdges++;
       }else if(s.phase==="R"&&s.p===1){
         check(project(alt)!==project(u),"gate must distinguish parity");
         st.gatedBranchFailures++;
       }else{
         check(project(alt)===project(u),"wrong gated quotient divergence");
         st.gateBisimEdges++;
       }
     }
   }
   if(par){
     let pivot=b.findIndex(s=>s.phase==="R"&&s.p===1);
     check(pivot>=0 && b[pivot+1].phase==="DO","odd pivot");
     let fake=step({...b[pivot],par:0},x,true);
     check(fake.phase==="O"&&project(fake)!==project(b[pivot+1]),"not genuinely spurious");
     check(phi(b[0],L)===2*(L+1)+1,"candidate short path");
     check(b.length-1-phi(b[0],L)===2*(L+1),"missing charge");
     st.maySpurious++;
     check(2+2*(L+1) === b.length-1-pivot,"refined suffix");
     st.refinedParityChecks++;
   }
 }
 return st;
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
