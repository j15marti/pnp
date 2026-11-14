"use strict";
// TMR-1 EI5 hybrid erasing INDEX + native sequential moves. Full original 3-CNF source audit.
// Does not instruction-simulate the fallback Turing machine.
const audit = function audit() {
 "use strict";
 const W = n => Math.max(1, Math.ceil(Math.log2(Math.max(2,n))));
 const assert = (p,m) => {stat.assertions++;if(!p){stat.failures++;throw Error(m)}};
 const stat = {id:"TMR1-EI5",model:"one erasing INDEX tape with ordinary physical +1 source-head moves; finite source-level charged emulator, not a TM",sources:0,sat:0,unsat:0,adversarial:0,original_clause_bruteforce:0,assertions:0,failures:0,read_moves:0,index_jumps:0,index_bits_written:0,maxL:0,maxChargeRatio:0,largestN:0,samples:[]};
 function encode(n,a,b) {
   const w=W(5*n);
   let s="1".repeat(5*n)+"0"+"1".repeat(8*n)+"0";
   for(let bank=0;bank<2;bank++)for(let i=0;i<n;i++){
     const bit=(bank===0?a:b)[i],z=(bank===0?n:3*n)+2*i;
     for(let u=0;u<2;u++)for(let v=0;v<2;v++)
       s+=String(1-bit)+i.toString(2).padStart(w,"0")+u+z.toString(2).padStart(w,"0")+v+(z+1).toString(2).padStart(w,"0");
   }
   return s;
 }
 function simulate(src) {
   const width=W(src.length+2);
   let head=0, scan=0, cost=0, reads=0, localMoves=0, jumps=0, indexedBits=0;
   let n=0, w=0, g=0, h=0, anchor=0, equal=true;
   function local() {
     if(head!==scan)throw Error("uncorrected indexed jump");
     let v=head<src.length?src[head]:"#";
     reads++;cost++; // source read transition
     if(v!=="#") {
       localMoves++;cost++;head++;
       let trailing=0,t=scan;
       while(t%2===1){trailing++;t=Math.floor(t/2)}
       cost+=4*(trailing+1)+3; // paid scan-coordinate binary increment and tape-head return
       scan++;
     }
     return v;
   }
   function jump(addr) {
     if(addr<0 || addr>src.length)throw Error("out-of-range jump");
     const s=addr.toString(2);
     // Charge writing exactly the address bits on the index tape with an ordinary head,
     // physical indexed jump, and destruction of the entire index content.
     indexedBits+=s.length;
     cost+=4*s.length+3;
     head=addr;jumps++;
   }
   function target(num,width) {
     const digits=num.toString(2).padStart(width,"0");
     cost+=2*width+3; // materialize candidate expected literal identifier on work tape
     for(let j=0;j<width;j++)if(local()!==digits[j])return false;
     return true;
   }
   function reject() {return {member:false,cost,reads,localMoves,jumps,indexedBits};}
   let c;
   while((c=local())==="1")n++;
   if(c!=="0" || n<5 || n%5!==0)return reject();
   const N=n;n=N/5;w=W(N);g=12*(w+1);h=13*n+2;
   for(let i=0;i<8*n;i++)if(local()!=="1")return reject();
   if(local()!=="0" || scan!==h)return reject();
   anchor=h;
   for(let bank=0;bank<2;bank++)for(let i=0;i<n;i++){
     let z=(bank===0?n:3*n)+2*i,sign=null;
     for(let u=0;u<2;u++)for(let v=0;v<2;v++){
       const q=local();
       if(q!=="0"&&q!=="1")return reject();
       if(sign===null)sign=q;
       if(q!==sign||!target(i,w)||local()!==String(u)||!target(z,w)||local()!==String(v)||!target(z+1,w))return reject();
       cost+=3*w+5; // compare verifier state, advance literal counters
     }
     if(bank===1){
       const saved=scan;
       jump(anchor); // input head travels physically by the native INDEX transition
       const first=head<src.length?src[head]:"#";reads++;cost++;
       if(first!==sign)equal=false;
       jump(saved); // INDEX is rebuilt AFTER erasure to resume sequential source scan
       if(head!==scan)throw Error("return failed");
       anchor+=g;
       cost+=5*width+5; // charged binary stride update, counter bookkeeping
     }
   }
   if(local()!=="#")return reject();
   return {member:true,sat:equal,n,L:src.length,cost,reads,localMoves,jumps,indexedBits};
 }
 function semanticBruteforce(n,s) {
   const w=W(5*n),header=13*n+2,record=3*(w+1);
   const clauses=[];
   for(let k=0;k<8*n;k++){
     let clause=[];
     for(let j=0;j<3;j++){
       let t=s.slice(header+k*record+j*(w+1),header+k*record+(j+1)*(w+1));
       clause.push([Number.parseInt(t.slice(1),2),t[0]==="1"]);
     }
     clauses.push(clause);
   }
   for(let mask=0;mask<2**(5*n);mask++){
     if(clauses.every(c=>c.some(([i,neg])=>(((mask>>i)&1)===1)!==neg)))return true;
   }
   return false;
 }
 function test(n,a,b){
   const src=encode(n,a,b),r=simulate(src),want=a.every((v,i)=>v===b[i]);
   assert(r.member && r.sat===want,"wrong classification");
   assert(r.jumps===2*n,"not exactly two index jumps per comparison");
   assert(r.localMoves===src.length,"did not locally traverse every original source bit");
   assert(r.reads===src.length+1+n,"not all source reads charged");
   assert(r.indexedBits<=2*n*W(src.length+2),"address-write bound");
   assert(r.cost<=120*(src.length+1),"O(L) finite charged witness");
   if(n<=2){assert(semanticBruteforce(n,src)===want,"original CNF brute-force disagreement");stat.original_clause_bruteforce++}
   stat.sources++;stat[want?"sat":"unsat"]++;
   stat.read_moves+=r.localMoves;stat.index_jumps+=r.jumps;
   stat.index_bits_written+=r.indexedBits;
   stat.maxL=Math.max(stat.maxL,src.length);stat.largestN=Math.max(stat.largestN,n);
   stat.maxChargeRatio=Math.max(stat.maxChargeRatio,r.cost/src.length);
   if(n===1 || n>=128 && want && a.every(x=>x===0))stat.samples.push({n,L:src.length,cost:r.cost,ratio:Number((r.cost/src.length).toFixed(3)),jumps:r.jumps});
   const corrupt=[
     src.slice(0,-1),src+"0",src.slice(1),
     src.slice(0,13*n+2)+"2"+src.slice(13*n+3),
     src.slice(0,13*n+2+(1+w(n))) // replaced below
   ];
   function w(n){return W(5*n)}
   corrupt.pop();
   const pos=13*n+2+1+W(5*n);
   corrupt.push(src.slice(0,pos)+(src[pos]==="0"?"1":"0")+src.slice(pos+1));
   for(const bad of corrupt){assert(!simulate(bad).member,"bad source accepted as family");stat.adversarial++}
 }
 for(let n=1;n<=4;n++)for(let i=0;i<(1<<n);i++)for(let j=0;j<(1<<n);j++)
   test(n,Array.from({length:n},(_,k)=>(i>>k)&1),Array.from({length:n},(_,k)=>(j>>k)&1));
 let seed=2166136261;
 function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>27)&1}
 for(const n of [8,16,32,64,128,256,512,1024])for(let t=0;t<8;t++){
   let a=Array.from({length:n},rnd),b=t%4===0?a.slice():Array.from({length:n},rnd);
   test(n,a,b);
 }
 for(const n of [2048,4096])test(n,Array(n).fill(0),Array(n).fill(0));
 stat.maxChargeRatio=Number(stat.maxChargeRatio.toFixed(4));
 return stat;
};
if(typeof require!=="undefined" && require.main===module) process.stdout.write(JSON.stringify(audit(),null,2)+"\n");
if(typeof module!=="undefined") module.exports={audit};
