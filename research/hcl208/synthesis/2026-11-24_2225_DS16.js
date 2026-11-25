"use strict";
function runDS16(){
 let checks=0,nodes=0,scans=0;
 const ok=(b,m)=>{checks++;if(!b)throw Error(m||"assertion")};
 const legal=(e,w)=>e.v.some(v=>w[v]!==w[e.v[0]]);
 const E=(p,v)=>({p,v});
 function plane(){let es=[];for(let a=0;a<3;a++)for(let b=0;b<3;b++)es.push(E(a,[0,1,2].map(i=>3*i+(a*i+b)%3)));for(let i=0;i<3;i++)es.push(E(3,[3*i,3*i+1,3*i+2]));return {n:9,es}}
 function ring(q){let L=12*q,es=[];for(let i=0;i<L;i++)for(let j=0;j<3;j++)es.push(E((i+j)%3,[3*i+j,3*((i+1)%L)+j,3*((i+1)%L)+(j+1)%3]));for(let b=0;b<q;b++)for(let j=0;j<3;j++){let t=b===0&&j===0?[[0,4,8],[1,3,6],[2,9,11],[5,7,10]]:j===2?[[0,2,5],[1,3,10],[4,7,9],[6,8,11]]:[[0,2,5],[1,3,8],[4,7,10],[6,9,11]];for(let a of t)es.push(E(3,a.map(i=>3*(12*b+i)+j)))}return {n:3*L,es}}
 function check(n,es,full){let incidence=Array.from({length:n},()=>Array(4).fill(0)),pairs=new Set();for(let {p,v} of es){ok(v.length===3&&new Set(v).size===3&&p>=0&&p<4);for(let a of v){ok(a>=0&&a<n);ok(++incidence[a][p]===1)}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let k=[v[i],v[j]].sort((a,b)=>a-b).join(",");ok(!pairs.has(k),"linearity");pairs.add(k)}}if(full)for(let a of incidence)ok(a.every(x=>x===1),"perfect partition");return incidence}
 const P=plane(), G=P.es.filter((_,i)=>i!==0&&i!==1);
 let gmodels=[];for(let k=0;k<512;k++){let w=Array.from({length:9},(_,i)=>(k>>i)&1);ok(!P.es.every(e=>legal(e,w)));if(G.every(e=>legal(e,w))){ok(w[1]===w[4]&&w[4]===w[7]);gmodels.push(w)}}
 ok(gmodels.length===12);ok(new Set(gmodels.map(w=>w[1])).size===2);
 function addSlack(src){let es=src.es.slice(),n=src.n,seen=new Set(),roots=[];
 const adj=Array.from({length:src.n},()=>[]);src.es.forEach((e,i)=>e.v.forEach(v=>adj[v].push(i)));
 for(let i=0;i<src.es.length;i++){if(seen.has(i))continue;let Q=[i];seen.add(i);for(let h=0;h<Q.length;h++)for(let v of src.es[Q[h]].v)for(let j of adj[v])if(!seen.has(j)){seen.add(j);Q.push(j)}
 let old=src.es[i],p=old.p;es=es.filter(e=>e!==old);let outs=[];
 for(let a of old.v){let o=n;n+=9;for(let e of G)es.push(E((p+e.p)%4,e.v.map(v=>o+v)));es.push(E(p,[a,o+1,o+4]));outs.push(o+7);roots.push(o)}
 es.push(E(p,outs))}
 check(n,es,false);return {n,es,roots}}
 function ordering(src){let inc=check(src.n,src.es,false),adj=Array.from({length:src.n},()=>[]);src.es.forEach((e,i)=>e.v.forEach(v=>adj[v].push(i)));let seen=new Set(),order=[];
 for(let i=0;i<src.es.length;i++){if(seen.has(i)||!src.es[i].v.some(v=>inc[v].includes(0)))continue;let Q=[i];seen.add(i);for(let h=0;h<Q.length;h++)for(let v of src.es[Q[h]].v)for(let j of adj[v])if(!seen.has(j)){seen.add(j);Q.push(j)}order.push(...Q.reverse())}
 ok(order.length===src.es.length,"every component has slack");return order.map(i=>src.es[i])}
 function completion(n,es,w){let inc=check(n,es,false),out=es.slice(),z=w.slice(),N=n,fill=0;
 for(let p=0;p<4;p++){let miss=[];for(let v=0;v<n;v++)if(!inc[v][p])miss.push(v);ok(miss.length%3===0);
 for(let h=0;h<miss.length;h+=3){let o=N;N+=42;fill++;for(let c=0;c<2;c++)for(let j=0;j<21;j++)z.push((j>=7&&j<14?1:0)^c);
 for(let c=0;c<2;c++)for(let q=0;q<4;q++)for(let k=0;k<7;k++){if(q===p&&k===0)continue;out.push(E(q,[0,7+(k+q)%7,14+(k+2*q)%7].map((v,j)=>o+21*c+(j===0?k:v))))}
 let a=[0,7+p,14+2*p];for(let j=0;j<3;j++)out.push(E(p,[miss[h+j],o+a[j],o+21+a[j]]))}}
 check(N,out,true);for(let e of out.slice(es.length))ok(legal(e,z),"transparent filler");return {n:N,es:out,w:z,fill}}
 function solve(n,es,prefer){function rec(a){nodes++;let changed=true;while(changed){changed=false;scans++;for(let e of es){let s=e.v.map(v=>a[v]),u=e.v.filter(v=>a[v]<0),known=s.filter(v=>v>=0);if(known.includes(0)&&known.includes(1))continue;if(!u.length)return null;if(u.length===1){a[u[0]]=1-known[0];changed=true}}}
 let e=es.find(e=>!(e.v.some(v=>a[v]===0)&&e.v.some(v=>a[v]===1)));if(!e)return a.map((x,i)=>x<0?prefer[i]:x);let v=e.v.find(v=>a[v]<0);for(let b of [prefer[v],1-prefer[v]]){let next=a.slice();next[v]=b;let w=rec(next);if(w)return w}return null}return rec(Array(n).fill(-1))}
 function verifyFlow(es,w,p,q){let a=es.filter(e=>e.p===p),b=es.filter(e=>e.p===q);let sa=0,sb=0;for(let e of a){let s=e.v.reduce((t,v)=>t+w[v],0);ok(s===1||s===2);sa+=s}for(let e of b){let s=e.v.reduce((t,v)=>t+w[v],0);ok(s===1||s===2);sb+=s}ok(sa===sb&&sa===w.reduce((t,v)=>t+v,0),"hub balance")}
 let cases=[];
 for(let [name,src] of [["M22 plane",P],["BS15 q=1",ring(1)],["BS15 q=2",ring(2)]]){
 check(src.n,src.es,true);let T=addSlack(src),order=ordering(T),prefix=[],w=Array(T.n).fill(0),repairs=0,maxN=0,outcome=true,firstRepair=null,lastRepair=null;
 for(let e of order){prefix.push(e);let inc=check(T.n,prefix,false);let v=e.v.find(v=>inc[v].some((c,q)=>c===0&&q!==e.p));ok(v!==undefined,"activation slack");
 if(legal(e,w))continue;
 let q=inc[v].findIndex((c,q)=>!c&&q!==e.p),rem=[0,1,2,3].filter(c=>c!==q&&c!==e.p);
 let C=completion(T.n,prefix,w),y=C.w.slice(),x=y.slice();x[v]^=1;maxN=Math.max(maxN,C.n);
 ok(C.es.filter(e=>!legal(e,y)).length===1);verifyFlow(C.es,x,e.p,q);verifyFlow(C.es,y,...rem);verifyFlow(C.es,x.map(b=>1-b),e.p,q);verifyFlow(C.es,y.map(b=>1-b),...rem);
 ok(x.filter((b,i)=>b!==y[i]).length===1);repairs++;let info={step:prefix.length,seed:v,pair:[e.p,q],n:C.n,fill:C.fill};if(!firstRepair)firstRepair=info;lastRepair=info;
 let z=solve(T.n,prefix,w);if(!z){outcome=false;break}
 let lift=completion(T.n,prefix,z);ok(lift.es.every(e=>legal(e,lift.w)));verifyFlow(lift.es,lift.w,e.p,q);verifyFlow(lift.es,lift.w,...rem);
 w=z;ok(prefix.every(e=>legal(e,w)))}
 if(outcome){ok(src.es.every(e=>legal(e,w)));let a=w.slice(0,src.n);for(let b of [0,1]){let z=a[0]===b?a:a.map(x=>1-x);ok(z[0]===b&&src.es.every(e=>legal(e,z)))}}
 ok(outcome===(name!=="M22 plane"));cases.push({name,sourceN:src.n,partialN:T.n,partialOwners:T.es.length,processed:prefix.length,repairs,maxCompletedN:maxN,outcome,firstRepair,lastRepair})}
 return {checks,referenceDpllNodes:nodes,referencePropagationScans:scans,gadgetModels:gmodels.length,cases}
}
console.log(JSON.stringify(runDS16(),null,2));
