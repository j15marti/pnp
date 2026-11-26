function audit(){
let checks=0;const ok=(b)=>{checks++;if(!b)throw Error("check "+checks)};
const perms=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]],mask=239;
const P=perms.filter(p=>p.every((j,i)=>(mask>>(3*i+j))&1));
const ports=[0,2,1];
ok(P.length===3);for(let i=0;i<3;i++)for(let j=0;j<3;j++)ok(+(P[i][ports[j]]===0)===+(i===j));
let seed=20261126;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
function compile(n,F){
 const blocks=Array.from({length:n},()=>2), guards=[];
 const add=()=>{blocks.push(3);return blocks.length-1};
 for(const C of F){const sel=add();for(let j=0;j<3;j++){const h=add(),lit=C[j],v=Math.abs(lit)-1;guards.push([h,0,sel,j,0],[h,1,v,0,lit>0?1:0]);}}
 return {blocks,guards};
}
function val(B,state,p){return +(state===p)}
function solve(Q){
 let D=Q.blocks.map(x=>Array.from({length:x},(_,i)=>i));
 function rec(D){let changed=true;while(changed){changed=false;for(const [a,p,b,q,s] of Q.guards){let A=D[a].filter(i=>D[b].some(j=>(val(a,i,p)^val(b,j,q))===s));let B=D[b].filter(j=>A.some(i=>(val(a,i,p)^val(b,j,q))===s));if(!A.length||!B.length)return null;if(A.length!==D[a].length||B.length!==D[b].length)changed=true;D[a]=A;D[b]=B}}
 let k=-1;for(let i=0;i<D.length;i++)if(D[i].length>1&&(k<0||D[i].length<D[k].length))k=i;
 if(k<0)return D.map(x=>x[0]);for(let v of D[k]){let E=D.map(x=>x.slice());E[k]=[v];let r=rec(E);if(r)return r}return null
 }return rec(D)
}
function ref(n,F){for(let a=0;a<(1<<n);a++)if(F.every(C=>C.some(l=>!!((a>>(Math.abs(l)-1))&1)===(l>0))))return a;return null}
function lift(Q,S){let off=0,M=[],A=[];for(let k=0;k<Q.blocks.length;k++){let b=Q.blocks[k],p=b===2?(S[k]===0?[0,1]:[1,0]):P[S[k]];for(let i=0;i<b;i++){M.push(off+p[i]);A.push([off,b,i]);}off+=b}
 let inv=[];M.forEach((j,i)=>inv[j]=i);ok(new Set(M).size===off);
 for(let i=0;i<off;i++)for(let j=0;j<off;j++){let [o,b,row]=A[i];let available=j>=o&&j<o+b&&(b===2||((mask>>(3*row+j-o))&1));let N=+(inv[j]<i),E=+(M[i]<=j),S=+(inv[j]<=i),W=+(M[i]<j);ok((E===W&&S===N)||(available&&N===0&&E===1&&S===1&&W===0))}
 let starts=[];let t=0;for(let b of Q.blocks){starts.push(t);t+=b}
 function physical(k,p){let o=starts[k],i=Q.blocks[k]===2?o:o+ports[p];return +(M[i]===o)}
 for(const [a,p,b,q,s] of Q.guards)ok((physical(a,p)^physical(b,q))===s);return off
}
let yes=0,no=0,largest=0;for(let k=0;k<120;k++){let n=3+rnd(3),m=1+rnd(10),F=Array.from({length:m},()=>Array.from({length:3},()=>{let x=1+rnd(n);return rnd(2)?x:-x}));let Q=compile(n,F),S=solve(Q);ok((S!==null)===(ref(n,F)!==null));if(S){yes++;largest=Math.max(largest,lift(Q,S))}else no++}
const all=Array.from({length:8},(_,a)=>[1,2,3].map((v,i)=>a>>i&1?v:-v));let F=all.map(x=>x.slice());F[0][0]*=-1;
let Q=compile(3,all),R=compile(3,F);ok(solve(Q)===null);let witness=solve(R);ok(witness!==null);largest=Math.max(largest,lift(R,witness));ok(Q.guards.filter((g,i)=>g.some((v,j)=>v!==R.guards[i][j])).length===1);
let scales=[];for(let b of [1,2,4,8]){let G=[];for(let j=0;j<b;j++)for(let C of F)G.push(C.map(l=>Math.sign(l)*(Math.abs(l)+3*j)));let q=compile(3*b,G),s=solve(q);ok(s!==null);let side=lift(q,s);let H=G.map(x=>x.slice());H[0][0]*=-1;ok(solve(compile(3*b,H))===null);scales.push({blocks:b,side,cells:side*side});}
function bin(n,k){if(k<0||k>n)return 0n;let a=1n;for(let i=1;i<=k;i++)a=a*BigInt(n-i+1)/BigInt(i);return a}
function clean(B,q){let n=B.length,I=[],J=Array.from({length:n},(_,i)=>i),U=J.slice();
 function mass(U,J,k){return J.reduce((s,j)=>s+bin(U.filter(i=>!B[i][j]).length,k),0n)}
 if(mass(U,J,q)<BigInt(q)*bin(n,q))return null;
 while(I.length<q){let best=-1,w=-1n,Jbest;for(let i of U){let jj=J.filter(j=>!B[i][j]),u=U.filter(k=>k!==i),v=mass(u,jj,q-I.length-1);if(v>w){w=v;best=i;Jbest=jj}}I.push(best);U=U.filter(i=>i!==best);J=Jbest;ok(w>=BigInt(q)*bin(U.length,q-I.length))}
 ok(J.length>=q);ok(I.every(i=>J.every(j=>!B[i][j])));return [I,J.slice(0,q)]
}
let bicliqueCases=0,admitted=0;for(let b=0;b<512;b++)for(let q=1;q<=3;q++){let B=Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>(b>>(3*i+j))&1));bicliqueCases++;if(clean(B,q))admitted++}
for(let n of [8,16,32])for(let t=0;t<20;t++){let B=Array.from({length:n},()=>Array.from({length:n},()=>rnd(11)<2?1:0));let q=2+rnd(4);bicliqueCases++;if(clean(B,q))admitted++}
return {checks,randomFormulaCases:120,yes,no,largestRandomOrNeighborSide:largest,scales,bicliqueCases,admitted,neighborSide:6+8*12,seed:20261126}
}
console.log(JSON.stringify(audit(),null,2));
