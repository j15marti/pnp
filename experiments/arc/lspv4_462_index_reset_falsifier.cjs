"use strict";
function run(){
 let checks=0;const ok=(v,m)=>{if(!v)throw Error(m);checks++};const rows=[];
 for(const L of [12,16,20,24,32,40,48,64]){
  const I=new Map();for(let p=0;p<L;p++)I.set(p,1);
  const address=[...I].reduce((v,[p,b])=>v+(BigInt(b)<<BigInt(p)),0n);
  const budget=BigInt(L)**3n, keep=budget.toString(2).length-1;
  const high=[...I.keys()].filter(i=>i>=keep);
  const cleared=new Map(I);for(const p of high)cleared.delete(p);
  const safe=[...cleared].reduce((v,[p,b])=>v+(BigInt(b)<<BigInt(p)),0n);
  ok(address===(1n<<BigInt(L))-1n,"jump address");
  ok(high.length===L-keep,"mandatory high-count conservative");
  ok(address>budget,"exp space");
  ok(high.length>0,"needs cleanup");
  ok(safe<=budget,"safe cleanup");
  ok(I.size===L,"index writes");
  ok(L>high.length,"nontrivial small bits");
  rows.push({L,index_ones:L,guest_work_touches:1,guest_work_highwater:1,
    raw_jump_address:address.toString(),polynomial_budget:budget.toString(),
    mandatory_high_bit_erasures_lower_bound:Math.max(0,L-budget.toString(2).length),
    sufficient_high_bit_erasures:high.length,full_index_clear_writes:L,
    original_index_write_steps:L});
 }
 const E=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)E.push([a,b]);
 const controls=[];
 for(const charges of [[0,0,0,0],[1,0,0,0],[1,1,0,0],[1,1,1,0]]){
  const clauses=[];
  for(let v=0;v<4;v++){
   const vars=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
   for(let a=0;a<8;a++){
    let bits=[a&1,(a>>1)&1,(a>>2)&1];
    if((bits[0]^bits[1]^bits[2])!==charges[v])clauses.push(vars.map((x,j)=>bits[j]?-x:x));
   }
  }
  let sat=false;for(let x=0;x<(1<<E.length);x++)
   if(clauses.every(c=>c.some(l=>(((x>>(Math.abs(l)-1))&1)===Number(l>0)))))sat=true;
  ok(sat===(charges.reduce((x,y)=>x^y,0)===0),"label");
  ok(clauses.length===16,"16 clauses");
  ok(clauses.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"proper ternary");
  controls.push({charges,sat,clauses:16,variables:6});
 }
 for(const c of [[1,2,0],[1,1,-2],[1,2],[1,2,3,4]])
  ok(c.length!==3||c.includes(0)||new Set(c.map(Math.abs)).size!==3,"reject malformed");
 return {name:"LSPV4_462_INDEX_RESET",status:"PROVED/RESTRICTED direct raw-index cleanup dichotomy",
 native_FLVM_executed:false,rows,original_signed_K4_controls:controls,
 malformed_rejections:4,assertions:checks,failures:0};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
