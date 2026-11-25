
function search(){
let state=918273;const rnd=n=>{state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)%n};
const n=24,d=0;const bit=(w,i)=>(w>>>i)&1,ok=(w,t)=>{const a=bit(w,t[0]),b=bit(w,t[1]),c=bit(w,t[2]);return a!==b||b!==c},minor=(w,t)=>t.find(i=>t.filter(j=>bit(w,j)===bit(w,i)).length===1);
const pairs=t=>[[t[0],t[1]],[t[0],t[2]],[t[1],t[2]]].map(([a,b])=>Math.min(a,b)*n+Math.max(a,b));
let attempts=0,swaps=0,best=0;
for(let trial=0;trial<250;trial++){
let x=rnd(1<<n),y=x^1,z=rnd(1<<n);if((x&1)!==(z&1))z^=1;
let O=[],used=new Set(),good=true;
for(let p=0;p<4;p++){
let w=p<2?x:y,part=null;
for(let k=0;k<400&&!part;k++){
let left=Array.from({length:n-1},(_,i)=>i+1),ts=[],seen=new Set(used),fail=false;
for(let j=0;j<n/3;j++){
let a=j===0?0:left.splice(rnd(left.length),1)[0], candidates=[];
for(let b of left)for(let c of left)if(b<c){let t=[a,b,c];if(ok(w,t)&&ok(z,t)&&(!t.includes(d)||minor(w,t)===d)&&pairs(t).every(e=>!seen.has(e)))candidates.push(t)}
if(!candidates.length){fail=true;break}
let t=candidates[rnd(candidates.length)];left=left.filter(i=>!t.slice(1).includes(i));pairs(t).forEach(e=>seen.add(e));ts.push(t)
}
if(!fail){part=ts;used=seen}
}
if(!part){good=false;break}O.push(...part.map(t=>({p,t,bad:[0,7]})))
}
if(!good)continue;attempts++;
function score(){return new Set(O.map(o=>minor(o.p<2?x:y,o.t))).size}
let s=score();
for(let k=0;k<18000&&s<n;k++){
let p=rnd(4),i=p*(n/3)+rnd(n/3),j=p*(n/3)+rnd(n/3);if(i===j)continue;
let a=rnd(3),b=rnd(3),t=O[i].t,u=O[j].t;if(t[a]===d||u[b]===d)continue;
[t[a],u[b]]=[u[b],t[a]];swaps++;
let w=p<2?x:y;let ps=O.flatMap(o=>pairs(o.t));
let valid=ok(w,t)&&ok(w,u)&&ok(z,t)&&ok(z,u)&&(!t.includes(d)||minor(w,t)===d)&&(!u.includes(d)||minor(w,u)===d)&&new Set(ps).size===ps.length;
let q=valid?score():-1;
if(q>=s||(valid&&rnd(1000)<15)){s=q}else [t[a],u[b]]=[u[b],t[a]];
best=Math.max(best,s);
}
if(s===n)return {n,d,x,y,z,O,trial,attempts,swaps,best};
}
return {attempts,swaps,best};
}

console.log(JSON.stringify(search(),null,2));
