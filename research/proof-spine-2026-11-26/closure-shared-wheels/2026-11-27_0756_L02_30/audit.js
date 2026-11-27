"use strict";
function audit(){
const bit=i=>1n<<BigInt(i), pop=x=>{let n=0;while(x){x&=x-1n;n++}return n}, key=(a,b)=>a.toString(16)+":"+b.toString(16);
const eq=(p,msg)=>{if(!p)throw Error(msg)};
const edge=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function source(h,even=false){
 let F=[],rows=[];
 for(let v=0;v<4;v++){
  let ids=edge.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
  let em=ids.reduce((a,i)=>a|bit(i),0n), c=v===0&&!even?1:0;
  rows.push([em,c]);
  for(let w=0;w<8;w++)if(pop(BigInt(w))%2!==c){
   let ev=ids.reduce((a,i,j)=>a|((w>>j&1)?bit(i):0n),0n);
   let hm=(bit(h)-1n)<<6n;
   for(let i=0;i<h;i++)F.push({id:F.length,v,a:em|(hm^bit(i+6)),b:ev});
   for(let j=1;j<h;j++)for(let i=0;i<j;i++)F.push({id:F.length,v,a:em|((bit(j+1)-1n)<<6n),b:ev|bit(i+6)|bit(j+6)});
  }
 }
 return {F,rows,d:h+6,h};
}
function meet(a,b,c,d){if(((b^d)&a&c)!==0n)return null;return [a|c,b|d]}
function budget(cap=10000000){return {n:0,cap,tick(){if(++this.n>this.cap)throw Error("CAP")}}}
function signed(F,B){
 let D=new Map([["0:0",[0n,0n,1n]]]),peak=1;
 for(const {a,b} of F){
  let next=new Map(D);
  for(const [k,[c,d,z]] of D){B.tick();let u=meet(a,b,c,d);if(!u)continue;let s=key(...u),w=(next.get(s)?.[2]||0n)-z;if(w===0n)next.delete(s);else next.set(s,[...u,w])}
  D=next;peak=Math.max(peak,D.size);
 }
 return {D,peak};
}
function count(D,d,B,mask=0n,rhs=0){
 let out=0n;for(const [a,b,z] of D.values()){B.tick();let n=d-pop(a),m=mask&~a;
 if(m===0n){if(pop(mask&b)%2===rhs)out+=z*bit(n)}
 else out+=z*bit(n-1)}
 return out;
}
function gauss(rows,B){
 let P=new Map();for(let [a,b] of rows){B.tick();while(a){let i=a&-a;if(!P.has(i)){P.set(i,[a,b]);break}let [c,d]=P.get(i);a^=c;b^=d;B.tick()}if(!a&&b)return true}return false;
}
function unitScan(F,B){for(const c of F){B.tick();eq(pop(c.a)>1,"unexpected unit")}}
function run(h,even=false){
 const S=source(h,even),{F,d,rows}=S;
 const A=budget(),B=budget(),C=budget(),I=budget();
 unitScan(F,A);unitScan(F,B);unitScan(F,C);unitScan(F,I);
 // A: four-way intersection witness, no assumption of bounded overlap.
 let first=F.filter(c=>c.v===0).slice(0,4);
 let u=[0n,0n];for(const c of first){A.tick();u=meet(...u,c.a,c.b);if(!u)break}
 eq(u!==null,"four-way intersection");
 // B: independent classification of each local hub word by first two ones.
 // For larger h, test all partition classes using exact expected cube key sets and sizes.
 let direct=0,exhaustive=0,imports=[],stats=[];
 for(let v=0;v<4;v++){
  const R=F.filter(c=>c.v===v),[em,c]=rows[v],ids=edge.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
  let groups=new Map();
  for(const f of R){B.tick();let w=(f.b&em).toString();if(!groups.has(w))groups.set(w,[]);groups.get(w).push(f)}
  eq(groups.size===4,"wrong words");
  for(const [w,G] of groups){let ev=BigInt(w);eq(pop(ev)%2!==c,"wrong parity");let seen=new Set(G.map(f=>key(f.a&~em,f.b&~em)));let hm=(bit(h)-1n)<<6n;
   for(let i=0;i<h;i++){B.tick();eq(seen.delete(key(hm^bit(i+6),0n)),"unit weight cube")}
   for(let j=1;j<h;j++)for(let i=0;i<j;i++){B.tick();eq(seen.delete(key((bit(j+1)-1n)<<6n,bit(i+6)|bit(j+6))),"first pair cube")}
   eq(seen.size===0,"extra cube");direct++;
  }
  if(h<=8)for(let w=0;w<8;w++)for(let y=0;y<(1<<h);y++){
    let x=BigInt(y)<<6n;ids.forEach((id,j)=>{if(w>>j&1)x|=bit(id)});
    let bad=false;for(const f of R){B.tick();if((x&f.a)===f.b){bad=true;break}}
    eq(bad===(pop(BigInt(w))%2!==c),"enumeration");exhaustive++;
  }
  // C: signed intersection recurrence, exact global-coordinate counts.
  let {D,peak}=signed(R,C),total=count(D,d,C),wrong=count(D,d,C,em,1-c);
  eq(total===bit(d-1)&&wrong===0n,"signed count");
  eq(peak===1+4*(h+1+h*(h-1)/2),"distinct count");
  stats.push({v,peak,terms:D.size,wrong:wrong.toString(),total:total.toString()});
  // integrated: replay on same source, verify imported parity certificate
  let replay=signed(R,I);eq(count(replay.D,d,I,em,1-c)===0n,"replay");
  imports.push([em,c]);unitScan(F,I); // no unit on original clauses, affine closure via Gaussian
 }
 const noB=gauss(rows,B),noI=gauss(imports,I);
 eq(noB===!even&&noI===!even,"global parity");
 // C independently checks original charge conservation.
 let sum=0n,rhs=0;for(const [a,b] of rows){C.tick();sum^=a;rhs^=b}
 eq(sum===0n&&rhs===Number(!even),"conservation");
 unitScan(F,I);
 const M=F.length,K=Math.max(2,M,d),N=16*K*K+8*K+Math.floor(Math.log2(K))+1;
 return {h,d,M,N,regionTerms:stats[0].terms,peak:stats[0].peak,old:"OVERLAP",B:noB?"NO":"UNKNOWN",C:rhs?"NO":"UNKNOWN",I:noI?"NO":"UNKNOWN",direct,exhaustive,ops:[A.n,B.n,C.n,I.n],stats};
}
let results=[4,8,12,16,24].map(h=>run(h));
let S=source(4),R=S.F.filter(c=>c.v===0),[a,c]=S.rows[0],B=budget();
let del=R.slice(0,-1),deleted=count(signed(del,B).D,S.d,B,a,1-c);
eq(deleted>0n,"deletion must invalidate row");
let even=run(4,true);
let capF=Array.from({length:16},(_,i)=>({a:bit(2*i)|bit(2*i+1),b:0n}));let cap=budget(1000),capStatus="unexpected";
try{signed(capF,cap)}catch(e){if(e.message==="CAP")capStatus="UNKNOWN";else throw e}
eq(capStatus==="UNKNOWN","cap status");
return {results,controls:{deletedWrongCount:deleted.toString(),even:even.I,capStatus,capAttempts:cap.n},capPerCopy:10000000};
}
console.log(JSON.stringify(audit(),null,2));
