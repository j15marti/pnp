function experiment(){
let seed=20261124;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;}
const sum=(a)=>a.reduce((x,y)=>x+y,0);
const stats={seed:20261124,random:{cases:0,sat:0,unsat:0,referenceTuples:0,verifiedWitnesses:0,pinCases:0,pinSat:0,pinUnsat:0},scaling:[],hostile:[]};
function verify(rows,K,t,x){if(!x||x.length!==rows.length)return false;const c=K.map(()=>0);let tag=0;for(let i=0;i<x.length;i++){const r=rows[i][x[i]];if(!r)return false;for(let j=0;j<K.length;j++)c[j]+=r.c[j];tag^=r.t;}return c.every((v,j)=>v<=K[j])&&tag===t;}
function brute(rows,K,t){let first=null;const supports=rows.map(rs=>rs.map(()=>false));const x=[];function rec(i){if(i===rows.length){stats.random.referenceTuples++;if(verify(rows,K,t,x)){if(!first)first=x.slice();x.forEach((v,j)=>supports[j][v]=true);}return;}for(let j=0;j<rows[i].length;j++){x[i]=j;rec(i+1);}}rec(0);return {first,supports};}
function solve(rows,K,t,d,pin=null){
 const H=K.length, B=rows.length, metrics={closureScans:0,deletions:0,countVectors:0,flowCalls:0,augmentations:0,groups:0,good:0,misaligned:0};const ids=rows.map((r,i)=>r.map((_,j)=>j).filter(j=>!pin||i!==pin[0]||j===pin[1]));
 const fail=()=>({x:null,metrics});
 // Certified affordability and all-ones price closure, restart on each deletion.
 let mins,base,Hr;
 while(true){metrics.closureScans++;if(ids.some(a=>!a.length))return fail();mins=ids.map((js,i)=>K.map((_,h)=>Math.min(...js.map(j=>rows[i][j].c[h]))));base=K.map((_,h)=>sum(mins.map(v=>v[h])));Hr=K.map((v,h)=>v-base[h]);if(Hr.some(v=>v<0))return fail();
 const pm=ids.map((js,i)=>Math.min(...js.map(j=>sum(rows[i][j].c))));const gap=sum(K)-sum(pm);if(gap<0)return fail();
 let changed=false;outer:for(let i=0;i<B;i++)for(const j of ids[i]){if(rows[i][j].c.some((v,h)=>v-mins[i][h]>Hr[h])||sum(rows[i][j].c)-pm[i]>gap){ids[i]=ids[i].filter(k=>k!==j);metrics.deletions++;changed=true;break outer;}}
 if(!changed)break;
 }
 let target=t;const good=[],groups=new Map(),off=Hr.slice(),active=new Set();
 for(let i=0;i<B;i++){
 const a=ids[i].map(j=>({id:j,c:rows[i][j].c.map((v,h)=>v-mins[i][h]),t:rows[i][j].t}));
 const owner=r=>{const nz=r.c.map((v,h)=>v?h:-1).filter(h=>h>=0);return nz.length===0?H:nz.length===1&&r.c[nz[0]]===d[nz[0]]?nz[0]:-1;};
 if(a.every(r=>r.t===a[0].t&&owner(r)>=0)){target^=a[0].t;const opts=a.map(r=>({id:r.id,o:owner(r)}));opts.forEach(r=>{if(r.o<H)active.add(r.o)});good.push({i,opts});}
 else {if(a.length!==2)throw Error("nonbinary exceptional");target^=a[0].t;for(let h=0;h<H;h++)off[h]-=a[0].c[h];const diff=a[1].c.map((v,h)=>v-a[0].c[h]),tag=a[0].t^a[1].t,key=JSON.stringify([diff,tag]);if(!groups.has(key))groups.set(key,{diff,tag,members:[]});groups.get(key).members.push({i,ids:a.map(r=>r.id)});}
 }
 const gs=[...groups.values()];metrics.groups=gs.length;metrics.good=good.length;metrics.misaligned=[...active].filter(h=>gs.some(g=>g.diff[h]%d[h]!==0)).length;
 function flow(cap){metrics.flowCalls++;const slots=Array.from({length:H+1},()=>[]),picked=new Array(good.length);
 function aug(b,seen){for(const opt of good[b].opts){let o=opt.o;if(seen.has(o))continue;seen.add(o);if(slots[o].length<cap[o]){slots[o].push(b);picked[b]=opt.id;return true;}for(let k=0;k<slots[o].length;k++){const old=slots[o][k];if(aug(old,seen)){slots[o][k]=b;picked[b]=opt.id;return true;}}}return false;}
 for(let b=0;b<good.length;b++){if(!aug(b,new Set()))return null;metrics.augmentations++;}return picked;}
 let found=null,counts=[];function rec(j,rem,tag){if(j===gs.length){metrics.countVectors++;if(tag!==target||rem.some(v=>v<0))return;const cap=rem.map((v,h)=>Math.min(good.length,Math.floor(v/d[h])));cap.push(good.length); // dummy capacity only matters when some block has a dummy choice
 const hasDummy=good.some(b=>b.opts.some(r=>r.o===H));if(!hasDummy&&sum(cap.slice(0,H))<good.length)return;
 const p=flow(cap);if(!p)return;const x=new Array(B);good.forEach((g,b)=>x[g.i]=p[b]);gs.forEach((g,k)=>g.members.forEach((m,a)=>x[m.i]=m.ids[+(a<counts[k])]));if(!verify(rows,K,t,x)||pin&&x[pin[0]]!==pin[1])throw Error("bad witness");found=x;return;}
 const g=gs[j];for(let k=0;k<=g.members.length&&!found;k++){counts[j]=k;rec(j+1,rem.map((v,h)=>v-k*g.diff[h]),tag^((k%2)?g.tag:0));}}
 rec(0,off,0);return {x:found,metrics};
}
function make(H,B){const d=Array.from({length:H},()=>1+rnd(4));const rows=[];let templates=[];for(let j=0;j<2;j++){let a=rnd(H),b=(a+1+rnd(H-1))%H,w=2+rnd(6);let c0=Array(H).fill(0),c1=Array(H).fill(0);c0[a]=w;c1[b]=w+1;templates.push([{c:c0,t:rnd(4)},{c:c1,t:rnd(4)}]);}
for(let i=0;i<B;i++){const bas=Array.from({length:H},()=>rnd(3));let rs;if(i%3===0){rs=templates[rnd(2)].map(r=>({c:r.c.map((v,h)=>v+bas[h]),t:r.t}));}else {let n=2+rnd(2),tag=rnd(4);rs=Array.from({length:n},()=>{let o=rnd(H+1),c=bas.slice();if(o<H)c[o]+=d[o];return {c,t:tag};});}rows.push(rs);}
const K=Array(H).fill(0);let t=0;rows.forEach(rs=>{const r=rs[rnd(rs.length)];r.c.forEach((v,h)=>K[h]+=v);t^=r.t;});if(rnd(3)===0){const i=rnd(H);K[i]=Math.max(0,K[i]-1-rnd(5));}if(rnd(4)===0)t^=1+rnd(3);return {rows,K,t,d};}
for(let n=0;n<240;n++){const {rows,K,t,d}=make(2+rnd(3),3+rnd(5));const ref=brute(rows,K,t);const r=solve(rows,K,t,d);stats.random.cases++;stats.random[ref.first?"sat":"unsat"]++;if(!!r.x!==!!ref.first)throw Error("reference mismatch");if(r.x)stats.random.verifiedWitnesses++;
 // Exact row support probes on a subset of cases.
 if(n<60)for(let i=0;i<rows.length;i++)for(let j=0;j<rows[i].length;j++){let p=solve(rows,K,t,d,[i,j]);stats.random.pinCases++;stats.random[p.x?"pinSat":"pinUnsat"]++;if(!!p.x!==ref.supports[i][j])throw Error("pin mismatch");}}
for(let h of [2,4,8,16,24]){const H=h+4,M=4*h+2,d=Array(H).fill(M),rows=[],K=Array(H).fill(0);function add(a,b,w,sel){let c0=Array(H).fill(0),c1=c0.slice();c0[a]=w;c1[b]=w;rows.push([{c:c0,t:0},{c:c1,t:0}]);const c=sel?c1:c0;c.forEach((v,j)=>K[j]+=v);}
 for(let a=0;a<H;a++)for(let b=a+1;b<H;b++)add(a,b,M,(a+b)%2);
 for(let i=0;i<2*h;i++)add(0,1,2*M,1);for(let i=0;i<2*h;i++)add(0,1,2*M+1,0);
 const satK=K.slice(),unsatK=K.slice();unsatK[0]++;unsatK[1]--;satK[0]++; // SAT one-budget neighbor
 const u=solve(rows,unsatK,0,d),s=solve(rows,satK,0,d);if(u.x||!s.x)throw Error("scale mismatch");stats.scaling.push({h,owners:H,blocks:rows.length,good:rows.length-4*h,groups:2,rawAssignmentsLog2:rows.length,unsat:u.metrics,sat:s.metrics});}
 // Dropping floor on two unit-load owners permits a fake half-flow: one block, two costs 2, residual budgets 1 and 1.
 const rows=[[{c:[2,0],t:0},{c:[0,2],t:0}]];const r=solve(rows,[1,1],0,[2,2]);if(r.x)throw Error("fractional control");stats.hostile.push({name:"nonintegral capacity",fractionalFlow:[0.5,0.5],exactSAT:false,metrics:r.metrics});
 return stats;
}
console.log(JSON.stringify(experiment(), null, 2));
