// P3CC12 independent Node.js audit, no external libraries.
const run=()=>{
 const B=[[0,0,0],[1,1,1],[0,0,1],[1,1,0],[0,1,0],[1,0,1],[0,1,1],[1,0,0]];
 const R0=[[6,10,12,8],[7,9,13,11],[6,8,11,13],[9,7,12,10],[10,6,13,9],[8,12,7,11],[0,2,4],[5,3,1],[2,0,5],[1,3,4],[3,0,4],[1,2,5],[3,5,0],[4,2,1]];
 const P0=[[[2,0],[0,1]]],P1=[[[0,0],[2,1]],[[6,0],[2,2]]];
 let checks=0;const ok=x=>{checks++;if(!x)throw Error("assertion "+checks)};
 const pairs=[[0,1],[0,2],[1,2]];
 function build(k,pat){
   const T=[],R=[];for(let i=0;i<k;i++){for(let t of B)T.push(t.map(x=>x+2*i));for(let a of R0)R.push((i%2?a.slice().reverse():a).map(v=>v+14*i));}
   function replace(a,b,c){let j=R[a].indexOf(b);ok(j>=0);R[a][j]=c;}
   for(let u=0;u<k-1;u++)for(let [i,c] of pat[u%pat.length]){
     let j=i^1,l=8*u+i,r=8*(u+1)+j,a=14*u+6+i,b=14*(u+1)+6+j;
     let x=14*u+2*c+B[i][c],y=14*(u+1)+2*c+B[j][c];
     replace(a,x,y);replace(x,a,b);replace(b,y,x);replace(y,b,a);
     [T[l][c],T[r][c]]=[T[r][c],T[l][c]];
   }
   ok(new Set(T.map(t=>t.join(","))).size===8*k);
   for(let i=0;i<R.length;i++)for(let v of R[i])ok(R[v].includes(i));
   for(let j=0;j<T.length;j++)for(let c=0;c<3;c++){const q=T[j][c],v=14*Math.floor(q/2)+2*c+q%2;ok(R[14*Math.floor(j/8)+6+j%8].includes(v));}
   let seen=new Set(),faces=0;for(let u=0;u<R.length;u++)for(let v of R[u])if(!seen.has(u+","+v)){
     faces++;let a=u,b=v;while(!seen.has(a+","+b)){seen.add(a+","+b);let c=R[b][(R[b].indexOf(a)+1)%R[b].length];a=b;b=c;}ok(a===u&&b===v);
   }ok(seen.size===48*k);ok(14*k-24*k+faces===2);
   let C=new Set([0]),Q=[0];for(let i=0;i<Q.length;i++)for(let v of R[Q[i]])if(!C.has(v)){C.add(v);Q.push(v);}ok(C.size===R.length);
   return {T,R,faces,n:2*k};
 }
 function checkCover(T,n,J){ok(J.length===n);for(let c=0;c<3;c++)ok(new Set(J.map(j=>T[j][c])).size===n);}
 function rankGF(rows){let D=new Map();for(let x of rows){while(x){let p=x.toString(2).length-1;if(D.has(p))x^=D.get(p);else{D.set(p,x);break;}}}return D.size;}
 function phase(k,pat){
   let D=[1n,1n,1n,1n];for(let i=0;i<k-1;i++){const p=pat[i%pat.length].map(a=>a[0]>>1);D=D.map((_,b)=>D.reduce((s,v,a)=>s+(p.every(q=>(a===q)===(b===q))?v:0n),0n));}return D;
 }
 function brute(T,n){
   const row=Array.from({length:3*n},()=>[]);T.forEach((t,j)=>t.forEach((u,c)=>row[c*n+u].push(j)));
   const mask=T.map(t=>t.reduce((m,u,c)=>m|(1n<<BigInt(c*n+u)),0n));const full=(1n<<BigInt(3*n))-1n;
   function f(s){if(s===full)return 1n;let best=null;for(let u=0;u<3*n;u++)if(!(s>>BigInt(u)&1n)){
     const P=row[u].filter(j=>!(s&mask[j]));if(!P.length)return 0n;if(best===null||P.length<best.length)best=P;
   }return best.reduce((a,j)=>a+f(s|mask[j]),0n);}return f(0n);
 }
 function cert(k,pat,mixed){
   let {T,R,faces,n}=build(k,pat);let ranks=[];
   for(let p=0;p<4;p++)checkCover(T,n,Array.from({length:n},(_,i)=>8*(i>>1)+2*p+i%2));
   for(let [a,b] of pairs){
     const c=3-a-b,G=new Map(),H=Array.from({length:2*n},()=>[]);
     T.forEach((t,j)=>{let q=t[a]+","+t[b];if(!G.has(q))G.set(q,[]);G.get(q).push(j);H[t[a]].push(n+t[b]);H[n+t[b]].push(t[a]);});
     let vis=new Set([0]),Q=[0];for(let i=0;i<Q.length;i++)for(let v of H[Q[i]])if(!vis.has(v)){vis.add(v);Q.push(v);}ok(vis.size===2*n);ok([...G.values()].every(v=>v.length<=2));
     let z=[];for(let p=0;p<4;p++){
       let W=[];for(let i=0;i<k;i++)for(let v of [0,1]){let j=8*i+2*p+v;for(let h of G.get(T[j][a]+","+T[j][b]))if(h!==j)W.push((1n<<BigInt(T[j][c]))^(1n<<BigInt(T[h][c])));}
       z.push(rankGF(W));
     }ok(Math.max(...z)===n-1);if(k>1)ok(Math.min(...z)<=k);ranks.push(z);
   }
   const rows=Array(3*n).fill(0n);T.forEach((t,j)=>t.forEach((u,c)=>rows[c*n+u]|=1n<<BigInt(j)));ok(T.length-rankGF(rows)===2*k+2);
   let count=phase(k,pat).reduce((a,b)=>a+b,0n);
   if(!mixed)ok(count===2n+(1n<<BigInt(k)));
   else {let a=0n,b=1n;for(let i=0;i<k+3;i++)[a,b]=[b,a+b];ok(count===a+1n);}
   if(k<=5)ok(brute(T,n)===count);
   if(mixed){for(let u=0;u<k-1;u+=2){
     let M=Array.from({length:n},(_,i)=>8*(i>>1)+2*(((i>>1)===u||(i>>1)===u+1)?0:2)+i%2);checkCover(T,n,M);
     for(let [a,b] of pairs){let S=new Set(M.map(j=>T[j][a]+","+T[j][b]));let C=new Set(Array.from({length:n},(_,i)=>8*(i>>1)+4+i%2).map(j=>T[j][a]+","+T[j][b]));ok([...S].some(x=>!C.has(x)));}
   }}
   // Direct verification of each proposed four-incidence cut and the balanced local ports.
   for(let u=0;u<k-1;u++){
     let cross=[];for(let j=0;j<T.length;j++)for(let c=0;c<3;c++)if((j<8*(u+1))!==(T[j][c]<2*(u+1)))cross.push([j,c,T[j][c]]);
     ok(cross.length===4);for(let c of new Set(cross.map(v=>v[1]))){let L=cross.filter(v=>v[1]===c);ok(L.length===2);ok(L.filter(v=>v[0]<8*(u+1)).length===1);}
   }
   return {k,triples:8*k,faces,ranks,sourceNullity:2*k+2,count:count.toString(),skeletonLowerBound:mixed?(1n<<BigInt(k>>1)).toString():null};
 }
 const cube=[1,2,4,8,16,32,64,128,256].map(k=>cert(k,P0,false));
 const mixed=[3,5,9,13,17,25,49,97,193].map(k=>cert(k,P1,true));
 let seed=26112612;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;}
 let forestChecks=0;for(let r=1;r<=10;r++)for(let t=0;t<32;t++){
   let E=[];for(let i=1;i<r;i++)if(rand(4))E.push([i,rand(i)]);
   for(let m=0;m<(1<<r);m++){let c=0;for(let i=0;i<r;i++)c+=m>>i&1;let q=1-c+E.filter(([i,j])=>(m>>i&1)&&(m>>j&1)).length;ok(q<=Number(m===0));forestChecks++;}
 }
 const MFU="000 002 010 011 021 022 100 101 111 201 202 221".split(" ").map(t=>[...t].map(Number)),MFV=MFU.concat([[1,1,0]]);let neighbors=[];
 for(let k of [1,3,5])for(let yes of [false,true]){let {T,n}=build(k,P1);T=T.concat((yes?MFV:MFU).map(t=>t.map(v=>v+n)));for(let [i,c,h] of [[0,0,0],[2,1,1]]){let l=8*(k-1)+i,r=8*k+h;[T[l][c],T[r][c]]=[T[r][c],T[l][c]];}let v=brute(T,n+3);let ref=0n;if(yes){const C=[[1,11,12],[4,10,12],[5,9,12]],D=phase(k,P1);for(let p=0;p<4;p++)for(let S of C)if((p===0)===S.includes(0)&&(p===1)===S.includes(1))ref+=D[p];}ok(v===ref);neighbors.push({k,yes,triples:T.length,count:v.toString()});}
 return {checks,forestChecks,cube,mixed,neighbors};
};
console.log(JSON.stringify(run(),null,2));
