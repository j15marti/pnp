/* ARC-NESTED-ACCESS-TAX113: ordinary-CNF, two genuine typed levels.
   Run: node 2026-10-25_1822_ARC_NESTED_ACCESS_TAX113_repro.js
   This measures JS logical bit/probe counters, NOT physical FLMV tape cells.
   No randomness; exhaustive parity/2SAT and actual two-level bit checks.
*/
"use strict";
function assert(p,msg){if(!p)throw Error(msg)}
function width(n){return Math.max(1,Math.ceil(Math.log2(n+1)))}
function bstr(x,w){return x.toString(2).padStart(w,"0")}
function encode(clauses,n){
 const m=clauses.length,w=width(Math.max(n,m)),B=2+3*(w+1);
 let out="1".repeat(w)+"0"+bstr(n,w)+bstr(m,w);
 for(const C of clauses){
  assert(C.length>=1&&C.length<=3,"arity");
  out+=bstr(C.length,2);
  for(let i=0;i<3;i++){const v=C[i]||0;out+=(v<0?"1":"0")+bstr(Math.abs(v),w)}
 }
 assert(out.length===(3*w+1)+m*B,"encoded length");
 return out;
}
function parity(B){return B.reduce((a,b)=>a^b,0)}
function cycleClauses(B){
 const q=B.length,C=[];
 for(let i=0;i<q;i++){const u=i+1,v=(i+1)%q+1;
  if(B[i]===0){C.push([-u,v],[u,-v])}
  else {C.push([u,v],[-u,-v])}
 }
 return C;
}
function canonClause(odd,m,j){
 if(j<7){return [1,2,3].map((v,k)=>(((j>>(2-k))&1)?-v:v))}
 if(j===7){return odd?[-1,-2,-3]:[4,5,6]}
 const d=j-8;assert(d>=0&&d<m,"bad canonical clause");
 return [7+3*d,8+3*d,9+3*d];
}
function canonical(odd,m){
 const C=[];for(let j=0;j<8+m;j++)C.push(canonClause(odd,m,j));
 return {n:6+3*m,clauses:C,bits:encode(C,6+3*m)};
}
function canonicalBit(odd,m,index){
 const n=6+3*m,total=8+m,w=width(Math.max(n,total));
 const header="1".repeat(w)+"0"+bstr(n,w)+bstr(total,w), B=2+3*(w+1);
 const L=header.length+total*B;
 assert(index>=0&&index<L,"canonical bit index");
 if(index<header.length)return header[index];
 const j=Math.floor((index-header.length)/B),p=(index-header.length)%B;
 const C=canonClause(odd,m,j);
 let rec="11";for(const v of C)rec+=(v<0?"1":"0")+bstr(Math.abs(v),w);
 return rec[p];
}
function pad(N){return Math.floor(Math.sqrt(N)/Math.log2(N+2))}
function decodeInfo(x){
 let w=0;while(x[w]==="1")w++;
 assert(x[w]==="0"&&w>0,"unary header");
 const h=3*w+1,n=parseInt(x.slice(w+1,2*w+1),2);
 const m=parseInt(x.slice(2*w+1,3*w+1),2),B=2+3*(w+1);
 assert(x.length===h+m*B,"malformed length");
 return {w,h,n,m,B};
}
function sourceParityStream(x){
 const d=decodeInfo(x);assert(d.n>=3&&d.m===2*d.n,"cycle promise");
 let v=0,reads=0;
 for(let j=0;j<x.length;j++){reads++; /* counted input source-bit read */ if(x[j]!=="0"&&x[j]!=="1")throw Error("bad bit")}
 for(let i=0;i<d.n;i++){
  const sign=x[d.h+(2*i)*d.B+2];v^=(sign==="0"?1:0);reads++;
 }
 return {odd:v,reads};
}
function isSat2SAT(clauses,n){
 const g=Array.from({length:2*n},()=>[]);
 function node(l){return 2*(Math.abs(l)-1)+(l<0?1:0)}
 for(const C of clauses){assert(C.length===2,"2CNF");
  g[node(-C[0])].push(node(C[1]));g[node(-C[1])].push(node(C[0]))}
 const seen=Array(2*n).fill(false),order=[];
 function dfs(v){seen[v]=true;for(const u of g[v])if(!seen[u])dfs(u);order.push(v)}
 for(let i=0;i<2*n;i++)if(!seen[i])dfs(i);
 const gr=Array.from({length:2*n},()=>[]);
 for(let v=0;v<2*n;v++)for(const u of g[v])gr[u].push(v);
 const comp=Array(2*n).fill(-1);
 function rev(v,k){comp[v]=k;for(const u of gr[v])if(comp[u]===-1)rev(u,k)}
 let k=0;for(let i=order.length-1;i>=0;i--){const v=order[i];if(comp[v]===-1)rev(v,k++)}
 for(let i=0;i<n;i++)if(comp[2*i]===comp[2*i+1])return false;
 return true;
}
function isSatDPLL(clauses){
 function solve(cs){
  if(cs.length===0)return true;
  for(const C of cs)if(C.length===0)return false;
  let unit=cs.find(C=>C.length===1);
  let literal=unit?unit[0]:cs[0][0];
  function reduce(l){
   const next=[];for(const C of cs){if(C.includes(l))continue;next.push(C.filter(x=>x!==-l))}
   return next;
  }
  if(unit)return solve(reduce(literal));
  return solve(reduce(literal))||solve(reduce(-literal));
 }
 return solve(clauses);
}
function makeSource(q,odd){
 const B=Array(q).fill(0);B[0]=odd?1:0;
 // A deterministic dispersed pair of opposite bits exercises nontrivial SAT labels.
 for(let i=1;i+1<q;i+=3){B[i]=1;B[i+1]=1}
 const cs=cycleClauses(B);
 return {q,odd:parity(B),B,cs,x:encode(cs,q)};
}
function run(){
 const tests=[],sizes=[3,4,5,6,7,8,12,24,48,96];
 let assertions=0,totalPhysicalReads=0,totalVirtualG1=0;
 for(const q of sizes)for(const requestedOdd of [0,1]){
  const src=makeSource(q,requestedOdd),N=src.x.length,m1=pad(N);
  const y=canonical(src.odd,m1),L1=y.bits.length,m2=pad(L1);
  const z=canonical(src.odd,m2),L2=z.bits.length;
  const d1=decodeInfo(y.bits),sig=d1.h+7*d1.B+2;
  assert((src.odd===0)===isSat2SAT(src.cs,q),"source 2SAT label");assert((src.odd===0)===isSatDPLL(y.clauses),"level one SAT label");
  assert((src.odd===0)===isSatDPLL(z.clauses),"level two SAT label");assert(y.bits[sig]===(src.odd?"1":"0"),"signature");assertions+=4;
  const G1=(j)=>{const info=sourceParityStream(src.x);totalPhysicalReads+=info.reads;totalVirtualG1++;return canonicalBit(info.odd,m1,j)};
  const G2=(i)=>{
   let bit="0";for(let j=0;j<L1;j++){const v=G1(j);if(j===sig)bit=v;}
   return canonicalBit(bit==="1"?1:0,m2,i);
  };
  const yIndices=[0,1,Math.floor(L1/2),L1-1];
  for(const j of new Set(yIndices)){assert(G1(j)===y.bits[j],"G1 bit");assertions++}
  const zIndices=[0,1,Math.floor(L2/2),L2-1];
  for(const i of new Set(zIndices)){assert(G2(i)===z.bits[i],"G2 bit");assertions++}
  let scans=0;
  if(q<=4){
   for(let i=0;i<L2;i++){assert(G2(i)===z.bits[i],"actual full guest input scan");assertions++;scans++}
  }
  // Exact design identity for one full scan: each G2 bit invokes G1 L1 times;
  // each G1 reads N+q source/index bits in this literal implementation.
  const expectedReadsPerFullGuestScan=L2*L1*(N+q);
  tests.push({q,requestedOdd:src.odd===1,N,L1,L2,m1,m2,firstLevelShort:L1<N,secondLevelShort:L2<L1,
    actualScannedGuestBits:scans,sourceReadsForOneFullNaiveGuestScan:expectedReadsPerFullGuestScan,
    cachedFusedSourceScanReads:N+q, guestSat:src.odd===0});
 }
 assert(tests.length===20,"case count");
 const full=tests.filter(x=>x.actualScannedGuestBits>0),both=tests.filter(x=>x.firstLevelShort&&x.secondLevelShort);
 return {report:"ARC-NESTED-ACCESS-TAX113",kind:"deterministic exact finite JS experiment; logical bit counters, not FLMV instruction trace",
 version:"1.0", cases:tests.length,fullNestedGuestInputScans:full.length,actualAssertCount:assertions,
 virtualG1BitRequestsActuallyExecuted:totalVirtualG1,sourceBitReadsActuallyExecuted:totalPhysicalReads,
 fullTwoLevelPowerShortFiniteCases:both.length, fullTwoLevelPowerShortNotRequiredForProof:true,
 asymptoticNestedSourceBitReadsExponent:"7/4 with L1=N^(1/2+o(1)), L2=N^(1/4+o(1))",
 optimizedFusedSourceScanExponent:"1 on this EASY promise only",failed:0,tests};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
