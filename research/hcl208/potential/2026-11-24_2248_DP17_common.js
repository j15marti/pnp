"use strict";
function main(){
 const rows=[];let scans=0,checks=0;function ck(v,m){checks++;if(!v)throw Error(m)}
 const pairs=[[0,1],[0,2],[1,2]];
 function repair(E,w){let R=[],bad=[];for(const e of E){let t=e.map(v=>w[v]);if(t.every(b=>b===t[0]))bad.push(e);else{let j=t.findIndex((v,k)=>v!==t[(k+1)%3]&&v!==t[(k+2)%3]);R.push([e[j],...e.filter((_,k)=>k!==j)]);}}return{R,bad};}
 function scan(n,R,D,k){let m=R.length;if(m<16)return {status:"credit-too-small",scans:0};let before=scans,found=null,adj=Array.from({length:n},()=>new Set());for(let e of [...R,D])for(let i=0;i<e.length;i++)for(let j=i+1;j<e.length;j++){adj[e[i]].add(e[j]);adj[e[j]].add(e[i]);}
 function test(U){scans++;let S=new Set(U),C=Array(n).fill(-1),num=0;for(let i=0;i<n;i++)if(!S.has(i)&&C[i]<0){let q=[i];C[i]=num;for(let z=0;z<q.length;z++)for(let v of adj[q[z]])if(!S.has(v)&&C[v]<0){C[v]=num;q.push(v);}num++;}
 let W=Array(num).fill(0);for(let e of R){let v=e.find(v=>!S.has(v));if(v===undefined)W.push(1);else W[C[v]]++;}
 let reachable=1n;for(let w of W)reachable|=reachable<<BigInt(w);for(let b=8;b<=m/2;b++)if((reachable>>BigInt(b))&1n)return{U,b};return null;}
 function recur(U,start){if(U.length===k){found=test(U);return;}for(let i=start;i<n&&!found;i++)recur([...U,i],i+1);}
 recur([],0);return{status:found?"eligible":"decline",scans:scans-before,found};}
 const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 let r=repair(F,[1,1,1,0,0,0,0]);ck(r.bad.length===1,"Fano anchor");rows.push({name:"Fano actual",m:r.R.length,three:scan(7,r.R,r.bad[0],3),jointCut:[12,14]});
 let P=[];for(let c=0;c<3;c++)P.push([0,1,2].map(i=>3*i+c));for(let c=0;c<3;c++)P.push([0,1,2].map(j=>3*c+j));for(let a of [1,2])for(let c=0;c<3;c++)P.push([0,1,2].map(i=>3*i+(a*i+c)%3));
 let best=12;for(let w=0;w<512;w++){let x=Array.from({length:9},(_,i)=>(w>>i)&1);best=Math.min(best,repair(P,x).bad.length);}ck(best===2,"plane");rows.push({name:"M22 actual plane",minBad:best,status:"outside single-demand chart",jointCut:[20,24]});
 for(let q of [1,2]){let L=12*q,E=[],id=(i,j)=>3*((i+L)%L)+(j+3)%3;for(let i=0;i<L;i++)for(let j=0;j<3;j++)E.push([id(i,j),id(i+1,j),id(i+1,j+1)]);for(let b=0;b<q;b++)for(let j=0;j<3;j++){let temp=j===2?[[0,2,5],[1,3,10],[4,7,9],[6,8,11]]:[[0,2,5],[1,3,8],[4,7,10],[6,9,11]];if(b===0&&j===0)temp=[[0,4,8],[1,3,6],[2,9,11],[5,7,10]];for(const t of temp)E.push(t.map(i=>id(12*b+i,j)));}let n=3*L,w=Array.from({length:n},(_,i)=>Math.floor(i/3)%2),r=repair(E,w);ck(r.bad.length===1,"ring anchor");let z=Array.from({length:n},(_,i)=>+(i%3===Math.floor(i/3)%3)),x=z.map((b,i)=>b^w[i]);ck(E.every(e=>!e.every(v=>x[v]===x[e[0]])),"known ring witness");
 let result=[];for(const [a,b] of pairs){let D=[r.bad[0][a],r.bad[0][b]];result.push({D,two:scan(n,r.R,D,2),three:scan(n,r.R,D,3),knownWitnessSeparates:z[D[0]]!==z[D[1]]});}rows.push({name:"BS15 ring",q,n,rootNAE:scan(n,r.R,r.bad[0],3),result});}
 return{checks,scans,rows};
}
console.log(JSON.stringify(main(),null,2));
