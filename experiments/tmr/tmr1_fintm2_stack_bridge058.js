'use strict';
// TMR-1/058: finite-stack -> locally headed multitape microstep equivalence.
// FINITE EVIDENCE ONLY; symbolic theorem is in the mathematical report.
const SEED=20261115; let seed=SEED >>> 0;
function rng(){seed ^= seed<<13;seed ^= seed>>>17;seed ^= seed<<5;return seed>>>0;}
const pick=n=>rng()%n;
let assertions=0, cases=0, steps=0, internalOps=0, microOps=0, failures=0;
let maxBlockOps=0, maxPeak=0, maxLength=0, completed=0;
function check(x,detail){assertions++;if(!x){failures++;throw Error(detail);}}
const MOD=5, K=4;
function mix(v,top,offset){return ((v+(top===null?3:top)+offset)%MOD);}
function read0(stack){return stack.length?stack[0]:null;}
function makeStatement(depth=0){
  if(depth>=4) return {kind:pick(6)===0?'halt':'goto',target:pick(3)};
  const kind=pick(9);
  if(kind===0) return {kind:'push',k:pick(K),bias:pick(3),q:makeStatement(depth+1)};
  if(kind===1) return {kind:'pop',k:pick(K),bias:pick(MOD),q:makeStatement(depth+1)};
  if(kind===2) return {kind:'peek',k:pick(K),bias:pick(MOD),q:makeStatement(depth+1)};
  if(kind===3) return {kind:'load',bias:pick(MOD),q:makeStatement(depth+1)};
  if(kind===4) return {kind:'branch',bias:pick(MOD),yes:makeStatement(depth+1),no:makeStatement(depth+1)};
  if(kind===5) return {kind:'halt'};
  return {kind:'goto',target:pick(3)};
}
function termSize(st){switch(st.kind){case 'branch':return 1+termSize(st.yes)+termSize(st.no);case 'goto':case 'halt':return 1;default:return 1+termSize(st.q);}}
function normalStep(cfg,prg){
 if(cfg.label===null)return {cfg,ops:0};
 let l=cfg.label,v=cfg.state,S=cfg.stacks.map(x=>x.slice()),ops=0;
 let node=prg[l];
 while(true){ops++;
   switch(node.kind){
   case 'push': S[node.k].unshift((v+node.bias)%3);node=node.q;break;
   case 'pop':{const t=read0(S[node.k]);v=mix(v,t,node.bias);if(t!==null)S[node.k].shift();node=node.q;break;}
   case 'peek':v=mix(v,read0(S[node.k]),node.bias);node=node.q;break;
   case 'load':v=(v+node.bias)%MOD;node=node.q;break;
   case 'branch':node=(v+node.bias)%2?node.yes:node.no;break;
   case 'goto':return {cfg:{label:node.target,state:v,stacks:S},ops};
   case 'halt':return {cfg:{label:null,state:v,stacks:S},ops};
   default:throw Error('invalid statement');
 }}
}
// Tape head at first blank to the RIGHT of stored symbols.  One tape per stack,
// with bottom at cell zero; top symbol at head-1. All moves are local.
function physicalStep(cfg,prg){
 if(cfg.label===null)return {cfg,ops:0,micro:0};
 let l=cfg.label,v=cfg.state,tapes=cfg.tapes.map(t=>({cells:t.cells.slice(),head:t.head})),ops=0,micro=0;
 let node=prg[l];
 while(true){ops++;
  switch(node.kind){
   case 'push':{
     const t=tapes[node.k];check(t.head===t.cells.length,'write at end only');
     t.cells.push((v+node.bias)%3);t.head++;micro+=3;node=node.q;break;
   }
   case 'pop':{
     const t=tapes[node.k];const top=t.head?t.cells[t.head-1]:null;
     v=mix(v,top,node.bias);if(t.head){t.head--;t.cells.pop();micro+=3;}else micro+=1;
     node=node.q;break;
   }
   case 'peek':{
     const t=tapes[node.k];const top=t.head?t.cells[t.head-1]:null;
     v=mix(v,top,node.bias);micro+=3;node=node.q;break;
   }
   case 'load':v=(v+node.bias)%MOD;micro++;node=node.q;break;
   case 'branch':node=(v+node.bias)%2?node.yes:node.no;micro++;break;
   case 'goto':micro++;return {cfg:{label:node.target,state:v,tapes},ops,micro};
   case 'halt':micro++;return {cfg:{label:null,state:v,tapes},ops,micro};
   default:throw Error('invalid statement');
  }
 }
}
for(let p=0;p<120;p++){
 const program=Array.from({length:3},()=>makeStatement());
 const sizeMax=Math.max(...program.map(termSize));maxBlockOps=Math.max(maxBlockOps,sizeMax);
 for(let w=0;w<16;w++){
  let len=pick(29),word=Array.from({length:len},()=>pick(2));maxLength=Math.max(maxLength,len);
  let s={label:0,state:0,stacks:[word,...Array.from({length:K-1},()=>[])]};
  // Initial physical encoding lays input list in reverse order, so head-1 is its first item;
  // charge <=2B copy moves and <=2B initialization writes.
  let t={label:0,state:0,tapes:[{cells:word.slice().reverse(),head:len},...Array.from({length:K-1},()=>({cells:[],head:0}))]};
  let currentSteps=0,pushUpper=0;
  for(let r=0;r<80;r++){
    check(s.label===t.label&&s.state===t.state,'control mismatch');
    for(let k=0;k<K;k++){
      check(t.tapes[k].head===t.tapes[k].cells.length,'head mismatch');
      check(JSON.stringify(s.stacks[k])===JSON.stringify(t.tapes[k].cells.slice().reverse()),'stack mismatch');
    }
    let peak=t.tapes.reduce((a,z)=>a+z.head,0);maxPeak=Math.max(maxPeak,peak);
    check(peak<=len+currentSteps*sizeMax,'charged symbol capacity');
    if(s.label===null){completed++;break;}
    const a=normalStep(s,program),b=physicalStep(t,program);
    check(a.ops===b.ops && b.ops<=sizeMax,'fixed block cost');
    check(b.micro<=3*b.ops,'local micro work');
    s=a.cfg;t=b.cfg;currentSteps++;steps++;internalOps+=a.ops;microOps+=b.micro;
  }
  cases++;
 }
}
const summary={revision:'tmr1-fintm2-stack-bridge058.v1',seed:SEED,programs:120,cases,finite_steps:steps,statement_nodes:internalOps,charged_microsteps:microOps,assertions,failures,terminated_samples:completed,max_block_ast_nodes:maxBlockOps,max_initial_input_bits:maxLength,max_live_stack_symbols:maxPeak,model:'fixed K=4 stacks, 3 labels, 5 finite states, symbols 0/1/2; random bounded finite block trees',limits:'Finite-state synthetic machine replay only. Not pinned theorem proof, not Lean kernel rebuild, not a standard physical TM interpreter microtrace.'};
process.stdout.write(JSON.stringify(summary,null,2)+'\n');
