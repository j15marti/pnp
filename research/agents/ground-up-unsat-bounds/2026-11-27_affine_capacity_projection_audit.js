console.log(JSON.stringify((function audit(){
let seed=20261127;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n},par=x=>{let b=0;while(x){b^=1;x&=x-1}return b};
let words=0,networks=0,empty=0,full=0;
for(let t=0;t<160;t++){
 const h=1+rand(5),d=1+rand(4),E=Array.from({length:rand(7)},()=>[rand(h),rand(h)]),P=Array.from({length:rand(3)},()=>rand(h)),A=Array.from({length:h},()=>[rand(1<<d),rand(2)]);
 const adj=Array.from({length:h},()=>[]);for(const [i,j] of E){adj[i].push(j);adj[j].push(i)}
 const seen=new Set(),trees=[];for(let i=0;i<h;i++)if(!seen.has(i)){const V=[i];seen.add(i);for(let k=0;k<V.length;k++)for(const j of adj[V[k]])if(!seen.has(j)){seen.add(j);V.push(j)}if(V.reduce((s,j)=>s+adj[j].length,0)===2*(V.length-1)&&!P.some(j=>V.includes(j)))trees.push(V)}
 let sat=0;
 for(let z=0;z<(1<<d);z++){
 const charge=A.map(([a,b])=>par(a&z)^b),target=charge.reduce((s,b,i)=>s|(b<<i),0);
 const pred=!trees.some(V=>V.every(j=>charge[j]===1));
 let reach=new Set([0]);for(const [i,j] of E){const old=[...reach];for(const x of old){reach.add(x^(1<<i));reach.add(x^(1<<j))}}for(const i of P)for(const x of [...reach])reach.add(x^(1<<i));
 if(pred!==reach.has(target))throw Error("projection disagreement");words++;sat+=Number(pred);
 }networks++;empty+=Number(sat===0);full+=Number(sat===(1<<d))
}
const pairs=[[0,1],[2,4],[3,7],[5,6]],directions=pairs.map(([a,b])=>a^b);if(new Set(pairs.flat()).size!==8||new Set(directions).size!==4)throw Error("bad obstruction");
return {seed:20261127,networks,words,empty,full,nonparallelCover:pairs,directions};
})(),null,2));
