"use strict";
function run(){
 const R={assertions:0,searchNodes:0,closureRounds:0,graphs:[],momentComparisons:0,cutChecks:0,bruteMomentChecks:0,cycleFourierChecks:0,guardedFourierChecks:0,cycleControls:[],peer:{}};
 function ok(x){R.assertions++;if(!x)throw Error("assertion "+R.assertions);}
 function subs(m,k,cb,start=0,a=[]){if(k===0){cb(a);return;}for(let j=start;j<=m-k;j++)subs(m,k-1,cb,j+1,[...a,j]);}
 function adj(n,E,skip=new Set()){let A=Array.from({length:n},()=>[]);E.forEach(([u,v,s=0],i)=>{if(!skip.has(i)){A[u].push([v,s,i]);A[v].push([u,s,i]);}});return A;}
 function reach(A,u,v=-1){let seen=new Set([u]),Q=[u];for(let i=0;i<Q.length;i++)for(let [w] of A[Q[i]])if(!seen.has(w)){seen.add(w);Q.push(w);}return v<0?seen.size:seen.has(v);}
 function valid(E,x){return E.every(([u,v,s=0])=>(x[u]^x[v])!==s);}
 const pc=[0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4];
 function solve(n,E){let A=adj(n,E);function rec(D){R.searchNodes++;let changed=true;while(changed){R.closureRounds++;changed=false;for(let [u,v,s=0] of E){for(let [a,b] of [[u,v],[v,u]])if(pc[D[a]]===1){let t=D[b]&~(1<<(Math.log2(D[a])^s));if(!t)return null;if(t!==D[b]){D[b]=t;changed=true;}}}}let j=-1;for(let i=0;i<n;i++)if(pc[D[i]]>1&&(j<0||pc[D[i]]<pc[D[j]]||(pc[D[i]]===pc[D[j]]&&A[i].length>A[j].length)))j=i;if(j<0)return D.map(Math.log2);for(let c=0;c<4;c++)if(D[j]&(1<<c)){let X=D.slice();X[j]=1<<c;let x=rec(X);if(x)return x;}return null;}let D=Array(n).fill(15);D[0]=1;return rec(D);}
 function myc(n,E){let F=E.map(e=>e.slice());for(let [u,v] of E){F.push([u,n+v,0],[v,n+u,0]);}for(let i=0;i<n;i++)F.push([n+i,2*n,0]);return [2*n+1,F];}
 function critical(n,E){ok(!solve(n,E));for(let i=E.length-1;i>=0;i--){let F=E.filter((_,j)=>j!==i);if(!solve(n,F))E=F;}let used=[...new Set(E.flatMap(e=>e.slice(0,2)))].sort((a,b)=>a-b);let M=new Map(used.map((v,i)=>[v,i]));return [used.length,E.map(([u,v,s])=>[M.get(u),M.get(v),s])];}
 function distance(A,u,v){let d=Array(A.length).fill(-1),Q=[u];d[u]=0;for(let i=0;i<Q.length;i++)for(let [w] of A[Q[i]])if(d[w]<0){d[w]=d[Q[i]]+1;Q.push(w);}return d[v];}
 function cycleThrough(n,E,i){let [u,v]=E[i],A=adj(n,E,new Set([i])),p=Array(n).fill(null),Q=[u];p[u]=[-1,-1];for(let j=0;j<Q.length;j++)for(let [w,,k] of A[Q[j]])if(p[w]===null){p[w]=[Q[j],k];Q.push(w);}if(!p[v])return [];let C=[i];while(v!==u){C.push(p[v][1]);v=p[v][0];}return C;}
 function moment(n,E,F){let A=adj(n,F.map(i=>E[i])),x=Array(n).fill(-1),cc=0;for(let u=0;u<n;u++)if(x[u]<0){cc++;x[u]=0;let Q=[u];for(let j=0;j<Q.length;j++)for(let [v,s] of A[Q[j]]){let z=x[Q[j]]^s;if(x[v]<0){x[v]=z;Q.push(v);}else if(x[v]!==z)return 0n;}}return 4n**BigInt(cc);}
 function brute(n,E,F=null){let count=0n;for(let a=0;a<4**n;a++){let x=Array.from({length:n},(_,i)=>(a>>(2*i))&3);if(F?F.every(i=>{let [u,v,s]=E[i];return (x[u]^x[v])===s;}):valid(E,x))count++;}return count;}
 function chart(n,E){let A=adj(n,E),seen=Array(n).fill(false),tree=new Set(),cc=0;for(let u=0;u<n;u++)if(!seen[u]){cc++;seen[u]=true;let Q=[u];for(let j=0;j<Q.length;j++)for(let [v,,i] of A[Q[j]])if(!seen[v]){seen[v]=true;tree.add(i);Q.push(v);}}let T=adj(n,E,new Set(E.map((_,i)=>i).filter(i=>!tree.has(i))));let cycles=[];for(let i=0;i<E.length;i++)if(!tree.has(i)){let [u,v]=E[i],p=Array(n).fill(null),Q=[u];p[u]=[-1,-1];for(let j=0;j<Q.length;j++)for(let [w,,k] of T[Q[j]])if(!p[w]){p[w]=[Q[j],k];Q.push(w);}let C=[i];while(v!==u){C.push(p[v][1]);v=p[v][0];}cycles.push(C);}return {cc,cycles};}
 function parity(x){let p=0;while(x){p^=x&1;x>>>=1;}return p;}
 function fourier(n,E,allowed=null){let {cc,cycles}=chart(n,E),b=cycles.length;let rows=allowed??E.map(([,,s])=>[0,1,2,3].filter(x=>x!==s));let sum=0n;for(let i=0;i<4**b;i++){let tag=Array(E.length).fill(0);cycles.forEach((C,j)=>{let x=(i>>(2*j))&3;for(let k of C)tag[k]^=x;});let term=1n;for(let j=0;j<E.length;j++){let w=rows[j].reduce((t,x)=>t+(parity(x&tag[j])?-1:1),0);term*=BigInt(w);}sum+=term;}ok(sum%(4n**BigInt(b))===0n);return sum/(4n**BigInt(b))*4n**BigInt(cc);}
 function coreCheck(n,E,name){let m=E.length;ok(!solve(n,E));let g=Math.min(...E.map((_,i)=>cycleThrough(n,E,i).length));ok(g>=3);let neighbors=0;for(let i=0;i<m;i++){let F=E.filter((_,j)=>j!==i),x=solve(n,F);ok(x&&valid(F,x));ok(x[E[i][0]]===x[E[i][1]]);for(let s=1;s<=3;s++){let H=E.map((e,j)=>j===i?[e[0],e[1],s]:e);ok(valid(H,x));neighbors++;}}
 let H=E.map((e,j)=>j===0?[e[0],e[1],1]:e);let local=0;
 for(let k=0;k<g;k++)subs(m,k,F=>{let a=moment(n,E,F),b=moment(n,H,F);ok(a===b&&a===4n**BigInt(n-k));R.momentComparisons++;local++;});
 let C=cycleThrough(n,E,0);ok(moment(n,H,C)===0n&&moment(n,E,C)>0n);
 for(let k=1;k<=3;k++)subs(m,k,F=>{ok(reach(adj(n,E,new Set(F)),0)===n);R.cutChecks++;});
 // Each edge's plane is absorbed by a vertex star cut; for each candidate legal row,
 // a vertex potential realizing that row extends the relaxed ambient equation.
 for(let i=0;i<m;i++){let [u,v,s]=E[i];for(let r=0;r<4;r++)if(r!==s){let x=Array(n).fill(0);x[u]=r;ok((x[u]^x[v])===r);for(let C of chart(n,E).cycles){let z=0;for(let k of C)z^=x[E[k][0]]^x[E[k][1]];ok(z===0);}}}
 R.graphs.push({name,n,m,g,beta:m-n+1,neighbors,lowOrderMomentComparisons:local,firstSeparatingCycle:C.length,forestCreditNumerator:15-3*m,forestCreditDenominator:16,edges:E});}
 let K5=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)K5.push([i,j,0]);coreCheck(5,K5,"K5");
 let C5=Array.from({length:5},(_,i)=>[i,(i+1)%5,0]);let [n,E]=myc(...myc(5,C5));[n,E]=critical(n,E);coreCheck(n,E,"edge-minimal double Mycielski C5");
 let seed=20261124;function rng(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k;}
 for(let t=0;t<100;t++){let n=3+rng(4),E=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(E.length<9&&rng(5)<3)E.push([i,j,rng(4)]);let F=E.map((_,i)=>i).filter(()=>rng(2)===0);ok(moment(n,E,F)===brute(n,E,F));R.bruteMomentChecks++;ok(fourier(n,E)===brute(n,E));R.cycleFourierChecks++;if(E.length){let i=rng(E.length),d=rng(4),rows=E.map(([,,s],j)=>j===i?(d===s?[]:[d]):[0,1,2,3].filter(x=>x!==s));let B=0n;for(let a=0;a<4**n;a++){let x=Array.from({length:n},(_,k)=>(a>>(2*k))&3);if(valid(E,x)&&(x[E[i][0]]^x[E[i][1]])===d)B++;}ok(fourier(n,E,rows)===B);R.guardedFourierChecks++;}}
 for(let n of [4,8,16,32,64]){let E=Array.from({length:n},(_,i)=>[i,(i+1)%n,0]),H=E.map((e,j)=>j===0?[e[0],e[1],1]:e);let F=E.map((_,i)=>i);ok(moment(n,E,F)===4n&&moment(n,H,F)===0n);for(let j=0;j<n;j++){let A=F.filter(i=>i!==j);ok(moment(n,E,A)===moment(n,H,A));}let a=fourier(n,E),b=fourier(n,H);ok(a>0n&&b>0n);R.cycleControls.push({n,zeroCount:String(a),twistedCount:String(b),firstSeparatingOrder:n});}
 for(let k of [3,4]){let support=new Set();function rec(a){if(a.length===k){let x=0;for(let j=0;j<k-1;j++)x|=(a[j]^a[k-1])<<(2*j);support.add(x);return;}for(let i=1;i<4;i++)rec([...a,i]);}rec([]);ok(support.size===(k===3?16:58));R.peer["I12_circuit_"+k]=support.size;}
 let events=[[[[1,0],[12,1],[4,1]],2],[[[8,0],[1,0],[4,1],[16,0],[48,1],[16,0],[2,1]],4],[[[48,1],[8,1],[16,1],[32,0],[48,1],[1,1]],3],[[[1,1],[48,1],[3,1],[3,1]],2],[[[8,0],[2,0],[12,1],[3,0]],4]];
 // Restore exact fifth event as published.
 events[4]=[[[8,0],[2,0],[12,1],[8,0],[3,0]],4];
 let M=64,words=Array.from({length:M},(_,i)=>i),B=events.map(([rows,H])=>words.map(x=>+(rows.reduce((a,[w,d])=>a+(parity(w&x)^d),0)>H))),masses=B.map(b=>b.reduce((a,b)=>a+b,0)),legal=words.filter(x=>B.every(b=>!b[x])).length;
 let pool=words.filter(x=>pc[x&15]+pc[(x>>4)&15]<=2),P=[];
 for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++){let s=words.map(x=>B[i][x]+B[j][x]),a=pool.map(w=>words.reduce((t,x)=>t+s[x]*(parity(x&w)?-1:1),0)),h=words.map(x=>pool.reduce((t,w,k)=>t+a[k]*(parity(x&w)?-1:1),0));let ell=words.map(x=>2*M*h[x]*s[x]-h[x]**2-M*M*s[x]);for(let x of words)ok(2*M*M*B[i][x]*B[j][x]-ell[x]===(M*s[x]-h[x])**2);let fs=words.map(x=>2*M*M*(s[x]-1)),sum=A=>A.reduce((a,b)=>a+b,0),cand=[Array(M).fill(0),fs,ell].sort((a,b)=>sum(b)-sum(a))[0];P.push({i,j,cand,w:sum(cand)});}
 let parents=B.map((_,i)=>i),find=i=>parents[i]===i?i:find(parents[i]),credit=words.map(x=>2*M*M*(1-B.reduce((a,b)=>a+b[x],0)));for(let {i,j,cand,w} of P.sort((a,b)=>b.w-a.w))if(w>0&&find(i)!==find(j)){parents[find(i)]=find(j);credit=credit.map((v,x)=>v+cand[x]);}for(let x of words)ok(credit[x]<=2*M*M*+(B.every(b=>!b[x])));let total=credit.reduce((a,b)=>a+b,0);ok(legal===14&&total===1408);let split=[0,1].map(b=>words.filter(x=>parity(x&11)===b).reduce((a,x)=>a+credit[x],0));ok(split[0]+split[1]===total);R.peer.MS12={legal,creditNumerator:total,creditDenominator:2*M*M,guardMask:11,split};
 return R;
}
console.log(JSON.stringify(run(),null,2));
