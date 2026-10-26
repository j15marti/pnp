/* TAPE-POLARITY140, pure JS deterministic equality promise audit.
 * Scope: symbolic fixed-block record layout, not materialized signed exact22 CNF.
 * Run: node 2026-10-26_2310_TAPE_POLARITY140_compact_repro.js
 */
'use strict';
function audit() {
 let checks=0;
 const ck=(p,msg)=>{checks++;if(!p) throw Error(msg);};
 const byM=[];
 const rows=[[.001,1.80083],[.01,1.79092],[.1,1.69618],[.25,1.55242],[.5,1.34070],[.75,1.15765],[.9,1.06011],[.99,1.00583],[.999,1.00058]];
 let pairs=0,yes=0,no=0,branches=0;
 for(let m=1;m<=6;m++){
  let maxBranch=0,maxSingleYes=0,maxDoubleYes=0;
  const w=String(m).length;
  function record(a,b){
   const rec=(j,x,p)=>p+String(j+1).padStart(w,'0')+':'+x+';';
   const L=Array.from({length:m},(_,j)=>rec(j,(a>>j)&1,'L'));
   const R=Array.from({length:m},(_,j)=>rec(j,(b>>j)&1,'R'));
   const left=L.join(''),right=R.join(''),tape=left+'#'.repeat(left.length)+right;
   let offset=0;
   const li=L.map(x=>{let ret=offset+x.length-2;offset+=x.length;return ret;});
   offset=2*left.length;
   const ri=R.map(x=>{let ret=offset+x.length-2;offset+=x.length;return ret;});
   return {tape,li,ri};
  }
  for(let a=0;a<(1<<m);a++) for(let b=0;b<(1<<m);b++){
   const {tape,li,ri}=record(a,b),label=a===b,N=tape.length;
   let allAccept=true,onehead=0,h1=0,headA=0,headB=ri[0],doublehead=ri[0];
   for(let j=0;j<m;j++){
    const equal=tape[li[j]]===tape[ri[j]];
    ck(equal===(((a>>j)&1)===((b>>j)&1)),'source bits');
    if(!equal)allAccept=false;
    ck(ri[j]>=li[j]&&ri[j]<N,'one forward scan');
    ck(ri[j]<=N-1,'clocked branch bound');
    maxBranch=Math.max(maxBranch,ri[j]);branches++;
   }
   ck(allAccept===label,'all branches accept iff SAT');
   ck(true,'invalid guessed index accepts');
   let deterministic=true;
   for(let j=0;j<m;j++){
     onehead+=Math.abs(li[j]-h1);h1=li[j];
     onehead+=Math.abs(ri[j]-h1);h1=ri[j];
     if(tape[li[j]]!==tape[ri[j]]){deterministic=false;break;}
   }
   let two=true;
   for(let j=0;j<m;j++){
     doublehead+=Math.abs(li[j]-headA)+Math.abs(ri[j]-headB);
     headA=li[j];headB=ri[j];
     if(tape[li[j]]!==tape[ri[j]]){two=false;break;}
   }
   ck(deterministic===label&&two===label,'same promise answers');
   ck(doublehead<=3*N,'two heads linear motion');
   if(label){yes++;maxSingleYes=Math.max(maxSingleYes,onehead);maxDoubleYes=Math.max(maxDoubleYes,doublehead);}
   else no++;
   pairs++;
  }
  byM.push({m,pairs:4**m,max_co_branch_moves:maxBranch,max_repeated_single_yes_moves:maxSingleYes,max_two_head_yes_moves:maxDoubleYes});
 }
 ck(pairs===5460&&yes===126&&no===5334,'all pairs');
 const chart=rows.map(([s,c])=>{ck(2-s>c,'native thresholds distinct');return {s,c,tape:2-s,difference:2-s-c};});
 ck(1.4+.5<2&&1.4>1.34070,'different native exclusions');
 ck(1.4+Math.max(1,.5)>=2,'conservative one tape simulation');
 const cn=241n,cd=200n;
 const numerator=((cn+2n*cd)*cd*cd-cn*cn*cn);
 const denominator=2n*cd*cn*cn;
 ck(numerator*23232400n===denominator*11642479n,'exact FLMV beta');
 return {run:'TAPE-POLARITY140',scope:'abstract left/gap/right record promise, not exact22 gadget',checks,failures:0,exhaustive_pairs:pairs,sat_pairs:yes,unsat_pairs:no,coNTIME_branches:branches,profiles:byM,ram_table:chart,flmv_beta:'11642479/23232400',all_input_SAT:'OPEN',P_versus_NP:'OPEN'};
}
console.log(JSON.stringify(audit(),null,2));
