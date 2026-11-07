'use strict';
/* LSPV-4/477 published independent combinatorial theorem control. For complete 
  original-source parser, 64 brute-force cases, and 120 witness controls see the
  separately linked reproducibility archive. No native FLMV is executed. */
const assert=require('node:assert/strict');
let checks=0;
function check(a){assert(a);checks++;}
function parity(v){return ((v^(v>>1)^(v>>2))&1);}
function spectrum(mask){let z=0;for(let t=0;t<8;t++)
 if(((mask>>>t)&1)===0)z|=1<<parity(t);return z;}
function popcnt(v){let c=0;while(v){v&=v-1;c++;}return c;}
const forb=[0,0];
for(let t=0;t<8;t++)forb[parity(t)]|=1<<t;
check(popcnt(forb[0])===4 && popcnt(forb[1])===4);
let legal=0, exceptional=0, parityPackets=0;
for(let mask=0;mask<256;mask++){
 if(popcnt(mask)>4)continue;
 legal++;
 const p=spectrum(mask);
 check(p!==0);
 if(mask===forb[0]||mask===forb[1]){
  parityPackets++;check(popcnt(mask)===4 && (p===1||p===2));
 }else{exceptional++;check(p===3);}
}
check(legal===163);check(exceptional===161);check(parityPackets===2);
// Original binary clauses directly, one width-three clause excludes one triple.
for(let x=0;x<8;x++){
 const lits=[0,1,2].map(j=>((x>>>j)&1)?-(j+1):j+1);
 for(let a=0;a<8;a++){
  const sat=lits.some(l=>l>0?((a>>>(l-1))&1)===1:((a>>>(-l-1))&1)===0);
  check(sat===(a!==x));
 }
}
console.log(JSON.stringify({role:'LSPV-4',run:477,
 status:'COMPUTATIONAL/finite theorem-control',
 packet_masks_popcount_at_most_4:legal,exceptional_masks:exceptional,
 parity_packet_masks:parityPackets,checks,errors:0,
 native_FLMV_executed:false,p_vs_np:'OPEN'},null,2));
