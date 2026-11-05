// LSPV-4/404 independent exhaustive truth-table oracle: all f/g 3-input functions
"use strict";
function verify(){
 let count=0,valid=0,invalid=0;
 const tests=[[4],[-4],[5],[-5],[4,5],[4,-5],[-4,5],[-4,-5],[4,-4],[5,-5],[1,4],[2,5],[-3,-5],[1,2,-4],[1,-1,4],[2,3,5]];
 function val(l,s,w,g){let x=Math.abs(l),v=x===4?w:x===5?((g>>s)&1):((s>>(x-1))&1);return l<0?!v:!!v}
 for(let f=0;f<256;f++)for(let g=0;g<256;g++)for(const C of tests){
  let full=true,small=true;
  for(let s=0;s<8;s++){if(!((f>>s)&1))continue;
   for(let w=0;w<=1;w++)if(!C.some(l=>val(l,s,w,g)))full=false;
   if(C.includes(4)&&C.includes(-4))continue;
   if(!C.filter(l=>Math.abs(l)!==4).some(l=>val(l,s,0,g)))small=false;
  }
  if(full!==small)throw Error("mismatch "+JSON.stringify({f,g,C,full,small}));
  count++;valid+=full?1:0;invalid+=full?0:1;
 }
 return {status:"PASS",function_pairs:65536,clauses_per_pair:16,checks:count,valid,invalid};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(verify(),null,2));
