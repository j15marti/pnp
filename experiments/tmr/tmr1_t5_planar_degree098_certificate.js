'use strict';
// TMR-1/098. Dependency-free computational verification; theorem has separate proof.
const assert=require('node:assert/strict');
const R=(x,y)=>[1,3].includes((y-x+5)%5);
const C=(x,y)=>[1,4].includes((y-x+5)%5);
let checks=0, graphs=0, subcubic=0, targetEnumerations=0, assignments=0;
function ok(t,msg){checks++;assert.ok(t,msg);}
const pow=(n,k)=>n**k;
const label=(t,n)=>{let a=[];for(let i=0;i<n;i++){a.push(t%5);t=Math.floor(t/5);}return a;};
function sourceEdges(n,mask){let e=[],j=0;for(let u=0;u<n;u++)for(let v=u+1;v<n;v++,j++)if(mask&2**j)e.push([u,v]);return e;}
function target(n,E){let arcs=[];for(let j=0;j<E.length;j++){let [u,v]=E[j],a=n+2*j,b=a+1;arcs.push([u,a],[a,v],[v,b],[b,u]);}return {N:n+2*E.length,arcs};}
function countHom(n,E,test){let ans=0n;for(let z=0;z<pow(5,n);z++){let a=label(z,n);if(E.every(([u,v])=>test(a[u],a[v])))ans++;}return ans;}
let W=[];for(let x=0;x<5;x++){let row=[];for(let y=0;y<5;y++){
 let fa=0,back=0,full=0;
 for(let z=0;z<5;z++){if(R(x,z)&&R(z,y))fa++;if(R(y,z)&&R(z,x))back++;}
 for(let a=0;a<5;a++)for(let b=0;b<5;b++)if(R(x,a)&&R(a,y)&&R(y,b)&&R(b,x))full++;
 ok(full===fa*back);ok(full===(C(x,y)?2:0));row.push(full);
 }W.push(row);}
for(let n=0;n<=6;n++){
 const possibilities=n*(n-1)/2;
 for(let mask=0;mask<2**possibilities;mask++){
  const E=sourceEdges(n,mask),m=E.length,degree=Array(n).fill(0);
  E.forEach(([u,v])=>{degree[u]++;degree[v]++;});
  if(Math.max(0,...degree)>3)continue;
  subcubic++;
  const {N,arcs}=target(n,E);let ind=Array(N).fill(0),out=Array(N).fill(0),udeg=Array(N).fill(0);
  for(let [u,v] of arcs){out[u]++;ind[v]++;udeg[u]++;udeg[v]++;ok(u!==v);}
  ok(N===n+2*m);ok(arcs.length===4*m);
  ok(ind.every((d,i)=>d===out[i]));
  ok(ind.every((d,i)=>i>=n?d===1:d===degree[i]));
  ok(udeg.every(d=>d<=6));
  ok(arcs.every(([u,v])=>(u<n)!==(v<n)));
  const w=k=>Math.max(1,Math.ceil(Math.log2(Math.max(2,k))));
  const LH=n+m+2+2*m*w(n),LD=N+4*m+2+8*m*w(N);
  ok(LD<=7*LH);
  if(n<=5){
    graphs++;
    let sourceCount=0n,weighted=0n;
    for(let t=0;t<5**n;t++){
      const a=label(t,n);assignments++;
      const good=E.every(([u,v])=>C(a[u],a[v]));
      if(good)sourceCount++;
      let val=1n;for(let [u,v] of E)val*=BigInt(W[a[u]][a[v]]);
      weighted+=val;
    }
    ok(weighted===(1n<<BigInt(m))*sourceCount);
    if(N<=9){targetEnumerations++;
      const direct=countHom(N,arcs,R);ok(direct===weighted);
    }
  }
 }
}
const result={version:'TMR-1/098',all25TerminalPairs:true,graphs,subcubic,assignments,targetEnumerations,checks,failures:0,scope:'finite COMPUTATIONAL; planarity and arbitrary-size hardness separately proved'};
console.log(JSON.stringify(result));
