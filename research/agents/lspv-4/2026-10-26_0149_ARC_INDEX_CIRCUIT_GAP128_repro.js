'use strict';
// Run: node 2026-10-26_0149_ARC_INDEX_CIRCUIT_GAP128_repro.js
let checks=0;
function ok(x,msg){checks++;if(!x)throw Error(msg)}
function gcd(a,b){return b===0n?a:gcd(b,a%b)}
function f(a,b=1n){a=BigInt(a);b=BigInt(b);let g=gcd(a,b);return [a/g,b/g]}
function add([a,b],[c,d]){return f(a*d+b*c,b*d)}
function sub([a,b],[c,d]){return f(a*d-b*c,b*d)}
function mul([a,b],[c,d]){return f(a*c,b*d)}
function div([a,b],[c,d]){return f(a*d,b*c)}
function str(x){return String(x[0])+'/'+String(x[1])}
const bs=(x,w)=>x.toString(2).padStart(w,'0');
function force(c,l,next){const u=next(),v=next();c.push([l,u,v],[l,u,-v],[l,-u,v],[l,-u,-v])}
function enc(n,c){
  const m=c.length,w=Math.ceil(Math.log2(Math.max(n,m)+1));
  const header='1'.repeat(w)+'0'+bs(n,w)+bs(m,w);
  const body=c.map(row=>row.map(l=>(l>0?'1':'0')+bs(Math.abs(l),w)).join('')).join('');
  return {n,m,w,c,header,bits:header+body,stride:3*(w+1)};
}
function build(k,a,z){
  const L=2**k;let id=0;const next=()=>++id;
  const leaves=Array.from({length:L},next),addr=Array.from({length:k},next);
  let layer=leaves;const gates=[];
  for(let j=0;j<k;j++){
    const parents=[];
    for(let p=0;p<layer.length;p+=2){const y=next();gates.push([y,addr[j],layer[p],layer[p+1]]);parents.push(y)}
    layer=parents;
  }
  const c=[];
  z.forEach((b,i)=>force(c,b?leaves[i]:-leaves[i],next));
  addr.forEach((v,j)=>force(c,(a&(1<<j))?v:-v,next));
  gates.forEach(([y,s,l,h])=>c.push([s,-l,y],[s,l,-y],[-s,-h,y],[-s,h,-y]));
  force(c,layer[0],next);
  const x=enc(id,c);x.k=k;x.L=L;
  x.dataPos=i=>x.header.length+4*i*x.stride;
  x.addrPos=j=>x.header.length+(4*L+4*j)*x.stride;
  return x;
}
function promise(x){let a=0;for(let j=0;j<x.k;j++)a|=Number(x.bits[x.addrPos(j)])<<j;return Number(x.bits[x.dataPos(a)])}
function solve(c,n){
  function dfs(state){
    while(true){
      let changed=false,unresolved=false;const scores=new Int32Array(n+1);
      for(const row of c){
        let yes=false,count=0,last=0;
        for(const l of row){const v=state[Math.abs(l)];if(v<0){count++;last=l;}else if(v===(l>0?1:0)){yes=true;break}}
        if(yes)continue;unresolved=true;if(!count)return false;
        if(count===1){const i=Math.abs(last),v=last>0?1:0;if(state[i]>=0&&state[i]!==v)return false;if(state[i]<0){state[i]=v;changed=true}}
        else for(const l of row)if(state[Math.abs(l)]<0)scores[Math.abs(l)]++;
      }
      if(changed)continue;if(!unresolved)return true;
      let varId=0,best=-1;
      for(let i=1;i<=n;i++)if(state[i]<0&&scores[i]>best){best=scores[i];varId=i}
      if(!varId)return true;
      for(const v of [1,0]){const other=state.slice();other[varId]=v;if(dfs(other))return true}
      return false;
    }
  }
  const state=new Int8Array(n+1);state.fill(-1);return dfs(state);
}
function child(b){let n=1;const next=()=>++n,c=[];force(c,1,next);if(!b)force(c,-1,next);return enc(n,c)}
function run(){
  const C=f(241,200),S=f(11642479,23232400),d=f(901,500);
  const beta=div(sub(div(add(C,f(2)),mul(C,C)),C),f(2));
  ok(str(beta)===str(S),'FLMV');
  const tm=sub(C,f(6,5)),sm=sub(S,f(1,2));
  ok(str(tm)==='1/200'&&str(sm)==='26279/23232400','margins');
  const Cco=div(sub(mul(f(2),d),f(1)),mul(d,sub(d,f(1))));
  const D=mul(d,d),q=div(D,sub(D,f(1)));
  ok(str(Cco)==='651000/361301','conditional coNTIME');
  ok(str(q)==='811801/561801','conditional circuit');
  let sources=0,attacks=0,childLevels=0;const rows=[];
  for(const k of [1,2,3]){
    const L=2**k,masks=k<=2?2**L:32;let representative;
    for(let pattern=0;pattern<masks;pattern++){
      const mask=k<=2?pattern:(pattern*73+17)%256;
      for(let a=0;a<L;a++){
        if(k===3&&a>1)continue;
        const z=Array.from({length:L},(_,i)=>(mask>>i)&1),x=build(k,a,z);
        ok(x.n===4*L+3*k+1&&x.m===8*L+4*k,'counts');
        ok(x.bits.length===3*x.w+1+3*x.m*(x.w+1),'bits');
        ok(x.c.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),'proper');
        ok(promise(x)===z[a],'promise selector');
        const v=solve(x.c,x.n);ok(v===(z[a]===1),'SAT label');
        const child1=child(v),child2=child(v);
        ok(solve(child1.c,child1.n)===v,'child1');
        ok(solve(child2.c,child2.n)===v,'child2');
        ok(child1.bits.length===3*child1.w+1+3*child1.m*(child1.w+1),'child1 bits');
        ok(child2.bits.length===3*child2.w+1+3*child2.m*(child2.w+1),'child2 bits');
        if(!representative)representative={N:x.bits.length,n:x.n,m:x.m,readBits:k+1,firstChildN:child1.bits.length,secondChildN:child2.bits.length};
        sources++;childLevels+=2;
      }
    }
    for(let a=0;a<L;a++){
      const z=Array(L).fill(1);z[a]=0;const x=build(k,a,z);
      ok(!solve(x.c,x.n),'negative source');
      const changed=x.c.map(c=>c.slice());changed[4*a+1][0]*=-1;
      const off=x.header.length+(4*a+1)*x.stride;
      const bits=x.bits.slice(0,off)+(x.bits[off]==='1'?'0':'1')+x.bits.slice(off+1);
      const encoded=enc(x.n,changed);
      ok(encoded.bits===bits,'one physical sign bit');
      ok(solve(changed,x.n),'sign flip makes source SAT');
      ok(promise({...x,bits})===0,'unread sign flips answer');
      attacks++;
    }
    rows.push({k,L,representative,circuitGateLowerBound:L-1,sources:k<=2?masks*L:masks*2,attacks:L});
  }
  ok(rows.every(r=>r.representative.N>r.L),'header overhead');
  return {assertions:checks,sources,attacks,childLevels,exact:{flmvBeta:str(beta),timeMargin:str(tm),spaceMargin:str(sm),extraSeedC:str(Cco),extraSeedQ:str(q),ShalunovStrictQ:str(mul(f(2),S))},rows,scope:'restricted indexed-CNF promise; not all-input SAT; P vs NP OPEN'};
}
console.log(JSON.stringify(run(),null,2));
