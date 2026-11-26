function partialAudit(){
 const S=n=>Array.from({length:n},(_,i)=>i),ck=(x,m)=>{if(!x)throw Error(m)};
 let modelWords=0,guardComparisons=0,partialJobs=0,models=0,prisms=[];
 for(let k of [1,2]){let n=6*k,e=[];for(let i=0;i<k;i++)for(let j=0;j<3;j++){e[6*i+j]=6*i+3+(3-j)%3;e[6*i+3+j]=6*i+(3-j)%3}for(let i=1;i<k;i++){let a=6*(i-1)+5,b=6*i;[e[a],e[b]]=[e[b],e[a]]}let rev=S(n);e.forEach((c,v)=>rev[c]=v);let R=S(n).map(c=>{let b=3*Math.floor(c/3),j=c%3;return [b+j,b+(j+1)%3,rev[c]]});
 let ms=[];for(let w=0;w<2**n;w++){modelWords++;let x=S(n).map(i=>(w>>>i)&1);if(R.every(r=>r.reduce((s,i)=>s+x[i],0)===1))ms.push(x)}ck(ms.length===1+2**k,"raw count");models+=ms.length;
 for(let h=0;h<2**(2*k);h++){let chosen=new Set(S(2*k).filter(i=>(h>>>i)&1)),E=[],next=new Map(),forced=new Set(),incoming=0;for(let b of chosen)for(let j=0;j<3;j++){let a=rev[3*b+j],t=3*b+(j+2)%3;E.push([a,t,b]);next.set(a,[t,b]);if(!chosen.has(Math.floor(a/3)))incoming++}for(let a of next.keys()){let w=[],seen=new Map(),v=a;while(next.has(v)&&!seen.has(v)){seen.set(v,w.length);w.push(v);v=next.get(v)[0]}if(seen.has(v))w.slice(seen.get(v)).forEach(u=>forced.add(next.get(u)[1]))}partialJobs++;for(let x of ms){let d=b=>1-x[3*b]-x[3*b+1]-x[3*b+2];ck(E.every(([a,t,b])=>x[a]-x[t]===d(b)),"strand identity");ck([...forced].every(b=>d(b)===0),"cycle saturation");ck(3*[...chosen].reduce((s,b)=>s+d(b),0)<=incoming,"boundary budget")}
 for(let v=0;v<n;v++)for(let bit of [0,1]){let exact=ms.filter(x=>x[v]===bit);let reduced=ms.filter(x=>x[v]===bit&&[...forced].every(b=>x[3*b]+x[3*b+1]+x[3*b+2]===1)&&E.every(([a,t,b])=>!forced.has(b)||x[a]===x[t]));ck(exact.length===reduced.length,"guarded soundness");guardComparisons++}}
 }
 for(let n of [12,18,24,48,96,192,384,768]){let R=S(n).map(i=>[(i+n-1)%n,i,(i+1)%n]);for(let r of [0,1,2]){let x=S(n).map(i=>+(i%3===r));ck(R.every(a=>a.reduce((s,i)=>s+x[i],0)===1),"prism lift")}prisms.push({n,faces:[4,n],models:3,allBitsSupported:true})}
 return {modelWords,models,partialJobs,guardComparisons,prisms}
}
console.log(JSON.stringify(partialAudit(),null,2));
