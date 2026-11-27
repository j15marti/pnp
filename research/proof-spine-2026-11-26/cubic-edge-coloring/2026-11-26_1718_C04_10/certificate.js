// C04-10 independent finite verifier; run with Node.js.
function audit(){
const ok=x=>{if(!x)throw Error("certificate failed")};
const norm=w=>{let m=new Map();return w.map(x=>{if(!m.has(x))m.set(x,m.size+1);return m.get(x)}).join("")};
const words=new Set();for(let x=0;x<729;x++){let y=x,w=[];for(let i=0;i<6;i++){w.push(y%3+1);y=Math.floor(y/3)}if([1,2,3].every(c=>w.filter(z=>z===c).length%2===0))words.add(norm(w))}
const T=[...words].sort().map(w=>[...w].map(Number)),idx=new Map(T.map((w,i)=>[w.join(""),i])),ALL=2147483647;ok(T.length===31);
const bit=w=>1<<idx.get(norm(w));
function pairs(a){if(!a.length)return [[]];let out=[];for(let i=1;i<a.length;i++)for(const p of pairs(a.filter((_,j)=>j!==0&&j!==i)))out.push([[a[0],a[i]],...p]);return out}
function perms(a){if(!a.length)return [[]];return a.flatMap((x,i)=>perms(a.filter((_,j)=>i!==j)).map(p=>[x,...p]))}
function support(E,P){let e=[...E,...P.map((v,i)=>[v,-i-1])],used=new Map(),w=[],s=0;function dfs(i){if(i===e.length){s|=bit(w.slice(-6));return}let [u,v]=e[i],a=used.get(u)||0,b=used.get(v)||0;for(let c=1;c<=3;c++){let z=1<<c;if((a|b)&z)continue;used.set(u,a|z);used.set(v,b|z);w.push(c);dfs(i+1);w.pop();used.set(u,a);used.set(v,b)}}dfs(0);return s}
const base=[[[[24,25],[24,29],[25,26],[25,30],[26,31],[27,29],[27,30],[28,30],[28,31],[29,31],[0,26],[2,27]],[24,28,0,0,2,2],1596],[[[24,25],[24,29],[25,26],[25,30],[26,31],[27,29],[27,30],[28,30],[28,31],[29,31],[0,26],[12,24]],[27,28,0,12,0,12],1125123328],[[[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]],[0,1,2,3,4,5],1112802507],[[[0,1],[1,2],[2,3]],[0,0,1,2,3,3],31660032],[[[0,3],[1,3],[2,3]],[0,1,2,0,1,2],830636800],[[[0,1],[0,4],[1,2],[1,5],[2,3],[3,4]],[0,2,4,5,5,3],606712576]];
const P=perms([0,1,2,3,4,5]),caps=new Set();
for(const [e,p,s] of base){ok(support(e,p)===s);for(const q of P){let t=0;T.forEach((w,i)=>{if(s&(1<<i))t|=bit(q.map(j=>w[j]))});caps.add(t)}}
for(const p of pairs([0,1,2,3,4,5]))caps.add(T.reduce((s,w,i)=>p.every(([a,b])=>w[a]===w[b])?s|(1<<i):s,0));
ok(caps.size===415);let tests=0,maximum=0,positive=0;
for(const s of caps){let chosen=new Set();for(let i=0;i<31;i++){const b=1<<i;let t=[...caps].find(t=>s&b?(s&t)===b:!(s&t)&&Boolean(t&b));ok(t!==undefined);chosen.add(t);tests++;if(s&b)positive++}maximum=Math.max(maximum,chosen.size)}
const options=T.map(w=>[[1,2],[1,3],[2,3]].map(([a,b])=>pairs(w.map((c,i)=>c===a||c===b?i:-1).filter(i=>i>=0)).map(p=>{let m=0;for(let x=0;x<1<<p.length;x++){let v=w.slice();p.forEach(([i,j],k)=>{if(x&(1<<k)){v[i]=a+b-v[i];v[j]=a+b-v[j]}});m|=bit(v)}return m})));
function K(s){while(true){let t=s;options.forEach((row,i)=>{if((s&(1<<i))&&row.some(a=>!a.some(m=>(m&s)===m)))t&=~(1<<i)});if(t===s)return s;s=t}}
for(const s of caps){ok(K(s)===s);ok(K(ALL^s)===(ALL^s))}
const u=support([[0,4],[0,6],[1,3],[1,8],[2,5],[2,9],[3,6],[4,8],[4,9],[5,8],[6,7],[7,9]],[1,5,0,3,2,7]);
ok(u===1724704822&&K(ALL^u)===0&&!caps.has(u));ok([...caps].every(s=>s&u));
const gap=2090009856;ok(K(gap)===gap&&[...caps].every(s=>(s&gap)!==s));
ok(3n*415n*3n**31n<4n**31n);
return {types:T.length,caps:caps.size,bit_certificates:tests,positive,negative:tests-positive,max_distinct_probes:maximum,universal_cap:u,abstract_gap:gap};
}
console.log(JSON.stringify(audit(),null,2));
