"use strict";
/* TMR-3/008: original strict 3CNF equality source batched without altering a clause.
 * Executes exact source-level verification, head motion and cache accounting.
 * NOT a physical finite-alphabet multitape TM simulator.
 */
const W=n=>Math.max(1,Math.ceil(Math.log2(Math.max(2,n))));
const bits=(n,w)=>n.toString(2).padStart(w,"0");
const gcd=(a,b)=>b?gcd(b,a%b):a;
function block(n,i,bank,value){
  const w=W(5*n),z=(bank===0?n:3*n)+2*i,s=String(1-value);
  let out="";
  for(let u=0;u<2;u++)for(let v=0;v<2;v++)
    out+=s+bits(i,w)+u+bits(z,w)+v+bits(z+1,w);
  return out;
}
function encode(n,a,c,batch){
  if(n<1||batch<1||!Number.isInteger(batch))throw Error("bad size");
  let src="1".repeat(5*n)+"0"+"1".repeat(8*n)+"0";
  for(let base=0;base<n;base+=batch){
    const stop=Math.min(n,base+batch);
    for(let i=base;i<stop;i++)src+=block(n,i,0,a[i]);
    for(let i=base;i<stop;i++)src+=block(n,i,1,c[i]);
  }
  return src;
}
function groupedPermutation(src,n,batch){
  const h=13*n+2,g=12*(W(5*n)+1);
  let out=src.slice(0,h);
  for(let base=0;base<n;base+=batch){
    const stop=Math.min(n,base+batch);
    for(let i=base;i<stop;i++)out+=src.slice(h+i*g,h+(i+1)*g);
    for(let i=base;i<stop;i++)out+=src.slice(h+(n+i)*g,h+(n+i+1)*g);
  }
  return out;
}
function recognize(src,batchForN,rForN){
  let pos=0,moves=0,reads=0,fieldChecks=0,rounds=0,compared=0,maxCache=0,rewound=0;
  function next(){reads++;if(pos>=src.length)return "#";const x=src[pos++];moves++;return x;}
  function rewind(count){if(count>pos)throw Error("left end");pos-=count;moves+=count;rewound+=count;}
  const fail=()=>({member:false,pos,moves,reads,fieldChecks,rounds,compared,maxCache,rewound});
  let n5=0,ch;
  while((ch=next())==="1")n5++;
  if(ch!=="0"||n5<5||n5%5)return fail();
  const n=n5/5,w=W(5*n),g=12*(w+1),batch=batchForN(n),r=rForN(n);
  if(!Number.isInteger(batch)||batch<1||!Number.isInteger(r)||r<1)return fail();
  for(let j=0;j<8*n;j++)if(next()!=="1")return fail();
  if(next()!=="0")return fail();
  let equal=true;
  for(let base=0;base<n;base+=batch){
    const size=Math.min(batch,n-base),origin=pos,numRounds=Math.ceil(size/r);
    for(let pass=0;pass<numRounds;pass++){
      if(pass>0)rewind(2*size*g);
      if(pos!==origin)throw Error("batch seek mismatch");
      const lo=pass*r,hi=Math.min(size,lo+r),cache=[];
      rounds++;
      for(let bank=0;bank<2;bank++)for(let j=0;j<size;j++){
        const i=base+j,z=(bank===0?n:3*n)+2*i;
        let first=null;
        for(let u=0;u<2;u++)for(let v=0;v<2;v++){
          const sign=next();if(sign!=="0"&&sign!=="1")return fail();
          if(first===null)first=sign;
          if(sign!==first)return fail();
          const expected=bits(i,w)+u+bits(z,w)+v+bits(z+1,w);
          for(let k=0;k<expected.length;k++){fieldChecks++;if(next()!==expected[k])return fail();}
        }
        if(j>=lo&&j<hi){
          if(bank===0){cache.push(first);maxCache=Math.max(maxCache,cache.length);}
          else{if(cache[j-lo]!==first)equal=false;compared++;}
        }
      }
      if(pos!==origin+2*size*g)throw Error("batch end mismatch");
    }
  }
  if(next()!=="#"||pos!==src.length)return fail();
  return {member:true,sat:equal,n,L:src.length,batch,r,moves,reads,fieldChecks,rounds,compared,maxCache,rewound};
}
function clauses(src,n){
  const h=13*n+2,rec=3*(W(5*n)+1),m=8*n;
  return Array.from({length:m},(_,j)=>src.slice(h+j*rec,h+(j+1)*rec));
}
function brute(src,n){
  const w=W(5*n),h=13*n+2,rec=3*(w+1),arr=[];
  for(let j=0;j<8*n;j++){
    let clause=[];
    for(let k=0;k<3;k++){
      const f=src.slice(h+j*rec+k*(w+1),h+j*rec+(k+1)*(w+1));
      clause.push([parseInt(f.slice(1),2),f[0]==="1"]);
    }
    arr.push(clause);
  }
  for(let assignment=0;assignment<2**(5*n);assignment++){
    if(arr.every(c=>c.some(([id,neg])=>Boolean((assignment>>id)&1)!==neg)))return true;
  }
  return false;
}
function audit(){
  const out={id:"TMR3-BATCH-CROSSING008",status:"COMPUTATIONAL",scope:"single local input-head source-level model, not native finite TM",parameters:{seed:"0x3b71c008",exhaustiveN:"1..4",largeN:[8,16,32,64,128,256]},valid:0,sat:0,unsat:0,variants:0,sublinearCacheVariants:0,originalCNFBrute:0,wholeClausePermutations:0,negativeControls:0,moves:0,rewinds:0,reads:0,rounds:0,pairedSignChecks:0,maxInputLength:0,maxCache:0,failures:0,samples:[]};
  function assert(cond,msg){if(!cond){out.failures++;throw Error(msg);}}
  function check(n,a,c){
    const grouped=encode(n,a,c,n),originalClauses=clauses(grouped,n).sort();
    const sizeSet=[1,2,Math.max(1,Math.floor(Math.sqrt(n))),Math.max(1,Math.floor(n/2)),n];
    for(const batch of new Set(sizeSet)){
      const src=encode(n,a,c,batch),expect=a.every((x,i)=>x===c[i]);
      assert(src===groupedPermutation(grouped,n,batch),"not literal original block permutation");
      assert(src.length===13*n+2+24*n*(W(5*n)+1),"length discrepancy");
      assert(JSON.stringify(clauses(src,n).sort())===JSON.stringify(originalClauses),"changed CNF multiset");
      out.wholeClausePermutations++;
      for(const r of new Set([1,Math.max(1,Math.floor(Math.sqrt(batch))),batch])){
        const run=recognize(src,()=>batch,()=>r);
        assert(run.member&&run.sat===expect&&run.n===n&&run.L===src.length,"wrong membership/answer");
        assert(run.maxCache<=r&&run.compared===n,"unpaid cache or comparison");
        assert(run.moves===src.length+2*run.rewound,"head movement accounting");
        assert(run.rounds===Array.from({length:Math.ceil(n/batch)},(_,k)=>Math.ceil(Math.min(batch,n-k*batch)/r)).reduce((x,y)=>x+y,0),"round count");
        out.valid++;out[expect?"sat":"unsat"]++;out.variants++;if(r<batch)out.sublinearCacheVariants++;
        out.moves+=run.moves;out.rewinds+=run.rewound;out.reads+=run.reads;out.rounds+=run.rounds;out.pairedSignChecks+=run.compared;out.maxInputLength=Math.max(out.maxInputLength,run.L);out.maxCache=Math.max(out.maxCache,run.maxCache);
        if(out.samples.length<14&&!out.samples.some(x=>x.n===n&&x.batch===batch&&x.r===r))out.samples.push({n,batch,r,L:run.L,rounds:run.rounds,moves:run.moves,rewound:run.rewound,cache:run.maxCache,sat:run.sat});
      }
      if(n<=2){assert(brute(src,n)===expect,"original CNF brute mismatch");out.originalCNFBrute++;}
      const h=13*n+2,g=12*(W(5*n)+1),mutated=[src.slice(0,-1),src+"0",src.slice(1),src.slice(0,h+g+1)+(src[h+g+1]==="0"?"1":"0")+src.slice(h+g+2)];
      for(const bad of mutated){assert(!recognize(bad,()=>batch,()=>1).member,"structural mutant accepted");out.negativeControls++;}
    }
  }
  for(let n=1;n<=4;n++)for(let ai=0;ai<2**n;ai++)for(let ci=0;ci<2**n;ci++)check(n,Array.from({length:n},(_,i)=>(ai>>i)&1),Array.from({length:n},(_,i)=>(ci>>i)&1));
  let seed=0x3b71c008;
  function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
  for(const n of out.parameters.largeN)for(let j=0;j<8;j++){
    const a=Array.from({length:n},()=>rand()>>>29&1),c=j===0?a.slice():Array.from({length:n},()=>rand()>>>29&1);
    check(n,a,c);
  }
  return out;
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
if(typeof module!=="undefined")module.exports={W,bits,block,encode,groupedPermutation,recognize,clauses,brute,audit};
