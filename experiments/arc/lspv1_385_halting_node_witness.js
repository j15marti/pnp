'use strict';
// LSPV-1/385: finite two-bit instruction trace controls; NOT a halting oracle.
const ops={'00':'flip','01':'loop','10':'halt'};
function source(bits){
 if(!/^(?:[01]{2})*$/.test(bits))throw Error('bad encoding');
 return [[1],[-1],...Array.from(bits,(b,i)=>[(b==='1'?1:-1)*(i+2)])];
}
function parseSource(clauses){
 if(!Array.isArray(clauses)||clauses.length<2||JSON.stringify(clauses.slice(0,2))!=='[[1],[-1]]')return null;
 let b='';
 for(let j=2;j<clauses.length;j++){
  const c=clauses[j];
  if(!Array.isArray(c)||c.length!==1||!Number.isInteger(c[0])||Math.abs(c[0])!==j)return null;
  b+=c[0]>0?'1':'0';
 }
 return b.length%2===0?b:null;
}
function simulate(bits,limit=20){
 let pc=0,bit=0,trace=[];
 for(let k=0;k<limit;k++){
  const op=ops[bits.slice(2*pc,2*pc+2)];
  if(op===undefined)return null;
  trace.push([pc,bit]);
  if(op==='halt')return trace;
  if(op==='flip'){pc++;bit^=1;}
 }
 return null;
}
function checkSpecial(f,trace){
 const bits=parseSource(f);
 if(bits===null||!Array.isArray(trace)||trace.length===0)return false;
 let pc=0,bit=0;
 for(let i=0;i<trace.length;i++){
  const item=trace[i];
  if(!Array.isArray(item)||item.length!==2||item[0]!==pc||item[1]!==bit)return false;
  const op=ops[bits.slice(2*pc,2*pc+2)];
  if(op==='halt')return i===trace.length-1;
  if(op==='flip'){pc++;bit^=1;}
  else if(op!=='loop')return false;
 }
 return false;
}
function checkFallback(f,proof){
 return parseSource(f)!==null && JSON.stringify(proof)==='[[1,-1,0],[0,"FINAL"]]';
}
let tests=0,halt=0,nonhalt=0,reject=0;
for(let words=0;words<=3;words++)for(let i=0;i<4**words;i++){
 let code='';
 for(let j=words-1;j>=0;j--)code+=((i>>(2*j))&3).toString(2).padStart(2,'0');
 const f=source(code),tr=simulate(code);
 if(tr)halt++;else nonhalt++;
 if(checkSpecial(f,tr||[])!==(tr!==null))throw Error('special mismatch '+code);
 if(!checkFallback(f,[[1,-1,0],[0,'FINAL']]))throw Error('bad default');
 if(checkSpecial(f,[[0,0],[0,0]]))throw Error('false special');
 if(checkSpecial(f,[[0,0],[0,1]]))throw Error('false flip');
 tests+=4;
}
for(const bad of [[],[[1]],[[1],[-1],[3]],[[1],[-1],[2],[2]],[[1],[-1],[-2],[3],[4]]]){
 if(parseSource(bad)!==null||checkSpecial(bad,[[0,0]])||checkFallback(bad,[[1,-1,0],[0,'FINAL']]))throw Error('accepted malformed');
 reject+=3;
}
console.log(JSON.stringify({model:'finite two-bit-op toy; NOT universal TM',programs:85,words_max:3,halt,nonhalt,assertions:tests+reject,invalid_rejected:reject,seed:null,scope:'finite controls only; uncomputability proved symbolically'},null,2));
