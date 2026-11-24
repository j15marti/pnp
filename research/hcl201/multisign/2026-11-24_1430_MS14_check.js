/* Node.js, deterministic audit */
function experiment(){
 const bit=i=>1n<<BigInt(i), par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p}, sign=x=>par(x)?-1n:1n;
 function insert(B,v,c=0n){while(v){let i=v.toString(2).length-1;if(B[i]){v^=B[i][0];c^=B[i][1]}else{B[i]=[v,c];return [true,c]}}return [false,c]}
 function reduce(B,v,c=0n){while(v){let i=v.toString(2).length-1;if(!B[i])return [v,c];v^=B[i][0];c^=B[i][1]}return [0n,c]}
 function rank(a){let B=[];for(let x of a)insert(B,x);return B.filter(Boolean).length}
 function mask(rows,x){let v=0n;rows.forEach((r,i)=>{if(par(r&x))v|=bit(i)});return v}
 let stats={seed:20261124,random_queries:0,sat_queries:0,unsat_queries:0,guarded_queries:0,signed_comparisons:0,attempts:0,peak_keys:0,closure_deductions:0};
 // Blocks are {r: private rows, ok: allowed actual output words, b: affine offset}.
 function moment(blocks,w){
  let rows=blocks.flatMap(b=>b.r), B=[], deps=[];rows.forEach((r,i)=>{let [ok,c]=insert(B,r,bit(i));if(!ok)deps.push(c)});
  let [rem,lam]=reduce(B,w); if(rem)return [0n,1n,0,0];
  let cols=rows.map((_,i)=>mask(deps,bit(i))), suf=Array(rows.length+1);suf[rows.length]=[];
  for(let i=rows.length-1;i>=0;i--){suf[i]=suf[i+1].slice();insert(suf[i],cols[i])}
  let dp=new Map([[0n,1n]]), pos=0, peak=1, width=0;
  for(let b of blocks){let nxt=new Map(), k=b.r.length, end=pos+k, opts=[];
   for(let v of b.ok){let y=BigInt(v)^b.b,s=0n;for(let j=0;j<k;j++)if(y&bit(j))s^=cols[pos+j];opts.push([s,sign((y<<BigInt(pos))&lam)])}
   for(let [p,n] of dp)for(let [s,sg] of opts){stats.attempts++;let q=p^s;if(reduce(suf[end],q)[0])continue;nxt.set(q,(nxt.get(q)||0n)+sg*n)}
   dp=nxt;pos=end;peak=Math.max(peak,dp.size);width=Math.max(width,rank(rows.slice(0,pos))+rank(rows.slice(pos))-rank(rows));
  }
  stats.peak_keys=Math.max(stats.peak_keys,peak);if(peak>2**width)throw Error("width");
  return [dp.get(0n)||0n,bit(B.filter(Boolean).length),peak,width];
 }
 function holds(bs,x){return bs.every(b=>b.ok.includes(Number(mask(b.r,x)^b.b)))}
 // Substitute x_j = value; leave unused coordinate as a dummy, so averaging is unchanged.
 function pin(bs,j,v){return bs.map(b=>({...b,b:b.b^(v?mask(b.r,bit(j)):0n),r:b.r.map(r=>r&~bit(j))}))}
 let rng=20261124>>>0;function rnd(k){rng=(Math.imul(rng,1664525)+1013904223)>>>0;return (rng>>>8)%k}
 for(let trial=0;trial<100;trial++){
  let n=3+rnd(5),bs=[];for(let i=0;i<1+rnd(4);i++){let k=1+rnd(4),r=Array.from({length:k},()=>BigInt(rnd(1<<n))),ok=Array.from({length:1<<k},(_,j)=>j).filter(()=>rnd(4)!==0);bs.push({r,ok,b:BigInt(rnd(1<<k))})}
  let ref=Array.from({length:1<<n},(_,j)=>BigInt(j)).filter(x=>holds(bs,x));
  stats.random_queries++;if(ref.length)stats.sat_queries++;else stats.unsat_queries++;
  for(let j=0;j<10;j++){let w=BigInt(rnd(1<<n)),[a,b]=moment(bs,w),r=ref.reduce((s,x)=>s+sign(x&w),0n);if(a*bit(n)!==r*b)throw Error("moment");stats.signed_comparisons++}
  // Certified individual-event coverage and opposite coordinate coverage; here bs denotes one bad event.
  let cur=bs, fixed=new Map();for(;;){let [a,b]=moment(cur,0n);if(a===b)break;let change=false;for(let j=0;j<n;j++){if(fixed.has(j))continue;for(let v=0;v<2;v++){let [p,q]=moment(pin(cur,j,v),0n);if(p===q){let good=1-v;for(let x=0;x<(1<<n);x++){let X=BigInt(x);if([...fixed].every(([k,h])=>Number((X>>BigInt(k))&1n)===h)&&!holds(bs,X)&&Number((X>>BigInt(j))&1n)!==good)throw Error("closure")}fixed.set(j,good);cur=pin(cur,j,good);stats.closure_deductions++;change=true;break}}if(change)break}if(!change)break}
  let j=rnd(n),v=rnd(2),w=BigInt(rnd(1<<n))&~bit(j),[a,b]=moment(pin(bs,j,v),w),r=ref.filter(x=>Number((x>>BigInt(j))&1n)===v).reduce((s,x)=>s+sign(x&w),0n);if(a*bit(n-1)!==r*b)throw Error("guard");stats.guarded_queries++;
 }
 // RT13 path chart: each vertex sees two consecutive edge colors and one leaf color,
 // the fourth is their XOR. Root boundary XOR is fixed to zero.
 const ok=[];for(let v=0;v<256;v++){let c=[v&3,(v>>2)&3,(v>>4)&3,(v>>6)&3];if(new Set(c).size===4)ok.push(v)}
 function path(t,shift=0n){let bs=[];for(let i=0;i<t;i++){let r=[bit(2*i),bit(2*i+1),bit(2*i+2),bit(2*i+3),bit(2*(t+1+i)),bit(2*(t+1+i)+1)];r.push(r[0]^r[2]^r[4],r[1]^r[3]^r[5]);bs.push({r,ok,b:mask(r,shift)})}return bs}
 let scale=[];for(let t of [1,2,4,8,16,32,64]){
  let bs=path(t),[a,b,peak,width]=moment(bs,0n);if(a*8n**BigInt(t)!==b*3n**BigInt(t))throw Error("path density");
  let sh=bit(0)^bit(2*t)^bit(4*t+1), shifted=path(t,sh), w=bit(0)^bit(2);
  let [u,v]=moment(bs,w),[h,k]=moment(shifted,w);if(u*k*sign(w&sh)!==h*v)throw Error("gauge phase");
  // Pin the boundary chart to a bad proper-edge-coloring, then change one a color
  // to collide; the affine parity chart changes two exterior edge colors.
  let x=0n;for(let i=0;i<=t;i++){if(i%2)x|=bit(2*i)}for(let i=0;i<t;i++)x|=bit(2*(t+1+i)+1);
  if(!holds(bs,x)||holds(bs,x^bit(2*(t+1)+1)))throw Error("opposite labels");
  scale.push({t,chart_bits:4*t+2,peak,width,bad_count:(4n*6n**BigInt(t)).toString(),density:`${3n**BigInt(t)}/${8n**BigInt(t)}`,flat_cover:(3n**BigInt(t)).toString()});
 }
 // Small uniform PSD example: three bad events on a common pair of bits plus
 // three independent bits. e_i = (s != 0) AND a_i=0. P=3/8, pair P=3/16.
 // Compute pair lower from complete local feature unions (<= 12 masks per pair).
 let events=[0,1,2].map(i=>[{r:[1n,2n,bit(i+2)],ok:[1,2,3],b:0n}]);
 let coeff=events.map(e=>Array.from({length:32},(_,w)=>{let [a,b]=moment(e,BigInt(w));return a*32n/b}));
 let c=32n*32n*2n-2n*32n*coeff.reduce((s,v)=>s+v[0],0n);
 for(let [i,j] of [[0,1],[1,2]]){let ss=coeff[i].reduce((s,a,w)=>s+(a+coeff[j][w])**2n,0n);c+=ss-32n*(coeff[i][0]+coeff[j][0])}
 if(c!==512n)throw Error("PSD credit"); // 1/4
 let legal=0;for(let x=0n;x<32n;x++)if(events.every(e=>!holds(e,x)))legal++;
 if(c>BigInt(legal)*64n)throw Error("credit");
 return {stats,scale,psd:{uniform_credit:"1/4",union_bound:"9/8",legal_of_32:legal},scope:"signed trellis, one-coordinate closure, gauge translation checks; no general quotient discovery, common-prefix lift, physical compiler or complete closure implemented"};
}
console.log(JSON.stringify(experiment(),null,2));
