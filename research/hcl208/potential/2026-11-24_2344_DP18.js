// DP18 finite reference checker. Run: node 2026-11-24_2344_DP18.js DR17.json BW17.json M23.json
// Immutable input commits: af8584879409ad3364795d50902f02b5a030bd2a, 9164cb11c6fcdf96d470de9d86b061e3201a591f, a412bf23a0b63f03c886b7bf5bd50217b5502db2
"use strict";
function run(data){
 const stats={assertions:0,rowXors:0,closureScans:0,forces:0,referenceWords:0,splitTests:0,creditTests:0,lifts:0,queryTests:0};
 const ok=(x,msg)=>{stats.assertions++;if(!x)throw Error(msg)};
 const bit=i=>1n<<BigInt(i), hi=x=>x.toString(2).length-1;
 const par=x=>{let p=0;while(x){p^=1;x&=x-1n}return p};
 const val=(x,r)=>par(x&r);
 const canon=rows=>{
  const B=new Map();
  for(let [r,v] of rows){
   for(const [i,[a,b]] of [...B].sort((x,y)=>y[0]-x[0]))if(r&bit(i)){r^=a;v^=b;stats.rowXors++}
   if(!r){if(v)return null;continue}
   const i=hi(r);
   for(const [j,[a,b]] of B)if(a&bit(i)){B.set(j,[a^r,b^v]);stats.rowXors++}
   B.set(i,[r,v]);
  }
  return [...B].sort((x,y)=>y[0]-x[0]).map(x=>x[1])
 };
 const reduce=(rows,G)=>canon(rows.map(([r,v])=>{for(const [a,b] of G)if(r&bit(hi(a))){r^=a;v^=b;stats.rowXors++}return [r,v]}));
 const key=p=>p.map(([r,v])=>r.toString()+":"+v).join(",");
 const mass=P=>P.reduce((s,p)=>s+p.length,0);
 const accepts=(P,x)=>P.every(p=>!p.every(([r,v])=>val(x,r)===v));
 const satisfies=(G,x)=>G.every(([r,v])=>val(x,r)===v);
 const close=(P,guard=[])=>{
  let G=canon(guard);if(G===null)return {bad:true};
  while(true){let out=[],seen=new Set(),force=null;
   for(const p of P){stats.closureScans++;let q=reduce(p,G);if(q===null)continue;if(!q.length)return {bad:true};
    if(q.length===1){force=[q[0][0],q[0][1]^1];break}
    if(!seen.has(key(q))){seen.add(key(q));out.push(q)}
   }
   if(!force)return {bad:false,P:out,G};
   G=canon([...G,force]);stats.forces++;if(G===null)return {bad:true}
  }
 };
 const basis=P=>canon(P.flat().map(([r])=>[r,0])).map(([r])=>r);
 const inter=(A,B)=>{
  const a=basis(A),b=basis(B),M=new Map(a.map(r=>[hi(r),[r,0n]])),I=[];
  for(const v of b){let r=v,t=v;
   while(r){let h=hi(r);if(!M.has(h)){M.set(h,[r,t]);break}
    const [u,w]=M.get(h);r^=u;t^=w;stats.rowXors++
   }
   if(!r)I.push(t)
  }
  ok(I.length===a.length+b.length-basis([...A,...B]).length,"intersection dimension");
  return I
 };
 const obs=(I,x)=>I.reduce((s,r,i)=>s+val(x,r)*2**i,0);
 const solve=rows=>{const q=canon(rows);if(q===null)return null;return q.reduce((x,[r,v])=>v?x|bit(hi(r)):x,0n)};
 const gate=(a,b,d)=>{if(b>a)[a,b]=[b,a];const Q=1n<<BigInt(d),H=BigInt(d)*Q;return b>=1&&Q*BigInt(b+1)<=BigInt(a+b+1)&&2n*H<=BigInt(b-1)};
 const credit=(a,b,d)=>{if(b>a)[a,b]=[b,a];const Q=1n<<BigInt(d),H=BigInt(d)*Q;return Q*BigInt(b+1)**4n+(BigInt(a)+H+1n)**4n < BigInt(a+b+1)**4n};
 const nae=(t,flip=-1)=>[[bit(t[0])^bit(t[1]),Number(flip===0||flip===1)],[bit(t[0])^bit(t[2]),Number(flip===0||flip===2)]];
 const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const small=[];
 function finite(name,n,P,G=[]){
  let C=close(P,G),words=[];for(let x=0n;x<bit(n);x++){stats.referenceWords++;if(satisfies(G,x)&&accepts(P,x))words.push(x)}
  if(C.bad){ok(!words.length,"closure false reject");return {name,models:0,closed:true}}
  for(let x=0n;x<bit(n);x++){stats.referenceWords++;ok((satisfies(G,x)&&accepts(P,x))===(satisfies(C.G,x)&&accepts(C.P,x)),"closure equivalence")}
  let checked=0;
  for(let cut=1;cut<C.P.length;cut++){
   const A=C.P.slice(0,cut),B=C.P.slice(cut),I=inter(A,B),d=I.length,S=new Map();
   for(let x=0n;x<bit(n);x++){stats.referenceWords++;if(satisfies(C.G,x)&&accepts(B,x))S.set(obs(I,x),x)}
   for(let s=0;s<2**d;s++){
    const J=I.map((r,i)=>[r,(s>>i)&1]),child=close(B,[...C.G,...J]);stats.queryTests++;
    let has=false;if(!child.bad)for(let x=0n;x<bit(n);x++){stats.referenceWords++;if(satisfies(child.G,x)&&accepts(child.P,x)){has=true;break}}
    ok(has===S.has(s),"support query after closure")
   }
   const missing=[];for(let s=0;s<2**d;s++)if(!S.has(s))missing.push(I.map((r,i)=>[r,(s>>i)&1]));
   let found=false;for(let x=0n;x<bit(n);x++){stats.referenceWords++;
    if(!satisfies(C.G,x)||!accepts([...A,...missing],x))continue;
    found=true;const y=S.get(obs(I,x));ok(y!==undefined,"unsupported continuation");
    const z=solve([...C.G,...basis(A).map(r=>[r,val(x,r)]),...basis(B).map(r=>[r,val(y,r)])]);
    ok(z!==null&&satisfies(G,z)&&accepts(P,z),"lift failed");stats.lifts++;break
   }
   ok(found===Boolean(words.length),"split label");checked++
  }
  return {name,models:words.length,splitChecks:checked}
 }
 small.push(finite("Fano",7,F.map(t=>nae(t))));
 for(let i=0;i<7;i++){small.push(finite("Fano deletion "+i,7,F.filter((_,j)=>i!==j).map(t=>nae(t))));for(let k=0;k<3;k++)small.push(finite("Fano sign "+i+"/"+k,7,F.map((t,j)=>nae(t,i===j?k:-1))));
 for(let v=0;v<2;v++)small.push(finite("Fano budget "+i+"/"+v,7,F.map((t,j)=>i===j?t.map(q=>[bit(q),v]):nae(t))))}
 let seed=20261124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 for(let j=0;j<80;j++){let n=5+rnd(4),P=[];for(let k=0;k<5+rnd(5);k++){let p=[];for(let r=0;r<1+rnd(3);r++)p.push([BigInt(1+rnd(2**n-1)),rnd(2)]);P.push(p)}let G=j%3===0?[[BigInt(1+rnd(2**n-1)),rnd(2)]]:[];small.push(finite("random "+j,n,P,G))}
 const growth=[];for(let d=0;d<=12;d++){const Q=2**d,H=d*Q,b=2*H+1,a=Math.max(b,Q*(b+1)-b-1);ok(gate(a,b,d)&&credit(a,b,d),"growth gate");growth.push({d,Q,H,a,b,ratio:Number((BigInt(Q)*BigInt(b+1)**4n+(BigInt(a+H+1))**4n)*1000000n/BigInt(a+b+1)**4n)/1000000})}
 for(let a=1;a<=160;a++)for(let b=1;b<=a;b++)for(let d=0;d<=7;d++)if(gate(a,b,d)){stats.creditTests++;ok(credit(a,b,d),"credit gate")}
 function scan(name,O,n,pin,witness){
  const P=O.map(o=>nae(o.t)),G=pin<0?[]:[[1n,pin]],C=close(P,G);
  ok(!C.bad&&C.P.length===P.length&&mass(C.P)===mass(P),"common closure changed");
  let valid=satisfies(G,witness)&&accepts(P,witness);ok(valid,"peer witness failed");
  const m=O.length,seen=new Set(),hist={},eligible=[];let examined=0;
  const check=idx=>{let s=new Set(idx);if(!s.size||s.size===m)return;if(s.size>m/2||s.size===m/2&&s.has(0))s=new Set(Array.from({length:m},(_,i)=>i).filter(i=>!s.has(i)));
   const k=[...s].sort((a,b)=>a-b).join(",");if(seen.has(k))return;seen.add(k);examined++;stats.splitTests++;
   const B=C.P.filter((_,i)=>s.has(i)),A=C.P.filter((_,i)=>!s.has(i)),d=inter(A,B).length,a=mass(A),b=mass(B);
   hist[d]=(hist[d]||0)+1;if(gate(a,b,d)){ok(credit(a,b,d),"common credit");eligible.push({idx:[...s],a,b,d})}
  };
  const adj=O.map((o,i)=>O.map((p,j)=>i!==j&&o.t.some(v=>p.t.includes(v))?j:-1).filter(j=>j>=0));
  for(let root=0;root<m;root++){let q=[root],v=new Set(q);for(let i=0;i<q.length;i++){for(const j of adj[q[i]])if(!v.has(j)){v.add(j);q.push(j)}}
   for(let j=1;j<q.length;j++)check(q.slice(0,j))
  }
  for(let j=1;j<m;j++)check(Array.from({length:j},(_,i)=>i));
  for(let s=1;s<15;s++)check(O.map((o,i)=>(s>>o.p)&1?i:-1).filter(i=>i>=0));
  return {name,n,pin,m,examined,hist,eligible,peerWitnessVerified:valid,positiveCutReject:2*m>Math.floor(n*n/4)}
 }
 const [dr,bw,mt]=data;
 const arrWord=a=>a.reduce((s,v,i)=>v?s|bit(i):s,0n);
 const common=[scan("DR17",dr.registry,36,-1,arrWord(dr.witness)),scan("BW17",bw.O,bw.n,-1,BigInt(bw.z))];
 for(const j of mt.jobs){const p=j.both.path.at(-1);common.push(scan("M23 "+j.k+"/"+j.pin,mt.owners,mt.n,j.pin,BigInt(p.x)))}
 return {stats,growth,finite:{cases:small.length,sat:small.filter(x=>x.models>0).length,unsat:small.filter(x=>!x.models).length,details:small},common};
}
const fs=require("fs");const data=process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,"utf8")));console.log(JSON.stringify(run(data),null,2));
