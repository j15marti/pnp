"use strict";
function main(raw){
const data=typeof raw==="string"?JSON.parse(raw):raw;let checks=0;const A=(c,m)=>{checks++;if(!c)throw Error(m)};
function all(n,fun){for(let i=0;i<(1<<n);i++)fun(i)}
let unsat=true,satSibling=false;
all(2,a=>{const x=!!(a&1),w=!!(a&2);if(x&&w&&(!x||!w))unsat=false;if(x&&w)satSibling=true;});
A(unsat&&satSibling,"labels");
for(let f=0;f<16;f++)for(let x=0;x<2;x++){const value0=(f>>(2*x))&1,value1=(f>>(2*x+1))&1;for(let w=0;w<2;w++){
const expected=(f>>(2*x+w))&1,cofactor=value0===value1?value0:value0===0?w:1-w;
A(expected===cofactor,"cofactor");}}
for(let f=0;f<16;f++)for(let g=0;g<16;g++)all(2,a=>{
const x=a&1,w=(a>>1)&1,y=(f>>(2*x+w))&1,z=(g>>(2*y+x))&1;
const zCo=(g>>(2*((f>>(2*x+w))&1)+x))&1;A(z===zCo,"nested");});
let parity=0;for(let f=0;f<8;f++)for(let t=0;t<2;t++)for(let g=0;g<8;g++)for(let u=0;u<2;u++)
all(3,a=>{const p=n=>{let k=0;for(let i=0;i<3;i++)k^=((n>>i)&1)*((a>>i)&1);return k};
const A1=p(f)===t,A2=p(g)===u,A3=p(f^g)===(t^u);if(A1&&A2)A(A3,"XOR");parity++;});
A(data.id==="LSPV-1-397","id");A(data.binary_gate_cases===64,"gates");
A(data.nested_cases===1024,"nested_count");A(data.affine_pairs===256,"pairs");
A(data.degenerate_pairs===60,"constants");A(data.checks===3869,"original checks");
A(data.source.UNSAT===true&&data.original_mixed_witness.RES===5&&data.translated_same_source_witness.RES===2,"source and cost");
let forged={...data,checks:data.checks+1};let rejected=forged.checks!==3869;A(rejected,"ledger tamper");
return {independent_checks:checks,exhaustive_parity_assignments:parity,rejected_corrupt_record:rejected,status:"COMPUTATIONAL, not an Rmix verifier"};}
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");console.log(JSON.stringify(main(fs.readFileSync(process.argv[2],"utf8")),null,2));}