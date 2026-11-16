#!/usr/bin/env node
"use strict";
function runAudit(){
  const REV="tmr3-schedule-cover063-js-v1", SEED=202611152338;
  let seed=SEED>>>0; const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;};
  const counts={checks:0,valid:0,guesses:0,fail:0,accepted:0,H:0,revisits:0,nonlinearReads:0,maxLive:0,malformed:0,physicalChecked:0,labels0:0,labels1:0};
  function ck(b,msg){counts.checks++;if(!b)throw Error("FAIL "+msg);}
  const auth=x=>typeof x==="string"&&x.length>=1&&/^[01]+$/.test(x);
  const pars=x=>{const n=x.length,r=Math.floor(Math.log2(n))+1,b=n+5;return {n,r,b,B:r+3,T:b*(r+2)+1};};
  function trans(q0,q1,d,x){return [q0^x^d,(q0&(1-q1))^x^d];}
  function active(z,k,r){counts.H++;return k===0?0:(z>>>(r-k))&1;}
  function real(x){
    const {n,r,b,B,T}=pars(x);ck(T<2**b||b>52,"legal b");
    let q0=0,q1=0,pos=0,D=[0,0],snap=[],steps=[];
    for(let k=0;k<r;k++){
      ck(pos===0||pos===1,"active block");let d=D[pos],v=trans(q0,q1,d,+x[k]);
      q0=v[0];q1=v[1];D[pos]=q0;counts.nonlinearReads++;
      const next=q1;steps.push(next-pos);
      if(n<=5){for(let i=1;i<b;i++){ck(pos===0||pos===1,"intra-block held");counts.physicalChecked++;}}
      ck(Math.abs(next-pos)<=1,"local move at block boundary");pos=next;
      snap.push({q0,q1,blocks:D.slice(),pos});
    }
    return {out:q0^q1,snap,steps,par:{n,r,b,B,T}};
  }
  function checkCandidate(x,z,realState){
    const {r,b}=realState.par;
    let cache=new Map(),q0=0,q1=0,peak=0;
    for(let k=0;k<r;k++){
      let a=active(z,k,r),M=cache.get("M"+a)||Array(b).fill(0),S=cache.get("S0")||Array(b).fill(0);
      cache.delete("M"+a);cache.delete("S0");
      let d=M[a===0?b-1:0],v=trans(S[0],S[1],d,+x[k]);
      q0=v[0];q1=v[1];S[0]=q0;S[1]=q1;M[a===0?b-1:0]=q0;
      const expected=realState.snap[k];
      ck(q0===expected.q0&&q1===expected.q1,"source-work canonical prefix");
      ck(M[a===0?b-1:0]===expected.blocks[a],"revisited canonical cell");
      let next=active(z,k+1,r);
      if(next!==q1){counts.fail++;return {ok:false,peak};}
      for(const [h,id,contents] of [["M",a,M],["S",0,S]]){
        let future=false;
        for(let j=k+1;j<=r;j++){
          const f=h==="M"?active(z,j,r):0;
          if(f===id){future=true;break;}
        }
        if(future)cache.set(h+id,contents);
      }
      ck(cache.size<=3,"bounded future-live dictionary");peak=Math.max(peak,cache.size+2);
    }
    counts.accepted++;return {ok:true,out:q0^q1,peak};
  }
  function test(x){
    ck(auth(x),"valid source");const rstate=real(x),{n,r}=rstate.par;
    ck((1<<r)<=2*n,"poly sized support");
    let success=0,live=0;
    for(let z=0;z<(1<<r);z++){
      const result=checkCandidate(x,z,rstate);counts.guesses++;
      if(result.ok){success++;ck(result.out===rstate.out,"complete input output");
        ck(result.peak<=5,"same-run full block budget");live=Math.max(live,result.peak);}
    }
    ck(success===1,"unique consistent schedule");
    counts.maxLive=Math.max(counts.maxLive,live);
    let path=[0];for(const step of rstate.steps)path.push(path[path.length-1]+step);
    if(path.includes(0,2)&&path.includes(1))counts.revisits++;
    counts.valid++;
    if(rstate.out===0)counts.labels0++;else counts.labels1++;
  }
  for(let n=1;n<=10;n++)for(let val=0;val<(1<<n);val++)test(val.toString(2).padStart(n,"0"));
  for(const n of [11,12,15,20,31,32,33,48,63,64]){
    for(let i=0;i<25;i++){let x="";for(let j=0;j<n;j++)x+=(rand()&1);test(x);}
  }
  for(const x of ["","2","01?","abc","0 1","\n","00x"]){ck(!auth(x),"reject malformed");counts.malformed++;}
  ck(counts.labels0>0&&counts.labels1>0,"both labels");
  const witness=real("100");ck(witness.steps[0]===1&&witness.steps[1]===-1,"real revisit");
  return {revision:REV,seed:SEED,checks:counts.checks,failures:0,valid_sources:counts.valid,guesses:counts.guesses,failed_guesses:counts.fail,verified_guesses:counts.accepted,public_schedule_queries:counts.H,physical_intra_block_checks:counts.physicalChecked,revisited_work_reads:counts.nonlinearReads,source_labels:{zero:counts.labels0,one:counts.labels1},max_simultaneous_full_blocks:counts.maxLive,malformed:counts.malformed,revisit_source:"100",time_formula:"T=(N+5)*(bitlength(N)+2)+1",space_scope:"frontier model counts at most five b-cell buffers, not native runtime RSS",limitations:["finite special-machine macrostep verification","no full native transition compiler","no generic Cook-Mertz evaluator or P/NP claim"]};
}
console.log(JSON.stringify(runAudit(),null,2));
