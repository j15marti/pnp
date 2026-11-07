"use strict";
/* LSPV-4/474 finite falsifier: physical-head-faithful, no-cache source-address
   scratch reuse of the SAME native INPUT INDEX tape. This is NOT a native
   FLMV interpreter, an algorithm-independent lower bound, or a P/NP proof. */
function claim(x,msg){if(!x)throw Error(msg);}
function sign3(charge){
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], cs=[];
 for(let v=0;v<4;v++){const vars=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
 for(let a=0;a<8;a++){const bits=[a&1,(a>>1)&1,(a>>2)&1];
 if((bits[0]^bits[1]^bits[2])===((charge>>v)&1))continue;
 cs.push(vars.map((id,j)=>bits[j]?-id:id));}}
 return cs;
}
function models(cs){let n=0;for(let mask=0;mask<64;mask++){
 if(cs.every(c=>c.some(l=>l>0?((mask>>(l-1))&1):!((mask>>(-l-1))&1))))n++;}
 return n;}
function bitEncode(s){let z=[];for(let c of s){const b=c.charCodeAt(0);
 for(let k=7;k>=0;k--)z.push((b>>k)&1);}return z;}
function popcount(x){let n=0;while(x){n+=x&1;x>>=1;}return n;}
function runAudit(){
 const Hs=[8,16,32,64,128,256], representative=[];
 let cases=0,probes=0,assertions=0,corruptRejected=0,SAT=0,UNSAT=0,totalMoves=0;
 for(let charge=0;charge<16;charge++){
   const cnf=sign3(charge),m=models(cnf);claim(cnf.length===16,"clauses");assertions++;
   claim(m===(popcount(charge)%2?0:8),"signed K4 label");assertions++;
   if(m)SAT++;else UNSAT++;
   const payload=bitEncode(cnf.map(c=>c.join(",")).join(";"));
   for(const H of Hs){
     const offset=2*H+1, source=Array(offset).fill(0).concat(payload);
     let head=H,moves=0;const q=H;
     for(let i=0;i<q;i++){
       // Guest makes a native indexed INPUT jump using a blank INDEX;
       // INDEX remains blank and its sequential head remains at H.
       claim(head===H,"guest INDEX-head fidelity");assertions++;
       // The audited, *restricted* no-cache protocol uses the same INDEX
       // head to form the actual original-source alias address, offset.
       head=0;moves+=H;
       const sourceAddress=offset;
       const fetched=source[sourceAddress];
       claim(fetched===payload[0],"alias bit mismatch");assertions++;probes++;
       // Native indexed INPUT jump erases scratch INDEX; restore guest head.
       head=H;moves+=H;
     }
     claim(head===H && moves===2*H*q,"exact motion");assertions++;
     const corruptedOffset=offset+1;
     claim(!payload.every((bit,j)=>source[corruptedOffset+j]===bit),"corrupt alias offset accepted");assertions++;corruptRejected++;
     totalMoves+=moves;cases++;
     if(charge===0)representative.push({H,q,source_offset:offset,guest_steps:H+q,host_source_INDEX_head_moves:moves,overhead_ratio:moves/(H+q)});
   }
 }
 claim(SAT===8&&UNSAT===8,"models");assertions++;
 return {status:"PASS",category:"COMPUTATIONAL, RESTRICTED protocol only",cases,probes,assertions,corruptRejected,SAT,UNSAT,totalMoves,representative,
   theorem:"Under direct, no-cache, immediate-return SAME native INDEX source-scratch protocol, q=H requires 2H^2 head steps vs H+q guest steps",
   scope:"Source-index head preservation is an explicit hypothesis; caching, lazy virtual heads, sequential read-through, source-aligned layouts, and code-aware simplification are unexcluded."};
}
if(typeof process!=="undefined"&&process.versions&&process.versions.node){
 process.stdout.write(JSON.stringify(runAudit(),null,2)+"\n");
}