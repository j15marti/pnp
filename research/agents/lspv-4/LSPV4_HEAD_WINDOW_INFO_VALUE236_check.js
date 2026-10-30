// HEAD-WINDOW-INFO-VALUE236: dependency-free exact finite controls.
// Run with: node LSPV4_HEAD_WINDOW_INFO_VALUE236_check.js
// Intended scope: independently reset future INDEX contexts on one read-only source head.
// No conclusion about unrestricted SAT, RAM travel, or polynomial-time lower bounds.
"use strict";
function encode(t, signs) {
  const d=Math.ceil(Math.log2(4*t+3));
  const bin=(v)=>v.toString(2).padStart(d,"0");
  const prefix="10111"+bin(t)+"00";
  const records=signs.map((s,i)=>"01"+bin(i)+"101"+s+"011");
  const tail=Array.from({length:t},(_,i)=>"11"+bin(i)+"00010011").join("");
  const text=prefix+records.join("")+tail, g=d+9;
  const positions=Array.from({length:t},(_,i)=>prefix.length+i*g+2+d+3);
  for(let i=0;i<t;i++) if(text[positions[i]]!==String(signs[i])) throw Error("serialization");
  return {text,positions,g,N:text.length};
}
function bruteContext(t,s,i) {
  const n=4*t+1;
  for(let v=0;v<2**n;v++) {
    const bit=(j)=>Math.floor(v/2**j)%2;
    if(bit(i+1)||bit(t+1+i)||bit(2*t+1)||bit(3*t+1)) continue;
    let good=true;
    for(let j=0;j<t;j++) {
      const left=bit(0)||(bit(1+j)^s[j])||bit(t+1+j);
      const right=!bit(0)||bit(2*t+1+j)||bit(3*t+1+j);
      if(!left||!right){good=false;break;}
    }
    if(good) return true;
  }
  return false;
}
function frontier(t,L) {
  const s=Array.from({length:t},(_,i)=>(7*i+Math.floor(i/3)+1)%2);
  const {text,positions,g,N}=encode(t,s);
  const p=L<t?Math.floor((positions[L]+positions[t-1])/2):positions[0];
  let H=0;
  for(let i=0;i<t;i++) {
    const got=i<L?s[i]:Number(text[positions[i]]);
    if(got!==s[i]) throw Error("incorrect read");
    H=Math.max(H,i<L?0:Math.abs(positions[i]-p));
  }
  const optimum=L<t?Math.ceil(g*(t-L-1)/2):0;
  if(H!==optimum)throw Error("frontier mismatch");
  const capacity=L+Math.floor(2*H/g)+1;
  if(capacity<t)throw Error("capacity bound");
  return {t,L,N,g,H,capacity,optimum,headStart:p};
}
function rewritable(t) {
  const s=Array.from({length:t},(_,i)=>i%2);
  const {text,positions,g,N}=encode(t,s);
  const w=text.split(""); let changes=0;
  for(let i=0;i<t;i++) {
    const bit=w[positions[i]];
    if(w[i]!==bit){w[i]=bit;changes++;}
  }
  for(let i=0;i<t;i++)if(w[i]!==String(s[i]))throw Error("rewriter error");
  if(changes>t)throw Error("change bound");
  return {t,N,originalGap:g,rewrittenGap:1,changedInputCells:changes,
          sourceStillPhysicallyPresentBits:N,conservativeMoveUpper:2*t*N};
}
function run(){
  let contexts=0;
  for(let t=1;t<=3;t++)for(let mask=0;mask<2**t;mask++){
    const s=Array.from({length:t},(_,i)=>(mask>>i)&1);
    for(let i=0;i<t;i++){
      if(bruteContext(t,s,i)!==Boolean(s[i]))throw Error("four-pin error");
      contexts++;
    }
  }
  const rows=[];
  for(let t of [4,8,16,32,64]) {
    const ls=[...new Set([0,Math.floor(t/4),Math.floor(t/2),
                           Math.floor(3*t/4),t-1,t])].sort((a,b)=>a-b);
    for(let L of ls)rows.push(frontier(t,L));
  }
  const rewritten=[4,8,16,32,64].map(rewritable);
  const example=rows.find(x=>x.t===64&&x.L===32);
  const xor={first:0,second:0,secondAfterFirst:1,firstAfterSecond:1,duplicate:0};
  return {run:"HEAD-WINDOW-INFO-VALUE236",status:"COMPUTATIONAL bounded",
    bruteForceFourPinContexts:contexts,frontierRows:rows.length,
    writableSourceControls:rewritten.length,example,xor,
    rows,rewritten,
    theorem:"fixed head Hmin=max(0,ceil(g*(t-L-1)/2))",
    limitation:"source-present readonly sequential head; not a SAT time lower bound"};
}
if(typeof require!=="undefined" && require.main===module)console.log(JSON.stringify(run(),null,2));
