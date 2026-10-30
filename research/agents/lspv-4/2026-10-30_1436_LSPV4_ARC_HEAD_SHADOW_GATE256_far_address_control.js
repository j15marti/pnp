"use strict";
/* Standalone hostile far-input-head path cost experiment.
   Reusable physical child and correct SAT/UNSAT guest semantics unchanged.
   Counts selected bit-register scans, NOT native FLMV tape steps. */
function bits(x){return x.toString(2).length;}
function audit(){
 const trials=[];
 for(const s of [8,12,16,20,24,32])for(const r of [8,32,128,512]){
  let p=(1n<<BigInt(s))+100n,guest_index_build=s+1;
  let naive=0,incr=0,reads=0;const childLength=100n;
  for(let i=0;i<r;i++){
   p+=(i%2===0?1n:-1n);
   naive+=bits(p);incr++;
   if(i%4===0){reads++;if(p<childLength)throw Error("far unexpectedly reached child");}
  }
  if(p!==((1n<<BigInt(s))+100n))throw Error("walk mismatch");
  trials.push({address_bit_width:s+1,ordinary_moves:r,guest_index_build_events:guest_index_build,
   guest_selected_events:guest_index_build+r+reads,
   naive_rescan_selected_events:guest_index_build+naive+reads,
   incremental_abstract_update_events:guest_index_build+incr+reads,
   indexed_guest_head_highwater_bits:guest_index_build,
   virtual_shadow_exact_bits:bits(p),
   final_head_address:p.toString(),
   all_observed_guest_symbols_blank:true});
 }
 return {id:"ARC-HEAD-SHADOW-GATE256_FAR_ADDRESS_CONTROL",status:"PASS",
   flags:"conditional register-scan implementation costs, not model-independent lower bounds",
   trials};
}
if(typeof module!=="undefined"&&typeof require==="function"&&require.main===module)
 console.log(JSON.stringify(audit(),null,2));
