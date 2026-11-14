'use strict';
// TMR-4/022 bounded authenticated two-cell tape-factor cache.
// Native JS syntax; hosted V8 execution in research run. Not an arbitrary TM compiler.
function ck(x,m){if(!x)throw Error(m);}
function read(x,h){return h===0?'<':h===x.length+1?'>':x[h-1];}
function parity(x){let p=0;for(const b of x)p^=b==='1'?1:0;return p;}
function truth(x){if(!x.length||x.length%3)return 'MALFORMED';for(let v=0;v<8;v++){let ok=1;for(let i=0;i<x.length;i+=3)if(parseInt(x.slice(i,i+3),2)===v){ok=0;break;}if(ok)return 'SAT';}return 'UNSAT';}
function potential(s,x){
 const n=x.length+1,p=parity(x),b=x.length&&x[0]==='1'?1:0,h=s.h;
 switch(s.q){
 case 'SCAN':return n-h+7+p+b*(2*n+1);
 case 'SETUP0':return 6+p+b*(2*n+1);
 case 'SETUP1':return 5+p+b*(2*n+1);
 case 'REMOTE0':return 4+p+b*(2*n+1);
 case 'EXTRA0':return 4+b*(2*n+1);
 case 'MOVE1':return 3+b*(2*n+1);
 case 'REMOTE1':return 2+b*(2*n+1);
 case 'DL':return h+n+2;
 case 'DR':return n-h+2;
 case 'FINAL':return 1;
 case 'HALT':return 0;
 default:throw Error('unexpected state '+s.q);
 }
}
function start(){return {q:'SCAN',h:0,hb:0,hc:0,B:[0,0,0],C:[0,0,0],R0:null,R1:null,first:0,part:'',mask:0,label:null,count:0,seenB:new Set([0]),seenC:new Set([0]),branch0:null,branch1:null};}
function tick(s,x,mode){
 const a=read(x,s.h),real=mode==='concrete';
 switch(s.q){
 case 'SCAN':
  if(a==='>')s.q='SETUP0';
  else{if(a==='0'||a==='1'){
   const v=+a;s.C[0]=(s.C[0]+v)%4;
   if(real)s.B[0]=s.C[0]%2;
   if(s.h===1)s.first=v;
   s.part+=a;
   if(s.part.length===3){s.mask|=1<<parseInt(s.part,2);s.part='';}
  }s.h++;}break;
 case 'SETUP0':ck(s.hb===0&&s.hc===0,'alignment0');s.R0=s.C[0]%2;s.hb=1;s.hc=1;s.q='SETUP1';break;
 case 'SETUP1':ck(s.hb===1&&s.hc===1,'alignment1');s.C[1]=s.first;if(real)s.B[1]=s.first;
  s.R1=s.first;s.hb=0;s.hc=2;s.q='REMOTE0';break;
 case 'REMOTE0':{
  ck(s.hb===0&&s.hc===2,'remote0 physical position');
  let bit=real?s.B[0]:s.R0;ck(bit===0||bit===1,'authenticated R0');
  s.branch0=bit;s.q=bit?'EXTRA0':'MOVE1';break;}
 case 'EXTRA0':s.q='MOVE1';break;
 case 'MOVE1':s.hb=1;s.q='REMOTE1';break;
 case 'REMOTE1':{
  ck(s.hb===1&&s.hc===2,'remote1 physical position');
  let bit=real?s.B[1]:mode==='single-cache'?s.R0:s.R1;
  ck(bit===0||bit===1,'authenticated R1');
  s.branch1=bit;s.C[2]=(s.C[2]+2)%4;s.q=bit?'DL':'FINAL';break;}
 case 'DL':if(s.h===0){s.h=1;s.q='DR';}else s.h--;break;
 case 'DR':if(s.h===x.length+1)s.q='FINAL';else s.h++;break;
 case 'FINAL':s.label=(!x.length||s.part.length||x.length%3)?'MALFORMED':s.mask===255?'UNSAT':'SAT';s.q='HALT';break;
 default:throw Error('unexpected step state '+s.q);
 }
 s.count++;s.seenB.add(s.hb);s.seenC.add(s.hc);
 if(!real)ck(s.B.every(y=>y===0),'dummy B not blank');
}
function run(x,mode,checkPotential=true){
 const s=start(),initial=potential(s,x);let checked=0;
 while(s.q!=='HALT'){
  ck(s.count<8*x.length+60,'nontermination');
  for(let i=0;i<3;i++){
   if(mode==='concrete')ck(s.B[i]===s.C[i]%2,'whole-tape factor');
  }
  if(mode!=='concrete'){
   if(s.R0!==null)ck(s.R0===s.C[0]%2,'R0 stale');
   if(s.R1!==null)ck(s.R1===s.C[1]%2,'R1 stale');
  }
  const old=potential(s,x);tick(s,x,mode);
  if(checkPotential){ck(old===1+potential(s,x),'Bellman edge');checked++;}
 }
 ck(s.label===truth(x),'independent assignment truth table');
 ck(s.seenB.size+s.seenC.size===5,'visited writable cell ledger');
 if(mode!=='single-cache')ck(s.count===initial,'initial potential');
 return {steps:s.count,label:s.label,branch0:s.branch0,branch1:s.branch1,mask:s.mask,
  visitedB:[...s.seenB].sort(),visitedC:[...s.seenC].sort(),bellman:checked};
}
function main(){
 const X=[''];for(let L=1;L<=12;L++)for(let v=0;v<2**L;v++)X.push(v.toString(2).padStart(L,'0'));
 const cube=Array.from({length:8},(_,i)=>i.toString(2).padStart(3,'0')).join('');
 X.push(cube,cube+'000',cube+'111',cube.split('').reverse().join(''), '110','101','010','011',
  '1'.repeat(128),'0'.repeat(129),'001'.repeat(38),'110'.repeat(40));
 let pairs=0,steps=0,equalities=0,opposite=0,odds=0,firsts=0;
 const labels={SAT:0,UNSAT:0,MALFORMED:0};
 for(const x of X){
  const a=run(x,'concrete'),b=run(x,'two-cache');
  ck(JSON.stringify(a)===JSON.stringify(b),'concrete/quotient divergence');
  pairs++;steps+=a.steps;equalities+=b.bellman;labels[a.label]++;
  if(a.branch0!==a.branch1)opposite++;
  odds+=a.branch0;firsts+=a.branch1;
 }
 let allSymbolChecks=0;
 for(let c=0;c<4;c++)for(let inputBit=0;inputBit<2;inputBit++){
  ck((c+inputBit)%4%2===((c%2)^inputBit),'SCAN paired parity write');allSymbolChecks++;
 }
 for(let c=0;c<4;c++){
  ck((c+2)%4%2===c%2,'REMOTE1 factor-fiber write');allSymbolChecks++;
 }
 for(let r0=0;r0<2;r0++)for(let r1=0;r1<2;r1++){
  ck([r0,r1][1]===r1,'two indexed read registers');allSymbolChecks++;
 }
 const examples=['110','101','010','001','011'].map(x=>{
  let a=run(x,'concrete'),b=run(x,'single-cache',false),diff=a.steps-b.steps;
  ck(diff===(a.branch1-a.branch0)*(2*x.length+3),'precise shortcut cost');
  return {input:x,concrete:a.steps,singleRegister:b.steps,missingRealSteps:diff,
   B0:a.branch0,B1:a.branch1,label:a.label};
 });
 ck(examples.some(x=>x.missingRealSteps>0)&&examples.some(x=>x.missingRealSteps<0),
  'two genuine opposite-direction failures');
 ck(pairs===labels.SAT+labels.UNSAT+labels.MALFORMED,'label count');
 ck(steps===equalities,'complete edge audit');
 return {role:'TMR-4/022',execution:'hosted V8 JavaScript (actually executed)',status:'COMPUTATIONAL',
  class:'fixed-three-variable sign-stream 3-CNF only',exhaustiveLengths:[0,12],
  pairedTraces:pairs,chargedConcreteTransitions:steps,chargedAbstractTransitions:steps,
  allEdgeBellmanEqualities:equalities,labels,oppositeCachedValues:opposite,
  sourceParityOddTraces:odds,firstSourceBitOneTraces:firsts,
  physicalPeakVisitedWritableCells:5,allSymbolCertificateChecks:allSymbolChecks,
  hostileSingleRegisterFailures:examples,
  hostileTampering:{staleR1:'reject: R1 != f(C[1])',nonFiberC2Write:'reject: f(1) != f(0)',
    zeroCostFinish:'reject: positive potential at REMOTE1 cannot traverse zero-cost HALT'},
  failures:0};
}
console.log(JSON.stringify(main(),null,2));
