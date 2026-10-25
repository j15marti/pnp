#!/usr/bin/env node
"use strict";
/* ARC-EPOCH-TAPES173: deterministic source-level controls and symbolic tape
   counters. Not a physical FLMV-TM instruction profiler. */
function audit() {
 let checks=0, sourceBits=0, guestCalls=0, satRoots=0, unsatRoots=0;
 const assert=(b,msg)=>{checks++;if(!b)throw Error("check "+checks+": "+msg);};
 const enc=(n,cs)=>"p cnf "+n+" "+cs.length+"\n"+cs.map(c=>c.join(" ")+" 0\n").join("");
 function dec(str) {
   const lines=str.trimEnd().split("\n"),h=lines.shift().split(" ");
   if(h.length!==4||h[0]!=="p"||h[1]!=="cnf")throw Error("bad header");
   const n=Number(h[2]),m=Number(h[3]);
   if(!Number.isInteger(n)||n<1||!Number.isInteger(m)||m<0||lines.length!==m)throw Error("bad counts");
   const cs=lines.map(line=>{
     if(!/^-?\d+( -?\d+)*$/.test(line))throw Error("bad line");
     const nums=line.split(" ").map(Number);
     if(nums.at(-1)!==0||nums.slice(0,-1).some(x=>x===0||Math.abs(x)>n))throw Error("bad literal");
     return nums.slice(0,-1);
   });
   return {n,cs};
 }
 const restrict=(cs,k,b)=>cs.filter(c=>!c.some(l=>Math.abs(l)===k&&(l>0)===b))
    .map(c=>c.filter(l=>Math.abs(l)!==k));
 function brute(cs,n) {
   for(let mask=0;mask<2**n;mask++){
     if(cs.every(c=>c.some(l=>(((mask>>(Math.abs(l)-1))&1)===1)===(l>0))))return true;
   }
   return false;
 }
 function dpll(cs,n) {
   function go(a){
     for(;;){
       let change=false,pivot=0;
       for(const c of cs){
         let yes=false,count=0,last=0;
         for(const l of c){
           const v=a[Math.abs(l)];
           if(v<0){count++;last=l;}
           else if((v===1)===(l>0)){yes=true;break;}
         }
         if(yes)continue;
         if(!count)return false;
         if(count===1){
           const k=Math.abs(last),v=last>0?1:0;
           if(a[k]>=0&&a[k]!==v)return false;
           if(a[k]<0){a[k]=v;change=true;}
         } else if(!pivot)pivot=Math.abs(last);
       }
       if(change)continue;
       if(!pivot)return true;
       const b=a.slice();b[pivot]=0;
       if(go(b))return true;
       a[pivot]=1;return go(a);
     }
   }
   return go(Array(n+1).fill(-1));
 }
 class Tape {
   constructor(w){this.w=w;this.epoch=0;this.mem=new Map();this.extent=0;
     this.readBits=0;this.writeBits=0;this.unchanged=0;this.flips=0;}
   start(){this.epoch++;assert(this.epoch<2**this.w,"epoch wrap");}
   touch(k){assert(Number.isSafeInteger(k)&&k>=0,"index");
     this.extent=Math.max(this.extent,(k+1)*(this.w+2));}
   get(k){this.touch(k);this.readBits+=this.w+2;
     const v=this.mem.get(k);return v&&v.epoch===this.epoch?v.value:0;}
   set(k,val){this.touch(k);const old=this.mem.get(k);
     const repr=(e,x)=>e.toString(2).padStart(this.w,"0")+x;
     const oldbits=old?repr(old.epoch,old.value):"0".repeat(this.w+1);
     const newbits=repr(this.epoch,val);let delta=0;
     for(let j=0;j<newbits.length;j++)delta+=+(oldbits[j]!==newbits[j]);
     this.flips+=delta;this.unchanged+=newbits.length-delta;
     this.writeBits+=newbits.length;this.mem.set(k,{epoch:this.epoch,value:val});}
 }
 const records=[];let first=0,grand=0,parent=0;
 for(let q=1;q<=5;q++)for(const sat of [true,false]){
   const n=3+3*q,cs=[];
   for(let b=0;b<8;b++){
     if(sat&&b===0)continue;
     cs.push([1,2,3].map((v,k)=>(b>>k)&1?v:-v));
   }
   for(let k=0;k<q;k++)cs.push([4+3*k,5+3*k,6+3*k]);
   const root=enc(n,cs),N=8*root.length,W=Math.ceil(3*Math.log2(N+2))+4;
   assert(JSON.stringify(dec(root).cs)===JSON.stringify(cs),"ordinary root roundtrip");
   const tape=new Tape(W);
   function guest(str){
     tape.start();guestCalls++;
     for(let k=1;k<=3;k++)assert(tape.get(k)===0,"fresh blank across guest calls");
     let copy="",xor=0;
     for(let i=0;i<str.length;i++){
       const v=str.charCodeAt(i);assert(v<128,"ASCII");
       let recovered=0;
       for(let j=7;j>=0;j--){
         const bit=(v>>j)&1;recovered=2*recovered+bit;xor^=bit;
         tape.set(1,xor);tape.set(2,bit);
         assert(tape.get(1)===xor&&tape.get(2)===bit,"tagged storage");
         sourceBits++;
       }
       copy+=String.fromCharCode(recovered);
     }
     assert(copy===str,"all virtual input bits regenerated");
     const actual=dec(copy);return dpll(actual.cs,actual.n);
   }
   const expected=brute(cs,n);assert(expected===sat,"independent SAT/UNSAT root");
   assert(guest(root)===expected,"charged parent guest baseline");parent++;
   const firstLabels=[];
   for(const b of [false,true]){
     const c1=restrict(cs,1,b),s1=enc(n,c1),l1=guest(s1);
     assert(l1===brute(c1,n),"first child ordinary independent label");
     first++;firstLabels.push(l1);
     const secondLabels=[];
     for(const c of [false,true]){
       const c2=restrict(c1,2,c),s2=enc(n,c2),l2=guest(s2);
       assert(l2===brute(c2,n),"grandchild ordinary independent label");
       secondLabels.push(l2);grand++;
     }
     assert(l1===secondLabels.some(Boolean),"true second-level Shannon join");
   }
   assert(expected===firstLabels.some(Boolean),"true first-level Shannon join");
   assert(tape.writeBits===tape.unchanged+tape.flips,"all writes counted");
   if(sat)satRoots++;else unsatRoots++;
   const far=Math.ceil(N**(3/4));
   assert(far>0,"hostile remote cell exists");
   records.push({q,label:sat?"SAT":"UNSAT",inputBits:N,epochWidth:W,
     actualCalls:tape.epoch,logicalCellsEverTouched:tape.mem.size,
     guestMaxTapeCoordinate:tape.extent,tagReadBits:tape.readBits,
     tagWriteBits:tape.writeBits,tagUnchangedWrites:tape.unchanged,
     tagChangedBits:tape.flips,hostileSingleRemoteReadCoordinate:far,
     hostileStoredDataBits:1,hostileIndexBits:Math.ceil(Math.log2(far+1))});
 }
 let malformed=0;
 for(const str of ["","p cnf 3 1\n1 0\n2 0\n","p cnf 3 1\n4 0\n","p cnf 3 x\n1 0\n"]){
   let bad=false;try{dec(str);}catch(e){bad=true;}
   assert(bad,"malformed ordinary encoding rejection");malformed++;
 }
 assert(brute([[1]],1)&&brute([[-1]],1)&&!brute([[1],[-1]],1),
   "independent SAT labels cannot join conjunction on common name");
 assert(parent===10&&first===20&&grand===40&&guestCalls===70,
   "two real levels and parent guest charged");
 return {run:"ARC-EPOCH-TAPES173",classification:"COMPUTATIONAL",
  caveat:"symbolic tape/bit counters, not a FLMV physical TM trace",
  sourceCases:10,SAT:satRoots,UNSAT:unsatRoots,firstChildren:first,
  secondChildren:grand,parentGuestCalls:parent,guestCalls,checks,failed:0,
  guestInputBitReads:sourceBits,malformed,seed:"none; exhaustive fixed",
  records};
}
if(typeof process!=="undefined"&&process.versions&&process.versions.node)
  console.log(JSON.stringify(audit(),null,2));