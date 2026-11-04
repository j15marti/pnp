// LSPV-1 Result 375, deterministic bit-level affine identity and both-label controls.
// No dependencies, no randomization; run: node experiments/arc/lspv1_375_affine_rows.js
function parity(x) {let r=0;while(x){r^=1;x&=x-1;}return r;}
function ensure(v,msg){if(!v)throw new Error(msg);}
function run() {
  let pairs=0,assignments=0,invariantChecks=0,corruptRejected=0;
  for(let v=1;v<=7;v++){const t=1<<v;
    for(let a=0;a<t;a++)for(let b=0;b<t;b++){
      pairs++;
      for(let x=0;x<t;x++){
        ensure((parity(a&x)^parity(b&x))===parity((a^b)&x),'XOR step unsound');
        invariantChecks++;assignments++;
      }
    }
  }
  // K4 source uses edges 01,02,03,12,13,23 and prescribed degree-three parities.
  const incidence=[[0,1,2],[0,3,4],[1,3,5],[2,4,5]];
  function models(charge){let count=0;
    for(let x=0;x<64;x++){
      let valid=true;
      for(let i=0;i<4;i++) {
        let parityValue=0;
        for(const e of incidence[i])parityValue^=(x>>e)&1;
        if(parityValue!==charge[i]){valid=false;break;}
      }
      if(valid)count++;
    }
    return count;
  }
  const odd=[1,0,0,0],even=[0,0,0,0];
  ensure(models(odd)===0,'odd label');ensure(models(even)===8,'even label');
  // For every false affine identity, changing one of the two summand masks 
  // while keeping the declared XOR result fixed is detected by some assignment.
  for(let v=1;v<=6;v++){
    const t=1<<v;
    for(let a=0;a<t;a++)for(let b=0;b<t;b++)for(let bit=0;bit<v;bit++){
      const falseResult=(a^b)^(1<<bit);
      let found=false;
      for(let x=0;x<t;x++)if((parity(a&x)^parity(b&x))!==parity(falseResult&x)){found=true;break;}
      ensure(found,'corrupt mask was not detected');corruptRejected++;
    }
  }
  return {report:"AFFINE_ROW_ER2_SIMULATION375",scope:"finite Boolean identities, not full ER2 compiler",
    v_max:7,mask_pairs:pairs,affine_identity_assignments:assignments,
    invalid_declared_results_rejected:corruptRejected,odd_k4_models:models(odd),
    even_k4_models:models(even),random_seed:null,status:"COMPUTATIONAL"};
}
const data=run();
if(typeof module!=='undefined'&&module.exports)module.exports={run};
if(typeof console!=='undefined')console.log(JSON.stringify(data,null,2));
