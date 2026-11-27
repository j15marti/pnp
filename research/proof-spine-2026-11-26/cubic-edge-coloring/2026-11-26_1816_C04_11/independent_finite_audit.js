function audit(){
const assert=(x)=>{if(!x)throw Error("audit failed")};
const norm=w=>{const m=new Map();return w.map(x=>{if(!m.has(x))m.set(x,m.size+1);return m.get(x)}).join("")};
const words=new Set();for(let a=0;a<729;a++){let q=a,w=[];for(let j=0;j<6;j++){w.push(q%3+1);q=Math.floor(q/3)}if([1,2,3].every(c=>w.filter(x=>x===c).length%2===0))words.add(norm(w))}
const T=[...words].sort().map(w=>[...w].map(Number)),ALL=2147483647,bit=w=>1<<T.findIndex(t=>t.join("")===norm(w));assert(T.length===31);
function pair(a){if(!a.length)return [[]];return a.slice(1).flatMap((v,i)=>pair(a.filter((_,j)=>j!==0&&j!==i+1)).map(p=>[[a[0],v],...p]))}
function perm(a){if(!a.length)return [[]];return a.flatMap((v,i)=>perm(a.filter((_,j)=>i!==j)).map(p=>[v,...p]))}
function support(e,p){const E=[...e,...p.map((v,i)=>[v,-1-i])],used=new Map(),w=[];let s=0,count=0;function dfs(i){if(i===E.length){s|=bit(w.slice(-6));count++;return}const [u,v]=E[i],a=used.get(u)||0,b=used.get(v)||0;for(let c=1;c<=3;c++){const z=1<<c;if((a|b)&z)continue;used.set(u,a|z);used.set(v,b|z);w.push(c);dfs(i+1);w.pop();used.set(u,a);used.set(v,b)}}dfs(0);return {s,count}}
const opt=T.map(w=>[[1,2],[1,3],[2,3]].map(([a,b])=>pair(w.flatMap((c,i)=>c===a||c===b?[i]:[])).map(p=>{let m=0;for(let k=0;k<1<<p.length;k++){let z=w.slice();p.forEach(([i,j],l)=>{if(k&(1<<l)){z[i]=a+b-z[i];z[j]=a+b-z[j]}});m|=bit(z)}return m})));
function K(s){for(;;){let t=s;opt.forEach((row,i)=>{if((s&(1<<i))&&row.some(ch=>!ch.some(m=>(m&s)===m)))t&=~(1<<i)});if(t===s)return s;s=t}}
const base=[[[[24,25],[24,29],[25,26],[25,30],[26,31],[27,29],[27,30],[28,30],[28,31],[29,31],[0,26],[2,27]],[24,28,0,0,2,2],1596],[[[24,25],[24,29],[25,26],[25,30],[26,31],[27,29],[27,30],[28,30],[28,31],[29,31],[0,26],[12,24]],[27,28,0,12,0,12],1125123328],[[[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]],[0,1,2,3,4,5],1112802507],[[[0,1],[1,2],[2,3]],[0,0,1,2,3,3],31660032],[[[0,3],[1,3],[2,3]],[0,1,2,0,1,2],830636800],[[[0,1],[0,4],[1,2],[1,5],[2,3],[3,4]],[0,2,4,5,5,3],606712576]];
const caps=new Map();for(const [e,p,s] of base){assert(support(e,p).s===s);for(const q of perm([0,1,2,3,4,5])){let t=0;T.forEach((w,i)=>{if(s&(1<<i))t|=bit(q.map(j=>w[j]))});if(!caps.has(t))caps.set(t,{e,p:q.map(j=>p[j])})}}
for(const p of pair([0,1,2,3,4,5])){let s=0;T.forEach((w,i)=>{if(p.every(([a,b])=>w[a]===w[b]))s|=1<<i});caps.set(s,{wire:p})}assert(caps.size===415);
const E=[[0,4],[1,4],[0,5],[2,5],[0,6],[3,6],[1,7],[2,7],[1,8],[3,8],[2,9],[3,9]],P=[4,5,6,7,8,9],s=support(E,P);assert(s.s===1066632960&&s.count===120);
function match(v){if(!v.length)return true;let x=v[0];return E.some(([a,b])=>{const y=a===x?b:b===x?a:-1;return y>=0&&v.includes(y)&&match(v.filter(t=>t!==x&&t!==y))})}
let H=ALL,pairsFeasible=0;for(let j=0;j<64;j++){const selected=P.filter((_,i)=>j&(1<<i));if(selected.length%2)continue;const yes=match(Array.from({length:10},(_,i)=>i).filter(x=>!selected.includes(x)));if(yes&&selected.length===2)pairsFeasible++;if(!yes)T.forEach((w,i)=>{if([1,2,3].some(c=>w.reduce((m,x,k)=>x===c?m|(1<<k):m,0)===j))H&=~(1<<i)})}
assert(pairsFeasible===15&&H===2140374784&&K(H)===H);
const probe=[...caps.keys()].filter(t=>!(t&s.s)&&(t&H)).sort((a,b)=>a-b)[0];assert(probe!==undefined&&K(H&~probe)===s.s);const cap=caps.get(probe);let closed;
if(cap.wire)closed=E.concat(cap.wire.map(([a,b])=>[P[a],P[b]]));else closed=E.concat(cap.e.map(([a,b])=>[a+100,b+100]),cap.p.map((v,i)=>[P[i],v+100]));
function colorable(e){if(e.some(([a,b])=>a===b))return false;const used=new Map();function go(i){if(i===e.length)return true;const [u,v]=e[i],a=used.get(u)||0,b=used.get(v)||0;for(let c=1;c<=3;c++){const z=1<<c;if((a|b)&z)continue;used.set(u,a|z);used.set(v,b|z);if(go(i+1))return true;used.set(u,a);used.set(v,b)}return false}return go(0)}assert(!colorable(closed));
const universal=support([[0,4],[0,6],[1,3],[1,8],[2,5],[2,9],[3,6],[4,8],[4,9],[5,8],[6,7],[7,9]],[1,5,0,3,2,7]);assert(universal.s===1724704822&&K(ALL^universal.s)===0);
const gap=2090009856;let closedMasks=[];for(let t=gap;t;t=(t-1)&gap){if(K(t)===t)closedMasks.push(t)}assert(closedMasks.length===2&&closedMasks.includes(1553138944));
assert(3n*31n*3n**19n<4n**19n);
return {cap_count:caps.size,hostile:s,matching_upper:H,pairsFeasible,probe,cap,closed_edges:closed,closed_colorable:false,universal:universal.s,abstract_closed_masks:closedMasks};
}
console.log(JSON.stringify(audit(),null,2));
