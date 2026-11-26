function run(){
 let checks=0;const ck=v=>{checks++;if(!v)throw Error("assert "+checks)};
 let seed=99131;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
 const inf=Infinity;
 function certificate(q,E,p,r){let lam=q*Math.max(p,r),U=[];
 for(let sign of [1,-1]){let d=Array(q).fill(-inf);d[0]=0;for(let k=0;k<q-1;k++){let z=d.slice();for(let [i,j,t,c] of E)z[j]=Math.max(z[j],d[i]+sign*(t?r:-p)-lam*c);d=z}
 if(E.some(([i,j,t,c])=>d[j]<d[i]+sign*(t?r:-p)-lam*c))return null;U.push(d)}
 return {lam,U,M:Math.max(0,...U.flat().filter(Number.isFinite))}}
 function DP(A,B,q,T,C,p,r,slack,band){let a=A.length,b=B.length,P=Array.from({length:a+1},()=>Array.from({length:b+1},()=>Array(q).fill(inf)));P[0][0][0]=0;let s=p+r,w=Math.ceil((C.M+C.lam*slack)/s);
 let ok=(i,j)=>!band||Math.abs(i-Math.floor(r*(i+j)/s))<=w;for(let i=0;i<=a;i++)for(let j=0;j<=b;j++){let x=P[i][j];for(let t=0;t<2;t++){if(t?j===b:i===a)continue;let ni=i+(t===0),nj=j+(t===1);if(i<a&&j<b&&!ok(ni,nj))continue;let mat=(t?B[j]:A[i]);for(let u=0;u<q;u++)for(let v=0;v<q;v++)P[ni][nj][v]=Math.min(P[ni][nj][v],x[u]+mat[u][v])}}
 return Math.min(...P[a][b])<=T}
 let trials=0,positive=0,strict=0,refused=0,allpaid=0;
 for(let z=0;z<240;z++){let [p,r]=[[1,1],[2,1],[1,2],[2,3],[3,2]][z%5],q=p+r,word=[...Array(r).fill(0),...Array(p).fill(1)],H=[0];for(let t of word.slice(0,-1))H.push(H.at(-1)+(t?r:-p));
 let m=4+z%7,n=3+(z*3)%8,slack=z%4,base=0,E=[],M=[];
 for(let [t,len] of [[0,m],[1,n]]){let F=[];for(let k=0;k<len;k++){let b=1+k%3;base+=b;let a=Array.from({length:q},(_,i)=>Array.from({length:q},(_,j)=>{
 let e=H[j]-H[i]===(t?r:-p)&&rnd()<.8?0:rnd()<.45?1+Math.floor(3*rnd()):inf;
 if(Number.isFinite(e))E.push([i,j,t,e]);return b+e}));F.push(a)}M.push(F)}
 let C=certificate(q,E,p,r);ck(!!C);for(let sign of [1,-1])for(let [i,j,t,e] of E)ck(C.U[sign===1?0:1][j]>=C.U[sign===1?0:1][i]+sign*(t?r:-p)-C.lam*e);
 let full=DP(...M,q,base+slack,C,p,r,slack,false),band=DP(...M,q,base+slack,C,p,r,slack,true);ck(full===band);positive+=Number(full);trials++;
 if(E.some(([i,j,t,e])=>i===j&&e>0))strict++;
 }
 // Free pure drift loop cannot be charged, but a unit-cost excess loop is admitted.
 ck(certificate(2,[[0,0,0,0],[0,1,0,0],[1,0,1,0]],1,1)===null);refused++;
 let C=certificate(2,[[0,0,0,1],[0,1,0,0],[1,0,1,0]],1,1);ck(!!C);allpaid++;
 return{checks,trials,positive,negative:trials-positive,strict,refused,allpaid,scope:"abstract weighted macro tables; full grid vs certified cost-dependent strip at fixed deadline; not native rule-table tests or measured runtime"}}
console.log(JSON.stringify(run(),null,2));
