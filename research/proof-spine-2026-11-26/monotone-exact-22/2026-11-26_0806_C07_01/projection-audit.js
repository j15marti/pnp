function audit(){
let checks=0;const A=(b)=>{checks++;if(!b)throw Error("failed "+checks)};
const V=(F,x)=>F.every(r=>r.reduce((s,v)=>s+x[v],0)===2);
function build(k){
let n=0,F=[],left=[],right=[],H=Array.from({length:k},()=>Array.from({length:k},()=>n++)),T=Array.from({length:k},()=>Array.from({length:k},()=>n++)),eqs=[],cross=[];
function eq(a,b){let p=[n++,n++,n++];F.push([a,...p],[b,...p]);eqs.push([a,b,p])}
for(let i=0;i<k;i++)for(let j=0;j<k;j++){if(j+1<k)eq(H[i][j],H[i][j+1]);if(i+1<k)eq(T[i][j],T[i+1][j]);let p=[n++,n++];F.push([H[i][j],T[i][j],...p]);cross.push([H[i][j],T[i][j],p])}
for(let i=0;i<k;i++){left.push(H[i][0]);right.push(H[i][k-1])}for(let j=0;j<k;j++){left.push(T[0][j]);right.push(T[k-1][j])}return{n,F,H,T,eqs,cross,left,right}}
let boundaries=[];
for(let k of [2,3,4,6]){let G=build(k),count=0;for(let z=0;z<1<<(2*k);z++){let x=Array(G.n).fill(-1);for(let i=0;i<k;i++)for(let j=0;j<k;j++){x[G.H[i][j]]=(z>>i)&1;x[G.T[i][j]]=(z>>(k+j))&1}for(let [a,b,p] of G.eqs){A(x[a]===x[b]);p.forEach((v,j)=>x[v]=+(j<2-x[a]))}for(let [a,b,p] of G.cross)p.forEach((v,j)=>x[v]=+(j<2-x[a]-x[b]));A(V(G.F,x));A(G.left.every((v,i)=>x[v]===((z>>i)&1)&&x[v]===x[G.right[i]]));count++}boundaries.push({k,attained:count})}
let caps=[];
for(let k=5;k<=64;k++){let t=[Math.floor(k/3),Math.floor((k+1)/3),Math.floor((k+2)/3)],n=0,scopes=Array.from({length:4},()=>[]),types=[[[0,1],[2,3]],[[0,2],[1,3]],[[0,3],[1,2]]];
for(let i=0;i<3;i++)for(let [a,b] of types[i])for(let j=0;j<t[i];j++){scopes[a].push(n);scopes[b].push(n++)}A(scopes.every(s=>s.length===k));let cuts=[];for(let z of [3,5,9]){let a=new Set(scopes.filter((_,i)=>(z>>i)&1).flat()),b=new Set(scopes.filter((_,i)=>!((z>>i)&1)).flat());cuts.push([...a].filter(v=>b.has(v)).length)}A(Math.min(...cuts)>k);caps.push({k,min:Math.min(...cuts)})}
return{checks,boundaries,caps}}
console.log(JSON.stringify(audit(),null,2));
