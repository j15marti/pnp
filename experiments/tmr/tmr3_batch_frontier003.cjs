"use strict";

// TMR-3/003 finite source emulator, NOT physical TM step simulation.

// Run: node experiments/tmr/tmr3_batch_frontier003.cjs

function enc(n,a,b){
  const w=Math.max(1,Math.ceil(Math.log2(5*n)));
  let src="1".repeat(5*n)+"0"+"1".repeat(8*n)+"0";
  for(let side=0;side<2;side++){
    const bits=side===0?a:b;
    for(let i=0;i<n;i++){
      const aux=(side===0?n:3*n)+2*i;
      for(let r=0;r<4;r++){
        const signs=[1-bits[i],(r>>1)&1,r&1],ids=[i,aux,aux+1];
        for(let h=0;h<3;h++)src+=signs[h]+ids[h].toString(2).padStart(w,"0");
      }
    }
  }
  return src;
}

function familyShape(src){
  if(typeof src!=="string"||!src.length)return null;
  for(let i=0;i<src.length;i++)if(src[i]!=="0"&&src[i]!=="1")return null;
  let i=0;while(i<src.length&&src[i]==="1")i++;
  const N=i;if(!N||N%5||src[i]!=="0")return null; const n=N/5;
  i++;let M=0;while(i<src.length&&src[i]==="1"){M++;i++;}
  if(M!==8*n||src[i]!=="0")return null;
  i++;const base=i,w=Math.max(1,Math.ceil(Math.log2(N))),g=12*(1+w),L=base+2*n*g;
  if(src.length!==L)return null;
  for(let side=0;side<2;side++)for(let j=0;j<n;j++){
    const aux=(side===0?n:3*n)+2*j;
    let fixedSign=null;
    for(let r=0;r<4;r++){
      const expectedSigns=[null,(r>>1)&1,r&1],expectedIDs=[j,aux,aux+1];
      for(let k=0;k<3;k++){
        const sign=src.charCodeAt(i)-48;
        let idx=0;for(let z=0;z<w;z++)idx=idx*2+(src.charCodeAt(i+1+z)-48);
        if(idx!==expectedIDs[k]||(k!==0&&sign!==expectedSigns[k]))return null;
        if(k===0){if(fixedSign===null)fixedSign=sign;else if(sign!==fixedSign)return null;}
        i+=1+w;
      }
    }
  }
  return {n,w,g,base,L};
}

function streamBatches(src,s,shape){
  if(!shape)throw Error("nonfamily source");
  const {n,g,base,L}=shape;const b=Math.max(1,Math.min(n,Math.floor(s)));
  let equal=true,sweeps=0,forward=0,reversals=0,maxBuffer=0;
  for(let from=0;from<n;from+=b){
    const count=Math.min(b,n-from),buf=[];
    let block=0,nextStart=base;
    for(let pos=0;pos<L;pos++){
      forward++;
      if(pos===nextStart&&block<2*n){
        const bank=Math.floor(block/n),j=block%n;
        if(j>=from&&j<from+count){
          if(bank===0)buf.push(src[pos]);
          else if(buf[j-from]!==src[pos])equal=false;
        }
        block++;nextStart+=g;
      }
    }
    if(block!==2*n||buf.length!==count)throw Error("stream layout");
    maxBuffer=Math.max(maxBuffer,buf.length);
    sweeps++;
    if(from+b<n)reversals+=L-1;
  }
  return {sat:equal,sweeps,forward,reversals,maxBuffer,readHeadMoves:forward+reversals};
}

function audit(){
  let stats={format:"TMR3-FRONTIER003",exhaustivePairs:0,exhaustiveRuns:0,randomPairs:0,randomRuns:0,satisfiablePairs:0,unsatisfiablePairs:0,malformedRejects:0,flipRejects:0,assertions:0,forwardBitVisits:0,rewindHeadMoves:0,maxN:0,maxL:0,failures:0,randomSeed:"0x31f7d509",lengths:{}};
  function check(v,msg){stats.assertions++;if(!v)throw Error(msg);}
  function verify(n,a,b){
    const src=enc(n,a,b),p=familyShape(src);
    check(!!p,"family membership");
    check(p.n===n&&p.L===src.length,"length");
    check(p.L===13*n+2+24*n*(1+p.w),"length formula");
    const eq=a.every((z,i)=>z===b[i]);
    const targets=Array.from(new Set([1,2,Math.ceil(Math.log2(n+1)),Math.ceil(n/3),Math.ceil(n/2),n])).filter(s=>s<=n);
    for(const s of targets){
      const o=streamBatches(src,s,p);
      check(o.sat===eq,"SAT label");
      check(o.sweeps===Math.ceil(n/s),"pass count");
      check(o.maxBuffer<=s,"retained sign bound");
      check(o.forward===o.sweeps*src.length,"full read cost");
      check(o.reversals===(o.sweeps-1)*(src.length-1),"paid reversals");
      stats.forwardBitVisits+=o.forward;stats.rewindHeadMoves+=o.reversals;
    }
    const at=p.base;
    const flip=src.slice(0,at)+(src[at]==="1"?"0":"1")+src.slice(at+1);
    check(familyShape(flip)===null,"single gadget sign mutation rejected");
    stats.flipRejects++;
    for(const bad of [src.slice(0,-1),src+"1",src.replace(/^1/,"0")]){
      check(familyShape(bad)===null,"malformed control rejected");stats.malformedRejects++;
    }
    stats.maxN=Math.max(stats.maxN,n);stats.maxL=Math.max(stats.maxL,src.length);
    return {eq,runs:targets.length,L:src.length};
  }
  for(let n=1;n<=5;n++){
    stats.lengths[n]=enc(n,new Array(n).fill(0),new Array(n).fill(0)).length;
    for(let x=0;x<2**n;x++)for(let y=0;y<2**n;y++){
      const a=Array.from({length:n},(_,i)=>(x>>i)&1);
      const b=Array.from({length:n},(_,i)=>(y>>i)&1);
      const r=verify(n,a,b);
      stats.exhaustivePairs++;stats.exhaustiveRuns+=r.runs;
      stats[r.eq?"satisfiablePairs":"unsatisfiablePairs"]++;
    }
  }
  let z=0x31f7d509;function next(){z^=z<<13;z^=z>>>17;z^=z<<5;return z>>>0;}
  for(const n of [6,8,16,32,64,128]){
    for(let r=0;r<20;r++){
      const a=Array.from({length:n},()=>next()&1),b=r%4===0?a.slice():Array.from({length:n},()=>next()&1);
      const v=verify(n,a,b);stats.randomPairs++;stats.randomRuns+=v.runs;
      stats[v.eq?"satisfiablePairs":"unsatisfiablePairs"]++;
    }
  }
  stats.cases=stats.exhaustivePairs+stats.randomPairs;
  return stats;
}

if (require.main === module) process.stdout.write(JSON.stringify(audit(),null,2)+"\n");

module.exports={enc,familyShape,streamBatches,audit};
