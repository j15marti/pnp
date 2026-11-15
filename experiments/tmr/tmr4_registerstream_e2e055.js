'use strict';
const REV='tmr4-registerstream-e2e055.v1',SEED=20261115;
let rng=SEED>>>0;
function rand(){rng^=rng<<13;rng^=rng>>>17;rng^=rng<<5;return rng>>>0;}
function ok(b,msg){if(!b)throw Error(msg||'assertion failed');stats.assertions++;}
function integer(x){return Number.isSafeInteger(x)&&x>=0;}
const stats={revision:REV,seed:SEED,programs:0,assignments:0,assertions:0,rectangles:0,malformed_rejected:0,failures:0,samples:[]};
function parse(raw){
  let a=JSON.parse(raw);
  if(!a||JSON.stringify(a)!==raw||a.version!==1||!integer(a.n)||a.n<1||!integer(a.s)||a.s<1||!integer(a.init)||a.init>=2**a.s||!Array.isArray(a.stages)||a.stages.length!==a.n||!a.accept)throw Error('header');
  if(a.n>10||a.s>8)throw Error('finite audit cutoff');
  const q=Math.ceil(Math.log2(a.n));let G=0;
  function inspect(d,final){
    if(!d||!Array.isArray(d.gates))throw Error('gates');
    for(let i=0;i<d.gates.length;i++){
      let g=d.gates[i];
      if(!Array.isArray(g)||g.length!==3||!g.every(integer)||g[2]>15||g[0]>=a.s+3+i||g[1]>=a.s+3+i)throw Error('gate');
    }
    let cap=a.s+3+d.gates.length;
    if(final){if(!integer(d.out)||d.out>=cap)throw Error('out');}
    else{
      if(!Array.isArray(d.next)||d.next.length!==a.s||d.next.some(v=>!integer(v)||v>=cap))throw Error('next');
      if((d.index===undefined)===(d.select===undefined))throw Error('index/select');
      if(d.index!==undefined&&(!integer(d.index)||d.index>=a.n))throw Error('index');
      if(d.select!==undefined&&(!Array.isArray(d.select)||d.select.length!==q||d.select.some(v=>!integer(v)||v>=cap)))throw Error('select');
    }
    G+=d.gates.length;
  }
  a.stages.forEach(d=>inspect(d,false));inspect(a.accept,true);
  return {a,G,B:raw.length};
}
function calc(d,r,z,s){
  let v=Array.from({length:s},(_,i)=>(r>>i)&1);v.push(z,0,1);
  for(let g of d.gates)v.push((g[2]>>((v[g[0]]<<1)|v[g[1]]))&1);
  return v;
}
function move(a,t,r,z){
  let d=a.stages[t],v=calc(d,r,z,a.s),index=d.index;
  if(d.select!==undefined){index=0;d.select.forEach((ref,i)=>index+=v[ref]*2**i);}
  let next=0;d.next.forEach((ref,i)=>next+=v[ref]*2**i);
  return {index,next};
}
function accept(a,r){let d=a.accept;return calc(d,r,0,a.s)[d.out];}
function runSource(a,x){let r=a.init,mask=0;
  for(let t=0;t<a.n;t++){
    let l=move(a,t,r,0),h=move(a,t,r,1),j=l.index;
    if(j!==h.index||j>=a.n||mask&(1<<j))throw Error('bad read-once source');
    mask|=1<<j;r=((x>>j)&1)?h.next:l.next;
  }
  return accept(a,r);
}
function compile(raw){
  let {a,G,B}=parse(raw),nodes=[],ids=new Map(),queue=[],seen=new Set();
  function id(t,r){if(t===a.n)return accept(a,r)?-2:-1;
    let key=t+','+r;if(!ids.has(key)){ids.set(key,nodes.length);nodes.push({t,r,index:-1,next:null});}return ids.get(key);
  }
  id(0,a.init);queue.push([0,a.init,0]);
  for(let head=0;head<queue.length;head++){
    let [t,r,mask]=queue[head],triple=t+','+r+','+mask;
    if(seen.has(triple))continue;seen.add(triple);
    if(seen.size>250000)throw Error('finite audit cutoff');
    let lo=move(a,t,r,0),hi=move(a,t,r,1),j=lo.index;
    if(j!==hi.index||!integer(j)||j>=a.n)throw Error('selector uses unread bit');
    if(mask&(1<<j))throw Error('repeated read');
    let targets=[id(t+1,lo.next),id(t+1,hi.next)],v=nodes[id(t,r)];
    if(v.next)ok(v.index===j&&v.next.every((u,i)=>u===targets[i]),'unsound state quotient');
    else{v.index=j;v.next=targets;}
    if(t+1<a.n)for(let nxt of [lo,hi])queue.push([t+1,nxt.next,mask|(1<<j)]);
  }
  ok(nodes.every(v=>v.index>=0&&v.next&&v.next.length===2),'uninitialized node');
  ok(nodes.length<=a.n*2**a.s,'node bound');
  ok(seen.size<=2**a.s*(2**a.n-1),'history bound');
  return {a,G,B,nodes,history:seen.size,outputBits:8*JSON.stringify(nodes).length};
}
function trace(c,x,mask){let node=0,last='',switches=[],steps=0;
  while(node>=0){let d=c.nodes[node],side=(mask&(1<<d.index))?'X':'Y';
    if(last&&last!==side)switches.push(node);
    last=side;node=d.next[(x>>d.index)&1];steps++;
    ok(steps<=c.a.n,'cycle');
  }
  return {value:node===-2?1:0,transcript:switches.join('/'),b:switches.length};
}
function rank(M,p){M=M.map(row=>row.slice());let r=0;
  for(let col=0;col<M[0].length&&r<M.length;col++){
    let k=r;while(k<M.length&&M[k][col]===0)k++;if(k===M.length)continue;
    [M[r],M[k]]=[M[k],M[r]];
    let inv=1;while(inv*M[r][col]%p!==1)inv++;
    for(let j=col;j<M[r].length;j++)M[r][j]=M[r][j]*inv%p;
    for(let i=0;i<M.length;i++)if(i!==r){let t=M[i][col];for(let j=col;j<M[i].length;j++)M[i][j]=(M[i][j]-t*M[r][j]%p+p)%p;}
    r++;
  }return r;
}
function audit(a,name){
  let c=compile(JSON.stringify(a)),n=a.n,k=Math.floor(n/2),X=(1<<k)-1,m=Array.from({length:2**k},()=>Array(2**(n-k)).fill(0)),groups=new Map(),b=0;
  for(let x=0;x<2**n;x++){
    let z=trace(c,x,X),y=runSource(a,x);ok(z.value===y,'source/target semantics');stats.assignments++;
    let row=x&X,col=x>>k;m[row][col]=y;b=Math.max(b,z.b);
    if(y){if(!groups.has(z.transcript))groups.set(z.transcript,[]);groups.get(z.transcript).push([row,col]);}
  }
  for(let pairs of groups.values()){let A=new Set(pairs.map(v=>v[0])),B=new Set(pairs.map(v=>v[1]));ok(pairs.length===A.size*B.size,'nonrectangular switch class');stats.rectangles++;}
  let r2=rank(m,2),r101=rank(m,101),V=c.nodes.length;
  let cap=0n;for(let i=0;i<=b;i++)cap+=BigInt(V)**BigInt(i);
  ok(BigInt(r2)<=cap&&BigInt(r101)<=cap,'rank/switch');
  if(c.nodes.every(v=>v.index===v.t))ok(r2<=2**a.s&&r101<=2**a.s,'fixed-order rank/state');
  stats.programs++;
  if(stats.samples.length<16)stats.samples.push({name,n,s:a.s,gates:c.G,sourceBytes:c.B,compiledNodes:V,historyStates:c.history,peakSwitches:b,rankGF2:r2,rankGF101:r101,acceptingRectangles:groups.size,serializedBpBits:c.outputBits});
}
function stage(s,j,mode,idx){
  let next=Array.from({length:s},(_,i)=>i),gates=[],z=s;
  if(mode==='store')next[idx]=z;
  if(mode==='pending')next[0]=z;
  if(mode==='and' || mode==='xor'){
    gates=[[idx,z,mode==='and'?8:6],[s+3,s-1,mode==='and'?14:6]];
    next[s-1]=s+4;
  }
  if(mode==='pending_and'||mode==='pending_xor'){
    gates=[[0,z,mode==='pending_and'?8:6],[s+3,1,mode==='pending_and'?14:6]];
    next[1]=s+4;
  }
  if(mode==='parity'){gates=[[0,z,6]];next[0]=s+3;}
  return {index:j,gates,next};
}
function terminal(s,bit,neg){return neg?{gates:[[bit,bit,3]],out:s+3}:{gates:[],out:bit};}
function family(k,inter,xor){
  let s=inter?2:k+1,d=[];
  if(inter)for(let i=0;i<k;i++){d.push(stage(s,i,'pending'));d.push(stage(s,k+i,xor?'pending_xor':'pending_and'));}
  else{for(let i=0;i<k;i++)d.push(stage(s,i,'store',i));for(let i=0;i<k;i++)d.push(stage(s,k+i,xor?'xor':'and',i));}
  return {version:1,n:2*k,s,init:0,stages:d,accept:terminal(s,s-1,true)};
}
function parity(n){return {version:1,n,s:1,init:0,stages:Array.from({length:n},(_,i)=>stage(1,i,'parity')),accept:terminal(1,0,false)};}
function adaptive(){
  let s=2,first=stage(s,0,'store',0);first.next[1]=s;
  return {version:1,n:3,s,init:0,stages:[first,
    {gates:[[0,0,3],[1,s,6]],select:[s+3,0],next:[0,s+4]},
    {gates:[[0,0,3],[1,s,6]],select:[0,s+3],next:[0,s+4]}],
    accept:terminal(s,1,false)};
}
function randomSource(n,s){
  let order=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){let j=rand()%(i+1);[order[i],order[j]]=[order[j],order[i]];}
  let d=order.map(j=>{let g=[],count=rand()%4;for(let i=0;i<count;i++)g.push([rand()%(s+3+i),rand()%(s+3+i),rand()%16]);
    return {index:j,gates:g,next:Array.from({length:s},()=>rand()%(s+3+count))};});
  return {version:1,n,s,init:rand()%(2**s),stages:d,accept:terminal(s,rand()%s,(rand()&1)!==0)};
}
for(let k=1;k<=3;k++){audit(family(k,true,false),'DISJ'+k+'_interleaved');audit(family(k,false,false),'DISJ'+k+'_grouped');audit(family(k,true,true),'EQ'+k+'_interleaved');audit(family(k,false,true),'EQ'+k+'_grouped');}
for(let n=2;n<=6;n++)audit(parity(n),'AFFINE_PARITY'+n);
audit(adaptive(),'ADAPTIVE_PARITY3');
for(let i=0;i<160;i++)audit(randomSource(1+rand()%5,1+rand()%3),'seeded_'+i);
function mustReject(a,match){let failed=false;try{compile(typeof a==='string'?a:JSON.stringify(a));}catch(e){failed=match.test(String(e.message));}ok(failed,'missing malformed reject');stats.malformed_rejected++;}
let r=family(2,true,false);r.stages[1].index=0;mustReject(r,/repeated/);
r=parity(3);r.stages[0].gates=[[1,1,8]];r.stages[0].select=[1,1];delete r.stages[0].index;mustReject(r,/selector uses/);
r=parity(2);r.stages[0].gates=[[999,0,8]];mustReject(r,/gate/);
mustReject('{not json',/Unexpected|JSON/);
const RESULT=stats;
if(typeof process!=='undefined'&&process.stdout)process.stdout.write(JSON.stringify(RESULT,null,2)+'\n');
