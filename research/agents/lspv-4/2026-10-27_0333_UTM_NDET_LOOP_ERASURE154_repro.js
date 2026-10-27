"use strict";
// Deterministic finite audit of existential nondeterministic path selection.
// Machine transition relation: only LOOP has two possible transitions.
// The external 'bounces' argument chooses a PATH, not machine-readable advice.
let CHECKS=0;
function ok(b,s){if(!b)throw Error(s);CHECKS++;}
const QS=["COPY","REWIND","ENTRY","LOOP","RETURN","WALK","COMPARE","YES","NO"];
function sig(c){return c.q+","+c.i+","+c.w+","+c.t.join("");}
function sim(a,b,g,bounces){
 const input=a+"|"+".".repeat(g)+"|"+b,n=a.length;
 let i=0,w=0,q="COPY",t=Array(n+2).fill(0),left=bounces,steps=[];
 function move(nq,ni,nw,write=-1,value=0){
  const before={i,w,q,t:t.slice()},old=write>=0?t[write]:null;
  if(write>=0)t[write]=value;
  i=ni;w=nw;q=nq;
  ok(Math.abs(before.i-i)<=1 && Math.abs(before.w-w)<=1,"unit head moves");
  steps.push({before,after:{i,w,q,t:t.slice()},edit:write>=0 && old!==value?{at:write,value}:null});
 }
 for(let guard=0;q!=="YES"&&q!=="NO";guard++){
  if(guard>10000)throw Error("no halt");
  if(q==="COPY"){
   if(input[i]!=="|"){ok(input[i]==="0"||input[i]==="1","source bit");move("COPY",i+1,w+1,w,+(input[i]==="1"));}
   else move("REWIND",i,w);
  }else if(q==="REWIND"){if(w)move("REWIND",i,w-1);else move("ENTRY",i,w);}
  else if(q==="ENTRY")move("LOOP",i+1,w);
  else if(q==="LOOP"){if(left){left--;move("RETURN",i-1,w);}else move("WALK",i+1,w);}
  else if(q==="RETURN")move("LOOP",i+1,w);
  else if(q==="WALK"){if(input[i]==="|")move("COMPARE",i+1,w);else{ok(input[i]===".","gap");move("WALK",i+1,w);}}
  else if(q==="COMPARE"){if(i===input.length)move("YES",i,w);else if(input[i]==="1"&&t[w]===1)move("NO",i,w);else move("COMPARE",i+1,w+1);}
  else throw Error(q);
 }
 return {accept:q==="YES",input,steps};
}
function erase(steps){
 let keep=[],seen=new Map([[sig(steps[0].before),0]]);
 for(const st of steps){
  const prev=keep.length?keep[keep.length-1].after:steps[0].before;
  ok(sig(prev)===sig(st.before),"path stitches");
  const z=sig(st.after);
  if(seen.has(z)){
   const n=seen.get(z);
   while(keep.length>n)seen.delete(sig(keep.pop().after));
  }else{keep.push(st);seen.set(z,keep.length);}
 }
 ok(sig(keep[0].before)===sig(steps[0].before),"same start");
 ok(sig(keep[keep.length-1].after)===sig(steps[steps.length-1].after),"same accepting or rejecting final config");
 return keep;
}
function ledger(steps,cut){
 let edits=0,turns=0,last=0,seen=new Set(),cross=0,events=[];
 for(const st of steps){
  seen.add(st.before.w);seen.add(st.after.w);
  if(st.edit){edits++;events.push("E"+st.edit.at+"="+st.edit.value);}
  const dir=Math.sign(st.after.i-st.before.i);
  if(dir&&last&&dir!==last)turns++;
  if(dir)last=dir;
  if((st.before.i===cut&&st.after.i===cut+1)||(st.before.i===cut+1&&st.after.i===cut)){
   cross++;events.push("C"+dir+","+st.after.q+","+st.after.w);
  }
 }
 return {D:edits,S:seen.size,R:turns,T:steps.length,L:cross,word:events.join("|")};
}
function bin(i,n){return i.toString(2).padStart(n,"0");}
function audit(){
 const result={type:"finite-exhaustive-with-constructed-nondeterministic-bounce-branches",seed:null,pairs:0,yesPairs:0,noPairs:0,normalized:0,diagonals:0,cutChecks:0,samples:{}};
 for(let m=1;m<=5;m++){
  const lim=1<<m,g=2*m+3;
  for(let i=0;i<lim;i++)for(let j=0;j<lim;j++){
   const a=bin(i,m),b=bin(j,m),yes=(i&j)===0;
   const base=sim(a,b,g,0),long=sim(a,b,g,3),short=erase(long.steps);
   ok(base.accept===yes&&long.accept===yes,"DISJ native YES/NO soundness");
   ok(short[short.length-1].after.q===(yes?"YES":"NO"),"loop removal preserves final label");
   const bb=ledger(base.steps,m),ll=ledger(long.steps,m),ss=ledger(short,m);
   ok(ss.D<=ll.D&&ss.S<=ll.S&&ss.R<=ll.R&&ss.T<=ll.T,"resource monotonicity");
   ok(bb.D===ss.D,"optional bounces do not change work");
   result.pairs++;result.normalized++;if(yes)result.yesPairs++;else result.noPairs++;
  }
  for(let c=m+1;c<m+g;c++){
   const signatures=new Set();
   for(let i=0;i<lim;i++){
    const a=bin(i,m),b=bin(lim-1-i,m),path=sim(a,b,g,7);
    ok(path.accept,"SAT diagonal");
    const accepted=erase(path.steps),z=ledger(accepted,c);
    const V=2*QS.length*(2*z.S+3);
    ok(z.L<=Math.min(z.R+1,(z.D+1)*V+z.D),"loop-free no-change epoch");
    ok(!signatures.has(z.word),"diagonal splice-injective chronicle");
    signatures.add(z.word);result.cutChecks++;
    if(m===5&&i===21&&c===m+1)result.samples.diagonal={m,a,b,resources:z};
   }
  }
  result.diagonals+=lim;
 }
 const raw=sim("0","1",3,260),short=erase(raw.steps),A=ledger(raw.steps,1),B=ledger(short,1);
 const V=2*QS.length*(2*B.S+3);
 ok(raw.accept&&short[short.length-1].after.q==="YES","nondeterministic branch accepts");
 ok(A.D===0&&B.D===0,"no work symbol changed");
 ok(A.L>V,"raw accepting path violates deterministic no-change epoch cap");
 ok(B.L<=V,"loop-erased accepting path respects epoch cap");
 result.samples.epochCounterexample={input:raw.input,raw:A,loopErased:B,V};
 for(let k=1;k<=3;k++)for(let si=0;si<=5;si++)for(let di=0;di<=5;di++){
  const s=si/10,d=di/10;
  ok(d+k*s<1-1e-9 || d+k*s+Math.min(d,s)>=1-1e-9,"new face implies old face");
 }
 result.assertions=CHECKS;
 return result;
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
