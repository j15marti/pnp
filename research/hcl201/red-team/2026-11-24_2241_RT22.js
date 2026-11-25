"use strict";
function main(){
 const st={assertions:0,closureScans:0,referenceWords:0,separatorPairs:0,adjReads:0,gadgetWords:0,lifts:0};const rows=[];
 const ck=(p,m)=>{st.assertions++;if(!p)throw Error(m)};
 const bits=(n,w)=>Array.from({length:n},(_,i)=>(w>>i)&1);
 const good=(x,[a,b,c])=>x[a]===x[b]||x[a]===x[c];
 const nae=(x,[a,b,c],sign=0)=>{let p=x[a]^(sign&1),q=x[b]^((sign>>1)&1),r=x[c]^((sign>>2)&1);return p!==q||q!==r};
 function close(n,R,pins=[]){let d=Array(n).fill(3);for(const [v,b] of pins){d[v]&=1<<b;if(!d[v])return null}for(;;){st.closureScans++;let ch=false;for(const t of R){const vs=[...new Set(t)],s=vs.map(()=>0);for(let w=0;w<2**vs.length;w++){let a=bits(vs.length,w);if(!a.every((b,i)=>d[vs[i]]&(1<<b)))continue;let z=t.map(v=>a[vs.indexOf(v)]);if(z[0]!==z[1]&&z[0]!==z[2])continue;a.forEach((b,i)=>s[i]|=1<<b)}for(let i=0;i<vs.length;i++){let v=vs[i],a=d[v]&s[i];if(!a)return null;if(a!==d[v]){ch=true;d[v]=a}}}if(!ch)return d}}
 function exact(n,R,pins=[],eq=[]){const d=close(n,R,pins);if(!d)return null;for(let w=0;w<2**n;w++){st.referenceWords++;let x=bits(n,w);if(x.every((b,i)=>d[i]&(1<<b))&&eq.every(([a,b])=>x[a]===x[b])&&R.every(t=>good(x,t)))return x}return null}
 const pairs=t=>[[t[0],t[1]],[t[0],t[2]],[t[1],t[2]]];
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 function repair(E,w,signs=[]){const R=[],bad=[];E.forEach((t,i)=>{let a=t.map((v,j)=>w[v]^(((signs[i]||0)>>j)&1));if(a.every(x=>x===a[0]))bad.push(t);else{let j=a.findIndex((x,j)=>x!==a[(j+1)%3]&&x!==a[(j+2)%3]);R.push([t[j],...t.filter((_,k)=>k!==j)])}});return{R,bad}}
 function pad(n,R,k){let A=R.map(t=>t.slice()),g=[];for(let i=0;i<k;i++){let u=i%n,v=(i+1)%n,[p,q,r,s,t]=Array.from({length:5},(_,j)=>n+5*i+j);let B=[[u,p,q],[v,r,s],[p,r,t],[q,s,t]];A.push(...B);g.push({u,v,p,q,r,s,t,B})}return{n:n+5*k,R:A,g}}
 function adj(n,R,primal){let a=Array.from({length:n},()=>new Set);for(let t of R)for(let [u,v] of (primal?pairs(t):[[t[0],t[1]],[t[0],t[2]]])){a[u].add(v);a[v].add(u)}return a}
 function comps(a,ban){let seen=new Set(ban),out=[];for(let i=0;i<a.length;i++)if(!seen.has(i)){let q=[i];seen.add(i);for(let j=0;j<q.length;j++)for(let v of a[q[j]]){st.adjReads++;if(!seen.has(v)){seen.add(v);q.push(v)}}out.push(q)}return out}
 function sep(n,R,s,t){let a=adj(n,R,true);for(let u=0;u<n;u++)for(let v=u+1;v<n;v++){st.separatorPairs++;let c=comps(a,[u,v]);if(c.length<=1)continue;for(let z of c)if(!z.includes(s)&&!z.includes(t)){let S=new Set(z),B=R.filter(e=>e.some(x=>S.has(x)));if(B.length&&B.length<R.length)return{u,v,B}}}return null}
 const lift=(x,g)=>{let z=x.slice();for(let a of g){z[a.p]=z[a.r]=0;z[a.q]=z[a.s]=1;z[a.t]=0}st.lifts++;return z};
 const g=pad(2,[],1).g[0], counts=[];
 for(let a=0;a<2;a++)for(let b=0;b<2;b++){let c=0;for(let w=0;w<32;w++){st.gadgetWords++;let x=[a,b,...bits(5,w)];if(g.B.every(t=>good(x,t)))c++}ck(c>0,"neutral");counts.push(c)}
 rows.push({test:"neutral gadget boundary extension counts (00,01,10,11)",counts});
 // Compare adaptive separator decision with entire exact union. B is either a neutral gadget or Fano-minus-line equality relation.
 const A=[[0,1,2],[2,1,3]], B0=[[0,4,5],[1,6,7],[4,6,8],[5,7,8]];
 let anchor=repair(fano,bits(7,7));ck(anchor.bad.length===1,"Fano anchor");
 const bad=anchor.bad[0],u=bad[0],v=bad[1];let map=new Map([[u,0],[v,1]]),j=4;for(let i=0;i<7;i++)if(!map.has(i))map.set(i,j++);const B1=anchor.R.map(t=>t.map(i=>map.get(i)));
 for(let [B,n] of [[B0,9],[B1,9]]){const b=exact(n,B,[[0,0],[1,1]]);for(let s=0;s<4;s++)for(let t=s+1;t<4;t++){let pins=[[s,0],[t,1]];close(n,A.concat(B),pins);let x=exact(n,A,pins,b?[]:[[0,1]]),ref=exact(n,A.concat(B),pins);ck(!!x===!!ref,"adaptive separator equivalence");if(x){let y=exact(n,B,[[0,x[0]],[1,x[1]]]);ck(!!y,"lift B");let z=x.slice();for(let i=4;i<n;i++)z[i]=y[i];ck(A.concat(B).every(t=>good(z,t))&&z[s]===0&&z[t]===1,"lift verified");st.lifts++}}rows.push({test:"adaptive projection",B:B===B0?"neutral":"Fano equality",opposite:!!b})}
 let fn={anchors:0,unsat:0,satOtherPair:0,closureRejects:0};for(let w=0;w<128;w++){let {R,bad}=repair(fano,bits(7,w));if(bad.length!==1)continue;fn.anchors++;for(let [s,t] of pairs(bad[0])){let p=[[s,0],[t,1]];fn.closureRejects+=+(!close(7,R,p));ck(!exact(7,R,p),"Fano bad pair");fn.unsat++}let found=false;for(let s=0;s<7;s++)for(let t=s+1;t<7;t++)if(exact(7,R,[[s,0],[t,1]]))found=true;ck(found,"same registry SAT pair");fn.satOtherPair++}rows.push({test:"Fano exact source IDs",...fn});
 let signs=0;for(let i=0;i<7;i++)for(let k=0;k<3;k++){let sg=Array(7).fill(0);sg[i]=1<<k;let count=0;for(let w=0;w<128;w++){st.referenceWords++;if(fano.every((t,j)=>nae(bits(7,w),t,sg[j])))count++}ck(count===10,"sign neighbor");signs++}rows.push({test:"Fano sign neighbors",signs});
 // Plane same coordinates as BH16/M22.
 let plane=[];for(let c=0;c<3;c++)plane.push([0,1,2].map(i=>3*i+c));for(let c=0;c<3;c++)plane.push([0,1,2].map(j=>3*c+j));for(let a of [1,2])for(let c=0;c<3;c++)plane.push([0,1,2].map(i=>3*i+(a*i+c)%3));
 let best=null,pc=0;for(let w=0;w<512;w++){let x=bits(9,w),r=repair(plane,x);if(!best||r.bad.length<best.bad.length)best={...r,w:x};if(plane.every(t=>nae(x,t)))pc++}ck(pc===0&&best.bad.length===2,"plane");rows.push({test:"M22 plane",models:pc,minBad:best.bad.length,anchor:best.w,bad:best.bad,cutBound:20,required:24});
 // Same near-anchor registry; change only seed pair. All k>=7 yield biconnected sparse host and min owner-degree >=2.
 let R=anchor.R,[s,t]=pairs(anchor.bad[0])[0], sat=null;for(let i=0;i<7&&!sat;i++)for(let j=i+1;j<7&&!sat;j++){let z=exact(7,R,[[i,0],[j,1]]);if(z)sat={i,j,z}}ck(!!sat,"neighbor");
 for(let k of [7,14,28,56]){let p=pad(7,R,k),a=adj(p.n,p.R,false),ds=Array(p.n).fill(0);p.R.flat().forEach(v=>ds[v]++);ck(ds.every(d=>d>=2),"min owner degree");ck(a.reduce((s,x)=>s+x.size,0)===4*p.R.length,"simple paired edges");ck(2*p.R.length<=2*p.n,"density");ck(comps(a,[]).length===1,"connected");for(let i=0;i<p.n;i++)ck(comps(a,[i]).length===1,"2-connected");let z=lift(sat.z,p.g);ck(p.R.every(t=>good(z,t))&&z[sat.i]!==z[sat.j],"padded SAT lift");let sp=sep(p.n,p.R,s,t);ck(!!sp,"2-separator discovered");let d=close(p.n,p.R,[[s,0],[t,1]]);ck(!!d,"padded singleton stagnates");rows.push({test:"same registry seed neighbors",k,n:p.n,m:p.R.length,unsatSeed:[s,t],satSeed:[sat.i,sat.j],firstSeparator:[sp.u,sp.v],sideOwners:sp.B.length,certifiedSatLift:true,closureRejected:false})}
 // Actual BS15 map copied from BH16 code, verified witness, no raw two-separator if returned null.
 for(let q of [1,2,4]){let L=12*q,E=[],id=(i,j)=>3*((i+L)%L)+(j+3)%3;for(let i=0;i<L;i++)for(let j=0;j<3;j++)E.push([id(i,j),id(i+1,j),id(i+1,j+1)]);for(let b=0;b<q;b++)for(let j=0;j<3;j++){let temp=j===2?[[0,2,5],[1,3,10],[4,7,9],[6,8,11]]:[[0,2,5],[1,3,8],[4,7,10],[6,9,11]];if(b===0&&j===0)temp=[[0,4,8],[1,3,6],[2,9,11],[5,7,10]];for(let t of temp)E.push(t.map(i=>id(12*b+i,j)))}let n=3*L,w=Array.from({length:n},(_,i)=>Math.floor(i/3)%2),r=repair(E,w),z=Array.from({length:n},(_,i)=>+(i%3===Math.floor(i/3)%3)),x=z.map((b,i)=>b^w[i]);ck(r.bad.length===1&&E.every(t=>nae(x,t)),"BS15 known witness");let out=[];for(let [s,t] of pairs(r.bad[0])){close(n,r.R,[[s,0],[t,1]]);let p=sep(n,r.R,s,t);out.push({seed:[s,t],separator:p?[p.u,p.v]:null,knownWitnessSeparates:z[s]!==z[t]})}rows.push({test:"BS15 actual ring",q,n,results:out})}
 return{st,rows};
}
console.log(JSON.stringify(main(),null,2));
