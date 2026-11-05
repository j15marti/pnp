// LSPV3/418 independent bit-level signed-gauge checker. No producer imports.
'use strict';
let tick=0, tests=0;
function check(b,m){tests++;if(!b)throw Error(m)}
function next(){tick=(Math.imul(tick,1664525)+1013904223)>>>0;return tick}
function gateVal(table,a,b){return (table>>((a<<1)|b))&1}
function run(nInputs,gates,mask){let wires=Array.from({length:nInputs},(_,i)=>(mask>>>i)&1);
 for(const g of gates){const [a,b,table]=g;if(a<0||b<0||a>=wires.length||b>=wires.length||table<0||table>15)throw Error('bad gate');wires.push(gateVal(table,wires[a],wires[b]))}return wires}
function gauge(gates,nInputs,flips){return gates.map(([a,b,tt],i)=>{let nt=0;
 for(let x=0;x<=1;x++)for(let y=0;y<=1;y++){
 const c=(gateVal(tt,x^(a>=nInputs?flips[a-nInputs]:0),y^(b>=nInputs?flips[b-nInputs]:0))^flips[i]);
 nt|=c<<((x<<1)|y)
 }return [a,b,nt]})}
function rowTrue(value,idx,rhs){let x=0;for(const j of idx)x^=value[j];return x===rhs}
function clTrue(value,lits){return lits.some(([id,sign])=>value[id]===sign)}
function transformedRhs(idx,rhs,flips,nInputs){let out=rhs;for(const id of idx) if(id>=nInputs)out^=flips[id-nInputs];return out}
function transformedClause(lits,flips,nInputs){return lits.map(([id,s])=>[id,s^(id>=nInputs?flips[id-nInputs]:0)])}
const n=4,m=6;
for(let k=0;k<70;k++){
 const G=[];
 for(let i=0;i<m;i++){
  const nwire=n+i;
  const a=next()%nwire,b=next()%nwire,tt=next()%16;
  G.push([a,b,tt])
 }
 for(let f=0;f<(1<<m);f++){
  const flip=Array.from({length:m},(_,i)=>(f>>>i)&1), H=gauge(G,n,flip);
  for(let x=0;x<(1<<n);x++){
   const p=run(n,G,x),q=run(n,H,x);
   for(let j=0;j<n+m;j++)check(p[j]=== (q[j]^(j>=n?flip[j-n]:0)),`wire mismatch k=${k},f=${f},x=${x},j=${j}`);
   for(const [ids,rhs] of [[[],0],[[4,6,9],1],[[0,1,7],0],[[4],1],[[2,3],1],[[7,8,9],0]]){
    check(rowTrue(p,ids,rhs)===rowTrue(q,ids,transformedRhs(ids,rhs,flip,n)),'wrong affine map')
   }
   for(const c of [[[4,1],[6,0]],[[0,0],[7,1],[9,1]],[[3,1]],[[4,0],[4,1]]]){
    check(clTrue(p,c)===clTrue(q,transformedClause(c,flip,n)),'wrong literal polarity map')
   }
  }
 }
}
const Fplus=[[[0,1],[1,1]],[[0,0],[2,1]]];
const Fminus=Fplus.concat([[[0,1]],[[0,0]]]);
for(const [F,expected] of [[Fplus,8],[Fminus,0]]){let count=0;for(let x=0;x<16;x++)if(F.every(c=>clTrue(run(n,[],x),c)))count++;check(count===expected,'source model wrong')}
const G=[[0,1,6],[4,2,8],[4,5,6]];
const flip=[1,1,0],first=run(4,G,7),other=run(4,gauge(G,4,flip),7);
const ids=[4,6,0],rhs=0;
check(rowTrue(first,ids,rhs)===rowTrue(other,ids,transformedRhs(ids,rhs,flip,4)),'corrected affine failed');
check(rowTrue(first,ids,rhs)!==rowTrue(other,ids,rhs),'forgotten affine RHS passed');
for(const bad of [[[4,1,8]],[[0,1,16]],[[0,9,6]]]){
 let rejected=false;try{run(4,bad,0)}catch(e){rejected=true}check(rejected,'bad gate accepted')
}
process.stdout.write(JSON.stringify({run:'LSPV3/418',independent:'no producer import',networks:70,gauges:64,inputs_per_gauge:16,checks:tests,source_plus_models:8,source_minus_models:0,malformed_controls:3},null,2)+'\n');
