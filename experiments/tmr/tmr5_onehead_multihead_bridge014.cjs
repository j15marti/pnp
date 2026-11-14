"use strict";
// Executed in the hosted V8 isolate; source emitted directly from this function.
const audit = function audit(){
"use strict";
const insist=(q,m)=>{if(!q)throw Error(m||"assertion")};
const tape=w=>({bits:Array(w).fill(0),at:0,seen:new Set([0])});
const shift=(t,d)=>{t.at+=d;insist(t.at>=0&&t.at<=t.bits.length);t.seen.add(t.at);return 1};
const go0=t=>{let c=0;while(t.at)c+=shift(t,-1);return c};
const value=t=>t.bits.reduce((acc,v,i)=>acc+v*2**i,0); // audit only
const change=(t,sgn)=>{
 let c=0;insist(t.at===0);
 for(let i=0;i<t.bits.length;i++){
  let old=t.bits[t.at];c+=1; // charged current-cell read
  t.bits[t.at]=old?0:1;c+=1; // charged current-cell write
  if((sgn===1&&!old)||(sgn===-1&&old))break;
  insist(i+1<t.bits.length,"overflow");c+=shift(t,1);
 }
 c+=go0(t);return c;
};
const equal=(a,b,w)=>{
 insist(a.at===0&&b.at===0);let c=0,eq=true;
 for(let i=0;i<w;i++){
  if(a.bits[a.at]!==b.bits[b.at])eq=false;
  c++; // simultaneous work-tape read
  if(i+1<w){shift(a,1);shift(b,1);c++}
 }
 for(let i=1;i<w;i++){shift(a,-1);shift(b,-1);c++}
 return [eq,c]
};
const oracle=x=>{
 if(x.length%3!==0)return "MALFORMED";
 let seen=0;for(let j=0;j<x.length;j+=3)seen|=1<<parseInt(x.slice(j,j+3),2);
 return seen===255?"UNSAT":"SAT"
};
const motions=(h,q)=>{
 let out=[];const rec=k=>{
  if(k===0){for(let t=0;t<q;t++)out.push([0,1]);for(let t=0;t<q;t++)out.push([0,-1]);}
  else{for(let t=0;t<q;t++){rec(k-1);out.push([k,1])}for(let t=0;t<q;t++)out.push([k,-1])}
 };rec(h-1);return out;
};
const run=(x,h)=>{
 const L=x.length,q=L+1,w=Math.max(1,Math.floor(Math.log2(L+2))+1);
 const v=Array.from({length:h},()=>tape(w)),cur=tape(w);
 let source=0,cost=0,reads=0,lookup=0,positions=Array(h).fill(0);
 const symbol=p=>p===0?"L":(p===q?"R":x[p-1]);
 const query=k=>{
  insist(source===0&&value(cur)===0);lookup++;
  for(;;){
   const [same,c]=equal(cur,v[k],w);cost+=c;
   if(same)break;
   insist(source<q);cost+=change(cur,1);source++;cost++;
  }
  insist(source===value(v[k]));
  const out=symbol(source);cost++;reads++; // physical current-cell read
  while(source>0){cost+=change(cur,-1);source--;cost++}
  insist(value(cur)===0&&cur.at===0);return out;
 };
 const plan=motions(h,q);
 insist(plan.length===2*Array.from({length:h},(_,j)=>q**(j+1)).reduce((a,b)=>a+b,0));
 let first=true,partial="",mask=0,result=null,maximum=0;
 for(const [k,d] of plan){
  const prior=cost;
  for(let j=0;j<h;j++){
   const s=query(j);insist(s===symbol(positions[j]),"wrong source symbol")
   if(first&&j===0&&k===0&&d===1&&positions[0]>=1&&positions[0]<=L){
    partial+=s;if(partial.length===3){mask|=1<<parseInt(partial,2);partial=""}
   }
  }
  cost++; // paid logical control/work-tape transition
  cost+=change(v[k],d);positions[k]+=d;
  insist(positions[k]>=0&&positions[k]<=q&&value(v[k])===positions[k],"head update");
  if(first&&k===0&&d===1&&positions[0]===q){
   result=partial?"MALFORMED":(mask===255?"UNSAT":"SAT");
   first=false
  }
  maximum=Math.max(maximum,cost-prior);
 }
 cost++;
 insist(positions.every(p=>p===0)&&v.every(t=>value(t)===0)&&value(cur)===0);
 insist(result===oracle(x),"wrong SAT label");
 insist(reads===h*plan.length);
 const footprint=v.concat([cur]).reduce((a,t)=>a+t.seen.size,0);
 insist(footprint<=(h+1)*(w+1),"space");
 insist(cost<=40*h*(q+1)*(w+1)*(plan.length+1),"time");
 return {cost,steps:plan.length+1,reads,lookup,footprint,label:result,maxstep:maximum};
};
let cases=0,charged=0,steps=0,reads=0,lookups=0,peakspace=0,peakratio=0;
let labels={SAT:0,UNSAT:0,MALFORMED:0},byhead=[];
for(const [h,maxL] of [[1,7],[2,5],[3,3]]){
 let n=0,t=0;
 for(let L=0;L<=maxL;L++){
  for(let v=0;v<2**L;v++){
   const x=L?v.toString(2).padStart(L,"0"):"";
   const a=run(x,h);n++;t+=a.cost;cases++;charged+=a.cost;steps+=a.steps;
   reads+=a.reads;lookups+=a.lookup;peakspace=Math.max(peakspace,a.footprint);
   peakratio=Math.max(peakratio,a.cost/a.steps);labels[a.label]++;
  }
 }byhead.push({h,cases:n,microsteps:t});
}
for(const [x,wanted] of [
 ["000001010011100101110111","UNSAT"],
 ["000001010011100101110110","SAT"],
 ["0000010100111001011101111","MALFORMED"],
 ["000".repeat(7),"SAT"]
]){
 for(const h of [1,2]){
  const a=run(x,h);insist(a.label===wanted);cases++;charged+=a.cost;steps+=a.steps;
  reads+=a.reads;lookups+=a.lookup;peakspace=Math.max(peakspace,a.footprint);
  peakratio=Math.max(peakratio,a.cost/a.steps);labels[a.label]++;
 }
}
return {claim:"TMR5-HB14 one original input head simulates h-head positional clocks with paid binary registers",status:"COMPUTATIONAL",cases,chargedMicrosteps:charged,simulatedTransitions:steps,currentCellReads:reads,paidSourceLookups:lookups,labels,maxAuxVisitedCells:peakspace,maxCostRatio:peakratio,byhead,errors:0,scope:"fixed-three-variable 3CNF sign-stream clock h=1..3; controls h=1,2"};
};
console.log(JSON.stringify(audit(),null,2));
