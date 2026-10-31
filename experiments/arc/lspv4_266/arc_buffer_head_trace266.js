"use strict";
/* Exact finite hostile wrapper trace for LSPV-4 ARC-QUIESCENT-DFS-LEDGER266.
 * Moves only a single sequential buffer head; an FLMV guest instead writes
 * charged O(log m)-bit input indices. Dummy reads do not affect SAT answers. */
function trace(length,reads=length){
  let pos=0,moves=0,operations=[];
  for(let i=0;i<reads;i++){
    const t=(i%2)?length-1:0;
    moves+=Math.abs(t-pos);pos=t;
    if(i<8)operations.push({i,address:t,cumulative_sequential_steps:moves});
  }
  let address_width=Math.ceil(Math.log2(length+1));
  return {physical_child_bytes:length,read_count:reads,guest_index_address_width:address_width,
   guest_index_bit_writes:reads*address_width,guest_read_transitions:reads,
   sequential_head_moves:moves,trace_first_eight:operations,
   slowdown_head_moves_over_address_writes:moves/(reads*address_width)};
}
function run(R){
  return {id:"ARC-QUIESCENT-DFS-LEDGER266-HEAD-TRACE",source_raw:"results/raw/arc/2026-10-31_0039_LSPV4_ARC_QUIESCENT_DFS_LEDGER266_raw.json",
   physical_model:"single sequential read/write child-buffer head, NOT an indexed work RAM",
   cases:R.cases.map(c=>({name:c.name,original_sat:c.original_sat,children:c.serial.child_log.map(ch=>({pin:ch.pin_x1,child_sat:ch.sat,...trace(ch.physical_child_bytes)}))})),
   theorem_scope:"deterministic index-based label-preserving dummy read wrapper: Omega(q*m) sequential head moves, O(q*log m) guest index-bit writes; source scans/guest A after the reads are extra"};
}
if(typeof require!=="undefined" && require.main===module){let fs=require("fs");let R=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));console.log(JSON.stringify(run(R),null,2));}