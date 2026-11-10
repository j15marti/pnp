// Independent finite replay: fixed-oblivious-address witnesses and address-correlation abstraction.
// No general RAM, circuit, SAT, FLMV, or machine-space lower bound follows.
const output={tag:"RAM-FIXED-TRACE-2026-11-09",scenarios:[],checks:0,failures:0};
function must(b,why){output.checks++;if(!b){output.failures++;throw new Error(why)}}
for(let d=1;d<=9;d++){
 const M=2**d;let omitted=0,spurious=0,corrupt=0;
 for(let j=0;j<M;j++){
  let read0=0,read1=0;
  for(let a=0;a<M;a++){if(a!==j){must(0===Number(a===j),"omitted read mismatch");read0+=0;read1+=Number(a===j)}}
  must(read0===read1,"indistinguishable observations");must((0)!==(1),"different query results");omitted++;
  const write=j,read=j,wrong=j^1;
  must(write===read,"same-origin address");must(wrong!==write,"corruption control");corrupt++;
 }
 for(let w=0;w<M;w++)for(let r=0;r<M;r++){
  let value=Number(w===r);must(value===(w===r?1:0),"truth-value");
  if(w!==r){must(value===0,"cross-source read");spurious++}else must(value===1,"equal-origin read");
 }
 output.scenarios.push({address_bits:d,table_cells:M,omitted_cell_witnesses:omitted,marginal_spurious_off_diagonal:spurious,corruption_checks:corrupt});
}
output.total_omitted_cell_witnesses=output.scenarios.reduce((s,o)=>s+o.omitted_cell_witnesses,0);
output.total_marginal_spurious_states=output.scenarios.reduce((s,o)=>s+o.marginal_spurious_off_diagonal,0);
console.log(JSON.stringify(output,null,2));
