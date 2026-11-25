// NAE4A6, bounded hitting-set transition audit. Node.js, no dependencies.
'use strict';
let seed=20261125, assertions=0;
const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const check=x=>{assertions++;if(!x)throw Error('assertion '+assertions)};
const bit=(w,i)=>(w>>i)&1;
function valid(x,owners,pins){return pins.every(([v,c])=>x[v]===c)&&owners.every(([v,...a])=>a.some(w=>x[w]===x[v]))}
function brute(n,owners,pins){for(let w=0;w<2**n;w++){let x=Array.from({length:n},(_,i)=>bit(w,i));if(valid(x,owners,pins))return x}return null}
// Exact local domain closure over suffix, with explicit original and pending guards.
function close(n,by,pin,i,pending){let dom=Array(n).fill(3);const set=(v,c)=>{dom[v]&=1<<c;return dom[v]!==0};for(let v=i;v<n;v++)if(pin[v]>=0&&!set(v,pin[v]))return null;for(let [v,c] of pending)if(!set(v,c))return null;let changed=true;while(changed){changed=false;for(let v=i;v<n;v++)for(let a of by[v]){let vs=[...new Set([v,...a])],support=Array(vs.length).fill(0);for(let w=0;w<2**vs.length;w++){if(!vs.every((u,k)=>dom[u]&(1<<bit(w,k))))continue;let c=bit(w,vs.indexOf(v));if(!a.some(u=>bit(w,vs.indexOf(u))===c))continue;vs.forEach((u,k)=>support[k]|=1<<bit(w,k));}for(let k=0;k<vs.length;k++){let u=vs[k],d=dom[u]&support[k];if(!d)return null;if(d!==dom[u]){dom[u]=d;changed=true}}}}return dom}
function solve(n,owners,pins,cap=n,dominance=true){
 let by=Array.from({length:n},()=>[]),pin=Array(n).fill(-1),stats={states:0,peak:0,attempts:0,closures:0,overflow:0,dominance:0};for(let [v,...a] of owners){if(!a.length||a.some(w=>w<=v||w>=n))throw Error('non-DAG');by[v].push([...new Set(a)]);}
 for(let [v,c] of pins){if(pin[v]>=0&&pin[v]!==c)return {status:'UNSAT',stats};pin[v]=c;}
 let root={mark:new Map(),prev:null,v:-1,c:-1};let layer=[root];
 for(let i=0;i<n;i++){let next=new Map();
 const add=(mark,prev,c)=>{stats.attempts++;if(mark.size>cap){stats.overflow++;return}let key=[...mark].sort((a,b)=>a[0]-b[0]).map(p=>p.join(':')).join(',');if(!next.has(key))next.set(key,{mark,prev,v:i,c});};
 for(let state of layer){stats.states++;stats.closures++;let dom=close(n,by,pin,i,state.mark);if(!dom)continue;
 let fixed=state.mark.get(i);if(fixed===undefined&&pin[i]>=0)fixed=pin[i];let rest=new Map(state.mark);rest.delete(i);
 // Only genuinely unmarked, unpinned single-owner vertices can be deferred.
 if(fixed===undefined&&by[i].length<=1){add(rest,state,-1);continue;}
 for(let c=0;c<2;c++){if((fixed!==undefined&&fixed!==c)||!(dom[i]&(1<<c)))continue;
 let options=by[i];
 function choose(j,m){if(m.size>cap){stats.overflow++;return;}while(j<options.length&&options[j].some(w=>m.get(w)===c))j++;if(j===options.length){add(m,state,c);return;}for(let w of options[j]){if(!(dom[w]&(1<<c))||m.has(w))continue;let mm=new Map(m);mm.set(w,c);choose(j+1,mm)}}
 choose(0,rest);
 }}
 let arr=[...next.values()];
 // At a fixed layer weaker pending guards dominate stronger guards. Decision only.
 if(dominance){arr.sort((a,b)=>a.mark.size-b.mark.size);let keep=[];for(let q of arr){if(keep.some(p=>[...p.mark].every(([v,c])=>q.mark.get(v)===c))){stats.dominance++;continue}keep.push(q)}arr=keep;}
 layer=arr;stats.peak=Math.max(stats.peak,...layer.map(s=>s.mark.size),0);if(!layer.length)break;
 }
 if(!layer.length)return {status:stats.overflow?'UNKNOWN':'UNSAT',stats};
 let x=Array(n).fill(-1),s=layer[0];while(s.prev){x[s.v]=s.c;s=s.prev}
 for(let i=n-1;i>=0;i--)if(x[i]<0)x[i]=by[i].length?x[by[i][0][0]]:0;
 check(valid(x,owners,pins));return {status:'SAT',x,stats};
}
function plane(){let out=[];for(let j=0;j<3;j++)out.push([j,3+j,6+j]);for(let i=0;i<3;i++)out.push([3*i,3*i+1,3*i+2]);for(let j=0;j<3;j++){out.push([j,3+(j+1)%3,6+(j+2)%3]);out.push([j,3+(j+2)%3,6+(j+1)%3]);}return out}
function sourceControl(n,cs){ // distributed pinned source vertices, all clauses become four one-owner R constraints
 let owners=[],pins=[],base=4*cs.length;for(let k=0;k<cs.length;k++){let [a,b,c]=cs[k].map(v=>v+base),s=4*k,t=s+1,u=s+2,v=s+3;owners.push([s,a,u],[t,a,v],[u,b,c],[v,b,c]);pins.push([s,1],[t,0]);}
 let expected=0;for(let w=0;w<2**n;w++)if(cs.every(([a,b,c])=>bit(w,a)!==bit(w,b)||bit(w,b)!==bit(w,c)))expected++;
 let r=solve(n+base,owners,pins);check((r.status==='SAT')===(expected>0));if(r.x)check(cs.every(([a,b,c])=>new Set([r.x[a+base],r.x[b+base],r.x[c+base]]).size===2));return {sourceVars:n,clauses:cs.length,sourceSolutions:expected,status:r.status,stats:r.stats};
}
let controls=[sourceControl(9,plane()),sourceControl(9,plane().slice(1)),sourceControl(9,plane().slice(2)),sourceControl(3,[[0,1,2]])];
let jobs=0,sat=0,unsat=0,unknown=0,capSat=0,capUnsat=0,maxPeak=0,dominance=0;
for(let n=2;n<=10;n++)for(let job=0;job<110;job++){
 let owners=[];for(let v=0;v<n-1;v++)for(let k=0,m=rand(4);k<m;k++){let a=v+1+rand(n-v-1),b=v+1+rand(n-v-1);owners.push([v,a,b]);}
 let pins=[];for(let v=0;v<n;v++)if(rand(5)<2)pins.push([v,rand(2)]);
 let expected=brute(n,owners,pins),r=solve(n,owners,pins);check(r.status!=='UNKNOWN');check((r.status==='SAT')===!!expected);
 let b=solve(n,owners,pins,2);if(b.status==='UNKNOWN')unknown++;else{check((b.status==='SAT')===!!expected);if(b.status==='SAT')capSat++;else capUnsat++}
 if(expected)sat++;else unsat++;jobs++;maxPeak=Math.max(maxPeak,r.stats.peak);dominance+=r.stats.dominance;
}
// Rooted compiler-like selector obligations: first selector requires p simultaneous marks.
let width=[];for(let p=1;p<=9;p++){let owners=[],n=2*p+2;for(let j=0;j<p;j++){owners.push([0,2+2*j,3+2*j],[1,2+2*j,3+2*j]);}let pins=[[0,0],[1,1]],r=solve(n,owners,pins,p-1);check(r.status==='UNKNOWN');let exact=solve(n,owners,pins,n);check(exact.status==='SAT');check(exact.stats.peak>=p);width.push({p,cap:p-1,overflow:r.stats.overflow,peak:exact.stats.peak,rawFirstStates:2**p});}
console.log(JSON.stringify({seed:20261125,assertions,jobs,sat,unsat,unknown,capSat,capUnsat,maxPeak,dominance,controls,width}));