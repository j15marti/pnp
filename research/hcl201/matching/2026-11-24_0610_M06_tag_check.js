console.log(JSON.stringify((function run(){
let s=0x2010611;const r=n=>{s=(Math.imul(s,1103515245)+12345)>>>0;return (s>>>8)%n;};
const out={cases:0,sat:0,unsat:0,referenceCombinations:0,compressedCandidates:0,verified:0,maxChildren:0,scaling:[]};
function choices(H,q,cb){ // each child H0,H1; baseline is valid for either allowed status
 let base=H.map(([h0,h1])=>(h1.length?h1:h0)[0]);if(base.some(x=>x===undefined))return;
 let baseTag=base.reduce((a,b)=>a^b,0),disabled=H.reduce((a,h,i)=>h[1].length?a:a|(1n<<BigInt(i)),0n);
 function rec(start,rem,tag,mask,dev){cb({tag,mask,dev:dev.slice(),base});out.compressedCandidates++;if(!rem)return;
 for(let i=start;i<H.length;i++)for(let h of H[i][0])if(h!==base[i]){dev.push([i,h]);rec(i+1,rem-1,tag^base[i]^h,H[i][1].includes(h)?mask:mask|(1n<<BigInt(i)),dev);dev.pop();}}
 rec(0,q,baseTag,disabled,[]);
}
function actual(H,mask,tag,q){let S=new Set([0]);for(let i=0;i<H.length;i++){let h=H[i][Number((mask>>BigInt(i))&1n)],N=new Set();for(let a of S)for(let b of h){N.add(a^b);out.referenceCombinations++;}S=N;}return S.has(tag);}
for(let k=0;k<300;k++){let q=1+r(3),Q=1<<q,n=1+r(8),H=[];for(let i=0;i<n;i++){let a=[],b=[];for(let j=0;j<Q;j++)if(r(3)){a.push(j);if(r(2))b.push(j);}H.push([a,b]);}
 let masks=Array.from({length:1+r(10)},()=>BigInt(r(1<<n))),target=r(Q),local=masks.map(()=>r(Q)),want=masks.some((m,i)=>actual(H,m,target^local[i],q)),got=false;
 choices(H,q,c=>{for(let i=0;i<masks.length;i++){if((masks[i]&c.mask)||local[i]^c.tag^target)continue;let h=c.base.slice();for(let [j,v] of c.dev)h[j]=v;if(!h.every((v,j)=>H[j][Number((masks[i]>>BigInt(j))&1n)].includes(v))||h.reduce((a,b)=>a^b,local[i])!==target)throw Error("bad witness");got=true;}});
 if(got!==want)throw Error("mismatch");out.cases++;out[got?"sat":"unsat"]++;if(got)out.verified++;out.maxChildren=Math.max(out.maxChildren,n);}
for(let n of [16,64,256,1024]){let H=Array.from({length:n},()=>[[0,1],[0]]),before=out.compressedCandidates,count=0,all=(1n<<BigInt(n))-1n;choices(H,1,c=>{if(c.tag===1&&!(c.mask&(all^1n)))count++;});out.scaling.push({children:n,candidates:out.compressedCandidates-before,oneAbsentWitnesses:count});if(count!==1)throw Error("scale mismatch");}
return out;})(),null,2));
