function experiment(){
 const stats={seed:172024,random:0,sat:0,unsat:0,queries:0,transitions:0,pins:0,assertions:0,peak:0,width:0,scaling:[],adverse:[]};
 const check=(x)=>{stats.assertions++;if(!x)throw Error("assertion "+stats.assertions)};
 const bit=i=>1n<<BigInt(i), parity=x=>{let p=0;while(x){p^=1;x&=x-1n}return p};
 const hi=x=>x.toString(2).length-1;
 function reduce(x,b){while(x){const a=b.get(hi(x));if(a===undefined)break;x^=a}return x}
 function insert(x,b){x=reduce(x,b);if(x)b.set(hi(x),x);return !!x}
 const value=(a,z)=>parity(a[0]&z)^a[1];
 function compile(F,query){
  const events=[];for(const {terms,target} of F.quotas){
   let T=target, max=0n;const ts=terms.map(([w,a,c])=>{if(w<0n){T-=w;w=-w;c^=1}max+=w;return [w,a,c]});
   if(T<0n||T>max)return null;
   for(let j=0;j<Math.max(1,max.toString(2).length);j++){
    for(const [w,a,c] of ts)if(w&bit(j))events.push({k:"add",a,c});
    events.push({k:"end",v:Number((T>>BigInt(j))&1n)});
   }events.push({k:"zero"});
  }
  for(const [a,c,b,d,mask] of F.masks){events.push({k:"first",a,c});events.push({k:"second",a:b,c:d,mask})}
  for(const [a,c,v] of [...F.pins,...(query?[query]:[])])events.push({k:"pin",a,c,v});
  return events;
 }
 function plan(events){
  const basis=new Map(),deps=[],rows=[];
  for(const e of events)if(e.a!==undefined){e.i=rows.length;rows.push(e);let x=e.a,q=bit(e.i);while(x&&basis.has(hi(x))){const [a,b]=basis.get(hi(x));x^=a;q^=b}if(x)basis.set(hi(x),[x,q]);else deps.push(q)}
  const P=rows.map((_,i)=>{let p=0n;deps.forEach((v,j)=>{if(v&bit(i))p|=bit(j)});return p});
  const suffix=[new Map()];for(let i=P.length-1;i>=0;i--){const b=new Map(suffix[0]);insert(P[i],b);suffix.unshift(b)}
  const pre=new Map();let width=0;for(let i=0;i<=P.length;i++){width=Math.max(width,pre.size+suffix[i].size-deps.length);if(i<P.length)insert(P[i],pre)}
  return {rows,P,suffix,rank:basis.size,width};
 }
 function solve(F,query=null,onlyPlan=false){
  const events=compile(F,query);if(!events)return {count:0n,width:0,peak:0};const {rows,P,suffix,rank,width}=plan(events);
  if(onlyPlan)return {width};
  stats.queries++;stats.width=Math.max(stats.width,width);
  let states=new Map([["0,0,0",{p:0n,c:0,m:0,n:1n,obs:0n}]]),peak=1;
  for(const e of events){const next=new Map();
   for(const s of states.values())for(const b of e.a===undefined?[0]:[0,1]){
    stats.transitions++;let {p,c,m,obs}=s;
    if(e.a!==undefined){if(b^e.c)p^=P[e.i];if(reduce(p,suffix[e.i+1]))continue;if(b)obs|=bit(e.i)}
    if(e.k==="add")c+=b;
    if(e.k==="end"){if((c&1)!==e.v)continue;c=Math.floor(c/2)}
    if(e.k==="zero"&&c!==0)continue;
    if(e.k==="first")m=b;
    if(e.k==="second"){if(!(e.mask&(1<<(2*m+b))))continue;m=0}
    if(e.k==="pin"&&b!==e.v)continue;
    const key=[p,c,m].join(","),old=next.get(key);
    if(old)old.n+=s.n;else next.set(key,{p,c,m,n:s.n,obs});
   }states=next;peak=Math.max(peak,states.size);if(!states.size)break;
  }
  stats.peak=Math.max(stats.peak,peak);
  if(!states.size)return {count:0n,width,peak};
  const s=states.get("0,0,0");check(states.size===1&&!!s);
  // Lift one actual observation word by triangular elimination, free coordinates zero.
  const b=new Map();
  for(const e of rows){let a=e.a,v=Number((s.obs>>BigInt(e.i))&1n)^e.c;while(a&&b.has(hi(a))){const [aa,vv]=b.get(hi(a));a^=aa;v^=vv}if(a)b.set(hi(a),[a,v]);else check(v===0)}
  let z=0n;for(const i of [...b.keys()].sort((a,b)=>a-b)){const [a,v]=b.get(i);if(parity(a&z)^v)z|=bit(i)}
  check(valid(F,z)&&(!query||value(query,z)===query[2]));
  return {count:s.n*bit(F.d-rank),z,width,peak};
 }
 function valid(F,z){return F.quotas.every(q=>q.terms.reduce((s,[w,a,c])=>s+w*BigInt(value([a,c],z)),0n)===q.target)&&F.masks.every(([a,c,b,d,m])=>!!(m&(1<<(2*value([a,c],z)+value([b,d],z)))))&&F.pins.every(([a,c,v])=>value([a,c],z)===v)}
 function closure(F,root,forms){if(!root.count)return [];const done=new Map();let again=true;while(again){again=false;for(const a of forms){if(done.has(a))continue;const n=solve(F,[a,0,0]).count;check(n>=0n&&n<=root.count);if(n===0n||n===root.count){done.set(a,n===0n?1:0);stats.pins++;again=true;break}}}return [...done]}
 let seed=stats.seed;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 for(let j=0;j<80;j++){
  const d=3+rnd(4),z=BigInt(rnd(1<<d)),forms=Array.from({length:d+2},()=>[BigInt(rnd(1<<d)),rnd(2)]);
  const quotas=Array.from({length:1+j%2},()=>{const terms=forms.map(([a,c])=>[BigInt(rnd(19)-9),a,c]);return {terms,target:terms.reduce((s,[w,a,c])=>s+w*BigInt(value([a,c],z)),0n)}});
  const masks=Array.from({length:2},()=>{const [a,c]=forms[rnd(forms.length)],[b,e]=forms[rnd(forms.length)];let m=1+rnd(15);m|=1<<(2*value([a,c],z)+value([b,e],z));return [a,c,b,e,m]});
  const pins=[[BigInt(rnd(1<<d)),rnd(2),0]];pins[0][2]=value(pins[0],z);
  if(j%2)quotas[0].target+=BigInt(1+rnd(6));
  const F={d,quotas,masks,pins},ref=[];for(let x=0n;x<bit(d);x++)if(valid(F,x))ref.push(x);
  const r=solve(F);check(r.count===BigInt(ref.length));stats.random++;if(r.count)stats.sat++;else stats.unsat++;
  // All nonzero linear forms for small controls: full affine forced-predicate audit.
  const fs=Array.from({length:(1<<d)-1},(_,i)=>BigInt(i+1)),p=closure(F,r,fs);
  if(r.count){const expected=fs.filter(a=>ref.every(x=>parity(a&x)===parity(a&ref[0])));check(p.length===expected.length);for(const [a,v] of p)check(ref.every(x=>parity(a&x)===v))}
 }
 for(const n of [8,32,64,128]){
  const terms=Array.from({length:n},(_,i)=>[bit(i),bit(i),0]);
  const target=bit(n-1)+3n;
  const F={d:n+1,quotas:[{terms,target}],masks:[],pins:[[3n,0,0]]};
  for(const v of [0,1]){F.pins[0][2]=v;const r=solve(F);check(r.count===(v===0?2n:0n));const f=closure(F,r,[1n,2n,3n,bit(n)]);check(f.length===(v===0?3:0));stats.scaling.push({n,pin:v,count:String(r.count),width:r.width,peak:r.peak,registeredForced:f.length})}
 }
 for(const n of [4,8,16,32]){
  const terms=Array.from({length:n},(_,i)=>[1n+bit(i+1),bit(i),0]);const F={d:n,quotas:[{terms,target:3n}],masks:[],pins:[]};
  const r=solve(F,null,true);check(r.width===n);stats.adverse.push({n,width:r.width});
 }
 return stats;
}
console.log(JSON.stringify(experiment(),null,2));
