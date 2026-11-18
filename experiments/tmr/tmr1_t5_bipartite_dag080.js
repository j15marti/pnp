#!/usr/bin/env node
"use strict";
// Complete deterministic standalone V8/Node verifier, no dependencies.
// Execute: node experiments/tmr/tmr1_t5_bipartite_dag080.js
const result=(function verify080(){
 "use strict";
 let checks=0,graphs=0,valuations=0,yes=0,no=0,gadgetChecks=0,witnesses=0,invalid=0;
 function A(v,m){checks++;if(!v)throw Error("FAIL: "+m);}
 const md=x=>(x%5+5)%5,R=(a,b)=>[1,3].includes(md(b-a)),w=n=>Math.max(1,Math.ceil(Math.log2(Math.max(n,2))));
 const enc=(x,k)=>Array.from({length:k},(_,i)=>(x>>i)&1).join("");
 function serialize(n,E,dir){const S=E.map(p=>p.slice()).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);for(let i=0;i<S.length;i++){let [u,v]=S[i];A(u>=0&&u<n&&v>=0&&v<n&&u!==v&&(!dir?u<v:true),"edge range");if(i)A(S[i-1][0]<u||(S[i-1][0]===u&&S[i-1][1]<v),"edge order");}return "1".repeat(n)+"0"+"1".repeat(S.length)+"0"+S.map(([a,b])=>enc(a,w(n))+enc(b,w(n))).join("");}
 function parse(s,dir){if(!/^[01]*$/.test(s))throw Error("alphabet");let i=0,n=0,m=0;while(s[i]==="1"){n++;i++;}if(s[i++]!=="0")throw Error("n delimiter");while(s[i]==="1"){m++;i++;}if(s[i++]!=="0")throw Error("m delimiter");const k=w(n);if(s.length-i!==2*m*k)throw Error("length");function read(){let v=0;for(let j=0;j<k;j++)v+=(s[i++]==="1"?2**j:0);return v;}let E=[];for(let j=0;j<m;j++){let a=read(),b=read();if(a<0||b<0||a>=n||b>=n||a===b||(!dir&&a>=b))throw Error("bad endpoints");if(j&&!(E[j-1][0]<a||(E[j-1][0]===a&&E[j-1][1]<b)))throw Error("order");E.push([a,b]);}return {n,E};}
 function D(n,E){const arcs=[];for(let i=0;i<E.length;i++){const [u,v]=E[i],a=n+3*i,b=a+1,c=a+2;arcs.push([u,a],[a,b],[b,c],[u,c],[c,v]);}return {n:n+3*E.length,arcs};}
 const tab=Array.from({length:5},()=>Array(5).fill(0));
 for(let u=0;u<5;u++)for(let v=0;v<5;v++){let cnt=0;for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++){gadgetChecks++;if(R(u,a)&&R(a,b)&&R(b,c)&&R(u,c)&&R(c,v)){cnt++;A(a===md(u+1)&&b===md(u+2)&&c===md(u+3),"not unique");}}const d=md(v-u);A(cnt===((d===1||d===4)?1:0),"gadget endpoint");tab[u][v]=cnt;}
 for(let n=0;n<=5;n++){const pairs=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)pairs.push([u,v]);for(let mask=0;mask<2**pairs.length;mask++){const E=pairs.filter((p,i)=>(mask>>>i)&1),source=serialize(n,E,false),back=parse(source,false);A(back.n===n&&JSON.stringify(back.E)===JSON.stringify(E),"source roundtrip");const G=D(n,E),target=serialize(G.n,G.arcs,true),got=parse(target,true);A(got.n===n+3*E.length&&got.E.length===5*E.length,"target roundtrip");A(target.length<=15*source.length,"encoded length");
 const rank=t=>t<n?4*t:4*E[Math.floor((t-n)/3)][0]+(t-n)%3+1,partition=t=>t<n?0:(((t-n)%3)===1?0:1);
 for(const [a,b] of G.arcs){A(rank(a)<rank(b),"DAG");A(partition(a)!==partition(b),"bipartite");}
 let cs=0,ct=0;
 for(let x=0;x<5**n;x++){valuations++;let r=x,labels=[];for(let j=0;j<n;j++){labels.push(r%5);r=Math.floor(r/5);}const proper=E.every(([a,b])=>[1,4].includes(md(labels[b]-labels[a])));let f=1;for(const [a,b] of E)f*=tab[labels[a]][labels[b]];ct+=f;
 if(proper){cs++;witnesses++;let complete=labels.slice();for(const [a,b] of E)complete.push(md(labels[a]+1),md(labels[a]+2),md(labels[a]+3));A(complete.length===G.n&&G.arcs.every(([a,b])=>R(complete[a],complete[b])),"witness");}}
 A(cs===ct,"count");graphs++;cs?yes++:no++;}}
 const s=serialize(3,[[0,1],[1,2]],false),bad=["",s+"0",s.slice(0,-1),"1","a0","10","1110110"+enc(0,2)+enc(1,2)+enc(0,2)+enc(1,2),"1110110"+enc(0,2)+enc(0,2)+enc(1,2)+enc(2,2)];
 for(const x of bad){try{parse(x,false);}catch(e){invalid++;}}
 A(invalid>=7,"malformed controls");
 let tri=false;for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++)if([[a,b],[a,c],[b,c]].every(([x,y])=>[1,4].includes(md(y-x))))tri=true;A(!tri,"K3 NO image");
 return {revision:"tmr1-t5-bipartite-dag-triadfree080-js-v2",gadgetEndpointCounts:tab[0],gadgetAssignmentsChecked:gadgetChecks,undirectedGraphs:graphs,sourceLabelingsChecked:valuations,yesGraphs:yes,noGraphs:no,satisfyingWitnessesValidated:witnesses,malformedRejections:invalid,assertions:checks,failures:0,scope:"finite checks; theorem symbolic",notes:"Each graph count uses factorization of private gadgets, not full 5^(n+3m) target enumeration",bitRatioBoundValidCanonicalInputs:15};
})();
console.log(JSON.stringify(result,null,2));
