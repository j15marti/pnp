"use strict";
// Independently authored TMR-5/013 charged multihead finite-state redteam.
// Each tick moves at most one read-only head by one cell. The scanned symbol is
// read only at the current physical input position, never from the adjacent cell.
function assert(z,m){if(!z)throw Error(m);}

function classify(bits){if(bits.length%3)return "MALFORMED";const m=new Set();for(let i=0;i<bits.length;i+=3)m.add(parseInt(bits.slice(i,i+3),2));return m.size===8?"UNSAT":"SAT";}

function begin(d){return {phase:"F",p:0,parity:0,last:0,part:0,mod:0,mask:0,heads:Array(d).fill(0),carry:-1,label:null};}

function tick(s,bits,d,gated){
 const n={...s,heads:s.heads.slice()},q=bits.length+1,L=bits.length;
 switch(s.phase){
 case "F":
   if(s.p>=1&&s.p<=L){const v=+bits[s.p-1];n.parity^=v;n.last=v;n.part=((n.part<<1)|v)&7;n.mod=(n.mod+1)%3;if(n.mod===0)n.mask|=1<<n.part;}
   n.p++;if(n.p===q)n.phase="R";break;
 case "R":
   assert(s.p>0,"return underflow");n.p--;if(n.p===0)n.phase="G";break;
 case "G":
   n.label=n.mod?"MALFORMED":n.mask===255?"UNSAT":"SAT";
   n.phase=gated&&n.parity?"DO":"H";break;
 case "DO":
   assert(s.p<q,"overrun outward");n.p++;if(n.p===q)n.phase="DB";break;
 case "DB":
   assert(s.p>0,"overrun back");n.p--;if(n.p===0){if(d===0)n.phase="H";else {n.phase="INC";n.carry=d-1;}}break;
 case "INC":
   assert(s.carry>=0&&s.carry<d&&s.heads[s.carry]<q,"bad increment");
   n.heads[s.carry]++;if(n.heads[s.carry]<q){n.phase="DO";n.carry=-1;}else n.phase="RESET";break;
 case "RESET":
   assert(s.carry>=0&&s.heads[s.carry]>0,"bad reset");
   n.heads[s.carry]--;if(n.heads[s.carry]===0){if(s.carry===0){n.phase="H";n.carry=-1;}else {n.carry--;n.phase="INC";}}break;
 default:throw Error("HALT has no step");
 }return n;
}

function project(s){return JSON.stringify([s.phase,s.p,s.part,s.mod,s.mask,s.heads,s.carry,s.label]);}

function phi(s,q){return s.phase==="F"?2*q-s.p+1:s.phase==="R"?s.p+1:s.phase==="G"?1:0;}

function audit(bits,d,gated,stats){
 const q=bits.length+1,truth=classify(bits),pTruth=[...bits].reduce((p,c)=>p^(+c),0);let s=begin(d),steps=0,leaves=0,gate=null;
 while(s.phase!=="H"){
   assert(steps<20*q**(d+1)+100*q+10,"failed totality bound");
   if(s.phase==="G")gate=s;
   if(s.phase==="DB"&&s.p===1)leaves++;
   const n=tick(s,bits,d,gated);
   assert(phi(s,q)<=1+phi(n,q),"Bellman every edge");
   const flipped={...s,parity:s.parity^1,last:s.last^1},other=tick(flipped,bits,d,gated);
   if(!gated||s.phase!=="G")assert(project(other)===project(n),"wrong non-gate projection");
   else assert(project(other)!==project(n),"gate expected to differ");
   if(s.phase==="F"&&s.p===0)assert(n.parity===s.parity,"off-head first-bit read");
   s=n;steps++;stats.edges++;
 }
 assert(s.label===truth&&s.parity===pTruth,"terminal label or parity");
 assert(s.heads.every(p=>p===0)&&s.p===0,"nonrestored source heads");
 const baseline=2*q+1,odd=gated&&pTruth;
 if(!odd)assert(steps===baseline&&leaves===0,"cheap path count");
 else{
   const exactExtra=2*q**(d+1)+2*Array.from({length:d},(_,i)=>q**(i+1)).reduce((a,b)=>a+b,0);
   assert(leaves===q**d&&steps===baseline+exactExtra,"wrong charged odometer cost");
   const cheap=tick({...gate,parity:0},bits,d,true);
   assert(cheap.phase==="H"&&cheap.label===truth,"spurious gate replay");
   assert(phi(begin(d),q)===baseline,"Bellman potential start");
   stats.spurious++;stats.savedTotal+=exactExtra;stats.savedLower+=2*q**(d+1);
 }
 stats.cases++;stats[truth.toLowerCase()]++;stats.totalSteps+=steps;
 if(gated&&pTruth)stats.odd++;if(gated&&!pTruth)stats.even++;
}

function run(){
 const stats={engine:"hosted V8 direct independent source",kind:"COMPUTATIONAL",cases:0,sat:0,unsat:0,malformed:0,edges:0,totalSteps:0,spurious:0,savedTotal:0,savedLower:0,odd:0,even:0,failures:0,perD:{}};
 for(let d=0;d<=3;d++){
  const z={cases:0,sat:0,unsat:0,malformed:0,edges:0,totalSteps:0,spurious:0,savedTotal:0,savedLower:0,odd:0,even:0};
  let inputs=[];for(let L=0;L<=(d===3?5:7);L++)for(let v=0;v<2**L;v++)inputs.push(L===0?"":v.toString(2).padStart(L,"0"));
  if(d<=2){inputs.push("001".repeat(7)+"000");inputs.push(Array.from({length:8},(_,i)=>i.toString(2).padStart(3,"0")).join("")+"001");inputs.push("000".repeat(8));}
  for(const bits of inputs){audit(bits,d,false,z);audit(bits,d,true,z);}
  assert(z.spurious>0,"missing spurious control");
  stats.perD[d]={...z,fixtureCount:inputs.length};
  for(const k of Object.keys(z))stats[k]+=z[k];
 }
 return stats;
}

if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
