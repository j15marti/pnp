#!/usr/bin/env node
"use strict";
const audit = function audit(){
  let assertions=0, foolingPairs=0, truthPairs=0, negativePairs=0, samples=0;
  const ck=(p,m)=>{assertions++;if(!p)throw Error(m||"failed")};
  const vectors=m=>Array.from({length:2**m},(_,x)=>Array.from({length:m},(_,i)=>(x>>i)&1));
  const disj=(a,b)=>a.every((v,i)=>!(v&b[i]));
  const transcript=(a,B)=>{let z=[];for(let i=0;i<a.length;i+=B)z.push(a.slice(i,i+B).join(""));return z.join("|")};
  for(let m=1;m<=8;m++){
    const vs=vectors(m);
    for(const a of vs)ck(disj(a,a.map(z=>1-z)),"fooling YES");
    if(m<=6)for(const a of vs)for(const b of vs){
      truthPairs++;ck(disj(a,b)==!a.some((v,i)=>v===1&&b[i]===1),"disjoint");
      if(a.join("")!==b.join("")){negativePairs++;ck(!disj(a,b.map(z=>1-z))||!disj(b,a.map(z=>1-z)),"splicing");}
    }
    for(let i=0;i<vs.length;i++)for(let j=i+1;j<vs.length;j++){
      foolingPairs++;ck(transcript(vs[i],1)!==transcript(vs[j],1),"trace");
      if(m<=5)for(let B=1;B<=m;B++)ck(transcript(vs[i],B)!==transcript(vs[j],B),"buffer trace");
    }
  }
  const rows=[];
  for(const m of [4,8,16,32,64,128]){
    const w=Math.max(4,Math.ceil(Math.log2(32*m+2))+4);
    const N=20*m*w,G=16*m*w;
    const ls=Array.from({length:m},(_,i)=>i*w);
    const rs=Array.from({length:m},(_,i)=>18*m*w+i*w);
    ck(G===4*N/5);ck(ls[m-1]<2*m*w);ck(rs[0]===18*m*w);
    const Bset=[...new Set([1,2,4,Math.ceil(Math.sqrt(m)),m])].filter(B=>B<=m).sort((a,b)=>a-b);
    const Jset=[...new Set([1,2,8,Math.ceil(Math.sqrt(N)),N])].filter(J=>J<=N).sort((a,b)=>a-b);
    for(const B of Bset){
      let reversals=[],moves=[];
      for(const J of Jset){
        const z={pos:0,sign:0,rev:0,moves:0,cuts:0,reads:0,idx:0};
        function step(target){
          const delta=target-z.pos;
          if(delta){
            const sign=Math.sign(delta);
            if(z.sign&&sign!==z.sign)z.rev++;
            z.sign=sign;
            z.moves+=Math.ceil(Math.abs(delta)/J);
            const lo=Math.min(target,z.pos),hi=Math.max(target,z.pos);
            z.cuts+=Math.max(0,Math.min(hi,18*m*w)-Math.max(lo,2*m*w));
          } else z.moves++;
          z.pos=target;z.reads++;
          z.idx+=Math.max(1,Math.ceil(Math.abs(delta)/J))*Math.ceil(Math.log2(N+1));
        }
        for(let i=0;i<m;i+=B){for(let t=i;t<Math.min(m,i+B);t++)step(ls[t]);for(let t=i;t<Math.min(m,i+B);t++)step(rs[t]);}
        ck(z.reads===2*m);ck(z.cuts<=J*z.moves);ck(z.rev+1>=Math.ceil(m/B));ck(z.moves>=m);
        reversals.push(z.rev);moves.push(z.moves);samples++;
        if(([16,64,128].includes(m))&&(B===1||B===m)&&(J===1||J===N)){
          rows.push({m,N,buffer:B,jump_radius:J,head_commands:z.moves,input_reversals:z.rev,work_upper:B+Math.ceil(Math.log2(N+1))+8,source_reads:z.reads,gap_crossed_cuts:z.cuts,charged_index_bits:z.idx});
        }
      }
      ck(reversals.every(x=>x===reversals[0]),"reversal monotonic");
      ck(moves.every((x,i)=>i===0||x<=moves[i-1]),"jump monotonic");
    }
  }
  return {run:"HEADMOVE-JUMP-REVERSAL141",status:"COMPUTATIONAL; symbolically proved model-native lemma in LaTeX",abstract_source:"fixed-record left, middle gap (80% of N), right; not materialized CNF",assertions,failed:0,fooling_pairs:foolingPairs,truth_pairs:truthPairs,negative_pairs:negativePairs,configurations:samples,selected_rows:rows};
};
const result = audit();
console.log(JSON.stringify(result,null,2));
