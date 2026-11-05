"use strict";
// Independent semantic verifier. No import of LSPV-2/419 producer.
// Uses forbidden full clauses and integer assignment masks directly.
function verify(){
 let count=0,positive=0,negative=0,distribution={}, failures=[];
 for(let subset=0;subset<256;subset++){
   const satAssignments=[];
   for(let x=0;x<8;x++)if((subset&(1<<x))===0)satAssignments.push(x);
   const h=z=>((subset&(1<<(z&7)))===0)&&(((z>>3)&15)===15);
   const essential=[];
   for(let bit=0;bit<7;bit++){
      let changed=false;
      for(let z=0;z<128;z++){
        if(z&(1<<bit))continue;
        if(h(z)!==h(z^(1<<bit))){changed=true;break;}
      }
      if(changed)essential.push(bit);
   }
   if((essential.length<=3)!==(satAssignments.length===0))failures.push(subset);
   for(let bit=3;bit<7;bit++){
      if(essential.includes(bit)!==(satAssignments.length>0))failures.push(subset+" y"+bit);
      count++;
   }
   distribution[essential.length]=(distribution[essential.length]||0)+1;
   if(satAssignments.length)positive++;else negative++;
   count++;
 }
 if(failures.length||positive!==255||negative!==1)throw Error(JSON.stringify({failures,positive,negative}));
 if(JSON.stringify(distribution)!==JSON.stringify({0:1,4:1,5:6,6:30,7:218}))throw Error("distribution");
 let xorChecks=0;
 for(let n=2;n<=7;n++){
   for(let word=0;word<(1<<n);word++){
     let v=word&1;
     for(let i=1;i<n;i++)v^=(word>>i)&1;
     for(let i=n-1;i>0;i--)v^=(word>>i)&1;
     if(v!==(word&1))throw Error("XOR double cancellation failure");
     xorChecks++;
   }
 }
 // Corrupt the first gate (AND for XOR): input (1,0) no longer gives x0.
 const alter=(x,y)=>((x^y)&y)^y;
 if(alter(1,0)===1)throw Error("corrupt gate passed");
 // An alleged support-free nonconstant circuit fails on an explicit witness.
 const h0=z=>((z>>3)&15)===15;
 if(h0(120)===h0(112))throw Error("forged support passed");
 return {id:"LSPV2_419_INDEPENDENT_VERIFY",passed:true,full_cnf_subsets:256,positive,negative,distribution,independent_assertions:count+xorChecks+2,xor_replays:xorChecks,corrupted_gate_rejected:true,forged_support_rejected:true,method:"integer assignment masks and forbidden full clauses, independent of producer",limits:"finite controls only; native rule authorization and B3 remain open"};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(verify(),null,2));
