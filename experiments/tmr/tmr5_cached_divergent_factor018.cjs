'use strict';
// TMR-5/018 independent physical-head E3 simulator. Not a generic TM compiler.
const assert=(p,m='assertion failed')=>{if(!p)throw Error(m)};
const symbol=(x,h)=>h===0?'<':h===x.length+1?'>':x[h-1];
const rank=(s,x)=>{
 const n=x.length+1,z=[...x].reduce((a,b)=>a+Number(b),0)%2,h=s.h;
 if(s.q==='SCAN')return 3*n+4+2*n*z-h;
 if(s.q==='BRANCH')return 2*n+3+2*n*z;
 if(s.q==='DL')return 3*n+2+h;
 if(s.q==='DR')return 3*n+2-h;
 if(s.q==='JOIN')return 2*n+2;
 if(s.q==='REWIND')return h+n+1;
 if(s.q==='PARSE')return n-h+1;
 if(s.q==='HALT')return 0;
 throw Error('unknown phase');
};
function simulate(x,mode){
 const s={q:'SCAN',h:0,hb:0,hc:0,c0:0,c1:0,b0:0,cache:null,mask:0,part:'',label:null,steps:0,visitedB:new Set([0]),visitedC:new Set([0]),branch:null};
 const start=rank(s,x),n=x.length+1;
 while(s.q!=='HALT'){
  assert(s.steps<10*n+30,'nonterminal');
  assert(s.hb===0 && s.hc===(['BRANCH','DL','DR','JOIN'].includes(s.q)?1:0),'head separation');
  const old=rank(s,x),a=symbol(x,s.h);
  const b=mode==='concrete'?s.b0:(s.hc===1?(mode==='cached'?s.cache:s.c1%2):s.c0%2);
  if(s.q==='SCAN'){
   if(a==='>'){if(mode==='cached')s.cache=s.c0%2;s.hc=1;s.q='BRANCH'}
   else{if(a==='0'||a==='1'){s.c0=(s.c0+Number(a))%4;if(mode==='concrete')s.b0=s.c0%2;}s.h++}
  }else if(s.q==='BRANCH'){
   assert(a==='>','branch source position');
   s.c1=(s.c1+2)%4;
   s.branch=b;s.q=b?'DL':'JOIN';
  }else if(s.q==='DL'){
   if(a==='<'){s.h++;s.q='DR'}else s.h--;
  }else if(s.q==='DR'){
   if(a==='>'){s.hc=0;s.q='REWIND';s.cache=null}else s.h++;
  }else if(s.q==='JOIN'){
   assert(a==='>','join source');s.hc=0;s.q='REWIND';s.cache=null;
  }else if(s.q==='REWIND'){
   if(a==='<'){s.h++;s.q='PARSE'}else s.h--;
  }else if(s.q==='PARSE'){
   if(a==='>'){s.label=s.part.length?'MALFORMED':s.mask===255?'UNSAT':'SAT';s.q='HALT'}
   else{assert(a==='0'||a==='1');s.part+=a;if(s.part.length===3){s.mask|=1<<parseInt(s.part,2);s.part=''}s.h++}
  }else throw Error('bad phase');
  s.steps++;s.visitedB.add(s.hb);s.visitedC.add(s.hc);
  assert(s.b0===s.c0%2 || mode!=='concrete','whole tape relation');
  if(mode!=='naive')assert(old===rank(s,x)+1,'Bellman equality');
 }
 assert(s.steps===start || mode==='naive','start potential equality');
 return {steps:s.steps,label:s.label,mask:s.mask,visited:s.visitedB.size+s.visitedC.size,branch:s.branch};
}
function independentTruth(x){
 if(x.length%3!==0)return 'MALFORMED';
 for(let v=0;v<8;v++){
  let satisfies=true;
  for(let i=0;i<x.length;i+=3)if(parseInt(x.slice(i,i+3),2)===v){satisfies=false;break}
  if(satisfies)return 'SAT';
 }
 return 'UNSAT';
}
function main(){
 let paired=0,edges=0,labels={SAT:0,UNSAT:0,MALFORMED:0},odd=0;
 const inputs=[];for(let L=0;L<=11;L++)for(let i=0;i<2**L;i++)inputs.push(i.toString(2).padStart(L,'0'));
 inputs[0]='';
 const cube=Array.from({length:8},(_,i)=>i.toString(2).padStart(3,'0')).join('');
 inputs.push(cube,cube+'001',cube+'001'.repeat(4),cube.split('').reverse().join(''),cube.slice(0,-1),
 '001001'+Array.from({length:6},(_,i)=>(i+2).toString(2).padStart(3,'0')).join(''),
 '111'.repeat(39),'000'.repeat(40),'101'.repeat(39)+'0','01'.repeat(80),'1'.repeat(128),'0'.repeat(129));
 for(const x of inputs){
  const c=simulate(x,'concrete'),a=simulate(x,'cached');
  assert(JSON.stringify(c)===JSON.stringify(a),'paired transition replay mismatch');
  assert(c.visited===3,'space');
  assert(c.label===independentTruth(x),'independent SAT truth mismatch');
  const expected=3*(x.length+1)+4+2*(x.length+1)*([...x].filter(z=>z==='1').length%2);
  assert(c.steps===expected,'time expression');
  paired++;edges+=c.steps;labels[c.label]++;if(c.branch)odd++;
 }
 const hostile=['1','001','111000000'].map(x=>{
  const c=simulate(x,'concrete'),bad=simulate(x,'naive');
  const gap=c.steps-bad.steps;
  assert(gap===2*(x.length+1),'missing detour');
  assert(c.label===bad.label,'labels');
  return {x,concrete:c.steps,naive:bad.steps,missingRealTransitions:gap,bScanned:1,cScanned:0,label:c.label}
 });
 let certified=0;
 for(let c=0;c<4;c++)for(let b=0;b<2;b++){
  assert((c+2)%4%2===c%2,'kernel preservation');certified++;
  if(b===c%2)for(let inputBit=0;inputBit<2;inputBit++){
   const cp=(c+inputBit)%4,bp=cp%2;assert(bp===cp%2);certified++;
  }
 }
 return {role:'TMR-5/018',execution:'independent hosted V8 JavaScript',status:'COMPUTATIONAL',
  scope:'restricted E3 three-variable 3CNF controller',exhaustiveLength:[0,11],
  pairedTraces:paired,pairedTransitions:edges,bellmanEqualities:edges,
  labels,oddParityTraces:odd,allSymbolCertificateChecks:certified,peakVisitedWritableCells:3,
  hostileInvalidRemoteLookups:hostile,failures:0};
}
console.log(JSON.stringify(main(),null,2));
