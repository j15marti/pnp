console.log(JSON.stringify((function check(){
let seed=20261124; const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const add=(a,b)=>[a[0]+b[0],a[1]^b[1]], neg=a=>[-a[0],a[1]], key=a=>a.join(":");
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a};
function eg(a,b){if(b===0n)return [a,1n,0n];let [g,x,y]=eg(b,a%b);return [g,y,x-a/b*y]}
const parity=x=>Number((x%2n+2n)%2n);
function envelope(rows){
let a=[0n,0],lo=0n,hi=0n,gen=[];
for(const r of rows){a=add(a,r[0]);let l=r[0][0],h=l;for(const v of r){gen.push(add(v,neg(r[0])));if(v[0]<l)l=v[0];if(v[0]>h)h=v[0]}lo+=l;hi+=h}
let d=0n,t=0;
for(const [x,p] of gen){if(!x)continue;let [g,u,v]=eg(d,x<0n?-x:x);if(x<0n)v=-v;t=parity(u)*t^parity(v)*p;d=g}
let free=gen.some(([x,p])=>d?(p^(parity(x/d)*t))!==0:p!==0);
return {a,lo,hi,d,t,free};
}
function inside(E,x){if(x[0]<E.lo||x[0]>E.hi)return false;let [v,p]=add(x,neg(E.a));if(!E.d)return v===0n&&(E.free||!p);return v%E.d===0n&&(E.free||p===parity(v/E.d)*E.t)}
let stats={random:0,sat:0,unsat:0,reference:0,checks:0,closureQueries:0,deleted:0,pairAttempts:0,peakStates:0,scale:[]};
function assert(b){stats.checks++;if(!b)throw Error("mismatch")}
function close(rows,target){rows=rows.map(r=>r.slice());for(;;){let changed=false;for(let i=0;i<rows.length&&!changed;i++){let E=envelope(rows.filter((_,j)=>i!==j));for(let k=0;k<rows[i].length;k++){stats.closureQueries++;if(!inside(E,add(target,neg(rows[i][k])))){rows[i].splice(k,1);stats.deleted++;if(!rows[i].length)return null;changed=true;break}}}if(!changed)return rows}}
function dp(rows,target){if(!rows)return {count:0n,peak:0};let table=new Map([["0:0",{a:[0n,0],c:1n,w:[]}]]),peak=1;
for(let i=0;i<rows.length;i++){let E=envelope(rows.slice(i+1)),P=envelope(rows.slice(0,i+1)),next=new Map;for(const v of table.values())for(let j=0;j<rows[i].length;j++){stats.pairAttempts++;let a=add(v.a,rows[i][j]);if(!inside(E,add(target,neg(a))))continue;assert(inside(P,a));let k=key(a),old=next.get(k);if(old)old.c+=v.c;else next.set(k,{a,c:v.c,w:[...v.w,j]})}table=next;peak=Math.max(peak,table.size)}
stats.peakStates=Math.max(stats.peakStates,peak);let v=table.get(key(target));if(v){let s=[0n,0];for(let i=0;i<rows.length;i++)s=add(s,rows[i][v.w[i]]);assert(key(s)===key(target))}return {count:v?.c??0n,peak}}
function ref(rows,target){let c=0n;function rec(i,s){if(i===rows.length){stats.reference++;if(key(s)===key(target))c++;return}for(const a of rows[i])rec(i+1,add(s,a))}rec(0,[0n,0]);return c}
for(let z=0;z<200;z++){let n=2+rnd(6),rows=Array.from({length:n},()=>Array.from({length:2+rnd(2)},()=>[BigInt(rnd(17)-8),rnd(2)]));let target=z%2?rows.reduce((a,r)=>add(a,r[rnd(r.length)]),[0n,0]):[BigInt(rnd(41)-20),rnd(2)];let c=ref(rows,target),cl=close(rows,target),got=dp(cl,target);assert(c===got.count);stats.random++;if(c)stats.sat++;else stats.unsat++;
for(let i=0;i<n;i++)for(let j=0;j<rows[i].length;j++){let pin=rows.map((r,k)=>k===i?[r[j]]:r);assert(ref(pin,target)===dp(close(pin,target),target).count)}}
for(let n of [8,16,32,64,128]){let W=1n<<128n,rows=Array.from({length:n},()=>[[0n,0],[W,1]]),k=n/2;for(let t of [k%2,1-k%2]){let target=[BigInt(k)*W,t],cl=close(rows,target),got=dp(cl,target);let c=1n;for(let i=1;i<=k;i++)c=c*BigInt(n-i+1)/BigInt(i);assert(got.count===(t===k%2?c:0n));stats.scale.push({n,tag:t,sat:got.count>0n,peak:got.peak,count:got.count.toString()})}}
let hole=[[[0n,0],[3n,0]],[[0n,0],[5n,0]],[[0n,0],[6n,0]]];assert(inside(envelope(hole),[7n,0]));assert(dp(close(hole,[7n,0]),[7n,0]).count===0n);
return stats;
})(),null,2));
