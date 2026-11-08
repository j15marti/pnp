// LSPV-2/499 independent, standalone V8/Node exact-source streaming check.
// Finite validation only; original user source is treated as read-only input.
// No native FLMV machine is claimed by this executable.
"use strict";
function run499() {
 let checks=0;
 function check(b,msg){if(!b)throw Error(msg);checks++;}
 function eq(a,b,msg){check(a===b,msg);}
 function mul(a,b,d){
   let z=0n, top=1n<<BigInt(d), f=top^(1n<<BigInt(d/2))^1n;
   for(let k=0;k<d;k++){if((b>>BigInt(k))&1n)z^=a;a<<=1n;if(a&top)a^=f;}
   return z;
 }
 function forward(k,v,d){
   let mask=(1n<<BigInt(d))-1n,a=v&mask,b=v>>BigInt(d),L=1n<<BigInt(d/2);
   let x,y;
   if(k===1){x=a^mul(L,b,d);y=mul(mul(L^1n,2n,d),a,d)^b;}
   else if(k===2){x=a^b;y=mul(2n,a,d)^b;}
   else if(k===3){x=a^mul(L^1n,b,d);y=mul(mul(L,2n,d),a,d)^b;}
   else throw Error("bad edge color");
   return x|(y<<BigInt(d));
 }
 function back(k,v,d){
   let mask=(1n<<BigInt(d))-1n,inv=(1n<<BigInt(d))-(1n<<BigInt(d/2));
   let z=forward(k,v,d);
   return mul(inv,z&mask,d)|(mul(inv,z>>BigInt(d),d)<<BigInt(d));
 }
 function params(d){
   let Q=2**(2*d)-1,H=2*Q,W=Math.ceil(Math.log2(2*H+1));
   return {d,Q,H,W,head:3*H+10,packet:12*(W+1),N:3*H+12+12*H*(W+1)};
 }
 function vertexIds(v,bit,p){
   if(v<p.Q)return [2*v+1+bit,p.H+2*v+1,p.H+2*v+2];
   let r=v-p.Q,j=[1,2,3].map(c=>Number(back(c,BigInt(r+1),p.d))-1);
   return [2*j[0]+1+bit,p.H+2*j[1]+1,p.H+2*j[2]+2];
 }
 function source(a,b,p){
   let parts=["11100011","1".repeat(p.H),"0","1".repeat(2*p.H),"0"];
   for(let v=0;v<p.H;v++){
     let j=v<p.Q?v:Number(back(1,BigInt(v-p.Q+1),p.d))-1;
     let ids=vertexIds(v,v<p.Q?a[j]:b[j],p).sort((x,y)=>x-y);
     for(let z=0;z<8;z++){
       let parity=((z>>2)&1)^((z>>1)&1)^(z&1);
       if(parity===(v===0?1:0))continue;
       for(let k=0;k<3;k++)parts.push(String((z>>(2-k))&1)+ids[k].toString(2).padStart(p.W,"0"));
     }
   }
   parts.push("10");let s=parts.join("");eq(s.length,p.N,"source length");return s;
 }
 function classify(s,p){
   let reads=0,jumps=0,packetCount=0,position=0,mismatch=false;
   const at=i=>{reads++;return s[i]},bad=()=>({label:"OUTSIDE",reads,jumps,packetCount});
   if(s.length!==p.N)return bad();
   for(let k=0;k<8;k++)if(at(position++)!=="11100011"[k])return bad();
   for(let k=0;k<p.H;k++)if(at(position++)!=="1")return bad();
   if(at(position++)!=="0")return bad();
   for(let k=0;k<2*p.H;k++)if(at(position++)!=="1")return bad();
   if(at(position++)!=="0")return bad();
   eq(position,p.head,"header boundary");
   for(let v=0;v<p.H;v++){
     let j=v<p.Q?v:Number(back(1,BigInt(v-p.Q+1),p.d))-1;
     let value=0;
     for(let w=0;w<p.W;w++){
       let c=at(position+1+w);
       if(c!=="0"&&c!=="1")return bad();
       value=2*value+(c==="1"?1:0);
     }
     let bit=value-(2*j+1);if(bit!==0&&bit!==1)return bad();
     let ids=vertexIds(v,bit,p).sort((a,b)=>a-b);
     if(new Set(ids).size!==3)return bad();
     for(let z=0;z<8;z++){
       let parity=((z>>2)&1)^((z>>1)&1)^(z&1);
       if(parity===(v===0?1:0))continue;
       for(let k=0;k<3;k++){
         if(at(position++)!==String((z>>(2-k))&1))return bad();
         for(let w=p.W-1;w>=0;w--)if(at(position++)!==String((ids[k]>>w)&1))return bad();
       }
     }
     packetCount++;
     if(v>=p.Q){
       let left=0,offset=p.head+j*p.packet+1;
       for(let w=0;w<p.W;w++){let c=at(offset+w);jumps++;if(c!=="0"&&c!=="1")return bad();left=left*2+(c==="1"?1:0);}
       if(left!==value)mismatch=true;
     }
   }
   eq(position,p.N-2,"body boundary");
   if(at(position++)!=="1"||at(position++)!=="0")return bad();
   eq(position,p.N,"source boundary");
   return {label:mismatch?"MEMBER_SAT":"MEMBER_UNSAT",reads,jumps,packetCount};
 }
 let results=[];
 for(let d of [2,6]){
   let p=params(d),samples=d===2?32:4,maxReads=0,negative=0;
   for(let j=1;j<=p.Q;j+=(d===2?1:113))for(let k=1;k<=3;k++){
     let r=forward(k,BigInt(j),d);check(r>0n&&r<=BigInt(p.Q),"neighbor range");eq(back(k,r,d),BigInt(j),"inverse");
   }
   for(let z=0;z<samples;z++){
     let a=Array.from({length:p.Q},(_,j)=>(z+3*j+j*j)%2),b=a.slice();
     if(z%2)b[(z*7)%p.Q]^=1;
     let x=source(a,b,p),r=classify(x,p);
     eq(r.label,z%2?"MEMBER_SAT":"MEMBER_UNSAT","correct label");
     eq(r.packetCount,p.H,"all packets");
     check(r.reads>=p.N,"must authenticate all bits");
     maxReads=Math.max(maxReads,r.reads);
     if(z===0){
       let sites=[0,8,p.head,Math.floor(p.N/3),Math.floor(2*p.N/3),p.N-2,p.N-1];
       for(let i=0;i<80;i++)sites.push((i*197+11)%p.N);
       for(const i of new Set(sites)){
         let y=x.slice(0,i)+(x[i]==="1"?"0":"1")+x.slice(i+1);
         eq(classify(y,p).label,"OUTSIDE","corruption");negative++;
       }
       eq(classify(x+"0",p).label,"OUTSIDE","extra bit");negative++;
       eq(classify(x.slice(1),p).label,"OUTSIDE","missing bit");negative++;
     }
   }
   results.push({d,H:p.H,N:p.N,samples,sat:samples/2,unsat:samples/2,negative,maxReads});
 }
 return {status:"PASS",checks,results,scope:"Finite n=4 and n=12 only; hosted strings/arrays are uncharged input/test-fixture storage, not an executed native FLMV TM."};
}
if(typeof console!=="undefined" && typeof module!=="undefined" && module.exports){console.log(JSON.stringify(run499(),null,2));}
