function rankControls(){
let seed=37219871,rand=()=>seed=(Math.imul(seed,1664525)+1013904223)>>>0;
const pop=x=>{let c=0;while(x){x&=x-1;c++}return c};
const rank=arr=>{let b=new Map(),ops=0;for(let a of arr){while(a){let p=a&-a;ops++;if(!b.has(p)){b.set(p,a);break}a^=b.get(p)}}return{rank:b.size,ops}};
let checks=0,ops=0, cases=0;
for(let n=2;n<=6;n++)for(let d=1;d<=Math.min(3,n);d++)for(let j=0;j<30;j++){
 let M=Array.from({length:2**n},(_,i)=>i).filter(m=>pop(m)<=d),T=M.filter(m=>pop(m)===d),idx=new Map(M.map((m,i)=>[m,i])),W=[[],[]];
 for(let b=0;b<2;b++)for(let k=0;k<1+rand()%4;k++){let a=0n;for(let i=0;i<M.length;i++)if((rand()>>>29)&1)a^=1n<<BigInt(i);W[b].push(a)}
 let top=a=>T.reduce((s,m,i)=>s+(((a>>BigInt(idx.get(m)))&1n)<<BigInt(i)),0n),r0=rank(W[0]),r1=rank(W[1]),rt=rank(W.flat().map(top));
 let formula=r0.rank+r1.rank-rt.rank;
 // Enumerate every coefficient combination of the two lists, and explicitly check matching top part.
 let A=W.map(rows=>Array.from({length:2**rows.length},(_,s)=>rows.reduce((a,b,i)=>s>>i&1?a^b:a,0n))),P=new Set();
 for(let f of A[0])for(let g of A[1]){checks++;if(top(f)===top(g))P.add((f+(g^f)*(1n<<BigInt(M.length))).toString())}
 if(BigInt(P.size)!==1n<<BigInt(formula))throw Error("rank formula");
 cases++;ops+=r0.ops+r1.ops+rt.ops;
}
let guardChecks=0,degreeChecks=[];
for(let b=1;b<=8;b++){
 // Affine coordinate axis case; exact ANF via Möbius transform for every singleton guard word.
 let min=Infinity,max=0;
 for(let t=0;t<2**b;t++){let a=new Uint8Array(2**b);a[t]=1;for(let i=0;i<b;i++)for(let s=0;s<2**b;s++)if(s>>i&1){a[s]^=a[s^(1<<i)];guardChecks++}let deg=Math.max(...Array.from(a, (v,s)=>v?pop(s):0));min=Math.min(min,deg);max=Math.max(max,deg)}
 if(min!==b||max!==b)throw Error("guard degree");degreeChecks.push({b,guards:2**b,min,max});
}
const choose=(n,k)=>{if(k<0||k>n)return 0n;let c=1n;for(let i=1;i<=k;i++)c=c*BigInt(n-i+1)/BigInt(i);return c};
let debt=[];for(let r of [8,16,32,64,128,256]){let d=3,delta=choose(r-1,d)+BigInt(r-2);debt.push({r,d,empty_span_split_inflation:delta.toString(),D3:(Array.from({length:4},(_,i)=>choose(r,i)).reduce((s,v)=>s+v,0n)).toString()})}
return{model:"T4-GUARD-SPLICE-FILTER-v1",seed:37219871,cases,pairChecks:checks,rankOps:ops,guardMobiusUpdates:guardChecks,degreeChecks,debt,scope:"exact finite algebra controls only, not native hard-instance tests or universal lower bound"};
}
console.log(JSON.stringify(rankControls(),null,2));
