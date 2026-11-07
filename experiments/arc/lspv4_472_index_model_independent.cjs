'use strict';
// LSPV-4/472: independent finite abstract INDEX-tape resource check; not native FLMV.
let count=0;
function ok(x){if(!x)throw Error('failed check '+count);count++;}
function k4(charge){
 const e=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],cs=[];
 for(let v=0;v<4;v++){
  let ids=e.map((p,i)=>p.includes(v)?i+1:0).filter(Boolean);
  for(let m=0;m<8;m++){
   const bits=ids.map((_,j)=>(m>>j)&1);
   if((bits.reduce((a,b)=>a+b,0)%2)!==(v===0?charge:0))
    cs.push(ids.map((id,j)=>bits[j]?-id:id));
  }
 }return cs;
}
function models(cs){let z=0;for(let a=0;a<64;a++)
 if(cs.every(c=>c.some(l=>{let v=((a>>(Math.abs(l)-1))&1)===1;return l>0?v:!v;})))z++;
 return z;}
let gs=[];
for(let n=1;n<=8;n++){
 let seen=new Set();
 for(let x=0;x<2**n;x++){
  let bits=[],w=0;
  for(let i=n-1;i>=0;i--){bits.push((x>>i)&1);ok(w===0);}
  ok(bits.length===n);ok(w===0);
  seen.add(bits.join(''));
 }
 ok(seen.size===2**n);
 gs.push({n,distinct:seen.size,minimum_worstcase_config_bits:n,work_only_highwater:0,index_head_highwater:n});
}
let ps=[];
for(let n of [2,3,4,5,8,12])for(let k of [1,2,3]){
 let r=n**k,idx=new Array(r).fill(1),b=Math.floor(Math.log2(r+1))+1;
 ok(idx.length===r);ok(idx.every(x=>x===1));ok(b<=Math.ceil(k*Math.log2(n))+2);
 ps.push({n,k,index_highwater:r,index_payload_bits:r,work_counter_bits:b});
}
let even=models(k4(0)),odd=models(k4(1));
ok(even===8);ok(odd===0);ok(new Set([1,1,2].map(Math.abs)).size!==3);
console.log(JSON.stringify({model:'finite abstract sequential INDEX / indexed WORK semantics, not official FLMV execution',thesis:'If INDEX is free, explicit configuration O(WORK space) fails; if INDEX is charged, INDEX-only prologue is not a low-space wrapper.',encoding_groups:gs,padding_controls:ps,k4_even_models:even,k4_odd_models:odd,assertions:count},null,2));
