function experiment(){
const L={gauss:0,xor:0,closure:0,deleted:0,pins:0,pair:0,candidates:0,localQueries:0,localWords:0,refWords:0,orderTests:0,verified:0};
const ok=(x,msg)=>{if(!x)throw Error(msg)};
const row=(i,b)=> (1n<<BigInt(i+1))|BigInt(b);
function canon(rows){L.gauss++;let a=[];for(let r of rows){for(let p of a){let bit=1n<<BigInt(p.toString(2).length-1);if(r&bit){r^=p;L.xor++}}if(r===1n)return null;if(r===0n)continue;let bit=1n<<BigInt(r.toString(2).length-1);a=a.map(p=>{if(p&bit){L.xor++;return p^r}return p});a.push(r);a.sort((u,v)=>u>v?-1:u<v?1:0)}return a}
function holds(rows,x){return rows.every(r=>{let a=(r>>1n)&x,b=Number(r&1n);while(a){b^=1;a&=a-1n}return !b})}
function close(n,G,E){G=canon(G);if(!G)return null;E=E.map((e,i)=>({i,rows:e.rows??e}));while(true){L.closure++;let next=[],change=false;for(const e of E){const H=canon([...G,...e.rows]);if(!H){L.deleted++;change=true;continue}if(H.length===G.length)return null;if(H.length===G.length+1){let r=e.rows.find(r=>{let C=canon([...G,r]);return C&&C.length>G.length});ok(r!==undefined,"pin");G=canon([...G,r^1n]);L.pins++;change=true;break}next.push(e)}if(change&&next.length!==E.length){if(next.length<E.length&&E.some(e=>{const H=canon([...G,...e.rows]);return H&&H.length===G.length+1})){} // restart from full list, retaining guard
 if(G===null)return null;
 // restart only if a pin was installed; otherwise all surviving entries were processed
 }
 // check if a codimension-one pin caused early exit: recompute entire list under new G
 let survivors=[];let restart=false;for(const e of E){let H=canon([...G,...e.rows]);if(!H)continue;if(H.length===G.length)return null;if(H.length===G.length+1){let r=e.rows.find(r=>{let C=canon([...G,r]);return C&&C.length>G.length});G=canon([...G,r^1n]);L.pins++;restart=true;break}survivors.push(e)}if(restart){E=survivors.concat(E.filter(e=>!survivors.includes(e)));continue}
 E=survivors;
 // delete contained events (including duplicate, retain lowest index)
 let drop=-1;outer:for(let i=0;i<E.length;i++){let A=canon([...G,...E[i].rows]);for(let j=0;j<E.length;j++)if(i!==j){let B=canon([...G,...E[j].rows]);if(A.length<B.length)continue;let C=canon([...A,...E[j].rows]);if(C&&C.length===A.length&&(A.length>B.length||i>j)){drop=i;break outer}}}if(drop>=0){E.splice(drop,1);L.deleted++;continue}return {G,E};}}
function setup(G,E){let H=E.map(e=>canon([...G,...e.rows])),adj=E.map(()=>[]);for(let i=0;i<E.length;i++)for(let j=i+1;j<E.length;j++){L.pair++;if(canon([...H[i],...E[j].rows])){adj[i].push(j);adj[j].push(i)}}return {H,adj}}
function planAt(E,D,i,S){L.candidates++;let J=D.adj[i].filter(j=>S.includes(j)),basis=D.H[i].slice(),obs=[];for(const j of J)for(let r of E[j].rows){let q=canon([...basis,r&~1n]); // rank only; inconsistent RHS can occur, use homogeneous bases instead
 if(!q){q=canon([...basis.map(x=>x&~1n),r&~1n])}
 if(q.length>basis.length){obs.push(r&~1n);basis=q}}
 return {i,J,obs,k:Math.min(J.length,obs.length)}}
function order(E,D){let S=E.map((_,i)=>i),out=[];while(S.length){let best=null;for(const i of S){let p=planAt(E,D,i,S);if(!best||p.k<best.k)best=p}out.push(best);S=S.filter(i=>i!==best.i)}return out}
function count(n,G0,E0,cap=20){let C=close(n,G0,E0);if(!C)return {z:0n,k:0,credit:0n};let {G,E}=C,D=setup(G,E),P=order(E,D),k=Math.max(0,...P.map(p=>p.k)),credit=P.reduce((s,p)=>s+(1n<<BigInt(p.k)),0n);if(k>cap)return {z:null,k,credit};let z=1n<<BigInt(n-G.length);for(const p of P){L.localQueries++;let total=0n;let H=D.H[p.i];if(p.J.length<=p.obs.length){for(let m=0;m<2**p.J.length;m++){L.localWords++;let rows=H.slice(),sgn=1n;for(let j=0;j<p.J.length;j++)if((m>>j)&1){rows.push(...E[p.J[j]].rows);sgn=-sgn}let R=canon(rows);if(R)total+=sgn*(1n<<BigInt(n-R.length))}}else{for(let m=0;m<2**p.obs.length;m++){L.localWords++;let R=canon([...H,...p.obs.map((r,j)=>r|BigInt((m>>j)&1))]);ok(R,"basis extension");if(!p.J.some(j=>canon([...R,...E[j].rows])!==null))total+=1n<<BigInt(n-R.length)}}ok(total>=0n,"negative");z-=total}ok(z>=0n,"count");return {z,k,credit}}
function brute(n,G,E){let z=0n;for(let x=0n;x<(1n<<BigInt(n));x++){L.refWords++;if(holds(G,x)&&!E.some(e=>holds(e,x)))z++}return z}
function lift(n,G,E){let r=count(n,G,E);if(!r.z)return false;let A=G.slice(),x=0n;for(let i=0;i<n;i++){let R=count(n,[...A,row(i,0)],E);let b=R.z>0n?0:1;A.push(row(i,b));if(b)x|=1n<<BigInt(i)}ok(holds(G,x)&&!E.some(e=>holds(e,x)),"lift");L.verified++;return true}
let seed=20807;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
let random={sat:0,unsat:0};for(let t=0;t<100;t++){let n=3+rnd(4),E=Array.from({length:1+rnd(7)},()=>Array.from({length:1+rnd(3)},()=>BigInt((1+rnd((1<<n)-1))*2+rnd(2)))),G=t%3===0?[BigInt((1+rnd((1<<n)-1))*2+rnd(2))]:[];let r=count(n,G,E);ok(r.z===brute(n,G,E),"random");random[r.z?"sat":"unsat"]++;if(r.z)lift(n,G,E)}
let cube=Array.from({length:8},(_,i)=>[0,1,2].map(j=>row(j,(i>>j)&1)));let cubes={sat:0,unsat:0};for(let m=0;m<256;m++){let E=cube.filter((_,j)=>(m>>j)&1);let r=count(3,[],E);ok(r.z===BigInt(8-E.length),"cube");cubes[r.z?"sat":"unsat"]++}
let lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],fano=lines.flatMap(e=>[0,1].map(b=>e.map(i=>row(i,b))));let fc=[];for(let j=-1;j<14;j++){let E=fano.filter((_,i)=>i!==j),r=count(7,[],E);ok(r.z===brute(7,[],E),"fano");fc.push(String(r.z))}
function opt(E,D,S){if(!S.length)return 0;let k=Infinity;for(let i of S)k=Math.min(k,Math.max(planAt(E,D,i,S).k,opt(E,D,S.filter(j=>j!==i))));return k}
for(let t=0;t<25;t++){let n=5,E=Array.from({length:5},(_,i)=>({i,rows:[row(rnd(n),rnd(2)),row(rnd(n),rnd(2))]}));let C=close(n,[],E);if(!C)continue;let D=setup(C.G,C.E),P=order(C.E,D);ok(Math.max(0,...P.map(p=>p.k))===opt(C.E,D,C.E.map((_,i)=>i)),"optimal");L.orderTests++}
function slotPath(s){let E=[];for(let a=0;a<(1<<s)-1;a++){let b=a+1,d=a^b,p=0;while(!(d&(1<<p)))p++;let R=[];for(let j=0;j<s;j++)if(j!==p){let m=(1<<j)|((d&(1<<j))?(1<<p):0);let v=((a>>j)&1)^((d&(1<<j))?((a>>p)&1):0);R.push(BigInt(m*2+v))}for(let u=0;u<4;u++)E.push([...R,row(s,u&1),row(s+1,u>>1)])}return E}
let scaling=[];for(let s=2;s<=4;s++){let E=slotPath(s),a=count(s+2,[],E),b=count(s+2,[],E.slice(1));ok(a.z===0n&&b.z===1n,"slot path");scaling.push({slots:1<<s,events:E.length,k:a.k,credit:String(a.credit),neighborK:b.k,neighborCredit:String(b.credit)})}
let barrier=[];for(let m of [3,6,10,16]){let n=2*m+1,E=Array.from({length:m},(_,i)=>[row(0,0),row(2*i+1,0),row(2*i+2,0)]),r=count(n,[],E,0);ok(r.k===m-1,"barrier");barrier.push({m,k:r.k,credit:String(r.credit),trueCount:String((1n<<BigInt(2*m))+3n**BigInt(m))})}
return {random,cubes,fano:fc,scaling,barrier,ledger:L};
}
console.log(JSON.stringify(experiment(),null,2));
